# 更新日志

本文件记录笔记与仓库结构的变更。仓库尚在持续扩充中。

## 2026-10-16 — 建立公开仓库

**仓库结构化**

- 将 49 篇精读与总索引统一迁入 `docs/`，接入 MkDocs Material 文档站
  （中文全文检索、深色模式、按 7 大分类分组的侧边栏导航）。
- 新增 `.github/workflows/deploy.yml`：推送到 `main` 后自动构建并发布到 GitHub Pages。
- 新增 `LICENSE`（CC BY 4.0）、`README.md`、`.gitignore`、`requirements.txt`。
- 原 `README.md`（总索引）转为站点首页 `docs/index.md`。

**新增维护脚本**

- `scripts/gen_nav.py` —— 依文件名自动生成侧边栏导航，避免手工维护 49 条目录项。
- `scripts/extract_refs.py` —— 从各篇的「论文信息」块抽取文献元数据，
  生成 `docs/references.md`；只转录笔记已有内容，不猜测 arXiv 编号。
- `scripts/check_notes.py` —— 一致性自检（文件名编码 / 模板 0–9 节完整性 /
  站内链接 / 非标准连字符）。

---

## 2026-10-16 — 修复线上站点

首次发布后线上站点并非本仓库的 MkDocs 产物，而是 **GitHub 用 Jekyll 构建分支目录**的结果，
表现为：首页是 README 的 Jekyll 渲染版，`/docs/*.html` 与 `/docs/*.md` 可被直接访问，
而 `references/`、`search/search_index.json` 均 404 —— 侧边栏导航、中文全文检索、
深色模式全部失效。

**根因**：Pages 的 Source 仍为「Deploy from a branch」。该模式下 GitHub 每次 push 都会
用内置工作流 `pages build and deployment`（`Build with Jekyll` → `Deploy to GitHub Pages`）
构建分支并与本仓库的 Actions 发布**竞争**，且其部署记录（`02:56:42`）晚于本仓库工作流的
部署（`02:56:25`）17 秒，因而覆盖了后者。**两条工作流都显示 success**，故障只体现在
Pages 的 Source 设置上，站点外观正常但功能全失。

**处置**：将 Source 切换为「GitHub Actions」后重新发布。复核已通过 32 项断言：
51 个页面（49 篇精读 + 首页 + 文献清单）全部返回 200，检索索引 954 条且 jieba 分词生效
（76407 处零宽空格分隔），旧的 `/docs/*.html` 路径均已 404。

> 若不切换 Source，此故障会**静默复现**——工作流始终全绿。排错入口见 README「部署说明」。

## 2026-10-16 — 统一非标准连字符

笔记中混入了 `U+2011`（NON-BREAKING HYPHEN，非断连字符）：它与 ASCII 连字符外形完全相同、
码位却不同，多出现在英文术语与论文标题里（`Self-Harness`、`Co-Evolving`、`End-to-End`
这类词原本用的都是它）。后果是读者用常规键盘输入 `Self-Harness` **搜不到**这些内容。

已用 `python scripts/check_notes.py --fix-hyphens --apply` 统一替换：**18 个文件、458 处**。
逐字节核对确认改动**仅是** `U+2011` → `-`，未触碰任何其他字符；`docs/references.md`
已按修正后的标题重新生成（如 `Self-Improvement`、`Co-Evolving`、`End-to-End`）。

同时修掉了一处会让问题**复发**的源头：`scripts/extract_refs.py` 的 `OVERRIDES` 里硬编码的
Live-SWE-agent 标题本身含 `U+2011`，每次重新生成文献清单都会把它灌回 `references.md`，
即 `--fix-hyphens` 并**不幂等**。现已改为 ASCII 连字符。

> `U+2212` 减号 6 处、`U+2013` 短破折号 30 处可能是刻意的数学符号或数值区间，
> 脚本只提示、不自动替换；中文破折号 `——`（`U+2014`）属正常排版，不在检查范围。
> 该字符的真实样本今后只保留在 `scripts/check_notes.py` 的 `FIXABLE` 表里——探测逻辑本身需要它。

