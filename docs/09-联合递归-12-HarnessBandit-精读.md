# HarnessBandit：多 Harness Agentic RL 的可学习性-迁移性联合调度（精读笔记）

> 论文信息：*HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning*（arXiv:2609.13739，2026-09-12，v1，162 KB——篇幅小，方法集中）
> 精读日期：2026-10-20 | 阅读方式：**摘要级精读**（abstract，全文未逐节核）

---

## 0. 速览卡片

| 字段 | 内容 |
|---|---|
| 一句话概括 | 多 harness 训练不是混在一起就行，而是一个**调度问题**：每个 optimizer step 用 bandit 选一个 harness，选择信号 = 可学习性（batch 平均绝对优势）× 迁移性（梯度 sketch 余弦），在 held-out 任务+harness 上超过 mixed-batch |
| 所属领域 | agentic RL / 在线调度 |
| Tags | #harness调度 #bandit #learnability #transferability #梯度sketch |
| RSI 分级 | **L0.5（训练优化器，harness 是选择对象非改进对象）** |
| 核心贡献标签 | 调度形式化 / 双信号融合 / held-out 双评估 |

## 1. 动机漏斗：六步走到问题

1. **大目标**：训练对 harness 变化鲁棒的共享策略。
2. **现状**：同一模型在不同 harness（system prompt、工具 schema、控制循环、轨迹格式）上表现不均——鲁棒性成为目标。
3. **自然方案**：多 harness 训共享策略。但 **Multi-Harness RL（2609.04518）刚证明**：朴素混合增益温和（≤0.77pp）且不迁移。
4. **裂缝**：混合失败的机制——每个训练步该选哪个 harness 是未被优化的自由度：应选**当前能提供有用学习信号**、且**其更新能惠及其它 harness** 的那个。
5. **约束**：两个目标可能冲突（最易学的 harness 未必迁移最好），需要在线平衡，还要防止调度器塌缩到单一 harness。
6. **本文问题**：把 harness 选择形式化为带双信号的在线调度（bandit）问题。

## 2. Insight 与理论依据

### 两个信号的分解（本文的概念贡献）

**Learnability（可学习性）**：GRPO 更新后观测 batch 的**平均绝对优势**——这组轨迹此刻有没有学习信号（优势≈0 的 batch 是浪费算力）。

**Transferability（迁移性）**：当前 harness 的**低维梯度 sketch** 与其余 harness 梯度 EMA 的**余弦相似度**——在这个 harness 上算的梯度方向，与其它 harness 需要的方向是否一致。用 sketch（降维投影）而非全梯度，成本控制意识明确。

**融合的工程细节**（摘要级可见的纪律）：池化滑动窗 min-max 归一化（两信号量纲不同且随训练漂移）+ 访问依赖 bonus（UCB 式，防塌缩）+ 显式探索下限（保底采样）。诊断发现**两个信号是不同且演化的**——验证分解非冗余。

### 与 Multi-Harness RL 的关系

直接建设性回应：既然 harness 间方差大且混合训练增益小，那把"harness 混合比例"从均匀/固定变成**在线优化的调度变量**。这是"诊断→机制"的标准科学推进，两篇应合读。

## 3. 方法拆解（摘要可推断部分）

```
每个 optimizer step：
  1. 对六个 harness 计算双信号（learnability / transferability）
  2. 池化滑动窗 min-max 归一化后融合
  3. 加访问 bonus + 探索下限，采样选出一个 harness
  4. 该 harness 收集 batch → GRPO 更新 → 更新信号统计
```

**关键设计点评**：
- **梯度 sketch 余弦**做迁移性代理：避免跨 harness 全梯度比较的成本，且 sketch 的投影维度是 bias-variance 旋钮（摘要未给维度，全文待查）；
- **EMA 做其它 harness 的参考**：平滑调度噪声，但 EMA 滞后与策略漂移的冲突待消融；
- 调度器自身**不更新权重**——是训练器的 harness 选择策略，不是被训对象（分级停在 L0.5 的原因）。

## 4. 实验声称（摘要，未核）

