# -*- coding: utf-8 -*-
import re, json

txt_file = r"d:\PassageGenerator\output\novels\fanqie_序列觉醒_不止是地球第一.txt"
json_file = r"d:\PassageGenerator\output\novels\fanqie_序列觉醒_不止是地球第一.json"

with open(txt_file, "r", encoding="utf-8") as f:
    raw = f.read().replace("\r\n", "\n")

chs = re.split(r"\n(?=第\d+章 )", raw)
for c in chs:
    m = re.match(r"第(\d+)章 (.+)", c.split("\n")[0])
    if m and int(m.group(1)) == 6:
        body = "\n".join(c.split("\n")[1:]).strip()
        words = len(re.sub(r"\s", "", body))
        print("Chapter 6:", words, "words")
        print("OK" if 2200 <= words <= 3200 else "NEEDS FIX: {}".format(words))
        
        with open(json_file, "r", encoding="utf-8") as fj:
            data = json.loads(fj.read())
        for ch in data["chapters"]:
            if ch["index"] == 6:
                ch["content"] = body
                print("JSON Ch6 updated")
                break
        with open(json_file, "w", encoding="utf-8") as fj:
            fj.write(json.dumps(data, ensure_ascii=False, indent=2))
        print("Done")
        break
