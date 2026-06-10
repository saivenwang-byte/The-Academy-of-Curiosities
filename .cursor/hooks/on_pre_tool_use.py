#!/usr/bin/env python3
"""Block Write/StrReplace to Vol1 protected paths unless workflow_preflight passes."""

from __future__ import annotations

import json
import subprocess
import sys
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/tools/guard_protected_path.py"

PROTECTED = (
    "03_插画成片",
    "06_主编审阅包",
    "PRODUCT_",
    "/prompts/",
)


def _path_from_tool_input(tool_input: object) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    for key in ("path", "file_path", "target_file", "target_notebook"):
        val = tool_input.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return None


def _is_protected(path: str) -> bool:
    norm = path.replace("\\", "/")
    return any(fragment in norm for fragment in PROTECTED)


def main() -> int:
    try:
        stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        payload = json.load(stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(json.dumps({"permission": "allow"}))
        return 0

    tool_input = payload.get("tool_input") or payload.get("arguments") or {}
    target = _path_from_tool_input(tool_input)
    if not target or not _is_protected(target):
        print(json.dumps({"permission": "allow"}))
        return 0

    phase = "review-pack" if "06_主编审阅包" in target.replace("\\", "/") else "default"
    cmd = [sys.executable, str(GUARD), "--write", target, "--phase", phase]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True)
    if proc.returncode == 0:
        print(json.dumps({"permission": "allow"}))
        return 0

    detail = (proc.stdout + proc.stderr).decode("utf-8", errors="replace").strip().splitlines()
    block_line = next((line for line in reversed(detail) if "BLOCK" in line or "FAIL" in line), detail[-1] if detail else "workflow preflight failed")
    msg = f"硬拦截：未过 workflow_preflight，禁止写入受保护路径。{block_line}"
    print(
        json.dumps(
            {
                "permission": "deny",
                "user_message": msg,
                "agent_message": msg + " 见 单元1_第一单元_五案/00_硬拦截说明_V1.0.md",
            },
            ensure_ascii=True,
        )
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
