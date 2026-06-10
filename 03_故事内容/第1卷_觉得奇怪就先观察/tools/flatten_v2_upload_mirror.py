#!/usr/bin/env python3
"""Flatten V2迁移/打包 nested repo mirror — keep diffs, drop duplicate tree."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "V2迁移/打包"
UPLOAD = PACK / "第二次检查上传包_V0.1"
NESTED_DIFF = (
    UPLOAD
    / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/打包/02_正文_diff"
)
FLAT_DIFF = PACK / "02_正文_diff"
NESTED_ROOT = UPLOAD / "03_故事内容"


def main() -> None:
    if NESTED_DIFF.is_dir():
        FLAT_DIFF.mkdir(parents=True, exist_ok=True)
        for f in NESTED_DIFF.glob("*.diff"):
            dst = FLAT_DIFF / f.name
            if not dst.exists():
                shutil.copy2(f, dst)
                print(f"copied {f.name} -> {FLAT_DIFF}")
            else:
                print(f"skip {f.name} (exists)")
    if NESTED_ROOT.is_dir():
        shutil.rmtree(NESTED_ROOT)
        print(f"removed nested mirror: {NESTED_ROOT}")
    else:
        print("no nested mirror to remove")
    # drop empty parents
    for p in sorted(NESTED_ROOT.parents, key=lambda x: len(str(x)), reverse=True):
        if p == UPLOAD:
            break
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
            print(f"removed empty {p}")


if __name__ == "__main__":
    main()
