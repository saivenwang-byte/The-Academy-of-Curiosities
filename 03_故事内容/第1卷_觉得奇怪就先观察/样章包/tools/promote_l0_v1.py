#!/usr/bin/env python3
"""Promote G1draft → v1.0 by batch."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_VOL1 = Path(__file__).resolve().parents[2]
DEPTH = REPO_VOL1 / "样章包/插图/depth_anchor"
ASSETS = REPO_VOL1 / "正式版/02_插画/assets"

BATCHES: dict[str, list[tuple[str, str]]] = {
    "1": [
        ("V-S01-A1_侧廊发现_G1draft.png", "V-S01-A1_侧廊发现_v1.0.png"),
        ("V-S01-A3_风侧线索_G1draft.png", "V-S01-A3_风侧线索_v1.0.png"),
        ("V-S01-A4_验证收束_G1draft.png", "V-S01-A4_验证收束_v1.0.png"),
        ("V-S01-B1_风侧机制图_G1draft.png", "V-S01-B1_风侧机制图_v1.0.png"),
    ],
    "2": [
        ("V-S01-A2_误导搜查_G1draft.png", "V-S01-A2_误导搜查_v1.0.png"),
        ("V-S01-TAIL_壁报空栏_G1draft.png", "V-S01-TAIL_壁报空栏_v1.0.png"),
    ],
    "all": [],
}

ASSET_MAP = {
    "V-S01-A1_侧廊发现_v1.0.png": "V-S01_侧廊海报.png",
    "V-S01-B1_风侧机制图_v1.0.png": "V-S03_风侧示意图.png",
    "V-S01-TAIL_壁报空栏_v1.0.png": "V-S01-TAIL_壁报草稿空栏.png",
}


def promote(batch_key: str) -> list[str]:
    pairs = BATCHES["all"] if batch_key == "all" else BATCHES[batch_key]
    if batch_key == "all":
        pairs = BATCHES["1"] + BATCHES["2"]
    promoted = []
    for src_name, dst_name in pairs:
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
    manifest = DEPTH / f"L0_v1.0_batch{batch_key}_manifest.txt"
    manifest.write_text(
        f"Batch {batch_key} v1.0 promoted from G1draft\n" + "\n".join(promoted) + "\n",
        encoding="utf-8",
    )
    return promoted


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("batch", choices=["1", "2", "all"], default="2", nargs="?")
    args = p.parse_args()
    names = promote(args.batch)
    print("Promoted:", ", ".join(names))


if __name__ == "__main__":
    main()
