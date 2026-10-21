# HELIX：模型—Harness 共进化的递归自改进（精读笔记）

> 论文信息：*Model-Harness Co-evolution for Recursive Self-Improvement*（arXiv:2608.13951，2026-08）
> 机构：HKUDS（港大数据智能实验室，Tianyu Fan, Chao Huang 等）
> 精读日期：2026-10-20 | 阅读方式：全文速读（abstract + intro + 结论 + 关键章节，实验细节未逐节核）
> 开源：**是**（github.com/HKUDS/HELIX）——本篇 12 篇中第三个开源工作（前两个 WHALE、SIA）

---

## 0. 速览卡片

| 字段 | 内容 |
|---|---|
| 一句话概括 | 把 RSI 的递归单元从"模型"重新定义为状态对 Z_t=(M_t, Φ_t)，build→update→rebuild 三阶段闭环：为当前模型进化 harness portfolio，把验证过的兄弟轨迹变成学习数据更新模型，再为新模型重建 harness |
| 所属领域 | RSI 基础框架 / harness 工程 |
| Tags | #模型-harness共进化 #build-update-rebuild #组合式基板 #来源可追溯 #一轮验证 |
| RSI 分级 | **L5 设计 / 实验只验证一轮** |
| 核心贡献标签 | 递归单元重定义 / 可审计 harness 基板 / 验证经验移交 |

## 1. 动机漏斗：六步走到问题

1. **大目标**：agent 的递归自改进。
2. **现状**：RSI 文献的改进对象几乎都是模型权重，harness 是训练/评估的固定背景。
3. **裂缝**：交互式 agent 通过 harness 作用于世界——harness 中介上下文、工具、控制流和终止，**它同时决定模型能做什么和模型从什么轨迹里学**。只改模型，等于只改进系统的一半。
4. **问题**：能不能让模型和 harness 作为一对状态共同进入改进循环，而且每一轮的交接是可审计的？
5. **约束**：现代 harness（OpenCode、Pi、Nanobot、Hermes 等）是大型紧耦合系统，随意自改写会让"干预的身份和证据"在重组中丢失——无法审计的改进无法复现也无法归因。
6. **本文问题**：设计一个基板，使异构 harness 家族的行为可以被显式声明、组合、执行，且每次干预从配方到运行时证据全程留痕，支撑可重复的 build-update-rebuild 循环。

**金句**："Harness 是当下模型的行为算子（behavior operator），也是后继模型的课程算子（curriculum operator）。"

## 2. Insight 与理论依据

### 核心 Insight

观测到的 agent 能力不是模型的属性，而是系统的属性：

```
observed capability = f(model, harness, task, budget, verifier)
```

推论：**递归改进的状态必须是 Z_t = (M_t, Φ_t)**（模型 × harness portfolio），而不是 M_t 单点。每轮 harness 进化有两个输出，不是两个目标：

- 输出 1（执行侧）：为当前模型找到更强固定 harness + 暴露 portfolio 互补覆盖；
- 输出 2（学习侧）：同一批干预产生的配对成功/回归/险败/替代解 = **验证兄弟轨迹（verified sibling trajectories）**，是下一轮模型更新的数据。

"改进执行的过程"与"生成训练数据的过程"是同一个过程——这是 HELIX 相对 WHALE/Co-Harness 交替范式的概念升级：交替范式里两个阶段是接力的，HELIX 里它们是同一次运行的两面。

### 与先行工作的差异定位

- vs DGM：DGM 的存档保存 agent 变体；HELIX 保存的是**干预身份 + 验证证据**（从声明配方到运行时证据的来源链）。
- vs Recursive Harness Self-Improvement（2607.15524）：RHI 在 prompt 级规范上做修订历史的两两反馈；HELIX 在类型化组件（ports/atoms/recipes/shells/policies）上做可执行重组。
- vs HarnessX（2606.14249v3）：HarnessX 做跨 harness GRPO 联合训练；HELIX 聚焦交接的可审计性这一互补系统层。

## 3. 方法拆解

### 整体骨架

