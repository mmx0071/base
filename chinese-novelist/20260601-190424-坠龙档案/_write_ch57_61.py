#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble _body57-61.md into chapter files and verify word count."""
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).parent
CHECK = Path.home() / ".cursor/skills/chinese-novelist/scripts/check_chapter_wordcount.py"

CHAPTERS = [
    (57, "涪陵印记"),
    (58, "贵阳天眼洞"),
    (59, "广州黄花塘"),
    (60, "香港译报"),
    (61, "华侨信"),
]


def count_cn(text: str) -> int:
    text = re.sub(r"#{1,6}\s*", "", text)
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def main():
    results = []
    for num, title in CHAPTERS:
        body_path = BASE / f"_body{num}.md"
        if not body_path.exists():
            print(f"Missing {body_path}")
            sys.exit(1)
        body = body_path.read_text(encoding="utf-8").strip() + "\n"
        out = BASE / f"第{num}章-{title}.md"
        out.write_text(f"# 第{num}章：{title}\n\n{body}\n", encoding="utf-8")
        wc = count_cn(body)
        results.append((out.name, wc, wc >= 3000))
        print(f"  {out.name}: {wc} 字 {'pass' if wc >= 3000 else 'FAIL'}")

    failed = [r for r in results if not r[2]]
    if failed:
        sys.exit(1)

    print("\n--- check_chapter_wordcount.py ---")
    for num, title in CHAPTERS:
        p = BASE / f"第{num}章-{title}.md"
        subprocess.run([sys.executable, str(CHECK), str(p)], check=False)

    print("\nOK")


if __name__ == "__main__":
    main()
