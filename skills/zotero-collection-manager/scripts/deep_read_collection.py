#!/usr/bin/env python3
"""Second-pass deep-reading upgrade for an imported Zotero collection.

The script only upgrades items with local PDF/full-text evidence. It rewrites
the matching Obsidian note in place and records a separate deep-reading log so
the first-pass import log remains intact.
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
    authors,
    best_abstract,
    best_pdf_key,
    clean_text,
    evidence_profile,
    first_pdf_page_link,
    frontmatter_lines,
    infer_core_variable,
    infer_methodology,
    infer_theme,
    sanitize_filename,
    source_link,
    split_sentences,
    strip_html,
    yaml_quote,
    year_from_date,
)
from zotero_collection_queue import list_collection_items  # noqa: E402
from zotero_fetch import (  # noqa: E402
    assess_raw_data_quality,
    connect_db,
    default_data_dir,
    fetch_from_sqlite,
)
from safety_io import guarded_append_line, guarded_write_text  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


SECTION_HEAD_RE = re.compile(
    r"(?im)^\s*(?:\d+(?:\.\d+)*\s+)?"
    r"(abstract|introduction|background|literature review|model|theory|data|"
    r"empirical strategy|estimation|calibration|quantitative model|results|"
    r"counterfactual|discussion|conclusion|concluding remarks|references|appendix)"
    r"\s*$"
)
NOISE_RE = re.compile(
    r"(all rights reserved|electronic copy available|copyright|doi:|"
    r"journal homepage|appendix table|references|bibliography|issn|isbn)",
    re.I,
)
METHOD_WORDS = {
    "model",
    "equilibrium",
    "estimate",
    "estimation",
    "identify",
    "identification",
    "calibrate",
    "calibration",
    "simulate",
    "simulation",
    "counterfactual",
    "gravity",
    "hank",
    "heterogeneous",
    "dynamic",
    "spatial",
    "migration",
    "elasticity",
    "instrument",
    "difference-in-differences",
}
DATA_WORDS = {
    "data",
    "sample",
    "census",
    "survey",
    "panel",
    "county",
    "city",
    "region",
    "state",
    "worker",
    "household",
    "firm",
    "year",
    "period",
}
FINDING_WORDS = {
    "find",
    "shows",
    "show",
    "result",
    "results",
    "imply",
    "implies",
    "effect",
    "increase",
    "decrease",
    "welfare",
    "gains",
    "decline",
    "higher",
    "lower",
    "important",
    "substantial",
    "significant",
}
RESULT_ANCHOR_RE = re.compile(
    r"\b(we find|we show|we estimate|our results|results show|results suggest|"
    r"find that|show that|suggest that|imply that|demonstrate that|"
    r"counterfactual|welfare gains?|main finding)\b",
    re.I,
)
REFERENCE_START_RE = re.compile(r"(?im)^\s*(references|bibliography)\s*$")
PDF_HEADER_RE = re.compile(
    r"(journal homepage|to cite this article|article views|view related articles|"
    r"published online|submit your article|contact .+@|issn:|copyright|"
    r"terms and conditions of use|downloaded by|all rights reserved)",
    re.I,
)


def normalize_ws(value: str) -> str:
    value = html.unescape(value or "")
    value = value.replace("\x0c", "\n")
    ref_match = REFERENCE_START_RE.search(value)
    if ref_match:
        value = value[: ref_match.start()]
    cleaned_lines = []
    for line in value.splitlines():
        if PDF_HEADER_RE.search(line):
            continue
        cleaned_lines.append(line)
    value = "\n".join(cleaned_lines)
    value = re.sub(r"-\s*\n\s*", "", value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def fulltext_from_payload(payload: dict[str, Any]) -> tuple[str, str, str]:
    for attachment in payload.get("attachments") or []:
        if (attachment.get("contentType") or "").lower() != "application/pdf":
            continue
        text = attachment.get("fulltext_cache") or ""
        if text:
            return normalize_ws(text), attachment.get("key") or "", attachment.get("path") or ""
    for attachment in payload.get("attachments") or []:
        text = attachment.get("fulltext_cache") or ""
        if text:
            return normalize_ws(text), attachment.get("key") or "", attachment.get("path") or ""
    return "", "", ""


def has_existing_pdf(payload: dict[str, Any]) -> bool:
    for attachment in payload.get("attachments") or []:
        if (attachment.get("contentType") or "").lower() != "application/pdf":
            continue
        path = attachment.get("path") or ""
        if path and Path(path).exists():
            return True
    return False


def split_sections(text: str) -> dict[str, str]:
    matches = list(SECTION_HEAD_RE.finditer(text))
    if not matches:
        return {"body": clean_text(text[:12000])}
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = match.group(1).lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = clean_text(text[start:end])
        if len(chunk) > 80 and name not in sections:
            sections[name] = chunk[:9000]
    return sections


def section_text(sections: dict[str, str], names: list[str], fallback: str = "") -> str:
    for name in names:
        if sections.get(name):
            return sections[name]
    return fallback


def score_sentence(sentence: str, words: set[str]) -> int:
    lower = sentence.lower()
    return sum(1 for word in words if word in lower)


def useful_sentences(text: str, words: set[str], count: int = 4) -> list[str]:
    candidates = []
    for sentence in split_sentences(text):
        sentence = clean_text(sentence)
        if len(sentence) < 45 or len(sentence) > 520 or NOISE_RE.search(sentence):
            continue
        score = score_sentence(sentence, words)
        candidates.append((score, sentence))
    ranked = sorted(candidates, key=lambda item: (-item[0], len(item[1])))
    picked: list[str] = []
    seen: set[str] = set()
    for score, sentence in ranked:
        marker = sentence[:80].lower()
        if marker in seen:
            continue
        if score <= 0 and len(picked) >= 1:
            continue
        seen.add(marker)
        picked.append(sentence)
        if len(picked) >= count:
            break
    return picked


def result_sentences(text: str, count: int = 5) -> list[str]:
    picked: list[str] = []
    seen: set[str] = set()
    for sentence in split_sentences(text):
        sentence = clean_text(sentence)
        if len(sentence) < 60 or len(sentence) > 520 or NOISE_RE.search(sentence):
            continue
        if not RESULT_ANCHOR_RE.search(sentence):
            continue
        marker = sentence[:80].lower()
        if marker in seen:
            continue
        seen.add(marker)
        picked.append(sentence)
        if len(picked) >= count:
            break
    return picked


def finding_summary(sentence: str, title: str, theme: str, idx: int) -> str:
    lower = f"{title} {sentence}".lower()
    if "welfare" in lower:
        return "地区差异会改变政策或空间调整的福利归宿。"
    if "migration" in lower or "commuting" in lower:
        return "迁移和通勤是地区冲击传播与劳动力再配置的核心渠道。"
    if "housing" in lower or "land" in lower:
        return "住房或土地约束会放大空间错配并影响就业增长。"
    if "trade" in lower or "tariff" in lower:
        return "贸易冲击通过劳动力与产业重新配置影响地区收入。"
    if "monetary" in lower or "fiscal" in lower or "multiplier" in lower:
        return "宏观政策冲击在地区之间呈现显著异质性。"
    if "climate" in lower or "carbon" in lower:
        return "气候政策的宏观影响取决于部门和地区间再分配。"
    if "model" in lower or "equilibrium" in lower or "hank" in lower:
        return "一般均衡反馈会改变局部冲击的总量与分布效应。"
    if idx == 1:
        return f"论文的核心发现服务于“{theme}”这一问题。"
    return "结论强调空间异质性会系统性影响宏观经济结果。"


def quote_excerpt(sentence: str, max_words: int = 22) -> str:
    words = clean_text(sentence).split()
    if len(words) <= max_words:
        return " ".join(words)
    return " ".join(words[:max_words]).rstrip(",;:") + "..."


def chinese_topic(title: str, abstract: str, fulltext: str, collection: str = "") -> tuple[str, str, str, str]:
    collection_lower = collection.lower()
    title_lower = title.lower()
    haystack = f"{title} {abstract} {fulltext[:8000]}".lower()
    if "因果" in collection:
        if "double" in title_lower or "debiased" in title_lower or "orthogonal" in title_lower:
            methodology = "正交化机器学习与双重机器学习"
        elif "forest" in title_lower:
            methodology = "因果森林与异质处理效应估计"
        elif "meta-learner" in title_lower or "treatment effect" in title_lower:
            methodology = "元学习器与个体处理效应估计"
        elif "recursive partitioning" in title_lower or "mob" in title_lower or "partykit" in title_lower:
            methodology = "模型递归分割与子群识别"
        else:
            methodology = "因果机器学习与处理效应估计"
        return (
            "因果效应识别与异质性估计",
            "观测数据、实验数据或模拟处理效应任务",
            methodology,
            "处理变量、结果变量和条件平均处理效应",
        )
    if "结构化ml" in collection_lower or "结构化" in collection:
        if "set" in title_lower:
            methodology = "集合不变神经网络与注意力机制"
            core = "集合元素、置换不变性和注意力表示"
        elif "graph" in title_lower or "message passing" in title_lower:
            methodology = "图神经网络与消息传递"
            core = "节点、边、图结构和消息聚合"
        elif "fourier" in title_lower or "operator" in title_lower:
            methodology = "神经算子与频域函数逼近"
            core = "函数输入、算子映射和频域卷积"
        elif "geometric" in title_lower:
            methodology = "几何深度学习统一框架"
            core = "对称性、等变性和几何结构"
        else:
            methodology = "结构化表示学习"
            core = "结构约束、归纳偏置和神经表示"
        return (
            "结构化数据上的深度学习建模",
            "集合、图、几何结构或物理系统任务",
            methodology,
            core,
        )
    if "hank" in collection_lower or "spartial" in collection_lower or "urhank" in collection_lower:
        # Fall through to the existing spatial-macro heuristics.
        pass
    elif collection == "未归类":
        return (
            "未归类文献的主题初筛",
            "论文自身定义的研究对象或应用场景",
            infer_methodology(title, abstract, fulltext),
            infer_core_variable(title, abstract),
        )
    if is_review_article(title, abstract, fulltext):
        return (
            "空间宏观经济学文献整合",
            "空间宏观经济学文献与专题论文",
            "专题综述与文献整合",
            "空间一般均衡、地区政策和宏观冲击",
        )
    theme = infer_theme(title)
    methodology = infer_methodology(title, abstract, fulltext)
    core_variable = infer_core_variable(title, abstract)
    haystack = f"{title} {abstract}".lower()
    if "china" in haystack or "chinese" in haystack:
        study_area = "中国城市、地区或迁移样本"
    elif "united states" in haystack or "u.s." in haystack or "us " in haystack:
        study_area = "美国地区、州或劳动力市场"
    elif "indonesia" in haystack:
        study_area = "印度尼西亚地区迁移样本"
    elif "model" in haystack or "equilibrium" in haystack or "hank" in haystack:
        study_area = "理论经济体与数值模型"
    else:
        study_area = "地区、城市或空间经济单元"
    return theme, study_area, methodology, core_variable


def collection_context(collection: str) -> dict[str, str]:
    if "因果" in collection:
        return {
            "intro": "该文服务于因果推断和异质处理效应估计，重点在识别、正交化、泛化误差或子群结构。",
            "reason": "该方法适合在高维协变量和复杂异质性下估计可解释的因果参数。",
            "logic": "通过识别假设、正交化估计、样本拆分或模型比较来支撑处理效应推断。",
            "steps": "先界定处理效应目标和识别假设，再构造机器学习估计器，最后评估误差、稳健性或应用表现。",
            "advantage": "能够把现代机器学习的预测能力转化为更稳健的因果参数估计。",
            "relevance": "连接计量识别、机器学习预测和异质性分析",
            "question": "该文的识别假设、正交化结构或异质性估计能否用于当前经验研究设计？",
            "relation": f"可作为 {collection} 文献库中连接计量识别和机器学习方法的核心条目。",
        }
    if "结构化ML" in collection or "结构化" in collection:
        return {
            "intro": "该文关注结构化对象的神经表示，重点是集合、图、几何结构、算子或物理系统中的归纳偏置。",
            "reason": "该方法适合利用数据自身的对称性、连接关系或函数结构来提升泛化能力。",
            "logic": "通过结构约束、模型架构和任务实验说明归纳偏置如何改变表示学习效果。",
            "steps": "先刻画输入结构和不变性/等变性，再设计网络算子或聚合机制，最后在标准任务或物理系统上验证。",
            "advantage": "能够把结构信息显式嵌入模型，减少纯黑箱建模对样本规模的依赖。",
            "relevance": "提供结构化表示学习的架构原则和归纳偏置",
            "question": "该文的结构约束、聚合机制或等变设计能否迁移到经济网络、区域系统或动态状态表示？",
            "relation": f"可作为 {collection} 文献库中理解结构化神经网络的核心条目。",
        }
    if collection == "未归类":
        return {
            "intro": "该文暂未归入具体主题，二次精读主要用于保留可检索的核心问题、方法和证据。",
            "reason": "该方法适合围绕论文自身问题组织证据，便于后续决定是否迁入正式主题目录。",
            "logic": "依据论文的模型、数据、实验或论证结构提炼核心结论。",
            "steps": "先识别研究问题，再提炼方法和证据，最后判断与现有研究库的潜在连接。",
            "advantage": "能够为后续主题归档提供可比较的摘要和证据入口。",
            "relevance": "为后续主题归档提供初步判断依据",
            "question": "该文应归入哪个正式研究主题，还是保留为背景材料？",
            "relation": "可作为未归类文献池中的候选条目，后续按研究用途迁移。",
        }
    return {
        "intro": "该文从空间或异质性维度组织宏观经济问题，关注地区之间的差异、流动摩擦和政策传导。",
        "reason": "该方法适合同时处理地区异质性、主体差异和政策冲击的反馈效应。",
        "logic": "依据模型结构、估计/校准结果或反事实比较来支持结论。",
        "steps": "先构造空间或异质主体框架，再估计/校准关键参数，最后比较政策或冲击下的响应。",
        "advantage": "能够把地区间调整、迁移/住房/贸易摩擦和宏观冲击的分布效应联动起来。",
        "relevance": "连接空间异质性、地区调整与宏观传导",
        "question": f"该文的核心方法或证据能否嵌入 {collection} 的问题体系？",
        "relation": f"可作为 {collection} 文献库中连接理论、方法与证据的候选基础文献。",
    }


def is_review_article(title: str, abstract: str, fulltext: str) -> bool:
    haystack = f"{title} {abstract} {fulltext[:8000]}".lower()
    return (
        "review" in title.lower()
        or "spatial macroeconomics" == title.strip().lower()
        or "special issue" in haystack
        or "the papers in this issue" in haystack
    )


def data_source_label(data_sentences: list[str], title: str, collection: str = "") -> str:
    if "因果" in collection:
        return "模拟实验、经验应用或公开基准数据"
    if "结构化ML" in collection or "结构化" in collection:
        if "theory" in title.lower() or "deep sets" in title.lower():
            return "理论构造与机器学习基准任务"
        return "基准任务、模型实验或物理系统数据"
    if collection == "未归类":
        return "论文自身使用的数据、模型或案例材料"
    if is_review_article(title, "", ""):
        return "文献综述与专题论文"
    joined = " ".join(data_sentences).lower()
    if "census" in joined:
        return "人口普查与地区面板数据"
    if "survey" in joined:
        return "调查数据与地区经济指标"
    if "county" in joined or "city" in joined or "state" in joined:
        return "地区面板与城市统计数据"
    if "calibration" in joined or "simulate" in joined:
        return "校准参数与数值模拟样本"
    if "model" in title.lower():
        return "模型校准与文献参数"
    return "全文缓存识别的数据与模型信息"


def compact_field_from_finding(sentence: str, title: str, theme: str) -> str:
    if is_review_article(title, "", ""):
        return "梳理空间宏观经济学的核心议题与模型谱系。"
    return finding_summary(sentence, title, theme, 1)


def find_existing_note_by_key(target_dir: Path, key: str) -> Path | None:
    patterns = [
        re.compile(rf'(?m)^\s*item_key:\s*"{re.escape(key)}"\s*$'),
        re.compile(rf"(?m)^\s*item_key:\s*{re.escape(key)}\s*$"),
    ]
    for path in sorted(target_dir.glob("*.md")):
        if path.name.startswith("_ProcessLog_"):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")[:3000]
        if any(pattern.search(text) for pattern in patterns):
            return path
    return None


def make_deep_note(payload: dict[str, Any], collection: str) -> str:
    item = payload["item"]
    data = item.get("data") or {}
    title = html.unescape(data.get("title") or "Untitled")
    item_key = item.get("key") or ""
    attachments = payload.get("attachments") or []
    pdf_key = best_pdf_key(attachments)
    fulltext, evidence_pdf_key, pdf_path = fulltext_from_payload(payload)
    if evidence_pdf_key:
        pdf_key = evidence_pdf_key
    quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
    abstract = best_abstract(data, payload.get("online_supplements") or {})
    if not abstract:
        abstract = section_text(split_sections(fulltext), ["abstract"])
    sections = split_sections(fulltext)
    intro = section_text(sections, ["introduction", "background", "literature review"], fulltext[:6000])
    method_text = section_text(
        sections,
        ["model", "theory", "empirical strategy", "estimation", "calibration", "quantitative model"],
        intro,
    )
    data_text = section_text(sections, ["data"], method_text)
    result_text = section_text(
        sections,
        ["results", "counterfactual", "discussion", "conclusion", "concluding remarks"],
        fulltext[-9000:],
    )
    conclusion_text = section_text(sections, ["conclusion", "concluding remarks"], result_text)

    method_sentences = useful_sentences(method_text, METHOD_WORDS, 4)
    data_sentences = useful_sentences(data_text, DATA_WORDS, 3)
    finding_sentences = result_sentences(conclusion_text or result_text, 5)
    if len(finding_sentences) < 3:
        finding_sentences.extend(result_sentences(result_text + " " + intro, 5))
        deduped = []
        seen = set()
        for sentence in finding_sentences:
            marker = sentence[:80].lower()
            if marker not in seen:
                seen.add(marker)
                deduped.append(sentence)
        finding_sentences = deduped[:5]

    theme, study_area, methodology, core_variable = chinese_topic(title, abstract, fulltext, collection)
    context = collection_context(collection)
    data_source = data_source_label(data_sentences, title, collection)
    review_like = is_review_article(title, abstract, fulltext)
    key_finding = (
        compact_field_from_finding(finding_sentences[0], title, theme)
        if finding_sentences
        else "全文缓存未稳定识别结论，需人工复核"
    )
    relevance = context["relevance"]
    author_text = authors(data.get("creators") or [])
    year = year_from_date(data.get("date")) or str(data.get("year") or "")
    source = data.get("publicationTitle") or data.get("publisher") or data.get("libraryCatalog") or ""
    date = datetime.now().strftime("%Y-%m-%d")
    deep_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf_link = first_pdf_page_link(pdf_key, 1) or "本地无PDF"

    intro_context = (
        context["intro"]
        if not intro or review_like
        else quote_excerpt(intro, 24)
    )
    method_overview = f"以{methodology}为主线，将{core_variable}放入“{theme}”的框架中比较。"
    method_reason = (
        "综述类文章的目标是建立概念边界和文献谱系，而不是估计单一因果效应。"
        if review_like
        else context["reason"]
    )
    infer_logic = (
        "通过归纳不同模型和应用场景，说明空间维度如何改变宏观经济推断。"
        if review_like
        else context["logic"]
    )
    concrete_steps = (
        "先界定研究领域，再整理代表性模型与应用，最后提炼未来可扩展的问题。"
        if review_like
        else context["steps"]
    )
    data_sample = (
        "文献与专题论文；无统一实证样本。"
        if review_like
        else f"{study_area}；具体样本边界需回到 PDF 数据段复核。"
    )
    data_period = "不适用，综述类文章无统一时间范围。" if review_like else "全文缓存未稳定识别，需要查阅正文数据段。"
    data_n = "不适用，综述类文章无统一样本量。" if review_like else "全文缓存未稳定识别。"

    limitations = "自动精读基于 Zotero 全文缓存，公式和页码没有逐页人工复核；关键估计设定仍需后续重点核对。"
    follow_up_questions = [context["question"]]
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
        pdf_uri=first_pdf_page_link(pdf_key, 1),
        collection=collection,
        quality=quality,
        workflow_tags=["literature-note", "reading-note", "deep-read"],
        reading_stage="二次精读",
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
        f"| Zotero 条目 | {source_link(item_key)} |",
        f"| PDF 链接 | {pdf_link} |",
        f"| 证据等级 | {evidence_profile(quality)['evidence_level']} |",
        f"| 引用资格 | {evidence_profile(quality)['citation_status']} |",
        f"| 本地 PDF | {pdf_path or 'Zotero 已记录 PDF 附件；路径未解析'} |",
        "",
        "## 一句话摘要",
        "",
        f"> 本文围绕“{theme}”，使用{methodology}分析{study_area}中的{core_variable}，核心价值在于{relevance}。",
        "",
        "## 研究对象",
        "",
        f"- **研究对象**：{study_area}。",
        f"- **核心问题**：{theme}。",
        f"- **研究情境/范围**：{intro_context}",
        "",
        "## 研究方法",
        "",
        "### 方法概述",
        "",
        f"- **方法类型**：{methodology}。",
        f"- **总体思路**：{method_overview}",
        f"- **为什么用这种方法**：{method_reason}",
        "",
        "### 方法分析",
        "",
        f"- **分析单位**：{study_area}。",
        f"- **关键变量/概念**：{core_variable}。",
        f"- **识别/推断逻辑**：{infer_logic}",
        f"- **具体步骤**：{concrete_steps}",
        f"- **方法优势**：{context['advantage']}",
        f"- **方法局限**：{limitations}",
        "",
        "## 数据来源",
        "",
        f"- **数据类型**：{data_source}。",
        f"- **样本来源**：{data_sample}",
        f"- **时间范围**：{data_period}",
        f"- **样本量/案例数**：{data_n}",
        "- **数据局限**：批量精读未进行表格逐项核对，涉及精确样本量、变量定义和清洗规则时需回到 PDF。",
        "",
        "## 研究结论",
        "",
        ]
    )
    if review_like:
        lines.extend(
            [
                "- **主要发现 1**：该文主要贡献是界定空间宏观经济学问题域，而不是给出单一实证结论。",
                f"- **原文引用 1**：缓存未提供稳定页码；{first_pdf_page_link(pdf_key, 1) or source_link(item_key)}",
                "",
            ]
        )
    elif finding_sentences:
        for idx, sentence in enumerate(finding_sentences[:5], start=1):
            summary = finding_summary(sentence, title, theme, idx)
            lines.append(f"- **主要发现 {idx}**：{summary}")
            lines.append(f"- **原文引用 {idx}**：缓存未提供稳定页码；{first_pdf_page_link(pdf_key, 1) or source_link(item_key)}")
            lines.append(f"> “{quote_excerpt(sentence)}”")
            lines.append("")
    else:
        lines.extend(
            [
                "- **主要发现 1**：全文缓存未稳定识别结论段，暂不生成实质性强结论。",
                f"- **原文引用 1**：{first_pdf_page_link(pdf_key, 1) or source_link(item_key)}",
                "",
            ]
        )

    lines.extend(
        [
            "## 我的判断",
            "",
            f"- **最有启发的点**：{relevance}。",
            f"- **可借鉴的方法**：{methodology}。",
            f"- **可继续追问的问题**：{context['question']}",
            f"- **与我的研究关联**：{context['relation']}",
            "",
            "## 二次精读状态",
            "",
            f"- **精读时间**：{deep_time}",
            "- **证据来源**：Zotero 本地 PDF 全文缓存",
            f"- **全文缓存字符数**：{quality.get('fulltext_cache_chars', 0)}",
            f"- **Zotero批注数**：{quality.get('annotations_count', 0)}",
            f"- **Zotero笔记数**：{quality.get('notes_count', 0)}",
            "- **需要后续人工复核**：公式、表格、精确页码与变量定义",
        ]
    )
    return "\n".join(lines) + "\n"


def append_log(log_file: Path, status: str, key: str, title: str, detail: str = "", *, write: bool = False) -> dict[str, object]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    suffix = f" | {detail}" if detail else ""
    return guarded_append_line(
        log_file,
        f"- [x] {timestamp} | {status} | {key} | {title}{suffix}\n",
        write=write,
    ).to_dict()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection", required=True)
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--note-root", type=Path, default=Path(r"<note_root>"))
    parser.add_argument("--recursive", action="store_true")
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

    target_dir = args.note_root / args.collection
    log_file = target_dir / "_DeepReadLog_二次精读记录.md"
    log_init = None
    if not log_file.exists():
        log_init = guarded_write_text(
            log_file,
            f"# Deep Read Log: {args.collection}\n\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
            write=effective_write,
            overwrite=False,
            backup=False,
            diff=False,
        ).to_dict()

    conn = connect_db(args.data_dir)
    try:
        items = list_collection_items(conn, args.collection, args.recursive)
    finally:
        conn.close()
    if args.limit > 0:
        items = items[: args.limit]

    report: dict[str, Any] = {
        "collection": args.collection,
        "started_at": datetime.now().isoformat(timespec="seconds"),
        "write": effective_write,
        "overwrite": args.overwrite,
        "backup": args.backup,
        "log_init": log_init,
        "total_items": len(items),
        "deep_read": 0,
        "skipped_no_local_pdf": 0,
        "failed": 0,
        "items": [],
    }

    for index, row in enumerate(items, start=1):
        key = row["key"]
        title = html.unescape(row.get("title") or key)
        try:
            payload = fetch_from_sqlite(args.data_dir, key, None)
            quality = payload.get("raw_data_quality") or assess_raw_data_quality(payload)
            fulltext, pdf_key, pdf_path = fulltext_from_payload(payload)
            has_pdf = has_existing_pdf(payload)
            if quality.get("level") != "local_fulltext" or not has_pdf:
                report["skipped_no_local_pdf"] += 1
                log_result = None
                if effective_write:
                    log_result = append_log(log_file, "⚠️ 跳过无PDF全文", key, title, quality.get("level", ""), write=effective_write)
                report["items"].append(
                    {
                        "index": index,
                        "key": key,
                        "title": title,
                        "status": "skipped_no_local_pdf",
                        "quality": quality.get("level"),
                        "log_result": log_result,
                    }
                )
                print(f"[{index}/{len(items)}] skipped_no_local_pdf | {quality.get('level')} | {key} | {title}", flush=True)
                continue

            note_path = find_existing_note_by_key(target_dir, key)
            if not note_path:
                note_path = target_dir / sanitize_filename(title)
            write_result = guarded_write_text(
                note_path,
                make_deep_note(payload, args.collection),
                write=effective_write,
                overwrite=args.overwrite,
                backup=args.backup,
                diff=args.diff,
            )
            log_result = None
            if write_result.status in {"created", "updated"}:
                log_result = append_log(log_file, "✅ 二次精读", key, title, note_path.name, write=effective_write)
                report["deep_read"] += 1
            elif write_result.status == "skipped_existing":
                log_result = append_log(log_file, "⚠️ 跳过", key, title, "existing note; --overwrite not set", write=effective_write)
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": title,
                    "status": write_result.status,
                    "quality": quality.get("level"),
                    "path": str(note_path),
                    "fulltext_cache_chars": quality.get("fulltext_cache_chars", 0),
                    "write_result": write_result.to_dict(),
                    "log_result": log_result,
                }
            )
            print(f"[{index}/{len(items)}] {write_result.status} | {quality.get('fulltext_cache_chars', 0)} chars | {key} | {title}", flush=True)
        except Exception as exc:
            report["failed"] += 1
            if effective_write:
                append_log(log_file, f"❌ 失败（{exc}）", key, title, write=effective_write)
            report["items"].append(
                {
                    "index": index,
                    "key": key,
                    "title": title,
                    "status": "failed",
                    "error": str(exc),
                }
            )
            print(f"[{index}/{len(items)}] failed | {key} | {exc}", flush=True)

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
