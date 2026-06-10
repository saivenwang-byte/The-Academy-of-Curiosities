#!/usr/bin/env python3
"""Move non-canonical StyleB PNGs to _quarantine/ per illustration_canon_manifest.json."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
UNIT = VOL1 / "单元1_第一单元_五案"


def quarantine_case(case: str, dry_run: bool = False) -> int:
    style_dir = UNIT / case / "03_插画" / "StyleB_V3.9"
    manifest_p = style_dir / "illustration_canon_manifest.json"
    if not manifest_p.is_file():
        print(f"FAIL: missing {manifest_p}")
        return 1
    data = json.loads(manifest_p.read_text(encoding="utf-8"))
    canonical_files = {
        e["file"]
        for e in data.get("frames", {}).values()
        if e.get("canonical") and e.get("verdict") == "PASS"
    }
    qdir = style_dir / "_quarantine"
    qdir.mkdir(exist_ok=True)
    moved = 0
    for png in style_dir.glob("*.png"):
        if png.name in canonical_files:
            print(f"  KEEP {png.name}")
            continue
        dest = qdir / png.name
        print(f"  MOVE {png.name} -> _quarantine/")
        if not dry_run:
            if dest.exists():
                dest.unlink()
            shutil.move(str(png), str(dest))
        moved += 1
    print(f"\n{'would move' if dry_run else 'moved'} {moved} file(s); canonical: {len(canonical_files)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="A001")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    return quarantine_case(args.case.upper(), args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
