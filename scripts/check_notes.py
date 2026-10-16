#!/usr/bin/env python3
"""精读笔记一致性自检与字符规范化。

检查五件事：

1. **文件名归一化**——必须是 NFC。中文 macOS 上常出现 NFD 分解形式，
   会造成 MkDocs 路由与 Markdown 链接静默失配。
2. **模板完整性**——按笔记的**深度档位**校验必备小节（模板 v1.0）。论文按阅读
   深度分三档：完整精读须含 `## 0.`–`## 9.`；简读至少 `## 0.`–`## 4.`；
   卡片式至少 `## 0.`–`## 2.`。档位由笔记开头的「（卡片式）」自声明与节数共同
   判定，以免把有意的分档误报成「缺小节」。
3. **站内链接可解析**——相对 Markdown 链接必须指向 docs/ 下真实存在的文件。
4. **arXiv 号缺失**——头部未写明编号的篇目，供人工补充；脚本不猜。
   笔记头部已声明「非 arXiv 文献」的条目不列入（如 HALO 是开源项目、
   Anthropic 是立场报告、FunSearch 只有 Nature 版无预印本）。
5. **非标准连字符**——`U+2011`、`U+2010` 等外形与 ASCII `-` 相同但码位不同的字符，
   会导致读者用常规键盘搜不到内容（如输入 `Self-Harness` 搜不到 `Self‑Harness`）。

退出码只反映**会破坏站点的结构性错误**（第 1、3 项）；第 2、4、5 项属内容待办，
只报告不报错，以免 CI 常红。中文破折号 `U+2014`（——）是正常排版，不在检查范围。

用法：

    python scripts/check_notes.py                 # 全面检查
    python scripts/check_notes.py --quiet         # 只输出问题计数（CI 用）
    python scripts/check_notes.py --fix-hyphens   # 预览连字符替换，不写入
    python scripts/check_notes.py --fix-hyphens --apply   # 实际执行替换
"""

from __future__ import annotations

import re
import sys
import pathlib
import unicodedata
import collections
from urllib.parse import unquote

# Windows 控制台默认 GBK，直接 print 中文/符号会 UnicodeEncodeError
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

SECTION_RE = re.compile(r"^##\s+(\d)\.\s", re.MULTILINE)
ARXIV_NEW = re.compile(r"arXiv[:\s]*(\d{4}\.\d{4,5})")           # 2402.04319
ARXIV_OLD = re.compile(r"arXiv[:\s]*([a-z-]+(?:\.[A-Z]{2})?/\d{7})")  # cs/0309048
# 头部声明「非 arXiv 文献」的条目不缺编号，与 extract_refs.py 的判定保持一致
NON_ARXIV_RE = re.compile(r"非\s*arXiv|无\s*arXiv")
MD_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)#\s]+)(?:#[^)]*)?\)")

# 深度分档：档位不同，必备小节不同。三档由「自声明 + 节数」判定，见 note_tier()。
FULL_SECTIONS = set(range(10))     # 完整精读：## 0. – ## 9.
BRIEF_SECTIONS = {0, 1, 2, 3, 4}   # 简读：至少 ## 0. – ## 4.
CARD_SECTIONS = {0, 1, 2}          # 卡片式：至少 ## 0. – ## 2.
REQUIRED_BY_TIER = {
    "完整精读": FULL_SECTIONS,
    "简读": BRIEF_SECTIONS,
    "卡片式": CARD_SECTIONS,
}
# 「（卡片式）」写在笔记开头的模板说明行里，是作者显式的档位声明
CARD_RE = re.compile(r"卡片式")

# 首页、文献清单与模板页本身都不是精读笔记，不套精读模板
NOT_A_NOTE = {"index.md", "references.md", "template.md", "template-v1.md"}

