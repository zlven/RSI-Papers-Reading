#!/usr/bin/env python3
"""从各篇精读的「论文信息」块抽取文献元数据，生成 docs/references.md。

笔记头部的元信息有四种历史格式，本脚本逐种兼容：

  A. `> **论文信息**：<作者>；arXiv:XXXX.XXXXX（日期）`      ← 01 主线 / 03 部分
  B. `> 论文：<作者>. "<标题>". <会议>（arXiv:XXXX.XXXXX）。` ← 03–07 多数
  C. `## 0. 论文元信息` + `- **标题**：/ - **作者**：/ - **发表**：`
  D. `> **项目信息**` / `> **文献信息**`（非 arXiv 文献）

H1 兜底取标题时，两个簇的破折号语义相反，必须区别对待：

  `精读：STaR —— <英文全称>`           → 取破折号「后」（英文全称）
  `AHE 精读：<英文全称>——<中文副标题>`  → 取破折号「前」（砍掉中文副标题）

**核心原则：脚本只转录笔记里已写明的内容，绝不猜测或生成 arXiv 号。**
笔记未写明 arXiv 号的条目会标注「待补」，交由人工确认（部分文献本就不是
arXiv 论文，例如 HALO 是开源项目、Anthropic 报告是实验室立场文）。

用法：

    python scripts/extract_refs.py            # 生成 docs/references.md
    python scripts/extract_refs.py --dry-run  # 只打印结果，不写文件
"""

from __future__ import annotations

import re
import sys
import pathlib

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "references.md"

FILENAME_RE = re.compile(r"^(\d{2})-([^-]+)-(\d{2})-(.+)\.md$")
HEAD_LINES = 25  # 元信息只可能出现在开头这么多行内

ARXIV_NEW = re.compile(r"arXiv[:\s]*(\d{4}\.\d{4,5})")
ARXIV_OLD = re.compile(r"arXiv[:\s]*([a-z-]+(?:\.[A-Z]{2})?/\d{7})")

VENUES = (
    "NeurIPS", "ICML", "ICLR", "COLM", "ACL", "EMNLP", "NAACL", "CVPR",
    "ICCV", "ECCV", "AAAI", "IJCAI", "TMLR", "JMLR", "Nature", "Science",
    "Springer",
)
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
# arXiv 编号自带 4 位数字串（2505.20347 → "2034"、2509.19349 → "1934"、
# 2506.02049 → "2049"），会被 YEAR_RE 误当成年份。检索年份前必须先摘掉编号，
# 否则「预印本 2034」这类错误年份会随每次重新生成复发。
ARXIV_ANY = re.compile(
    r"arXiv[:\s]*\d{4}\.\d{4,5}|arXiv[:\s]*[a-z-]+(?:\.[A-Z]{2})?/\d{7}"
)
# 笔记里已显式声明"非 arXiv 文献"的条目不计入缺编号清单
# （HALO 是开源项目、Anthropic 是立场报告、FunSearch 只有 Nature 版无预印本）。
NON_ARXIV_RE = re.compile(r"非\s*arXiv|无\s*arXiv")


def strip_arxiv(text: str) -> str:
    """摘掉 arXiv 编号，避免编号内的数字串被年份正则误匹配。"""
    return ARXIV_ANY.sub(" ", text)

CATEGORY_TITLES = {
    "01": "01 · 主线：哥德尔式 RSI 与自我改进智能体",
    "02": "02 · 综述与立场",
    "03": "03 · 其他路线：权重自编辑与经典自举",
    "04": "04 · 零数据自博弈",
    "05": "05 · 进化搜索",
    "06": "06 · 经验与上下文",
    "07": "07 · 自动化科研",
    "08": "08 · 评测基准",
}

