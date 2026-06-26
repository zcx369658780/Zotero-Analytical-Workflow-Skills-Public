---
name: zotero-analytical-writer
description: 接收原始语料，进行中文逻辑重构，严格按照当前 Obsidian 模板格式化并写入文件。
---

# Zotero Analytical Writer

## 1. Frontmatter 属性提取
在生成 Frontmatter 时，必须经过深度思考与提炼，**严禁直接大段复制摘要**。每个字段必须严格遵守以下定义，且**长度限制在一句话（10-30字）以内**：

Stage 2A 起，新笔记必须使用分区 frontmatter：

- `zotero`：只放 Zotero 原始元数据与链接，如 `item_key`、`pdf_key`、`select_uri`、`pdf_uri`、`doi`、`citekey`。
- `zotero_collections` / `zotero_tags`：保留 Zotero 分类和 Zotero 标签，不与 Obsidian 工作流标签混写。
- `obsidian_workflow_tags`：只放 `literature-note`、`auto-imported`、`deep-read` 等工作流状态标签。
- `evidence_level`、`citation_eligible`、`citation_status`、`usable_for`、`evidence_sources`：必须按语料等级保守填写。
- `human_verified` 默认 `false`；脚本或模型不得自动生成 `E3`，也不得把 `reading_stage: "二次精读"` 解释为人工核验。

* **`theme`（研究主题）**：一句话概括核心研究问题。（❌ 错误示范：复制整段摘要开头。✅ 正确示范：探讨城市创新空间生态位适宜性的评价指标与空间格局。）
* **`study_area`（研究区/样本）**：必须**严格依据标题和摘要**提取真实地名或样本范围，绝不能自行脑补常见城市。（❌ 错误示范：北京、上海等。✅ 正确示范：江苏省南京市。）
* **`data_source`（数据来源）**：仅提取**数据提供方、数据库名称或时间跨度**，绝不能包含作者信息或摘要前言！（❌ 错误示范：作者单位+邮编+摘要... ✅ 正确示范：南京市统计局数据及相关地理空间矢量数据，年份为 2020 年。）
* **`methodology`（研究方法）**：必须具体到**模型名称或分析工具**，严禁与 theme 字段重复！（❌ 错误示范：基于生态位视角探讨... ✅ 正确示范：构建 3 个维度的评价指标体系，结合 GIS 空间分析方法。）
* **`core_variable`（核心变量/指标）**：提取具体的**自变量、因变量或评价维度**，严禁堆砌论文的 Keywords！（❌ 错误示范：创新经济地理、创新生态系统。✅ 正确示范：资源生态位、环境生态位、技术生态位适宜度。）
* **`key_finding`（核心发现）**：用最精炼的语言总结最重要的结论，去掉“结果表明”等废话。
* **`relevance`（研究启发）**：说明该文的具体闪光点（如：提供了南京的对比基准 / 提供了生态位测度指标），拒绝“可用于补充文献脉络”这种正确的废话。

**⚠️ 强制校验机制**：在写入 Frontmatter 前，核对 `data_source` 中是否混入了类似“摘要：”、“作者：”、“210096”等无效字符；核对 `study_area` 是否与文章标题中的地名冲突。如发现，必须重写该字段。

## 1.1 Evidence 等级与引用资格

- `metadata_only` -> `E0`，`citation_eligible: false`，只能用于 indexing / triage / reading_queue。
- `online_abstract` -> `E1`，`citation_eligible: false`，只能用于 screening / topic_clustering / reading_queue。
- `zotero_notes_or_annotations` -> `E2`，`citation_eligible: candidate`，仅能作为 literature_map / mechanism / citation 候选，需人工核验。
- `local_fulltext` -> `E2`，`citation_eligible: candidate`，不能自动升级为正式引用。
- `E3 human_verified_deep_read` 只能由人工核验后设置；自动脚本、缓存全文、二次精读标签都不能生成 `citation_eligible: true`。

## 2. 模板套用与数学公式处理
模板路径：`../../templates/论文精读模板.md`

- **Zotero 链接**：Frontmatter 或基本信息区必须保留 `zotero://select/library/items/<itemKey>`；有 PDF 页码依据时，引用必须附带 `zotero://open-pdf/library/items/<pdfKey>?page=<页码>`。
- **结论结构**：灵活调整条目数，严格采用成对结构（主要发现 + 原文引用）。没有页码依据时，不要伪造页码，明确写“缓存未提供页码”。
- **数学公式提取铁律与连带阻断（防乱码与胡编乱造）**：
  1. **无效公式判定**：如果提取到的公式内容仅包含孤立的求和号（`\sum`）、极短的残片（如 `ic x`）、无意义的英文字母堆叠，则**强制判定为无效乱码**。绝对禁止强行套用 `$$...$$` 输出。
  2. **连带删除机制（关键）**：如果公式被判定为无效，使用了占位符，或者原文无公式，**必须彻底删除该公式对应的“公式拆解”、“符号代表什么”等所有下级解释区块**。绝对禁止为残缺符号或占位符凭空捏造解释（如重复生成“用于加权汇总”的废话）。
  3. **OCR 兜底**：如指令提供 `image_path` 且当前环境存在 `formula_ocr` 工具，立即调用；如果工具不存在，只保留“需截图/OCR 复核”的说明，不要假装已识别。
  4. **占位底线**：遇乱码且无截图时，仅输出单行说明“公式复杂/缓存乱码，需截图后 OCR 复核”，后续拆解区块直接删除。

## 3. 正文内容纯净度控制
在填写“具体步骤”、“数据来源”、“样本来源”等正文分析区块时，必须经过智能过滤，严禁机械搬运：

- **学术垃圾黑名单**：绝对禁止将以下内容写入笔记的任何分析字段：作者姓名、工作单位（如“XX大学XX学院”）、通讯地址、邮编、邮箱、基金项目编号（如“52008087”）、期刊投稿须知或排版规范（如“稿件内容应符合...”）。
- **提炼而非凑数**：必须从原文的“数据与方法”章节提取真正的研究步骤和数据集名称。如果在摘要或导言附近抓不到具体数据，宁可如实写“缓存文本未包含具体数据来源，需查阅完整正文”，也绝不能拿作者简介和基金号来凑字数！

## 4. 写入与终检
- **路径指定**：写入 `对应论文库位置`。
- **Stage 1 写入保护**：通过批处理脚本调用时，实际写入必须受 `--write` 控制；覆盖已有 Markdown 必须额外传入 `--overwrite`，并保留备份和 diff 摘要。不要在未授权的普通分析步骤中直接改写 Obsidian 笔记。
- **后置校验**：在最终保存前进行自我检查：
  1. Frontmatter 必填概括字段是否为全中文？
  2. 是否有未闭合的 `$` 符号？
  3. 是否包含有效跳转的 `zotero://select/...` 和 PDF 链接？
  4. 是否仍残留模板占位文本，如“在此粘贴”“按需继续补充”？
- 若校验通过，执行写入操作。
- **索引页刷新（新增论文时强制执行）**：若本次写入产生了新的论文笔记文件，而不是覆盖旧文件，则必须立即刷新 `论文库` 根目录下 4 个 Dataview 索引页：
  1. `文献索引.md`
  2. `研究主题索引.md`
  3. `研究方法索引.md`
  4. `字段补全检查.md`
