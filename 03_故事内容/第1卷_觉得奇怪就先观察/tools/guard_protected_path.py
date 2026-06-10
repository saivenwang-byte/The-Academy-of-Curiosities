#!/usr/bin/env python3
"""Guard writes to protected Vol1 paths — call before GenerateImage / review pack / PRODUCT copy.

Usage:
  python tools/guard_protected_path.py --write "03_.../03_插画成片/foo.png" --phase generate-image --prompt DA2.md
  python tools/guard_protected_path.py --write "03_.../06_主编审阅包_V1.0/..." --phase review-pack

Exit: same as workflow_preflight (0/1/2). Prints BLOCK code on stderr.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
REPO = VOL1.parents[1]
PREFLIGHT = VOL1 / "tools/workflow_preflight.py"

PROTECTED_FRAGMENTS = (
    "03_插画成片",
    "06_主编审阅包",
    "PRODUCT_",
    "/prompts/",
)


def is_protected(path: str) -> bool:
    norm = path.replace("\\", "/")
    return any(f in norm for f in PROTECTED_FRAGMENTS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", required=True, help="Target path agent intends to write")
    ap.add_argument("--phase", choices=("generate-image", "review-pack", "default"), default="default")
    ap.add_argument("--prompt", type=Path)
    args = ap.parse_args()

    if not is_protected(args.write):
        return 0

    norm = args.write.replace("\\", "/")
    if "06_主编审阅包" in norm or "PRODUCT_" in norm or "07_试读交付" in norm:
        mode = "deliver"
        phase = "review-pack"
    elif "03_插画成片" in norm or "/prompts/" in norm:
        mode = "produce"
        phase = args.phase if args.phase != "default" else "generate-image"
    else:
        return 0

    cmd = [
        sys.executable,
        str(PREFLIGHT),
        "--mode",
        mode,
        "--phase",
        phase,
        "--case",
        "A001",
    ]
    if phase == "generate-image":
        if not args.prompt:
            print("FAIL: generate-image guard requires --prompt", file=sys.stderr)
            return 1
        cmd.extend(["--prompt", str(args.prompt)])

    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        print(f"GUARD BLOCK write to {args.write}", file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
