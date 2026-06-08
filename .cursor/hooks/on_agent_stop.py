#!/usr/bin/env python3
"""Cursor stop hook: volume lint + optional memory checkpoint nudge."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VOLUME_LINT = ROOT / "scripts" / "volume_lint.py"
SESSIONS_DIR = ROOT / ".cursor" / "memory" / "sessions"
CHECKPOINT_RECENT_DAYS = 7


def _recent_checkpoint_exists() -> bool:
    if not SESSIONS_DIR.is_dir():
        return False
    cutoff = datetime.now() - timedelta(days=CHECKPOINT_RECENT_DAYS)
    for path in SESSIONS_DIR.glob("*.md"):
        if path.name == ".gitkeep":
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            continue
        if mtime >= cutoff:
            return True
    return False


def main() -> int:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass

    messages: list[str] = []

    if VOLUME_LINT.is_file():
        code = subprocess.run(
            [sys.executable, str(VOLUME_LINT), "--all", "-q"],
            cwd=ROOT,
            capture_output=True,
        ).returncode
        if code != 0:
            messages.append(
                "Planning lint failed (Case/Scene/story table). "
                "Run: python scripts/pre_push_check.py"
            )

    if not _recent_checkpoint_exists():
        messages.append(
            f"No session checkpoint in the last {CHECKPOINT_RECENT_DAYS} days. "
            "Save handoff: .\\tools\\ecc-memory\\bin\\memory_checkpoint.ps1 -Topic \"…\" "
            "or update .cursor/memory/MEMORY.md"
        )

    if messages:
        print(json.dumps({"followup_message": " | ".join(messages)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
