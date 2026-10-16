#!/usr/bin/env python3
"""精读笔记一致性自检与字符规范化。

检查五件事：

1. **文件名归一化**——必须是 NFC。中文 macOS 上常出现 NFD 分解形式，
   会造成 MkDocs 路由与 Markdown 链接静默失配。
2. **模板完整性**——每篇应含 `## 0.` 到 `## 9.` 共 10 个小节（模板 v1.0）。
3. **站内链接可解析**——相对 Markdown 链接必须指向 docs/ 下真实存在的文件。
4. **arXiv 号缺失**——头部未写明编号的篇目，供人工补充；脚本不猜。
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
MD_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)#\s]+)(?:#[^)]*)?\)")

EXPECTED_SECTIONS = set(range(10))  # 注意是 int，需与 int(n) 同型才能求差集
NOT_A_NOTE = {"index.md", "references.md"}  # 首页与文献清单不套精读模板

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


def check_sections(files: list[pathlib.Path]) -> tuple[list[str], list[str]]:
    problems, no_arxiv = [], []
    for path in files:
        if path.name in NOT_A_NOTE:
            continue
        text = path.read_text(encoding="utf-8")
        found = {int(n) for n in SECTION_RE.findall(text)}
        missing = sorted(EXPECTED_SECTIONS - found)
        if missing:
            problems.append(
                f"[模板] {rel(path)} 缺少小节：{', '.join('## ' + str(n) + '.' for n in missing)}"
            )
        head = "\n".join(text.split("\n")[:25])
        if not (ARXIV_NEW.search(head) or ARXIV_OLD.search(head)):
            no_arxiv.append(rel(path))
    return problems, no_arxiv


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
    tmpl, no_arxiv = check_sections(files)
    links = check_links(files)

    if not quiet:
        print(f"扫描 {rel(DOCS)}：{len(files)} 个文件（{len(notes)} 篇精读）\n")

        print(f"1. 文件名编码：{'全部 NFC ✓' if not enc else str(len(enc)) + ' 个问题'}")
        for p in enc:
            print("   " + p)

        print(f"\n2. 模板完整性（## 0.–## 9.）：{'全部完整 ✓' if not tmpl else str(len(tmpl)) + ' 个问题'}")
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
