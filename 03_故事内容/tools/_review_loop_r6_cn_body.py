#!/usr/bin/env python3
"""REVIEW LOOP Round 6 — FC strip, A004 expand, reader-flow (post-R5 baseline)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A002 = BODY / "案02_没有人写过的道歉_HybridVoice_V2.0.txt"
A003 = BODY / "案03_每个人都记得的海报_HybridVoice_V2.0.txt"
A004 = BODY / "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt"
A005 = BODY / "案05_午休后消失的影子_HybridVoice_V2.0.txt"


def strip_fc_inline(text: str) -> str:
    return re.sub(r"【FC-\d+[^】]*】", "", text)


def polish_a002(text: str) -> str:
    text = strip_fc_inline(text)
    text = text.replace(
        "【FC-1 回响】口述 **又开始分叉** —— 像案③ **提前** 在壁报栏 **排练**。",
        "口述又开始分叉——像上一案壁报栏提前在排练。",
    )
    return text


def polish_a003(text: str) -> str:
    # Reader jump: shorten floor inventory list
    old = (
        "他们把媒体器材车上的所有视觉材料摊在空教室地板上：红色标题条「不得参加」、水野的排练照片、蓝色箭头、黄色便签「公开日节目调整中」、安全说明「未佩戴名牌者不得参加器材搬运」、一张空白海报底纸、四枚圆形磁铁。\n\n\n"
        "每一件都真实存在。**没有一件单独构成「水野不得参加公开日展示」。**"
    )
    new = (
        "他们把器材车上的材料摊在空教室地板上：红标题条、水野排练照、蓝箭头、便签、安全说明、空白底纸、四枚磁铁——"
        "每一件都真实存在，却没有一件单独构成「水野不得参加展示」。"
    )
    if old in text:
        text = text.replace(old, new)
    text = text.replace("案①", "上一案")
    text = text.replace("案②", "上一案")
    return text


def polish_a004(text: str) -> str:
    text = strip_fc_inline(text)
    text = text.replace(
        "他轻敲柜顶五下 —— 标签跳进缝半寸。【FC-3 预演】",
        "他轻敲柜顶五下——标签跳进缝半寸，像预演了一次振动。",
    )

    # Restore reader-friendly beat trimmed in R4 (length + mechanism clarity)
    insert_after = "志郎建立复现实验。他在上层分别放入厚橡皮、纸片、金属徽章、塑料名牌、小钥匙、录音卡。"
    addition = (
        "先让全班记：厚橡皮不动，纸片只挪一点——"
        "轻的东西才听地板的话。"
    )
    if insert_after in text and addition not in text:
        text = text.replace(
            insert_after,
            insert_after + addition,
        )

    # Expand 水野藏卡 moment (reader empathy, not production meta)
    old_hide = "水野闭了闭眼：「卡滑进来的时候，我吓到了。我藏起来……怕大家又播。」"
    new_hide = (
        "水野闭了闭眼：「卡滑进来的时候，我吓到了。」\n\n\n"
        "她没看抽屉，只看自己的手——像那三秒哭声还贴在指尖。\n\n\n"
        "「我藏起来……怕大家又播。」"
    )
    if old_hide in text:
        text = text.replace(old_hide, new_hide)

    text = text.replace("案③", "上一案")
    text = text.replace("案②", "上一案")
    text = text.replace("案①", "上一案")
    return text


def polish_a005(text: str) -> str:
    text = strip_fc_inline(text)
    text = text.replace(
        "第四次，对照：同一地点单次快门 —— 五人皆有影。【FC-4 再验】",
        "第四次对照：同一地点单次快门——五人皆有影。",
    )
    text = text.replace("案④", "上一案")
    return text


def main() -> None:
    for path, fn in [
        (A002, polish_a002),
        (A003, polish_a003),
        (A004, polish_a004),
        (A005, polish_a005),
    ]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R6 polished {path.name}")
        else:
            print(f"No change {path.name}")


if __name__ == "__main__":
    main()
