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

## 待办

以下问题由 `scripts/check_notes.py` 自动检出，需人工补齐（脚本不会代为推断内容）。

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
