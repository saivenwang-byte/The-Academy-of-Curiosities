#!/usr/bin/env python3
"""A001 body freeze guard — warn if 案01 HybridVoice changed from anchor commit.

Usage:
  python 03_故事内容/tools/check_a001_freeze.py
  python 03_故事内容/tools/check_a001_freeze.py --strict   # exit 1 on drift

SSOT: V2迁移/40_A001迭代冻结_E20门禁_V0.1.md · anchor 11cf625
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
A001 = (
    REPO
    / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"
    / "案01_全班都听见了他的声音_HybridVoice_V2.0.txt"
)
FREEZE_COMMIT = "11cf625"
FREEZE_DOC = (
    REPO
    / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移"
    / "40_A001迭代冻结_E20门禁_V0.1.md"
)


def git_diff_quiet(commit: str, rel_path: str) -> bool:
    """Return True if working tree matches commit for rel_path."""
    try:
        proc = subprocess.run(
            ["git", "diff", "--quiet", commit, "--", rel_path],
            cwd=REPO,
            capture_output=True,
            check=False,
        )
    except OSError:
        return False
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="A001 freeze drift check")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 if body differs from freeze anchor",
    )
    args = parser.parse_args()

    rel = "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文/案01_全班都听见了他的声音_HybridVoice_V2.0.txt"

    if not A001.exists():
        print(f"ERROR: missing {A001}")
        return 1

    matches = git_diff_quiet(FREEZE_COMMIT, rel)

    result = {
        "frozen": True,
        "case": "A001",
        "file": rel,
        "freeze_commit": FREEZE_COMMIT,
        "freeze_doc": str(FREEZE_DOC.relative_to(REPO)),
        "drift": False,
        "e20_gate": "0/12 slots · REVIEW_LOOP_R16 terminal",
        "message": "",
    }

    if not matches:
        result["drift"] = True
        result["frozen"] = False
        result["message"] = (
            "A001 FREEZE VIOLATION: 案01 HybridVoice_V2.0.txt differs from "
            f"{FREEZE_COMMIT}. Do NOT edit until E20 ≥1 slot + IP approval. "
            f"See {FREEZE_DOC.relative_to(REPO)}"
        )
        print(result["message"])
        return 1 if args.strict else 0

    result["message"] = (
        f"OK: A001 frozen at {FREEZE_COMMIT} — no body drift detected"
    )
    print(result["message"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