# 可安全替换为 ASCII 连字符的字符（外形与 '-' 相同，语义就是连字符）
FIXABLE = {
    "‐": "U+2010 HYPHEN 连字符",
    "‑": "U+2011 NON-BREAKING HYPHEN 非断连字符",
    "­": "U+00AD SOFT HYPHEN 软连字符",
    "－": "U+FF0D FULLWIDTH HYPHEN-MINUS 全角连字符",
}
# 只报告、不自动替换：可能是刻意的数学符号或数值区间
REPORT_ONLY = {
    "−": "U+2212 MINUS SIGN 减号",
    "–": "U+2013 EN DASH 短破折号",
}
# U+2014 EM DASH（——）是中文正常排版，故意不检查


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def check_encoding(files: list[pathlib.Path]) -> list[str]:
    problems = []
    for path in files:
        if unicodedata.normalize("NFC", path.name) != path.name:
            problems.append(f"[编码] {path.name} 不是 NFC 形式（macOS 上易致链接失效）")
    return problems


def note_tier(text: str, found: set[int]) -> str:
    """判定笔记的深度档位。

    自声明优先（开头几行的「（卡片式）」）；否则按已写出的节数：满 10 节为完整
    精读，≥5 节为简读，再少归卡片式。返回 REQUIRED_BY_TIER 的键之一。
    """
    if CARD_RE.search("\n".join(text.split("\n")[:6])):
        return "卡片式"
    if FULL_SECTIONS <= found:
        return "完整精读"
    return "简读" if len(found) >= 5 else "卡片式"


def check_sections(files: list[pathlib.Path]) -> tuple[list[str], list[str], collections.Counter]:
    problems, no_arxiv = [], []
    tiers: collections.Counter = collections.Counter()
    for path in files:
        if path.name in NOT_A_NOTE:
            continue
        text = path.read_text(encoding="utf-8")
        found = {int(n) for n in SECTION_RE.findall(text)}
        # 注意 int(n) 需与档位集合同型才能求差集
        tier = note_tier(text, found)
        tiers[tier] += 1
        missing = sorted(REQUIRED_BY_TIER[tier] - found)
        if missing:
            problems.append(
                f"[模板] {rel(path)}（{tier}）缺少小节："
                f"{', '.join('## ' + str(n) + '.' for n in missing)}"
            )
        head = "\n".join(text.split("\n")[:25])
        if not (ARXIV_NEW.search(head) or ARXIV_OLD.search(head)) and not NON_ARXIV_RE.search(head):
            no_arxiv.append(rel(path))
    return problems, no_arxiv, tiers


def check_links(files: list[pathlib.Path]) -> list[str]:
    problems = []
    known = {p.name for p in DOCS.glob("*.md")}
    for path in files:
        text = path.read_text(encoding="utf-8")
        for _label, target in MD_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "<")):
                continue
            if target.startswith("../"):
                problems.append(
                    f"[外链] {rel(path)} 引用了 docs/ 之外的路径：{target}（MkDocs 无法解析）"
                )
                continue
            # 只校验同目录下的 .md 目标；%20 / %C3%B6 需先解码再比对
            if not target.endswith(".md"):
                continue
            base = unquote(target).split("/")[-1]
            if base not in known:
                problems.append(f"[断链] {rel(path)} -> {target}（docs/ 下无此文件）")
    return problems


def scan_chars(files: list[pathlib.Path]) -> tuple[collections.Counter, dict[str, set[str]]]:
    """统计可疑字符出现次数与涉及文件。"""
    counts: collections.Counter = collections.Counter()
    where: dict[str, set[str]] = collections.defaultdict(set)
    for path in files:
        text = path.read_text(encoding="utf-8")
        for ch in list(FIXABLE) + list(REPORT_ONLY):
            c = text.count(ch)
            if c:
                counts[ch] += c
                where[ch].add(path.name)
    return counts, where


