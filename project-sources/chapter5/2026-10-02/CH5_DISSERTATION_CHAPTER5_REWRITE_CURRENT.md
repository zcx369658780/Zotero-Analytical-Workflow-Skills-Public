# 博士论文第五章改写与两资产多省份 HANK 路线

状态快照：2026-09-27（Asia/Shanghai）。本文件与论文知识库文档分开：这里记录第五章模型、改写边界和当前任务门，不是可发表的 Results。实时权威为 `D:\ProjectTemp\c5k1bturn56` 的 `CURRENT.md`、`SCIENTIFIC_DECISIONS.md`、`TASK_CURRENT.md` 和独立裁决。

## 研究对象与改写原则

- 项目正在把原 MATLAB 多省份两资产 HANK 的 source-faithful 参考路线，与修正经济结构的 Python successor 明确分开。忠实复现、经济合理性、数值有效性、固定点/GE 与论文 Results 是不同的证明对象。
- 原一资产 R5 只作历史迁移参照；原 MATLAB 中名为 IRF 的顺序比较静态不能直接当作已验证的动态 HANK。K2、年度动力学、冲击、IRF、福利、政策解释和正式 Results 尚未开启。
- 第五章写作现在可整理研究问题、模型结构、变量与来源、已采纳科学合同、失败/限制和待验证路线；不得写出“已收敛”“已达到稳态/GE”或定量政策结论。

## 两资产与省际资本网络

household 仍只保留流动/非流动两资产 `(b,a)`，不把 31 个省份资产显式加进 HJB。省 `i` 的聚合非流动财富 `W_i=A_i N_i` 经 post-household 的省籍基金配置到目的省企业。`S[j,i]` 采用 `destination x origin` 方向：

```text
theta_i = inter_prv_ratio_i                 (K1 阶段固定)
S[i,i] = 1 - theta_i
S[j,i] = theta_i * P[j,i], j != i
sum_{j != i} P[j,i] = 1; sum_j S[j,i] = 1
M_K[j,i] = S[j,i] * W_i
Kprivate_j = sum_i M_K[j,i]
rah_i = sum_j S[j,i] * portfolio_return_j
sum_j M_K[j,i] = W_i; sum_j Kprivate_j = sum_i W_i
```

这一设计恢复原程序遗漏的本省 retained private capital，并去掉 `rah` 外省项中不一致的目的省 `theta_j` 二次权重。capital quantity 与 household payoff 必须使用同一 `S`；legacy allocation 继续只用于 parity 溯源。历史非对称 fixture 的 national private wealth 为 200，legacy destination K `[63,50,17]` 修正为 `[79,80,41]`，`rah` 权重和从 `[.93,.75,.48]` 修正为 `[1,1,1]`；这些是受界实现证据，不是实证均衡结果。

foreign conditional shares 使用 foreign-only stable softmax，候选分数结构是 `-beta_distance*distance_score[j,i]+beta_return*lagged_return_score[j]`。已冻结的 bounded K1B route 采纳 `beta_distance=2`、`beta_return=0.5`、foreign attractiveness 的总体 z-score (`ddof=0`)；raw `ra0` 水平用于 payoff，不混成 attractiveness。参数采纳不代表 K1B 收敛、稳态或 Results 接受。只可用上一完整 outer iteration 的 return 信号决定下一次配置，禁止 same-turn `firm -> return -> share -> K -> firm` 回路。这是稳态数值迭代时序，不是现实日历期的瞬时行为。

## 阶段与相关科学合同

