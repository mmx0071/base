#!/usr/bin/env python3
"""Remove AI boilerplate and duplicate blocks from chapter files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BOILERPLATE = re.compile(
    r"\n我合上册时，窗外雨线如针，针脚缝住满城嘴；缝住了，档还在床底.*?墨里龙在。\n",
    re.DOTALL,
)

DANZHONG = re.compile(
    r"\n担重的人，睡眠浅。浅梦里，营口雨、西湖雨.*?就不算坠。\n",
    re.DOTALL,
)

# Trailing index chains (章足 style)
INDEX_CHAIN = re.compile(
    r"\n(?:识钩|不掉|鸣中|再记|补记：档案续链)[^\n]*(?:八[0-9]|九[0-9]|第[0-9]+章|章足|此章足)[^\n]*\n(?:.*(?:八[0-9]|九[0-9]|第[0-9]+章|章足|此章足).*\n)+\n",
    re.DOTALL,
)

CH96_TAIL = re.compile(
    r"\n生物学先生第四封信至.*?第九十六章尽。\n\n---\n\n补记：档案续链.*?（96-0）\n",
    re.DOTALL,
)


def dedupe_paragraphs(text: str) -> str:
    """Remove consecutive duplicate paragraphs."""
    paras = text.split("\n\n")
    out = []
    prev = None
    for p in paras:
        s = p.strip()
        if not s:
            continue
        if s == prev:
            continue
        out.append(p)
        prev = s
    return "\n\n".join(out)


def clean_file(path: Path) -> list[str]:
    changes = []
    text = path.read_text(encoding="utf-8")
    orig = text

    if m := BOILERPLATE.search(text):
        text = text[: m.start()] + "\n" + text[m.end() :]
        changes.append("removed_boilerplate")

    # keep first 担重 block only
    blocks = list(DANZHONG.finditer(text))
    if len(blocks) > 1:
        for b in reversed(blocks[1:]):
            text = text[: b.start()] + text[b.end() :]
        changes.append(f"removed_{len(blocks)-1}_danzhong_dupes")

    if path.name == "第96章-最后一声雷.md" and CH96_TAIL.search(text):
        # keep content up to line 118 area, trim runaway tail
        marker = "雨灾后第七日，河平"
        idx = text.find(marker)
        if idx != -1:
            end_section = text.find("\n---\n\n## 章节备注", idx)
            if end_section != -1:
                good = text[:idx].rstrip()
                tail = (
                    "\n\n雨灾后第七日，河平，平如无波。我于顶阁听，听无雷——无雷证尾尽。"
                    "尾尽，约尽，跪别可起。世人只记雨，档案记雷；雷在喉，不在天，"
                    "最后一声是别，不是怒。\n"
                )
                text = good + tail + text[end_section:]
                changes.append("trimmed_ch96_tail")

    text = dedupe_paragraphs(text)

    if text != orig:
        path.write_text(text, encoding="utf-8")
    return changes


def main():
    targets = sorted(ROOT.glob("第*.md"))
    for p in targets:
        ch = changes = clean_file(p)
        if changes:
            print(f"{p.name}: {', '.join(changes)}")


if __name__ == "__main__":
    main()
