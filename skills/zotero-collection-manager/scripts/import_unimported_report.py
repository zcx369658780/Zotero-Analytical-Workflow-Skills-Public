#!/usr/bin/env python3
"""Import Zotero items listed in an unimported-items Markdown report.

The importer uses the report as the queue source, writes notes into directories
named after the first top-level Zotero collection listed for each item, and
deduplicates globally by Zotero parent item key.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
FETCHER_SCRIPTS = THIS_DIR.parents[1] / "zotero-data-fetcher" / "scripts"
sys.path.insert(0, str(FETCHER_SCRIPTS))
sys.path.insert(0, str(THIS_DIR))

from batch_import_collection import (  # noqa: E402
    append_log,
    make_note,
    sanitize_filename,
)
from zotero_collection_queue import ensure_log  # noqa: E402
from zotero_fetch import (  # noqa: E402
    add_online_supplements,
    assess_raw_data_quality,
    build_raw_buffer,
    default_data_dir,
    fetch_from_sqlite,
)
from safety_io import guarded_write_text  # noqa: E402


ITEM_KEY_RE = re.compile(r'^\s*item_key:\s*["\']?(?P<key>[A-Z0-9]{8})["\']?\s*$', re.M)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


def read_imported_keys(note_root: Path) -> set[str]:
    keys: set[str] = set()
    if not note_root.exists():
        return keys
    for path in note_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        keys.update(match.group("key") for match in ITEM_KEY_RE.finditer(text))
    return keys


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line:
        if escaped:
            current.append(char)
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    cells.append("".join(current).strip())
    return cells


def extract_section_lines(text: str, heading: str) -> list[str]:
    marker = f"## {heading}"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"Section not found: {marker}")
    next_heading = text.find("\n## ", start + len(marker))
    section = text[start:] if next_heading < 0 else text[start:next_heading]
    return section.splitlines()


def top_level_collection(collection_cell: str) -> str:
    first_path = (collection_cell or "未归类").split(";")[0].strip() or "未归类"
    return first_path.split(" / ")[0].strip() or "未归类"


def read_report_queue(report_path: Path) -> list[dict[str, str]]:
    text = report_path.read_text(encoding="utf-8")
    lines = extract_section_lines(text, "全部未录入条目")
    rows: list[dict[str, str]] = []
    for line in lines:
        if not line.startswith("|"):
            continue
        if line.startswith("|---") or line.startswith("| Key "):
            continue
        cells = split_markdown_row(line)
        if len(cells) < 8:
            continue
        key = cells[0].strip()
        if not re.fullmatch(r"[A-Z0-9]{8}", key):
            continue
        rows.append(
            {
                "key": key,
                "year": cells[1],
                "item_type": cells[2],
                "pdf_status": cells[3],
                "cache_status": cells[4],
                "title": cells[5],
                "creators": cells[6],
                "collections": cells[7],
                "target_collection": top_level_collection(cells[7]),
            }
        )
    return rows


def note_path_for(target_dir: Path, title: str, key: str, existing_key_paths: dict[str, Path]) -> Path:
    base = target_dir / sanitize_filename(title)
    if not base.exists():
        return base
    if existing_key_paths.get(key) == base:
        return base
    stem = base.stem[:120].rstrip()
    candidate = target_dir / f"{stem} - {key}.md"
    suffix = 2
    while candidate.exists() and existing_key_paths.get(key) != candidate:
        candidate = target_dir / f"{stem} - {key}-{suffix}.md"
        suffix += 1
    return candidate


def index_existing_key_paths(note_root: Path) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    if not note_root.exists():
        return paths
    for path in note_root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in ITEM_KEY_RE.finditer(text):
            paths.setdefault(match.group("key"), path)
    return paths


def import_one(
    *,
    data_dir: Path,
    note_root: Path,
    row: dict[str, str],
    online_email: str | None,
    skip_unpaywall: bool,
    no_online: bool,
    existing_key_paths: dict[str, Path],
    write: bool,
    overwrite: bool,
    backup: bool,
    diff: bool,
) -> dict[str, Any]:
    key = row["key"]
    collection = row["target_collection"]
    target_dir = note_root / collection
    log_file = target_dir / "_ProcessLog_进度记录.md"
    log_init = ensure_log(log_file, collection, write=write)

    payload = fetch_from_sqlite(data_dir, key, None)
    data = (payload.get("item") or {}).get("data") or {}
    title = html.unescape(data.get("title") or row.get("title") or key)
    quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
    if quality.get("needs_fulltext_for_deep_reading") and not no_online:
        payload = add_online_supplements(
            payload,
            email=online_email,
            skip_unpaywall=skip_unpaywall,
        )
        quality = payload.get("raw_data_quality") or quality
    else:
        payload["raw_data_quality"] = quality
        payload["raw_data_buffer"] = build_raw_buffer(payload)

    note_path = note_path_for(target_dir, title, key, existing_key_paths)
    write_result = guarded_write_text(
        note_path,
        make_note(payload, collection),
        write=write,
        overwrite=overwrite,
        backup=backup,
        diff=diff,
    )
    if write_result.status in {"created", "updated"}:
        append_log(log_file, "✅ 成功", key, title, write=write)
        existing_key_paths[key] = note_path
    elif write_result.status == "skipped_existing":
        append_log(log_file, "⚠️ 跳过", key, title, write=write)
    return {
        "key": key,
        "title": title,
        "target_collection": collection,
        "quality": (quality or {}).get("level", "unknown"),
        "path": str(note_path),
        "status": write_result.status,
        "log_init": log_init,
        "write_result": write_result.to_dict(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--note-root", type=Path, default=Path(r"<note_root>"))
    parser.add_argument("--online-email")
    parser.add_argument("--skip-unpaywall", action="store_true")
    parser.add_argument("--no-online", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true", help="Read-only plan mode. This never creates directories, logs, reports, or notes.")
    parser.add_argument("--write", action="store_true", help="Allow note/log/report writes.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing note.")
    parser.add_argument("--no-overwrite", dest="overwrite", action="store_false", help="Skip existing notes. This is the default.")
    parser.add_argument("--backup", dest="backup", action="store_true", default=True, help="Create a timestamped backup before overwrite. Default.")
    parser.add_argument("--no-backup", dest="backup", action="store_false", help="Do not create backups before overwrite.")
    parser.add_argument("--diff", dest="diff", action="store_true", default=True, help="Include diff summaries for updates. Default.")
    parser.add_argument("--no-diff", dest="diff", action="store_false", help="Suppress diff summaries.")
    parser.add_argument("--run-report", type=Path)
    args = parser.parse_args()
    effective_write = args.write and not args.dry_run

    queue = read_report_queue(args.report)
    imported_keys = read_imported_keys(args.note_root)
    existing_key_paths = index_existing_key_paths(args.note_root)
    pending = [row for row in queue if row["key"] not in imported_keys]
    if args.limit > 0:
        pending = pending[: args.limit]

    run_report: dict[str, Any] = {
        "source_report": str(args.report),
        "data_dir": str(args.data_dir),
        "note_root": str(args.note_root),
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "write": effective_write,
        "overwrite": args.overwrite,
        "backup": args.backup,
        "report_queue_items": len(queue),
        "initial_imported_keys": len(imported_keys),
        "queued": len(pending),
        "success": 0,
        "failed": 0,
        "skipped_existing": len(queue) - len(pending),
        "quality_counts": {},
        "target_collection_counts": {},
        "items": [],
    }

    for index, row in enumerate(pending, start=1):
        key = row["key"]
        try:
            item_result = import_one(
                data_dir=args.data_dir,
                note_root=args.note_root,
                row=row,
                online_email=args.online_email,
                skip_unpaywall=args.skip_unpaywall,
                no_online=args.no_online,
                existing_key_paths=existing_key_paths,
                write=effective_write,
                overwrite=args.overwrite,
                backup=args.backup,
                diff=args.diff,
            )
            if item_result["status"] in {"created", "updated"}:
                run_report["success"] += 1
            elif item_result["status"] == "skipped_existing":
                run_report["skipped_existing"] += 1
            quality = item_result["quality"]
            collection = item_result["target_collection"]
            run_report["quality_counts"][quality] = run_report["quality_counts"].get(quality, 0) + 1
            run_report["target_collection_counts"][collection] = (
                run_report["target_collection_counts"].get(collection, 0) + 1
            )
            run_report["items"].append({"index": index, **item_result})
            print(
                f"[{index}/{len(pending)}] success | {quality} | {collection} | {key} | {item_result['title']}",
                flush=True,
            )
        except Exception as exc:
            run_report["failed"] += 1
            run_report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": row.get("title", ""),
                    "target_collection": row.get("target_collection", ""),
                    "status": "failed",
                    "error": str(exc),
                }
            )
            print(f"[{index}/{len(pending)}] failed | {key} | {exc}", flush=True)

    run_report["finished_at"] = datetime.now().isoformat(timespec="seconds")
    if args.run_report:
        report_result = guarded_write_text(
            args.run_report,
            json.dumps(run_report, ensure_ascii=False, indent=2),
            write=effective_write,
            overwrite=args.overwrite,
            backup=args.backup,
            diff=args.diff,
        )
        run_report["run_report_write"] = report_result.to_dict()
    print(json.dumps({k: v for k, v in run_report.items() if k != "items"}, ensure_ascii=False, indent=2))
    return 0 if run_report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
