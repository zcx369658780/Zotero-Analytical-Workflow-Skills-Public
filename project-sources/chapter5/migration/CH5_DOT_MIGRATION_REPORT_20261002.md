# 知识库与博士论文第五章：DOT 项目迁移报告书

日期：2026-10-02（Asia/Shanghai）。性质：文档迁移与接续入口；不是模型启动、数据重建、科学验收或部署授权。

## 1. 项目基本情况与迁移基线

本项目包含两个相互关联的部分：论文知识库负责文献、来源、引用资格与研究笔记；第五章改写负责原 MATLAB 多省份两资产 HANK 的溯源、Python successor 的科学合同、实现、受界诊断与论文写作。研究对象保留家庭流动资产 b 和非流动资产 a，通过省籍基金的省际资本配置连接 31 个省份；不会把 31 省资产直接扩充为家庭 HJB 的状态维度。

工作必须区分源程序忠实复现、经济结构修正、数值有效性、固定点/GE 与论文 Results。这些是不同的证明对象。原 MATLAB 中名为 IRF 的顺序比较静态不能直接称为已经验证的动态 HANK。

### 1.1 已完成的 GitHub 迁移准备

| 对象 | 仓库与固定版本 | 已完成范围 |
|---|---|---|
| 项目源文档 | [知识库仓库](https://github.com/zcx369658780/Zotero-Analytical-Workflow-Skills-Public)，源包提交 `76b2e3c62f6f9503ef5f659c25d64504dc6afcf0` | Downloads 的 7 个原件：5 MD、论文 PDF、原 MATLAB ZIP；另有 README、清单与属性文件。7/7 原件字节核对通过 |
| 第五章当前进度 | [第五章迁移分支](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/tree/migration/dot-progress-20261002)，提交 `1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581` | 25,115 个变更路径；25,113 个可作 SHA 比较的候选字节差异为 0，清单/回执两项由提交封存 |

上述两个远端版本在编写本报告时再次通过指定 SSH key 的 `ls-remote` 回读确认。第五章 main 没有被本次同步合并；DOT 应使用迁移分支的固定提交，而非默认 main。未创建 PR。源文档上传不自动授予第三方论文/程序 MIT 许可，权利范围见源包 README 与仓库第三方说明。

第五章唯一当前本地模型树为 `D:\ProjectTemp\c5k1bturn56`，本地分支为 `codex/ch5-mp4c-k1b-turn5-turn6-bounded-continuation-20260922`。不得进入、读取、搜索或修改 `deep-learning-hank`。云端接续必须登记新的路径映射，但不得将映射当成启动模型的授权。

当前迁移提交的 `HEAD:src` 为 `f9fa75055d301deae0e4f6f08496d362052a1d3a`。旧状态文档中的 `00682b2e1a7ba23665f6e16f6acf48ad35874883` 是同步前的 src 树身份；本次把原未跟踪候选源码也保存到 Git，因此不能把整个新 src 树视为已经科学接受。

### 1.2 必读文档位置

以下第五章链接固定在上述迁移提交，避免分支未来变化混淆本报告的事实。读取顺序为 AGENTS 后，CURRENT → SCIENTIFIC_DECISIONS → TASK_CURRENT → REVIEW_GATE，再按具体问题读取直接引用的证据。

| 文档 | 用途与时效 |
|---|---|
| [AGENTS.md](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/AGENTS.md) | 工作树、角色、授权、预算和保护边界 |
| [CURRENT.md](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/CURRENT.md) | 当前状态及日期递进记录；下部大量旧段落属于历史 |
| [SCIENTIFIC_DECISIONS.md](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/SCIENTIFIC_DECISIONS.md) | 已采纳科学合同索引及重新开启条件 |
| [TASK_CURRENT.md](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/TASK_CURRENT.md) | 最近 TASK54 的文档同步范围；关闭任务不授权科学 successor |
| [REVIEW_GATE.md](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/REVIEW_GATE.md) | LOW/MEDIUM/HIGH SCIENTIFIC RISK 的职责和独立审查门 |
| [Git 同步迁移说明](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/docs/CH5_DOT_MIGRATION_SYNC_20261002.md) | 发布范围、字节保真、排除项、限制及行政异常 |
| [同步清单与发布前回执目录](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/tree/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/EVIDENCE/ch5_dot_migration_sync_20261002) | `sync_candidate_manifest.json` 与 `sync_prepublication_receipt.json`；回执是发布前时间点 |
| [迁移前最新交接 TASK49–53](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/EVIDENCE/ch5_frozen_c8_conditional_design_20261001/work_task49_53_handoff_20261001.md) | 文献补证、失败记录、预算及下一门；其中“未签发 TASK54”已被后续同步覆盖 |
| [TASK46–48 交接](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/EVIDENCE/ch5_frozen_c8_conditional_design_20261001/work_task46_48_handoff_20261001.md) | SDK 单次查询失败、无效封存和文档建议的接受边界 |
| [Python 重建路线正文](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/docs/DISSERTATION_CH5_PYTHON_MULTI_PROVINCE_HANK_REBUILD_ROADMAP_CURRENT.md) | 2026-09-20 的路线参考；“当前 turn5/6 任务”已经过时 |
| [路线入口](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/docs/CH5_TWO_ASSET_HANK_ROADMAP_CURRENT.md) | 2026-09-11 索引；旧参数待冻结等状态已由后续采纳覆盖 |
| [修订 GDP 接入计划](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/docs/CH5_REVISED_GDP_BINDING_AND_ADOPTION_PLAN_20260930.md) | 数据来源/日历/价格/年度双消费者合同的准备背景，须联读 10 月 1 日采纳 |

源文档包固定入口：[project-sources/chapter5/2026-10-02](https://github.com/zcx369658780/Zotero-Analytical-Workflow-Skills-Public/tree/76b2e3c62f6f9503ef5f659c25d64504dc6afcf0/project-sources/chapter5/2026-10-02)。其中：

- `DISSERTATION_KNOWLEDGE_BASE_CURRENT.md`：知识库范围与 E0–E3 / D0–D4 资格。
- `CH5_DISSERTATION_CHAPTER5_REWRITE_CURRENT.md`：研究问题、两资产/资本网络、科学合同与改写原则。
- `CH5_PROJECT_GOVERNANCE_CURRENT.md`：项目治理摘要。
- `CH5_HISTORICAL_EVIDENCE_INDEX_20260927.md`：旧审计/forensic/路线材料的索引。
- `PROJECT_SOURCES_REPLACEMENT_MANIFEST_20260927.md`：Sources 替换与来源记录。

这些 MD 是 2026-09-27 的来源快照，其旧 HEAD、旧任务和旧备份路径不能覆盖实时状态。备份目的地后来改为 `D:\Zotero-Analytical-Workflow\Chapter5LocalBackups`；该路径只作备份定位，不授权访问另一个仓库的内容。

**发布时态说明：**迁移提交中的 CURRENT、TASK_CURRENT、同步说明和回执刻意保留发布前措辞（如 pending / NOT_COMMITTED_NOT_PUSHED）。本报告记录已完成的后续发布与独立远端回读；不改写旧回执。迁移前交接曾建议换会话，Owner 已纠正本会话不足 30 轮并撤销提前交接。

## 2. 历史决策与来源覆盖

### 2.1 记忆读取范围

本报告实际读取了上述五份项目源 MD，以及本地现行 `SCIENTIFIC_DECISIONS.md`、状态、交接、Owner 采纳和指定技术材料。它们包含可追溯的项目记忆与历史决策摘要。ChatGPT 网页端未导出的完整项目会话记忆无法从本地直接读取，因此本报告不声称覆盖全部会话历史。

历史索引另指向本地 24 项旧 Sources 备份：`C:\Users\zcxve\Documents\Chapter5LocalBackups\chatgpt-project-sources-pre-governance-20260927.zip`，索引所载 SHA-256 为 `CB2898D82518415D805515C234B03FFFCF63143A3699C02BC91A251CF2230707`。本轮未打开或重核该 ZIP，不能宣称它已上传或在 DOT 可用。若需要补齐未导出的研究动机/讨论，应请网页端 GPT 顾问导出带日期、原话、证据路径及采纳范围的决策记录，再作为补充材料核对；无出处内容保留 UNKNOWN。

### 2.2 已确认的重要决策

| 决策 | 当前采纳范围及理由 | 直接依据 |
|---|---|---|
| 原 MATLAB/source-faithful 路线与修正经济结构的 Python successor 分开 | 原一资产 R5 只作迁移历史；忠实复现不等于 successor 科学合法性 | 项目源知识库与改写文档；SCIENTIFIC_DECISIONS |
| 采用省籍基金资本网络，数量和 payoff 共用 `S[destination,origin]` | `S[i,i]=1-theta_i`，外省权重和为 theta；恢复本省 retained private capital，去掉旧外省收益项不一致的二次 theta 权重 | 改写源文档；K1 payoff 合同索引 |
| K1A→K1B→K2 分阶段 | K1 固定 `theta_i=inter_prv_ratio_i`；K1B 外省 stable softmax，`beta_distance=2`、`beta_return=0.5`、吸引力总体 z-score `ddof=0`；K2 内生 theta 尚关闭 | SCIENTIFIC_DECISIONS 的 K1A/K1B 采纳项 |
| 采用 raw `ra0` payoff 和滞后时序 | `rah_i=sum_j S[j,i]*ra0_j`；已完成 turn n 的收益只用于 n+1，禁止同轮循环反馈，不擅自年化/平滑/缩放/裁剪 | `CH5_MP4C_K1A_RAW_RA0_PAYOFF_OWNER_ADOPTION_20260920.md` 及 timing freeze |
| C1 公共资本 residual | `GovInv=max(Ktarget-Kprivate_current,0)`，不是收益率控制器；私有资本超 target 时保留 overshoot | `CH5_MP4C_C1_GOVINV_RESIDUAL_LEVEL_REPLACEMENT_IMPLEMENTATION_ACCEPTANCE.md` |
| 有界 K1B 保留 source-faithful labor | 另行接受的双边劳动归一化组件未自动接入 | SCIENTIFIC_DECISIONS 的 labor 项 |
| 固定家庭求解合同 | 20×20×2、F-order、b 最快、source-native 初始化；HJB Delta=1000，同 checkpoint 同时 B≤1e-8 与 D≤1e-7 | corrected-household acceptance 与 nonlinear law adoption |
| 正 liquid-shadow 域及单调性保持 | 拒绝非正影子价格外推；一次已过门的 solve 后按 alpha=1,1/2,…,2^-52 首个合法候选回溯，760 个 raw b slopes 有限且严格正；不 floor/clip/投影或二次 solve | `CH5_MP4C_MONOTONICITY_PRESERVING_HJB_RELAXATION_OWNER_ADOPTION_20260921.md` |
| terminal KFE 的唯一闭类支持解 | 一次 exact-positive SCC，唯一闭类，闭类 `Q_CC.T` 上 dense gesvd，transient 支持精确零，完整 `Q.T@p` 验证 | `CH5_MP4C_UNIQUE_CLOSED_CLASS_SUPPORT_KFE_OWNER_ADOPTION_20260920.md` |
| 家庭聚合遵从已采纳质量口径 | Ct、Lt、At、Bt、AtTax 按 SCIENTIFIC_DECISIONS 的明确公式，不额外密度归一化/端点加权 | corrected-household aggregate binding acceptance |
| 九分量外层诊断采用预设 strict `<1e-6`，R2 连续两次 | 八个同阶段省向量加 S；它是冻结有界 K1B 映射的数值判据，不是数学收敛定理/GE；clipped ra 命中单独报告 | `CH5_FULL_OUTER_STATE_STOP_FAILURE_BUDGET_OWNER_ADOPTION_20260925.md` |
| 跨日只接受完整 outer checkpoint、协作式暂停 | 不把省 terminal/部分 HJB 当成可续跑状态；单次 C8 计时不是 C9/C10 时长上界；后续 C9 风险例外及墙限不构成普遍完成上界 | SCIENTIFIC_DECISIONS 的 checkpoint/timing/resource 项 |
| Output Mutation Objective A 保留 | 不缩减并发/恶意路径替换威胁模型；静态报告、身份哈希、文件唯一标识不等于最后检查到 mutation 的保护 | CURRENT、TASK46–53 交接及独立裁决 |
| 修订年度数据仅用于限定的固定 C8 中间层条件对照路线 | target2018/observation2017；冻结原 C8 家庭输出、进入 C8 的省份状态和份额，只设计年度 labor/wage 系数来源替换，保留原人口/参数/距离；不重算家庭/份额或 fullouter | [Owner 设计采纳](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/EVIDENCE/ch5_frozen_c8_conditional_design_20261001/owner_design_adoption.md)；后续 option1 有条件范围见 CURRENT，准备/保护/最终链未闭合 |
| 价格方法论与实际输入资格分开 | 修订历史统计量为事后回溯诊断，不声称当年实时可得；不以 CPI/PPP 或改布尔值解决缺证。方法论选项无需重问，但实际 `price_verified=False`、release UNKNOWN、baseyear None 仍保留 | 修订 GDP 接入计划、Owner baseline packet、CURRENT |
| Work 可处理类似小型行政事项 | 小型行政/文献事项可另限定范围与预算，无需重复请示；重大方向、经济法则、保护目标改变、科学/实验启动仍归 Owner，独立审查保留 | TASK46–48 / TASK49–53 交接中的 Owner 原话 |

具体经济合同遇到冲突时须回到 SCIENTIFIC_DECISIONS 所引原件与独立裁决，不从报告摘要或 legacy 行为自行推导替代法则。详细历史拒绝和失败记录保留，不以最新报告追认旧任务。

## 3. 当前进度与证据资格

### 3.1 已取得与尚未取得的证据

- corrected household HJB/KFE、selector 修复、单调性回溯、唯一闭类 KFE、源聚合、C1 residual 和滞后 K1B 在其限定路线内有实现及独立接受记录。
- turn5–turn8 的有界诊断已在各自范围接受；turn7、turn8 各有 31/31 household HJB/KFE 与一次 integration。C6→C7 只有 2/9 分量低于 strict 1e-6，C7→C8 为 5/9，R2 未满足。
- 一组 C5→C6-prime same-frozen-input 重复在九分量和 70 个中间量上 bitwise 相同；仅支持该输入的一对重复，不提供一般误差界。
- 一次 C8 frozen-input timing 测量为 3,382.203 秒，历史证据已接受；测量预算已耗尽，不是 C9/C10 上界，不可自动重测。
- 两次 C9 尝试均已消耗且没有完整新 outer turn；两份实际账本仍 `CALL_LEDGER_UNRESOLVED`，不可根据治理扣账推算真实调用数。
- 修订数据 artifact、inactive carriers/common seam 的限定工程证据、31-size 虚构 fixture，以及固定 C8 条件设计有各自有限接受；不等于实际 scientific consumer 已执行或新均衡已完成。
- 平台文献补证已确认 FILE_ID_INFO 的字段、FileIdInfo 映射及 open-handle 身份比较文字；仍未建立 parent/root/leaf mutation 绑定、生命周期、并发替换窗口与完整平台可用性。

主要数值依据位于 `docs/CH5_MP4C_K1B_TURN5_TURN6_INDEPENDENT_REVIEW_ACCEPTANCE_20260923.md`、`docs/CH5_K1B_TURN7_OUTER_R2_EXECUTION_INDEPENDENT_REVIEW_20260925.md`、`docs/CH5_K1B_TURN8_OUTER_R2_EXECUTION_INDEPENDENT_REVIEW_20260925.md`、`docs/CH5_TURN6_SAME_FROZEN_INPUT_REPEAT_EXECUTION_INDEPENDENT_REVIEW_20260925.md` 和 `docs/CH5_K1B_C8_TIMING_MEASUREMENT_EXECUTION_INDEPENDENT_REVIEW_20260926.md`。本报告复用这些历史接受事实，没有运行或解析科学数组来重新验算。

### 3.2 迁移后必须保留的状态

| 状态 | 当前值 |
|---|---|
| C9 | PAUSED |
| Output Mutation Objective A | 完整保留；16 项义务全部 UNRESOLVED |
| final-check-to-mutation window | UNACCEPTED |
| 历史 C9 实际调用账本 | CALL_LEDGER_UNRESOLVED |
| price_verified / release / baseyear | False / UNKNOWN / None |
| model_activation | False |
| Results eligibility | FALSE |
| K2、GE、年度动力学、冲击/IRF、福利、正式 Results | 尚未开启 |

SDK 登记查询 consumed1/rem0/retry0，原失败只证明查询失败，不证明 SDK 未安装；不得换 registry view、猜安装目录或读 header 作为替代重试。旧 passive query2/rem0；HTTP 批次 3/2/1/2/2/1 各 rem0；protected byte7/rem0；actualdata/fixture/archiveadmin/V1/V2 各 consumed1/rem0。历史科学及其他精确账本按原件保留，任何对话/平台迁移都不重置。

TASK47 的原无效 seal 和虚假完成字段保留，TASK48 只接受文档建议并排除这些字段；TASK49 capacity STOP、TASK52 truncation STOP 不重开；TASK53 仅 FILE_ID_INFO 字段与文档限制的有限 ACCEPT。TASK54 的 Git 发布完成只表示进度保存。

## 4. 当前 Python 程序详细信息

### 4.1 包身份、运行环境和可复现边界

固定代码入口：[src/ch5_two_asset_hank](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/tree/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/src/ch5_two_asset_hank)；配置：[pyproject.toml](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/pyproject.toml)。

包名 `ch5-two-asset-hank`，声明版本 `0.1.0`，Python `>=3.11`，核心依赖 `numpy>=2.0`、`scipy>=1.14`，构建 `setuptools>=68`；pytest 配置 pythonpath=src、testpaths=tests。这里的版本和下限不是一份精确可复现环境锁，也不保证任意新版本依赖科学等价。

历史被精确路径绑定的解释器为 `C:\Users\zcxve\AppData\Local\Programs\Python\Python311\python.exe`，Python 3.11.9 / MSC v.1938 / 64-bit AMD64 / Windows build26200。历史 repeat preflight 的文档记录为 NumPy2.4.6、SciPy1.17.1；BLAS/线程信息保留于原 preflight。本轮未启动解释器或重新探测版本，DOT 环境尚未验证。依据：`docs/CH5_K1B_C9_OUTPUT_MUTATION_A_EXACT_INTERPRETER_CAPABILITY_REPAIR1_20260927.md` 及 `docs/CH5_OUTER_STOP_REPEATABILITY_OWNER_DECISION_PACKET_20260925.md`。

精确解释器的一次历史标准库 probe 已显示所列 mkdir/unlink/rmdir/open/stat/lstat 没有相关 dir_fd 支持；这只描述该构建，不证明原生 Windows handle-relative backend 不存在或可用。SDK/API/native-support 仍 UNKNOWN；迁到 Linux/DOT 不能自动消除保护证明门。

### 4.2 模块地图与计算链

以下均为迁移提交中存在的源码位置；模块存在不表示当前已获运行授权。

| 路径（相对第五章仓库） | 职责 |
|---|---|
| `src/ch5_two_asset_hank/matlab_faithful_hjb.py` | MATLAB faithful HJB 计算部分，须按 corrected-route 合同区分接受范围 |
| `src/ch5_two_asset_hank/matlab_faithful_kfe.py` | faithful KFE 部分；现行 terminal 合同另由唯一闭类采纳约束 |
| `src/ch5_two_asset_hank/matlab_faithful_operator.py` | 离散算子/generator 的 faithful 路线 |
| `src/ch5_two_asset_hank/multi_province/household_adapter.py`、`corrected_household_adapter.py` | 家庭求解与省级聚合连接；不能假定旧入口自动切为 corrected opt-in |
| `src/ch5_two_asset_hank/multi_province/stationary_runtime.py` | 家庭稳态计算适配层；名字不构成模型稳态已经证明 |
| `src/ch5_two_asset_hank/multi_province/one_turn.py` | 一轮省际整合 |
| `src/ch5_two_asset_hank/multi_province/steady_state.py` | 外层迭代结构；其存在不表示 K1B/完整模型已收敛 |
| `src/ch5_two_asset_hank/multi_province/annual.py` | 年度输入、规范化输入和年度制品接口；不表示跨年度动力学已获科学接受 |
| `src/ch5_two_asset_hank/multi_province/capital_network.py`、`capital_allocation.py` | 省际资本网络、份额与资本配置 |
| `src/ch5_two_asset_hank/multi_province/firm.py`、`wage.py`、`migration_labor.py` | 企业、工资与劳动力模块；当前有界路线 labor 选择以采纳文件为准 |

有界 K1B 的解释链为：绑定进入 turn 的省份状态/冻结份额及 lagged payoff → 31 省 corrected household HJB/KFE/聚合 → 同一 S 的资本数量配置、C1 residual、企业/工资/劳动等整合 → 完整 outer checkpoint → 生成下一 turn 的 lagged raw-return signal、份额/输入候选 → 预设九分量比较、账本与独立审查。这是数值迭代顺序，不是现实日历期瞬时行为。

### 4.3 入口、runner 与测试资料

年度相关入口位于 `validators/multi_province/mp4c_python_annual_production.py`、`mp4c_python_annual_empirical.py`、`mp4c_run_full_annual_batch.py`；轨迹诊断位于 `validators/multi_province/call725_multi_iteration_trajectory/launch.py` 与 `python_trajectory.py`。这些历史/程序入口不能作为 DOT 自动运行命令。

明确的受界 runner 包括：

- `validators/multi_province/k1b_turn6_same_frozen_input_repeat/run.py`。
- `validators/multi_province/k1b_turn7_outer_r2/run.py`、`k1b_turn8_outer_r2/run.py`。
- `validators/multi_province/k1b_turn8_same_frozen_timing_measurement/run.py`。
- C9 相关 `k1b_turn9_outer_r2/run.py`、`k1b_turn9_timed_risk_exception/run.py`、`k1b_turn9_post_failure_new_attempt_outer_r2/run.py`、`k1b_turn9_post_failure_new_attempt_timed/run.py`。

C6/C7/C8 对应历史任务预算均已消耗；C9 相关 runner 没有当前执行授权。完整 runner ACCEPT、有限静态接受、候选 REJECT 需逐项查原独立审查；不得把后来的入口修复追认此前 REJECT 或违规 --execute 探测。

`tests/` 与 validator 文件随进度保存，既含已接受实现的测试资料也含候选/历史文件；本轮没有运行测试，不能声称整个当前树测试通过。Git 备份没有统一升级所有源码/测试的接受状态。

### 4.4 年度数据与固定 C8 条件设计

当前年度 observed / inactive carrier / common seam 的具体位置如下；它们的工程接受不能代替真实消费链授权：

| 路径 | 主要静态接口 |
|---|---|
| `validators/multi_province/annual_observed_labor_diagnostic/data_only.py` | `check_execution_gate`、`serialize_prepared_carrier`、`DataOnlyParser`、`main` |
| `src/ch5_two_asset_hank/corrected_diagnostic/annual_observed_labor_context.py` | `AnnualContext`、`AuthenticatedObservedSnapshot`、`authenticate_observed_binding`、`prepare_synthetic_context`、`prepare_observed_data_only_context` |
| `src/ch5_two_asset_hank/corrected_diagnostic/annual_labor_array_adapter.py` | `AnnualArrayCarrier`、`prepare_annual_array` |
| `validators/multi_province/annual_observed_labor_diagnostic/middle_stage.py`、`integration.py` | `PreparedMiddleStage`、`prepare_middle_stage`；`OneTurnInputs`、`integrate_turn` |
| `tests/test_ch5_observed_annual_array_seam.py`、`test_ch5_annual_k1b_middle_stage.py`、`test_ch5_annual_common_consumer_31_fixture.py` | 静态/合成 seam 资料；31 省 fixture 使用虚构输入，不是 observed 模型运行证据 |

年度替换针对劳动/复合工资共同使用的系数对象。设计保持 destination×origin 方向，`q_i=10000*GDP_亿元(i,t-1)/年末常住人口_万人(i,t-1)`，元/人；候选 `phi[j,i]=1+0.3*(q_i-q_j)/(q_i+q_j)`，原公式/方向和两消费者合同不擅自改变。目标年2018对应观察年2017，使用修订后的回溯统计量不能称为2018实时信息集。

[baseline packet](https://github.com/zcx369658780/dissertation-ch5-two-asset-hank/blob/1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581/EVIDENCE/ch5_annual_common_consumer_31_fixture_20261001/owner_scientific_baseline_packet.md) 指定原 C8 household aggregate receipt、C7 生成的 entering-C8 JSON 与 frozen-share/payoff NPZ。固定 C8 条件设计不是替换工资后重新求解家庭的一致均衡；partial C9 不能充作 baseline。真实 typed input、source-loader、单位/日历、dependency pins、对象 lifetime、保护和最终链仍需闭合。

### 4.5 DOT 尚需核对的迁移缺口

GitHub 保存了大量既有 EVIDENCE/reports 产物，但未发布 `data_local`、ignored 数据/文件或环境依赖。2,999 个 node_modules 文件被排除并原位保留；GitHub 快照不是完整运行环境或全部私人数据的备份。报告不承诺任何未发布输入可以在 DOT 取得。

DOT 接续需先只读登记 Python/NumPy/SciPy/BLAS/线程环境、Windows native/MATLAB runtime 历史依赖、31 省轴序、来源数据与 cache 的可用性、绝对路径映射、输出身份/保护合同及未发布输入清单。原任务耗尽的 probe/query/数据预算不能借“迁移验证”重做；任何新的执行检查须有新的具体范围和相应授权。

源代码 import、依赖安装、科学数组重建、测试、模型调用、native/DLL 实验、DOT 部署均未由本报告执行。先形成缺口清单，不生成虚假的可运行性 PASS。

## 5. DOT 接续路线与论文改写范围

1. **只读接收**：读取本报告、固定源包及四个当前权威文件，确认提交、迁移前/后时态和路径映射。输出已接受/拒绝/待定事项，不能把旧任务重新激活。
2. **资料整理**：在小型行政授权下整理文献/模型来源索引、固定 C8 条件设计的输入及平台文档缺口；优先复用既有官方文本，不重查已失败 SDK 或已耗尽预算。
3. **准备科学决策材料**：只有输入、单位/日历、依赖、生命周期、Objective A 和独立最终链可审查后，才向 Owner 提交具体可审查的科学/实验提案。科学方向、保护目标或执行预算变化仍由 Owner 决策。
4. **未来科学路线**：有界 fixed-point、GE、年度映射、冲击/IRF、福利与 Results 需要分别准备、授权和审查；这里列出目标，不安排运行。
5. **论文写作**：当前可整理研究问题、模型设定、已采纳合同、来源、诊断及限制；不得写“已收敛/稳态/GE”或定量政策结论。核心文献 claim 须 E3 人工核对原文/页码；数据 D0–D2 不支持强 Results，D3/D4 也不能绕过模型资格门。

现有 Builder 为 `01a0f67a-6f00-79a3-9b6e-24a75d875068` / local / “第五章平台契约文献零科学接续”，上次 TASK54 为 dialogue16，完成后 idle。此身份是本地工具定位，不保证 DOT 可直接调用。迁移本身不创建新科学 successor，也不让历史 Builder 自动启动。

## 6. 给 DOT 的接续 prompt

> 请接收“知识库与博士论文第五章改写”项目，先读取迁移报告：
> https://github.com/zcx369658780/Zotero-Analytical-Workflow-Skills-Public/blob/main/project-sources/chapter5/migration/CH5_DOT_MIGRATION_REPORT_20261002.md
>
> 以报告列明的固定源包提交 `76b2e3c62f6f9503ef5f659c25d64504dc6afcf0` 和第五章迁移提交 `1d5eccb78a08ee8155e4d4f2df9ec8bc64a0d581` 为接收基线。第五章使用 `migration/dot-progress-20261002`，不要使用 main 代替。先只读核对 AGENTS、CURRENT、SCIENTIFIC_DECISIONS、TASK_CURRENT、REVIEW_GATE、项目源决策摘要与最新交接；明确报告所说明的发布前旧措辞及过时路线图。
>
> 先输出接收核对结果、关键文档地图、Python 程序/环境/未发布数据缺口和下一项可做的有限文档工作。较小行政/文献事项可自行限定并推进；重大方向、科学/实验启动、保护目标改变及新预算仍交 Owner 决定，保留独立审查门。C9 PAUSED、完整 Objective A、16 UNRESOLVED、window UNACCEPTED、CALL_LEDGER_UNRESOLVED、price/model False、Results FALSE 不变；SDK consumed1/rem0/retry0 及全部旧预算不重置、不重试。禁止 deep-learning-hank；原本地唯一模型树为 D:\ProjectTemp\c5k1bturn56，云端需明确路径映射。不要运行模型/测试/import/native 实验，不安装依赖、不部署、不创建 PR；本次接收先完成资料与缺口整理。

## 7. 本报告的核查范围

编写过程只读项目源 MD、权威文件、指定文档及源码文本，由两名分工只读助手分别核对文档时效和 Python 地图；主 Work 负责范围、事实整合和发布。行政输出截断曾发生，未采用被截断的缺失内容作证明；一个 baseline packet 的错误目录读取失败后，按 Owner adoption 中的确切引用改读正确路径。它们不改判任何旧科学 STOP，不消耗或重置旧受保护预算。本轮没有模型、测试、SDK/native、受保护科学结果重算或 DOT 执行。

本报告新增事实是文档整理与远端提交回读；历史数值/环境/科学接受事实标明原记录，不冒充本轮重验。公开仓库只作资料保存，不自动成为科学授权源。
