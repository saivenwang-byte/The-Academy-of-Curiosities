#!/usr/bin/env python3
"""REVIEW LOOP Round 9 — final narrative polish A003/A005 for expert lift."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A003 = BODY / "案03_每个人都记得的海报_HybridVoice_V2.0.txt"
A005 = BODY / "案05_午休后消失的影子_HybridVoice_V2.0.txt"


def polish_a003(text: str) -> str:
    old = "瑆：「记得有时候比看见更满 —— **满到把空白也填满了**」"
    new = "瑆：「记得有时候比看见更满——满到把空白也填满了。」"
    if old in text:
        text = text.replace(old, new)
    return text


def polish_a005(text: str) -> str:
    old = "陸珣把本子合上。案④最后一行：**振动 · 倾斜 · 藏卡**。"
    new = "陸珣把本子合上。上一案最后一行还写着：振动、倾斜、藏卡。"
    if old in text:
        text = text.replace(old, new)
    return text


def main() -> None:
    for path, fn in [(A003, polish_a003), (A005, polish_a005)]:
        raw = path.read_text(encoding="utf-8")
        out = fn(raw)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"R9 polished {path.name}")
        else:
            print(f"No change {path.name}")


if __name__ == "__main__":
    main()
