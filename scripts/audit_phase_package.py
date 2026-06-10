#!/usr/bin/env python3
"""Audit complete product phase packages — Agent self-review before reporting.

Usage:
  python scripts/audit_phase_package.py --phase P0
  python scripts/audit_phase_package.py --phase P1
  python scripts/audit_phase_package.py --phase P2
  python scripts/audit_phase_package.py --phase P3
  python scripts/audit_phase_package.py --all
"""

from __future__ import annotations

import argparse
import glob
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Check:
    phase: str
    label: str
    path: Path
    kind: str = "file"  # file | dir | glob | min_bytes
    min_bytes: int = 0


def checks() -> list[Check]:
    vol1 = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察"
    unit1 = vol1 / "单元1_第一单元_五案"
    trial = vol1 / "薄样张_试读"
    sample = vol1 / "样章包"
    formal = vol1 / "正式版"
    return [
        # P0
        Check("P0", "正典门禁", ROOT / "00_项目总览/00_正典门禁_2026-06-04.md"),
        Check("P0", "P0对齐清单", ROOT / "00_项目总览/正典对齐清单_P0_2026-06-05.md"),
        Check("P0", "README", ROOT / "README.md"),
        Check("P0", "CLAUDE", ROOT / "CLAUDE.md"),
        Check("P0", "academy-engine Skill", ROOT / ".cursor/skills/academy-engine/SKILL.md"),
        Check("P0", "正典文件索引", ROOT / "00_项目总览/正典文件索引.md"),
        Check("P0", "SSOT 登记册", unit1 / "00_正本登记册_V1.0.md"),
        Check("P0", "SSOT gate script", ROOT / "scripts/vol1_ssot_gate.py"),
        # P1
        Check("P1", "单元1 导航", unit1 / "00_单元导航.md"),
        Check("P1", "A001 正典指针", unit1 / "A001/00_正典指针.md"),
        Check("P1", "A001 JP 正文", unit1 / "A001/01_正文/案01_全班都听见了他的声音_HybridVoice_V3.8_日本語.txt"),
        Check("P1", "薄样张 README", trial / "README.md"),
        Check("P1", "NanoBanana prompts", trial / "01_NanoBanana_成图提示词_V1.0.md"),
        Check("P1", "试读脚本", trial / "02_试读脚本_主持人版_V1.0.md"),
        Check("P1", "问卷 JP", trial / "03_问卷_儿童家长_日本語_V1.0.md"),
        Check("P1", "募集 flyer HTML", trial / "04_試読募集フライヤー_日本語_V1.0.html"),
        Check("P1", "build kid PDF", trial / "tools/build_kid_trial_pdf.py"),
        Check("P1", "build investor PPT", trial / "tools/build_investor_deck_16x9.py"),
        Check("P1", "案① JP 正文", sample / "04_样章_序+案01_正文_日本語.txt"),
        Check("P1", "V-S01 插图", sample / "插图/V-S01_侧廊海报.png"),
        Check("P1", "试读 PDF", trial / "PDF", "dir"),
        Check("P1", "试读 PDF 文件", trial / "PDF", "glob_pdf"),
        # P2
        Check("P2", "样章总清单", sample / "00_样章包总清单.md"),
        Check("P2", "序+案01 CN", sample / "04_样章_序+案01_正文_HybridVoice.txt"),
        Check("P2", "瑆日记", sample / "05_陸瑆日记页_样章.txt"),
        Check("P2", "线索卡", sample / "07_线索卡_设计稿.md"),
        Check("P2", "实验页", sample / "12_案01_家庭实验页_样章.txt"),
        Check("P2", "C03 自检", sample / "11_自检_C03验收.md"),
        Check("P2", "试读协议", sample / "10_试读协议与反馈表.md"),
        Check("P2", "V-S01 prompt", sample / "插图/prompts_V-S01.md"),
        Check("P2", "build sample PDF script", sample / "tools/build_sample_reading_pdf.py"),
        # P3
        Check("P3", "正式版 正本 CN", formal / "01_正本", "dir"),
        Check("P3", "正式版 笔记", formal / "03_笔记", "dir"),
        Check("P3", "正式版 插画 tools", formal / "02_插画/tools/generate_vol1_illustrations.py"),
        Check("P3", "出版成果 tools", formal / "05_出版成果/tools/build_expert_publication_pack.py"),
        Check("P3", "出版成果目录", formal / "05_出版成果", "dir"),
        Check("P3", "出版 PDF", formal / "05_出版成果", "glob_pub_pdf"),
    ]


def resolve(c: Check) -> tuple[bool, str]:
    p = c.path
    if c.kind == "file":
        if not p.is_file():
            return False, f"missing file: {p.relative_to(ROOT)}"
        if c.min_bytes and p.stat().st_size < c.min_bytes:
            return False, f"too small: {p.relative_to(ROOT)}"
        return True, "ok"
    if c.kind == "dir":
        if not p.is_dir():
            return False, f"missing dir: {p.relative_to(ROOT)}"
        return True, "ok"
    if c.kind == "glob_pdf":
        hits = list(p.glob("*薄样张*日本語*.pdf")) + list(p.glob("*薄样张*.pdf"))
        if not hits:
            return False, f"no kid trial PDF in {p.relative_to(ROOT)}"
        if hits[0].stat().st_size < 100_000:
            return False, f"PDF too small: {hits[0].name}"
        return True, hits[0].name
    if c.kind == "glob_pub_pdf":
        hits = list(p.glob("*正式出版成果*日本語*.pdf"))
        if not hits:
            return False, f"no expert PDF in {p.relative_to(ROOT)}"
        return True, hits[0].name
    return False, "unknown kind"


def run_phase(phase: str) -> int:
    phase = phase.upper()
    subset = [c for c in checks() if c.phase == phase]
    if not subset:
        print(f"Unknown phase: {phase}", file=sys.stderr)
        return 2
    fails: list[str] = []
    oks: list[str] = []
    for c in subset:
        ok, msg = resolve(c)
        line = f"[{'PASS' if ok else 'FAIL'}] {c.label}: {msg}"
        print(line)
        if ok:
            oks.append(c.label)
        else:
            fails.append(line)
    print()
    print(f"=== {phase} · {len(oks)}/{len(subset)} PASS ===")
    if fails:
        print("FAILURES:")
        for f in fails:
            print(f"  {f}")
        print("\nFix missing items before reporting phase complete.")
        return 1
    print(f"Phase {phase} package audit: PASS")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit complete product phase packages")
    ap.add_argument("--phase", choices=["P0", "P1", "P2", "P3", "p0", "p1", "p2", "p3"])
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if args.all:
        rc = 0
        for ph in ("P0", "P1", "P2", "P3"):
            print(f"\n{'='*60}\n{ph}\n{'='*60}")
            if run_phase(ph) != 0:
                rc = 1
        return rc
    if not args.phase:
        ap.print_help()
        return 2
    return run_phase(args.phase)


if __name__ == "__main__":
    raise SystemExit(main())
