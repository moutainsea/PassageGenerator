#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 feilu_八零厨神.txt 全文重复叙述问题已修复。"""
import re

TXT_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.txt"

with open(TXT_PATH, "rb") as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode("utf-8")
text = text.replace("\r\n", "\n")
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
            "line": i + 1
        })

# 计算每章范围
chapter_ranges = []
for idx, c in enumerate(chapters):
    start_line = c["line"] - 1
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
        "char_count": len(ch_text),
        "text": ch_text
    })

# 检测重复特征词/句
suspicious_phrases = [
    "许大茂",
    "秦淮茹",
    "借了",
    "摆在",
    "卤煮",
    "三年前",
    "你到底",
    "200多块",
    "203块",
    "三环三冷三合",  # 第16章错字
    "三烤三冷三焖",
    "赊给我",
    "借我5块钱",
    "小当和槐花",
    "三烤三冷三焖",
    "拓",
    "熿光",
    "珓光",
    "釉光",
    "炀",
]

print("\n=== 章节基本信息 ===")
for c in chapter_ranges:
    print("第{}章: {} 字, 标题: {}".format(c["num"], c["char_count"], c["title"]))

# 两两章节对比，找出高度相似的
print("\n=== 检测跨章节重复叙述 ===")
# 简单方法：把每章文本按"句号"分句，统计"相似度"
import hashlib
def get_sentence_hashes(text):
    sentences = re.split(r"[。！？\n]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
    return set(sentences)

chapter_hashes = {c["num"]: get_sentence_hashes(c["text"]) for c in chapter_ranges}

# 检测：两章的公共句子数
for i, c1 in enumerate(chapter_ranges):
    for c2 in chapter_ranges[i+1:]:
        common = chapter_hashes[c1["num"]] & chapter_hashes[c2["num"]]
        if len(common) >= 5:  # 5个以上相同句子认为重复
            print("\n第{}章 vs 第{}章 有 {} 个相同句子:".format(c1["num"], c2["num"], len(common)))
            for s in list(common)[:5]:
                print("  - " + s[:60])