---

## 2026-10-16 — 扩充至 53 篇：主线补入 4 篇新作

**新增精读（4 篇，主线 19–22）**

- `01-主线-19-MetaSkill-Evolve-精读.md`（**L3**）——改进过程参数化为五份 Markdown 元技能，
  被**同一条**五智能体流水线做双时间尺度进化；ALFWorld 全部增益来自慢环。
- `01-主线-20-HyperAgents-精读.md`（**L3**）——任务/元智能体融合为单一可编辑程序（DGM-H），
  元认知自我修改；跨域迁移 imp@50=0.630 vs DGM-custom≈0。
- `01-主线-21-Mendel-Gödel-Machine-精读.md`（**L2.5**）——比较进化：反应规范变异 +
  跨谱系杂交，零额外评测；加性景观收敛定理；Polyglot 50.8→93.2%。
- `01-主线-22-RSI-Anything-精读.md`（**L4-**）——改进单元升格为「策略—世界模型配对」。
  该篇由 `JEPA-Anything与RSI-Anything论文笔记.md` 重写而来，JEPA-Anything 仅作背景。

编号**沿用上游索引**：MetaSkill-Evolve / HyperAgents / Mendel 占 19–21，RSI-Anything 顺延至 22。
系列规模 50 → **53 篇**（主线 19 → 22）。`docs/index.md` 与根 `README.md` 的规模表、分级图例的
L3 代表（补入 MetaSkill-Evolve、HyperAgents）、19–22 行、推荐阅读路径（新增「**L3 内部三形态**」
对照项：Gödel Agent ↔ HyperAgents ↔ MetaSkill-Evolve）均已同步。

**修正元数据错误**

- **HGM 正名**：原笔记题为「层级哥德尔机（Hierarchical Gödel Machine）」，与论文实际名称不符。
  该文实为 **Huxley-Gödel Machine**（arXiv:2510.21614，取名自进化生物学的支系/clade 概念）——
  与笔记正文描述的 CMP / Clade-Metaproductivity 本已一致，只是标题与头部写错了。已改标题、
  元信息块与速览卡片；正文中描述树结构的「层级」一词属正常用法，保留。
- **`docs/references.md` 年份误判（3 条）**：SeRL 显示「预印本 2034」、ShinkaEvolve「1934」、
  EvoGit「2049」。根因是 `extract_refs.py` 的年份正则会在 **arXiv 编号之前**的位置检索，把编号
  自带的 4 位数字串（`2505.20347`→2034、`2509.19349`→1934、`2506.02049`→2049）当成了年份。
  已在检索年份前先摘掉编号（新增 `strip_arxiv()`），从源头杜绝复发；三条均恢复为「预印本 2025」。
- **「非 arXiv 文献」判定统一**：HALO（Context Labs 开源项目）、Anthropic 报告（实验室立场文）、
  FunSearch（仅有 Nature 正刊、未发预印本）长期被两个脚本反复判为「缺 arXiv 号」，导致待办
  永远无法收敛。现 `check_notes.py` 与 `extract_refs.py` 一致识别笔记头部的「非 arXiv / 无 arXiv」
  声明，两边同时归零。
- **3 篇新笔记头部规范化**：原头部只有 `> **阅读方式**：…`，而 `extract_authors()` 只认
  `**论文信息**` / `**项目信息**` / `**文献信息**` 标签，会让 `references.md` 的作者列退化成「—」。
  已统一为仓库既有的格式 A（`> **论文信息**：<作者>（<机构>）；arXiv:…；代码开源 [repo](url)`）。

**补齐模板缺口（4 篇 → 0）**

