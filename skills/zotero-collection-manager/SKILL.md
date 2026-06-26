---
name: zotero-collection-manager
description: 批量处理 Zotero 指定分类下的论文，支持断点续传。读取数据库文献列表，比对本地处理日志后，仅对未完成的条目逐一调用精读流程，实时更新进度。
---

# Zotero Collection Manager

## 1. 任务初始化与断点读取
- **定位分类与目录**：获取目标 Zotero 分类名称，并设定目标路径为 `<note_root>\<分类名称>\`，默认 `<note_root>\<分类名称>\`。
- **读取进度日志（Breakpoint）**：在目标路径下查找 `_ProcessLog_进度记录.md` 或 `.json` 进度缓存文件。
  - 若存在，解析其中已被标记为 `✅ 成功` 或 `⚠️ 跳过` 的论文 `Item Key` 或标题。
  - 若不存在，默认只报告计划；只有显式传入 `--write` 时才创建进度文件。

## 0. 写入安全规则

- 所有脚本默认只读计划，不创建目录、日志、报告或 Obsidian 笔记。
- 真正写入必须显式传入 `--write`。
- 覆盖已有 Markdown 必须显式传入 `--overwrite`；否则报告 `skipped_existing`。
- 覆盖前默认生成时间戳备份；只有 `--no-backup` 会关闭备份。
- 涉及已有 Markdown 的更新必须输出 `diff_summary`。
- `--dry-run` 的优先级高于 `--write`，始终保持纯只读。

## 0.1 Evidence Schema 规则

新生成笔记必须写入 `evidence_level`、`citation_eligible`、`citation_status`、`usable_for` 和 `evidence_sources`：

- `metadata_only` -> `E0`；`citation_eligible: false`；仅可用于 `indexing`、`triage`、`reading_queue`。
- `online_abstract` -> `E1`；`citation_eligible: false`；仅可用于 `screening`、`topic_clustering`、`reading_queue`。
- `zotero_notes_or_annotations` -> `E2`；`citation_eligible: candidate`；只能作为文献地图、机制矩阵或引用素材候选。
- `local_fulltext` -> `E2`；`citation_eligible: candidate`；缓存全文不能自动升级为正式引用。
- `reading_stage: "二次精读"` 不等于人工核验；脚本不得自动生成 `E3` 或 `citation_eligible: true`。
- 旧笔记迁移不在本 skill 默认动作内；需要另开只读审计或明确授权的迁移阶段。
- 旧笔记 evidence 迁移规划只能使用 `scripts/evidence_migration_planner.py`；该脚本为 dry-run-only，不提供写入 vault、覆盖旧笔记、自动 E3 或 `citation_eligible: true` 的能力。
- 旧笔记 evidence 迁移执行只能使用 `scripts/evidence_migration_executor.py`，且默认 dry-run。真实写入必须同时传入 `--write --sample-only` 和 `--sample-list` 或 `--max-files`；写入 `<vault_root>` 还必须额外传入 `--allow-vault-write`。不得批量迁移，不得自动生成 `E3` 或 `citation_eligible: true`。

## 2. 数据获取与任务过滤
- **首选脚本**：运行 bundled script 生成待处理队列：

```bash
python scripts/zotero_collection_queue.py --collection "<分类名称>"
python scripts/zotero_collection_queue.py --collection "<分类名称>" --recursive --note-root "<note_root>"
```

- **批量初录入脚本**：当用户要求把整个 Zotero 分类录入 Obsidian，优先运行：

```bash
python scripts/batch_import_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>"
python scripts/batch_import_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>" --write
```

该脚本会串行抓取条目、写入结构化初录入笔记、实时更新 `_ProcessLog_进度记录.md`。有本地全文缓存时写为 `local_fulltext`；缺 PDF 时尝试公开来源补抓，并降级标记为 `online_abstract` 或 `metadata_only`。

- **二次精读升级脚本**：当用户要求对已录入分类做“二次精读”“只精读有 PDF 的论文”时，优先运行：

```bash
python scripts/deep_read_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>"
python scripts/deep_read_collection.py --collection "<分类名称>" --recursive --note-root "<note_root>" --write --overwrite
```

该脚本只处理同时具备本地 PDF 附件和 Zotero 全文缓存的条目，覆盖升级已有 Obsidian 笔记，写入 `reading_stage: "二次精读"`、`deep-read` 标签、二次精读状态区，并生成 `_DeepReadLog_二次精读记录.md` 与 `_DeepReadReport_二次精读报告.json`。没有 PDF 或只有摘要/元数据的条目必须跳过并记录原因；不要为这些条目伪造方法、结论、页码或公式。

- **旧笔记 evidence 迁移规划（只读）**：当用户要求审计旧笔记并生成迁移候选 patch 时，运行：

```bash
python scripts/evidence_migration_planner.py --note-root "<note_root>"
python scripts/evidence_migration_planner.py --note-root "<note_root>" --out-report "reports/stage2c/evidence_migration_plan.md"
```

该脚本默认只读扫描已有 note，默认只处理有 `item_key` 且 frontmatter 可解析的 paper notes，默认排除日志、队列、索引和支持文件。它只生成 YAML 增量 patch / diff preview / dry-run report，不写入 `<vault_root>`，不迁移旧笔记，不提供 `--write` 或 `--overwrite`。

- **旧笔记 evidence sample-only 执行器**：当用户明确要求 Stage 2D 或 sample-only evidence migration executor 时，优先运行 dry-run：

```bash
python scripts/evidence_migration_executor.py --note-root "<note_root>" --max-files 20
python scripts/evidence_migration_executor.py --note-root "<note_root>" --workflow-root "<workflow_root>" --out-report "reports/stage2d/executor_dry_run.md" --max-files 20
```

真实写入只允许在单独授权下运行 sample set，并必须保留所有写入门槛：

```bash
python scripts/evidence_migration_executor.py --note-root "<temporary-or-approved-note-root>" --write --sample-only --max-files 5
```

Stage 2E 小样本迁移必须使用 Stage 2E metadata 模式：

```bash
python scripts/evidence_migration_executor.py --note-root "<note_root>" --sample-list "reports/stage2e/sample_list.txt" --max-files 5 --stage2e-sample --skip-zotero-check
```

`--stage2e-sample` 等价于 `--migration-stage Stage2E_sample_migration --write-status written_sample`，且 dry-run preview 与未来真实写入计划必须一致。不要对真实 `<vault_root>` 运行写入，除非用户在同一轮明确授权 `--write --sample-only --allow-vault-write`。执行器只修改 frontmatter，必须保留 frontmatter 结束分隔符之后的正文 suffix，默认跳过已有 evidence 字段的笔记，写入时生成备份、diff summary 和 `_EvidenceMigrationLog_Stage2D.md`。

Stage 2I 起，真实写入可使用集中备份与新的 evidence-schema log：

```bash
python scripts/evidence_migration_executor.py --note-root "<note_root>" --sample-list "reports/stage2i/batch_01.txt" --max-files 20 --sample-only --write --allow-vault-write --stage2e-sample --backup-root "<backup_root>\\Stage2I_YYYYMMDD_HHMMSS" --migration-log-name "_EvidenceMigrationLog_EvidenceSchema.md"
```

集中备份规则：
- 未传 `--backup-root` 时保持历史行为：在 note 同目录生成时间戳 `.bak`。
- 传入 `--backup-root` 时，备份写入集中目录并保留 `note\<collection>\<filename>.md.bak` 相对结构，不再写同目录 `.bak`。
- `--backup-root` 可以缺失、为空，或包含先前 batch 的集中备份；不得位于 `--note-root` 下；不得位于 Zotero data directory 下。若已存在，执行器会逐个校验当前 batch 的 planned backup path，只有全部位于 backup root 内且目标文件不存在时才允许继续，绝不覆盖已有备份。
- 新 log 参数必须使用 `--migration-log-name "_EvidenceMigrationLog_EvidenceSchema.md"` 或 `--migration-log <path-under-note-root>`；不传时保持旧 `_EvidenceMigrationLog_Stage2D.md` 兼容。
- 即使使用集中备份和新 log，真实写入仍必须满足 `--write --sample-only`、`--sample-list` 或 `--max-files`、`--allow-vault-write`、`--max-files <= 20` 等门禁。

- **查询数据库**：脚本从 Zotero 数据库获取该分类下所有父条目清单（包含 `Item Key`、标题、类型）。
- **计算差集（过滤）**：
  - 将总清单与进度日志进行比对。
  - 剔除已完成（成功/跳过）的条目，生成本轮的**待处理队列**。
  - 如果待处理队列为空，提示用户“该分类下所有论文已处理完毕”。

## 3. 循环调度引擎（实时存档机制）
针对待处理队列中的每一篇论文，严格串行执行，并且**每处理完一篇必须立即更新日志**：
1. **清理上下文**：强制清空内存变量，重置大模型分析状态。
2. **抓取数据 (Fetcher)**：传递任务给 `zotero-data-fetcher`。
   - *异常捕获*：若抓取失败（如无附件、无缓存），将状态记录为 `❌ 失败（原因）`，写入日志，跳过当前篇。
3. **生成笔记 (Writer)**：传递语料给 `zotero-analytical-writer` 写入 Obsidian。
4. **实时打卡（关键点）**：当前论文写入 Obsidian 成功后，立即打开 `_ProcessLog_进度记录.md`，追加一行记录：
   - 格式要求：`- [x] [时间戳] | 状态 | Item Key | 论文标题`
   - 例如：`- [x] 2024-05-20 14:00 | ✅ 成功 | ABCD123 | From heat to high-tech...`
5. **刷新根 Dataview 索引页（新增论文时强制执行）**：若当前论文对应的 `.md` 文件是首次创建，而不是覆盖旧文件，则在写入成功后立刻刷新 vault 根目录下的 `文献索引.md`、`研究主题索引.md`、`研究方法索引.md` 和 `字段补全检查.md`。

## 4. 输出执行报告
全部循环结束后，向用户输出本轮的执行简报：
- 本轮总计发现未处理文献 [X] 篇。
- ✅ 新增成功：[数量] 篇
- ❌ 新增失败/待确认：[数量] 篇
- *附言：进度已实时同步至 Obsidian 文件夹内的日志文件中，下次执行将自动跳过以上成功条目。*
