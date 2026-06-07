#!/usr/bin/env python3
"""Promote G1draft → v1.0 for Batch 1 four frames (DA1, DA3, DA4, DB1)."""
from __future__ import annotations

import shutil
from pathlib import Path

REPO_VOL1 = Path(__file__).resolve().parents[2]
DEPTH = REPO_VOL1 / "样章包/插图/depth_anchor"
ASSETS = REPO_VOL1 / "正式版/02_插画/assets"

BATCH1 = [
    ("V-S01-A1_侧廊发现_G1draft.png", "V-S01-A1_侧廊发现_v1.0.png"),
    ("V-S01-A3_风侧线索_G1draft.png", "V-S01-A3_风侧线索_v1.0.png"),
    ("V-S01-A4_验证收束_G1draft.png", "V-S01-A4_验证收束_v1.0.png"),
    ("V-S01-B1_风侧机制图_G1draft.png", "V-S01-B1_风侧机制图_v1.0.png"),
]

# Optional sync to formal assets (legacy naming)
ASSET_MAP = {
    "V-S01-A1_侧廊发现_v1.0.png": "V-S01_侧廊海报.png",
    "V-S01-B1_风侧机制图_v1.0.png": "V-S03_风侧示意图.png",
}


def main() -> None:
    promoted = []
    for src_name, dst_name in BATCH1:
        src = DEPTH / src_name
        dst = DEPTH / dst_name
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copy2(src, dst)
        promoted.append(dst_name)
        alias = ASSET_MAP.get(dst_name)
        if alias:
            ASSETS.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, ASSETS / alias)
    manifest = DEPTH / "L0_v1.0_batch1_manifest_20260612.txt"
    manifest.write_text(
        "Batch1 v1.0 promoted from G1draft\n" + "\n".join(promoted) + "\n",
        encoding="utf-8",
    )
    print("Promoted:", ", ".join(promoted))


if __name__ == "__main__":
    main()
