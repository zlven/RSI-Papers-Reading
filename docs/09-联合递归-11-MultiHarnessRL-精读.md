# Multi-Harness RL for Coding Agents：训练增益与 Harness 依赖的对照研究（精读笔记）

> 论文信息：*Multi-Harness Reinforcement Learning for Coding Agents: Training Gains and Harness Dependence*（arXiv:2609.04518，2026-09-03 v1 / **10-09 v2**）
> 精读日期：2026-10-20 | 阅读方式：**摘要级精读**（abstract 信息密度高，全文未逐节核）

---

## 0. 速览卡片

| 字段 | 内容 |
|---|---|
| 一句话概括 | 严格对照实验：多 harness RL 的训练增益温和（+0.48~+0.77pp）且不迁移到未见 harness，而**跨 harness 性能方差（7.13pp）比 RL 增益大一个数量级**——先修 harness，再谈训练 |
| 所属领域 | coding agent / RL 方法论 |
| Tags | #对照实验 #负面结果 #奖励归一化 #harness方差 #可迁移性 |
| RSI 分级 | **N/A（诊断/对照研究，无改进循环）** |
| 核心贡献标签 | Within vs Cross 归一化 / harness 方差主导 / 训练增益不实 |

## 1. 动机漏斗：六步走到问题

1. **大目标**：用 RL 训练更强的 coding agent。
2. **现状**：近期系统在**多个执行 harness** 上收集轨迹训 RL（隐含的假设：多接口训练带来接口鲁棒性）。
3. **裂缝**：训练 harness 下看到的增益留下两个未答问题——增益**迁移到未见接口吗**？多依赖**奖励归一化方式**？
4. **问题**：受控测量——同 SFT checkpoint、同 replay 数据、唯一变量是归一化规则。
5. **约束**：SWE-bench Verified，Qwen3-8B，四个训练 harness + 一个未见 harness，多 seed × 多评估预算。
6. **本文问题**：把"多 harness RL 有效"这个领域默认假设放到对照实验下检验。

## 2. Insight 与理论依据

### 核心发现（三条，按摘要编号）

**(i) 训练增益温和**：四个训练 harness 上，Within 归一化 +0.48pp，Cross +0.77pp（相对 SFT 基线）。多 harness RL 不是免费的午餐。

**(ii) 归一化规则无关紧要**：Cross 确实增加了非零优势轨迹比例（机制上合理：跨 harness 归一化拉大方差），但在未见 harness 上**两种规则都不显著超 SFT**——训练分布内的小增益不迁移。

**(iii) harness 方差主导一切**：平均掉模型变体后，源 harness 最高与最低 solve rate 相差 **7.13pp**——比训练增益（≤0.77pp）大近 10 倍。即使多 harness RL 之后，执行接口间的性能差仍远大于训练增益和归一化差异。

### 对联合递归文献的含义

这是给整个 harness×weight 联合领域的一盆冷水：WHALE/Co-Harness 们报告的组合增益，需要与"harness 选择本身造成的方差"（7.13pp 量级）比较才有意义。若联合优化的总增益小于换个 harness 的方差，联合优化的价值主张不成立——**Q3 归因纪律的硬约束**。

## 3. 方法拆解（实验设计）

### 对照结构（方法即设计）

```
同一 SFT checkpoint（Qwen3-8B）
  ├─ RL-Within：奖励在每个 harness 内归一化
  └─ RL-Cross：奖励跨 harness 归一化
  （唯一变量：归一化规则；replay 数据完全相同）
评估：四个训练 harness + 一个 held-out harness
多 seed × 多评估预算
```

**设计点评**：
- 同 checkpoint + 同数据 + 单变量——教科书级对照；
- held-out harness 是关键（测的是**接口泛化**而非训练集记忆）；
- 多 seed × 多预算的稳健性声明直接回应 Gödel Agent 系工作的方差盲区。

## 4. 实验数字（摘要）

| 量 | 值 |
|---|---|
| Within 训练增益（4 harness 均值） | +0.48pp |
| Cross 训练增益（4 harness 均值） | +0.77pp |
| 未见 harness 上两规则 vs SFT | 均不显著 |
| 源 harness 最高-最低 solve rate 差 | **7.13pp** |

模型：Qwen3-8B；benchmark：SWE-bench Verified。

## 5. 评估三问

**Q1 内部标准**：无内部改进循环（对照研究，无门）。
**Q2 外部审计**：held-out harness + 多 seed + 多预算 + 公开 benchmark——12 篇里审计纪律**最严格**之一，与 Ceiling 论文并列"诊断方法论双壁"。
**Q3 量化**：方差分解思想明确（训练增益 vs 归一化 vs harness 选择三源分离）；"7.13pp ≫ 0.77pp"是 Q3 归因的标杆式陈述。

## 6. Contribution 提炼

1. **证伪领域默认假设**：多 harness RL 的接口鲁棒性声称在受控条件下不成立。
2. **方差层级排序**：harness 选择（7.13pp）> 训练（≤0.77pp）≈ 归一化规则——给"先优化什么"提供了量化优先级。
3. **方法论模板**：同 checkpoint/同数据/单变量/held-out 接口的对照设计，可直接复用到任何"harness 相关声称"的检验。

## 7. 缺点与攻击面

1. **8B 单模型、单 benchmark**：增益温和可能是小模型现象——frontier 模型的 RL 头部空间更大（Ceiling 论文的 regime 依赖警告适用）。结论外推需谨慎。
2. **四个训练 harness 的多样性未量化**：若四者同质，"多 harness"名不副实；harness 间距离需要度量。
3. **不否认联合优化**：本文证伪的是"多 harness RL 训练带来接口泛化"，不是"harness 多样性无用"——HarnessBandit（下篇）正是用调度挖掘同一设置的价值，两者不矛盾。
4. **solve rate 单指标**：未报成本/轨迹质量维度。

## 8. 谱系定位

**在 12 篇中的角色**：与 Ceiling 论文（04 号）同为**诊断方法论**，但作用点不同——Ceiling 分解"harness vs 权重谁能救哪种失败"，本篇分解"harness 方差 vs 训练增益谁主导"。两篇合读给出联合优化的两条可行性约束：

- Ceiling：权重救内容失败，harness 救过程失败（救错对象无效）；
- 本篇：harness 选择的方差 ≫ RL 增益（忽略 harness 选择的训练收益会被噪声淹没）。

**对你的研究**：这是写 follow-up 论文 motivation 的弹药库——"多 harness RL 增益 ≤0.77pp 且不迁移"说明**朴素联合**不够，为主动调度（HarnessBandit）或共同进化（HELIX 声称的方向）留出空间。同时它也是你自己实验设计的纪律模板。

## 9. 批判性问题清单

1. 8B 上成立，27B/70B 上方差层级排序会变吗？（规模×harness 方差交互）
2. 四个训练 harness 的成对距离怎么度量？多样性与泛化的剂量关系？
3. 未见 harness 不迁移——是接口表面差异（prompt/工具 schema）还是交互结构差异（控制流）导致？需要机制分析。
4. Cross 的非零优势轨迹更多却不迁移——这些"额外学习信号"学到了什么？（可能是 harness 特异噪声）
5. 7.13pp 的 harness 方差在 frontier 模型上是否压缩？（若压缩，"harness 工程时代结束于模型变强"的论点复活）

---

*系列：RSI 精读 | 分区：09-联合递归 | 编号：11*
