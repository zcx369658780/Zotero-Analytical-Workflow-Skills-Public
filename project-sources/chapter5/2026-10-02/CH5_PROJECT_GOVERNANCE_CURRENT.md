# 第五章项目治理与执行规则

更新：2026-09-27（Asia/Shanghai）。本文件合并旧项目规则；不创建科学任务或调用预算。若与本地现行文件冲突，以 `D:\ProjectTemp\c5k1bturn56` 中的实时文件、提交和独立裁决为准。

## 适用范围与入口

- 唯一论文工作树：`D:\ProjectTemp\c5k1bturn56`。禁止进入、读取、搜索、引用或修改 `deep-learning-hank`。
- 本地工作树、提交和证据是仓库状态权威；GitHub 只作可选备份和里程碑发布，不是日常任务队列、科学验收门或当前状态的替身。
- 开始工作依次读本地 `CURRENT.md`、`SCIENTIFIC_DECISIONS.md`、`TASK_CURRENT.md`、`REVIEW_GATE.md`，再读当前任务直接指定的源码与证据。历史报告只为具体溯源问题查阅，不凭旧交接重启任务。
- 本项目 Sources 是帮助项目会话定位知识与规则的日期快照；它本身不授权写入、实验、模型调用、Results 或论文结论。

## 职责和授权

- Owner 对经济含义、校准、科学合同、风险预算和论文结论保留最终权威。
- GPT Work 负责项目编排、有限任务、独立审查和 ACCEPT/REJECT；只能在已授权范围内自动下达下一项明确任务。消耗的预算、首个失败、受保护动作或实质 Owner 选择仍是停止门。
- Codex 是受界 Builder/执行者，仅按当前 `TASK_CURRENT.md` 的路径、测试/调用预算和停止条件工作，不自我接受高风险变更，不因对话交接重置预算。
- 已授权的常规工程细节可在任务范围内处理；不得为取得 PASS 调方程、KKT/边界法、校准、计时/收益律、求解器语义、网格、容差或重试次数。失败调用同样记账。
- LOW RISK 的文档、清单和惰性测试可按任务自检；MEDIUM RISK 的实现/集成需 Work 审查；HIGH SCIENTIFIC RISK 需明确科学授权、独立 Work 审查，实质定义还需 Owner 采纳。Builder PASS、有限 ACCEPT 和论文 Results 资格彼此不同。

## 本地文件与证据安全

- 写入前核对 HEAD、索引、跟踪/未跟踪状态、允许路径、受保护输出和输入哈希；保留用户或历史证据，不用宽泛清理、重置、stash、强推或覆盖来凑干净状态。
- 仅显式暂存任务允许路径，不用 `git add .` 或 `git add -A`。独占输出根、manifest/readback、原始调用账本和首故障记录须保持可复核；未知记为 `UNRESOLVED`，不得补猜。
- 对 Windows reparse/symlink、文件身份和输出变更安全合同保持 fail closed；静态 PASS 不自动允许 `--execute`。不可通过创建新会话、工作树或报告重置受保护预算。
- 模型/数据结果至少区分文件存在、机器诊断、人工解释、可复现投稿级证据；正式 Results 还须当前科学与审查授权。详细论文引用资格在独立的知识库文档中。
- 采用 Owner 指定的本地备份目录 `C:\Users\zcxve\Documents\Chapter5LocalBackups`；备份与 Git 发布都不等于科学验收。

## MATLAB / Python 诊断边界

- 原 MATLAB、历史 R5 和 source-faithful Python 是溯源与 parity 证据；successor 科学路线必须使用自己的已采纳合同，不从原程序的偶然行为推导新经济授权。
- 一项明确任务可覆盖计划、限定实现、必要静态检查、受预算约束的调用和证据收口；必须遵守它写明的精确次数、失败即停、先决门和禁止项。既有封存证据足够时不为形式完整重跑昂贵科学。
- 有限数值、残差或静态测试只能支持相应诊断，不自动证明经济可采纳、收敛、稳态、GE 或论文 Results。MATLAB/Python 一致性须按同一输入、形状/顺序、逐阶段最早差异和封存证据判断。

## 对话交接

- Work 在对话超过 30 记录、上下文不可靠或需更换会话时，先保存当前裁决、任务、证据标识、受保护根、消耗预算、实际账本和下一门，再在指定 Codex 项目 `Zotero-Analytical-Workflow` 内主动交接。新会话先只读核验项目归属和本地状态。
- 交接只转移上下文，不自动授权新科学、重试、输出根、候选 ACCEPT 或 Results。Owner 决策或受保护授权未闭合时，`TASK_CURRENT.md` 保持关闭。
- 当前指定 Codex 会话身份和证据以本地 `AGENTS.md` 与 `docs/CH5_K1B_CODEX_AUTOMATIC_HANDOFF_RULE_20260927.md` 为准；本 Sources 不固定一个未来会过期的会话 ID。

## 当前例外

Owner 已要求本轮源文档更新后停止 A1/C9 项目执行。当前 `TASK_CURRENT.md` 已关闭；本文件不能替它开启任务。当前事实见 `CH5_DISSERTATION_CHAPTER5_REWRITE_CURRENT.md`。
