import re, io, json
txt_path = r'd:\PassageGenerator\output\novels\外卖员的觉醒.txt'
json_path = r'd:\PassageGenerator\output\novels\外卖员的觉醒.json'
with io.open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read().replace(chr(13)+chr(10), chr(10))
chs = re.split(r'\n(?=第\d+章 )', text)
bodies = {}
for c in chs:
    lines = c.split(chr(10))
    m = re.match(r'第(\d+)章 (.+)', lines[0])
    if m:
        body = chr(10).join(lines[1:]).strip()
        bodies[int(m.group(1))] = body
for idx in [16, 17]:
    if idx in bodies:
        print('Ch%d: %d words' % (idx, len(re.sub(r'\s', '', bodies[idx]))))
with io.open(json_path, 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
updated = 0
for ch in data['chapters']:
    idx = ch.get('index')
    if idx in bodies and bodies[idx] != ch.get('content', ''):
        ch['content'] = bodies[idx]
        updated += 1
with io.open(json_path, 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
print('Updated %d chapters in JSON' % updated)
