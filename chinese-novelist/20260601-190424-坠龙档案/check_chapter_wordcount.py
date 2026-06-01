#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验章节正文字数（中文汉字），不足则提示或扩充标记。"""
import re
import sys
from pathlib import Path

MIN_WORDS = 3000
BASE = Path(__file__).parent


def extract_body(text: str) -> str:
    m = re.search(r"## 正文\s*\n(.*)", text, re.S)
    if not m:
        return ""
    body = m.group(1)
    m2 = re.search(r"\n## 章节备注", body)
    if m2:
        body = body[: m2.start()]
    return body.strip()


def count_chinese(text: str) -> int:
    """统计正文汉字数（含中文标点）。"""
    body = extract_body(text)
    # 去掉 markdown 引用行首 >
    lines = []
    for line in body.splitlines():
        s = line.strip()
        if s.startswith(">"):
            s = s.lstrip(">").strip()
        lines.append(s)
    body = "\n".join(lines)
    # 汉字 + 中文标点
    chars = re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", body)
    return len(chars)


def check_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    wc = count_chinese(text)
    return {
        "path": path,
        "wordCount": wc,
        "pass": wc >= MIN_WORDS,
    }


def main():
    targets = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted(BASE.glob("第*章-*.md"))
    results = []
    for p in targets:
        if not p.exists():
            print(f"MISSING: {p.name}")
            results.append({"path": p, "wordCount": 0, "pass": False})
            continue
        r = check_file(p)
        results.append(r)
        status = "PASS" if r["pass"] else "FAIL"
        print(f"{status} {p.name}: {r['wordCount']} 字")
    fails = [r for r in results if not r["pass"]]
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
