#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate chapters 46-50 with >=3000 Chinese characters each."""

import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent
CHECK = Path.home() / ".cursor/skills/chinese-novelist/scripts/check_chapter_wordcount.py"

CHAPTERS = []


def add(num, title, summary, carry, hook, epigraph, body, notes):
    CHAPTERS.append((num, title, summary, carry, hook, epigraph, body, notes))


def render(num, title, summary, carry, hook, epigraph, body, notes):
    return f"""# 第{num}章：{title}

## 本章概要
- **核心事件**：{summary}
- **承接上章**：{carry}
- **悬念钩子**：{hook}

---

## 章首引子

> {epigraph}

---

## 正文

{body}

---

## 章节备注
{notes}
"""


# Load bodies from companion files
for _f in ("gen_ch46_47_bodies.py", "gen_ch48_50_bodies.py"):
    exec((BASE / _f).read_text(encoding="utf-8"))

if __name__ == "__main__":
    for num, title, summary, carry, hook, epigraph, body, notes in CHAPTERS:
        path = BASE / f"第{num}章-{title}.md"
        path.write_text(
            render(num, title, summary, carry, hook, epigraph, body, notes),
            encoding="utf-8",
        )
        r = subprocess.run(
            [sys.executable, str(CHECK), str(path)],
            capture_output=True,
            text=True,
        )
        m = re.search(r"字数:\s*(\d+)", r.stdout)
        wc = int(m.group(1)) if m else 0
        ok = "✓" if wc >= 3000 else "✗"
        print(f"第{num}章 {title}: {wc} {ok}")
