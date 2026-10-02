# 项目 Sources 手动替换与覆盖清单

版本：2026-09-27 知识库保留版。本清单取代旧 `PROJECT_SOURCE_UPDATE_MANIFEST_20260911.md`，也取代先前不完整的 `CH5_Project_Sources_20260927.zip` 中“删除全部旧 Markdown、仅上传五份治理快照”的建议。**不要使用先前的 ZIP 执行替换。**

## 替换顺序

1. 先确认本地旧源完整备份存在：`C:\Users\zcxve\Documents\Chapter5LocalBackups\chatgpt-project-sources-pre-governance-20260927.zip`，应含旧 Sources 全部 24 项，SHA-256 `CB2898D82518415D805515C234B03FFFCF63143A3699C02BC91A251CF2230707`。
2. 项目 Sources 中的论文 PDF 与 MATLAB 原程序 ZIP **保留原样**，不删除、不用本包覆盖。
3. 先上传本包五份 Markdown，并在界面中确认五份都显示、可打开且抽查内容正确。**只有 Owner 完成这一步确认后**，才逐项移除旧 22 份 Markdown；不得在新文件未核实前批量删除旧源。
4. 最终项目 Sources 应为五份新 Markdown 加原有两项二进制参考材料，共七项。备份 ZIP 和本替换 ZIP 仅存本地，不上传为知识源。同步镜像 `sources/` 由产品维护，本任务不直接修改。

新五份职责：`DISSERTATION_KNOWLEDGE_BASE_CURRENT.md` 专管论文知识库、来源、Zotero/Obsidian 与引用资格；`CH5_DISSERTATION_CHAPTER5_REWRITE_CURRENT.md` 专管第五章模型改写及当前路线；`CH5_PROJECT_GOVERNANCE_CURRENT.md` 合并治理/执行规则；`CH5_HISTORICAL_EVIDENCE_INDEX_20260927.md` 提供旧证据入口；本文件负责替换和覆盖核验。前两份保持不同主题，不将当前 C9 任务状态混入通用知识库规则。

## 旧 Markdown 覆盖映射

| 原 Sources 文件 | 新入口 / 保留方式 |
|---|---|
| `AGENTS (project file).md` | `CH5_PROJECT_GOVERNANCE_CURRENT.md`；旧 GitHub 权威表述废止 |
| `PROJECT_RULE_OVERVIEW_CURRENT.md` | 治理文档的范围/角色；知识库文档的服务范围 |
| `PROJECT_RULE_INDEX_CURRENT(1).md` | 治理文档的本地入口；旧阶段状态废止 |
| `PROJECT_RULE_CODEX_GITHUB_WORKFLOW_CURRENT.md` | 治理文档；GitHub 改为可选备份/发布 |
| `PROJECT_RULE_GITHUB_CAPABILITY_AND_AUTHORITY_ROUTING_CURRENT(1).md` | 治理文档；旧 GitHub 主导任务路由废止 |
| `PROJECT_RULE_ACCEPTANCE_LEVELS_CURRENT.md` | 治理文档的风险/审查等级 |
| `PROJECT_RULE_LOCAL_FILE_SAFETY_CURRENT.md` | 治理文档的本地文件与证据安全 |
| `PROJECT_RULE_MATLAB_MODEL_DIAGNOSTIC_GATES_CURRENT.md` | 治理文档的 MATLAB/Python 诊断边界；原全文在备份 |
| `PROJECT_RULE_PYTHON_MODEL_REBUILD_DIAGNOSTIC_GATES_CURRENT(2).md` | 治理文档的 MATLAB/Python 诊断边界；原全文在备份 |
| `PROJECT_RULE_PROMPT_AND_HANDOFF_FORMAT_CURRENT.md` | 治理文档的交接原则；易变会话 ID 留在本地 |
| `PROJECT_RULE_MEMORY_AND_PROGRESS_SUMMARY_CURRENT(1).md` | 知识库长期维护与治理入口；旧 K1 当前阶段废止 |
| `PROJECT_RULE_RESEARCH_EVIDENCE_AND_CITATION_CURRENT.md` | `DISSERTATION_KNOWLEDGE_BASE_CURRENT.md` 的 E0–E3、D0–D4、Zotero/Obsidian 和引用资格 |
| `PROJECT_RULE_DISSERTATION_CH5_ROUTE_CURRENT(1).md` | `CH5_DISSERTATION_CHAPTER5_REWRITE_CURRENT.md` 的研究路线与 Results 边界 |
| `CH5_MP4C_BILATERAL_CAPITAL_NETWORK_SCIENTIFIC_DESIGN_FREEZE_CURRENT.md` | 第五章改写文档的结构与公式；历史完整冻结稿在备份 |
| `CH5_TWO_ASSET_HANK_PROJECT_STATUS_CURRENT(3).md` | 第五章改写文档的当前状态由本地 2026-09-27 事实更新；旧状态留备份 |
| `CH5_TWO_ASSET_HANK_ROADMAP_CURRENT(1).md` | 第五章改写文档的阶段路线；旧“下一步”废止 |
| `CH5_TWO_ASSET_HANK_SESSION_HANDOFF_CURRENT(1).md` | 治理交接规则及第五章状态；原历史交接在备份 |
| `DISSERTATION_CH5_PYTHON_MULTI_PROVINCE_HANK_REBUILD_ROADMAP_CURRENT(2).md` | 第五章改写文档的 K1A/K1B/K2 和后续目标；旧阶段指令废止 |
| `CH5_TWO_ASSET_HANK_MATLAB_MULTI_PROVINCE_LOGIC_AND_LEGACY_R5_MIGRATION_AUDIT_REPORT(1).md` | 知识库来源链与历史证据索引；完整调用图/迁移矩阵在备份 |
| `CH5_TWO_ASSET_HANK_MP4C_2018_CALL725_RAW_LIQUID_DERIVATIVE_BOUNDARY_ROOT_CAUSE_FORENSIC_REPORT.md` | 知识库与历史证据索引；完整 forensic 在备份 |
| `CH5_TWO_ASSET_HANK_MP4C_2018_CALL725_POST_CALL_RESIDUAL_VECTORIZATION_REPAIR_AND_FIRST_ITERATION_STAGEWISE_REEXECUTION_REPORT.md` | 知识库与历史证据索引；完整 forensic 在备份 |
| `PROJECT_SOURCE_UPDATE_MANIFEST_20260911.md` | 本替换清单；旧操作说明废止 |

治理后的 Sources 保留关键研究知识和现行入口，而不是逐字复刻每份旧报告。旧版 24 项全部可从本地备份恢复；需要审计某项历史公式、数据哈希或调用图时，回读原文及本地仓库证据，不能从摘要补猜。当前任务与预算在本地实时文件中，项目源仅是带日期的知识与治理快照。
