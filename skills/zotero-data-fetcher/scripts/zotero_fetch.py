#!/usr/bin/env python3
"""Fetch one Zotero item and its usable reading corpus.

The script prefers the Zotero Local API when available, then falls back to the
local SQLite database. It emits JSON for the analytical writer and does not
summarize or translate the source material.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR))

import metadata_client as _metadata  # noqa: E402


DEFAULT_API = "http://localhost:23119/api"
DEFAULT_USER_AGENT = "ZoteroAnalyticalWorkflow/0.1 (mailto:research-workflow@example.invalid)"


def locate_zotero_profile() -> Path | None:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
    profiles = Path(appdata) / "Zotero" / "Zotero" / "Profiles"
    if not profiles.exists():
        return None
    candidates = sorted(profiles.glob("*.default*")) or sorted(profiles.iterdir())
    for candidate in candidates:
        if (candidate / "prefs.js").exists():
            return candidate
    return None


def read_pref_data_dir(profile: Path | None) -> Path | None:
    if not profile:
        return None
    prefs = profile / "prefs.js"
    if not prefs.exists():
        return None
    pattern = re.compile(
        r'user_pref\("extensions\.zotero\.dataDir",\s*"(?P<path>.*?)"\);'
    )
    for line in prefs.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = pattern.search(line)
        if match:
            return Path(match.group("path").replace("\\\\", "\\"))
    return None


def default_data_dir() -> Path:
    configured = read_pref_data_dir(locate_zotero_profile())
    if configured:
        return configured
    return Path.home() / "Zotero"


def http_json(
    url: str,
    timeout: float = 8.0,
    headers: dict[str, str] | None = None,
) -> Any:
    request_headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json",
        "Zotero-API-Version": "3",
    }
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def local_api_item(api_base: str, key: str | None, title: str | None) -> dict[str, Any] | None:
    api_base = api_base.rstrip("/")
    candidates: list[str] = []
    if key:
        encoded = urllib.parse.quote(key)
        candidates.extend(
            [
                f"{api_base}/items/{encoded}",
                f"{api_base}/users/0/items/{encoded}",
                f"{api_base}/items?itemKey={encoded}",
                f"{api_base}/users/0/items?itemKey={encoded}",
            ]
        )
    elif title:
        encoded = urllib.parse.quote(title)
        candidates.extend(
            [
                f"{api_base}/items?q={encoded}&qmode=title",
                f"{api_base}/users/0/items?q={encoded}&qmode=title",
            ]
        )

    for url in candidates:
        try:
            payload = http_json(url)
        except Exception:
            continue
        if isinstance(payload, list):
            if payload:
                return payload[0]
        elif isinstance(payload, dict) and payload:
            return payload
    return None


def connect_db(data_dir: Path) -> sqlite3.Connection:
    db = data_dir / "zotero.sqlite"
    if not db.exists():
        raise FileNotFoundError(f"Zotero database not found: {db}")
    # Zotero keeps the database open while the desktop app is running. immutable
    # allows read-only analytical access without waiting on the live writer lock.
    uri = f"file:{db.as_posix()}?mode=ro&immutable=1"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("pragma query_only = true")
    return conn


def table_exists(conn: sqlite3.Connection, table: str) -> bool:
    row = conn.execute(
        "select 1 from sqlite_master where type='table' and name=?", (table,)
    ).fetchone()
    return row is not None


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row["name"] for row in conn.execute(f"pragma table_info({table})")}


def sqlite_find_item(
    conn: sqlite3.Connection, key: str | None, title: str | None
) -> sqlite3.Row | None:
    if key:
        return conn.execute(
            """
            select i.itemID, i.key, it.typeName as itemType
            from items i
            join itemTypes it on it.itemTypeID = i.itemTypeID
            where i.key = ?
            """,
            (key,),
        ).fetchone()
    if title:
        return conn.execute(
            """
            select i.itemID, i.key, it.typeName as itemType
            from items i
            join itemTypes it on it.itemTypeID = i.itemTypeID
            join itemData id on id.itemID = i.itemID
            join fields f on f.fieldID = id.fieldID and f.fieldName = 'title'
            join itemDataValues v on v.valueID = id.valueID
            where lower(v.value) like lower(?)
            limit 1
            """,
            (f"%{title}%",),
        ).fetchone()
    raise ValueError("Provide --key or --title")


def sqlite_item_fields(conn: sqlite3.Connection, item_id: int) -> dict[str, Any]:
    rows = conn.execute(
        """
        select f.fieldName, v.value
        from itemData id
        join fields f on f.fieldID = id.fieldID
        join itemDataValues v on v.valueID = id.valueID
        where id.itemID = ?
        order by f.fieldName
        """,
        (item_id,),
    ).fetchall()
    fields = {row["fieldName"]: row["value"] for row in rows}
    creators = conn.execute(
        """
        select c.firstName, c.lastName, ct.creatorType
        from itemCreators ic
        join creators c on c.creatorID = ic.creatorID
        join creatorTypes ct on ct.creatorTypeID = ic.creatorTypeID
        where ic.itemID = ?
        order by ic.orderIndex
        """,
        (item_id,),
    ).fetchall()
    fields["creators"] = [
        {
            "firstName": row["firstName"],
            "lastName": row["lastName"],
            "creatorType": row["creatorType"],
        }
        for row in creators
    ]
    return fields


def resolve_attachment_path(data_dir: Path, attachment_key: str, path_value: str | None) -> str | None:
    storage_dir = data_dir / "storage" / attachment_key
    if not path_value:
        pdfs = sorted(storage_dir.glob("*.pdf"))
        return str(pdfs[0]) if pdfs else None
    if path_value.startswith("storage:"):
        candidate = storage_dir / path_value.split(":", 1)[1]
        if candidate.exists():
            return str(candidate)
        pdfs = sorted(storage_dir.glob("*.pdf"))
        return str(pdfs[0]) if pdfs else str(candidate)
    return path_value


def sqlite_attachments(conn: sqlite3.Connection, data_dir: Path, parent_id: int) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        select i.itemID, i.key, ia.contentType, ia.path,
               (
                 select v.value
                 from itemData id
                 join fields f on f.fieldID = id.fieldID and f.fieldName = 'title'
                 join itemDataValues v on v.valueID = id.valueID
                 where id.itemID = i.itemID
                 limit 1
               ) as title
        from itemAttachments ia
        join items i on i.itemID = ia.itemID
        where ia.parentItemID = ?
        order by i.itemID
        """,
        (parent_id,),
    ).fetchall()
    attachments = []
    for row in rows:
        cache = data_dir / "storage" / row["key"] / ".zotero-ft-cache"
        attachments.append(
            {
                "itemID": row["itemID"],
                "key": row["key"],
                "title": row["title"],
                "contentType": row["contentType"],
                "path": resolve_attachment_path(data_dir, row["key"], row["path"]),
                "fulltext_cache_path": str(cache) if cache.exists() else None,
                "fulltext_cache": cache.read_text(encoding="utf-8", errors="ignore")
                if cache.exists()
                else "",
            }
        )
    return attachments


