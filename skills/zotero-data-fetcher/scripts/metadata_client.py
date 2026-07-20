"""Standard-library normalization and scholarly metadata service client."""

from __future__ import annotations

import html
import re
import urllib.parse
from collections.abc import Callable, Iterable, Mapping
from typing import Any


HttpJson = Callable[[str], Any]


def clean_doi(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("DOI must be a string or None")
    doi = value.strip()
    doi = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", doi, flags=re.I)
    doi = doi.strip().rstrip(".").strip()
    return doi or None


def abstract_from_openalex(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positioned: list[tuple[int, str]] = []
    for word, positions in index.items():
        if not isinstance(word, str) or not isinstance(positions, list):
            continue
        positioned.extend((position, word) for position in positions if isinstance(position, int))
    return " ".join(word for _, word in sorted(positioned, key=lambda entry: (entry[0], entry[1])))


def publication_year_from_crossref(message: dict[str, Any]) -> int | None:
    for key in ("published-print", "published-online", "published", "issued"):
        date_parts = (message.get(key) or {}).get("date-parts") if isinstance(message.get(key), dict) else None
        if date_parts and isinstance(date_parts, list) and date_parts[0]:
            year = date_parts[0][0]
            if isinstance(year, int):
                return year
    return None


def strip_markup(value: Any) -> str:
    if value is None:
        return ""
    text = re.sub(r"<[^>]*>", " ", str(value))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    plain = strip_markup(value).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", plain))


def title_similarity(left: str | None, right: str | None) -> float:
    left_tokens = set(normalize_title(left).split())
    right_tokens = set(normalize_title(right).split())
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def title_matches(left: str | None, right: str | None, threshold: float = 0.5) -> bool:
    left_normalized = normalize_title(left)
    right_normalized = normalize_title(right)
    if not left_normalized or not right_normalized:
        return False
    return (
        left_normalized in right_normalized
        or right_normalized in left_normalized
        or title_similarity(left, right) >= threshold
    )


def _first_text(value: Any) -> str:
    if isinstance(value, list):
        return strip_markup(value[0]) if value else ""
    return strip_markup(value)


def normalize_crossref_message(message: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "DOI": clean_doi(message.get("DOI")),
        "title": _first_text(message.get("title")),
        "container_title": _first_text(message.get("container-title")),
        "publisher": strip_markup(message.get("publisher")),
        "type": strip_markup(message.get("type")),
        "published_year": publication_year_from_crossref(dict(message)),
        "abstract": strip_markup(message.get("abstract")),
        "url": strip_markup(message.get("URL")),
    }


def _with_query(url: str, params: Mapping[str, str | int | None]) -> str:
    present = {key: value for key, value in params.items() if value not in (None, "")}
    return f"{url}?{urllib.parse.urlencode(present)}" if present else url


def crossref_lookup(doi: str | None, email: str | None, http_get: HttpJson) -> dict[str, Any] | None:
    cleaned = clean_doi(doi)
    if not cleaned:
        return None
    url = _with_query(
        "https://api.crossref.org/works/" + urllib.parse.quote(cleaned, safe=""),
        {"mailto": email},
    )
    try:
        payload = http_get(url)
        message = payload.get("message") if isinstance(payload, dict) else None
        return normalize_crossref_message(message) if isinstance(message, dict) else None
    except Exception:
        return None


def crossref_title_search(title: str | None, email: str | None, http_get: HttpJson) -> dict[str, Any] | None:
    if not normalize_title(title):
        return None
    url = _with_query(
        "https://api.crossref.org/works",
        {"query.title": title, "rows": 5, "mailto": email},
    )
    try:
        payload = http_get(url)
        message = payload.get("message") if isinstance(payload, dict) else None
        items = message.get("items") if isinstance(message, dict) else None
        if not isinstance(items, list):
            return None
        candidates = [item for item in items if isinstance(item, dict)]
        ranked = sorted(
            candidates,
            key=lambda item: (-title_similarity(title, _first_text(item.get("title"))), _first_text(item.get("title"))),
        )
        if not ranked or not title_matches(title, _first_text(ranked[0].get("title"))):
            return None
        result = normalize_crossref_message(ranked[0])
        result["match_score"] = title_similarity(title, result["title"])
        return result
    except Exception:
        return None


def _normalize_openalex(work: Mapping[str, Any]) -> dict[str, Any]:
    open_access = work.get("open_access") if isinstance(work.get("open_access"), dict) else {}
    locations = work.get("locations") if isinstance(work.get("locations"), list) else []
    primary = work.get("primary_location") if isinstance(work.get("primary_location"), dict) else None
    return {
        "id": work.get("id"),
        "doi": clean_doi(work.get("doi")),
        "title": strip_markup(work.get("title") or work.get("display_name")),
        "publication_year": work.get("publication_year"),
        "type": work.get("type"),
        "is_oa": bool(open_access.get("is_oa")),
        "oa_status": open_access.get("oa_status"),
        "abstract": abstract_from_openalex(work.get("abstract_inverted_index")),
        "primary_location": primary,
        "locations": locations,
    }


def openalex_lookup(
    doi: str | None,
    title: str | None,
    email: str | None,
    http_get: HttpJson,
) -> dict[str, Any] | None:
    cleaned = clean_doi(doi)
    if not cleaned and not normalize_title(title):
        return None
    if cleaned:
        identifier = urllib.parse.quote(f"https://doi.org/{cleaned}", safe="")
        url = _with_query(f"https://api.openalex.org/works/{identifier}", {"mailto": email})
    else:
        url = _with_query(
            "https://api.openalex.org/works",
            {"search": title, "per-page": 5, "mailto": email},
        )
    try:
        payload = http_get(url)
        if cleaned:
            work = payload if isinstance(payload, dict) else None
        else:
            results = payload.get("results") if isinstance(payload, dict) else None
            candidates = [entry for entry in (results or []) if isinstance(entry, dict)]
            candidates.sort(
                key=lambda entry: (-title_similarity(title, entry.get("title") or entry.get("display_name")), str(entry.get("id") or ""))
            )
            work = candidates[0] if candidates else None
        if not isinstance(work, dict):
            return None
        return _normalize_openalex(work)
    except Exception:
        return None


def unpaywall_lookup(doi: str | None, email: str | None, http_get: HttpJson) -> dict[str, Any] | None:
    cleaned = clean_doi(doi)
    if not cleaned or not email:
        return None
    url = _with_query(
        "https://api.unpaywall.org/v2/" + urllib.parse.quote(cleaned, safe=""),
        {"email": email},
    )
    try:
        payload = http_get(url)
        if not isinstance(payload, dict):
            return None
        return {
            "doi": clean_doi(payload.get("doi")),
            "doi_url": payload.get("doi_url"),
            "title": strip_markup(payload.get("title")),
            "year": payload.get("year"),
            "is_oa": bool(payload.get("is_oa")),
            "oa_status": payload.get("oa_status"),
            "best_oa_location": payload.get("best_oa_location") if isinstance(payload.get("best_oa_location"), dict) else None,
            "oa_locations": payload.get("oa_locations") if isinstance(payload.get("oa_locations"), list) else [],
        }
    except Exception:
        return None


def _locations(source: str, record: Mapping[str, Any] | None) -> Iterable[dict[str, str]]:
    if not record:
        return
    if source == "unpaywall":
        candidates = [record.get("best_oa_location"), *(record.get("oa_locations") or [])]
    else:
        candidates = [record.get("primary_location"), *(record.get("locations") or [])]
    for location in candidates:
        if not isinstance(location, dict):
            continue
        pdf_url = location.get("url_for_pdf") or location.get("pdf_url") or ""
        landing_url = (
            location.get("url_for_landing_page")
            or location.get("landing_page_url")
            or location.get("url")
            or ""
        )
        if not pdf_url and not landing_url:
            continue
        yield {
            "source": source,
            "pdf_url": str(pdf_url),
            "landing_page_url": str(landing_url),
            "license": str(location.get("license") or ""),
            "is_oa": "true" if bool(location.get("is_oa", True)) else "false",
        }


def collect_oa_locations(payload: Mapping[str, Any]) -> list[dict[str, str]]:
    collected: list[dict[str, str]] = []
    seen: set[str] = set()
    for source in ("unpaywall", "openalex"):
        record = payload.get(source)
        for location in _locations(source, record if isinstance(record, dict) else None):
            identity = location["pdf_url"] or location["landing_page_url"]
            if identity in seen:
                continue
            seen.add(identity)
            collected.append(location)
    return collected
