#!/usr/bin/env python3
"""Cursor stop hook: nudge if volume planning lint fails."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VOLUME_LINT = ROOT / "scripts" / "volume_lint.py"


def main() -> int:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    if not VOLUME_LINT.is_file():
        return 0

    code = subprocess.run(
        [sys.executable, str(VOLUME_LINT), "--all", "-q"],
        cwd=ROOT,
        capture_output=True,
    ).returncode

    if code != 0:
        msg = (
            "Planning lint failed (Case/Scene/story table). "
            "Run: python scripts/pre_push_check.py"
        )
        print(json.dumps({"followup_message": msg}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
