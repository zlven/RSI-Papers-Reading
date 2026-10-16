# RSI 文献精读

**递归自我改进（Recursive Self-Improvement, RSI）方向的论文精读笔记。**

从哥德尔机（Gödel Machine）的理论源头出发，沿"自我改进智能体"的实证谱系一路读到评估器可改写的
前沿工作，并横向覆盖零数据自博弈、进化搜索、经验与上下文、自动化科研等相关路线。
每篇都是**独立精读**：判断只基于该论文自身文本，不做预设的跨文对比。

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Docs](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E9%98%85%E8%AF%BB-GitHub%20Pages-4f46e5)](https://zlven.github.io/RSI-Papers-Reading/)

> **在线浏览**：<https://zlven.github.io/RSI-Papers-Reading/>
> （带左侧分类导航、中文全文检索、深色模式；也可直接点开 `docs/` 下的 Markdown 文件阅读。）

---

## 收录规模

| 分类 | 篇数 | 主题 |
|---|---:|---|
| **01 · 主线** | 24 | 哥德尔式 RSI 与自我改进智能体：Gödel Machine → STOP → Gödel Agent → SICA → DGM → MGM → HGM → HyperAgents → MetaSkill-Evolve → Self-/Co-Harness → RQGM → RSI-Anything → SIFT / GEA |
| **02 · 综述与立场** | 5 | 领域综述、RSI 分级框架与前沿实验室的立场报告 |
| **03 · 其他路线** | 8 | 权重自编辑与经典自举：SEAL、Transformer²、STaR、ReST-EM、Self-Refine、Reflexion、Self-Rewarding、SPIN |
| **04 · 零数据自博弈** | 7 | 无人类数据时判据从何而来：Absolute Zero、R-Zero、Socratic-Zero、Vision-Zero、SPICE、Self-Challenging、SeRL |
| **05 · 进化搜索** | 6 | FunSearch、AlphaEvolve、ShinkaEvolve、ThetaEvolve、EvoGit、LLM2LLM |
| **06 · 经验与上下文** | 4 | 经验资产化的载体谱系：Voyager、ACE、EvolveR、AFlow |
| **07 · 自动化科研** | 4 | AI Scientist v1/v2、AIDE²、AIDE |
| **08 · 评测基准** | 15 | "怎样才算真的在改进"：对象层代理基准、回路层审计、安全压测、过程与终身层 |
| **合计** | **73** | 完整清单见 [`docs/references.md`](docs/references.md) |

## 分析框架

每篇精读按精读模板撰写（现行 [v2.0](docs/template.md)，另有 [v1.0 历史版本](docs/template-v1.md)——
现有 73 篇均按 v1.0 写成），节数随阅读深度分**三档**——**完整精读**（`## 0.`–`## 9.`，58 篇）、
**简读**（至少 `## 0.`–`## 4.`，6 篇）、**卡片式**（至少 `## 0.`–`## 2.`，9 篇）。
档位在[总索引](docs/index.md)每行标注；`check_notes.py` 按对应档位校验必备小节，档位不同不算「缺小节」。
其中两个框架贯穿全系列：

**评估三问** —— 每篇第 5 节回答：

- **Q1 内部判据**：系统自己如何判断一次修改"成立"？（门控式 / 选择式 / 契约式 / 执行反馈 / 学习评判器 / 环境锚定 / 外部神谕 …）
- **Q2 外部审计**：旁观者如何判断它"真的在改进"？（held-out 基准 / 固定预算 / 独立实现 / 人类审计 / 真实同行评审 …）
- **Q3 量化方式**：改动如何被量化？（标量适应度 / 偏序支配 / 通过率差 / 成本帕累托 …）

**RSI 分级** —— 用 L0 → L5+ 标注每篇工作"自指到了哪一层"：

| 分级 | 含义 | 代表 |
|---|---|---|
| **L0** | 一阶改进：改进器固定，改进对象是外部产物 | FunSearch、AlphaEvolve、ADAS |
| **L0.5** | 边界形态：推理时自我修正 / teacher 外置循环 | Self-Refine、LLM2LLM、AFlow |
| **L1** | 自举循环：模型产出变成训练信号反过来改变模型 | STaR、ReST-EM、SPIN |
| **L1- / L1+** | L1 变体：记忆/上下文级持久化（-）；判据参与共进化（+） | Reflexion、Voyager、ACE（-）；Self-Rewarding（+） |
| **L1.5** | 课程自产：连"学什么"都由系统内生 | Absolute Zero、R-Zero、SPICE |
| **L2** | 改进者可被替换/改写，但改进规则固定 | SICA、Self-Harness、AIDE² |
| **L3** | 完全自指：改写逻辑自身也在可改写范围内 | Gödel Agent、HSI、MetaSkill-Evolve、HyperAgents |
| **L4 / L5** | 评估器可改写；权重×脚手架联合递归；理论上限 | RQGM、Co-Harness、Gödel Machine |

完整图例与推荐阅读路径见 **[总索引](docs/index.md)**。

---

## 仓库结构

```
.
├── docs/                      # 站点内容（MkDocs 的文档根目录）
│   ├── index.md               # 总索引：分级图例 + 评估三问 + 推荐阅读路径
│   ├── template.md            # 精读模板 v2.0（逐字收录；参考资料，不上侧边栏）
│   ├── template-v1.md         # 精读模板 v1.0（历史版本，现有 73 篇按此写成）
│   ├── references.md          # 参考文献清单（由脚本从笔记自动抽取生成）
│   ├── 01-主线-01-Gödel Machine理论源头-精读.md
│   └── …                      # 共 73 篇精读，分 8 个分类
├── scripts/                   # 笔记维护脚本
│   ├── gen_nav.py             # 依文件名重生成 mkdocs.yml 的侧边栏导航
│   ├── extract_refs.py        # 抽取论文元数据，生成 docs/references.md
│   └── check_notes.py         # 一致性自检：编码 / 分档模板完整性 / 断链 / 字符规范
├── mkdocs.yml                 # 站点配置（导航区块由 gen_nav.py 自动维护）
├── requirements.txt           # 构建依赖（mkdocs-material、jieba）
├── CHANGELOG.md               # 更新日志与待办
└── LICENSE                    # CC BY 4.0
```

## 本地预览

```bash
pip install -r requirements.txt
mkdocs serve          # 打开 http://127.0.0.1:8000
```

## 部署说明（只需做一次）

首次启用 GitHub Pages 时，必须把 **Settings → Pages → Build and deployment → Source**
设为 **「GitHub Actions」**。

若保留默认的「Deploy from a branch」，GitHub 会用 **Jekyll** 构建分支内容对外发布，
而该构建会在每次 push 时与本站的 Actions 发布**竞争并最终覆盖它**：访客看到的是 README
的 Jekyll 渲染版，`/docs/*.html` 被原样暴露，而侧边栏导航、中文全文检索、深色模式
**全部失效**（`references/`、`search/search_index.json` 均 404）。此时 Actions 工作流
仍显示全绿，故障只体现在这个 Source 设置上。

## 新增一篇精读

文件名必须遵循 `分类号-分类名-序号-标题-精读.md`，例如
`01-主线-25-NewPaper-精读.md`（分类号 `01`–`08`，分类名须与既有分类一致）。
深度自选：写卡片式笔记，只需在开头的模板说明行里写明「（卡片式）」，
`check_notes.py` 便会按卡片式档位（`## 0.`–`## 2.`）而非完整档校验，不会误报缺小节。
之后依次运行：

```bash
python scripts/check_notes.py     # 自检：按深度档位校验必备小节、有无断链
python scripts/gen_nav.py         # 把新笔记挂到侧边栏
python scripts/extract_refs.py    # 刷新参考文献清单
```

推送到 `main` 后，GitHub Actions 会自动构建并发布站点。

## 许可

文字内容采用 **[CC BY 4.0](LICENSE)** 许可协议：欢迎转载、改编、商用，请注明出处。
各篇所引述论文的著作权归原作者与出版方所有。
