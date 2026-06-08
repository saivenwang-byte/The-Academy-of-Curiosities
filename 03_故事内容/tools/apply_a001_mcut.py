#!/usr/bin/env python3
"""Apply M-cut1-5 per doc77 to A001 R17 → HybridVoice_V2.1."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY_DIR = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"
SRC = BODY_DIR / "案01_全班都听见了他的声音_HybridVoice_V2.0.txt"
OUT = BODY_DIR / "案01_全班都听见了他的声音_HybridVoice_V2.1.txt"
META = BODY_DIR / "案01_全班都听见了他的声音_A001_制作元数据.md"
FAQ = BODY_DIR / "案01_全班都听见了他的声音_A001_卷末实验与FAQ.md"

text = SRC.read_text(encoding="utf-8")

# Split P06 appendix
p06_start = text.find("【读者可以试 · P06家庭实验】")
editor_start = text.find("【EDITOR · REVIEW_LOOP")
xing_start = text.find("瑆笔记 · 第二真相")

if p06_start < 0 or editor_start < 0:
    raise SystemExit("markers not found")

reader_main = text[:p06_start].rstrip()
p06_block = text[p06_start:xing_start].strip()
xing_block = text[xing_start:editor_start].strip()
meta_block = text[editor_start:].strip()

# M-cut3: remove L71 duplicate timestamp line
reader_main = reader_main.replace(
    "——这件事发生在两小时前。名古屋四月下旬，樱瓣落得比风慢。公開日準備。午後可能有小雨。\n\n\n",
    "",
)

# M-cut3: compress observation club L79-91
old_corner = """陸珣来5年2組第三周。侧廊尽头有个 **观察社角落** —— 旧笔记墙、证物盒、一块故意留空的壁报栏。木门上钉着社徽： **翘起的海报角**，中间一只简笔眼睛。慧美说，空白栏是给还没核实的事留的。


松本志郎正拿胶带「加固」社徽。贴完，角翘得更高。


「更牢了。」他满意点头。


加藤慧美把透明膜按回他手里：「还没登记。」


「更牢了也比掉地上强。」志郎又扯了一截胶带，社徽彻底歪向一边。慧美叹气，在本子上写：**听说** · 志郎说更牢了 · 未确认是否更牢。"""
new_corner = """陸珣来5年2組第三周。侧廊尽头是 **观察社角落** —— 旧笔记墙、证物盒、一块故意留空的壁报栏；社徽是 **翘起的海报角**，中间一只简笔眼睛。慧美说，空白栏是给还没核实的事留的。


松本志郎正拿胶带「加固」社徽。加藤慧美把透明膜按回他手里：「还没登记。」志郎又扯了一截，社徽歪向一边。慧美在本子上写：**听说** · 志郎说更牢了 · 未确认是否更牢。"""
reader_main = reader_main.replace(old_corner, new_corner)

# M-cut3: compress equipment cart tags L94-98
reader_main = reader_main.replace(
    "灰白色的 **移动媒体器材车** 停在侧门。车侧标签：录音卡 · 展示膜 · 班级合照备份。\n\n\n",
    "灰白色的 **移动媒体器材车** 停在侧门，侧栏标签朝外：录音卡 · 展示膜 · 班级合照备份。\n\n\n",
)

# M-cut3: delete Xing body insert L210-211
reader_main = reader_main.replace(
    "四年级走廊，陸瑆把观察社社徽描进日记本。翘角旁边，她画了一只圆眼睛。\n\n\n",
    "",
)

# M-cut2: compress L236-246
old_queue = """平板屏幕上有十七段录音。名字乱得像把一盒字母倒在桌上。志郎从车后爬出来：「不是文件夹——像谁在喊救命。」


水野把器材车从放送室推到五年二班，是因为公开日的班级展示要测试声音。她插上电源，旧平板自动连接了音箱。之后她去职员室拿审批表，广播就在无人操作的情况下响了。


志郎点开平板 **上次没播完的那一条**。屏幕左上角灰字：「继续上次 · 还剩 1 段」。


「自动接着播？」志郎蹲下检查插座，「平板一插电，有可能自己接着上次没播完的地方。」


慧美问水野：「你插电源时，屏幕亮了吗？」


水野声音很轻：「亮了一下。我以为在 **连接** ……就去拿表了。」"""
new_queue = """平板屏幕上有十七段录音。水野把器材车从放送室推到五年二班，插上电源，旧平板自动连接音箱；她去职员室拿审批表，广播就在无人操作的情况下响了。屏幕灰字：「继续上次 · 还剩 1 段」。


慧美问水野：「你插电源时，屏幕亮了吗？」


水野声音很轻：「亮了一下。我以为在 **连接** ……就去拿表了。」"""
reader_main = reader_main.replace(old_queue, new_queue)

# M-cut1: compress L258-261 scissors
old_wave = """志郎把波形放大。在「不该参加」前面，有一刀硬切 —— 像被剪刀剪过，上一段尾巴断在奇怪的位置，下一段突然起振。


两段波峰像同一把剪刀剪出来的。「重复了。」志郎说，「不是人刚好吸得一样——是同一段录音被用了两次。」"""
new_wave = """志郎把波形放大。在「不该参加」前面有一刀硬切——两段波峰一模一样。「重复了，」志郎说，「同一段录音被用了两次。」"""
reader_main = reader_main.replace(old_wave, new_wave)

# M-cut1: delete L294 scissors narration
reader_main = reader_main.replace(
    "前段尾巴落在「迟——」的「迟」上；后段从「不该参加」起振。中间没有呼吸，没有停顿，像被 **一把剪刀** 直接接在一起。\n\n\n",
    "",
)

# M-cut3: compress corridor rumors L327-331
old_rumor = """走廊外有人贴墙偷听，又跑开。消息比脚步快——慧美一句不漏，全记进 **听说** 栏：


