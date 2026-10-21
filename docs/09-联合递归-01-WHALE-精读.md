# WHALE 精读：Weight-Harness Alternating Learning

> **论文信息**：Yoonho Lee（Stanford）、Gisang Lee（KRAFTON）、Chelsea Finn（Stanford）、Kangwook Lee（KRAFTON）；arXiv:2609.00196（2026-08-31，v1）；代码开源（github.com/krafton-ai/WHALE）
> **精读日期**：2026-10-16 ｜ **阅读方式**：全文（arXiv HTML，含附录算法与轨迹示例）

---

## 0. 速览卡片

| 项目 | 内容 |
|---|---|
| **一句话概括** | 提出 Weight-Harness Alternating LEarning（WHALE）：在「当前 harness 下做在线拒绝采样微调（RSFT）」与「当前权重下用 Meta-Harness 搜索 harness」两相位间交替，并用调度研究证明**小步交替严格优于分段式优化**；Qwen3.5-2B/4B 三域实验超单组件基线 +7.67~24.38pp、超 prompt 受限的 FST 对照 +4.15~13.00pp |
| **所属领域** | 联合优化（权重×harness）× agentic RL × 坐标下降式交替调度 |
| **Tags** | `[联合优化]` `[harness搜索]` `[RSFT]` `[交替调度]` `[Meta-Harness]` |
| **RSI 分级** | **L0（一阶改进）× 双杠杆**——harness 与权重都是被优化对象，改进器（Meta-Harness proposer、RSFT 管线）全程固定且外置；是"联合优化"而非"自我改进"，**不构成递归**。其价值是为 L5 提供受控的调度科学基础 |
| **核心贡献标签** | J(θ,h) 联合目标形式化；harness-dominant vs model-dominant 两种瓶颈域的实证刻画；交替 vs 分段的受控调度研究；adaptive WHALE（纯训练信号驱动的 patience 切换规则）；预算匹配对照设计 |

---

## 1. 动机（漏斗）

1. **领域现状**：联合适应的已有工作只优化「权重 + 文本 prompt」（Soylu et al. 2024、FST 等）；harness 搜索线与权重训练线各自孤立。
2. **现有痛点**：(1) 只调一个组件会被冻结的另一个组件 bottleneck——权重更新改变"什么 harness 有效"，harness 更新改变"什么模型能力被暴露"；(2) 两相位时间尺度不同（harness 搜索是长 propose-accept 周期，在线微调是 rollout-梯度交替），并发执行会让每次更新对着一个移动靶评估，信用分配被混淆。
3. **核心矛盾**：J(θ,h) 不可分——两个组件通过诱导的轨迹分布 π_{θ,h} 耦合，任何单组件优化都在对变化中的对手过拟合。
4. **本文目标**：研究交替式权重-harness 更新的设计决策，核心调度问题是——**每个组件该改多少才切换**？
5. **切入角度**：坐标下降（Wright 2015）——把耦合问题分解为对冻结对手的条件更新，回避并发评估的混淆。
6. **核心 idea**：交替两相位 + 调度规则位于"噪声极端"（证据不足就采纳侥幸候选）与"过优化极端"（对冻结对手优化过度）之间。

**判断**：动机成立且是真问题——它把 Co-Harness 类工作默认"交替就对"的隐含假设变成了受控研究对象。

## 2. Insight 与理论依据

- **核心 insight**：瓶颈是域依赖且可移动的。SearchQA 是 harness-dominant（harness 搜索仅用 5.79% 的 rollout 就追平 weight-only 峰值）；Math 是 model-dominant（harness-only 只达 0.42%，weight-only 15.42%——瓶颈是响应截断，只有权重能修）。因此"先 harness 诊断、后权重训练"可作为低成本探测流程。
- **理论依据**：交替最小化（coordinate descent）；RSFT 师承 RAFT/ReST 一脉；harness 搜索直接复用 Meta-Harness（Lee et al. 2026，同组工作）。
- **严格使用还是隐喻借用**：严格使用——就是标准的分块坐标下降应用于 J(θ,h)，没有理论包装的夸大。
- **逻辑跳跃**：无显著跳跃；论文把贡献恰当地限定为"受控调度研究"。

## 3. 方法

### 3.1 系统骨架（Algorithm 1）

1. 循环 k：权重相位——冻结 h_k，在 D_weight 上做在线 RSFT：采样 G=8 条轨迹/题，只保留 verifier 接受的 (x,τ)，做 token 归一化 SFT（Eq. 2），minibatch 梯度步间同步权重到 rollout worker；
2. harness 相位——冻结 θ_{k+1}，跑 I 轮 Meta-Harness：proposer 检查档案库与评测 artifact，每轮写 M 个候选 harness，在 D_harness（256 题、每候选 1 条 rollout）上打分，全部入档，h_accept = argmax 档案训练分；
3. 交替进行，返回测试集最优 (θ_k, h_k)。