- 设置：Qwen3.5-2B × **六个 harness** × ClawGym 训练；
- 评估双 benchmark：**PinchBench**（held-out 任务，分布内 OpenClaw harness）+ **ClawEval**（held-out 任务 **和** held-out harness）；
- 结果：两个 benchmark 均超 mixed-batch 多 harness 训练基线；
- 诊断：learnability 与 transferability 提供**distinct, evolving** 信号。

**注意评估纪律**：ClawEval 的 held-out harness 直接回应 Multi-Harness RL 的"不迁移"发现——调度器学的不是某个 harness 的偏好，而是选择策略。但摘要**未给具体增益数字**（只说 improves over）——162 KB 小篇幅 + 无数字摘要，增益幅度存疑，需全文核实。

## 5. 评估三问

**Q1 内部标准**：双信号在线估计 + 探索下限——调度器自身的防塌缩机制。
**Q2 外部审计**：held-out 任务（PinchBench）+ held-out 任务×harness（ClawEval）双层；但缺增益幅度数字、seed 数未知。
**Q3 量化**：信号分解的诊断（distinct/evolving）是过程量化；结果量化不足。

## 6. Contribution 提炼

1. **调度形式化**：把多 harness 训练从"数据混合"重构为"逐步 bandit 调度"——问题定义贡献。
2. **双信号分解**：learnability（当下值不值学）× transferability（学了惠及谁）——可直接移植到任何多源 RL（多任务、多环境、多域）。
3. **梯度 sketch 的实用方案**：低成本迁移性估计。
4. **对负面结果的建设性回应**：证明 Multi-Harness RL 的温和增益不是多 harness 训练的上限，而是朴素混合的上限。

## 7. 缺点与攻击面

1. **摘要无增益数字**：improves over 的幅度决定本文分量——若只有 1-2pp，则仍被 harness 间方差（7.13pp）主导，调度价值有限；若有 5pp+，则成立。全文第一查证点。
2. **2B 模型 + ClawGym**：生态与主流 SWE-bench 系隔离，横向可比性差；2B 上调度敏感，大模型上梯度方向跨 harness 可能天然更一致（transferability 信号退化）。
3. **调度器开销**：每步六 harness 的信号计算（含梯度 sketch）成本未报——若开销吃掉增益，实用性打折。
4. **harness 集合固定**：调度在固定六元集合上选；新 harness 加入（cold start）时 EMA 无历史——与 HELIX 的 harness 进化（集合本身增长）不兼容，两者是"选择 vs 生成"的分工。

## 8. 谱系定位

**在 12 篇分类中**：E 类（训练侧）第二篇，与 EvoTrainer 互补——EvoTrainer 改训练 harness 的内容，HarnessBandit 调度推理 harness 在训练中的使用。加上 Multi-Harness RL（诊断），三篇构成"训练侧 harness 利用"的问题-诊断-机制小生态：

| 篇 | 角色 | 一句话 |
|---|---|---|
| Multi-Harness RL | 诊断 | 朴素混合增益小且不迁移，harness 方差主导 |
| **HarnessBandit** | 机制（选择） | 逐步调度双信号，超 mixed-batch |
| EvoTrainer | 机制（改造） | 训练 harness 本身可进化（诊断/干预/技能） |

**对你的研究**：双信号是可直接借用的工具——若你做 DGM 系 follow-up，**存档变体的 parent 选择**（DGM 用 性能×1/children）可以换成 learnability×transferability 双信号，是有理论依据的增量改进点，且实现成本低。

## 9. 批判性问题清单

1. 两个 benchmark 上的具体增益幅度与置信区间？（决定本文分量）
2. sketch 维度、EMA 系数、探索下限三个超参的敏感性？
3. 调度学到的 harness 访问分布长什么样？是否出现"先学易后学难"的课程模式？（最有信息量的分析）
4. 大模型（>7B）上 transferability 信号是否退化（梯度天然一致 → 调度退化为 learnability 单信号）？
5. 与 EvoTrainer 组合的可行性：调度的 harness 集合由 EvoTrainer 式方法生成/改造——"生成-调度"双层架构是否成立？

---

*系列：RSI 精读 | 分区：09-联合递归 | 编号：12*
