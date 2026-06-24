# -*- coding: utf-8 -*-
"""Fix chapter 6 opening of 序列觉醒 to connect with chapter 5 ending."""
import re, json

txt_file = r"d:\PassageGenerator\output\novels\fanqie_序列觉醒_不止是地球第一.txt"
json_file = r"d:\PassageGenerator\output\novels\fanqie_序列觉醒_不止是地球第一.json"

with open(txt_file, "r", encoding="utf-8") as f:
    raw = f.read().replace("\r\n", "\n")

# Split chapters
chs = re.split(r"\n(?=第\d+章 )", raw)
chapters_dict = {}
for c in chs:
    line0 = c.split("\n")[0]
    m = re.match(r"第(\d+)章 (.+)", line0)
    if not m:
        continue
    idx = int(m.group(1))
    chapters_dict[idx] = c

ch6 = chapters_dict[6]
ch6_lines = ch6.split("\n")

# Find the index of "他闭上眼睛，脑海里闪过白天赵明被他一脚踹飞的画面"
# This is the last line we want to replace
# We replace from "第6章 地下邀请" to that line (inclusive)

# Build old text (from start of ch6 to the "他闭上眼睛" line)
old_lines = []
end_idx = None
for i, line in enumerate(ch6_lines):
    old_lines.append(line)
    if u"他闭上眼睛，脑海里闪过白天赵明被他一脚踹飞的画面" in line:
        end_idx = i
        break

if end_idx is None:
    print("ERROR: Could not find end marker")
    exit(1)

old_text = "\n".join(old_lines)
print("Old text length:", len(old_text))

