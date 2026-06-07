#!/usr/bin/env python3
"""REVIEW LOOP Round 2 — strip SC/FC headers from CN_BODY narrative flow."""

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


def strip_fc_tags(text: str) -> str:
    text = re.sub(r"【FC-\d+(?:\s+再强调|回响|预演|再验)?】\s*", "", text)
    text = re.sub(r"【EXPERT_LOCK】\s*", "", text)
    return text


def strip_sc_headers(text: str) -> str:
    # Remove ### SC-XX · title and ### SC-XX 续 · title lines
    text = re.sub(r"^### SC-\d+(?:\s+续)?\s*·[^\n]*\n+", "", text, flags=re.MULTILINE)
    return text


def friendly_rehearsal(text: str) -> str:
    text = text.replace("PLAY · `rehearsal_0328.wav`", "PLAY · 三周前彩排录音")
    text = text.replace("`rehearsal_0328.wav`", "三周前彩排录音")
    text = text.replace("rehearsal_0328", "三周前彩排")
    text = text.replace("**2026-03-28** · 三周前彩排录音", "三月二十八日 · 三周前彩排录音")
    return text


def readerize_metadata(text: str, case: str) -> str:
    replacements = [
        (r"陸珣要的是 metadata，不是谣言。", "陸珣要的是照片里的时间记录，不是谣言。"),
        (r"年级主任也来看 metadata。", "年级主任也来看拍摄信息。"),
        (r"志郎指 metadata：", "志郎指拍摄信息："),
        (r"陸珣\s+用投影讲metadata：", "陸珣用投影讲拍摄信息："),
        (r"水野没驳。只等metadata。", "水野没驳。只等拍摄信息。"),
        (r"没有一个节点看过 metadata。", "没有一个节点看过拍摄信息。"),
        (r"大屏投屏前，没人读metadata。", "大屏投屏前，没人读拍摄信息。"),
        (r"案⑤ metadata", "案⑤ 拍摄信息"),
        (r"FC-2 分段曝光metadata", "FC-2 分段曝光拍摄信息"),
        (r"SC-05 metadata时间线", "SC-05 拍摄信息时间线"),
        (r"SC-05 续 · metadata课", "SC-05 续 · 拍摄信息课"),
        (r"案① 时间戳 · 案② 膜边 · 案③ 空白底纸 · 案④ 倾斜水泡 · 案⑤ metadata",
         "案① 时间戳 · 案② 膜边 · 案③ 空白底纸 · 案④ 倾斜水泡 · 案⑤ 拍摄信息"),
        (r"还记得先看时间、板槽、空白、倾斜、metadata", "还记得先看时间、板槽、空白、倾斜、拍摄信息"),
    ]
    for pat, repl in replacements:
        text = re.sub(pat, repl, text)
    text = re.sub(r"\bmetadata\b", "拍摄信息", text)
    return text


def compress_a002_membrane(text: str) -> str:
    # Remove duplicate mid-case membrane explanation block in SC-05 area
    old = (
        "清洁液中的表面活性成分，加上展示膜背面残留的离型剂，在黑板上留下肉眼看不见的亲水差异。"
        "湿擦以后，水膜在不同区域干燥速度不同；粉笔灰又更容易停留在边缘，于是原本看不见的字形被重新「显」了出来。"
    )
    new = (
        "清洁液和膜背面的离型剂，在黑板上留下肉眼看不见的差异。"
        "湿擦后，粉笔灰更容易停在边缘——字不是新写的，是被「显」出来的。"
    )
    text = text.replace(old, new)
    # Trim one duplicate broadcast reference in SC-02 area
    text = text.replace(
        "「展示膜那事，广播设备也是他查的线——」\n\n\n\n",
        "",
    )
    return text


def trim_a004_tail(text: str) -> str:
    """Remove 续 padding blocks after SC-09 tail hook."""
    close = "\n\n（案④ 收束"
    hook = "水野没跑。她看自己的鞋尖—— 像案①里听广播却开不了口的同一种累。"
    if hook in text and close in text:
        head = text.split(hook, 1)[0] + hook
        tail = text.split(close, 1)[1]
        text = head + close + tail
    return text


def trim_a005_tail(text: str) -> str:
    """Keep main narrative through SC-10; drop 续 padding."""
    marker = "\n\n\n\n---\n\n\n\n### SC-02 续 · 八秒链"
    alt = "\n\n\n\n### SC-02 续 · 八秒链"
    for m in (marker, alt):
        if m in text:
            head, _ = text.split(m, 1)
            close = "\n\n（案⑤ 收束"
            if close in text:
                tail = text.split(close, 1)[1]
                text = head + "\n\n\n\n" + close + tail
            break
    return text


def trim_a003_xu(text: str) -> str:
    """Remove excessive 续 sections after main SC-09."""
    marker = "\n\n\n\n### SC-07 续 · 佐佐木之后"
    if marker in text:
        head, _ = text.split(marker, 1)
        close = "\n\n（案③ 收束"
        if close in text:
            tail = text.split(close, 1)[1]
            text = head + close + tail
        else:
            # fallback: cut at P06 block
            p06 = "\n\n---\n\n【读者可以试"
            if p06 in text:
                idx = text.index(p06)
                text = head + text[idx:]
    return text


def trim_a002_xu(text: str) -> str:
    marker = "\n\n\n\n### SC-08 续 · 流程课"
    if marker in text:
        head, _ = text.split(marker, 1)
        close = "\n\n（案② 收束"
        if close in text:
            tail = text.split(close, 1)[1]
            text = head + close + tail
    return text


def update_status_line(text: str) -> str:
    text = re.sub(
        r"· 状态：G-CN_PATCHED · LOCK aligned · Hybrid Voice v3 · voice-normalized 2026-06-08",
        "· 状态：REVIEW_LOOP_R2 · Hybrid Voice v3 · reader-flow 2026-06-08",
        text,
    )
    return text


def add_r2_footnote(text: str, case_id: str) -> str:
    note = (
        f"\n\n---\n\n【EDITOR · REVIEW_LOOP R2 · 2026-06-08】\n"
        f"叙事层已 strip SC/FC 场头 · 场级对照见上方 G-SHOT-T 块 · {case_id}\n"
    )
    if "【EDITOR · REVIEW_LOOP R2" not in text:
        # Insert before final --- editor blocks at end if present
        anchor = "\n\n---\n\n【V2.0 场级对照"
        if anchor in text:
            text = text.replace(anchor, note + anchor)
    return text


def process_file(name: str) -> tuple[str, dict]:
    path = BODY / name
    text = path.read_text(encoding="utf-8")
    case = f"A00{name[2]}"
    stats = {"before": len(text)}

    text = strip_sc_headers(text)
    text = strip_fc_tags(text)
    text = friendly_rehearsal(text)
    text = readerize_metadata(text, case)

    if case == "A002":
        text = compress_a002_membrane(text)
        text = trim_a002_xu(text)
    elif case == "A003":
        text = trim_a003_xu(text)
    elif case == "A004":
        text = trim_a004_tail(text)
    elif case == "A005":
        text = trim_a005_tail(text)

    text = update_status_line(text)
    text = add_r2_footnote(text, case)

    # Collapse excessive blank lines (max 2)
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
