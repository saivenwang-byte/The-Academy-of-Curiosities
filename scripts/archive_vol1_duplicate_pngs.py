#!/usr/bin/env python3
"""
Archive non-canonical duplicate PNGs in Vol1 插图 folder.

Moves files NOT matching canonical English snake_case names to _archive_cn_duplicates/.

Usage:
  python scripts/archive_vol1_duplicate_pngs.py --dry-run
  python scripts/archive_vol1_duplicate_pngs.py
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ILLUST = ROOT / "03_故事内容" / "第1卷_总是湿的椅子" / "插图"
ARCHIVE = ILLUST / "_archive_cn_duplicates"

CANONICAL = {
    "01_scene_wet_chair.png",
    "02_scene_four_chairs.png",
    "03_scene_rumor_search.png",
    "04_scene_window_frame.png",
    "05_scene_experiment_setup.png",
    "06_scene_dew_map.png",
    "07_scene_one_fist_gap.png",
    "08_scene_case_logbook.png",
    "09_summary_three_principles.png",
    "10_summary_home_experiment.png",
    "11_summary_hikaru_sketch.png",
    "12_summary_april_daily.png",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not ILLUST.is_dir():
        print(f"ERROR: {ILLUST} not found")
        return 1

    to_move: list[Path] = []
    for p in sorted(ILLUST.glob("*.png")):
        if p.name not in CANONICAL:
            to_move.append(p)

    if not to_move:
        print("No duplicate PNGs to archive.")
        return 0

    print(f"Found {len(to_move)} non-canonical PNG(s):")
    for p in to_move:
        print(f"  {p.name}")

    if args.dry_run:
        print("\nDry run — no files moved.")
        return 0

    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for p in to_move:
        dest = ARCHIVE / p.name
        if dest.exists():
            dest.unlink()
        shutil.move(str(p), str(dest))
        print(f"Moved → _archive_cn_duplicates/{p.name}")

    readme = ARCHIVE / "README.md"
    readme.write_text(
        "# 归档 · 中文前缀 PNG 副本\n\n"
        "正典文件名为英文 snake_case（见上级目录 `01_scene_wet_chair.png` 等）。\n"
        "本目录为 v2 统调时的重复导出，**排版/PDF 勿引用**。\n\n"
        f"归档日期：由 `scripts/archive_vol1_duplicate_pngs.py` 生成\n",
        encoding="utf-8",
    )
    print(f"\nArchived {len(to_move)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
