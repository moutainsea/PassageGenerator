# sync chapters from txt to json
import json, re, pathlib

base = pathlib.Path(r"d:\PassageGenerator\output\novels")
txt_path = base / u"\u5916\u5356\u5458\u7684\u89c9\u9192.txt"
json_path = base / u"\u5916\u5356\u5458\u7684\u89c9\u9192.json"

raw = txt_path.read_text(encoding="utf-8").replace("\r\n", "\n")
chs = re.split(r"\n(?=\u7b2c\d+\u7ae0 )", raw)

bodies = {}
for c in chs:
    line0 = c.split("\n")[0]
    m = re.match(r"\u7b2c(\d+)\u7ae0 (.+)", line0)
    if not m:
        continue
    idx = int(m.group(1))
    title = m.group(2).strip()
    body = "\n".join(c.split("\n")[1:]).strip()
    words = len(re.sub(r"\s", "", body))
    bodies[idx] = {"title": title, "body": body, "words": words}

print("=== Word Count ===")
bad = []
for idx in sorted(bodies):
    w = bodies[idx]["words"]
    ok = 2200 <= w <= 3200
    flag = "OK" if ok else "BAD"
    if not ok:
        bad.append((idx, bodies[idx]["title"], w))
    print("Ch{:02d} {:20s} {:5d} {}".format(idx, bodies[idx]["title"], w, flag))

if bad:
    print("\nBAD chapters:")
    for idx, title, w in bad:
        print("  Ch{} {}: {}".format(idx, title, w))
else:
    print("\nAll chapters OK!")

# sync to json
data = json.loads(json_path.read_text(encoding="utf-8"))
chapters = data.get("chapters", [])
updated = 0
for ch in chapters:
    idx = ch.get("index")
    if idx in bodies:
        new_body = bodies[idx]["body"]
        if ch.get("content", "").strip() != new_body:
            ch["content"] = new_body
            updated += 1
            print("Updated Ch{}".format(idx))

json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("JSON synced, {} chapters updated".format(updated))