```
第 t 轮：
  Build:   固定 M_t，构造并评估显式、来源可追溯的 harness 候选（matched tasks）
  Update:  验证兄弟轨迹 → 学习记录（SFT/critic/filter/preference）→ 更新模型到 M_{t+1}
  Rebuild: 为 M_{t+1} 重新进化 harness（能力画像变了，最优 runtime 设计可能也变）
  → Z_{t+1} = (M_{t+1}, Φ_{t+1}) 进入第 t+1 轮
外部锚：任务、目标、验证器由外部指定（同 DGM 的实验门、HGM 的外评器）
```

### 关键设计

**设计 1：组合式 harness 基板（typed ports / atoms / recipes / product shells / policies）**
- 功能：把 OpenCode、Pi Mono、Nanobot、Hermes Agent 四个开源 harness 分解为类型化可重组单元；干预以"配方"形式显式声明，执行前检查校验组合合法性。
- 核心思路：harness 重组发生在**受约束的组合空间**而非自由代码空间——每次干预可声明、可执行、可审计。
- 设计动机：DGM 式自由自改写的证据链在跨 harness 家族重组时必然断裂；要支持多轮共进化，必须先解决"干预身份保持"这个系统前提。这是 HELIX 选择的核心战场。

**设计 2：证据层（evidence layer）**
- 功能：执行全程保留 traces、测试结果、策略决策、provenance、结果标签。
- 设计动机：可审计性不是文档习惯，是 RSI 归因分析的基础设施——下一轮要知道"哪次干预造成了哪条轨迹差异"。

**设计 3：验证经验移交（verified experience handoff）**
- 功能：portfolio 中兄弟 harness 在相同任务上的差异结果（成功/回归/险败/替代解）转成四类学习记录：SFT、critic、filter、preference。
- 设计动机：harness 差异天然产生**配对对比数据**——这正是训练 critic/偏好模型需要的对比结构，比单轨迹 SFT 数据信息密度高。

## 4. 实验：验证了什么，没验证什么

**验证了什么（一轮 evolution，代码修复任务）**：

- 65 候选 LCB 进化矩阵：最强固定 harness 达 52/100，比基线 Pi 提升任务覆盖率 **+4.0%**；
- 完整 portfolio 事后并集达 79/100，比单候选暴露**至多 +58.0%** 的验证覆盖（兄弟互补行为真实存在且量大）；
- 选中成员经**重复运行 + 官方 SWE-bench 评估器**验证（不是自制指标）；
- 200-slot 兄弟切片产出 **438 条**验证学习记录（SFT/critic/filter/preference 四类）。

**没验证什么（必须诚实标注）**：

- **只跑了一个 evolution round**。"Update"阶段的产出止于 438 条学习记录——论文没有实际训出 M_{t+1} 并验证 Rebuild 阶段。双向闭环是框架声称，实验证据只覆盖 Build + 数据产出。
- 绝对水平：52/100 的固定 harness、79/100 的 portfolio 上界，覆盖率数字漂亮但任务绝对成功率未与 SWE-bench 榜单强基线直接对表。
- 65 候选的规模与 DGM（80 轮存档）相比是一轮快照，跨轮复利效应（HELIX 的核心卖点）零证据。

## 5. 评估三问

**Q1 内部标准**：预执行检查（组合合法性）+ 验证器标记的结果标签。门是"验证过的覆盖"，外部验证器固定——门不可改。
**Q2 外部审计**：官方 SWE-bench 评估器 + 重复运行——本篇在 12 篇里审计纪律属于上游；但只一轮，无跨轮 hold-out。
**Q3 量化**：有归因意识（证据层 + 来源链是归因基础设施），但未做成本核算（65 候选 × 代码修复任务的 token 账单未报）；"portfolio 互补覆盖 +58%"是最有价值的量化发现。

## 6. Contribution 提炼

