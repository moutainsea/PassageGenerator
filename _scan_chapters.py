#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 feilu_八零厨神.txt 的章节结构和重复叙述问题"""
import re
import json

TXT_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.txt"
JSON_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.json"

with open(TXT_PATH, "rb") as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode("utf-8")
text = text.replace("\r\n", "\n").replace("\r", "\n")
lines = text.split("\n")
print("总行数:", len(lines))

# 找章节
chapter_pattern = re.compile(r"^第(\d+)章\s+(.+)$")
chapters = []
for i, l in enumerate(lines):
    m = chapter_pattern.match(l.strip())
    if m:
        chapters.append({
            "num": int(m.group(1)),
            "title": m.group(2),
            "line": i + 1  # 1-based
        })

for c in chapters:
    print("第{}章: line={}, title={}".format(c["num"], c["line"], c["title"]))

# 计算每章字数
chapter_ranges = []
for idx, c in enumerate(chapters):
    start_line = c["line"] - 1  # 0-based
    if idx + 1 < len(chapters):
        end_line = chapters[idx + 1]["line"] - 1
    else:
        end_line = len(lines)
    ch_text = "\n".join(lines[start_line:end_line])
    chapter_ranges.append({
        "num": c["num"],
        "title": c["title"],
        "start": start_line,
        "end": end_line,
        "char_count": len(ch_text)
    })
    print("第{}章字符数: {}".format(c["num"], len(ch_text)))