### 3.2 关键设计（三段式）

> **Adaptive WHALE（per-phase patience 规则）**
> - 功能：免除 (E,I) 调度超参的手调
> - 核心思路：权重相位监控滑动窗口训练奖励，最小相位长度后 P_w 步无新高则停；harness 相位档案训练分 J* 在 P_h 轮无新高则停
> - 设计动机：**纯训练信号驱动、绝不看验证集**——避免调度规则本身成为信息泄漏通道；本质是 per-phase 的 early stopping

> **prompt 受限的 FST 对照**
> - 功能：隔离"harness 表达性"的贡献
> - 核心思路：与 WHALE 用完全相同的更新方法和调度，但 harness 搜索空间只限 system/user prompt
> - 设计动机：没有这个对照，"超过 prompt 联合优化"的声称无法归因到代码级 harness 搜索

> **预算匹配协议**
> - 功能：公平比较单组件与联合
> - 核心思路：weight-only 的 epoch 预算 = WHALE 全程累计训练 epoch；harness-only 的迭代预算 = 全程累计搜索迭代
> - 设计动机：排除"联合只是花更多算力"的混淆

### 3.3 【RSI 专项】可修改范围

- ☑ harness（prompts、工具 I/O 格式、错误反馈、停止准则、轮次预算；**verifier、环境、数据集固定**）
- ☑ 模型权重（RSFT，LoRA 之外的 full FT——论文用在线 SFT）
- ☐ 改进器自身（Meta-Harness proposer 固定）　☐ 训练算法（RSFT 固定）　☐ 调度规则（人工设定或由 patience 规则执行，均不可自改）
- 载体：harness 侧为代码文件系统编辑（Meta-Harness）；权重侧为梯度更新。

### 3.4 【RSI 专项】RSI 实现程度

**判级：L0 × 双杠杆**。这是本系列最需要强调边界的笔记之一：WHALE 是**外部优化器对 (θ,h) 的联合优化**，agent 不在改进回路内，无自指、无递归、无档案库演化动力学的自我修改。它与 Co-Harness（L5）的区别正是"联合优化 ≠ 联合递归"：Co-Harness 的 agent 参与改写自己的 harness，WHALE 的 proposer 是外置的。WHALE 的自我定位也诚实于此——它研究的是调度科学，不声称 RSI。

## 4. 实验

- **Benchmark**：SearchQA（7 个 QA 数据集 700 题，HotpotQA/NQ 训练）、Math（DAPO-Math-17K 训练，AIME 2024/2025 测试）、Chess Puzzles（Lichess，三数据集互不相交）；全部二值 verifier（SearchQA 用 GPT-5.4-mini judge + 固定 rubric；Math boxed 匹配；Chess python-chess 合法性+参考着法）。
- **协议**：共享 (θ₀,h₀)；weight-only 4/6/4 epochs，harness-only 40/60/40 迭代，WHALE (E,I)=(0.6,6)；测试 mean@8。
- **主结果**：WHALE 在全部三个域、全部 10 个子基准上最优（Table 2 逐数据集验证非子集带动）；超单组件较强者 +7.67~10.05pp，超 FST +4.15~13.00pp。
- **调度研究（全文精华）**：
  - 交替 vs 分段：分段式（先花完权重预算再花完 harness 预算）在 SearchQA/Math 分别落后 5.32/9.16pp，WHALE 用其 29%/49% 的 rollout 即超过分段终点；
  - 调度两端失效：Math 的 (0.2,2) 因证据不足采纳侥幸候选而**失稳终止**（noisy extreme 的实证标本）；扩大每周期预算从 (0.2,6)→(1.0,10) 单调变差（SearchQA 50.09→45.93）；
  - E 与 I 存在交叉交互：Math 中 E 从 0.2→0.6 在 I=2 时改善（16.67→17.92）但在 I=6 时恶化（28.33→24.79）——**调度超参不可独立选择**；
  - Adaptive WHALE 在 SearchQA 达全场最佳 52.82%（+2.73 超最优手调，省 23% rollout），Math 略低于最优手调（-1.87）。
- **行为归因**：SearchQA 的提升分解为检索准确率（harness 主导 26.88%→60.61%）与答案提取（权重主导）的正交通道；Math 的提升几乎全部来自截断率下降（95.83%→30.83%），harness 单独无法修。

## 5. 评估三问