def sqlite_notes(conn: sqlite3.Connection, parent_id: int) -> list[dict[str, Any]]:
    if not table_exists(conn, "itemNotes"):
        return []
    rows = conn.execute(
        """
        select i.key, n.note
        from itemNotes n
        join items i on i.itemID = n.itemID
        where n.parentItemID = ?
        order by i.itemID
        """,
        (parent_id,),
    ).fetchall()
    return [{"key": row["key"], "note": row["note"]} for row in rows]


def sqlite_annotations(conn: sqlite3.Connection, parent_id: int) -> list[dict[str, Any]]:
    if not table_exists(conn, "itemAnnotations"):
        return []
    columns = table_columns(conn, "itemAnnotations")
    type_col = "annotationType" if "annotationType" in columns else "type"
    text_col = "annotationText" if "annotationText" in columns else "text"
    comment_col = "annotationComment" if "annotationComment" in columns else "comment"
    page_col = "annotationPageLabel" if "annotationPageLabel" in columns else "pageLabel"
    sort_col = "annotationSortIndex" if "annotationSortIndex" in columns else "sortIndex"
    rows = conn.execute(
        f"""
        select i.key, ia.{type_col} as annotationType,
               ia.{text_col} as annotationText,
               ia.{comment_col} as annotationComment,
               ia.{page_col} as annotationPageLabel,
               ia.{sort_col} as annotationSortIndex
        from itemAnnotations ia
        join items i on i.itemID = ia.itemID
        join itemAttachments att on att.itemID = ia.parentItemID
        where att.parentItemID = ?
        order by ia.{sort_col}
        """,
        (parent_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def item_data(payload: dict[str, Any]) -> dict[str, Any]:
    item = payload.get("item") or {}
    data = item.get("data") if isinstance(item, dict) else {}
    if isinstance(data, dict):
        return data
    return item if isinstance(item, dict) else {}


def clean_doi(value: str | None) -> str | None:
    return _metadata.clean_doi(value)


def abstract_from_openalex(index: dict[str, list[int]] | None) -> str:
    return _metadata.abstract_from_openalex(index)


def publication_year_from_crossref(message: dict[str, Any]) -> int | None:
    return _metadata.publication_year_from_crossref(message)


def title_from_crossref(message: dict[str, Any]) -> str:
    title = message.get("title")
    value = title[0] if isinstance(title, list) and title else title
    return _metadata.strip_markup(value)


def first_container_title(message: dict[str, Any]) -> str:
    value = message.get("container-title")
    first = value[0] if isinstance(value, list) and value else value
    return _metadata.strip_markup(first)


def normalize_title(value: str | None) -> str:
    return _metadata.normalize_title(value)


def title_similarity(left: str | None, right: str | None) -> float:
    return _metadata.title_similarity(left, right)


def title_matches(
    expected: str | None,
    found: str | None,
    threshold: float = 0.5,
) -> bool:
    return _metadata.title_matches(expected, found, threshold)


def collect_oa_locations(payload: dict[str, Any]) -> list[dict[str, str]]:
    return _metadata.collect_oa_locations(payload)


def crossref_lookup(doi: str | None, email: str | None) -> dict[str, Any] | None:
    return _metadata.crossref_lookup(doi, email, http_json)


def crossref_title_search(title: str | None, email: str | None) -> dict[str, Any] | None:
    return _metadata.crossref_title_search(title, email, http_json)


def openalex_lookup(
    doi: str | None,
    title: str | None,
    email: str | None,
) -> dict[str, Any] | None:
    return _metadata.openalex_lookup(doi, title, email, http_json)


def unpaywall_lookup(doi: str | None, email: str | None) -> dict[str, Any] | None:
    return _metadata.unpaywall_lookup(doi, email, http_json)


def add_online_supplements(
    payload: dict[str, Any],
    email: str | None,
    skip_unpaywall: bool = False,
) -> dict[str, Any]:
    data = item_data(payload)
    doi = clean_doi(data.get("DOI") or data.get("doi"))
    title = str(data.get("title") or "").strip()
    warnings: list[str] = []

    crossref = crossref_lookup(doi, email) if doi else crossref_title_search(title, email)
    if crossref and title and not title_matches(title, crossref.get("title")):
        warnings.append("Crossref DOI result title mismatch; result rejected.")
        crossref = crossref_title_search(title, email)
    if crossref and title and not title_matches(title, crossref.get("title")):
        warnings.append("Crossref title-search result did not validate; result rejected.")
        crossref = None

    openalex = openalex_lookup(doi, title or None, email)
    if openalex and title and not title_matches(title, openalex.get("title")):
        warnings.append("OpenAlex result title mismatch; result rejected.")
        if doi:
            retry = openalex_lookup(None, title, email)
            openalex = retry if retry and title_matches(title, retry.get("title")) else None
        else:
            openalex = None

    unpaywall = None
    if doi and email and not skip_unpaywall:
        unpaywall = unpaywall_lookup(doi, email)
        if unpaywall and title and not title_matches(title, unpaywall.get("title")):
            warnings.append("Unpaywall result title mismatch; result rejected.")
            unpaywall = None

    supplements: dict[str, Any] = {
        "doi": doi,
        "title": title,
        "warnings": warnings,
        "crossref": crossref,
        "openalex": openalex,
        "unpaywall": unpaywall,
        "oa_locations": [],
    }
    supplements["oa_locations"] = collect_oa_locations(supplements)
    payload["online_supplements"] = supplements
    payload["raw_data_quality"] = assess_raw_data_quality(payload)
    payload["raw_data_buffer"] = build_raw_buffer(payload)
    return payload


def assess_raw_data_quality(payload: dict[str, Any]) -> dict[str, Any]:
    fulltext_chars = sum(
        len(attachment.get("fulltext_cache") or "")
        for attachment in payload.get("attachments", [])
    )
    notes_count = len(payload.get("notes") or [])
    annotations_count = len(payload.get("annotations") or [])
    online = payload.get("online_supplements") or {}
    abstracts = [
        ((online.get("crossref") or {}).get("abstract") or ""),
        ((online.get("openalex") or {}).get("abstract") or ""),
    ]
    has_online_abstract = any(abstract.strip() for abstract in abstracts)
    level = "metadata_only"
    if fulltext_chars > 3000:
        level = "local_fulltext"
    elif annotations_count or notes_count:
        level = "zotero_notes_or_annotations"
    elif has_online_abstract:
        level = "online_abstract"
    return {
        "level": level,
        "fulltext_cache_chars": fulltext_chars,
        "notes_count": notes_count,
        "annotations_count": annotations_count,
        "has_online_abstract": has_online_abstract,
        "oa_location_count": len(online.get("oa_locations") or []),
        "needs_fulltext_for_deep_reading": level in {"metadata_only", "online_abstract"},
    }


def build_raw_buffer(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    item = payload.get("item", {})
    parts.append("## Metadata")
    parts.append(json.dumps(item, ensure_ascii=False, indent=2))
    online = payload.get("online_supplements") or {}
    if online:
        parts.append("\n## Online Supplements")
        for source_name in ("crossref", "openalex", "unpaywall"):
            source = online.get(source_name) or {}
            if not source:
                continue
            parts.append(f"\n### {source_name}")
            compact = {
                k: v
                for k, v in source.items()
                if k not in {"locations", "primary_location", "oa_locations", "best_oa_location"}
            }
            parts.append(json.dumps(compact, ensure_ascii=False, indent=2))
        locations = online.get("oa_locations") or []
        if locations:
            parts.append("\n### Open Access Locations")
            parts.append(json.dumps(locations, ensure_ascii=False, indent=2))
    notes = payload.get("notes") or []
    if notes:
        parts.append("\n## Zotero Notes")
        for note in notes:
            parts.append(f"\n### Note {note.get('key', '')}\n{note.get('note', '')}")
    annotations = payload.get("annotations") or []
    if annotations:
        parts.append("\n## Zotero Annotations")
        for annotation in annotations:
            page = annotation.get("annotationPageLabel") or ""
            text = annotation.get("annotationText") or ""
            comment = annotation.get("annotationComment") or ""
            parts.append(f"\n### Page {page}\n{text}\n{comment}".strip())
    for attachment in payload.get("attachments", []):
        cache = attachment.get("fulltext_cache") or ""
        if cache:
            parts.append(
                f"\n## Full Text Cache: {attachment.get('key', '')}\n{cache}"
            )
    return "\n".join(parts).strip()


def fetch_from_sqlite(data_dir: Path, key: str | None, title: str | None) -> dict[str, Any]:
    conn = connect_db(data_dir)
    try:
        row = sqlite_find_item(conn, key, title)
        if not row:
            raise LookupError("No matching Zotero item found")
        item = {
            "itemID": row["itemID"],
            "key": row["key"],
            "itemType": row["itemType"],
            "data": sqlite_item_fields(conn, row["itemID"]),
        }
        payload = {
            "source": "sqlite",
            "data_dir": str(data_dir),
            "item": item,
            "attachments": sqlite_attachments(conn, data_dir, row["itemID"]),
            "notes": sqlite_notes(conn, row["itemID"]),
            "annotations": sqlite_annotations(conn, row["itemID"]),
        }
        payload["raw_data_quality"] = assess_raw_data_quality(payload)
        payload["raw_data_buffer"] = build_raw_buffer(payload)
        return payload
    finally:
        conn.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--key", help="Zotero parent item key")
    parser.add_argument("--title", help="Title or title fragment")
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--api-base", default=DEFAULT_API)
    parser.add_argument("--no-api", action="store_true", help="Skip Zotero Local API")
    parser.add_argument("--no-online", action="store_true", help="Skip Crossref/OpenAlex/Unpaywall fallback metadata")
    parser.add_argument("--online-email", default=os.environ.get("SCHOLAR_API_EMAIL") or os.environ.get("UNPAYWALL_EMAIL") or os.environ.get("CROSSREF_MAILTO"), help="Email used for polite scholarly API requests")
    parser.add_argument("--skip-unpaywall", action="store_true", help="Do not call Unpaywall even when an email is available")
    parser.add_argument("--write", action="store_true", help="Allow writing --out JSON. Without this, output is printed to stdout only.")
    parser.add_argument("--out", type=Path, help="Write JSON to this path")
    args = parser.parse_args()

    if not args.key and not args.title:
        parser.error("provide --key or --title")

    api_item = None if args.no_api else local_api_item(args.api_base, args.key, args.title)
    if api_item:
        payload = {
            "source": "local-api",
            "data_dir": str(args.data_dir),
            "item": api_item,
            "attachments": [],
            "notes": [],
            "annotations": [],
        }
        # The API result is useful for metadata, but local cache extraction still
        # requires the SQLite fallback when the parent key can be resolved.
        key = args.key or api_item.get("key")
        try:
            sqlite_payload = fetch_from_sqlite(args.data_dir, key, args.title)
            sqlite_payload["source"] = "local-api+sqlite-cache"
            payload = sqlite_payload
            payload["api_item"] = api_item
        except Exception as exc:
            payload["warning"] = f"SQLite cache extraction skipped: {exc}"
            payload["raw_data_quality"] = assess_raw_data_quality(payload)
            payload["raw_data_buffer"] = build_raw_buffer(payload)
    else:
        payload = fetch_from_sqlite(args.data_dir, args.key, args.title)

    if not args.no_online:
        payload = add_online_supplements(
            payload,
            email=args.online_email,
            skip_unpaywall=args.skip_unpaywall,
        )

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        if not args.write:
            print(
                json.dumps(
                    {
                        "status": "planned_output",
                        "path": str(args.out),
                        "message": "No file was written. Re-run with --write to create --out.",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                file=sys.stderr,
            )
            print(text)
        else:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
