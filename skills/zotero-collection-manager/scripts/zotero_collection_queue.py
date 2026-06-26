#!/usr/bin/env python3
"""Build a resumable processing queue for one Zotero collection."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


FETCHER_SCRIPTS = Path(__file__).resolve().parents[2] / "zotero-data-fetcher" / "scripts"
sys.path.insert(0, str(FETCHER_SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from zotero_fetch import connect_db, default_data_dir  # noqa: E402
from safety_io import guarded_write_text  # noqa: E402


DONE_STATUS_RE = re.compile(r"\|\s*(✅ 成功|⚠️ 跳过)\s*\|")
LOG_KEY_RE = re.compile(r"\|\s*(?P<key>[A-Z0-9]{8})\s*\|")


def item_title_expr() -> str:
    return """
    (
      select v.value
      from itemData id
      join fields f on f.fieldID = id.fieldID and f.fieldName = 'title'
      join itemDataValues v on v.valueID = id.valueID
      where id.itemID = i.itemID
      limit 1
    ) as title
    """


def collection_ids(conn: sqlite3.Connection, collection_name: str, recursive: bool) -> list[int]:
    row = conn.execute(
        "select collectionID from collections where collectionName = ?",
        (collection_name,),
    ).fetchone()
    if not row:
        matches = conn.execute(
            "select collectionID, collectionName from collections where lower(collectionName) like lower(?) order by collectionName",
            (f"%{collection_name}%",),
        ).fetchall()
        names = ", ".join(match["collectionName"] for match in matches[:10])
        raise LookupError(f"Collection not found: {collection_name}. Similar: {names}")

    ids = [row["collectionID"]]
    if not recursive:
        return ids

    queue = [row["collectionID"]]
    while queue:
        parent = queue.pop(0)
        children = conn.execute(
            "select collectionID from collections where parentCollectionID = ?",
            (parent,),
        ).fetchall()
        for child in children:
            ids.append(child["collectionID"])
            queue.append(child["collectionID"])
    return ids


def list_collection_items(
    conn: sqlite3.Connection, collection_name: str, recursive: bool
) -> list[dict[str, Any]]:
    ids = collection_ids(conn, collection_name, recursive)
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"""
        select distinct i.itemID, i.key, it.typeName as itemType, {item_title_expr()}
        from collectionItems ci
        join items i on i.itemID = ci.itemID
        join itemTypes it on it.itemTypeID = i.itemTypeID
        where ci.collectionID in ({placeholders})
          and it.typeName not in ('attachment', 'note', 'annotation')
        order by title collate nocase
        """,
        ids,
    ).fetchall()
    return [dict(row) for row in rows]


def read_done_keys(log_file: Path) -> set[str]:
    if not log_file.exists():
        return set()
    done: set[str] = set()
    for line in log_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not DONE_STATUS_RE.search(line):
            continue
        match = LOG_KEY_RE.search(line)
        if match:
            done.add(match.group("key"))
    return done


def ensure_log(log_file: Path, collection: str, *, write: bool = False) -> dict[str, object] | None:
    if log_file.exists():
        return None
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    result = guarded_write_text(
        log_file,
        f"# Process Log: {collection}\n\nCreated: {timestamp}\n\n",
        write=write,
        overwrite=False,
        backup=False,
        diff=False,
    )
    return result.to_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True, help="Exact Zotero collection name")
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--note-root", type=Path, default=Path(r"<note_root>"))
    parser.add_argument("--log-file", type=Path, help="Override process log path")
    parser.add_argument("--recursive", action="store_true", help="Include child collections")
    parser.add_argument("--dry-run", action="store_true", help="Read only. Do not create logs or output files.")
    parser.add_argument("--write", action="store_true", help="Allow creating a missing process log or --out file.")
    parser.add_argument("--out", type=Path, help="Write queue JSON to this file")
    args = parser.parse_args()

    target_dir = args.note_root / args.collection
    log_file = args.log_file or target_dir / "_ProcessLog_进度记录.md"
    log_write = ensure_log(log_file, args.collection, write=args.write and not args.dry_run)

    conn = connect_db(args.data_dir)
    try:
        all_items = list_collection_items(conn, args.collection, args.recursive)
    finally:
        conn.close()

    done_keys = read_done_keys(log_file)
    queue = [item for item in all_items if item["key"] not in done_keys]
    payload = {
        "collection": args.collection,
        "data_dir": str(args.data_dir),
        "target_dir": str(target_dir),
        "log_file": str(log_file),
        "log_write": log_write,
        "total_items": len(all_items),
        "done_items": len(done_keys),
        "queued_items": len(queue),
        "queue": queue,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        result = guarded_write_text(
            args.out,
            text,
            write=args.write and not args.dry_run,
            overwrite=False,
            backup=False,
            diff=False,
        )
        payload["output_write"] = result.to_dict()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
