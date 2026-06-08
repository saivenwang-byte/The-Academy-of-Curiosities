#!/usr/bin/env python3
"""Collapse mechanical per-character **bold** runs from batch expansion (Hybrid Voice v3 prep)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

RUN_RE = re.compile(r"(?:\*\*[^*]+\*\*\s*){2,}")


def is_mechanical_run(parts: list[str]) -> bool:
    if len(parts) < 2:
        return False
    avg = sum(len(p) for p in parts) / len(parts)
    short = sum(1 for p in parts if len(p) <= 3)
    if len(parts) == 2 and all(len(p) <= 2 for p in parts):
        return True
    if len(parts) >= 3 and avg <= 2.8 and short / len(parts) >= 0.7:
        return True
    if len(parts) >= 6 and avg <= 3.5:
        return True
    return False


def collapse_run(match: re.Match[str]) -> str:
    run = match.group(0)
    parts = re.findall(r"\*\*([^*]+)\*\*", run)
    if not is_mechanical_run(parts):
        return run
    joined = "".join(parts)
    # Preserve space before western tokens when glued to CJK
    return joined


def cleanup_cjk_spaces(line: str) -> str:
    line = re.sub(r"([，。；：「])\s+", r"\1", line)
    line = re.sub(r"\s+([，。；：」])", r"\1", line)
    line = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", line)
    line = re.sub(r"  +", " ", line)
    return line.strip() if line.strip() == line else line


def should_preserve_bold_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith(("###", "【", "relation：", "—", "==")):
        return True
    if s.startswith("·") or s.startswith("  ·"):
        return True
    if "**已确认**" in s or s.startswith("  A00") or s.startswith("  真事："):
        return True
    if s.startswith("- FC") or "FC概要" in s:
        return True
    if "【EXPERT_LOCK】" in s:
        return True
    return False


def strip_heavy_bold_line(line: str) -> str:
    if should_preserve_bold_line(line):
        return line
    if line.count("**") < 4:
        return cleanup_cjk_spaces(line) if line.count("**") >= 2 else line
    stripped = line.replace("**", "")
    return cleanup_cjk_spaces(stripped)


def normalize_line(line: str) -> str:
    prev = None
    out = line
    while prev != out:
        prev = out
        out = RUN_RE.sub(collapse_run, out)
    return strip_heavy_bold_line(out)


def normalize_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    changed = 0
    out_lines: list[str] = []
    for line in lines:
        new_line = normalize_line(line.rstrip("\n\r"))
        if new_line != line.rstrip("\n\r"):
            changed += 1
        if line.endswith("\r\n"):
            out_lines.append(new_line + "\r\n")
        elif line.endswith("\n"):
            out_lines.append(new_line + "\n")
        else:
            out_lines.append(new_line)
    return "".join(out_lines), changed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    default_dir = root / "第1卷_觉得奇怪就先观察/正式版/01_正文"
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else sorted(default_dir.glob("案0*_HybridVoice_V2.0.txt"))
    total_lines = 0
    for path in paths:
        if not path.is_file():
            print(f"skip (missing): {path}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = normalize_text(text)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
        print(f"{path.name}: {n} lines normalized")
        total_lines += n
    print(f"total: {total_lines} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
