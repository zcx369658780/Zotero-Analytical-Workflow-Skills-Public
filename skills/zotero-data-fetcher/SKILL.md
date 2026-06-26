---
name: zotero-data-fetcher
description: 根据 Item Key 或标题，从 Zotero 数据库及本地目录快速提取元数据、批注和全文缓存。此步骤严禁翻译和长篇推理。
---

# Zotero Data Fetcher

## 1. 首选脚本

优先运行 bundled script：

```bash
python scripts/zotero_fetch.py --key <ITEM_KEY>
python scripts/zotero_fetch.py --title "<标题关键词>"
```

输出为 JSON，核心字段包括：

- `item`：Zotero 父条目元数据。
- `attachments`：PDF 附件、附件 key、PDF 路径、`.zotero-ft-cache` 路径与缓存文本。
- `notes` / `annotations`：Zotero 子笔记、PDF 高亮、批注。
- `online_supplements`：当存在 DOI/URL 时，从 Crossref、OpenAlex、Unpaywall（需 email）补充公开元数据、摘要和开放获取位置。
- `raw_data_quality`：标记语料等级，如 `local_fulltext`、`zotero_notes_or_annotations`、`online_abstract`、`metadata_only`。
- `raw_data_buffer`：交给 `zotero-analytical-writer` 的原始语料。

脚本会先尝试 Zotero Local API（默认 `http://localhost:23119/api`），再回退到本地 `zotero.sqlite`。如需跳过 API：

```bash
python scripts/zotero_fetch.py --key <ITEM_KEY> --no-api
```

`--out` 只有配合 `--write` 才会写入 JSON 文件；未传 `--write` 时仍只打印结果，不产生文件副作用：

```bash
python scripts/zotero_fetch.py --key <ITEM_KEY> --out fetch.json
python scripts/zotero_fetch.py --key <ITEM_KEY> --out fetch.json --write
```

默认会在本地语料不足时尝试公开学术 API 补抓。可用环境变量 `SCHOLAR_API_EMAIL`、`UNPAYWALL_EMAIL` 或 `CROSSREF_MAILTO` 提供 email；如需禁用联网补抓：

```bash
python scripts/zotero_fetch.py --key <ITEM_KEY> --no-online
```

## 2. 数据源定位

- 默认从 `prefs.js` 读取 `extensions.zotero.dataDir`。
- 如果默认路径不对，显式传入 `--data-dir "D:\path\to\Zotero"`。
- 只读数据库，不直接改写 Zotero 数据。

## 3. 语料提取优先级

针对该条目，按以下优先级组织 `raw_data_buffer`：

1. **最高级（批注）**：提取 Zotero 内的高亮（Highlights）和笔记（Notes）。如果批注内容已足够丰富，可跳过后续读取。
2. **次高级（全文缓存）**：读取附件目录中的 `.zotero-ft-cache` 文件，提取包含核心方法、数据和结论的关键段落。
3. **备用级（本地 PDF）**：仅在前两者缺失或需要确认复杂公式时，才读取本地 PDF 对应页码。
4. **公开来源补抓**：若无本地 PDF/缓存，基于 DOI/URL 查询 Crossref、OpenAlex、Unpaywall，记录摘要、开放获取 PDF URL 或落地页；默认不下载 PDF。
5. **元数据骨架**：若只有标题、作者、DOI、期刊等元数据，只交付骨架语料，并标记 `metadata_only`。

不要自动化使用 Sci-Hub 或其他非授权全文来源。若用户已通过 Zotero 自行找回全文，本脚本会在下一次运行时读取 Zotero 附件和缓存。
公开来源补抓必须做标题一致性校验；若 DOI 返回标题与 Zotero 标题明显不一致，视为导入污染，改用标题搜索或退回元数据骨架。

## 4. 交付标准

- **严格约束**：保持论文的原始语言（通常为英文）。严禁在此步骤进行任何翻译、总结或模板套用动作，确保数据提取过程以最高速度完成，不消耗过多算力。
- 若 `raw_data_quality.needs_fulltext_for_deep_reading` 为 `true`，明确标记缺口，不要补写方法、结论、页码或公式。
- 将 JSON 或其中的 `raw_data_buffer` 交付至 `zotero-analytical-writer`。