- **Q1 内部判据**：harness 侧为选择式（档案 argmax，训练分）；权重侧为固定二值 verifier。**判据全程固定且人定**，无漂移机制。已知弱点：harness 候选每题仅 1 条 rollout 评分——选择噪声的直接来源，也是 noisy extreme 的机制解释。
- **Q2 外部审计**：预算匹配 + prompt 受限对照 + 逐数据集分解 + 行为指标归因，是本系列见过的联合优化工作中**最干净的审计设计**之一。缺口：所有域只测 Qwen3.5-2B/4B 一个规模档；SearchQA 的 judge 是 LLM（judge 提示词附录全文给出，可审计）。
- **Q3 量化方式**：rollout 成本逐法报告；**但 proposer（写 harness 的 LLM）的算力明确排除在核算外**（"exclude proposer compute"）——harness 搜索的真实成本被系统性低估。轨迹级质性证据充分（附录 D 三域并排轨迹）。

**总评**：Q2 的预算匹配与 FST 对照是范式级设计；Q3 的 proposer 成本排除是主要账目缺口。

## 6. Contribution 与结论

- 自陈贡献：联合框架、两种瓶颈域刻画、交替>分段、adaptive 调度。四条全部站得住，证据强度**强**（受控+预算匹配+行为归因）。
- 结论在证据范围内成立，且限定得当（不声称 RSI、不声称跨规模外推）。

## 7. 缺点与攻击面

- 作者自陈：需扩展到更大模型与更多域；黑盒接口允许替换两个算子（未做）。
- **额外缺点**：
  1. **proposer 成本不入账**——"harness 搜索更 rollout 高效"的对比（5.79% 追平）在计入 proposer 推理成本后可能反转；
  2. harness 相位在 256 题 D_harness 上 argmax——对 harness 过拟合训练集无 held-out 防护（Math 分段实验中"训练分涨、测试仅 +0.21"已经演示了这种过拟合）；
  3. 单规模档（2B/4B），"harness 先诊断"流程在强底座上的适用性未知——SICA 饱和发现提示该窗口随底座能力收窄。
- **最可能被攻击的点**：proposer 成本核算口径；harness 训练集过拟合。

## 8. 谱系定位

- **前置**：Meta-Harness（同组，harness 算子直接复用）；FST（Tiwari et al. 2026，作为 prompt 受限对照）；坐标下降文献。
- **后续影响**：作为"L5 联合递归"的调度科学底座——Co-Harness/ScienceBuddy 的双循环设计都隐含交替假设，本文是第一个对该假设做受控检验的。
- **一句话定位**：把"权重×harness 怎么协调"从工程直觉变成可测量的调度问题，并给出两端失效的实证标本。
- vs 对比：
  - **vs Co-Harness**：相同点=双杠杆交替；关键差异=Co-Harness 的 agent 在环（L5 递归），WHALE 的 proposer 外置（L0 联合优化）——递归性换受控性；
  - **vs SIA**：相同点=同攻"两杠杆协调"；关键差异=SIA 用 LLM 选杠杆（不可复现的启发式），WHALE 用固定/自适应调度规则（可复现、可消融）；
  - **vs Meta-Harness**：WHALE 是其"权重扩展版"，harness 算子原样复用。

| 维度 | 本文 | Co-Harness | SIA | Meta-Harness |
|---|---|---|---|---|
| 可修改范围 | harness+权重 | harness+权重（agent 在环） | harness+权重（LoRA） | 仅 harness |
| RSI 分级 | L0 双杠杆 | L5 | L2 双杠杆 | L1+ |
| 内部判据 | 固定二值 verifier + 档案 argmax | 归因→修复→回归门 | LLM 反馈代理选杠杆 | 训练分 argmax |
| 外部审计强度 | 强（预算匹配+FST 对照+行为归因） | 中（两轮即止） | 弱（混杂批评） | 中 |
| 成本核算 | rollout 级，proposer 除外 | 未系统报告 | 未系统报告 | 未系统报告 |

## 9. 批判性问题清单（供组会讨论）

1. （§5.2/6.1）proposer 的 LLM 推理成本被排除在 rollout 核算外——若计入，"harness-dominant 域先用 harness 诊断"的结论是否依然成立？给出含 proposer 成本的全账本会怎样改变结论？
2. （§3.2）harness 相位在固定 256 题上 argmax，无任何 held-out 防护——Math 分段实验已出现训练涨测试平的过拟合；为何不给 harness 相位也配 patience/验证分割？
3. （§6.2.2）E×I 交叉交互意味着调度景观是耦合的——adaptive 规则的 patience 参数（P_w, P_h）本身是否也存在同样的耦合敏感性？两域验证是否足以声称"免调参"？
4. （§B.3）SearchQA 用 GPT-5.4-mini 作 judge，而 harness 搜索的优化目标正是这个 judge 的判分——harness 是否学到了 judge-specific 的格式偏置而非检索能力？有无跨 judge 稳健性检验？
5. （§6.1）"harness-dominant/model-dominant"的划分基于 2B/4B 弱底座——该划分本身是底座能力的函数（对照 SICA 饱和发现）；在强底座上这个分类学是否还有操作意义？
