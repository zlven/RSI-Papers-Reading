#!/usr/bin/env python3
"""按 docs/ 下笔记文件名，重新生成 mkdocs.yml 里的 nav 导航块。

文件名约定：`<分类号>-<分类名>-<序号>-<标题>-精读.md`
例如：`01-主线-01-Gödel Machine理论源头-精读.md`

脚本只改写 mkdocs.yml 中两个标记之间的内容，其余部分原样保留：

    # --- NAV BEGIN ---（本行由 scripts/gen_nav.py 自动改写，请勿手改）
    nav:
      ...
    # --- NAV END ---

新增笔记后重跑本脚本即可，无需手工维护 49 条导航项：

    python scripts/gen_nav.py
"""

from __future__ import annotations

import re
import sys
import pathlib

# Windows 控制台默认 GBK，直接 print 中文会 UnicodeEncodeError
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MKDOCS = ROOT / "mkdocs.yml"

BEGIN = "# --- NAV BEGIN ---"
END = "# --- NAV END ---"

# 分类目录名 -> 侧边栏分组标题
CATEGORY_TITLES = {
    "主线": "01 · 主线：哥德尔式 RSI 与自我改进智能体",
    "综述": "02 · 综述与立场",
    "其他路线": "03 · 其他路线：权重自编辑与经典自举",
    "零数据自博弈": "04 · 零数据自博弈",
    "进化搜索": "05 · 进化搜索",
    "经验与上下文": "06 · 经验与上下文",
    "自动化科研": "07 · 自动化科研",
    "评测基准": "08 · 评测基准",
}

# 少数文件名自动清洗后不够达意或与索引短名不一致，手工指定侧边栏条目名
TITLE_OVERRIDES = {
    "01-主线-01-Gödel Machine理论源头-精读.md": "Gödel Machine 理论源头",
    "01-主线-03-ADAS-精读.md": "ADAS / Meta Agent Search",
    "01-主线-04-Gödel Agent-精读.md": "Gödel Agent",
    "01-主线-06-Darwin Gödel Machine-精读.md": "Darwin Gödel Machine",
    "01-主线-09-Self-Harness-精读.md": "Self-Harness",
    "01-主线-14-HALO-精读.md": "HALO",
    "01-主线-17-Red Queen Gödel Machine-精读.md": "Red Queen Gödel Machine",
    "01-主线-18-Hierarchical Self-Improvement-精读.md": "Hierarchical Self-Improvement",
    "02-综述-03-Anthropic-When AI Builds Itself-精读.md": "Anthropic：When AI Builds Itself",
    "07-自动化科研-03-AIDE2-RSI-of-AI-Research-Agents-精读.md": "AIDE²：AI 研究智能体的 RSI",
}

# 分类号前缀 -> 分类名（与 CATEGORY_TITLES 对应）
NUM_TO_CAT = {
    "01": "主线",
    "02": "综述",
    "03": "其他路线",
    "04": "零数据自博弈",
    "05": "进化搜索",
    "06": "经验与上下文",
    "07": "自动化科研",
    "08": "评测基准",
}

# 第 1 组是分类号、第 2 组是分类名，二者都要用，别弄反
FILENAME_RE = re.compile(r"^(\d{2})-([^-]+)-(\d{2})-(.+)\.md$")


def yaml_str(value: str) -> str:
    """输出一个 YAML 安全字符串字面量（单引号风格，转义内部单引号）。"""
    return "'" + value.replace("'", "''") + "'"


def page_title(stem: str, raw_title: str) -> str:
    if stem in TITLE_OVERRIDES:
        return TITLE_OVERRIDES[stem]
    # 剥掉文件名尾部的 -精读 / -综述-精读，保留连字符（Co-Harness 不该被拆成 Co Harness）
    return re.sub(r"(-综述)?-精读$", "", raw_title).strip()


def collect() -> dict[str, list[tuple[int, str, str]]]:
    """返回 {分组标题: [(序号, 侧边栏名, 相对路径), ...]}，按分类号与序号排序。"""
    groups: dict[str, list[tuple[int, str, str]]] = {}
    for path in sorted(DOCS.glob("*.md")):
        if path.name in ("index.md", "references.md"):
            continue  # 首页与参考文献清单单列，不进分组
        m = FILENAME_RE.match(path.name)
        if not m:
            print(f"  [跳过] 文件名不符合约定：{path.name}", file=sys.stderr)
            continue
        num, cat, order, raw_title = m.groups()
        if num not in NUM_TO_CAT:
            print(f"  [跳过] 未知分类号 {num!r}：{path.name}", file=sys.stderr)
            continue
        if NUM_TO_CAT[num] != cat:
            print(
                f"  [警告] 分类号 {num} 应对应 {NUM_TO_CAT[num]!r}，"
                f"文件名却写作 {cat!r}：{path.name}",
                file=sys.stderr,
            )
        group = CATEGORY_TITLES[NUM_TO_CAT[num]]
        groups.setdefault(group, []).append(
            (int(order), page_title(path.name, raw_title), path.name)
        )
    for items in groups.values():
        items.sort()
    # 按分类号排序（分组标题以 01 · 开头，字典序即正确顺序）
    return {k: groups[k] for k in sorted(groups)}


def render(groups: dict[str, list[tuple[int, str, str]]]) -> str:
    lines = [BEGIN, "nav:"]
    lines.append(f"  - 总索引: {yaml_str('index.md')}")
    lines.append(f"  - 参考文献清单: {yaml_str('references.md')}")
    for group, items in groups.items():
        lines.append(f"  - {yaml_str(group)}:")
        for _order, title, name in items:
            lines.append(f"      - {yaml_str(title)}: {yaml_str(name)}")
    lines.append(END)
    return "\n".join(lines) + "\n"


def main() -> int:
    if not MKDOCS.exists():
        print(f"找不到 {MKDOCS}", file=sys.stderr)
        return 1
    text = MKDOCS.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(f"{MKDOCS} 中缺少 {BEGIN} / {END} 标记，无法安全改写。", file=sys.stderr)
        return 1

    groups = collect()
    block = render(groups)
    head, rest = text.split(BEGIN, 1)
    _old, tail = rest.split(END, 1)
    new_text = head + block + tail
    MKDOCS.write_text(new_text, encoding="utf-8")

    total = sum(len(v) for v in groups.values())
    print(f"已写入 {MKDOCS.name}：{len(groups)} 个分组、{total} 条笔记导航")
    for group, items in groups.items():
        print(f"  {group}  ({len(items)} 篇)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
