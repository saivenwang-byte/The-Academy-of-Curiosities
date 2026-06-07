#!/usr/bin/env python3
"""REVIEW LOOP Round 4 — light reader-flow polish A002/A004 weak spots."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

A002 = BODY / "案02_没有人写过的道歉_HybridVoice_V2.0.txt"
A004 = BODY / "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt"


def polish_a002(text: str) -> str:
  # Trim redundant membrane recap; keep one FC beat
  old = (
    "志郎把膜对着窗。膜背面的字是反的——湿擦后，粉笔灰停在边缘，字就「浮」出来了。\n\n"
    "他在备课本上试：写「对不起」，压膜，湿擦——淡灰浮出，和板上同形。"
  )
  new = (
    "志郎把膜对着窗。膜背面是反字——湿擦后，粉笔灰停在边缘就会「浮」出来。"
    "备课本上一试：压膜、湿擦，板上同形。"
  )
  if old in text:
    text = text.replace(old, new)
  # Reader jump: collapse duplicate 字回来了 beat
  dup = (
    "字回来的那次，教室像案① 重复播放—— 同一句对不起，第二遍更像 「他干的」。\n\n\n"
    "陸珣没说不是。只把湿擦顺序画在本子上：先膜后擦=错序；错序+清洁液=再现。\n\n\n"
  )
  if dup in text:
    text = text.replace(dup, "")
  return text


def polish_a004(text: str) -> str:
  # E07 reader trim: shorten wrong_responsibility peak echo
  old = (
    "全班已经连好故事：水野逐一偷走展示物资 · 破坏公开日团结 · 观察社 **又要帮她说话**。\n\n\n"
    "**wrong_responsibility 峰值**。机制尚未当众讲完。\n\n\n"
    "有人 **把** 案③ 「海报」和案④ 「抽屉」接在一起：「水野早就被排斥了，偷东西是报应。」"
  )
  new = (
    "全班已经连好故事：水野偷物资 · 观察社又要帮她说话。\n\n\n"
    "有人把案③海报和案④抽屉接在一起：「她早就被排斥了。」"
  )
  if old in text:
    text = text.replace(old, new)
  return text


def main() -> None:
  for path, fn in [(A002, polish_a002), (A004, polish_a004)]:
    raw = path.read_text(encoding="utf-8")
    out = fn(raw)
    if out != raw:
      path.write_text(out, encoding="utf-8")
      print(f"R4 polished {path.name}")
    else:
      print(f"No change {path.name}")


if __name__ == "__main__":
  main()
