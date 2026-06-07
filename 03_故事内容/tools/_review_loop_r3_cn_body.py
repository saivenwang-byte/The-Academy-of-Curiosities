#!/usr/bin/env python3
"""REVIEW LOOP Round 3 — move production header to foot; A001 waveform; A002 membrane trim."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

FILES = [
    "案01_全班都听见了他的声音_HybridVoice_V2.0.txt",
    "案02_没有人写过的道歉_HybridVoice_V2.0.txt",
    "案03_每个人都记得的海报_HybridVoice_V2.0.txt",
    "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt",
    "案05_午休后消失的影子_HybridVoice_V2.0.txt",
]

NARRATIVE_START = re.compile(r"\n(序 ·|一、|二、|三、|四、|五、)")


def move_header_to_foot(text: str, case_id: str) -> str:
    marker = "【正式版 · Hybrid Voice"
    if marker not in text:
        return text
    prod_start = text.index(marker)
    tail = text[prod_start:]
    nav = NARRATIVE_START.search(tail)
    if not nav:
        return text
    narrative_start = prod_start + nav.start() + 1  # skip leading newline
    prod_block = text[prod_start:narrative_start].strip()
    sep_end = text.rfind("========================\n\n", 0, prod_start) + len("========================\n\n")
    new_text = text[:sep_end] + text[narrative_start:]
    prod = prod_block
    foot = (
        f"\n\n---\n\n【EDITOR · PRODUCTION META · {case_id} · foot · R3 2026-06-08】\n"
        f"{prod.replace('【正式版 · Hybrid Voice', '【Hybrid Voice')}\n"
        f"· 状态：REVIEW_LOOP_R3 · Hybrid Voice v3 · reader-flow 2026-06-08\n"
    )
    new_text = new_text.replace(
        "【EDITOR · REVIEW_LOOP R2 · 2026-06-08】",
        "【EDITOR · REVIEW_LOOP R3 · 2026-06-08】",
    )
    if "【EDITOR · REVIEW_LOOP R3" not in new_text:
        anchor = "\n\n---\n\n【V2.0 场级对照"
        if anchor in new_text:
            note = (
                f"\n\n---\n\n【EDITOR · REVIEW_LOOP R3 · 2026-06-08】\n"
                f"叙事层 production 头已移 foot · {case_id}\n"
            )
            new_text = new_text.replace(anchor, note + anchor)
    anchor = "\n\n---\n\n【V2.0 场级对照"
    if anchor in new_text:
        new_text = new_text.replace(anchor, foot + anchor)
    else:
        new_text = new_text.rstrip() + foot
    return new_text


def polish_a001_waveform(text: str) -> str:
    text = text.replace(
        "平板屏幕上有十七段音频。文件名乱得像把一盒字母倒在桌上。志郎从车后爬出来：「这不是文件夹。这是求救信号。」",
        "平板屏幕上有十七段录音。名字乱得像把一盒字母倒在桌上。志郎从车后爬出来：「不是文件夹——像谁在喊救命。」",
    )
    if "像被剪刀剪过，上一段" not in text:
        text = text.replace(
            "志郎把波形放大。在「不该参加」前面，有一刀硬切 —— 上一段尾巴断在奇怪的位置，下一段突然起振。",
            "志郎把波形放大。在「不该参加」前面，有一刀硬切 —— 像被剪刀剪过，上一段尾巴断在奇怪的位置，下一段突然起振。",
        )
    return text


def trim_a002_membrane(text: str) -> str:
    old = (
        "他们把透明展示膜拿出来，对着窗户。膜上的白色字是为了从背后投影到舞台，因此印刷时左右相反。黑板上浮出的字，也左右相反。\n\n\n"
        "志郎用备课本对照：他在本上写「对不起」，用膜压印再湿擦 —— 备课本上的字淡灰浮出，和板上同形。"
    )
    new = (
        "志郎把膜对着窗。膜背面的字是反的——湿擦后，粉笔灰停在边缘，字就「浮」出来了。\n\n"
        "他在备课本上试：写「对不起」，压膜，湿擦——淡灰浮出，和板上同形。"
    )
    if old in text:
        text = text.replace(old, new)
    text = text.replace(
        "窗缝的光移了一寸。板槽里那条膜边又亮了一下——像 FC-1 在等人来看。",
        "窗缝的光移了一寸。板槽里那条膜边又亮了一下——像在等人来看。",
    )
    return text


def process_file(name: str) -> tuple[str, dict]:
    path = BODY / name
    text = path.read_text(encoding="utf-8")
    case = f"A00{name[2]}"
    stats = {"before": len(text)}

    text = move_header_to_foot(text, case)
    if case == "A001":
        text = polish_a001_waveform(text)
    elif case == "A002":
        text = trim_a002_membrane(text)

    text = re.sub(r"\n{4,}", "\n\n\n", text)
    stats["after"] = len(text)
    stats["delta"] = stats["after"] - stats["before"]
    path.write_text(text, encoding="utf-8")
    return name, stats


def main() -> None:
    for name in FILES:
        n, stats = process_file(name)
        print(f"{n}: {stats['before']} -> {stats['after']} ({stats['delta']:+d})")


if __name__ == "__main__":
    main()
