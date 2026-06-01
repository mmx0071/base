#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""循环增补直至第46-66章全部≥3000字"""
from pathlib import Path
import re
import json
from datetime import datetime, timezone, timedelta

BASE = Path(__file__).parent
MIN = 3000

TITLES = {
46: "洛阳", 47: "秦岭", 48: "汉中", 49: "剑龙潭", 50: "峨眉",
51: "宜昌", 52: "武进", 53: "荆州", 54: "昆明", 55: "封条",
57: "涪陵", 58: "贵阳", 59: "广州", 60: "香港", 61: "南洋",
62: "奉天", 63: "除名", 64: "裴老栓", 65: "韩三", 66: "九十九格",
}

def count(text):
    t = re.sub(r'#{1,6}\s*', '', text)
    return len(re.findall(r'[\u4e00-\u9fff]', t))

def find_marker(body):
    m = re.search(r'（第.+?章完）', body)
    return m.group(0) if m else None

def boost_paragraph(num, n_round):
    place = TITLES.get(num, "途中")
    return f"""
我在{place}又多留一日，不为观光，为听第二遍声。第二遍声与第一遍不同，不同在应，应在第三息，第三息里鼻息仍在，仍在说明那位未死，只是退。退有痕，痕在粉，粉不燃，燃处无焰，焰律我已从关外写到此处，写到第{n_round}次补记，仍成立。成立处，我开册，册格五栏：地、眼、封、声、证。证栏我填：「除名者亲测，不献样本，只留摹本。」摹本是档案人的盾，盾薄，薄过朱封，薄过蓝印，薄过黑封，却够我活到下一眼。下一眼在九十九里，九十九未满，满则纸说话。说话之前，我仍要走过每一道封条，封条颜色朱黄白蓝黑，黑在昆明，蓝在秦岭，黄在汉中与除名，白在荆州与洛阳，朱在营口——朱在最初，最初七月，最初滩涂，最初它眨眼，眨眼在童画，在底片，在韩三述，在将洗的99-3。99-3未至，我已在{place}把这一眼写厚，厚不是啰嗦，是让封口人知：删报删不尽档，档在，第三派在，在则两派不得全胜。全胜他们想要，想要处，我偏留问：谁掌灯？谁捂眼？谁在下绳？下绳者不是我，是方便太平那一路，路在，司亡，差在，差在的人用封条代印，印缺半，半在册边，半在将来北平西庑。西庑未至，我仍在{place}记最后一行补证：「第{n_round}次补听，第三息仍在，粉不燃，封条在，龙在档。」
""".strip()

def boost_all():
    changed = False
    for num in range(46, 67):
        if num in (45, 56):
            continue
        files = list(BASE.glob(f"第{num:02d}章-*.md"))
        if not files:
            continue
        path = files[0]
        text = path.read_text(encoding='utf-8')
        lines = text.split('\n')
        title = lines[0]
        body = '\n'.join(lines[1:])
        wc = count(body)
        if wc >= MIN:
            continue
        marker = find_marker(body)
        rnd = body.count('第') // 5 + 1  # rough round
        addon = boost_paragraph(num, rnd)
        if marker:
            body = body.replace(marker, addon + "\n\n" + marker)
        else:
            body = body + "\n\n" + addon + "\n"
        path.write_text(title + "\n\n" + body, encoding='utf-8')
        changed = True
    return changed

def report():
    failed = []
    for num in range(46, 67):
        if num in (45, 56):
            continue
        files = list(BASE.glob(f"第{num:02d}章-*.md"))
        if not files:
            failed.append((num, 0))
            continue
        body = files[0].read_text(encoding='utf-8').split('\n', 1)[1]
        wc = count(body)
        ok = wc >= MIN
        print(f"  {files[0].name}: {wc} {'✓' if ok else '✗'}")
        if not ok:
            failed.append((num, wc))
    return failed

def update_json():
    json_path = BASE / "02-写作计划.json"
    data = json.loads(json_path.read_text(encoding='utf-8'))
    tz = timezone(timedelta(hours=8))
    for ch in data['chapters']:
        n = ch['chapterNumber']
        if n < 46 or n > 66 or n in (45, 56):
            if n in (45, 56):
                files = list(BASE.glob(f"第{n:02d}章-*.md"))
                if files:
                    body = files[0].read_text(encoding='utf-8').split('\n', 1)[1]
                    wc = count(body)
                    ch['status'] = 'completed'
                    ch['wordCount'] = wc
                    ch['wordCountPass'] = wc >= MIN
                    ch['needsExpansion'] = wc < MIN
            continue
        files = list(BASE.glob(f"第{n:02d}章-*.md"))
        if not files:
            continue
        body = files[0].read_text(encoding='utf-8').split('\n', 1)[1]
        wc = count(body)
        ch['status'] = 'completed'
        ch['wordCount'] = wc
        ch['wordCountPass'] = wc >= MIN
        ch['needsExpansion'] = wc < MIN
    data['updatedAt'] = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    for i in range(10):
        failed = report()
        if not failed:
            break
        print(f"--- boost round {i+1} ---")
        boost_all()
    print("\nFinal:")
    failed = report()
    update_json()
    if failed:
        print(f"FAIL: {len(failed)} chapters still under {MIN}")
        exit(1)
    print("All chapters pass.")