| 文件 | 处置 |
|---|---|
| `02-综述-01-Bounded-to-Autonomous-综述-精读.md` | 新增 `## 8. 未来方向（综述指出的空白）`，原 `## 8.` 顺延为 `## 9.` |
| `02-综述-02-The Last AI Built by Humans-精读.md` | 新增 `## 8. 未来方向（路线图所指向的缺口）`，原 `## 8.` 顺延为 `## 9.` |
| `02-综述-03-Anthropic-When AI Builds Itself-精读.md` | 原 `## 4. 评估三问视角` 拆为 `## 4. 材料来源与核对方式` + `## 5. 评估三问视角`，其后整体顺延，补齐 `## 7.`/`## 8.`/`## 9.` |
| `03-其他路线-02-Transformer²-精读.md` | 新增 `## 6. 实验结果与分析`，原 `## 6.`–`## 8.` 顺延为 `## 7.`–`## 9.` |

新增小节的内容均取自各篇笔记**自身已有**的条目与讨论，未引入笔记之外的数字或论断。

**本轮脚本链复核**

```
python scripts/check_notes.py    → 53 篇：NFC ✓ / 模板 0–9 ✓ / 站内链接 ✓
                                   缺 arXiv 号 0 篇 / 非标准连字符 0 处
python scripts/gen_nav.py        → 7 个分组、53 条导航
python scripts/extract_refs.py   → 53 篇文献、0 篇待补
```

---

## 2026-10-16 — 新增 20 篇：开辟「08 · 评测基准」分类

**新增精读（20 篇）**

- **01 · 主线**：`23-SIFT`（L2，简读）、`24-GEA`（L2.5，简读）——2026 年的「评测经济学」线与
  「群体进化」线：SIFT 用 Bradley-Terry LLM 裁判预筛候选、只为少数候选付全量评测费
  （Polyglot 35.1% vs DGM 30.7%，成本约 1/10）；GEA 以「组」而非「树」为进化单元 + 经验共享
  （SWE-bench Verified 71.0% vs DGM 56.7%）。
- **02 · 综述与立场**：`04-D2I分级综述`（卡片式）、`05-Self-Evolving-Agents综述`（卡片式）。
- **07 · 自动化科研**：`04-AIDE`（L2，简读）——AIDE² 的内层基座、「脚手架贡献可翻三倍」的证据源头。
- **08 · 评测基准（全新分类，15 篇）**：01 RSIBench-Data、02 SEABench、03 PaperBench、
  04 PostTrainBench、05 MLE-bench、06 RE-Bench 与 HCAST、07 MLS-Bench、08 TamperBench、
  09 PATH-Bench、10 LifelongAgentBench、11 RSI-Bench、12 MLAgentBench、13 AutoLab、
  14 SAEScientist-Bench、15 SAHOO。该簇统一回答「**怎样才算真的在改进**」，按测量对象分四类：
  对象层代理基准（05/07/03/06/13/12/14）、回路层审计（01/04）、安全压测（02/08/15）、
  过程与终身层（09/10/11）。

系列规模 53 → **73 篇**（主线 22→24、综述 3→5、自动化科研 3→4、评测基准 0→15）。

**新增分类 08 · 评测基准**

`gen_nav.py` 的 `CATEGORY_TITLES` / `NUM_TO_CAT` 与 `extract_refs.py` 的 `CATEGORY_TITLES`
各补一条。文件名分类号 `08`、分类名 `评测基准` 即被自动收纳，侧边栏成为 8 个分组、73 条导航。

**深度分档成为正式规则**

20 篇新笔记的节数**随阅读深度伸缩**（完整 10 节 / 简读 5–8 节 / 卡片式 2–3 节），
原先「必备 `## 0.`–`## 9.`」的校验会把有意的分档误报成「缺小节」。现改为一等规则：

- `check_notes.py` 以 `note_tier()` 判定档位——笔记开头写明「（卡片式）」即自声明，
  否则按节数（10 节＝完整精读、≥5 节＝简读、更少＝卡片式）——再按 `REQUIRED_BY_TIER`
  校验各自必备小节：完整精读 `## 0.`–`## 9.`、简读至少 `## 0.`–`## 4.`、卡片式至少 `## 0.`–`## 2.`。
