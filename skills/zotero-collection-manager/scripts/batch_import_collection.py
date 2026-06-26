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
    lower = title.lower()
    if "hank" in lower:
        return "异质主体宏观模型与政策传导"
    if "migration" in lower or "commuting" in lower:
        return "人口迁移与空间劳动力配置"
    if "housing" in lower:
        return "住房约束与空间资源错配"
    if "spatial" in lower or "geography" in lower:
        return "空间结构与宏观经济政策"
    if "monetary" in lower:
        return "货币政策传导与区域异质性"
    if "climate" in lower:
        return "气候冲击与宏观经济"
    return "空间宏观经济与异质性分析"


def infer_methodology(title: str, abstract: str, fulltext: str) -> str:
    haystack = " ".join([title, abstract, fulltext[:8000]]).lower()
    if "gravity" in haystack:
        return "引力模型与迁移流估计"
    if "hank" in haystack:
        return "HANK模型与政策冲击分析"
    if "dynamic spatial" in haystack or "spatial general equilibrium" in haystack:
        return "动态空间一般均衡模型"
    if "deep learning" in haystack or "neural" in haystack:
        return "深度学习近似动态规划"
    if "difference-in-differences" in haystack or "instrument" in haystack:
        return "准实验识别与计量估计"
    if "model" in haystack:
        return "结构模型与数值模拟"
    return "文献综述或理论分析"