- K1A 是修正会计/固定或空间配置基线；K1B 是固定 `theta_i`、带滞后收益吸引力的外省目的地配置；K2 才讨论 home-vs-foreign 比例 `theta_i` 内生化。K2 尚未获执行授权。
- C1 公共生产性资产 residual 为 `GovInv=max(Ktarget-Kprivate,0)`，不是收益率控制器。K1 改变 `Kprivate` 后必须联合核验；当 private K 超过 target 时，GovInv 归零并保留 private-only overshoot。
- 当前有界 K1B 仍使用 source-faithful labor；已接受的双边劳动归一化组件未自动接入。KFE 需要独立的 generator、唯一闭类、质量/非负性和终端验证；资本网络通过下一轮价格/`rah` 间接影响 KFE，不代表 KFE 问题自动解决。
- 历史 return bounds `[.02,.09]` 仅是 numerical safeguard，wage bounds `[.8,1.3]` 的经济单位仍需谨慎；不能根据轨迹表现事后改界限。
- household 使用冻结的 `20x20x2` F-order `(b,a,z)` 网格（`b` 最快）与 source-native 初始化。HJB 的固定 `Delta=1000`、直接稀疏解和 backward-error 门不因调参改变；同一接受 checkpoint 需同时满足 `B<=1e-8` 与 `D<=1e-7`。一次完整隐式 solve 通过既有门后，单调性保持只可从 `alpha=1,1/2,...,2^-52` 中取首个使 760 个 raw b slopes 有限且严格为正、状态与旧状态 bitwise 不同的候选；不作第二次 solve、floor、clip 或投影。
- terminal KFE 用一个 exact-positive SCC 分解并要求唯一闭类，仅在闭类支持上求解，再把 transient support 嵌为精确零并做完整 `Q.T@p` 验证。household 聚合 `Ct=sum(C*p)`、`Lt=sum(z*l*p)`、`At=sum(a*p)`、`Bt=sum(b*p)`，总资产为 `At+Bt`；`AtTax=At*rah-sum(a*effective_r_a*p)`，不另做密度归一化或端点加权。selector 的 D1/D2/D3、ordinary upwinding、interior-liquid Z、lower-a zero-kink 及后续已接受修复仍以本地 `SCIENTIFIC_DECISIONS.md` 与各采纳文件为准。
- corrected-2018 数据、单位、年份和来源须按本地接受合同逐项绑定；不把旧 MATLAB 混年数据或未核验缓存直接写成新论文实证结果。

## 已完成的有界证据和当前停止门

- K1B turn5–turn8 的有限诊断和一组 same-frozen-input 重复证据已接受于其各自范围。turn7/turn8 各 31/31 household HJB/KFE 并完成一次 integration，但九分量相邻比较均未达到全部严格 `<1e-6`；没有收敛、固定点、稳态、GE 或 Results 接受。C8 计时只有一次观察，不构成 C9/C10 时长上界。
- 两次 C9 尝试均已消耗；两份实际账本仍为 `CALL_LEDGER_UNRESOLVED`。Owner 采纳了新预算和旧失败的治理扣账方式，但这不补出实际调用数，也不授权新科学。C10、重试、部分续跑和 Results 均关闭；`Results eligibility=FALSE`。
- Output Mutation Objective A 的可信根、各层 `mkdir`、独占 JSON/NPZ 创建和 `unlink` 均为 `UNRESOLVED__FAIL_CLOSED`。A1 原候选 `f7005732d3a239dccc60f1ede4a551b1a5ba543a` 保持 REJECT；Repair1 `7cd442e55863b58fbda36a3113b60fd0ad8f1c40` 仅获官方引文可追溯性的有限 ACCEPT。早期静态 runner 的 REJECT 与两次违规 `--execute` 探测也不追认。
- 原静态 runner、Repair1、Repair2 的独立 REJECT（含 Repair2 `e860a54ac3fed1d104009a068722b1045bd87b5f`）仍是历史裁决；后续 `load_delegate` / `run_timed_action` 入口的有限静态验证不改判旧候选，也不构成完整 runner ACCEPT 或 C9 执行授权。后续链条的具体限定裁决以本地 `CURRENT.md` 和对应独立审查文件为准。
- 当前 `HEAD=bbd89a62bcda6b7c92e77444ee421298ed47fc7d`，`HEAD:src=00682b2e1a7ba23665f6e16f6acf48ad35874883`，`TASK_CURRENT.md` 为 `CLOSED__A1_QUOTE_REPAIR1_ACCEPTED__SOURCE_DOCUMENT_REFRESH_NEXT`。六个受保护未跟踪 `reports/` 输出根保持原样。本轮仅更新项目 Sources 并停下，没有活跃 A1/C9 Builder 或科学任务。

## 后续论文目标，不是当前任务

先保留可追溯的来源与模型合同，明确数值停止准则和真实调用账本，再由 Owner 对任何新科学尝试单独授权；独立审查后才可讨论 bounded fixed-point、GE、年度映射、冲击/IRF、福利与 Results。正式章节写作中，模型设定可按已采纳合同描述，计算诊断应标为诊断，尚未具备资格的结果不得提升为论文发现。文献 claim 另遵守 `DISSERTATION_KNOWLEDGE_BASE_CURRENT.md` 的 E0–E3 / D0–D4 规则。