def apply_hyphen_fix(files: list[pathlib.Path], counts: collections.Counter) -> int:
    changed_files = 0
    total = 0
    for path in files:
        text = original = path.read_text(encoding="utf-8")
        for ch in FIXABLE:
            if ch in text:
                text = text.replace(ch, "-")
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1
            total += sum(original.count(ch) for ch in FIXABLE)
    return changed_files, total


def main() -> int:
    argv = sys.argv[1:]
    quiet = "--quiet" in argv
    fix_mode = "--fix-hyphens" in argv
    apply_fix = "--apply" in argv

    files = sorted(DOCS.glob("*.md"))
    notes = [f for f in files if f.name not in NOT_A_NOTE]
    counts, where = scan_chars(files)

    if fix_mode:
        fixable_total = sum(counts[ch] for ch in FIXABLE)
        print(f"可替换字符合计：{fixable_total} 处，涉及 "
              f"{len(set().union(*[where[ch] for ch in FIXABLE if counts[ch]])) if fixable_total else 0} 个文件")
        for ch in FIXABLE:
            if counts[ch]:
                print(f"  {FIXABLE[ch]:46} {counts[ch]:>5} 处 / {len(where[ch])} 文件 → 替换为 '-'")
        for ch in REPORT_ONLY:
            if counts[ch]:
                print(f"  （跳过，仅提示）{REPORT_ONLY[ch]:34} {counts[ch]:>5} 处 / {len(where[ch])} 文件")
        if not apply_fix:
            print("\n以上为预览。确认无误后加 --apply 实际写入：")
            print("    python scripts/check_notes.py --fix-hyphens --apply")
            return 0
        n_files, n_chars = apply_hyphen_fix(files, counts)
        print(f"\n已写入：{n_files} 个文件，共替换 {n_chars} 处")
        return 0

    enc = check_encoding(files)
    tmpl, no_arxiv, tiers = check_sections(files)
    links = check_links(files)

    if not quiet:
        print(f"扫描 {rel(DOCS)}：{len(files)} 个文件（{len(notes)} 篇精读）\n")

        print(f"1. 文件名编码：{'全部 NFC ✓' if not enc else str(len(enc)) + ' 个问题'}")
        for p in enc:
            print("   " + p)

        print(f"\n2. 模板完整性（按深度档位）：{'全部达标 ✓' if not tmpl else str(len(tmpl)) + ' 个问题'}")
        for tier in ("完整精读", "简读", "卡片式"):
            if tiers[tier]:
                need = "、".join(f"## {n}." for n in sorted(REQUIRED_BY_TIER[tier]))
                print(f"   {tier}：{tiers[tier]:>3} 篇（必备 {need}）")
        for p in tmpl:
            print("   " + p)

        print(f"\n3. 站内链接：{'全部可解析 ✓' if not links else str(len(links)) + ' 个问题'}")
        for p in links:
            print("   " + p)

        print(f"\n4. 头部未识别到 arXiv 号：{len(no_arxiv)} 篇（需人工确认，脚本不猜）")
        for p in no_arxiv:
            print("   " + p)

        fixable_total = sum(counts[ch] for ch in FIXABLE)
        print(f"\n5. 非标准连字符：{fixable_total} 处（影响检索，可用 --fix-hyphens 修复）")
        for ch in FIXABLE:
            if counts[ch]:
                print(f"   {FIXABLE[ch]:46} {counts[ch]:>5} 处 / {len(where[ch])} 文件")
        for ch in REPORT_ONLY:
            if counts[ch]:
                print(f"   （仅提示，不自动改）{REPORT_ONLY[ch]:32} {counts[ch]:>5} 处")

    fatal = len(enc) + len(links)  # 只有结构性错误才影响退出码
    print(f"\n会破坏站点的结构性问题：{fatal}")
    print(f"内容待办（不影响构建）：缺小节 {len(tmpl)} 篇、缺 arXiv 号 {len(no_arxiv)} 篇、"
          f"非标准连字符 {sum(counts[ch] for ch in FIXABLE)} 处")
    return 1 if fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())