# 少数条目的自动抽取不理想，手工指定。
# 以下内容均逐字照抄自对应笔记的 H1 或元信息块，未作任何推断。
OVERRIDES: dict[str, dict[str, str]] = {
    "01-主线-01-Gödel Machine理论源头-精读.md": {
        "title": "Gödel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements",
        "authors": "Jürgen Schmidhuber（IDSIA & TU München）",
        "venue": "IDSIA 技术报告 2003 / Springer《Artificial General Intelligence》2007",
    },
    # 以下几篇 H1 的「精读：」之后是中文副标题而非英文全称，改用笔记自带的简称
    "01-主线-08-Live-SWE-agent-精读.md": {"title": "Live-SWE-agent"},
    "01-主线-16-DemoEvolve-精读.md": {"title": "DemoEvolve"},
    "01-主线-17-Red Queen Gödel Machine-精读.md": {
        "title": "Red Queen Gödel Machine（智能体与其评估器的共同进化）"
    },
    "01-主线-14-HALO-精读.md": {
        "venue": "开源项目（非 arXiv 论文）",
        "link": "[context-labs/halo](https://github.com/context-labs/halo)",
    },
    "02-综述-03-Anthropic-When AI Builds Itself-精读.md": {
        "venue": "Anthropic Institute 立场报告",
        "link": "—（非 arXiv 文献）",
    },
    # FunSearch 只有 Nature 正刊版本，未发 arXiv 预印本
    "05-进化搜索-01-FunSearch-精读.md": {
        "venue": "Nature 625, 468-475（2024）",
        "link": "[Nature](https://www.nature.com/articles/s41586-023-06924-6)",
    },
}