# New text
new_text = u"""第6章 地下邀请

9月5日，白天的江海大学笼罩在一种诡异的平静里。

昨天的兽袭事件已经在校园里传开了——官方说法是"灵气波动引发的偶发性灵气兽暴走"，已经被校方觉醒者社团处理完毕，提醒学生不必恐慌。林逸坐在教室最后一排，听着讲台上教授讲着《灵气复苏导论》的绪论课，心思却完全不在课本上。

那股监视感，从凌晨开始就一直没断过。

白天换了三节课、去了两次食堂、去图书馆借了一本《基础灵力感知》，始终有一道若有若无的视线跟在他身上。他试过几次突然回头，或是绕路走偏僻的小道，但都找不到监视者的踪影。那人对校园地形的熟悉程度远超常人，每次都能在他转身的瞬间消失在视野盲区。

更让他不安的是，觉醒者社团的人没有出现。

昨天王老师说"明天会有人来找你谈话"，可整整一天过去了，没有任何人主动接触他。这种沉默反而比直接找上门更让人心慌——像是猎人把弓拉满，却迟迟不肯放箭。

下午四点，林逸从图书馆出来时，在门口遇到了李伟。李伟神色古怪地凑过来，压低声音说："逸哥，今天中午食堂有人打听你。一个穿黑色夹克的家伙，问你住哪个宿舍、平时都跟谁来往。我问他是谁，他说是校报的，要采访兽袭事件。但哪有校报的人穿那种衣服？"

林逸心里一沉，面上却不动声色："嗯，我知道了。以后有人问我的事，你就说不知道。"

李伟点头应下，走的时候还回头看了他一眼，欲言又止。

林逸站在图书馆台阶上，望着校园里三三两两走过的学生，指尖不自觉地攥紧了书包带。看来对方不只是监视，还开始摸他的底了。

晚上九点，宿舍楼303室。

室友们已经陆续回来了——李伟在下面洗漱间洗衣服，另外两个室友在打手游。林逸靠在床头，手里捧着一本《基础灵力感知》，目光落在书页边缘，一个字都没看进去。

昨天操场上的兽袭、王老师意味深长的警告、凌晨钟楼上那道一闪而过的黑影、今天一整天如影随形的监视——这些事情在脑海里盘成一团乱麻，怎么也理不出头绪。他原本只想低调地度过大学四年，搞清楚自己觉醒的真相，但现在看来，对方根本不打算给他低调的机会。

手机屏幕突然亮了一下。

林逸下意识地瞄了一眼——不是什么锁屏通知，而是QQ上一个陌生头像跳出来的消息。头像是一片纯黑色，昵称只有一个字：影。好友添加时间是两分钟前，没有任何共同群聊或好友介绍。

他皱了皱眉，没有立刻点开。这几天骚扰消息太多了，大多数是来打听兽袭事件的，还有一些是社团拉人的。但不知道为什么，这个昵称让他心里莫名一紧——凌晨监视他的人，是否也和这个"影"有关？

他刚想翻过手机，又一条消息进来了。

这次是一条语音。

林逸犹豫了几秒，还是点开了。

一个低沉而平稳的男声从听筒中传出："林逸同学，我知道你今天过得不太安宁。被盯上的滋味不好受吧？我能帮你。"

林逸的手指猛地一顿。

他迅速扫了一眼消息发送者的信息——没错，头像纯黑，昵称"影"，没有任何备注。最关键的是，对方说"今天"过得不太安宁，而不是"昨天下午遇到了麻烦"——这说明对方知道的是今天这一整天的监视情况，而不是昨天操场上的事。

这个人，要么就是监视者本人，要么和监视者是同一伙人。

他放下手机，脑子里飞速运转。

帮？帮什么？怎么帮？对方到底想从他身上得到什么？

他重新拿起手机，打了几个字："你是谁？"

对方几乎秒回："一个想帮你的人。或者换个说法——一个能给你机会的人。"

林逸皱眉，回道："我不需要什么机会。"

"你需要。"第三条消息附着一条链接，标题是一串乱码，但预览内容里赫然写着几个字——"暗夜竞技场邀请函"。

林逸瞳孔微缩。

暗夜竞技场？他搜索过校内论坛，在那些被删掉的帖子中，隐约看到过这个词。据说那是江海市地下黑拳赛的别称，能参加的人都是觉醒者或者武道修炼者，里面打的每一场，都是生死之战。

他犹豫了几秒，最终还是点开了链接。

屏幕上立刻弹出一个极简风格的页面——黑底白字，中央只有几行字：

"欢迎，觉醒者。

江海大学-林逸同学，经核实，你已具备E级觉醒者资质。

暗夜竞技场现向你发出邀请。

首战获胜奖励：灵气丹x1（可提升灵力纯度，加速突破至D级）。

若拒绝，本邀请将在24小时后自动作废。"

下面还有一个闪烁的"接受"按钮。

林逸的手指悬停在屏幕上方。

他知道，这是一个陷阱。任何组织能通过校园网络精准定位到他，还知道他是觉醒者，这本身就已经说明对方的能量远超常人。更别提那个"灵气丹"——这种丹药他只在网上看到过，据说一颗就价值数万，根本不是普通大学生能接触到的。

但诱惑也是实打实的。

他现在的灵力纯度只有E级低阶，距离突破D级至少要三个月苦修。而一旦进入D级，很多原本对他紧闭的修炼资源就会打开，包括那些需要灵力门槛才能学习的武技。更重要的是，觉醒者社团今天虽然没来找他，但那只是暴风雨前的宁静——等他们摸清了他的底细，所谓"谈话"恐怕就不会这么客气了。

他需要变强。

他必须变强。

那个藏在暗处的"影"似乎看穿了他的犹豫，又发来一条消息："别急着做决定。但我提醒你一点——如果你拒绝，今天中午在食堂打听你住处的那个人，明天可能就会换一种方式出现在你面前。你确定你准备好了？"

林逸的心猛地一沉。

今天中午食堂的事，除了他和李伟，没有第三个人知道。对方竟然连这种细节都掌握——这意味着监视者不只是远观，很可能已经渗透到了他的生活圈里。

他深吸一口气，盯着屏幕上的"接受"按钮，拇指悬在空中。宿舍里很安静，隔壁宿舍的键盘敲击声和楼下空调外机的嗡鸣混在一起，窗外的路灯把昏黄的光投在地板上。

他闭上眼睛，脑海里闪过昨天操场上一拳打退灵气兽的画面，闪过王老师意味深长的眼神，闪过今天一整天那道如影随形的视线。然后，他睁开眼睛，手指狠狠按了下去。"""

# Replace in ch6
new_ch6 = ch6.replace(old_text, new_text)
chapters_dict[6] = new_ch6

# Rebuild full txt
sorted_chapters = []
for idx in sorted(chapters_dict.keys()):
    sorted_chapters.append(chapters_dict[idx])

new_txt = "\n\n\n".join(sorted_chapters)
with open(txt_file, "w", encoding="utf-8") as f:
    f.write(new_txt + "\n")

# Verify word count
body_text = "\n".join(new_ch6.split("\n")[1:]).strip()
words = len(re.sub(r"\s", "", body_text))
print("Chapter 6:", words, "words")
print("STATUS:", "OK" if 2200 <= words <= 3200 else "NEEDS FIX ({})".format(words))

# Sync JSON
with open(json_file, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

for ch in data.get("chapters", []):
    if ch.get("index") == 6:
        ch["content"] = body_text
        print("JSON Ch6 updated")
        break

with open(json_file, "w", encoding="utf-8") as f:
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
print("Done")
