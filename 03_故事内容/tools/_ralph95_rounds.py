#!/usr/bin/env python3
"""Ralph 9.5 target — REVIEW LOOP rounds R10–R14 (iter 8–12)."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A001 = BODY / "案01_全班都听见了他的声音_HybridVoice_V2.0.txt"
A002 = BODY / "案02_没有人写过的道歉_HybridVoice_V2.0.txt"
A003 = BODY / "案03_每个人都记得的海报_HybridVoice_V2.0.txt"
A004 = BODY / "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt"
A005 = BODY / "案05_午休后消失的影子_HybridVoice_V2.0.txt"


def r10_a002_fc_strip(text: str) -> str:
    text = text.replace(
        "四月上午的光移动很快。一分钟前膜边不亮，现在亮—— 像FC-1在等角度。",
        "四月上午的光移动很快。一分钟前膜边不亮，现在亮——像在等人来看。",
    )
    return text


def r11_a002_membrane_compress(text: str) -> str:
    old = """志郎把样品袋摊在窗台上。里面多了一小瓶 **清洁液**，标签还是昨天那卷膜的配套。


「不是写字。」志郎说，「是 **膜** 留下的。」


他在备课本空白页写字，撕下一条透明膜贴上，再按公开日流程 **湿擦**。字没了。


全班围近一步。有人屏住呼吸，像怕呼吸也会写字。


他又点一点清洁液，等板面潮了一寸，粉尘蹭过膜边——备课本上的字，淡灰地浮回来。


「再看板槽。」志郎把黑板侧对窗。斜光里，膜边像一条未撕净的线。


「膜边和板槽，」志郎指给慧美看，「昨天没撕净。湿擦把粉打进去了。清洁液一干，旧痕再显。」


清洁液和膜背面的离型剂，在黑板上留下肉眼看不见的差异。湿擦后，粉笔灰更容易停在边缘——字不是新写的，是被「显」出来的。"""
    new = """志郎把样品袋摊在窗台上，取出配套清洁液。


「不是写字。」他说，「是膜留下的。」


备课本上一试：压膜、湿擦，字没了；点一点清洁液，旧痕又浮出。


「膜边昨天没撕净。」志郎指板槽，「湿擦把粉打进去。清洁液一干，旧痕再显——字不是新写的，是被显出来的。」"""
    if old in text:
        text = text.replace(old, new)
    return text


def r12_a003_trim(text: str) -> str:
    old = """采访表贴出后，侧廊静了半分钟。半分钟里，有人第一次问：「所以……海报到底有没有？」


慧美指空白底纸：「完整的，没有。碎片，有。记忆把碎片拼满了空白。」


年级老师收回权限后，观察社仍可以写「仍不知道」——那三张小标识变成全单元的规矩预告。


陸珣在本画：空白·三版·无实体×3——案③的公平线索不是找到海报，是找不到同一张。


排练备份卡角上「勿播」两字，像上一案禁声回执——都是「今天不能出声」的另一种。


慧美沉默，因为一开口就要在「保护隐私」和「像删稿」之间选——她选了先不说。错在沉默太久，不在删完整海报。


光帮她补一句：「完整海报没有——这句要早说。」


放学前说明会，九份采访表贴满半面墙。有人仍说：「我就是记得。」慧美答：「记得可以。但别用记得判人。」


三次核对无实体写在红铅笔圈里：打印无·正式照无·残胶无。"""
    new = """采访表贴出后，侧廊静了半分钟。有人问：「所以……海报到底有没有？」


慧美指空白底纸：「完整的，没有。碎片，有。记忆把碎片拼满了空白。」


陸珣在本子画：空白·三版·无实体——公平线索不是找到海报，是找不到同一张。


光补一句：「完整海报没有——这句要早说。」"""
    if old in text:
        text = text.replace(old, new)
    return text


def r13_a005_gloss(text: str) -> str:
    replacements = [
        ("repair_action 分三步当众做：", "修复分三步当众做："),
        (
            "陸珣把五案记录夹摊在折叠桌：案① 时间戳 · 案② 膜边 · 案③ 空白底纸 · 上一案 倾斜水泡 · 案⑤ 拍摄信息 —— 像五枚不同的钉。",
            "陸珣把五案记录夹摊在折叠桌：时间戳、膜边、空白底纸、倾斜水泡、拍摄信息——像五枚不同的钉。",
        ),
        (
            "repair_action：全班重拍 · 慧美四栏壁报 · 水野名字并列写回 · 五案机制并列不串成阴谋。",
            "修复动作：全班重拍，慧美四栏壁报，水野名字并列写回，五案机制并列不串成阴谋。",
        ),
    ]
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    return text


def r14_a001_a004_polish(text: str, case: str) -> str:
    if case == "A001":
        old = "名字乱得像把一盒字母倒在桌上。志郎从车后爬出来：「不是文件夹——像谁在喊救命。」"
        new = "名字乱得像把一盒字母倒在桌上。志郎从车后爬出来：「不是文件夹——像谁在喊救命。」"
        # tighten waveform explanation
        old2 = "两段波峰像同一把剪刀剪出来的。「重复了。」志郎说，「不是人刚好吸得一样，是同一小段被用了两次。」"
        new2 = "两段波峰像同一把剪刀剪出来的。「重复了。」志郎说，「不是人刚好吸得一样——是同一段录音被用了两次。」"
        if old2 in text:
            text = text.replace(old2, new2)
    if case == "A004":
        old = "志郎把水平仪搁在柜顶。水泡 **偏了一格**。"
        new = "志郎把水平仪搁在柜顶。水泡 **偏了一格**——柜顶向抽屉一侧斜了。"
        if old in text:
            text = text.replace(old, new)
    return text


ROUNDS = {
    10: [(A002, r10_a002_fc_strip, "A002 FC-1 narrative strip")],
    11: [(A002, r11_a002_membrane_compress, "A002 membrane compress")],
    12: [(A003, r12_a003_trim, "A003 post-repair trim")],
    13: [(A005, r13_a005_gloss, "A005 production gloss")],
    14: [
        (A001, lambda t: r14_a001_a004_polish(t, "A001"), "A001 waveform gloss"),
        (A004, lambda t: r14_a001_a004_polish(t, "A004"), "A004 tilt clarity"),
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("round", type=int, choices=sorted(ROUNDS.keys()))
    args = parser.parse_args()
    changed = 0
    for path, fn, label in ROUNDS[args.round]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R{args.round} {label}: {path.name}")
            changed += 1
        else:
            print(f"R{args.round} no change: {path.name}")
    print(f"round {args.round}: {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
