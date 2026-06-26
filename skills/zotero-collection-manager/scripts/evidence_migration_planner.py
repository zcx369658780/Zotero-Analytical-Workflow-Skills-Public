#!/usr/bin/env python3
"""Dry-run evidence-field migration planner for existing Obsidian notes.

This script never writes to the note vault. It scans existing paper notes,
infers conservative Stage 2 evidence fields from old frontmatter, and emits
YAML patch previews for a future human-reviewed migration.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
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
DEFAULT_ZOTERO_DB = Path(r"<zotero_data_dir>\\zotero.sqlite")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
ITEM_KEY_RE = re.compile(r"^[A-Z0-9]{8}$")
TARGET_FIELDS = {
    "evidence_level",
    "citation_eligible",
    "citation_status",
    "usable_for",
    "evidence_sources",
    "human_verified",
    "verification_notes",
    "migration",
}
RECOGNIZED_RAW_QUALITY = {
    "metadata_only",
    "online_abstract",
    "zotero_notes_or_annotations",
    "local_fulltext",
}


@dataclass
class NoteRecord:
    path: Path
    rel_path: str
    folder: str
    text: str
    frontmatter_text: str
    frontmatter: dict[str, Any]
    item_key: str
    raw_data_quality: str
    reading_stage: str


@dataclass
class ExcludedFile:
    rel_path: str
    reason: str


@dataclass
class PlannedPatch:
    rel_path: str
    folder: str
    item_key: str
    raw_data_quality: str
    reading_stage: str
    evidence_level: str
    citation_eligible: str
    patch_yaml: str
    diff_preview: str
    needs_human_verification_for_e3: bool = False
    manual_review_reasons: list[str] = field(default_factory=list)


def yaml_quote(value: Any) -> str:
    return json.dumps("" if value is None else str(value), ensure_ascii=False)


def yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def parse_frontmatter(text: str) -> tuple[str, dict[str, Any]] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    raw_frontmatter = match.group(1)
    parsed: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in raw_frontmatter.splitlines():
        line = raw_line.rstrip("\r")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith((" ", "\t")) and ":" in line:
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if value == "":
                parsed[key] = ""
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                parsed[key] = [] if not inner else [part.strip().strip("\"'") for part in inner.split(",")]
            else:
                parsed[key] = value.strip("\"'")
            current_key = key
        elif current_key and stripped.startswith("- "):
            if not isinstance(parsed.get(current_key), list):
                parsed[current_key] = []
            parsed[current_key].append(stripped[2:].strip("\"'"))
    return raw_frontmatter, parsed


def has_nested_zotero_item_key(text: str) -> bool:
    return bool(re.search(r"\nzotero:\s*\n(?:\s+.+\n)*?\s+item_key\s*:", text))


def nested_zotero_item_key(text: str) -> str:
    match = re.search(r"\nzotero:\s*\n(?:\s+.+\n)*?\s+item_key\s*:\s*[\"']?([A-Z0-9]{8})[\"']?", text)
    return match.group(1) if match else ""


def early_log_file_reason(path: Path) -> str | None:
    name = path.name.lower()
    if "processlog" in name or "_processlog_" in name or "进度记录" in path.name:
        return "process_log"
    if "deepreadlog" in name or "_deepreadlog_" in name or "二次精读记录" in path.name:
        return "deep_read_log"
    return None


def non_paper_file_reason(path: Path) -> str:
    name = path.name.lower()
    if "queue" in name or "reading_queue" in name:
        return "queue_or_reading_queue_file"
    if "index" in name or "索引" in path.name:
        return "index_file"
    if "support" in name:
        return "support_file"
    return "missing_or_invalid_item_key"


def detect_pdf_link(text: str, frontmatter: dict[str, Any]) -> bool:
    if "zotero://open-pdf" in text:
        return True
    for key in ("pdf_link", "pdf_uri", "zotero_pdf_uri"):
        if str(frontmatter.get(key, "")).strip():
            return True
    return False


def detect_zotero_annotation(text: str) -> bool:
    haystack = text.lower()
    return "annotation" in haystack or "批注" in text or "annotated" in haystack


def evidence_mapping(raw_data_quality: str, text: str) -> tuple[str, str, str, list[str], dict[str, bool], str]:
    sources = {
        "metadata": False,
        "online_abstract": False,
        "zotero_notes": False,
        "zotero_annotations": False,
        "fulltext_cache": False,
        "pdf_human_checked": False,
    }
    inference_note = ""
    if raw_data_quality == "metadata_only":
        sources["metadata"] = True
        return "E0", "false", "not_eligible", ["indexing", "triage", "reading_queue"], sources, inference_note
    if raw_data_quality == "online_abstract":
        sources["online_abstract"] = True
        return "E1", "false", "not_eligible", ["screening", "topic_clustering", "reading_queue"], sources, inference_note
    if raw_data_quality == "zotero_notes_or_annotations":
        if detect_zotero_annotation(text):
            sources["zotero_annotations"] = True
            inference_note = "zotero_annotations inferred from note text markers"
        else:
            sources["zotero_notes"] = True
            inference_note = "zotero_notes inferred from raw_data_quality; notes vs annotations not distinguishable"
        return (
            "E2",
            "candidate",
            "candidate_needs_human_verification",
            ["literature_map_candidate", "mechanism_candidate", "citation_candidate"],
            sources,
            inference_note,
        )
    if raw_data_quality == "local_fulltext":
        sources["fulltext_cache"] = True
        return (
            "E2",
            "candidate",
            "candidate_needs_human_verification",
            ["literature_map_candidate", "mechanism_candidate", "citation_candidate"],
            sources,
            inference_note,
        )
    raise ValueError(f"Unsupported raw_data_quality: {raw_data_quality}")


def build_patch_yaml(record: NoteRecord, planned_at: str, planned_by: str) -> tuple[str, str, bool]:
    level, citation_eligible, citation_status, usable_for, sources, inference_note = evidence_mapping(
        record.raw_data_quality,
        record.text,
    )
    needs_e3 = record.reading_stage == "二次精读"
    lines = [
        f"evidence_level: {yaml_quote(level)}",
        f"citation_eligible: {citation_eligible}",
        f"citation_status: {yaml_quote(citation_status)}",
        "usable_for:",
    ]
    lines.extend(f"  - {yaml_quote(value)}" for value in usable_for)
    lines.append("evidence_sources:")
    lines.extend(f"  {key}: {yaml_bool(value)}" for key, value in sources.items())
    lines.append("human_verified: false")
    lines.append(
        "verification_notes: "
        + yaml_quote("auto-migrated evidence fields from raw_data_quality; not human verified")
    )
    if needs_e3:
        lines.append("needs_human_verification_for_E3: true")
    lines.append("migration:")
    lines.append(f"  planned_by: {yaml_quote(planned_by)}")
    lines.append(f"  planned_at: {yaml_quote(planned_at)}")
    lines.append(f"  source_raw_data_quality: {yaml_quote(record.raw_data_quality)}")
    lines.append(f"  source_reading_stage: {yaml_quote(record.reading_stage)}")
    lines.append('  migration_stage: "Stage2C_dry_run"')
    lines.append('  write_status: "not_written"')
    if inference_note:
        lines.append(f"  evidence_source_note: {yaml_quote(inference_note)}")
    return "\n".join(lines) + "\n", level, citation_eligible


def make_frontmatter_diff(record: NoteRecord, patch_yaml: str, max_lines: int = 80) -> str:
    old = ["---", *record.frontmatter_text.splitlines(), "---"]
    new = ["---", *record.frontmatter_text.splitlines(), *patch_yaml.rstrip().splitlines(), "---"]
    diff_lines = list(
        difflib.unified_diff(
            old,
            new,
            fromfile=f"{record.rel_path} frontmatter",
            tofile=f"{record.rel_path} planned frontmatter",
            lineterm="",
        )
    )
    if len(diff_lines) > max_lines:
        return "\n".join(diff_lines[:max_lines]) + f"\n... truncated {len(diff_lines) - max_lines} diff lines"
    return "\n".join(diff_lines)


def scan_notes(note_root: Path) -> tuple[list[NoteRecord], list[ExcludedFile], Counter[str]]:
    records: list[NoteRecord] = []
    excluded: list[ExcludedFile] = []
    stats: Counter[str] = Counter()
    if not note_root.exists():
        raise FileNotFoundError(f"note root not found: {note_root}")
    for path in sorted(note_root.rglob("*.md")):
        rel_path = path.relative_to(note_root).as_posix()
        folder = rel_path.split("/")[0] if "/" in rel_path else "(root)"
        stats["total_md_scanned"] += 1
        log_reason = early_log_file_reason(path)
        if log_reason:
            excluded.append(ExcludedFile(rel_path, log_reason))
            stats[f"excluded_{log_reason}"] += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        parsed = parse_frontmatter(text)
        if parsed is None:
            excluded.append(ExcludedFile(rel_path, "frontmatter_parse_failed"))
            stats["excluded_frontmatter_parse_failed"] += 1
            continue
        frontmatter_text, frontmatter = parsed
        item_key = str(frontmatter.get("item_key") or "").strip()
        if not item_key and has_nested_zotero_item_key(text):
            item_key = nested_zotero_item_key(text)
        if not item_key or not ITEM_KEY_RE.fullmatch(item_key):
            reason = non_paper_file_reason(path)
            excluded.append(ExcludedFile(rel_path, reason))
            stats[f"excluded_{reason}"] += 1
            continue
        stats["item_key_paper_notes"] += 1
        present_target_fields = sorted(TARGET_FIELDS.intersection(frontmatter))
        if present_target_fields:
            excluded.append(ExcludedFile(rel_path, "already_has_evidence_fields:" + ",".join(present_target_fields)))
            stats["excluded_already_has_evidence_fields"] += 1
            continue
        raw_data_quality = str(frontmatter.get("raw_data_quality") or "").strip()
        if raw_data_quality not in RECOGNIZED_RAW_QUALITY:
            excluded.append(ExcludedFile(rel_path, "missing_or_unrecognized_raw_data_quality"))
            stats["excluded_missing_or_unrecognized_raw_data_quality"] += 1
            continue
        reading_stage = str(frontmatter.get("reading_stage") or "").strip()
        records.append(
            NoteRecord(
                path=path,
                rel_path=rel_path,
                folder=folder,
                text=text,
                frontmatter_text=frontmatter_text,
                frontmatter=frontmatter,
                item_key=item_key,
                raw_data_quality=raw_data_quality,
                reading_stage=reading_stage,
            )
        )
    stats["excluded_files"] = len(excluded)
    return records, excluded, stats


def verify_keys_read_only(records: list[NoteRecord], zotero_db: Path) -> dict[str, Any]:
    if not zotero_db.exists():
        return {"status": "skipped_missing_db", "found": 0, "missing": []}
    uri = "file:" + zotero_db.as_posix() + "?mode=ro&immutable=1"
    con = sqlite3.connect(uri, uri=True)
    try:
        cur = con.cursor()
        missing: list[str] = []
        found = 0
        for record in records:
            if cur.execute("select 1 from items where key=? limit 1", (record.item_key,)).fetchone():
                found += 1
            else:
                missing.append(record.item_key)
        return {"status": "checked_read_only", "found": found, "missing": sorted(set(missing))}
    finally:
        con.close()


def select_sample_patches(plans: list[PlannedPatch], max_preview: int) -> list[PlannedPatch]:
    selected: list[PlannedPatch] = []

    def add_matching(predicate: Any, count: int) -> None:
        for plan in plans:
            if len([p for p in selected if predicate(p)]) >= count:
                break
            if plan not in selected and predicate(plan):
                selected.append(plan)

    add_matching(lambda p: p.evidence_level == "E0", 3)
    add_matching(lambda p: p.evidence_level == "E1", 1)
    add_matching(lambda p: p.raw_data_quality == "zotero_notes_or_annotations", 3)
    add_matching(lambda p: p.raw_data_quality == "local_fulltext", 3)
    add_matching(lambda p: p.needs_human_verification_for_e3, 3)
    for folder in [
        "2019年9月 HANK模型",
        "2026年1月30日 申请基金",
        "2026年3月10日 因果推断",
        "2026年3月30日 URHANK",
        "2026年4月13日 SpartialHANK",
        "2026年5月27日 结构化ML",
        "未归类",
    ]:
        for plan in plans:
            if plan.folder == folder and plan not in selected:
                selected.append(plan)
                break
    for plan in plans:
        if len(selected) >= max_preview:
            break
        if plan not in selected:
            selected.append(plan)
    return selected[:max_preview]


def build_plans(records: list[NoteRecord], planned_at: str, planned_by: str) -> list[PlannedPatch]:
    plans: list[PlannedPatch] = []
    for record in records:
        patch_yaml, level, citation_eligible = build_patch_yaml(record, planned_at, planned_by)
        manual_reasons: list[str] = []
        if level == "E2":
            manual_reasons.append("E2_candidate_needs_human_verification")
        if record.reading_stage == "二次精读":
            manual_reasons.append("deep_read_not_E3_without_human_verification")
        if detect_pdf_link(record.text, record.frontmatter) and record.raw_data_quality == "metadata_only":
            manual_reasons.append("pdf_link_but_metadata_only")
        plans.append(
            PlannedPatch(
                rel_path=record.rel_path,
                folder=record.folder,
                item_key=record.item_key,
                raw_data_quality=record.raw_data_quality,
                reading_stage=record.reading_stage,
                evidence_level=level,
                citation_eligible=citation_eligible,
                patch_yaml=patch_yaml,
                diff_preview=make_frontmatter_diff(record, patch_yaml),
                needs_human_verification_for_e3=record.reading_stage == "二次精读",
                manual_review_reasons=manual_reasons,
            )
        )
    return plans


def compute_summary(
    records: list[NoteRecord],
    excluded: list[ExcludedFile],
    scan_stats: Counter[str],
    plans: list[PlannedPatch],
    zotero_check: dict[str, Any],
) -> dict[str, Any]:
    raw_dist = Counter(record.raw_data_quality for record in records)
    evidence_dist = Counter(plan.evidence_level for plan in plans)
    folder_dist: dict[str, Counter[str]] = defaultdict(Counter)
    manual_review_paths: set[str] = set()
    pdf_link_metadata_only = 0
    for record, plan in zip(records, plans):
        folder_dist[record.folder]["total"] += 1
        folder_dist[record.folder][plan.evidence_level] += 1
        folder_dist[record.folder][record.raw_data_quality] += 1
        if "pdf_link_but_metadata_only" in plan.manual_review_reasons:
            pdf_link_metadata_only += 1
        if plan.manual_review_reasons:
            manual_review_paths.add(plan.rel_path)
    excluded_reasons = Counter(item.reason.split(":", 1)[0] for item in excluded)
    return {
        "total_md_scanned": scan_stats["total_md_scanned"],
        "item_key_paper_notes": scan_stats["item_key_paper_notes"],
        "excluded_files": len(excluded),
        "eligible_for_automatic_additive_planning": len(plans),
        "E0_planned": evidence_dist["E0"],
        "E1_planned": evidence_dist["E1"],
        "E2_planned": evidence_dist["E2"],
        "unknown_excluded": scan_stats["excluded_missing_or_unrecognized_raw_data_quality"],
        "deep_read_planned_with_needs_human_verification_for_E3": sum(
            1 for plan in plans if plan.needs_human_verification_for_e3
        ),
        "files_with_pdf_link_but_metadata_only": pdf_link_metadata_only,
        "files_requiring_manual_review": len(manual_review_paths),
        "files_with_anomalies_excluded": len(excluded),
        "raw_data_quality_distribution": dict(raw_dist),
        "evidence_level_distribution": dict(evidence_dist),
        "excluded_reason_distribution": dict(excluded_reasons),
        "excluded_samples": [
            {"path": item.rel_path, "reason": item.reason}
            for item in excluded[:20]
        ],
        "folder_distribution": {folder: dict(counts) for folder, counts in sorted(folder_dist.items())},
        "zotero_check": zotero_check,
    }


def markdown_report(summary: dict[str, Any], samples: list[PlannedPatch], planned_at: str) -> str:
    lines = [
        "# Stage 2C Evidence Migration Dry-Run Plan",
        "",
        "## Verdict",
        "",
        "DRY_RUN_ONLY. No vault note was modified.",
        "",
        "## Run Metadata",
        "",
        f"- planned_at: `{planned_at}`",
        f"- total md scanned: {summary['total_md_scanned']}",
        f"- eligible for automatic additive planning: {summary['eligible_for_automatic_additive_planning']}",
        f"- excluded files: {summary['excluded_files']}",
        "",
        "## Planning Statistics",
        "",
        f"- E0 planned: {summary['E0_planned']}",
        f"- E1 planned: {summary['E1_planned']}",
        f"- E2 planned: {summary['E2_planned']}",
        f"- deep-read planned with needs_human_verification_for_E3: {summary['deep_read_planned_with_needs_human_verification_for_E3']}",
        f"- files with PDF link but metadata_only: {summary['files_with_pdf_link_but_metadata_only']}",
        f"- files requiring manual review: {summary['files_requiring_manual_review']}",
        "",
        "## Exclusion Summary",
        "",
    ]
    for reason, count in summary["excluded_reason_distribution"].items():
        lines.append(f"- {reason}: {count}")
    lines.extend(["", "## Sample Patch Previews", ""])
    for index, sample in enumerate(samples, 1):
        lines.extend(
            [
                f"### Sample {index}: `{sample.rel_path}`",
                "",
                f"- item_key: `{sample.item_key}`",
                f"- raw_data_quality: `{sample.raw_data_quality}`",
                f"- planned evidence_level: `{sample.evidence_level}`",
                f"- planned citation_eligible: `{sample.citation_eligible}`",
                "",
                "```diff",
                sample.diff_preview,
                "```",
                "",
            ]
        )
    lines.extend(
        [
            "## Machine-Readable Summary",
            "",
            "```json",
            json.dumps(summary, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def resolve_report_path(out_report: str) -> Path:
    requested = Path(out_report)
    if not requested.is_absolute():
        requested = REPO_ROOT / requested
    resolved = requested.resolve()
    repo_resolved = REPO_ROOT.resolve()
    if repo_resolved not in [resolved, *resolved.parents]:
        raise ValueError(f"--out-report must stay inside workflow repo: {repo_resolved}")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run evidence migration planner for existing Obsidian literature notes."
    )
    parser.add_argument("--note-root", type=Path, default=DEFAULT_NOTE_ROOT, help="Obsidian note root to scan.")
    parser.add_argument("--zotero-db", type=Path, default=DEFAULT_ZOTERO_DB, help="Optional Zotero SQLite DB for read-only key checks.")
    parser.add_argument("--skip-zotero-check", action="store_true", help="Skip read-only Zotero item-key verification.")
    parser.add_argument("--out-report", help="Optional Markdown report path. Must be inside this workflow repository.")
    parser.add_argument("--max-preview", type=int, default=20, help="Maximum sample patch previews to include.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON summary to stdout.")
    args = parser.parse_args()

    planned_at = datetime.now().isoformat(timespec="seconds")
    records, excluded, scan_stats = scan_notes(args.note_root)
    zotero_check = {"status": "skipped", "found": 0, "missing": []}
    if not args.skip_zotero_check:
        zotero_check = verify_keys_read_only(records, args.zotero_db)
    plans = build_plans(records, planned_at=planned_at, planned_by="evidence_migration_planner.py")
    summary = compute_summary(records, excluded, scan_stats, plans, zotero_check)
    samples = select_sample_patches(plans, max(0, args.max_preview))
    report = markdown_report(summary, samples, planned_at)

    if args.out_report:
        report_path = resolve_report_path(args.out_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        summary["out_report"] = str(report_path)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
