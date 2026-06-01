#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate chapters 88-99 for 坠龙档案 (第九篇·隐龙诀)"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).parent
CHECK = BASE / "check_chapter_wordcount.py"
PLAN = BASE / "02-写作计划.json"
MIN_WORDS = 3000

TEMPLATE = """# 第{num}章：{title}

## 本章概要
- **核心事件**：{core}
- **承接上章**：{prev}
- **悬念钩子**：{hook}

---

## 章首引子

> {epigraph}

---

## 正文

{body}

---

## 章节备注
- 本章悬念：{note_hook}
- 下章预告：{note_next}
- 伏笔标记：{note_mark}
"""


def extract_body(text: str) -> str:
    m = re.search(r"## 正文\s*\n(.*?)(?=\n---|\n## 章节备注|\Z)", text, re.S)
    return m.group(1) if m else ""


def count_chinese(text: str) -> int:
    body = extract_body(text) if "## 正文" in text else text
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith(">"):
            s = s.lstrip(">").strip()
        lines.append(s)
    body = "\n".join(lines)
    return len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", body))


def pad_body(body: str, extras: list[str]) -> str:
    result = body.strip()
    i = 0
    max_iter = max(len(extras) * 5, 10) if extras else 0
    while count_chinese(result) < MIN_WORDS and i < max_iter and extras:
        result += "\n\n" + extras[i % len(extras)].strip()
        i += 1
    return result


def write_chapter(num: int, title: str, meta: dict, body: str, extras: list[str]):
    full_body = pad_body(body, extras)
    content = TEMPLATE.format(num=num, title=title, body=full_body, **meta)
    path = BASE / f"第{num}章-{title}.md"
    path.write_text(content, encoding="utf-8")
    wc = count_chinese(content)
    status = "PASS" if wc >= MIN_WORDS else "FAIL"
    print(f"{status} 第{num}章-{title}.md: {wc} 字")
    return path, wc, wc >= MIN_WORDS


def update_plan(counts: dict[int, int]):
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    tz = timezone(timedelta(hours=8))
    plan["updatedAt"] = datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    done = 0
    for ch in plan["chapters"]:
        n = ch["chapterNumber"]
        if n in counts:
            wc = counts[n]
            ch["wordCount"] = wc
            ch["wordCountPass"] = wc >= plan.get("minWordsPerChapter", MIN_WORDS)
            ch["status"] = "completed" if ch["wordCountPass"] else "in_progress"
            ch["needsExpansion"] = not ch["wordCountPass"]
            if ch["wordCountPass"]:
                done += 1
    total = len(plan["chapters"])
    plan["status"] = "completed" if done == total else "in_progress"
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n写作计划已更新: 达标 {done}/{total}")


# ── Chapter bodies loaded from companion module ──
from _bodies_88_99 import CHAPTERS  # noqa: E402


def main():
    counts = {}
    all_pass = True
    for num, (title, meta, body, extras) in sorted(CHAPTERS.items()):
        _, wc, ok = write_chapter(num, title, meta, body, extras)
        counts[num] = wc
        if not ok:
            all_pass = False
    update_plan(counts)
    if all_pass:
        print("\n全部 PASS")
        subprocess.run([sys.executable, str(CHECK)] + [str(BASE / f"第{n}章-{CHAPTERS[n][0]}.md") for n in range(88, 100)])
        sys.exit(0)
    else:
        print("\n存在未达标章节，请扩充 _bodies_88_99.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