def clip(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def extract_arxiv(head: str) -> str | None:
    """返回 arXiv ID；旧式（cs/0309048）优先，避免被新式正则误伤。"""
    m = ARXIV_OLD.search(head) or ARXIV_NEW.search(head)
    return m.group(1) if m else None


def title_from_h1(h1: str) -> str:
    t = re.sub(r"^#\s*", "", h1).strip()
    if t.startswith("精读"):
        # 03–07 簇： 精读：<简称> —— <英文全称>   破折号后才是全称
        t = re.sub(r"^精读\s*[：:]\s*", "", t)
        if re.search(r"[—–]{1,2}", t):
            t = re.split(r"\s*[—–]{1,2}\s*", t)[-1]
    else:
        # 01/02 簇： <简称> 精读：<全称>——<中文副标题>   破折号后是要丢弃的副标题
        if "精读" in t:
            t = re.split(r"精读\s*[①-⑳]?\s*[：:]?", t, maxsplit=1)[-1]
        if re.search(r"[—–]{1,2}", t):
            t = re.split(r"\s*[—–]{1,2}\s*", t)[0]
    # 去掉 "综述精读①：" 之类残留前缀与 "精读报告" 后缀
    t = re.sub(r"^(综述)?精读\s*[①-⑳]?\s*[：:]\s*", "", t)
    t = re.sub(r"^[①-⑳]\s*[：:]\s*", "", t)  # 精读二字已被切走时残留的序号
    t = re.sub(r"\s*精读报告\s*$", "", t)
    return t.strip()


def extract_title(lines: list[str], h1: str) -> str:
    head_lines = lines[:HEAD_LINES]
    for line in head_lines:
        m = re.match(r"\s*-\s*\*\*标题\*\*\s*[：:]\s*(.+)", line)
        if m:
            return m.group(1).strip()
    for line in head_lines:
        if line.lstrip().startswith(">") and "论文" in line:
            m = re.search(r'[“"]([^”"]{6,240})[”"]', line)
            if m:
                return m.group(1).strip()
    return title_from_h1(h1)


def extract_authors(lines: list[str], head: str) -> str:
    head_lines = lines[:HEAD_LINES]
    for line in head_lines:
        m = re.match(r"\s*-\s*\*\*作者\*\*\s*[：:]\s*(.+)", line)
        if m:
            return m.group(1).strip()
    for line in head_lines:
        s = line.lstrip().lstrip("> ").strip()
        # 格式 A / D：论文信息 / 项目信息 / 文献信息
        m = re.match(r"\*\*(?:论文信息|项目信息|文献信息)\*\*\s*[：:]\s*(.+)", s)
        if m:
            return re.split(r"[；;（(]", m.group(1))[0].strip()
        # 格式 B：`作者. "标题". 会议（arXiv:…）`
        m = re.match(r"论文\s*[：:]\s*(.+)", s)
        if m:
            return re.split(r'[.。]\s*[“"]', m.group(1))[0].strip()
    return "—"


def extract_venue(lines: list[str], head: str) -> str:
    # 格式 C 有显式「发表」字段，直接采用，比任何启发式都准
    for line in lines[:HEAD_LINES]:
        m = re.match(r"\s*-\s*\*\*发表\*\*\s*[：:]\s*(.+)", line)
        if m:
            return m.group(1).strip()

    # 年份只在"摘掉 arXiv 编号后"的文本上检索，否则会把编号里的数字串当成年份
    clean = strip_arxiv(head)
    for venue in dict.fromkeys(VENUES):
        idx = clean.find(venue)
        if idx < 0:
            continue
        # 取该会议名之后最近的年份，避免误取到更早出现的其他年份
        m = YEAR_RE.search(clean, idx, idx + 40)
        if not m:
            m = YEAR_RE.search(clean)
        return f"{venue} {m.group(0)}".strip() if m else venue

    m = YEAR_RE.search(clean)
    if m:
        return f"预印本 {m.group(0)}"
    return "见笔记元信息"


def extract(path: pathlib.Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").split("\n")
    head = "\n".join(lines[:HEAD_LINES])
    h1 = next((l for l in lines if l.startswith("# ")), "")
    arxiv = extract_arxiv(head)
    info = {
        "title": extract_title(lines, h1),
        "authors": extract_authors(lines, head),
        "venue": extract_venue(lines, head),
        "arxiv": arxiv or "",
        "non_arxiv": bool(NON_ARXIV_RE.search(head)),
        "link": f"[arXiv:{arxiv}](https://arxiv.org/abs/{arxiv})" if arxiv else "**待补**",
    }
    info.update(OVERRIDES.get(path.name, {}))
    return info


def main() -> int:
    dry = "--dry-run" in sys.argv
    groups: dict[str, list[tuple[int, str, dict[str, str]]]] = {}
    missing: list[str] = []

    for path in sorted(DOCS.glob("*.md")):
        m = FILENAME_RE.match(path.name)
        if not m:
            continue
        info = extract(path)
        groups.setdefault(m.group(1), []).append((int(m.group(3)), path.name, info))
        if not info["arxiv"] and not info["non_arxiv"]:
            missing.append(path.name)

    for items in groups.values():
        items.sort()

    total = sum(len(v) for v in groups.values())
    lines = [
        "# 参考文献清单",
        "",
        "> 本清单由仓库根目录的 `scripts/extract_refs.py` 从各篇精读头部的「论文信息」块"
        "自动抽取生成，运行该脚本即可刷新。",
        "> 脚本只转录笔记中已写明的内容，**不猜测 arXiv 编号**；"
        "标注「待补」的条目表示原笔记未写明编号（笔记头部已声明「非 arXiv 文献」"
        "的条目不在此列，如 HALO 是开源项目、Anthropic 是立场报告、FunSearch 只有 Nature 版）。",
        "",
        f"共 {total} 篇文献。",
        "",
        "| 分类 | 篇数 |",
        "|---|---|",
    ]
    for cat in sorted(groups):
        lines.append(f"| {CATEGORY_TITLES.get(cat, cat)} | {len(groups[cat])} |")
    lines.append("")

    for cat in sorted(groups):
        lines.append(f"## {CATEGORY_TITLES.get(cat, cat)}")
        lines.append("")
        lines.append("| # | 论文 | 作者 / 团队 | 发表 | 链接 | 精读 |")
        lines.append("|---|---|---|---|---|---|")
        for order, name, info in groups[cat]:
            note_link = name.replace(" ", "%20")
            lines.append(
                f"| {order:02d} | {clip(info['title'], 300)} "
                f"| {clip(info['authors'], 88)} | {clip(info['venue'], 56)} "
                f"| {info['link']} | [笔记]({note_link}) |"
            )
        lines.append("")

    if missing:
        lines += [
            "## 待补 arXiv 编号",
            "",
            "以下条目的原笔记头部未写明 arXiv 编号。脚本不作推断，"
            "确认后请补入对应笔记的元信息块：",
            "",
        ]
        lines += [f"- `{n}`" for n in missing]
        lines.append("")

    output = "\n".join(lines)
    if dry:
        print(output)
    else:
        OUT.write_text(output, encoding="utf-8")
        print(f"已写入 {OUT.relative_to(ROOT)}：{total} 篇文献，{len(missing)} 篇待补 arXiv 号")
        for n in missing:
            print("  [待补] " + n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
