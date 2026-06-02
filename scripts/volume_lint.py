#!/usr/bin/env python3
"""
Per-volume planning lint for 《学堂趣事录》.

Unifies Case Card + Scene Cards + story table row (+ optional scorecard / visuals).

Usage:
  python scripts/volume_lint.py --vol 1
  python scripts/volume_lint.py --vol 2
  python scripts/volume_lint.py --all
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "docs" / "volume_planning"
STORY_TABLE = ROOT / "docs" / "story_database" / "00_story_asset_table.md"
CASE_LINT = ROOT / "scripts" / "case_card_lint.py"
SCENE_LINT = ROOT / "scripts" / "scene_card_lint.py"

VOLUMES: dict[int, dict] = {
    1: {
        "id": "Vol01",
        "case": "volume_01_wet_chair_case_card.md",
        "scene": "volume_01_scene_cards.md",
        "scorecard": "volume_01_scorecard.yaml",
        "visual": True,
        "body": ROOT / "03_故事内容" / "第1卷_总是湿的椅子" / "完整文字稿.txt",
    },
    2: {
        "id": "Vol02",
        "case": "volume_02_eraser_case_card.md",
        "scene": "volume_02_scene_cards.md",
        "scorecard": "volume_02_scorecard.yaml",
        "decisions": "volume_02_decisions_locked.md",
        "body": ROOT / "03_故事内容" / "第2卷_谁偷了橡皮" / "完整文字稿.txt",
    },
}


@dataclass
class VolResult:
    vol: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _run_py(script: Path, args: list[str]) -> int:
    cmd = [sys.executable, str(script), *args]
    return subprocess.run(cmd, cwd=ROOT).returncode


def story_table_has(vol_id: str) -> bool:
    if not STORY_TABLE.is_file():
        return False
    return vol_id in STORY_TABLE.read_text(encoding="utf-8")


def lint_volume(vol: int) -> VolResult:
    r = VolResult(vol=vol)
    cfg = VOLUMES.get(vol)
    if not cfg:
        r.errors.append(f"Vol{vol} 未在 VOLUMES 注册")
        return r

    case_path = PLANNING / cfg["case"]
    scene_path = PLANNING / cfg["scene"]

    if not case_path.is_file():
        r.errors.append(f"缺少 Case Card: {case_path.name}")
    else:
        if _run_py(CASE_LINT, ["--file", str(case_path.relative_to(ROOT)), "-q"]) != 0:
            r.errors.append(f"Case Card lint 失败: {case_path.name}")

    if not scene_path.is_file():
        r.errors.append(f"缺少 Scene Cards: {scene_path.name}")
    else:
        if _run_py(SCENE_LINT, ["--file", str(scene_path.relative_to(ROOT)), "-q"]) != 0:
            r.errors.append(f"Scene Card lint 失败: {scene_path.name}")

    if not story_table_has(cfg["id"]):
        r.errors.append(f"故事总表缺少行: {cfg['id']}")

    scorecard = cfg.get("scorecard")
    if scorecard:
        sp = PLANNING / scorecard
        if not sp.is_file():
            r.warnings.append(f"建议有 scorecard: {scorecard}")

    decisions = cfg.get("decisions")
    if decisions:
        dp = PLANNING / decisions
        if not dp.is_file():
            r.warnings.append(f"Vol2 决策锁定文件缺失: {decisions}")

    body = cfg.get("body")
    if body and body.is_file():
        if _run_py(ROOT / "scripts" / "body_lint.py", ["--file", str(body.relative_to(ROOT))]) != 0:
            r.errors.append(f"正文 body_lint 失败: {body.name}")
    elif body:
        r.warnings.append(f"正文尚未写入: {body.relative_to(ROOT)}")

    if cfg.get("visual"):
        if _run_py(CASE_LINT, ["--visual", "vol1", "-q"]) != 0:
            r.errors.append("Vol1 插图 visual lint 失败")

    return r


def print_result(r: VolResult, quiet: bool) -> None:
    tag = "PASS" if r.ok else "FAIL"
    if not quiet or not r.ok:
        print(f"\n[{tag}] Vol{r.vol:02d}")
    for e in r.errors:
        print(f"  ERROR: {e}")
    if not quiet or r.warnings:
        for w in r.warnings:
            print(f"  WARN:  {w}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint registered volumes")
    parser.add_argument("--vol", type=int, action="append", dest="vols")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    vols = sorted(VOLUMES.keys()) if args.all else (args.vols or [])
    if not vols:
        parser.error("指定 --vol N 或 --all")

    failed = 0
    for v in vols:
        r = lint_volume(v)
        print_result(r, args.quiet)
        if not r.ok:
            failed += 1

    if failed:
        print(f"\n{failed} volume(s) failed.")
        return 1
    if not args.quiet:
        print("\nAll volume checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
