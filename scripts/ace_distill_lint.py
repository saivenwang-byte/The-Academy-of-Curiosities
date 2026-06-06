#!/usr/bin/env python3
"""Lint ACE distill cards under skills/ace-experts/*/cards/*.yaml"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
ACE_ROOT = ROOT / "skills" / "ace-experts"

REQUIRED = [
    "card_id",
    "version",
    "ace_officer",
    "status",
    "implementation",
    "capability_atom",
    "canon_refs",
    "knowledge_sources",
    "checks",
    "reject_if",
    "output_contract",
]

OFFICERS = {
    "ACE-A_Canon_Gate_Officer",
    "ACE-B_Sample_Visual_Production_Officer",
    "ACE-C_Trial_Market_Officer",
    "ACE-D_Publishing_IP_Extension_Officer",
}


def lint_card(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path.name}: parse error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path.name}: root must be mapping"]

    for key in REQUIRED:
        if key not in data:
            errors.append(f"{path.name}: missing '{key}'")

    impl = data.get("implementation") or {}
    if impl.get("mode") != "rag_rules_only":
        errors.append(f"{path.name}: implementation.mode must be rag_rules_only")
    if impl.get("fine_tune") is not False:
        errors.append(f"{path.name}: implementation.fine_tune must be false")

    officer = data.get("ace_officer")
    if officer not in OFFICERS:
        errors.append(f"{path.name}: invalid ace_officer '{officer}'")

    for src in data.get("knowledge_sources") or []:
        if isinstance(src, dict) and src.get("persona_agent_forbidden") is not True:
            errors.append(f"{path.name}: knowledge_sources persona_agent_forbidden must be true")

    out = data.get("output_contract") or {}
    if out.get("signoff") != "human_required":
        errors.append(f"{path.name}: output_contract.signoff must be human_required")

    if not data.get("checks"):
        errors.append(f"{path.name}: checks empty")
    if not data.get("reject_if"):
        errors.append(f"{path.name}: reject_if empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--officer", help="Filter by officer folder name")
    args = parser.parse_args()

    if args.officer:
        base = ACE_ROOT / args.officer / "cards"
        paths = sorted(base.glob("*.yaml")) if base.is_dir() else []
    else:
        paths = sorted(ACE_ROOT.glob("*/cards/*.yaml"))

    all_errors: list[str] = []
    for path in paths:
        all_errors.extend(lint_card(path))

    if all_errors:
        print(f"FAIL ({len(all_errors)} issues, {len(paths)} cards):")
        for e in all_errors:
            print(f"  - {e}")
        return 1

    print(f"PASS: {len(paths)} distill card(s) OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
