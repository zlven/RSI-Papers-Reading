# 参考文献清单

> 本清单由仓库根目录的 `scripts/extract_refs.py` 从各篇精读头部的「论文信息」块自动抽取生成，运行该脚本即可刷新。
> 脚本只转录笔记中已写明的内容，**不猜测 arXiv 编号**；标注「待补」的条目表示原笔记未写明编号。

共 49 篇文献。

| 分类 | 篇数 |
|---|---|
| 01 · 主线：哥德尔式 RSI 与自我改进智能体 | 18 |
| 02 · 综述与立场 | 3 |
| 03 · 其他路线：权重自编辑与经典自举 | 8 |
| 04 · 零数据自博弈 | 7 |
| 05 · 进化搜索 | 6 |
| 06 · 经验与上下文 | 4 |
| 07 · 自动化科研 | 3 |

## 01 · 主线：哥德尔式 RSI 与自我改进智能体

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements | Jürgen Schmidhuber（IDSIA & TU München） | IDSIA 技术报告 2003 / Springer《Artificial General Intellige… | [arXiv:cs/0309048](https://arxiv.org/abs/cs/0309048) | [笔记](01-主线-01-Gödel%20Machine理论源头-精读.md) |
| 02 | Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation | Eric Zelikman、Eliana Lorch、Lester Mackey、Adam Tauman Kalai（Stanford / Microsoft Researc… | arXiv:2310.02304（2023 年 10 月），COLM 2024 | [arXiv:2310.02304](https://arxiv.org/abs/2310.02304) | [笔记](01-主线-02-STOP-精读.md) |
| 03 | Automated Design of Agentic Systems | Shengran Hu, Cong Lu, Jeff Clune | ICML 2025 | [arXiv:2408.08435](https://arxiv.org/abs/2408.08435) | [笔记](01-主线-03-ADAS-精读.md) |
| 04 | Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement | Xunjian Yin、Xinyi Wang、Liangming Pan、Li Lin、Xiaojun Wan、William Yang Wang（北京大学 / UC San… | arXiv:2410.04444（2024 年 10 月），ACL 2025；代码开源 | [arXiv:2410.04444](https://arxiv.org/abs/2410.04444) | [笔记](01-主线-04-Gödel%20Agent-精读.md) |
| 05 | A Self-Improving Coding Agent (SICA) | Maxime Robeyns、Martin Szummer、Laurence Aitchison（布里斯托大学 / iGent AI） | arXiv:2504.15228（2025 年 4 月）；标准 Python 实现、无 DSL、全开源 | [arXiv:2504.15228](https://arxiv.org/abs/2504.15228) | [笔记](01-主线-05-SICA-精读.md) |
| 06 | Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents | Jenny Zhang*、Shengran Hu*、Cong Lu、Robert Lange、Jeff Clune（UBC / Vector Institute / Saka… | arXiv:2505.22954（2025 年 5 月），ICLR 2026 Oral；代码开源 | [arXiv:2505.22954](https://arxiv.org/abs/2505.22954) | [笔记](01-主线-06-Darwin%20Gödel%20Machine-精读.md) |
| 07 | Hierarchical Gödel Machine | KAUST | 预印本 2025 | **待补** | [笔记](01-主线-07-HGM-精读.md) |
| 08 | Live‑SWE‑agent | UIUC 团队 | 预印本 2025 | **待补** | [笔记](01-主线-08-Live-SWE-agent-精读.md) |
| 09 | Harnesses That Improve Themselves | Hangfan Zhang, Shao Zhang, Kangcong Li, Chen Zhang, Yang Chen, Yiqun Zhang, Lei Bai, Sh… | 预印本 2026 | [arXiv:2606.09498](https://arxiv.org/abs/2606.09498) | [笔记](01-主线-09-Self-Harness-精读.md) |
| 10 | Co‑Evolving Harnesses and Model Weights for LLM Agents | Zhengyu Chen, Teng Xiao, Huaisheng Zhu, Yige Yuan, Luan Zhang, Jingang Wang | 预印本 2026 | [arXiv:2607.22688](https://arxiv.org/abs/2607.22688) | [笔记](01-主线-10-Co-Harness-精读.md) |
| 11 | Self‑Evolution through Source‑Level Rewriting in Autonomous Agent Systems | Qianshu Cai, Yonggang Zhang, Xianzhang Jia, Huajiang Zheng, Wei Xue, Jun Song, Xinmei T… | 预印本 2026 | [arXiv:2605.22794](https://arxiv.org/abs/2605.22794) | [笔记](01-主线-11-MOSS-精读.md) |
| 12 | A Self‑Evolving Agent Protocol | Wentao Zhang, Zhe Zhao, Haibin Wen, Yingcheng Wu, Cankun Guo, Ming Yin, Bo An, Mengdi W… | 预印本 2026 | [arXiv:2604.15034](https://arxiv.org/abs/2604.15034) | [笔记](01-主线-12-Autogenesis-精读.md) |
| 13 | Agentic Harness Engineering | Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Hua… | 预印本 2026 | [arXiv:2604.25850](https://arxiv.org/abs/2604.25850) | [笔记](01-主线-13-AHE-精读.md) |
| 14 | Hierarchical Agent Loop Optimizer（Context Labs） | Context Labs / inference.net | 开源项目（非 arXiv 论文） | [context-labs/halo](https://github.com/context-labs/halo) | [笔记](01-主线-14-HALO-精读.md) |
| 15 | End‑to‑End Optimization of Model Harnesses | Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn | 预印本 2026 | [arXiv:2603.28052](https://arxiv.org/abs/2603.28052) | [笔记](01-主线-15-Meta-Harness-精读.md) |
| 16 | DemoEvolve | Lirong Che, Yuzhe Yang, Peiwen Lin, Chuang Wang, Xueqian Wang, Jian Su | 预印本 2026 | [arXiv:2605.24539](https://arxiv.org/abs/2605.24539) | [笔记](01-主线-16-DemoEvolve-精读.md) |
| 17 | Red Queen Gödel Machine（智能体与其评估器的共同进化） | Alex Iacob, Andrej Jovanović, William F. Shen, Daniel Burkhardt, Meghdad Kurmanji, Nurb… | 预印本 2026 | [arXiv:2606.26294](https://arxiv.org/abs/2606.26294) | [笔记](01-主线-17-Red%20Queen%20Gödel%20Machine-精读.md) |
| 18 | Hierarchical Self‑Improvement | Tailin Zhou | 预印本 2026 | [arXiv:2608.08466](https://arxiv.org/abs/2608.08466) | [笔记](01-主线-18-Hierarchical%20Self-Improvement-精读.md) |

## 02 · 综述与立场

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Recursive Self‑Improvement in AI: From Bounded Self‑Refinement to Autonomous Research Loops | Mingguang Chen, Licheng Wang, Bo Qu | 预印本 2026 | [arXiv:2607.07663](https://arxiv.org/abs/2607.07663) | [笔记](02-综述-01-Bounded-to-Autonomous-综述-精读.md) |
| 02 | The Last AI Built by Humans: Toward Genuine Recursive Self‑Improvement | Yi Duan, Ying Liu, Zirui Tang, …, Xuanhe Zhou, Fan Wu 等 36 位作者 | 预印本 2026 | [arXiv:2609.11873](https://arxiv.org/abs/2609.11873) | [笔记](02-综述-02-The%20Last%20AI%20Built%20by%20Humans-精读.md) |
| 03 | When AI Builds Itself（Anthropic Institute, 2026-06-04） | Marina Favaro & Jack Clark，Anthropic Institute，2026-06-04 发布 | Anthropic Institute 立场报告 | —（非 arXiv 文献） | [笔记](02-综述-03-Anthropic-When%20AI%20Builds%20Itself-精读.md) |

## 03 · 其他路线：权重自编辑与经典自举

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Self‑Adapting Language Models | Adam Zweiger, Jyothish Pari, Han Guo, Ekin Akyürek, Yoon Kim, Pulkit Agrawal | NeurIPS 2025 | [arXiv:2506.10943](https://arxiv.org/abs/2506.10943) | [笔记](03-其他路线-01-SEAL-精读.md) |
| 02 | Self‑Adaptive LLMs | Qi Sun, Edoardo Cetin, Yujin Tang | 预印本 2025 | [arXiv:2501.06252](https://arxiv.org/abs/2501.06252) | [笔记](03-其他路线-02-Transformer²-精读.md) |
| 03 | STaR: Bootstrapping Reasoning with Reasoning | Zelikman, Wu, Mu, Goodman | NeurIPS 2022 | [arXiv:2203.14465](https://arxiv.org/abs/2203.14465) | [笔记](03-其他路线-03-STaR-精读.md) |
| 04 | Beyond Human Data: Scaling Self-Training for Problem-Solving with Language Models | Singh et al. (Google DeepMind) | TMLR 2023 | [arXiv:2312.06585](https://arxiv.org/abs/2312.06585) | [笔记](03-其他路线-04-ReST-EM-精读.md) |
| 05 | Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al | NeurIPS 2023 | [arXiv:2303.17651](https://arxiv.org/abs/2303.17651) | [笔记](03-其他路线-05-Self-Refine-精读.md) |
| 06 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn, Yao et al | NeurIPS 2023 | [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) | [笔记](03-其他路线-06-Reflexion-精读.md) |
| 07 | Self-Rewarding Language Models | Yuan, Weston et al. (Meta AI) | ICML 2024 | [arXiv:2401.10020](https://arxiv.org/abs/2401.10020) | [笔记](03-其他路线-07-Self-Rewarding-LM-精读.md) |
| 08 | Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models | Chen, Deng, Yuan, Ji, Gu (UCLA) | ICML 2024 | [arXiv:2401.01335](https://arxiv.org/abs/2401.01335) | [笔记](03-其他路线-08-SPIN-精读.md) |

## 04 · 零数据自博弈

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Absolute Zero: Reinforced Self-play Reasoning with Zero Data | Zhao, Wu, Yue, Wu, Xu, Lin, Wang, Wu, Zheng, Huang | 预印本 2025 | [arXiv:2505.03335](https://arxiv.org/abs/2505.03335) | [笔记](04-零数据自博弈-01-Absolute-Zero-精读.md) |
| 02 | R-Zero: Self-Evolving Reasoning LLM from Zero Data | Huang, Yu, Wang, Zhang, Li, Li, Huang, Mi, Yu（Tencent AI Seattle Lab / WUSTL / UMD / UT… | 预印本 2025 | [arXiv:2508.05004](https://arxiv.org/abs/2508.05004) | [笔记](04-零数据自博弈-02-R-Zero-精读.md) |
| 03 | Socratic-Zero: Bootstrapping Reasoning via Data-Free Agent Co-evolution | Wang, Jiao, Zhang, Peng, Ze, Yang, Wang, Wei, Zhang | 预印本 2025 | [arXiv:2509.24726](https://arxiv.org/abs/2509.24726) | [笔记](04-零数据自博弈-03-Socratic-Zero-精读.md) |
| 04 | Vision-Zero: Scalable VLM Self-Improvement via Strategic Gamified Self-Play | Wang, Liu, Zhou, Shi, Lin, Chen, Li, Wan, Zhao | 预印本 2025 | [arXiv:2509.25541](https://arxiv.org/abs/2509.25541) | [笔记](04-零数据自博弈-04-Vision-Zero-精读.md) |
| 05 | SPICE: Self-Play In Corpus Environments Improves Reasoning | Liu, Jin, Kim, Yuan, Zhao, Kulikov, Li, Sukhbaatar, Lanchantin, Weston（Meta FAIR 等） | 预印本 2025 | [arXiv:2510.24684](https://arxiv.org/abs/2510.24684) | [笔记](04-零数据自博弈-05-SPICE-精读.md) |
| 06 | Self-Challenging Language Model Agents | Zhou, Yu, Levine, Weston, Li, Sukhbaatar（Meta / UC Berkeley 等） | 预印本 2025 | [arXiv:2506.01716](https://arxiv.org/abs/2506.01716) | [笔记](04-零数据自博弈-06-Self-Challenging-精读.md) |
| 07 | SeRL: Self-Play Reinforcement Learning for Large Language Models with Limited Data | Fang, Liu, Zhou, Zhang, Zheng, Chen, Song, Tao 等 | 预印本 2034 | [arXiv:2505.20347](https://arxiv.org/abs/2505.20347) | [笔记](04-零数据自博弈-07-SeRL-精读.md) |

## 05 · 进化搜索

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Mathematical discoveries from program search with large language models | Romera-Paredes, Barekatain, Novikov et al. (DeepMind) | Nature 2024 | **待补** | [笔记](05-进化搜索-01-FunSearch-精读.md) |
| 02 | AlphaEvolve: A coding agent for scientific and algorithmic discovery | Novikov, Vũ, Eisenberger, Dupont et al. (Google DeepMind) | 预印本 2025 | [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) | [笔记](05-进化搜索-02-AlphaEvolve-精读.md) |
| 03 | ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution | Lange, Imajuku, Cetin（Sakana AI） | 预印本 1934 | [arXiv:2509.19349](https://arxiv.org/abs/2509.19349) | [笔记](05-进化搜索-03-ShinkaEvolve-精读.md) |
| 04 | ThetaEvolve: Test-time Learning on Open Problems | Wang, Su, Zeng, Xu, Ren, Yang, Huang, He, Ma, Peng, Cheng, He, Chen, Wang, Du, Shen | 预印本 2025 | [arXiv:2511.23473](https://arxiv.org/abs/2511.23473) | [笔记](05-进化搜索-04-ThetaEvolve-精读.md) |
| 05 | EvoGit: Decentralized Code Evolution via Git-Based Multi-Agent Collaboration | Huang et al | 预印本 2049 | [arXiv:2506.02049](https://arxiv.org/abs/2506.02049) | [笔记](05-进化搜索-05-EvoGit-精读.md) |
| 06 | LLM2LLM: Boosting LLMs with Novel Iterative Data Enhancement | Lee, Wattanawong, Kim, Mangalam, Shen, Anumanchipalli, Mahoney, Keutzer, Gholami（UC Ber… | ACL 2024 | [arXiv:2403.15042](https://arxiv.org/abs/2403.15042) | [笔记](05-进化搜索-06-LLM2LLM-精读.md) |

## 06 · 经验与上下文

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | Voyager: An Open-Ended Embodied Agent with Large Language Models | Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar | TMLR 2023 | [arXiv:2305.16291](https://arxiv.org/abs/2305.16291) | [笔记](06-经验与上下文-01-Voyager-精读.md) |
| 02 | Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models | Zhang et al.（Stanford / SambaNova / UC Berkeley） | 预印本 2025 | [arXiv:2510.04618](https://arxiv.org/abs/2510.04618) | [笔记](06-经验与上下文-02-ACE-精读.md) |
| 03 | EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle | Wu, Wang, Mei, Cai, Fu, Yang, Wen, Yang, Shen, Wang, Shi（上海人工智能实验室 KnowledgeXLab / 浙江大学） | ICML 2026 | [arXiv:2510.16079](https://arxiv.org/abs/2510.16079) | [笔记](06-经验与上下文-03-EvolveR-精读.md) |
| 04 | AFlow: Automating Agentic Workflow Generation | Zhang, Xiang et al.（MetaGPT 团队） | ICLR 2025 | [arXiv:2410.10762](https://arxiv.org/abs/2410.10762) | [笔记](06-经验与上下文-04-AFlow-精读.md) |

## 07 · 自动化科研

| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |
|---|---|---|---|---|---|
| 01 | The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery | Lu, Lu, Lange, Foerster, Clune, Ha（Sakana AI / Oxford / UBC） | Science 2024 | [arXiv:2408.06292](https://arxiv.org/abs/2408.06292) | [笔记](07-自动化科研-01-AI-Scientist-精读.md) |
| 02 | The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search | Yamada et al.（Sakana AI 等） | ICLR 2025 | [arXiv:2504.08066](https://arxiv.org/abs/2504.08066) | [笔记](07-自动化科研-02-AI-Scientist-v2-精读.md) |
| 03 | Recursive self-improvement of AI research agents | Srikanth et al.（Weco AI） | 预印本 2026 | [arXiv:2609.26457](https://arxiv.org/abs/2609.26457) | [笔记](07-自动化科研-03-AIDE2-RSI-of-AI-Research-Agents-精读.md) |

## 待补 arXiv 编号

以下条目的原笔记头部未写明 arXiv 编号。脚本不作推断，确认后请补入对应笔记的元信息块：

- `01-主线-07-HGM-精读.md`
- `01-主线-08-Live-SWE-agent-精读.md`
- `01-主线-14-HALO-精读.md`
- `02-综述-03-Anthropic-When AI Builds Itself-精读.md`
- `05-进化搜索-01-FunSearch-精读.md`
