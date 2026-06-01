#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json
from datetime import datetime, timezone, timedelta

p = Path(__file__).parent / "第65章-韩三南下.md"
text = p.read_text(encoding='utf-8')

addon = """
后仓里，我把口述又与武进童子「西南逃」、昆明龙谱「至尊伤南迁歇花眼」并读。三句成扇：东扇江南，西扇西南，扇心空在营河口。空不是无，是阖裂未合；合要九十九格满，满要纸路北、水路南两线收网。韩三收水，我收格。何主编短笺「缓」字，缓不是停，是等韩三一息贴水南去，等裴老栓第三张与第二张仍勿合成，等协查过佟掌柜门而不入后仓。韩三述桨边沉前抬头，眼未开全，开一线，线指南——南是阖裂渗息的方向，不是它要给人看，是人要追息；追不上，只能记。记是除名者唯一不被缴的权。第六十五格满，蜡封毕，隔板六十六格空位在等，等编号与地图点逐一贴对；贴对九成八，余空在营河口，圈注「缺阖·待合」。合在下一格，合目则第七篇镇龙司旧档在北平西庑，卷四百七缺阖滨海——滨海即营河口，即七月滩涂。合处我此刻不往，往则观，观则目眚；我只留空圈，圈里最诚。

（第六十五章完）
"""

if '（第六十五章完）' not in text:
    text = text.replace('\n---\n\n## 章节备注', '\n' + addon.strip() + '\n\n---\n\n## 章节备注')
    p.write_text(text, encoding='utf-8')
    print("Appended expansion")

lines = text.split('\n')
for i, l in enumerate(lines):
    if l.startswith('# 第') and '章' in l:
        body = '\n'.join(lines[i+1:])
        break
wc = len(re.findall(r'[\u4e00-\u9fff]', re.sub(r'#{1,6}\s*', '', body)))
print(f"Word count: {wc}")

# update json for ch65
json_path = Path(__file__).parent / "02-写作计划.json"
data = json.loads(json_path.read_text(encoding='utf-8'))
for ch in data['chapters']:
    if ch['chapterNumber'] == 65:
        ch['wordCount'] = wc
        ch['wordCountPass'] = wc >= 3000
        ch['needsExpansion'] = wc < 3000
        ch['status'] = 'completed'
tz = timezone(timedelta(hours=8))
data['updatedAt'] = datetime.now(tz).strftime('%Y-%m-%dT%H:%M:%S+08:00')
json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
