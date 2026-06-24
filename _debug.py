#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
TXT_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.txt"
with open(TXT_PATH, "rb") as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode("utf-8")
text = text.replace("\r\n", "\n")

chapter_pattern = re.compile(r"^第(\d+)章\s+(.+)$")
matches = list(chapter_pattern.finditer(text))
print("matches found:", len(matches))
for i, m in enumerate(matches):
    ch_num = int(m.group(1))
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    ch_text = text[start:end]
    print("第{}章: len={}".format(ch_num, len(ch_text)))
