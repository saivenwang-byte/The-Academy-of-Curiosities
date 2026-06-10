#!/usr/bin/env python3
"""Illustration canon manifest — single SSOT for PNG verdicts (PASS/REVISE/REJECT).

Paths: A00X/03_插画/StyleB_V3.9/illustration_canon_manifest.json

Only entries with verdict==PASS and canonical==true may be promoted or bound to PDF.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
UNIT = VOL1 / "单元1_第一单元_五案"

VERDICTS = frozenset({"PASS", "REVISE", "REJECT", "PENDING"})


def manifest_path(case: str) -> Path:
    return UNIT / case / "03_插画" / "StyleB_V3.9" / "illustration_canon_manifest.json"


def load(case: str) -> dict:
    p = manifest_path(case)
    if not p.is_file():
        return {"case": case, "updated": None, "frames": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save(case: str, data: dict) -> None:
    p = manifest_path(case)
    p.parent.mkdir(parents=True, exist_ok=True)
    data["case"] = case
    data["updated"] = date.today().isoformat()
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def set_frame(
    case: str,
    shot: str,
    file: str,
    verdict: str,
    *,
    canonical: bool = False,
    reasons: list[str] | None = None,
    auditor: str = "agent",
) -> None:
    if verdict not in VERDICTS:
        raise ValueError(f"invalid verdict {verdict}")
    data = load(case)
    frames = data.setdefault("frames", {})
    frames[shot] = {
        "file": file,
        "verdict": verdict,
        "canonical": canonical and verdict == "PASS",
        "reasons": reasons or [],
        "auditor": auditor,
        "date": date.today().isoformat(),
    }
    save(case, data)


def get_frame(case: str, shot: str) -> dict | None:
    return load(case).get("frames", {}).get(shot)


def list_canonical(case: str) -> dict[str, dict]:
    return {k: v for k, v in load(case).get("frames", {}).items() if v.get("canonical")}


def cmd_init_a001() -> int:
    """Seed A001 manifest from known audit state (2026-06-10)."""
    case = "A001"
    seeds = {
        "DA1": ("A001_DA1_PRODUCT_StyleB_V3.9_v1.2.png", "REVISE", ["lip_sync", "podium_mic", "gcast"]),
        "DA2": ("A001_DA2_PRODUCT_StyleB_V3.9_v1.2.png", "REJECT", ["gray_white_hair", "sneakers", "gcast_overcount"]),
        "DA3": ("A001_DA3_PRODUCT_StyleB_V3.9_v1.1.png", "REJECT", ["chinese_wall_sign_学堂趣事录"]),
        "DA4": ("A001_DA4_PRODUCT_StyleB_V3.9_v1.1.png", "PASS", []),
        "DA5": ("A001_DA5_PRODUCT_StyleB_V3.9_v1.1.png", "REVISE", ["mizuno_unclear", "uwabaki"]),
        "TAIL": ("A001_TAIL_PRODUCT_StyleB_V3.9_v1.1.png", "REVISE", ["blackboard_text", "l0_drift"]),
        "DB1": ("A001_DB1_PRODUCT_StyleB_V3.9_v1.0.png", "PASS", []),
    }
    for shot, (fname, verdict, reasons) in seeds.items():
        set_frame(case, shot, fname, verdict, canonical=(verdict == "PASS"), reasons=reasons, auditor="visual-auditor")
    print(f"initialized {manifest_path(case)}")
    return 0


def cmd_show(case: str) -> int:
    data = load(case)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Illustration canon manifest")
    ap.add_argument("--case", default="A001")
    ap.add_argument("--init-a001", action="store_true", help="Seed A001 from audit")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--set", nargs=4, metavar=("SHOT", "FILE", "VERDICT", "CANONICAL"), help="0/1 canonical")
    args = ap.parse_args()
    if args.init_a001:
        return cmd_init_a001()
    if args.set:
        shot, fname, verdict, canon = args.set
        set_frame(args.case.upper(), shot.upper(), fname, verdict.upper(), canonical=canon == "1")
        return 0
    if args.show:
        return cmd_show(args.case.upper())
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
