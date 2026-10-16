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

## 待办

以下问题由 `scripts/check_notes.py` 自动检出，需人工补齐（脚本不会代为推断内容）。

### 0. 【阻塞】Pages 的 Source 仍是「Deploy from a branch」

线上站点目前是 **GitHub 用 Jekyll 构建分支目录**的产物，不是本仓库 MkDocs 站的产物：
首页是 README 的 Jekyll 渲染版，`/docs/*.html` 与 `/docs/*.md` 可被直接访问，而
`references/`、`search/search_index.json`、`sitemap.xml` 均返回 404 ——
侧边栏导航、中文全文检索、深色模式**全部失效**。

定位依据：内置工作流 `pages build and deployment` 的构建步骤为
`Build with Jekyll` + `Deploy to GitHub Pages`，且它的部署记录（`02:56:42`）
晚于本仓库工作流的部署（`02:56:25`）17 秒，因而覆盖了后者。**两条工作流都是 success**，
故障只出在 Pages 的 Source 设置上。

- [ ] Settings → Pages → Build and deployment → Source 改为 **「GitHub Actions」**
- [ ] 改完后重跑工作流：Actions → 构建并发布文档站 → Run workflow
- [ ] 复核：`https://zlven.github.io/RSI-Papers-Reading/references/` 返回 200

### 1. 缺少 arXiv 编号（5 篇）

脚本不猜测编号，请确认后补入对应笔记头部的元信息块：

- [ ] `01-主线-07-HGM-精读.md` —— 笔记仅写「arXiv 2025」，无编号
- [ ] `01-主线-08-Live-SWE-agent-精读.md` —— 笔记仅写「arXiv 2025」，无编号
- [ ] `05-进化搜索-01-FunSearch-精读.md` —— 笔记仅写「Nature 2024」，未记 arXiv 编号
- [x] `01-主线-14-HALO-精读.md` —— 非 arXiv 文献（Context Labs 开源项目），无需补
- [x] `02-综述-03-Anthropic-When AI Builds Itself-精读.md` —— 非 arXiv 文献（实验室立场报告），无需补

### 2. 缺少模板小节（4 篇）

- [ ] `02-综述-01-Bounded-to-Autonomous-综述-精读.md` 缺 `## 9. 批判性问题清单`
- [ ] `02-综述-02-The Last AI Built by Humans-精读.md` 缺 `## 9. 批判性问题清单`
- [ ] `02-综述-03-Anthropic-When AI Builds Itself-精读.md` 缺 `## 7.` `## 8.` `## 9.`
- [ ] `03-其他路线-02-Transformer²-精读.md` 缺 `## 9. 批判性问题清单`

### 3. 非标准连字符影响检索（458 处 / 18 个文件）

笔记中混入了 `U+2011`（非断连字符）等**与 ASCII 连字符外形相同但码位不同**的字符，
多出现在英文术语与标题中（如 `Self‑Harness`、`Per‑step Reflection`、
`Clade‑Metaproductivity`）。后果是读者用常规键盘输入 `Self-Harness` **搜不到**这些内容。

- [ ] 统一替换为 ASCII 连字符 `-`（`python scripts/check_notes.py --fix-hyphens --apply`）

> 另有 `U+2212` 减号 6 处、`U+2013` 短破折号 30 处，可能是刻意的数学符号或数值区间，
> 脚本只提示不自动替换。中文行文中的破折号 `——`（U+2014）属正常排版，不在检查范围。
