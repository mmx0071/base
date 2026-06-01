#!/usr/bin/env python3
"""从作者版章节 Markdown 导出读者版 TXT。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "读者版"
CHAPTER_GLOB = "第*章*.md"
BOOK_TITLE = "坠龙档案"


def extract_section(text: str, name: str, stop_before: str | None = None) -> str:
    """提取 ## name 与下一 ## 或 stop_before 之间的内容。"""
    pattern = rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not m:
        return ""
    body = m.group(1)
    if stop_before:
        stop = re.search(rf"^## {re.escape(stop_before)}\s", body, re.MULTILINE)
        if stop:
            body = body[: stop.start()]
    return body.strip()


def clean_epigraph(raw: str) -> str:
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            line = line.lstrip(">").strip()
        if line == "---":
            continue
        lines.append(f"　　{line}")
    return "\n".join(lines)


def clean_body(raw: str) -> str:
    """正文：保留段落，场景分隔线转为空行。"""
    raw = raw.strip()
    raw = re.sub(r"\n---\s*$", "", raw)
    parts: list[str] = []
    for block in re.split(r"\n---\n", raw):
        block = block.strip()
        if not block or block == "---":
            continue
        paras = [
            p.strip()
            for p in re.split(r"\n\s*\n", block)
            if p.strip() and p.strip() != "---"
        ]
        if paras:
            parts.append("\n\n".join(paras))
    return "\n\n".join(parts)


def parse_chapter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")

    title_m = re.match(r"^#\s*(.+?)\s*$", text, re.MULTILINE)
    if not title_m:
        raise ValueError(f"无法解析标题: {path.name}")
    title = title_m.group(1).strip()
    # 读者版标题：第1章 雨前的告示（去掉冒号）
    title = title.replace("：", " ", 1)

    epigraph_raw = extract_section(text, "章首引子")
    body_raw = extract_section(text, "正文", stop_before="章节备注")

    if not body_raw:
        raise ValueError(f"缺少正文: {path.name}")

    sections: list[str] = [title, ""]

    if epigraph_raw:
        epigraph = clean_epigraph(epigraph_raw)
        sections.extend([epigraph, ""])

    sections.append(clean_body(body_raw))
    return title, "\n".join(sections).rstrip() + "\n"


def chapter_sort_key(path: Path) -> int:
    m = re.search(r"第(\d+)章", path.name)
    return int(m.group(1)) if m else 0


def main() -> None:
    chapters = sorted(ROOT.glob(CHAPTER_GLOB), key=chapter_sort_key)
    if len(chapters) != 99:
        raise SystemExit(f"期望 99 章，实际 {len(chapters)} 章")

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "分章").mkdir(exist_ok=True)

    full_parts: list[str] = [
        BOOK_TITLE,
        "",
        "历史民俗悬疑 / 志怪档案体",
        "第一人称 · 沈砚清私人档案",
        "",
        "=" * 40,
        "",
    ]

    total_chars = 0
    for path in chapters:
        title, content = parse_chapter(path)
        # 分章文件
        out_name = path.stem + ".txt"
        (OUT_DIR / "分章" / out_name).write_text(content, encoding="utf-8")

        full_parts.append(content)
        full_parts.extend(["", "=" * 40, ""])

        # 统计正文汉字（不含标题与引子中的空白）
        body_only = content.split("\n\n", 2)[-1] if "章首引子" not in content else content
        total_chars += len(re.sub(r"\s", "", body_only))

    # 全书合订
    full_text = "\n".join(full_parts).rstrip() + "\n"
    (OUT_DIR / f"{BOOK_TITLE}.txt").write_text(full_text, encoding="utf-8")

    print(f"已导出 {len(chapters)} 章")
    print(f"分章目录: {OUT_DIR / '分章'}")
    print(f"合订本:   {OUT_DIR / f'{BOOK_TITLE}.txt'}")
    print(f"合订本约 {len(full_text):,} 字符")


if __name__ == "__main__":
    main()
