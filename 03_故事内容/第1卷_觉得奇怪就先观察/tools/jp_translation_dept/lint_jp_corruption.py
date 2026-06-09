#!/usr/bin/env python3
"""Build lint: fail on JP template corruption (duplicate furigana / event terms).

Usage:
  python lint_jp_corruption.py path/to/file.txt ...
  python lint_jp_corruption.py --unit1-v39   # all V3.9 JP canonical copies
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNIT = ROOT / "单元1_第一单元_五案"

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("repeated_furigana", re.compile(r"（[ぁ-んァ-ヶー]+）（[ぁ-んァ-ヶー]+）")),
    ("repeated_school", re.compile(r"(?:学校){2,}")),
    ("repeated_event_suffix", re.compile(r"(?:と学習発表会){2,}")),
    ("wrong_goudou_reading", re.compile(r"がっどうきょうしつ")),
    ("full_corrupt_block", re.compile(
        r"学校(?:学校)*(?:公開日と(?:学習発表会と)+学習発表会|学校公開日と(?:学習発表会と)+学習発表会)"
    )),
]

NO_PARTICLE_AFTER_EVENT = re.compile(
    r"公開日と学習発表会(?!の|に|、|。|」|」|・|を|は|が|で|と|から|まで|へ)"
    r"(リハーサル|展示|バッジ|カウントダウン|プレビュー|破壊|案内板|クラス|展示前|前に)"
)


def lint_text(text: str, path: str = "<text>") -> list[str]:
    errors: list[str] = []
    for name, pat in PATTERNS:
        for m in pat.finditer(text):
            line = text[: m.start()].count("\n") + 1
            errors.append(f"{path}:{line}: {name}: {m.group(0)!r}")
    for m in NO_PARTICLE_AFTER_EVENT.finditer(text):
        line = text[: m.start()].count("\n") + 1
        errors.append(
            f"{path}:{line}: missing_particle: {m.group(0)!r} (need の/に)"
        )
    return errors


def collect_unit1_v39() -> list[Path]:
    paths: list[Path] = []
    for sub in (
        UNIT / "正文" / "V3.9" / "02_日本語",
        UNIT / "A001" / "01_正文",
        UNIT / "A002" / "01_正文",
        UNIT / "A003" / "01_正文",
        UNIT / "A004" / "01_正文",
        UNIT / "A005" / "01_正文",
    ):
        if sub.exists():
            paths.extend(sorted(sub.glob("*_V3.9_日本語.txt")))
    seen: set[Path] = set()
    out: list[Path] = []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint JP text for template corruption")
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--unit1-v39", action="store_true", help="lint all Unit1 V3.9 JP files")
    args = ap.parse_args()

    files = list(args.files)
    if args.unit1_v39:
        files = collect_unit1_v39()

    if not files:
        ap.error("provide files or --unit1-v39")

    all_errors: list[str] = []
    for fp in files:
        if not fp.exists():
            all_errors.append(f"{fp}: file not found")
            continue
        text = fp.read_text(encoding="utf-8")
        all_errors.extend(lint_text(text, str(fp)))

    if all_errors:
        print("JP corruption lint FAILED:\n", file=sys.stderr)
        for e in all_errors:
            print(f"  {e}", file=sys.stderr)
        print(f"\n{len(all_errors)} issue(s)", file=sys.stderr)
        return 1

    print(f"JP corruption lint PASS ({len(files)} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
