#!/usr/bin/env python3
"""Merge Vol1 JP canon: sample A001 + formal A002-A005."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 正式版/
SAMPLE_A001 = ROOT.parent / "样章包" / "04_样章_序+案01_正文_日本語.txt"
CH_A002_005 = ROOT / "01_正本" / "Vol1_正本_日本語_A002-A005.txt"
OUT = ROOT / "01_正本" / "学堂趣事录_Vol1_觉得奇怪就先观察_正本_日本語.txt"


def extract_a001(sample: str) -> str:
    lines = sample.splitlines()
    out: list[str] = []
    skip_header = True
    for line in lines:
        if skip_header:
            if line.startswith("序 ·"):
                skip_header = False
                out.append("『学堂奇事録』（学堂趣事録）")
                out.append("第1巻 · おかしいと思ったら、まず見てみる")
                out.append("=" * 40)
                out.append("【正式版 · Hybrid Voice 日本語 v1】")
                out.append("  · 範囲：序 · 事件①–⑤")
                out.append("  · A001：JP_VOICE_v1（試読推敲済）")
                out.append("  · A002–A005：初訳 · E07/田中みどり待ち")
                out.append("")
                out.append(line)
                continue
            continue
        if line.strip().startswith("（事件① 試読章 終"):
            break
        if line.strip().startswith("---") and "日本語推敲メモ" in sample[sample.index(line) : sample.index(line) + 80]:
            break
        out.append(line)
    return "\n".join(out).rstrip()


def main() -> None:
    sample = SAMPLE_A001.read_text(encoding="utf-8")
    a001 = extract_a001(sample)
    rest = CH_A002_005.read_text(encoding="utf-8").strip()
    merged = a001 + "\n\n\n" + rest + "\n"
    OUT.write_text(merged, encoding="utf-8")
    print(f"Wrote {OUT} ({len(merged)} chars)")


if __name__ == "__main__":
    main()