1. **递归单元的重定义**：Z_t=(M_t, Φ_t) 是对 L5 最清晰的数学表述——比 Co-Harness 的"交替优化两个对象"更进一步，明确"进入下一轮的是状态对"。
2. **可审计基板**：typed 组合空间 + 证据层，回答"多轮共进化的系统前提是什么"——干预身份保持。
3. **经验移交机制**：harness 差异 → 四类配对学习记录，把"执行改进"和"数据生成"统一为同一过程的两个输出。
4. **诚实的范围标注**（少见）：论文明确说只验证一轮，把 portfolio 互补覆盖（而非单点胜利）作为主要效应——写作上没有过度声称。

## 7. 缺点与攻击面

1. **核心声称未闭环**：build-update-rebuild 只验证了 build 和数据产出。若 438 条记录训出的 M_{t+1} 不涨，框架塌一半；若 M_{t+1} 的最优 harness 与 M_t 相同，Rebuild 的必要性塌另一半。这两个实验是 v2 必须补的。
2. **+4.0% 固定 harness 增益偏小**：相对 portfolio 互补覆盖（+58%）的单点增益平淡，说明价值主要在数据侧而非执行侧——那么与直接做数据生成的管线（如 Yu et al. 的 correction pipeline）相比优势需要证明。
3. **基板成本**：分解四个 harness 为 typed 单元是大量人工工程；"可审计性"的代价是接入新 harness 家族的手工成本，框架的通用性受制于基板覆盖面。
4. **一轮快照无复利证据**：与 DGM 的 80 轮相比，HELIX 尚未证明共进化跨轮不退化。

## 8. 谱系定位

**HELIX vs WHALE vs Co-Harness（共进化三家）**：

| 维度 | HELIX | WHALE | Co-Harness |
|---|---|---|---|
| 递归单元 | 状态对 (M,Φ)，概念最清晰 | 交替双杠杆 | 交替双杠杆 |
| 闭环证据 | 只一轮（Build+数据） | 全程（但小模型） | 全程（14 轮） |
| harness 空间 | 组合式（typed atoms） | 代码级（Meta-Harness） | 五组件白盒 |
| 数据观 | 配对兄弟轨迹→四类记录 | 通过/未通过→RSFT | 轨迹 SFT |
| 开源 | **是（HKUDS/HELIX）** | 是 | 否 |
| 独有问题 | 闭环未验证 | 交替切换规则未消融 | 归因不明+不可复现 |

**对你的研究**：HELIX 是 L5 方向**概念框架最干净、工程基板最认真的开源底座**。它缺的恰好是 DGM 有的（跨轮证据）和 RQGM 有的（评估器共进化）——若做"HELIX 基板 × DGM 存档纪律 × RQGM 评估器轮"的组合，三个组件两个开源，可行性高。

### 本路线参照表

| 论文 | 递归状态 | harness 空间 | 闭环轮数 | 开源 | 精读价值 |
|---|---|---|---|---|---|
| **HELIX** | (M,Φ) 状态对 | 组合式 typed | **1（未闭环）** | **是** | 概念+基板 |
| WHALE | 交替 | 代码级 | 全程 | 是 | 交替动力学 |
| Co-Harness | 交替 | 白盒五组件 | 14 | 否 | 现象证据 |
| ScienceBuddy | 嵌套环 | 未公开 | 未公开 | 否 | 只取结构 |

## 9. 批判性问题清单

1. 438 条学习记录训出的 M_{t+1} 到底涨不涨？Rebuild 后的 Φ_{t+1} 与 Φ_t 差异多大？（v2 生死题）
2. "portfolio 互补覆盖 +58%"在多大程度上是 65 候选规模的函数？候选减半，互补覆盖掉多少？
3. typed 基板接入第五个 harness 家族（如 Claude Code）的边际人工成本是多少？
4. 配对兄弟轨迹数据 vs 等量随机轨迹数据，对模型更新的边际价值是多少？（数据观的核心证据缺失）
5. HELIX 的证据层能否直接导出 RQGM 式锚门需要的"修改前后配对性能"？如果能，它就是现成的锚门基础设施。

---

*系列：RSI 精读 | 分区：09-联合递归 | 编号：06*
