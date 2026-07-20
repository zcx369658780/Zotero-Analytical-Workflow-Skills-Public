#!/usr/bin/env python3
"""Batch-import one Zotero collection into Obsidian literature notes.

This is a first-pass importer for timing and coverage. It writes structured
notes with quality flags and source links; low-evidence records are explicitly
marked for later deep reading.
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

from zotero_collection_queue import list_collection_items, read_done_keys, ensure_log  # noqa: E402
from zotero_fetch import (  # noqa: E402
    add_online_supplements,
    assess_raw_data_quality,
    build_raw_buffer,
    connect_db,
    default_data_dir,
    fetch_from_sqlite,
)
from safety_io import guarded_append_line, guarded_write_text  # noqa: E402
from classification import (  # noqa: E402
    classify_core_variable,
    classify_methodology,
    classify_theme,
)
from template_renderer import discover_template, render_note  # noqa: E402


NOISE_RE = re.compile(
    r"(electronic copy available|all rights reserved|publisher and distributor|"
    r"telephone|fax|email|copyright|issn|nber working paper series)",
    re.I,
)


def sanitize_filename(value: str, max_len: int = 140) -> str:
    value = html.unescape(value or "Untitled")
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", value)
    value = re.sub(r"\s+", " ", value).strip().rstrip(".")
    return (value[:max_len].rstrip() or "Untitled") + ".md"


def yaml_quote(value: Any) -> str:
    text = "" if value is None else str(value)
    return json.dumps(text, ensure_ascii=False)


def yaml_bool(value: bool) -> str:
    return "true" if value else "false"


def yaml_list(values: list[str]) -> list[str]:
    if not values:
        return ["[]"]
    return [f"  - {yaml_quote(value)}" for value in values]


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def clean_text(value: str) -> str:
    value = value.replace("\x0c", "\n")
    value = re.sub(r"-\s*\n\s*", "", value)
    value = re.sub(r"\s+", " ", value)
    return html.unescape(value).strip()


def split_sentences(text: str) -> list[str]:
    text = clean_text(text)
    parts = re.split(r"(?<=[.!?。！？])\s+", text)
    return [p.strip() for p in parts if len(p.strip()) > 30]


def first_useful_sentences(text: str, count: int = 3) -> list[str]:
    sentences = []
    for sentence in split_sentences(text):
        if NOISE_RE.search(sentence):
            continue
        sentences.append(sentence)
        if len(sentences) >= count:
            break
    return sentences


def find_section(text: str, names: list[str], max_chars: int = 2500) -> str:
    lowered = text.lower()
    best = -1
    for name in names:
        for pattern in [f"\n{name.lower()}", f" {name.lower()} "]:
            idx = lowered.find(pattern)
            if idx >= 0 and (best < 0 or idx < best):
                best = idx
    if best < 0:
        return ""
    return clean_text(text[best : best + max_chars])


def authors(creators: list[dict[str, Any]]) -> str:
    names = []
    for creator in creators or []:
        first = creator.get("firstName") or ""
        last = creator.get("lastName") or ""
        names.append(" ".join([first, last]).strip() or last or first)
    return "; ".join([n for n in names if n])


def year_from_date(value: str | None) -> str:
    if not value:
        return ""
    match = re.search(r"(19|20)\d{2}", str(value))
    return match.group(0) if match else ""


def infer_theme(title: str) -> str:
    return classify_theme(title)


def infer_methodology(title: str, abstract: str, fulltext: str) -> str:
    return classify_methodology(title, abstract, fulltext)


def infer_core_variable(title: str, abstract: str) -> str:
    return classify_core_variable(title, abstract)


def quality_label(level: str) -> str:
    return {
        "local_fulltext": "本地全文缓存",
        "zotero_notes_or_annotations": "Zotero批注/笔记",
        "online_abstract": "在线摘要级",
        "metadata_only": "仅元数据",
    }.get(level, level)


def best_abstract(data: dict[str, Any], online: dict[str, Any]) -> str:
    local = strip_html(data.get("abstractNote") or data.get("abstract"))
    if local:
        return local
    for key in ("crossref", "openalex"):
        abstract = strip_html((online.get(key) or {}).get("abstract"))
        if abstract:
            return abstract
    return ""


def best_pdf_key(attachments: list[dict[str, Any]]) -> str:
    for attachment in attachments:
        if (attachment.get("contentType") or "").lower() == "application/pdf":
            return attachment.get("key") or ""
    return attachments[0].get("key") if attachments else ""


def first_fulltext(attachments: list[dict[str, Any]]) -> str:
    for attachment in attachments:
        cache = attachment.get("fulltext_cache") or ""
        if cache:
            return cache
    return ""


def first_pdf_page_link(pdf_key: str, page: int = 1) -> str:
    return f"zotero://open-pdf/library/items/{pdf_key}?page={page}" if pdf_key else ""


def source_link(item_key: str) -> str:
    return f"zotero://select/library/items/{item_key}"


def citation_key(data: dict[str, Any]) -> str:
    extra = data.get("extra") or ""
    for line in str(extra).splitlines():
        if line.lower().startswith("citation key:"):
            return line.split(":", 1)[1].strip()
    return str(data.get("citationKey") or "")


def evidence_profile(quality: dict[str, Any]) -> dict[str, Any]:
    level = quality.get("level") or "metadata_only"
    notes_count = int(quality.get("notes_count") or 0)
    annotations_count = int(quality.get("annotations_count") or 0)
    sources = {
        "metadata": True,
        "online_abstract": level == "online_abstract",
        "zotero_notes": level == "zotero_notes_or_annotations" and notes_count > 0,
        "zotero_annotations": level == "zotero_notes_or_annotations" and annotations_count > 0,
        "fulltext_cache": level == "local_fulltext",
        "pdf_human_checked": False,
    }
    if level == "metadata_only":
        return {
            "evidence_level": "E0",
            "citation_eligible": "false",
            "citation_status": "not_eligible",
            "usable_for": ["indexing", "triage", "reading_queue"],
            "evidence_sources": sources,
        }
    if level == "online_abstract":
        return {
            "evidence_level": "E1",
            "citation_eligible": "false",
            "citation_status": "not_eligible",
            "usable_for": ["screening", "topic_clustering", "reading_queue"],
            "evidence_sources": sources,
        }
    return {
        "evidence_level": "E2",
        "citation_eligible": "candidate",
        "citation_status": "candidate_needs_human_verification",
        "usable_for": ["literature_map_candidate", "mechanism_candidate", "citation_candidate"],
        "evidence_sources": sources,
    }


def frontmatter_lines(
    *,
    title: str,
    date: str,
    source: str,
    author_text: str,
    year: str,
    item: dict[str, Any],
    data: dict[str, Any],
    item_key: str,
    pdf_key: str,
    pdf_uri: str,
    collection: str,
    quality: dict[str, Any],
    workflow_tags: list[str],
    reading_stage: str,
    theme: str,
    study_area: str,
    data_source: str,
    methodology: str,
    core_variable: str,
    key_finding: str,
    relevance: str,
    limitations: str,
    follow_up_questions: list[str],
) -> list[str]:
    profile = evidence_profile(quality)
    evidence_sources = profile["evidence_sources"]
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        "aliases:",
        f"  - {yaml_quote(title)}",
        "tags:",
        *yaml_list(workflow_tags),
        f"created: {yaml_quote(date)}",
        "zotero:",
        f"  item_key: {yaml_quote(item_key)}",
        f"  pdf_key: {yaml_quote(pdf_key)}",
        f"  select_uri: {yaml_quote(source_link(item_key))}",
        f"  pdf_uri: {yaml_quote(pdf_uri)}",
        f"  item_type: {yaml_quote(item.get('itemType') or data.get('itemType'))}",
        f"  citekey: {yaml_quote(citation_key(data))}",
        f"  doi: {yaml_quote(data.get('DOI') or data.get('doi'))}",
        f"  url: {yaml_quote(data.get('url'))}",
        f"  source: {yaml_quote(source)}",
        f"  author: {yaml_quote(author_text)}",
        f"  year: {year or 'null'}",
        f"  publication: {yaml_quote(source)}",
        f"  abstract_present: {yaml_bool(bool(strip_html(data.get('abstractNote') or data.get('abstract'))))}",
        "zotero_collections:",
        f"  - {yaml_quote(collection)}",
        "zotero_tags: []",
        "obsidian_workflow_tags:",
        *yaml_list(workflow_tags),
        f"reading_stage: {yaml_quote(reading_stage)}",
        f"raw_data_quality: {yaml_quote(quality.get('level'))}",
        f"evidence_level: {yaml_quote(profile['evidence_level'])}",
        f"citation_eligible: {profile['citation_eligible']}",
        f"citation_status: {yaml_quote(profile['citation_status'])}",
        "usable_for:",
        *yaml_list(profile["usable_for"]),
        "evidence_sources:",
        f"  metadata: {yaml_bool(evidence_sources['metadata'])}",
        f"  online_abstract: {yaml_bool(evidence_sources['online_abstract'])}",
        f"  zotero_notes: {yaml_bool(evidence_sources['zotero_notes'])}",
        f"  zotero_annotations: {yaml_bool(evidence_sources['zotero_annotations'])}",
        f"  fulltext_cache: {yaml_bool(evidence_sources['fulltext_cache'])}",
        f"  pdf_human_checked: {yaml_bool(evidence_sources['pdf_human_checked'])}",
        "research_tags: []",
        "research_line: null",
        f"research_relevance: {yaml_quote(relevance)}",
        f"project_relevance: {yaml_quote(relevance)}",
        f"theme: {yaml_quote(theme)}",
        f"study_area: {yaml_quote(study_area)}",
        f"data_source: {yaml_quote(data_source)}",
        f"methodology: {yaml_quote(methodology)}",
        f"core_variable: {yaml_quote(core_variable)}",
        f"key_finding: {yaml_quote(key_finding)}",
        f"limitations: {yaml_quote(limitations)}",
        "follow_up_questions:",
        *yaml_list(follow_up_questions),
        "human_verified: false",
        "verified_at: null",
        "verified_by: null",
        "verification_notes: null",
        "---",
    ]
    return lines


def make_note(payload: dict[str, Any], collection: str) -> str:
    item = payload.get("item")
    if not isinstance(item, dict):
        raise ValueError("payload.item must be a mapping")
    nested_data = item.get("data")
    data = nested_data if isinstance(nested_data, dict) else item
    attachments = payload.get("attachments") or []
    if not isinstance(attachments, list):
        raise ValueError("payload.attachments must be a list")

    title = html.unescape(str(data.get("title") or "Untitled")).strip() or "Untitled"
    item_key = str(item.get("key") or "")
    pdf_key = best_pdf_key(attachments)
    pdf_uri = first_pdf_page_link(pdf_key)
    online = payload.get("online_supplements") or {}
    quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
    abstract = best_abstract(data, online)
    fulltext = first_fulltext(attachments)
    theme = infer_theme(title)
    methodology = infer_methodology(title, abstract, fulltext)
    core_variable = infer_core_variable(title, abstract)
    profile = evidence_profile(quality)

    evidence_sentences = first_useful_sentences(abstract or fulltext, 1)
    evidence_excerpt = evidence_sentences[0] if evidence_sentences else ""
    if evidence_excerpt:
        summary = f"> 自动初筛候选摘要：{evidence_excerpt}"
        conclusion = "\n".join(
            [
                "自动提取仅形成待核验候选，不构成正式可引用结论。",
                f"可追溯的文本片段为：{evidence_excerpt}",
                "",
                "该片段来自摘要或缓存文本，尚无稳定页码，需人工回到原文核验。",
            ]
        )
        key_finding = "现有文本提供了待人工核验的候选发现。"
    else:
        summary = "> 当前仅有元数据，无法形成可靠的内容摘要。"
        conclusion = "\n".join(
            [
                "证据不足，因此不生成发现。",
                "当前没有可核验的摘要、注释或全文片段。",
            ]
        )
        key_finding = "证据不足，未生成研究发现。"

    source = str(data.get("publicationTitle") or data.get("publisher") or "")
    author_text = authors(data.get("creators") or [])
    year = year_from_date(data.get("date"))
    limitations = "自动初筛未经人工核验，不得作为 E3 正式引用证据。"
    frontmatter = frontmatter_lines(
        title=title,
        date=datetime.now().strftime("%Y-%m-%d"),
        source=source,
        author_text=author_text,
        year=year,
        item=item,
        data=data,
        item_key=item_key,
        pdf_key=pdf_key,
        pdf_uri=pdf_uri,
        collection=collection,
        quality=quality,
        workflow_tags=["literature-note", "reading-note", "first-pass"],
        reading_stage="初录入",
        theme=theme,
        study_area="论文界定的分析主体、地区或样本范围，待人工核验。",
        data_source="当前可用元数据、摘要、Zotero 笔记或全文缓存。",
        methodology=methodology,
        core_variable=core_variable,
        key_finding=key_finding,
        relevance="用于文献索引、主题初筛和后续精读排队。",
        limitations=limitations,
        follow_up_questions=["需要核验原文方法、数据和结论的准确表述。"],
    )

    item_link = source_link(item_key) if item_key else ""
    sections = {
        "metadata": "\n\n".join(
            [
                f"署名记录为 {author_text or '未提供'}，年代记录为 {year or '未提供'}，载体记录为 {source or '未提供'}。",
                f"自动分类得到 {theme}。Zotero 入口为 {item_link or '未提供'}，PDF 入口为 {pdf_uri or '未提供'}。",
                f"当前自动证据级别为 {profile['evidence_level']}，使用门槛为 {profile['citation_status']}。",
            ]
        ),
        "summary": summary,
        "subject": (
            "论文界定的主体或空间单元仍待全文核验。"
            f"目前仅能识别出“{theme}”这一议题线索，无法确认精确适用范围。"
        ),
        "method": (
            f"自动分类结果为 {methodology}。该结果依据标题和现有文本生成，"
            f"尚未完成人工原文核验。{limitations}"
        ),
        "data": (
            "材料形态、时间跨度和样本规模均待人工核验。现有元数据没有提供"
            "可稳定核验的样本线索，因此不得据此推断精确样本。"
        ),
        "findings": conclusion,
        "assessment": (
            f"该记录目前是 {collection} 文献的初筛候选，可复用线索为 {methodology}。"
            "其实际价值需要精读后判断，并应核查方法、样本和结论能否由原文直接支持。"
        ),
        "evidence_status": (
            f"当前等级为 {profile['evidence_level']}，使用门槛为 {profile['citation_status']}。"
            "材料可用于索引、初筛和精读排队；在人工确认完成前，不得用于正式引文、"
            "精确页码或强结论。"
        ),
    }
    return render_note(
        template_path=discover_template(__file__),
        frontmatter=frontmatter,
        title=title,
        sections=sections,
    )

def append_log(log_file: Path, status: str, key: str, title: str, *, write: bool) -> dict[str, object]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return guarded_append_line(
        log_file,
        f"- [x] {timestamp} | {status} | {key} | {title}\n",
        write=write,
    ).to_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--note-root", type=Path, default=Path(r"<note_root>"))
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Limit items for testing")
    parser.add_argument("--online-email")
    parser.add_argument("--skip-unpaywall", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Read-only plan mode. This never creates directories, logs, reports, or notes.")
    parser.add_argument("--write", action="store_true", help="Allow note/log/report writes.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing note.")
    parser.add_argument("--no-overwrite", dest="overwrite", action="store_false", help="Skip existing notes. This is the default.")
    parser.add_argument("--backup", dest="backup", action="store_true", default=True, help="Create a timestamped backup before overwrite. Default.")
    parser.add_argument("--no-backup", dest="backup", action="store_false", help="Do not create backups before overwrite.")
    parser.add_argument("--diff", dest="diff", action="store_true", default=True, help="Include diff summaries for updates. Default.")
    parser.add_argument("--no-diff", dest="diff", action="store_false", help="Suppress diff summaries.")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    effective_write = args.write and not args.dry_run

    target_dir = args.note_root / args.collection
    log_file = target_dir / "_ProcessLog_进度记录.md"
    log_init = ensure_log(log_file, args.collection, write=effective_write)
    done = read_done_keys(log_file)

    conn = connect_db(args.data_dir)
    try:
        items = list_collection_items(conn, args.collection, args.recursive)
    finally:
        conn.close()

    queue = [item for item in items if item["key"] not in done]
    if args.limit > 0:
        queue = queue[: args.limit]

    report = {
        "collection": args.collection,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "write": effective_write,
        "overwrite": args.overwrite,
        "backup": args.backup,
        "log_init": log_init,
        "total_items": len(items),
        "initial_done": len(done),
        "queued": len(queue),
        "success": 0,
        "failed": 0,
        "quality_counts": {},
        "items": [],
    }

    for index, item in enumerate(queue, start=1):
        key = item["key"]
        title = html.unescape(item.get("title") or key)
        note_path = target_dir / sanitize_filename(title)
        try:
            payload = fetch_from_sqlite(args.data_dir, key, None)
            quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
            if quality.get("needs_fulltext_for_deep_reading"):
                payload = add_online_supplements(
                    payload,
                    email=args.online_email,
                    skip_unpaywall=args.skip_unpaywall,
                )
                quality = payload.get("raw_data_quality") or quality
            else:
                payload["raw_data_quality"] = quality
                payload["raw_data_buffer"] = build_raw_buffer(payload)
            write_result = guarded_write_text(
                note_path,
                make_note(payload, args.collection),
                write=effective_write,
                overwrite=args.overwrite,
                backup=args.backup,
                diff=args.diff,
            )
            status = write_result.status
            log_result = None
            if status in {"created", "updated"}:
                log_result = append_log(log_file, "✅ 成功", key, title, write=effective_write)
                report["success"] += 1
            elif status == "skipped_existing":
                log_result = append_log(log_file, "⚠️ 跳过", key, title, write=effective_write)
            level = (quality or {}).get("level", "unknown")
            report["quality_counts"][level] = report["quality_counts"].get(level, 0) + 1
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": title,
                    "status": status,
                    "quality": level,
                    "path": str(note_path),
                    "write_result": write_result.to_dict(),
                    "log_result": log_result,
                }
            )
            print(f"[{index}/{len(queue)}] {status} | {level} | {key} | {title}", flush=True)
        except Exception as exc:
            report["failed"] += 1
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": title,
                    "status": "failed",
                    "error": str(exc),
                }
            )
            append_log(log_file, f"❌ 失败（{exc}）", key, title, write=effective_write)
            print(f"[{index}/{len(queue)}] failed | {key} | {exc}", flush=True)

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
