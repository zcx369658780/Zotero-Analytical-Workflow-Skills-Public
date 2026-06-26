#!/usr/bin/env python3
"""Sample-only executor for existing-note evidence field migration.

Default mode is dry-run. Real writes require explicit sample gates and are
intended for small, reviewed samples only. This script must not be used for
bulk vault migration without a separate authorization stage.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parents[2]
DEFAULT_NOTE_ROOT = Path(r"<note_root>")
DEFAULT_WORKFLOW_ROOT = REPO_ROOT
DEFAULT_VAULT_ROOT = Path(r"<vault_root>")
DEFAULT_ZOTERO_ROOT = Path(r"<zotero_data_dir>")
DEFAULT_MIGRATION_LOG_NAME = "_EvidenceMigrationLog_Stage2D.md"
MAX_WRITE_FILES = 20
ALLOWED_MIGRATION_STAGES = {
    "Stage2D_sample_executor",
    "Stage2E_sample_migration",
}
ALLOWED_WRITE_STATUSES = {
    "written",
    "written_sample",
}

sys.path.insert(0, str(THIS_DIR))

from evidence_migration_planner import (  # noqa: E402
    ExcludedFile,
    FRONTMATTER_RE,
    NoteRecord,
    PlannedPatch,
    build_plans,
    compute_summary,
    detect_pdf_link,
    scan_notes,
    select_sample_patches,
    verify_keys_read_only,
)
from safety_io import guarded_append_line, guarded_write_text, summarize_diff  # noqa: E402


@dataclass
class ExecutionResult:
    path: str
    item_key: str
    status: str
    action: str
    backup_path: str | None
    diff_summary: str


def is_relative_to_path(path: Path, parent: Path) -> bool:
    resolved = path.resolve()
    parent_resolved = parent.resolve()
    return parent_resolved == resolved or parent_resolved in resolved.parents


def resolve_report_path(out_report: str, workflow_root: Path) -> Path:
    requested = Path(out_report)
    if not requested.is_absolute():
        requested = workflow_root / requested
    resolved = requested.resolve()
    workflow_resolved = workflow_root.resolve()
    if not is_relative_to_path(resolved, workflow_resolved):
        raise ValueError(f"--out-report must stay inside workflow root: {workflow_resolved}")
    allowed_roots = [workflow_resolved / "reports", workflow_resolved / "docs"]
    if not any(is_relative_to_path(resolved, allowed_root) for allowed_root in allowed_roots):
        raise ValueError("--out-report must be under workflow-root reports/ or docs/")
    if is_relative_to_path(resolved, DEFAULT_VAULT_ROOT):
        raise ValueError("--out-report must not point to the vault root")
    return resolved


def validate_backup_root(backup_root: Path | None, note_root: Path) -> Path | None:
    if backup_root is None:
        return None
    resolved = backup_root.resolve()
    if is_relative_to_path(resolved, note_root):
        raise ValueError("--backup-root must not be inside --note-root")
    if is_relative_to_path(resolved, DEFAULT_ZOTERO_ROOT):
        raise ValueError("--backup-root must not be inside the Zotero data directory")
    if resolved.exists() and not resolved.is_dir():
        raise ValueError("--backup-root must be a directory path")
    return resolved


def centralized_backup_path(record: NoteRecord, note_root: Path, backup_root: Path | None) -> Path | None:
    if backup_root is None:
        return None
    note_root_resolved = note_root.resolve()
    try:
        relative_note_path = record.path.resolve().relative_to(note_root_resolved)
    except ValueError as exc:
        raise ValueError(f"record path is outside note root: {record.path}") from exc
    backup_relative_path = Path(note_root.name) / relative_note_path
    return (backup_root / backup_relative_path).with_name(f"{backup_relative_path.name}.bak")


def validate_centralized_backup_targets(
    records: list[NoteRecord],
    *,
    note_root: Path,
    backup_root: Path | None,
) -> dict[str, Path]:
    if backup_root is None:
        return {}
    backup_root_resolved = backup_root.resolve()
    planned: dict[str, Path] = {}
    collisions: list[Path] = []
    duplicate_targets: list[Path] = []
    blocked_parents: list[Path] = []

    for record in records:
        backup_path = centralized_backup_path(record, note_root, backup_root)
        if backup_path is None:
            continue
        resolved = backup_path.resolve()
        if not is_relative_to_path(resolved, backup_root_resolved):
            raise ValueError(f"planned backup path escapes backup root: {resolved}")
        if is_relative_to_path(resolved, note_root):
            raise ValueError(f"planned backup path must not be inside --note-root: {resolved}")
        if is_relative_to_path(resolved, DEFAULT_ZOTERO_ROOT):
            raise ValueError(f"planned backup path must not be inside the Zotero data directory: {resolved}")
        if resolved in planned.values():
            duplicate_targets.append(resolved)
        if resolved.exists():
            collisions.append(resolved)
        parent = resolved.parent
        while parent != backup_root_resolved and backup_root_resolved in parent.parents:
            if parent.exists() and not parent.is_dir():
                blocked_parents.append(parent)
                break
            parent = parent.parent
        planned[record.rel_path] = resolved

    if blocked_parents:
        sample = "\n".join(f"- {path}" for path in blocked_parents[:10])
        raise ValueError(
            "centralized backup parent path is not a directory\n"
            f"backup root: {backup_root_resolved}\n"
            f"planned target count: {len(planned)}\n"
            f"collision count: {len(blocked_parents)}\n"
            f"collision sample paths:\n{sample}\n"
            "Use a new backup root or remove the blocking file after review."
        )
    if duplicate_targets:
        sample = "\n".join(f"- {path}" for path in duplicate_targets[:10])
        raise ValueError(
            "centralized backup target collision within current batch\n"
            f"backup root: {backup_root_resolved}\n"
            f"planned target count: {len(planned)}\n"
            f"collision count: {len(duplicate_targets)}\n"
            f"collision sample paths:\n{sample}\n"
            "Use unique sample entries or check the planned batch list."
        )
    if collisions:
        sample = "\n".join(f"- {path}" for path in collisions[:10])
        raise ValueError(
            "centralized backup target already exists\n"
            f"backup root: {backup_root_resolved}\n"
            f"planned target count: {len(planned)}\n"
            f"collision count: {len(collisions)}\n"
            f"collision sample paths:\n{sample}\n"
            "Use a new backup root or check whether this batch was already migrated."
        )
    return planned


def resolve_migration_log_path(
    *,
    note_root: Path,
    migration_log: Path | None,
    migration_log_name: str | None,
) -> Path:
    if migration_log and migration_log_name:
        raise ValueError("use only one of --migration-log or --migration-log-name")
    if migration_log_name:
        if Path(migration_log_name).name != migration_log_name:
            raise ValueError("--migration-log-name must be a filename, not a path")
        requested = note_root / migration_log_name
    elif migration_log:
        requested = migration_log if migration_log.is_absolute() else note_root / migration_log
    else:
        requested = note_root / DEFAULT_MIGRATION_LOG_NAME
    resolved = requested.resolve()
    if not is_relative_to_path(resolved, note_root):
        raise ValueError("--migration-log must stay inside --note-root")
    if is_relative_to_path(resolved, DEFAULT_ZOTERO_ROOT):
        raise ValueError("--migration-log must not be inside the Zotero data directory")
    return resolved


def read_sample_list(path: Path) -> set[str]:
    values: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        values.add(line.replace("\\", "/"))
    return values


def select_execution_plans(
    plans: list[PlannedPatch],
    *,
    sample_list: Path | None,
    max_files: int | None,
) -> list[PlannedPatch]:
    selected = plans
    if sample_list:
        requested = read_sample_list(sample_list)
        selected = [
            plan
            for plan in selected
            if plan.item_key in requested or plan.rel_path in requested or str(Path(plan.rel_path)) in requested
        ]
    if max_files is not None:
        selected = selected[:max_files]
    return selected


def validate_write_gates(args: argparse.Namespace, selected_count: int) -> None:
    if not args.write:
        return
    if not args.sample_only:
        raise ValueError("--write requires --sample-only")
    if args.sample_list is None and args.max_files is None:
        raise ValueError("--write requires --sample-list or --max-files")
    if args.max_files is not None and args.max_files > MAX_WRITE_FILES:
        raise ValueError(f"--max-files may not exceed {MAX_WRITE_FILES} for sample writes")
    if selected_count > MAX_WRITE_FILES:
        raise ValueError(f"sample write would affect {selected_count} files; maximum is {MAX_WRITE_FILES}")
    if is_relative_to_path(args.note_root, DEFAULT_VAULT_ROOT) and not args.allow_vault_write:
        raise ValueError("writing to the vault root requires --allow-vault-write")
    if is_relative_to_path(args.migration_log_path, DEFAULT_VAULT_ROOT) and not args.allow_vault_write:
        raise ValueError("writing migration log under the vault root requires --allow-vault-write")


def patch_yaml_for_execution(
    record: NoteRecord,
    migrated_at: str,
    migrated_by: str,
    *,
    migration_stage: str,
    write_status: str,
) -> tuple[str, str, str]:
    planned = build_plans([record], planned_at=migrated_at, planned_by=migrated_by)[0]
    patch = planned.patch_yaml
    patch = patch.replace("planned_by:", "migrated_by:")
    patch = patch.replace("planned_at:", "migrated_at:")
    patch = patch.replace('migration_stage: "Stage2C_dry_run"', f'migration_stage: "{migration_stage}"')
    patch = patch.replace('write_status: "not_written"', f'write_status: "{write_status}"')
    return patch, planned.evidence_level, planned.citation_eligible


def frontmatter_bounds(text: str) -> tuple[int, int, str]:
    """Return old frontmatter text bounds and the exact suffix start.

    The suffix starts immediately after the closing delimiter line ending.
    Extra blank lines after the delimiter belong to the body suffix and are
    preserved exactly.
    """
    if text.startswith("---\r\n"):
        first_line_end = 5
        newline = "\r\n"
    elif text.startswith("---\n"):
        first_line_end = 4
        newline = "\n"
    else:
        raise ValueError("frontmatter opening delimiter not found")

    pos = first_line_end
    while pos < len(text):
        next_lf = text.find("\n", pos)
        if next_lf == -1:
            line = text[pos:]
            line_end = len(text)
            line_ending = ""
        else:
            line = text[pos : next_lf + 1]
            line_end = next_lf + 1
            line_ending = "\n"
        stripped = line.rstrip("\r\n")
        if stripped.strip() == "---":
            suffix_start = line_end
            return first_line_end, pos, text[suffix_start:]
        if not line_ending:
            break
        pos = line_end
    raise ValueError("frontmatter closing delimiter not found")


def frontmatter_with_patch(record: NoteRecord, patch_yaml: str, newline: str = "\n") -> str:
    return "---" + newline + record.frontmatter_text.rstrip() + newline + patch_yaml.rstrip() + newline + "---" + newline


def content_with_patched_frontmatter(record: NoteRecord, patch_yaml: str) -> str:
    try:
        _, _, suffix = frontmatter_bounds(record.text)
    except ValueError as exc:
        raise ValueError(f"frontmatter parse failed unexpectedly: {record.rel_path}")
    newline = "\r\n" if record.text.startswith("---\r\n") else "\n"
    return frontmatter_with_patch(record, patch_yaml, newline=newline) + suffix


def stage_label(migration_stage: str) -> str:
    if migration_stage == "Stage2E_sample_migration":
        return "Stage2E"
    return "Stage2D"


def diff_for_record(record: NoteRecord, new_text: str, migration_stage: str) -> str:
    return summarize_diff(
        record.text,
        new_text,
        fromfile=record.rel_path,
        tofile=f"{record.rel_path} ({stage_label(migration_stage)} planned)",
        max_lines=80,
    )


def execute_plans(
    records_by_path: dict[str, NoteRecord],
    selected_plans: list[PlannedPatch],
    *,
    write: bool,
    migrated_at: str,
    note_root: Path,
    backup_root: Path | None,
    migration_log_path: Path,
    migration_stage: str,
    write_status: str,
) -> list[ExecutionResult]:
    results: list[ExecutionResult] = []
    selected_records = [records_by_path[plan.rel_path] for plan in selected_plans]
    backup_targets: dict[str, Path] = {}
    if backup_root is not None:
        backup_targets = validate_centralized_backup_targets(
            selected_records,
            note_root=note_root,
            backup_root=backup_root,
        )
    for plan in selected_plans:
        record = records_by_path[plan.rel_path]
        patch_yaml, evidence_level, citation_eligible = patch_yaml_for_execution(
            record,
            migrated_at=migrated_at,
            migrated_by="evidence_migration_executor.py",
            migration_stage=migration_stage,
            write_status=write_status,
        )
        if evidence_level == "E3" or citation_eligible == "true":
            raise ValueError(f"unsafe generated patch for {record.rel_path}")
        new_text = content_with_patched_frontmatter(record, patch_yaml)
        if not write:
            results.append(
                ExecutionResult(
                    path=record.rel_path,
                    item_key=record.item_key,
                    status="planned_update",
                    action="plan",
                    backup_path=str(backup_targets[record.rel_path]) if record.rel_path in backup_targets else None,
                    diff_summary=diff_for_record(record, new_text, migration_stage),
                )
            )
            continue
        write_result = guarded_write_text(
            record.path,
            new_text,
            write=True,
            overwrite=True,
            backup=True,
            backup_path=backup_targets.get(record.rel_path),
            diff=True,
            create_parents=False,
        )
        results.append(
            ExecutionResult(
                path=record.rel_path,
                item_key=record.item_key,
                status=write_result.status,
                action=write_result.action,
                backup_path=write_result.backup_path,
                diff_summary=write_result.diff_summary,
            )
        )

    if write:
        for result in results:
            guarded_append_line(
                migration_log_path,
                f"- [{migrated_at}] | {result.status} | {result.item_key} | {result.path}\n",
                write=True,
                create_parents=False,
            )
    return results


def build_markdown_report(
    *,
    summary: dict[str, Any],
    results: list[ExecutionResult],
    excluded: list[ExcludedFile],
    write: bool,
    migrated_at: str,
) -> str:
    counts = Counter(result.status for result in results)
    report_stage = stage_label(str(summary.get("migration_stage", "Stage2D_sample_executor")))
    lines = [
        f"# {report_stage} Evidence Migration Executor Report",
        "",
        "## Verdict",
        "",
        "WRITE_SAMPLE_EXECUTED." if write else "DRY_RUN_ONLY.",
        "",
        "## Run Metadata",
        "",
        f"- migrated_at: `{migrated_at}`",
        f"- write: `{str(write).lower()}`",
        f"- selected files: {len(results)}",
        f"- total md scanned: {summary['total_md_scanned']}",
        f"- eligible plans: {summary['eligible_for_automatic_additive_planning']}",
        f"- excluded files: {summary['excluded_files']}",
        "",
        "## Result Counts",
        "",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"- {status}: {count}")
    lines.extend(["", "## Execution Results", ""])
    for result in results[:20]:
        lines.extend(
            [
                f"### `{result.path}`",
                "",
                f"- item_key: `{result.item_key}`",
                f"- status: `{result.status}`",
                f"- action: `{result.action}`",
                f"- backup_path: `{result.backup_path or ''}`",
                "",
                "```diff",
                result.diff_summary,
                "```",
                "",
            ]
        )
    lines.extend(["## Excluded Samples", ""])
    for item in excluded[:20]:
        lines.append(f"- `{item.rel_path}`: {item.reason}")
    lines.extend(
        [
            "",
            "## Machine-Readable Summary",
            "",
            "```json",
            json.dumps(
                {
                    "summary": summary,
                    "result_counts": dict(counts),
                    "results": [asdict(result) for result in results],
                    "write": write,
                    "migrated_at": migrated_at,
                },
                ensure_ascii=False,
                indent=2,
            ),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sample-only executor for existing-note evidence migration."
    )
    parser.add_argument("--note-root", type=Path, default=DEFAULT_NOTE_ROOT, help="Obsidian note root to scan.")
    parser.add_argument("--workflow-root", type=Path, default=DEFAULT_WORKFLOW_ROOT, help="Workflow repository root for reports.")
    parser.add_argument("--out-report", help="Optional report path under workflow-root reports/ or docs/.")
    parser.add_argument("--write", action="store_true", help="Actually update selected sample notes.")
    parser.add_argument("--sample-only", action="store_true", help="Required with --write; documents sample-only intent.")
    parser.add_argument("--sample-list", type=Path, help="Text file of item keys or relative note paths to include.")
    parser.add_argument("--max-files", type=int, help=f"Maximum selected files. For writes, must be <= {MAX_WRITE_FILES}.")
    parser.add_argument("--allow-vault-write", action="store_true", help="Required only for future writes under the vault root.")
    parser.add_argument(
        "--backup-root",
        type=Path,
        help="Optional centralized backup root. Existing non-empty roots are allowed only when current backup targets do not collide.",
    )
    parser.add_argument(
        "--central-backup-root",
        type=Path,
        dest="backup_root",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--migration-log",
        type=Path,
        help="Optional migration log path under --note-root. Defaults to _EvidenceMigrationLog_Stage2D.md.",
    )
    parser.add_argument(
        "--migration-log-name",
        help="Optional migration log filename under --note-root.",
    )
    parser.add_argument(
        "--migration-stage",
        choices=sorted(ALLOWED_MIGRATION_STAGES),
        default="Stage2D_sample_executor",
        help="Whitelisted migration stage to write in patch metadata.",
    )
    parser.add_argument(
        "--write-status",
        choices=sorted(ALLOWED_WRITE_STATUSES),
        default="written",
        help="Whitelisted write status to write in patch metadata.",
    )
    parser.add_argument(
        "--stage2e-sample",
        action="store_true",
        help="Shortcut for --migration-stage Stage2E_sample_migration --write-status written_sample.",
    )
    parser.add_argument("--skip-zotero-check", action="store_true", help="Skip read-only Zotero item-key verification.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary to stdout.")
    args = parser.parse_args()

    if args.max_files is not None and args.max_files < 1:
        raise ValueError("--max-files must be positive")
    if args.write and args.max_files is not None and args.max_files > MAX_WRITE_FILES:
        raise ValueError(f"--max-files may not exceed {MAX_WRITE_FILES} for sample writes")
    if args.stage2e_sample:
        args.migration_stage = "Stage2E_sample_migration"
        args.write_status = "written_sample"
    args.note_root = args.note_root.resolve()
    args.backup_root = validate_backup_root(args.backup_root, args.note_root)
    args.migration_log_path = resolve_migration_log_path(
        note_root=args.note_root,
        migration_log=args.migration_log,
        migration_log_name=args.migration_log_name,
    )

    migrated_at = datetime.now().isoformat(timespec="seconds")
    report_path: Path | None = None
    if args.out_report:
        report_path = resolve_report_path(args.out_report, args.workflow_root)
    records, excluded, scan_stats = scan_notes(args.note_root)
    zotero_check = {"status": "skipped", "found": 0, "missing": []}
    if not args.skip_zotero_check:
        zotero_check = verify_keys_read_only(records, Path(r"<zotero_data_dir>\\zotero.sqlite"))
    plans = build_plans(records, planned_at=migrated_at, planned_by="evidence_migration_executor.py")
    selected = select_execution_plans(plans, sample_list=args.sample_list, max_files=args.max_files)
    validate_write_gates(args, len(selected))
    records_by_path = {record.rel_path: record for record in records}
    results = execute_plans(
        records_by_path,
        selected,
        write=args.write,
        migrated_at=migrated_at,
        note_root=args.note_root,
        backup_root=args.backup_root,
        migration_log_path=args.migration_log_path,
        migration_stage=args.migration_stage,
        write_status=args.write_status,
    )
    summary = compute_summary(records, excluded, scan_stats, plans, zotero_check)
    summary["selected_files"] = len(selected)
    summary["write"] = args.write
    summary["sample_only"] = args.sample_only
    summary["allow_vault_write"] = args.allow_vault_write
    summary["backup_root"] = str(args.backup_root) if args.backup_root else None
    summary["migration_log_path"] = str(args.migration_log_path)
    summary["migration_stage"] = args.migration_stage
    summary["write_status"] = args.write_status
    summary["unsafe_E3_generated"] = any("evidence_level: E3" in result.diff_summary for result in results)
    summary["unsafe_citation_true_generated"] = any("citation_eligible: true" in result.diff_summary for result in results)

    report = build_markdown_report(
        summary=summary,
        results=results,
        excluded=excluded,
        write=args.write,
        migrated_at=migrated_at,
    )
    if args.out_report:
        assert report_path is not None
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        summary["out_report"] = str(report_path)

    payload = {
        "summary": summary,
        "result_counts": dict(Counter(result.status for result in results)),
        "results": [asdict(result) for result in results],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