def infer_core_variable(title: str, abstract: str) -> str:
    haystack = " ".join([title, abstract]).lower()
    if "migration" in haystack:
        return "迁移流、城市便利性和就业机会"
    if "commuting" in haystack:
        return "通勤联系、本地就业弹性和福利"
    if "housing" in haystack:
        return "住房供给、价格约束和就业增长"
    if "monetary" in haystack:
        return "货币政策冲击、收入分布和消费响应"
    if "hank" in haystack:
        return "家庭异质性、资产分布和政策传导"
    return "空间分布、异质性和政策响应"


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
    item = payload["item"]
    data = item.get("data") or {}
    title = html.unescape(data.get("title") or "Untitled")
    item_key = item.get("key") or ""
    attachments = payload.get("attachments") or []
    pdf_key = best_pdf_key(attachments)
    online = payload.get("online_supplements") or {}
    quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
    abstract = best_abstract(data, online)
    fulltext = first_fulltext(attachments)
    intro = find_section(fulltext, ["introduction"])
    methods = find_section(
        fulltext,
        ["model", "method", "methods", "data", "empirical strategy", "quantitative model"],
    )
    conclusion = find_section(fulltext, ["conclusion", "concluding remarks", "discussion"])
    evidence_source = conclusion or abstract or intro or fulltext
    findings = first_useful_sentences(evidence_source, 3)
    method_sentences = first_useful_sentences(methods or intro or abstract, 3)
    date = datetime.now().strftime("%Y-%m-%d")
    year = year_from_date(data.get("date")) or str(data.get("year") or "")
    author_text = authors(data.get("creators") or [])
    source = data.get("publicationTitle") or data.get("publisher") or data.get("libraryCatalog") or ""
    theme = infer_theme(title)
    methodology = infer_methodology(title, abstract, fulltext)
    core_variable = infer_core_variable(title, abstract)
    key_finding = "；".join([clean_text(s)[:36] for s in findings[:2]]) or "需补充全文后确认核心结论"
    if len(key_finding) > 70:
        key_finding = key_finding[:70]
    relevance = f"为{collection}主题文献整理提供参考"
    data_source = "全文缓存与Zotero元数据" if fulltext else "Zotero元数据与公开摘要"
    study_area = "论文研究对象或模型样本"
    if any(k in title.lower() + " " + abstract.lower() for k in ["china", "chinese"]):
        study_area = "中国城市或省际样本"
    elif "united states" in (title.lower() + " " + abstract.lower()) or "u.s." in (
        title.lower() + " " + abstract.lower()
    ):
        study_area = "美国地区或城市样本"
    elif "model" in (title.lower() + " " + abstract.lower()) or "hank" in title.lower():
        study_area = "理论模型或数值经济体"

    pdf_uri = first_pdf_page_link(pdf_key, 1)
    limitations = "本条为批量初录入笔记，关键公式、估计细节和页码证据需后续人工精读校验。"
    follow_up_questions = ["该文如何处理空间结构、异质主体和一般均衡反馈之间的关系？"]
    lines: list[str] = frontmatter_lines(
        title=title,
        date=date,
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
        workflow_tags=["literature-note", "reading-note", "auto-imported"],
        reading_stage="初录入",
        theme=theme,
        study_area=study_area,
        data_source=data_source,
        methodology=methodology,
        core_variable=core_variable,
        key_finding=key_finding,
        relevance=relevance,
        limitations=limitations,
        follow_up_questions=follow_up_questions,
    )
    lines.extend(
        [
            "",
            f"# {title}",
            "",
            "## 基本信息",
            "",
            "| 项目 | 内容 |",
            "| --- | --- |",
            f"| 作者 | {author_text} |",
            f"| 年份 | {year} |",
            f"| 来源 | {source} |",
            f"| 主题 | {theme} |",
            f"| 语料等级 | {quality_label(quality.get('level', ''))} |",
            f"| Zotero 条目 | {source_link(item_key)} |",
            f"| PDF 链接 | {pdf_uri or '本地无PDF'} |",
            f"| 证据等级 | {evidence_profile(quality)['evidence_level']} |",
            f"| 引用资格 | {evidence_profile(quality)['citation_status']} |",
            "",
            "## 一句话摘要",
            "",
        ]
    )
    if abstract:
        lines.append(f"> {clean_text(abstract)[:420]}")
    else:
        lines.append("> 当前仅有元数据，缺少摘要或全文，需补充材料后精读。")

    lines.extend(
        [
            "",
            "## 研究对象",
            "",
            f"- **研究对象**：{study_area}。",
            f"- **核心问题**：{theme}。",
            f"- **研究情境/范围**：{collection} 相关文献。",
            "",
            "## 研究方法",
            "",
            "### 方法概述",
            "",
            f"- **方法类型**：{methodology}。",
            f"- **总体思路**：{method_sentences[0] if method_sentences else '待基于完整正文进一步提炼。'}",
            f"- **为什么用这种方法**：{method_sentences[1] if len(method_sentences) > 1 else '用于处理空间异质性、主体异质性或政策传导问题。'}",
            "",
            "### 方法分析",
            "",
            f"- **分析单位**：{study_area}。",
            f"- **关键变量/概念**：{core_variable}。",
            "- **识别/推断逻辑**：根据当前语料提取，后续精读时需进一步核对模型设定、识别假设和稳健性。",
            f"- **具体步骤**：{method_sentences[2] if len(method_sentences) > 2 else '自动录入阶段暂未完整解析所有步骤。'}",
            f"- **方法优势**：适合纳入 {collection} 主题下比较相关理论、方法与经验证据。",
            f"- **方法局限**：{limitations}",
            "",
            "## 数据来源",
            "",
            f"- **数据类型**：{data_source}。",
            f"- **样本来源**：{study_area}。",
            "- **时间范围**：自动录入阶段未稳定识别。",
            "- **样本量/案例数**：自动录入阶段未稳定识别。",
            f"- **数据局限**：语料等级为 {quality_label(quality.get('level', ''))}；若为摘要级或元数据级，不应用于强结论引用。",
            "",
            "## 研究结论",
            "",
        ]
    )
    if findings:
        for idx, sentence in enumerate(findings, start=1):
            lines.append(f"- **主要发现 {idx}**：{clean_text(sentence)[:260]}")
            if pdf_key:
                lines.append(f"- **原文依据 {idx}**：{first_pdf_page_link(pdf_key, 1)}")
            else:
                lines.append(f"- **原文依据 {idx}**：无本地 PDF；依据在线摘要或元数据，需补全文复核。")
            lines.append("")
    else:
        lines.extend(
            [
                "- **主要发现 1**：当前语料不足，暂不生成实质性结论。",
                "- **原文依据 1**：无可复核全文依据。",
                "",
            ]
        )

    lines.extend(
        [
            "## 我的判断",
            "",
            f"- **最有启发的点**：{relevance}。",
            f"- **可借鉴的方法**：{methodology}。",
            "- **可继续追问的问题**：该文如何处理空间结构、异质主体和一般均衡反馈之间的关系？",
            f"- **与我的研究关联**：可作为 {collection} 文献库的初筛条目，后续按研究重要性精读。",
            "",
            "## 自动录入状态",
            "",
            f"- **录入时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **语料等级**：{quality_label(quality.get('level', ''))}",
            f"- **全文缓存字符数**：{quality.get('fulltext_cache_chars', 0)}",
            f"- **Zotero批注数**：{quality.get('annotations_count', 0)}",
            f"- **Zotero笔记数**：{quality.get('notes_count', 0)}",
            f"- **需要后续精读**：{'是' if quality.get('needs_fulltext_for_deep_reading') else '否'}",
        ]
    )
    warnings = (online.get("warnings") or []) if isinstance(online, dict) else []
    if warnings:
        lines.append(f"- **在线补抓警告**：{'；'.join(warnings)}")
    return "\n".join(lines) + "\n"


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
