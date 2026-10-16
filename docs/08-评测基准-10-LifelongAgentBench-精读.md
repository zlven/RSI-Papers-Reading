# LifelongAgentBench 精读报告

> 按 RSI 论文精读模板 v1.0 生成（卡片式）

## 0. 论文元信息

- **标题**：LifelongAgentBench: Evaluating LLM Agents as Lifelong Learners
- **发表**：arXiv:2505.11942（2025）
- **一句话总结**：首个统一评估 LLM Agent 终身学习能力的基准——DB/OS/KG 三环境 + 经验回放协议。

## 1. 动机与方法

- 问题：经验积累对 Agent 是否有益、哪种经验表示最好？
- 设计：三个交互环境（数据库、操作系统、知识图谱）；经验回放（1–16 条历史轨迹）+ group self-consistency 协议。

## 2. 评估三问与定位

- **Q3 量化**：AP（平均性能）/ FWT（前向迁移）/ BWT（后向迁移）/ FGT（遗忘）四指标——该四联指标已成为终身 Agent 评测的通用语。
- 定位：经验簇入口基准；后继者 PATH-Bench 补上了它缺的路径依赖控制。
- 批判性问题：经验回放协议假设经验"可检索且相关"，对经验被错误泛化（SEABench 的上下文边界坍塌）无测量。

| 维度 | 本文 |
|---|---|
| 测量层 | 在线进化（记忆层） |
| 核心贡献 | AP/FWT/BWT/FGT 四联指标 |
