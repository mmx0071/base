#!/usr/bin/env python3
"""同步章节文件存在性与字数到 02-写作计划.json"""
import json
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PLAN_PATH = PROJECT / "02-写作计划.json"
MIN_WORDS = 3000


def extract_body(text: str) -> str:
    m = re.search(r"## 正文\s*\n(.*)", text, re.S)
    if not m:
        return ""
    body = m.group(1)
    m2 = re.search(r"\n## 章节备注", body)
    if m2:
        body = body[: m2.start()]
    return body.strip()


def count_words(md: Path) -> int:
    text = md.read_text(encoding="utf-8")
    body = extract_body(text)
    return len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", body))


def main():
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    done = 0
    total_words = 0
    for ch in plan["chapters"]:
        fp = PROJECT / ch["filePath"]
        if fp.exists():
            wc = count_words(fp)
            ch["wordCount"] = wc
            ch["wordCountPass"] = wc >= plan.get("minWordsPerChapter", MIN_WORDS)
            ch["status"] = "completed" if ch["wordCountPass"] else "in_progress"
            total_words += wc
            if ch["wordCountPass"]:
                done += 1
        else:
            ch["status"] = "pending"
            ch["wordCount"] = None
            ch["wordCountPass"] = None
    total = len(plan["chapters"])
    plan["status"] = "completed" if done == total else "in_progress"
    plan["updatedAt"] = "2026-06-01T23:59:00+08:00"
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"达标章节: {done}/{total}")
    print(f"总字数: {total_words:,}")


if __name__ == "__main__":
    main()
