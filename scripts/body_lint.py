#!/usr/bin/env python3
"""
Body text lint for 《学堂趣事录》完整文字稿.txt.

Usage:
  python scripts/body_lint.py --file 03_故事内容/第2卷_谁偷了橡皮/完整文字稿.txt
  python scripts/body_lint.py --vol 2
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Vol1 正典：方案 B · 觉得奇怪就先观察（湿椅子路径为 deprecated 素材）
BODY_PATHS: dict[int, Path] = {
    1: ROOT
    / "03_故事内容"
    / "第1卷_觉得奇怪就先观察"
    / "样章包"
    / "04_样章_序+案01_正文_HybridVoice.txt",
    2: ROOT / "03_故事内容" / "第2卷_谁偷了橡皮" / "完整文字稿.txt",
}

FORBIDDEN_CN = [
    ("报告老师", "改用：先生、これ見てください"),
    ("去食堂", "改用：給食"),
    ("食堂打饭", "改用：給食当番/配膳"),
    ("你太棒了", "改用：頑張ったね"),
]

FORBIDDEN_NAMES = [
    ("山本琦美", "正典：山本理紗（やまもと りさ）"),
    ("山本琦理", "正典：山本理紗"),
    ("河合琦美", "正典：山本理紗"),
    ("りく けい", "陸瑆正典：りく ひかる（妹妹）· けい 已废止"),
    ("Riku Kei", "陸瑆正典：Riku Hikaru"),
]

FORBIDDEN_TONE = [
    "鬼",
    "幽灵",
    "血腥",
    "魔法",
]

# V2 年级：瑆 4年2組 · 珣/光/慧美/志郎/理紗 5年各組 · 中谷 6年1組
# deprecated 素材（湿椅子等）不参与年级漂移 ERROR
DEPRECATED_BODY_MARKERS = (
    "第1卷_总是湿的椅子",
    "volume_01_wet_chair",
    "_archive",
    "00_归档",
)

V1_GRADE_DRIFT = [
    (re.compile(r"陸珣[^。\n]{0,12}4年2組"), "陸珣 应为 5年2組（V2）"),
    (re.compile(r"伊藤光[^。\n]{0,12}4年2組"), "伊藤光 应为 5年2組（V2）"),
    (re.compile(r"加藤慧美[^。\n]{0,12}4年2組"), "加藤慧美 应为 5年1組（V2）"),
    (re.compile(r"松本志郎[^。\n]{0,12}4年2組"), "松本志郎 应为 5年3組（V2）"),
    (re.compile(r"陸瑆[^。\n]{0,12}5年"), "陸瑆 应为 4年2組（V2）"),
    (re.compile(r"中谷琦[^。\n]{0,12}5年"), "中谷琦 应为 6年1組（V2）"),
    (re.compile(r"全员[^。\n]{0,8}4年2組"), "禁止 V1 全员同班 4年2組"),
    (re.compile(r"四人[^。\n]{0,8}4年2組"), "Vol1 核心为 5年跨班，非 4年2組 同班"),
]

# 陸珣 direct speech in Chinese narrative: lines with 陸珣...「...」 or 陸珣说
RIKUSHUN_SPEECH = re.compile(
    r"陸珣[^。\n]{0,20}(?:说|开口|忽然|低声)[^。\n]{0,10}[「『]([^」』]+)[」』]"
)


@dataclass
class BodyResult:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def lint_body(path: Path, max_rikushun_speech: int = 5) -> BodyResult:
    r = BodyResult(path=path)
    if not path.is_file():
        r.errors.append(f"正文不存在: {path.relative_to(ROOT)}")
        return r

    text = path.read_text(encoding="utf-8")
    if len(text) < 2000:
        r.warnings.append(f"篇幅较短 ({len(text)} 字)，目标 6000–8000")

    for phrase, hint in FORBIDDEN_CN:
        if phrase in text:
            r.errors.append(f"禁直译腔: 「{phrase}」 — {hint}")

    for phrase, hint in FORBIDDEN_NAMES:
        if phrase in text:
            r.errors.append(f"禁用角色名: 「{phrase}」 — {hint}")

    for phrase in FORBIDDEN_TONE:
        if phrase in text and "零恐怖" not in text[:500]:
            r.warnings.append(f"检查恐怖/超自然用词: 「{phrase}」")

    if "教室後方" in text and "流し" in text and "昼" in text:
        r.errors.append("可能误写昼歯磨き在教室後方流し — 应为廊下手洗い場")

    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    skip_grade = any(m in rel for m in DEPRECATED_BODY_MARKERS)
    if not skip_grade:
        for pattern, hint in V1_GRADE_DRIFT:
            if pattern.search(text):
                r.errors.append(f"年级漂移: {hint}")

    speeches = RIKUSHUN_SPEECH.findall(text)
    if len(speeches) > max_rikushun_speech:
        r.warnings.append(
            f"陸珣对外台词约 {len(speeches)} 处（目标 ≤{max_rikushun_speech}）"
        )

    if "【你可以这样做】" not in text:
        r.warnings.append("缺少实验页「【你可以这样做】」（全卷正文项 · 样章可忽略）")

    if "陸瑆笔记" not in text and "瑆笔记" not in text and "陸瑆" not in text:
        r.warnings.append("缺少陸瑆笔记层或瑆页")

    club_markers = ("怪事研究社", "学堂趣事录", "観察クラブ", "观察社", "おもしろ観察")
    if not any(m in text for m in club_markers):
        r.warnings.append("建议提及观察クラブ/观察社或学堂趣事录系列伏笔")

    return r


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint 完整文字稿.txt")
    parser.add_argument("--file", type=Path)
    parser.add_argument("--vol", type=int)
    args = parser.parse_args()

    paths: list[Path] = []
    if args.file:
        p = args.file if args.file.is_absolute() else ROOT / args.file
        paths = [p]
    elif args.vol:
        p = BODY_PATHS.get(args.vol)
        if not p:
            print(f"Vol{args.vol} 未注册", file=sys.stderr)
            return 1
        paths = [p]
    else:
        paths = [p for p in BODY_PATHS.values() if p.is_file()]

    if not paths:
        print("No body files to lint.", file=sys.stderr)
        return 1

    failed = 0
    for path in paths:
        r = lint_body(path)
        rel = path.relative_to(ROOT)
        print(f"\n[{'PASS' if r.ok else 'FAIL'}] {rel}")
        for e in r.errors:
            print(f"  ERROR: {e}")
        for w in r.warnings:
            print(f"  WARN:  {w}")
        if not r.ok:
            failed += 1

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