- `docs/index.md` 与根 `README.md` **每行/每档均标注档位**并说明校验差异，站点立即可构建，
  分档意图被保留且可见。

**补齐 12 篇缺失的 arXiv 编号（12 → 0）**

编号**逐篇直接打开 arXiv 摘要页确认**，非转述搜索结果，亦未作任何推断。笔记头部只写入已核实的编号：

| 文件 | 补入内容 |
|---|---|
| `01-主线-23-SIFT-精读.md` | arXiv:2609.19526（*Self Improvement via Fast Tree-search*，MIT / Sakana AI） |
| `01-主线-24-GEA-精读.md` | arXiv:2602.04837（*Group-Evolving Agents*，ICLR 2026） |
| `02-综述-04-D2I分级综述-精读.md` | **非 arXiv**——Preprints.org 预印本，DOI `10.20944/preprints202608.0051.v1` |
| `08-评测基准-04-PostTrainBench-精读.md` | arXiv:2603.08640（ICML 2026） |
| `08-评测基准-05-MLE-bench-精读.md` | arXiv:2410.07095（ICLR 2025） |
| `08-评测基准-07-MLS-Bench-精读.md` | arXiv:2605.08678（ICML 2026） |
| `08-评测基准-08-TamperBench-精读.md` | arXiv:2602.06911（KDD 2026） |
| `08-评测基准-11-RSI-Bench-精读.md` | **非 arXiv**——GitHub `sunghunkwag/rsi-bench`（MIT）软件项目，无配套论文 |
| `08-评测基准-12-MLAgentBench-精读.md` | arXiv:2310.03302 |
| `08-评测基准-13-AutoLab-精读.md` | arXiv:2606.05080 |
| `08-评测基准-14-SAEScientist-Bench-精读.md` | arXiv:2609.09113 |
| `08-评测基准-15-SAHOO-精读.md` | arXiv:2603.06333（ICLR 2026 Workshop on **AI with** RSI） |

新增的两条「非 arXiv」声明同样被两个脚本识别，`extract_refs.py` 的输出因此收敛到
**73 篇文献、0 篇待补**。空白的 `作者` 字段一并按论文页补入（SIFT / GEA / D2I / TamperBench /
RSI-Bench / MLAgentBench / AutoLab / SAEScientist-Bench / SAHOO），使 `references.md` 的作者列不再退化为「—」。

**顺带修掉一个会持续复发的显示错误**：`extract_refs.py` 的「链接」列对无 arXiv 的条目一律输出
「**待补**」，与「已声明非 arXiv」的语义直接矛盾——D2I 与 RSI-Bench 一入册就带上了这个假待办。
现改为：有 `OVERRIDES` 时用真实载体，否则输出「—（非 arXiv 文献）」，只有**真正缺编号**的条目
才显示「待补」。两条同时补上可核实的载体链接（D2I 指向其配套仓库、RSI-Bench 指向 GitHub 仓库）。

**本轮修订的元数据错误**

- **GEA 正名**：原笔记展开名写作「Generative Evolutionary Agent」，检索**无任何出处**；
  该文实为 ***Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing***
  （arXiv:2602.04837）。笔记正文的数字（SWE-bench Verified 71.0%、Polyglot 88.3%）与论文完全吻合，
  故仅订正名称与头部，正文保留。
- **SAHOO 的 workshop 全名**：由「Workshop on Recursive Self-Improvement」更正为
  「Workshop on **AI with** Recursive Self-Improvement」（arXiv:2603.06333 与 OpenReview 页一致）。

**仍需人工确认（本轮未擅自改动，仅在此记录）**