「光在广播里骂水野。」


「光骂了水野一整节课。」


「光从开学第一天就看水野不顺眼。」


慧美笔尖一顿，把最后一条圈出来：「……我们才开学第三周。」"""
new_rumor = """走廊外有人贴墙偷听，又跑开。消息比脚步快——慧美一句不漏，全记进 **听说** 栏。有人添了一句：「光从开学第一天就看水野不顺眼。」慧美笔尖一顿，圈出来：「……我们才开学第三周。」"""
reader_main = reader_main.replace(old_rumor, new_rumor)

# M-cut2: compress backup chain L366-382
old_backup = """志郎接上学校的 **备份链**。完整排练文件里，句子是：


……**迟到者**不该参加 **今天的彩排**。


广播里播出的，却是中间一段，像被人 **掐头去尾**：


 ……（迟）……**不该参加**……


再加上口语误听、传播缩写，到了班里，变成了：


 「水野根本不该参加。」"""
new_backup = """志郎接上学校的 **备份链**。完整排练文件里：……**迟到者**不该参加 **今天的彩排**。广播里播出的，却是中间一段，像被人 **掐头去尾**：……（迟）……**不该参加**…… 再加上口语误听、传播缩写，到了班里，变成了：「水野根本不该参加。」"""
reader_main = reader_main.replace(old_backup, new_backup)

# M-cut3: merge classroom reaction L408-417
old_class = """志郎把完整句投在讲台小屏上。有人小声读出来：「迟到者不该参加 **今天的彩排**。」


「原来中间还有 **迟到者** ……」


「还有 **今天的彩排** ……」


两句话像从同一锅汤里捞出不同的料。教室里没有立刻安静——安静太像认输。但推回去的椅子比刚才多了两把。"""
new_class = """志郎把完整句投在讲台小屏上。有人小声读出来：「迟到者不该参加 **今天的彩排**。」教室里有人小声说：「原来中间还有 **迟到者** ……」推回去的椅子比刚才多了两把。"""
reader_main = reader_main.replace(old_class, new_class)

# M-cut1: delete L420-421, compress L422
old_summary = """**失声日** + 旧文件误触。两段话被剪短黏在一起。语境截断。

生理上说不出；录音上不是现场——两层不可能，不能混成一句审判词。"""
new_summary = """两层对不上，不能混成一句审判词。"""
reader_main = reader_main.replace(old_summary, new_summary)

# M-cut3: compress after school L446-467
old_after = """放学后，观察社三个人又围住陸珣。


「你为什么先看时间？」光问。


「声音已经有人听了。」陸珣说，「我再听一遍，也不会比全班多一双耳朵。」


「所以你看屏幕？」


「声音告诉我们像谁。时间告诉我们它能不能是现在发生的。」


慧美合上笔记本：「来观察社吧。」


「我刚转学。」


「观察不看入学天数。」光说，「而且我们现在缺一个会先看时间的人。」


陸珣没有立刻答应。他看向器材车。车顶那叠透明展示膜被风吹起一角。最上面一张印着白色的「对不起」，是公开日短剧要用的道具字样。志郎用手掌把它压平。谁也没有注意到，膜的背面在刚擦过的黑板边缘蹭了一下。"""
new_after = """放学后，观察社三个人又围住陸珣。


「你为什么先看时间？」光问。


「声音已经有人听了。」陸珣说，「时间告诉我们它能不能是现在发生的。」


慧美合上笔记本：「来观察社吧。观察不看入学天数——我们现在缺一个会先看时间的人。」


陸珣没有立刻答应。他看向器材车。车顶那叠透明展示膜被风吹起一角。最上面一张印着白色的「对不起」，是公开日短剧要用的道具字样。志郎用手掌把它压平。谁也没有注意到，膜的背面在刚擦过的黑板边缘蹭了一下。"""
reader_main = reader_main.replace(old_after, new_after)

# Assemble V2.1 body (no P06 in main, no EDITOR meta)
out_text = reader_main.rstrip() + "\n\n\n---\n\n\n" + xing_block.strip() + "\n"
OUT.write_text(out_text, encoding="utf-8")

# M-cut4: metadata sidecar
META.write_text(
    f"""# A001 · 制作元数据 · sidecar

> **基线正文**: HybridVoice_V2.1（R18 · M-cut1–5 from R17）  
> **移出自**: HybridVoice_V2.0.txt L543–582 · P06 附录

---

## P06 · 家庭实验（读者附录）

{p06_block}

---

## EDITOR · REVIEW_LOOP

{meta_block.split('---')[1].strip() if '---' in meta_block else ''}

---

{meta_block}
""",
    encoding="utf-8",
)

FAQ.write_text(
    f"""# A001 · 卷末实验与 FAQ

> 自 HybridVoice_V2.1 正文移出 · 不计入 6000 字天花板

{p06_block}
""",
    encoding="utf-8",
)

def measure(p: Path) -> tuple[int, int]:
    t = p.read_text(encoding="utf-8")
    i = t.find("【EDITOR")
    if i < 0:
        i = len(t)
    return len(t), len(t[:i])

before_full, before_reader = measure(SRC)
after_full, after_reader = measure(OUT)
print(f"R17 full={before_full} reader={before_reader}")
print(f"V2.1 full={after_full} reader={after_reader}")
print(f"delta reader={before_reader - after_reader}")
print(f"Wrote {OUT.name}")
