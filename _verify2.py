#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证重排后的章节字数与重复叙述。"""
import re

TXT_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.txt"

with open(TXT_PATH, "rb") as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode("utf-8")
text = text.replace("\r\n", "\n")
lines = text.split("\n")

chapter_pattern = re.compile(r"^第(\d+)章\s+(.+)$")
matches = list(chapter_pattern.finditer(text))
chapters = []
for i, m in enumerate(matches):
    ch_num = int(m.group(1))
    ch_title = m.group(2)
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    ch_text = text[start:end]
    chapters.append({
        "num": ch_num,
        "title": ch_title,
        "char_count": len(ch_text),
        "text": ch_text
    })

print("=== 章节字数验证（要求 2200-3200） ===")
issues = []
for c in chapters:
    flag = ""
    if c["char_count"] < 2200:
        flag = "  [过短!]"
        issues.append(("过短", c["num"], c["char_count"]))
    elif c["char_count"] > 3200:
        flag = "  [过长!]"
        issues.append(("过长", c["num"], c["char_count"]))
    print("第{}章: {} 字, 标题: {}{}".format(c["num"], c["char_count"], c["title"], flag))

if issues:
    print("\n=== 问题章节 ===")
    for typ, num, cnt in issues:
        print("  {} - 第{}章: {}字".format(typ, num, cnt))
else:
    print("\n所有章节字数符合规范！")

# 重复检测
print("\n=== 重复叙述检测 ===")
def get_sentences(text):
    sents = re.split(r"[。！？\n]+", text)
    return set(s.strip() for s in sents if len(s.strip()) > 15)

chapter_sentences = {c["num"]: get_sentences(c["text"]) for c in chapters}

for i, c1 in enumerate(chapters):
    for c2 in chapters[i+1:]:
        common = chapter_sentences[c1["num"]] & chapter_sentences[c2["num"]]
        if len(common) >= 5:
            print("第{}章 vs 第{}章: {} 个相同句子".format(c1["num"], c2["num"], len(common)))
            for s in list(common)[:3]:
                print("  - " + s[:60])

print("\n=== 标题相似度检测 ===")
for i, c1 in enumerate(chapters):
    for c2 in chapters[i+1:]:
        # 检测相似标题
        t1 = re.sub(r"[，,。\s]", "", c1["title"])
        t2 = re.sub(r"[，,。\s]", "", c2["title"])
        if t1 == t2 or t1 in t2 or t2 in t1:
            print("  相似标题: 第{}章 '《{}》' vs 第{}章 '《{}》'".format(
                c1["num"], c1["title"], c2["num"], c2["title"]))