- **MLAgentBench 的会议归属**：arXiv:2310.03302 摘要页**无 Comments 字段**，无法证实笔记所记的
  「NeurIPS 2023 Datasets & Benchmarks」；检索结果则指向 ICML 2024。已在笔记中把该说法标注为
  「笔记记为…」并附上 arXiv 号，等确认后再定。
- **MLS-Bench 的标题**：笔记写 *A Holistic and Rigorous Assessment of ML Research Agents*，
  官方标题为 *A Holistic and Rigorous Assessment of **AI Systems on Building Better AI***（arXiv:2605.08678）。
- **TamperBench 的主题框架**：论文实际是**开放权重 LLM 的抗篡改基准**（jailbreak-tuning、LoRA、
  后门、表示空间攻击），笔记以「RSI 系统自我更新的安全底线」框定——作为本系列的解读角度成立，
  但不宜被当作论文自陈的定位。
- **`02-综述-02` 与 `02-综述-04` 的 L1–L5 分级同源**：两者共用同一套 L1–L5 坐标，检索提示可能
  出自同组作者。本轮按既有结构保留为两篇，未作合并。

**本轮脚本链复核**

```
python scripts/check_notes.py    → 73 篇：NFC ✓ / 站内链接 ✓ / 缺 arXiv 号 0 篇 / 非标准连字符 0 处
                                   深度分档：完整精读 58 篇 ｜ 简读 6 篇 ｜ 卡片式 9 篇，全部达标
python scripts/gen_nav.py        → 8 个分组、73 条导航（01 主线 24 / 02 综述 5 / 03 8 /
                                   04 7 / 05 6 / 06 4 / 07 4 / 08 评测基准 15）
python scripts/extract_refs.py   → 73 篇文献、0 篇待补
```

---

## 2026-10-16 — 收录精读模板 v1.0 / v2.0，独立成页

此前 `docs/index.md` 只写「模板文件未收录进本仓库」——原 `RSI论文精读Prompt模板.md` 在仓库内外
均不存在（git 历史中也从未有过），读者无从得知各篇的结构从何而来。现将模板原文逐字收录为站点页面。

**新增两个页面**

- `docs/template.md` —— **精读模板 v2.0**（现行版本），逐字收录。
- `docs/template-v1.md` —— **精读模板 v1.0**（历史版本），逐字收录，存为档案。

两版并存的理由：`docs/` 下现有 73 篇笔记**全部按 v1.0 写成**，v2.0 新增的 Tags、金句记忆点、
评分卡、漏斗六步、关键设计三段式、消融 Δ 列、`vs 对比` 等槽位在旧笔记里一概没有，节标题也有出入
（`0. 论文元信息` vs `0. 元信息与速览`、`4. 实验设计` vs `4. 实验`、`7. 未来方向与缺点` vs
`7. 缺点与攻击面`）。读旧笔记须以 v1.0 为准，故不能只留新版。两版差异已在 v2.0 页末列成逐节对照表
（8 行：§0 / §1 / §3.1–3.2 / §3.3–3.4 / §4 / §7 / §8 / 阅读规则），并反过来列出三处
**笔记先于模板**的约定（速览卡片写法、RSI 分级中间档、深度三档）。

**页面处理**

- 模板正文逐字照录，仅改**一处**：源文件 §3.2 三段式里的 `&gt;` 还原为 `>`——`&gt;` 是粘贴时被
  HTML 转义的产物，按原样渲染会丢掉引用块。文末另加「备注」一节，明确标注**不属于模板正文**。
- 中文标题生成不出锚点（Python-Markdown 默认 slugify 丢弃非 ASCII），三处跨页锚点改用
  `attr_list` 显式指定：`### 语料与模板的版本落差 {: #version-gap }`、
  `## RSI 分级图例（本系列约定） {: #rsi-grades }`。

**不占导航位**

模板属参考资料而非精读，**不进侧边栏**，只从首页正文那一行「统一模板」链入；
`docs/index.md` 顶部原本两段（统一模板 + 版本提示）也压回一行指针，细节都留在模板页上。

