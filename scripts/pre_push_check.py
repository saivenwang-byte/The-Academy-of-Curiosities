#!/usr/bin/env python3
"""
Pre-push / pre-commit quality gate for 《学堂趣事录》.

Runs bundled lints (Case Card, Scene Card, story table, Vol1 visuals).

Usage:
  python scripts/pre_push_check.py
  python scripts/pre_push_check.py --no-visual
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_LINT = ROOT / "scripts" / "case_card_lint.py"
SCENE_LINT = ROOT / "scripts" / "scene_card_lint.py"


def run_script(script: Path, extra_args: list[str]) -> int:
    cmd = [sys.executable, str(script), *extra_args]
    print(f"\n>>> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run all project lints")
    parser.add_argument("--no-visual", action="store_true", help="Skip Vol1 PNG check")
    args = parser.parse_args()

    steps: list[tuple[str, list[str]]] = [
        ("Case Cards", []),
        ("Story table", ["--story-table"]),
        ("Scene Cards", []),
    ]
    if not args.no_visual:
        steps.append(("Vol1 visuals", ["--visual", "vol1"]))

    failed: list[str] = []

    # case_card_lint handles case cards + optional flags
    code = run_script(CASE_LINT, [])
    if code != 0:
        failed.append("case_card_lint (cards)")

    code = run_script(CASE_LINT, ["--story-table"])
    if code != 0:
        failed.append("case_card_lint (story table)")

    if not args.no_visual:
        code = run_script(CASE_LINT, ["--visual", "vol1"])
        if code != 0:
            failed.append("case_card_lint (visual)")

    code = run_script(SCENE_LINT, [])
    if code != 0:
        failed.append("scene_card_lint")

    code = run_script(ROOT / "scripts" / "volume_lint.py", ["--all", "-q"])
    if code != 0:
        failed.append("volume_lint")

    code = run_script(ROOT / "scripts" / "body_lint.py", ["--vol", "2"])
    if code != 0:
        failed.append("body_lint (vol2)")

    print("\n" + "=" * 50)
    if failed:
        print("PRE-PUSH CHECK: FAIL")
        for name in failed:
            print(f"  - {name}")
        print("\nFix errors before commit/push.")
        return 1

    print("PRE-PUSH CHECK: PASS")
    print("Reminder: update 正典文件索引 if you changed docs/skills/rules.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
