#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove duplicate boilerplate paragraphs and fix English leaks in chapters."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

BOILERPLATE_STARTS = [
    "我再翻第五册，对照关东碑拓片",
    "旅舍/道观/巷口/看守所里，我听见远处更鼓",
]

REPEAT_BLOCK_START = "钥上刻绳，绳是链的语"

EN_REPLACEMENTS = [
    (r"\bJuly\b", "七月"),
    (r"\bdredge\b", "疏浚"),
    (r"\bbed\b", "床"),
    (r"\bpencil\b", "铅笔"),
    (r"\bfit\b", "吻合"),
    (r"\bsample\b", "样本"),
    (r"\beye\b", "眼"),
    (r"\bnot fish\b", "非鱼"),
    (r"\btest\b", "检验"),
    (r"\bfracture\b", "骨折"),
    (r"\bforeign\b", "外来"),
    (r"\bdepth\b", "深度"),
    (r"\bnightly\b", "每夜"),
    (r"\bunderwater\b", "水下"),
    (r"\brust\b", "锈"),
    (r"\bcrossing\b", "渡口"),
    (r"\bCHIN LUNG\b", "镇龙"),
    (r"\bRITUAL\b", "仪"),
    (r"\bTientsin\b", "天津"),
    (r"\bStrike\b", "罢工"),
    (r"\bProtect\b", "护"),
    (r"\bKun\b", "困"),
    (r"\bBurn\b", "燃"),
    (r"\bMission\b", "任务"),
    (r"\bdragon\b", "龙"),
    (r"\bbreath\b", "息"),
    (r"\bgeology\b", "地质"),
    (r"\bGeology\b", "地质"),
    (r"\bchemistry\b", "化学"),
    (r"\bserpent\b", "海蛇"),
    (r"\bSea Serpent\b", "海蛇"),
    (r"\bRumors\b", "谣言"),
    (r"\bManchuria\b", "满洲"),
    (r"\breptile\b", "爬行类"),
    (r"\biodine\b", "碘"),
    (r"\bchlor\b", "氯"),
    (r"\bspecimen\b", "标本"),
    (r"\bHan three coins\b", "韩三三块银圆"),
    (r"\bHan\b", "韩"),
    (r"\bthree coins\b", "三块银圆"),
    (r"\bHonest\b", "诚实"),
    (r"\bhonest\b", "诚实"),
    (r"\bmetaphor\b", "隐喻"),
    (r"\baloud\b", "出声"),
    (r"\bfear\b", "惧"),
    (r"\benough\b", "够"),
    (r"\bladder\b", "梯"),
]


def split_body(text: str):
    m = re.search(r"(## 正文\s*\n)(.*)", text, re.S)
    if not m:
        return None, None, None
    prefix = text[: m.start()]
    body = m.group(2)
    m2 = re.search(r"\n## 章节备注", body)
    if m2:
        suffix = body[m2.start() :]
        body = body[: m2.start()]
    else:
        suffix = ""
    return prefix + m.group(1), body, suffix


def dedup_paragraphs(body: str) -> str:
    paras = re.split(r"\n\s*\n", body.strip())
    seen = set()
    out = []
    skip_block = False
    for p in paras:
        p = p.strip()
        if not p:
            continue
        if p.startswith("---") and len(p) <= 5:
            if out and out[-1].startswith("---"):
                continue
            out.append(p)
            continue
        if any(p.startswith(s) for s in BOILERPLATE_STARTS):
            continue
        if p.startswith(REPEAT_BLOCK_START):
            if skip_block:
                continue
            skip_block = True
        key = re.sub(r"\s+", "", p)
        if key in seen and len(key) > 60:
            continue
        seen.add(key)
        out.append(p)
    return "\n\n".join(out)


def fix_english(body: str) -> str:
    for pat, rep in EN_REPLACEMENTS:
        body = re.sub(pat, rep, body)
    return body


def process_file(path: Path):
    text = path.read_text(encoding="utf-8")
    head, body, tail = split_body(text)
    if body is None:
        return False
    new_body = fix_english(dedup_paragraphs(body))
    if new_body == body.strip():
        return False
    path.write_text(head + new_body + tail, encoding="utf-8")
    return True


def main():
    targets = sorted(BASE.glob("第*章-*.md"))
    changed = [p.name for p in targets if process_file(p)]
    print(f"Updated {len(changed)} files")
    for n in changed:
        print(f"  {n}")


if __name__ == "__main__":
    main()
