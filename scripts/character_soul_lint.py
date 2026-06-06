#!/usr/bin/env python3
"""Lint Vol1 core character soul YAML files against schema minimums."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SOUL_DIR = ROOT / "characters" / "soul"

REQUIRED_TOP = [
    "meta",
    "soul_line",
    "core_desire",
    "core_fear",
    "language_fingerprint",
    "behavior_fingerprint",
    "growth_and_guardrails",
]

REQUIRED_META = ["character_id", "display_name", "status", "soul_version"]

VOL1_CORE = [
    "ito_hikaru_soul.yaml",
    "kato_keimi_soul.yaml",
    "matsumoto_shiro_soul.yaml",
    "riku_shun_soul.yaml",
    "riku_hikaru_soul.yaml",
]


def lint_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path.name}: parse error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path.name}: root must be mapping"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"{path.name}: missing top-level '{key}'")

    meta = data.get("meta") or {}
    if not isinstance(meta, dict):
        errors.append(f"{path.name}: meta must be mapping")
    else:
        for key in REQUIRED_META:
            if key not in meta:
                errors.append(f"{path.name}: meta missing '{key}'")
        status = meta.get("status", "")
        if status not in ("LOCK", "V0.1", "DRAFT"):
            errors.append(f"{path.name}: unexpected status '{status}'")

    lang = data.get("language_fingerprint") or {}
    if isinstance(lang, dict) and not lang.get("forbidden_patterns"):
        errors.append(f"{path.name}: language_fingerprint.forbidden_patterns empty")

    guard = data.get("growth_and_guardrails") or {}
    if isinstance(guard, dict) and not guard.get("never_write"):
        errors.append(f"{path.name}: growth_and_guardrails.never_write empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint character soul YAML files")
    parser.add_argument(
        "--vol1-core",
        action="store_true",
        help="Lint only Vol1 five core soul files",
    )
    parser.add_argument("files", nargs="*", help="Optional specific soul yaml paths")
    args = parser.parse_args()

    if args.files:
        paths = [Path(f) for f in args.files]
    elif args.vol1_core:
        paths = [SOUL_DIR / name for name in VOL1_CORE]
    else:
        paths = sorted(SOUL_DIR.glob("*_soul.yaml"))

    all_errors: list[str] = []
    checked = 0
    for path in paths:
        if not path.exists():
            all_errors.append(f"missing: {path}")
            continue
        checked += 1
        all_errors.extend(lint_file(path))

    if all_errors:
        print(f"FAIL ({len(all_errors)} issues, {checked} files checked):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(f"PASS: {checked} soul file(s) OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
