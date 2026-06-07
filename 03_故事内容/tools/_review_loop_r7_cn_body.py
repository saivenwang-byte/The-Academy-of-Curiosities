#!/usr/bin/env python3
"""REVIEW LOOP Round 7 — A001 reader gloss + A004 length restore."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A001 = BODY / "案01_全班都听见了他的声音_HybridVoice_V2.0.txt"
A004 = BODY / "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt"


def polish_a001(text: str) -> str:
    text = text.replace(
        "PLAY · 三周前彩排录音",
        "PLAY · 三周前彩排录音（像提前录好的带子）",
    )
    text = text.replace("rehearsal_0328", "三周前彩排录音")
    text = text.replace("rehearsal_0328.wav", "三周前彩排录音")
    return text


def polish_a004(text: str) -> str:
    # Restore mechanism clarity trimmed in R4 (reader-friendly, no production labels)
    old = (
        "全班已经连好故事：水野偷物资 · 观察社又要帮她说话。\n\n\n"
        "有人把案③海报和案④抽屉接在一起：「她早就被排斥了。」"
    )
    new = (
        "全班已经连好故事：水野偷物资 · 观察社又要帮她说话。\n\n\n"
        "机制还没当众讲完，误会已经连成了链。\n\n\n"
        "有人把上一案海报和这一案抽屉接在一起：「她早就被排斥了，偷东西是报应。」"
    )
    if old in text:
        text = text.replace(old, new)

    # Sensory beat at seal moment
    old2 = "封条没断。锁孔没新痕。最下一排 **第三格** 抽屉，半开着。"
    new2 = (
        "封条没断。锁孔没新痕。\n\n\n"
        "最下一排第三格抽屉半开着——像有人从后面推了一把，不是从前开锁。"
    )
    if old2 in text:
        text = text.replace(old2, new2)

    text = text.replace("案③", "上一案")
    text = text.replace("案②", "上一案")
    text = text.replace("案①", "上一案")
    text = text.replace("案④", "这一案")
    return text


def main() -> None:
    for path, fn in [(A001, polish_a001), (A004, polish_a004)]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R7 polished {path.name}")
        else:
            print(f"No change {path.name}")


if __name__ == "__main__":
    main()
