#!/usr/bin/env python3
"""G-CAST prompt gate — block GenerateImage prep without MAX_BODIES in prompt md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = [
    (re.compile(r"MAX_BODIES|G-CAST MAX", re.I), "MAX_BODIES"),
    (re.compile(r"具名|named|慧美|志郎", re.I), "具名名单"),
    (re.compile(r"禁止|NEGATIVE|NO Chinese|NO.*葛西|禁.*葛西", re.I), "禁止出场/NEGATIVE"),
    (re.compile(r"anonymous|匿名|faceless|无 L0 脸", re.I), "匿名群众规则"),
    (re.compile(r"PROMPT_HARD_LOCK|00_PROMPT_HARD_LOCK", re.I), "硬锁文件引用"),
    (re.compile(r"soft messy black|#1A1818|软黑", re.I), "珣发色 LOCK"),
    (re.compile(r"warm brown|#6A4830|暖棕", re.I), "光发色 LOCK"),
    (re.compile(r"STYLE_B_LOCK|StyleB_马克笔", re.I), "Style B LOCK"),
    (re.compile(r"white uwabaki|上履き", re.I), "上履き"),
]


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    missing = [label for pat, label in REQUIRED if not pat.search(text)]
    pad_section = ""
    if m := re.search(r"##\s*垫图[\s\S]*?(?=##|\Z)", text):
        pad_section = m.group(0)
    for line in pad_section.splitlines():
        if re.search(r"禁止|❌", line):
            continue
        if re.search(r"IP确认|十人排面|CHAR_lineup_L0_IP", line, re.I):
            missing.append("垫图含十人排面（应仅 StyleB 画风 LOCK）")
            break
    return missing


def main() -> int:
    ap = argparse.ArgumentParser(description="G-CAST prompt gate")
    ap.add_argument("prompt_md", type=Path, help="prompt markdown file")
    args = ap.parse_args()
    if not args.prompt_md.is_file():
        print(f"FAIL: missing {args.prompt_md}")
        return 1
    missing = check(args.prompt_md)
    if missing:
        print("G-CAST prompt gate FAIL:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("G-CAST prompt gate PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
