#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""同步 json 文件的 chapters 部分——按照新顺序重排。"""
import json
import re

TXT_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.txt"
JSON_PATH = r"d:\PassageGenerator\output\novels\feilu_八零厨神.json"

# 读取 txt 提取章节
with open(TXT_PATH, "rb") as f:
    raw = f.read()
if raw[:3] == b'\xef\xbb\xbf':
    raw = raw[3:]
text = raw.decode("utf-8")
text = text.replace("\r\n", "\n")

chapter_pattern = re.compile(r"^第(\d+)章\s+(.+)$", re.MULTILINE)
matches = list(chapter_pattern.finditer(text))
chapters_data = {}
for i, m in enumerate(matches):
    ch_num = int(m.group(1))
    ch_title = m.group(2)
    start = m.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(text)
    ch_text = text[start:end]
    # 去掉标题行（保留正文）
    body_start = ch_text.find("\n")
    ch_content = ch_text[body_start:].strip()
    chapters_data[ch_num] = {
        "title": ch_title,
        "content": ch_content,
        "word_count": len(ch_content)
    }
    print("第{}章: {}字".format(ch_num, len(ch_content)))

# 读取 json
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 重新映射
reorder_map = {
    1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
    10: 7, 11: 8, 12: 9, 13: 10,
    14: 11, 15: 12,
    7: 13, 8: 14, 9: 15,
    16: 16, 17: 17,
    18: 18, 19: 19, 20: 20,
}

# 倒推：旧章节号 -> 新章节号
old_to_new = reorder_map

# 构建按新章节号排序的 chapters 列表
new_chapters = []
# 先按旧章节号遍历，但放入新顺序
for old_num in sorted(old_to_new.keys(), key=lambda x: old_to_new[x]):
    new_num = old_to_new[old_num]
    if new_num in chapters_data:
        new_chapters.append({
            "title": chapters_data[new_num]["title"],
            "content": chapters_data[new_num]["content"],
            "word_count": chapters_data[new_num]["word_count"],
            "index": new_num
        })
        print("  新第{}章: {}字 标题:{}".format(new_num, chapters_data[new_num]["word_count"], chapters_data[new_num]["title"]))

# 替换 data["chapters"]
if "chapters" in data:
    data["chapters"] = new_chapters
    print("\n已替换 data['chapters']")

# 写回
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("JSON 写入完成")
