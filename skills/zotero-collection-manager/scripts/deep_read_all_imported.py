#!/usr/bin/env python3
"""Deep-read all imported Zotero notes that have local PDF full-text evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
FETCHER_SCRIPTS = THIS_DIR.parents[1] / "zotero-data-fetcher" / "scripts"
sys.path.insert(0, str(FETCHER_SCRIPTS))
sys.path.insert(0, str(THIS_DIR))

from deep_read_collection import (  # noqa: E402
    append_log,
    fulltext_from_payload,
    has_existing_pdf,
    make_deep_note,
)
from zotero_fetch import (  # noqa: E402
    assess_raw_data_quality,
    connect_db,
    default_data_dir,
    fetch_from_sqlite,
)
from safety_io import guarded_write_text  # noqa: E402


ITEM_KEY_RE = re.compile(r'^\s*item_key:\s*["\']?(?P<key>[A-Z0-9]{8})["\']?\s*$', re.M)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


def imported_note_index(note_root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in sorted(note_root.rglob("*.md")):
        if "zotero-imports" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")[:5000]
        except OSError:
            continue
        for match in ITEM_KEY_RE.finditer(text):
            index.setdefault(match.group("key"), path)
    return index


def collection_for_path(note_root: Path, path: Path) -> str:
    try:
        return path.relative_to(note_root).parts[0]
    except Exception:
        return path.parent.name


def active_parent_keys(data_dir: Path) -> set[str]:
    conn = connect_db(data_dir)
    try:
        rows = conn.execute(
            """
            select i.key
            from items i
            join itemTypes it on it.itemTypeID = i.itemTypeID
            where it.typeName not in ('attachment', 'note', 'annotation')
              and not exists (select 1 from deletedItems d where d.itemID = i.itemID)
            """
        ).fetchall()
        return {row["key"] for row in rows}
    finally:
        conn.close()


def ensure_deep_log(note_root: Path, collection: str, *, write: bool) -> tuple[Path, dict[str, object] | None]:
    target_dir = note_root / collection
    log_file = target_dir / "_DeepReadLog_二次精读记录.md"
    result = None
    if not log_file.exists():
        result = guarded_write_text(
            log_file,
            f"# Deep Read Log: {collection}\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
            write=write,
            overwrite=False,
            backup=False,
            diff=False,
        ).to_dict()
    return log_file, result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--note-root", type=Path, default=Path(r"<note_root>"))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Read-only plan mode. This never creates directories, logs, reports, or notes.")
    parser.add_argument("--write", action="store_true", help="Allow note/log/report writes.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing note.")
    parser.add_argument("--no-overwrite", dest="overwrite", action="store_false", help="Skip existing notes. This is the default.")
    parser.add_argument("--backup", dest="backup", action="store_true", default=True, help="Create a timestamped backup before overwrite. Default.")
    parser.add_argument("--no-backup", dest="backup", action="store_false", help="Do not create backups before overwrite.")
    parser.add_argument("--diff", dest="diff", action="store_true", default=True, help="Include diff summaries for updates. Default.")
    parser.add_argument("--no-diff", dest="diff", action="store_false", help="Suppress diff summaries.")
    args = parser.parse_args()
    effective_write = args.write and not args.dry_run

    notes = imported_note_index(args.note_root)
    rows: list[dict[str, Any]] = []
    active_keys = active_parent_keys(args.data_dir)
    for key, note_path in sorted(notes.items(), key=lambda item: str(item[1]).lower()):
        collection = collection_for_path(args.note_root, note_path)
        if collection in {"zotero-imports", "结构化ML"}:
            continue
        if key not in active_keys:
            continue
        rows.append({"key": key, "note_path": note_path, "collection": collection})
    if args.limit > 0:
        rows = rows[: args.limit]

    report: dict[str, Any] = {
        "note_root": str(args.note_root),
        "data_dir": str(args.data_dir),
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "write": effective_write,
        "overwrite": args.overwrite,
        "backup": args.backup,
        "imported_note_keys": len(notes),
        "active_zotero_parent_keys": len(active_keys),
        "queued_notes": len(rows),
        "deep_read": 0,
        "skipped_no_local_pdf": 0,
        "skipped_no_fulltext_cache": 0,
        "skipped_not_in_zotero": 0,
        "failed": 0,
        "by_collection": {},
        "items": [],
    }
    by_collection: Counter[str] = Counter()

    for index, row in enumerate(rows, start=1):
        key = row["key"]
        note_path: Path = row["note_path"]
        collection = row["collection"]
        write_result = None
        try:
            payload = fetch_from_sqlite(args.data_dir, key, None)
            title = ((payload.get("item") or {}).get("data") or {}).get("title") or key
            quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
            fulltext, pdf_key, pdf_path = fulltext_from_payload(payload)
            has_pdf = has_existing_pdf(payload)
            log_file, log_init = ensure_deep_log(args.note_root, collection, write=effective_write)

            if not has_pdf:
                report["skipped_no_local_pdf"] += 1
                status = "skipped_no_local_pdf"
                detail = quality.get("level", "")
            elif not fulltext or quality.get("level") != "local_fulltext":
                report["skipped_no_fulltext_cache"] += 1
                status = "skipped_no_fulltext_cache"
                detail = quality.get("level", "")
            else:
                write_result = guarded_write_text(
                    note_path,
                    make_deep_note(payload, collection),
                    write=effective_write,
                    overwrite=args.overwrite,
                    backup=args.backup,
                    diff=args.diff,
                )
                if write_result.status in {"created", "updated"}:
                    append_log(log_file, "✅ 二次精读", key, title, note_path.name, write=effective_write)
                    report["deep_read"] += 1
                    by_collection[collection] += 1
                elif write_result.status == "skipped_existing":
                    append_log(log_file, "⚠️ 跳过", key, title, "existing note; --overwrite not set", write=effective_write)
                status = write_result.status
                detail = f"{quality.get('fulltext_cache_chars', 0)} chars"

            if status in {"skipped_no_local_pdf", "skipped_no_fulltext_cache"} and effective_write:
                append_log(log_file, "⚠️ 跳过", key, title, detail, write=effective_write)

            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": title,
                    "collection": collection,
                    "status": status,
                    "quality": quality.get("level"),
                    "note_path": str(note_path),
                    "pdf_key": pdf_key,
                    "pdf_path": pdf_path,
                    "fulltext_cache_chars": quality.get("fulltext_cache_chars", 0),
                    "log_init": log_init,
                    "write_result": write_result.to_dict() if write_result else None,
                }
            )
            print(f"[{index}/{len(rows)}] {status} | {collection} | {key} | {title}", flush=True)
        except LookupError as exc:
            report["skipped_not_in_zotero"] += 1
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "collection": collection,
                    "status": "skipped_not_in_zotero",
                    "note_path": str(note_path),
                    "error": str(exc),
                }
            )
            print(f"[{index}/{len(rows)}] skipped_not_in_zotero | {collection} | {key} | {exc}", flush=True)
        except Exception as exc:
            report["failed"] += 1
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "collection": collection,
                    "status": "failed",
                    "note_path": str(note_path),
                    "error": str(exc),
                }
            )
            print(f"[{index}/{len(rows)}] failed | {collection} | {key} | {exc}", flush=True)

    report["by_collection"] = dict(sorted(by_collection.items()))
    report["finished_at"] = datetime.now().isoformat(timespec="seconds")
    if args.report:
        report_result = guarded_write_text(
            args.report,
            json.dumps(report, ensure_ascii=False, indent=2),
            write=effective_write,
            overwrite=args.overwrite,
            backup=args.backup,
            diff=args.diff,
        )
        report["report_write"] = report_result.to_dict()
    print(json.dumps({k: v for k, v in report.items() if k != "items"}, ensure_ascii=False, indent=2))
    return 0 if report["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
