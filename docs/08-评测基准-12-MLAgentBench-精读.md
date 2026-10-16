# MLAgentBench 精读报告

> 按 RSI 论文精读模板 v1.0 生成（卡片式）

## 0. 论文元信息

- **标题**：MLAgentBench: Evaluating Language Agents on Machine Learning Experimentation
- **作者**：Qian Huang、Jian Vora、Percy Liang、Jure Leskovec
- **发表**：2023（笔记记为 NeurIPS 2023 Datasets & Benchmarks）；arXiv:2310.03302（2023-10）
- **一句话总结**：13 个 ML 实验任务，Agent 读写文件并执行代码，ReAct 基线成功率 37.5%。

## 1. 要点

- 最早的 ML 研发 Agent 基准之一（2023 概念验证期的产物）；
- 轻量、易跑，适合作为改进回路的**内层验收信号**（DGM 类系统的验收器常用此类信号）；
- 局限：规模小、任务短程，2023 年的难度对 2026 年模型已基本饱和。

## 2. 定位与批判性问题

- 定位：对象层基准的历史起点；现主要用于内层信号而非能力声明。
- 问题：任务饱和后作为内层验收信号是否还有区分度？

| 维度 | 本文 |
|---|---|
| 测量层 | 对象层（轻量） |
| 关键数字 | 13 任务 / ReAct 37.5% |
