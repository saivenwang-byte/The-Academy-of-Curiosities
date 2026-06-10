#!/usr/bin/env python3
"""Post-image gate — block canon promotion without manifest PASS + prompt hard-lock.

Usage:
  python illustration_post_gate.py --case A001 --shot DA2 --file A001_DA2_...png
  python illustration_post_gate.py --case A001 --promote-all   # list blockers
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
UNIT = VOL1 / "单元1_第一单元_五案"
HARD_LOCK = "00_PROMPT_HARD_LOCK_V1.0.md"
PROMPT_GATE = VOL1 / "tools/g_cast_prompt_gate.py"

# Prompt md must include these (illustration hard lock)
HARD_PATTERNS = [
    (re.compile(r"soft messy black|#1A1818|软黑乱发", re.I), "珣发色 LOCK"),
    (re.compile(r"warm brown|暖棕发|#6A4830", re.I), "光发色 LOCK"),
    (re.compile(r"NO Chinese|禁.*中文|学堂趣事录.*NO|NO.*学堂趣事录", re.I), "禁中文入画"),
    (re.compile(r"NO.*葛西|NO.*Kasai|禁.*葛西", re.I), "禁葛西/名牌"),
    (re.compile(r"StyleB_马克笔|STYLE_B_LOCK", re.I), "Style B 词块"),
    (re.compile(r"white uwabaki|上履き", re.I), "上履き"),
]


def _load_manifest(case: str) -> dict:
    p = UNIT / case / "03_插画" / "StyleB_V3.9" / "illustration_canon_manifest.json"
    if not p.is_file():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def check_prompt_hard_lock(case: str, shot: str) -> list[str]:
    prompt = UNIT / case / "02_分镜头" / "prompts" / f"{shot}.md"
    hard = UNIT / case / "02_分镜头" / "prompts" / HARD_LOCK
    missing = []
    if not hard.is_file():
        missing.append(f"missing {HARD_LOCK}")
        return missing
    text = prompt.read_text(encoding="utf-8") if prompt.is_file() else ""
    if HARD_LOCK not in text and "PROMPT_HARD_LOCK" not in text:
        missing.append(f"{shot}.md must reference {HARD_LOCK}")
    combined = text + "\n" + hard.read_text(encoding="utf-8")
    for pat, label in HARD_PATTERNS:
        if not pat.search(combined):
            missing.append(f"hard-lock missing: {label}")
    return missing


def check_manifest(case: str, shot: str, filename: str | None) -> list[str]:
    data = _load_manifest(case)
    frames = data.get("frames", {})
    entry = frames.get(shot)
    if not entry:
        return [f"manifest: no entry for {shot} — run illustration_canon_manifest.py"]
    if filename and entry.get("file") != filename:
        return [f"manifest file mismatch: {entry.get('file')} != {filename}"]
    v = entry.get("verdict")
    if v != "PASS":
        reasons = entry.get("reasons") or []
        return [f"manifest verdict={v}" + (f" ({'; '.join(reasons)})" if reasons else "")]
    if not entry.get("canonical"):
        return [f"manifest: PASS but canonical=false — explicit promote required"]
    return []


def check_shot(case: str, shot: str, filename: str | None) -> int:
    errors = []
    errors.extend(check_prompt_hard_lock(case, shot))
    errors.extend(check_manifest(case, shot, filename))
    if errors:
        print(f"POST-GATE FAIL {case}/{shot}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"POST-GATE PASS {case}/{shot}")
    return 0


def promote_all(case: str) -> int:
    data = _load_manifest(case)
    frames = data.get("frames", {})
    if not frames:
        print(f"FAIL: empty manifest for {case}")
        return 1
    blocked = 0
    for shot, entry in sorted(frames.items()):
        if entry.get("canonical") and entry.get("verdict") == "PASS":
            print(f"  CANON  {shot}: {entry.get('file')}")
        else:
            blocked += 1
            print(f"  BLOCK  {shot}: {entry.get('verdict')} — {entry.get('file')}")
    print(f"\n{len(frames) - blocked}/{len(frames)} shots canonical")
    return 0 if blocked == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Illustration post-image gate")
    ap.add_argument("--case", default="A001")
    ap.add_argument("--shot", help="DA1, DA2, ...")
    ap.add_argument("--file", help="PNG basename to match manifest")
    ap.add_argument("--promote-all", action="store_true")
    args = ap.parse_args()
    case = args.case.upper()
    if args.promote_all:
        return promote_all(case)
    if not args.shot:
        ap.error("--shot or --promote-all required")
    return check_shot(case, args.shot.upper(), args.file)


if __name__ == "__main__":
    raise SystemExit(main())