需要说明的是，本想「折成一个可折叠分组塞到导航底部」，但 `mkdocs.yml` 开着
`navigation.sections`（顶级分组常驻展开），顶部一级分组根本折叠不起来，两行会一直露着——
所以摘出导航才是真的角落。

- `gen_nav.py`：新增 `OFF_NAV_PAGES = {"template.md", "template-v1.md"}`——既不进 `render()`
  的侧边栏，也避开 `collect()` 里「文件名不符合约定」的误报；`FRONT_PAGES` 复归
  总索引 / 参考文献清单两项。
- `mkdocs.yml`：新增 `validation.nav.omitted_files: ignore`。文件存在却不出现在 `nav` 中，
  MkDocs 默认告警、`--strict` 下直接构建失败，故显式降级为忽略。
- `check_notes.py`：`NOT_A_NOTE` 增加 `template-v1.md`（模板页不套精读模板校验）。
- `extract_refs.py` 无需改动——它按 `FILENAME_RE` 过滤，模板页天然不匹配。

模板页仍在构建产物里（`/template/`、`/template-v1/` 均 200）并进入中文检索索引，只是不上侧边栏。

**本轮脚本链复核**

```
python scripts/check_notes.py    → 77 个文件（73 篇精读）：NFC ✓ / 站内链接 ✓ /
                                   缺 arXiv 号 0 篇 / 非标准连字符 0 处
python scripts/gen_nav.py        → 8 个分组、73 条导航 + 4 个独立页面
python scripts/extract_refs.py   → 73 篇文献、0 篇待补
python -m mkdocs build --strict  → 通过（首次构建报出 3 处中文锚点失效，已修）
```

---

## 待办

### 1. 缺少 arXiv 编号（0 篇）✓

- `01-主线-07-HGM-精读.md` —— 已补 `arXiv:2510.21614`
- `01-主线-08-Live-SWE-agent-精读.md` —— 已补 `arXiv:2511.13646`
- `05-进化搜索-01-FunSearch-精读.md` —— 确认为**非 arXiv 文献**，已在 `extract_refs.py` 的
  `OVERRIDES` 中写入 Nature 正刊信息（Nature 625, 468-475），并注明「无 arXiv 预印本」
- HALO、Anthropic 报告 —— 由脚本识别「非 arXiv」声明后不再误报（详见上文）

### 2. 缺少模板小节（0 篇）✓

4 篇已全部补齐 0–9 节，见上文表格。

### 3. 嵌套重复目录（已删除）✓

`RSI精读/RSI精读/`（54 个 tracked 文件）先经逐一核对确认**无任何内容遗漏**（49 篇共有笔记中
40 篇正文完全一致、9 篇为 `docs/` 侧更全；3 篇新笔记已搬入并规范化头部；上游索引的 L3 代表、
19–21 行、推荐阅读路径、L3 三形态对照均已并入 `docs/index.md`），再以 `git rm -r RSI精读` 删除，
提交 `b5beb40`（54 files changed、7237 deletions(-)，**无任何非删除改动**）。

### 4. 待人工确认的文献信息（4 条）

见上一节「仍需人工确认」：MLAgentBench 的会议归属、MLS-Bench 的标题、TamperBench 的主题框架、
`02-综述-02` 与 `02-综述-04` 的分级同源。四项均已在笔记或本日志中留有出处与存疑标注，
不影响站点构建，确认后可各自单独修订。

### 5. 模板文件（已收录）✓

上游索引写的「模板文件见 `../RSI论文精读Prompt模板.md`」指向仓库外路径，该文件在上级目录
**并不存在**，git 历史中也从未提交过，故 `docs/index.md` 一度保留原措辞「模板文件未收录进本仓库」。
现已由作者提供 v1.0 / v2.0 原文，逐字收录为 `docs/template.md` 与 `docs/template-v1.md`，
`index.md` 的说明已同步改写。

