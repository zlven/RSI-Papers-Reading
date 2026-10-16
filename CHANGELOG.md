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

## 待办

上一轮列出的三类问题**已全部清零**。

### 1. 缺少 arXiv 编号（0 篇）✓

- `01-主线-07-HGM-精读.md` —— 已补 `arXiv:2510.21614`
- `01-主线-08-Live-SWE-agent-精读.md` —— 已补 `arXiv:2511.13646`
- `05-进化搜索-01-FunSearch-精读.md` —— 确认为**非 arXiv 文献**，已在 `extract_refs.py` 的
  `OVERRIDES` 中写入 Nature 正刊信息（Nature 625, 468-475），并注明「无 arXiv 预印本」
- HALO、Anthropic 报告 —— 由脚本识别「非 arXiv」声明后不再误报（详见上文）

### 2. 缺少模板小节（0 篇）✓

4 篇已全部补齐 0–9 节，见上文表格。

### 3. 嵌套重复目录待删除

`RSI精读/RSI精读/`（54 个文件）的内容已全部提取进 `docs/` 与根 `README.md`——逐一逐段核对确认
**无任何内容遗漏**（49 篇共有笔记中 40 篇正文完全一致、9 篇为 `docs/` 侧更全；3 篇新笔记已搬入并
规范化头部；上游索引的 L3 代表、19–21 行、推荐阅读路径、L3 三形态对照均已并入 `docs/index.md`）。

该目录**已被提交进仓库**（54 个 tracked 文件），删除需走 `git rm`：

```bash
git rm -r RSI精读
git commit -m "删除嵌套重复目录 RSI精读/RSI精读/"
```

> 待决：上游索引写的「模板文件见 `../RSI论文精读Prompt模板.md`」指向仓库外路径，该文件在
> 上级目录**并不存在**，故 `docs/index.md` 保留原措辞「模板文件未收录进本仓库」。

