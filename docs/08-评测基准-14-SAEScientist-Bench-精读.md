# SAEScientist-Bench 精读报告

> 按 RSI 论文精读模板 v1.0 生成（卡片式）

## 0. 论文元信息

- **标题**：SAEScientist-Bench（Can AI Agents Conduct Autonomous SAE Interpretability Research?）
- **作者**：Yuqiao Tan、Shizhu He、Jun Zhao、Kang Liu
- **发表**：arXiv:2609.09113（2026-09）
- **一句话总结**：让 Agent 自主做 SAE 可解释性研究——给定目标概念与 Gemma Scope 的 131K+ SAE 特征字典做对比探测。

## 1. 要点

- 意义特殊：把"AI 做 AI 安全研究"本身变成可测对象——若可解释性研究可自动化，安全研究的递归加速也成为可能；
- 评分：按激活排名/概念选择性/因果转向与专家参照的距离；
- 属"窄而深"的领域基准，与 SAHOO 同属 RSI Workshop 生态。

## 2. 批判性问题

1. 专家参照的唯一性——SAE 分析存在多种合理解，单一参照是否压制有效的新方法？
2. 该能力增长对安全是净正（更多可解释性人力）还是净负（攻击者也可用）？

| 维度 | 本文 |
|---|---|
| 测量层 | 对象层（安全研究专项） |
| 特殊性 | 自动化 AI 安全研究的可测化 |
