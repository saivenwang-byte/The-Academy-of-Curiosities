#!/usr/bin/env python3
"""REVIEW LOOP Round 8 — A005 reader gloss + A003/A002 final reader-flow."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A002 = BODY / "案02_没有人写过的道歉_HybridVoice_V2.0.txt"
A003 = BODY / "案03_每个人都记得的海报_HybridVoice_V2.0.txt"
A005 = BODY / "案05_午休后消失的影子_HybridVoice_V2.0.txt"


def polish_a002(text: str) -> str:
    text = text.replace("展示膜", "透明膜")
    return text


def polish_a003(text: str) -> str:
    old = (
        "「两秒像整张。」慧美轻声，「像不等于是。」\n\n\n"
        "她把空白底纸举高：「这张从未被贴满过。」"
    )
    new = "「两秒像整张。」慧美轻声，「像不等于是。」\n\n\n"
    if old in text:
        text = text.replace(old, new)
    return text


def polish_a005(text: str) -> str:
    subs = [
        ("metadata", "拍摄设置"),
        ("metadata三帧", "三帧拍摄设置"),
        ("全景模式", "全景拍摄"),
        ("wrong_responsibility", "误指"),
    ]
    for old, new in subs:
        text = text.replace(old, new)
    return text


def main() -> None:
    for path, fn in [(A002, polish_a002), (A003, polish_a003), (A005, polish_a005)]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R8 polished {path.name}")
        else:
            print(f"No change {path.name}")


if __name__ == "__main__":
    main()
