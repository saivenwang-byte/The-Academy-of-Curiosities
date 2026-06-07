#!/usr/bin/env python3
"""REVIEW LOOP Round 5 — targeted CN polish A002/A004 + P0 jump-read trim."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A002 = BODY / "案02_没有人写过的道歉_HybridVoice_V2.0.txt"
A004 = BODY / "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt"
A005 = BODY / "案05_午休后消失的影子_HybridVoice_V2.0.txt"


def polish_a002(text: str) -> str:
    # Remove duplicate 光后排 passage (R4 missed second instance)
    dup_light = (
        "光从后排经过，停了一下。他没接话 —— 案①里，他也写过书面说明。\n\n\n"
    )
    if dup_light in text:
        text = text.replace(dup_light, "")

    # Soften dense 案① callbacks → reader-flow
    subs = [
        ("像案①里「听见」和「看见」 自动接在一起。", "像上一案里「听见」和「看见」自动接在一起。"),
        ("时间线像案①：先有「像他」，后有「不可能刚写」。", "时间线一样：先有「像他」，后有「不可能刚写」。"),
        ("陸珣站在侧窗。他想起案①里屏幕上的 PLAY。", "陸珣站在侧窗。他想起上一案屏幕上的 PLAY。"),
    ]
    for old, new in subs:
        text = text.replace(old, new)

    # Trim 瑆笔记 home-lab echo (repeats narrative membrane beat)
    old_kei = (
        "今天我在家 **试** 了哥哥的实验。\n\n\n"
        "透明膜 湿擦后撒粉—— 字回来了。\n\n\n"
        "没有人写。是板和膜记得。\n\n\n"
        "哥哥说，  \n"
        "出现≠刚写。\n\n\n"
        "我觉得，  \n"
        "大家 看见对不起三个字，  \n"
        "就 以为对不起三个人——\n\n\n"
        "志郎 、观察社、公开日——都该低头。\n\n\n"
    )
    new_kei = (
        "今天我在家试了哥哥的实验——膜湿擦后撒粉，字会回来。没有人写，是板和膜记得。\n\n\n"
    )
    if old_kei in text:
        text = text.replace(old_kei, new_kei)

    # Collapse duplicate 慧美格子 write
    dup_grid = (
        "慧美 只在格子写：机制可复现·握笔仍不符·动机=未登记。不写「不是他」三字——写「不像他」和「他未登记」。\n\n\n"
        "慧美只在 **已确认** 写：字迹可随清洁再现 · 非新写 · 与握笔角度仍不符。\n\n\n"
    )
    if dup_grid in text:
        text = text.replace(
            dup_grid,
            "慧美只在 **已确认** 写：机制可复现 · 非新写 · 握笔仍不符 · 未登记。\n\n\n",
        )

    return text


def polish_a004(text: str) -> str:
    # Trim 瑆 tail duplicate thief framing
    old = (
        "我觉得，大家 **先** 定了她是小偷，\n\n"
        "才后去打开抽屉找证据。\n\n\n"
    )
    if old in text:
        text = text.replace(old, "")

    # Reduce cross-case label density in narrative
    text = text.replace(
        "有人仍只记住「对不起」两个字——像案②黑板上那三个字的回声。",
        "有人仍只记住「对不起」两个字——像上一案黑板上那三个字的回声。",
    )
    return text


def polish_a005(text: str) -> str:
    # Strip production jump-read label from reader body
    text = text.replace(
        "**wrong_responsibility 峰值**：水野/观察社用怪事破坏公开日。\n\n\n",
        "全班把五案串成一条链：水野和观察社用怪事破坏公开日。\n\n\n",
    )
    return text


def main() -> None:
    for path, fn in [
        (A002, polish_a002),
        (A004, polish_a004),
        (A005, polish_a005),
    ]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R5 polished {path.name}")
        else:
            print(f"No change {path.name}")


if __name__ == "__main__":
    main()
