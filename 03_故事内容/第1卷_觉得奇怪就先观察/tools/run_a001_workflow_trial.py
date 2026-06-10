#!/usr/bin/env python3

"""A001 workflow trial — run gates in order until PASS or BLOCKED.



Usage (from repo root):

  python "03_故事内容/第1卷_觉得奇怪就先观察/tools/run_a001_workflow_trial.py"

  python "03_故事内容/第1卷_觉得奇怪就先观察/tools/run_a001_workflow_trial.py" --preview-ab

"""



from __future__ import annotations



import argparse

import re

import subprocess

import sys

from dataclasses import dataclass

from pathlib import Path



VOL1 = Path(__file__).resolve().parents[1]

REPO = VOL1.parents[1]

UNIT = VOL1 / "单元1_第一单元_五案"

A001 = UNIT / "A001"

JP_V39 = A001 / "01_正文" / "案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt"

STYLE_DEMO_AUDIT = A001 / "03_插画/STYLE_DEMO/00_STYLE_DEMO_审计_V1.0.md"

ARCHIVED_PILOT = A001 / "04_样张/E20_pilot_A001_V3.8_20260609/00_ARCHIVED.md"

PREFLIGHT = VOL1 / "tools/workflow_preflight.py"





@dataclass

class Step:

    phase: str

    gate: str

    status: str  # PASS | FAIL | BLOCKED_HUMAN | SKIP

    detail: str





def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str]:

    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    out = (r.stdout or "") + (r.stderr or "")

    return r.returncode, out.strip()





def check_style_demo_gcast() -> str:

    if not STYLE_DEMO_AUDIT.is_file():

        return "UNKNOWN"

    text = STYLE_DEMO_AUDIT.read_text(encoding="utf-8")

    if "G-CAST 人头" in text and "❌" in text:

        return "FAIL"

    if "G-CAST" in text and "✅" in text:

        return "PASS"

    return "FAIL"





def run_preflight_step(preview: bool) -> tuple[int, str]:

    cmd = [sys.executable, str(PREFLIGHT), "--mode", "produce", "--phase", "default", "--case", "A001"]

    return run_cmd(cmd, REPO)





def trial(preview_ab: bool) -> int:

    steps: list[Step] = []



    # Phase 1 CN

    code, out = run_cmd([sys.executable, str(REPO / "scripts/vol1_ssot_gate.py"), "--case", "A001"], REPO)

    cn_ok = code == 0 and "7/7 PASS" in out

    steps.append(Step("1", "CN + SSOT pointer", "PASS" if cn_ok else "FAIL", "ssot_gate 7/7 PASS" if cn_ok else "ssot_gate FAIL"))

    if not cn_ok:

        _print_report(steps)

        return 1



    # M0-A lint

    lint = VOL1 / "tools/jp_translation_dept/lint_jp_corruption.py"

    code, out = run_cmd([sys.executable, str(lint), str(JP_V39)], REPO)

    steps.append(Step("2", "M0-A lint", "PASS" if code == 0 else "FAIL", "lint_jp_corruption PASS" if code == 0 else "lint FAIL"))

    if code != 0:

        _print_report(steps)

        return 1



    # produce preflight: 编+导 PASS + 译部 PASS/RETURN（不卡 M0-B）

    pf_code, pf_out = run_preflight_step(preview_ab)

    if pf_code == 0:

        steps.append(Step("2-5", "workflow preflight (produce)", "PASS", "编+导 + 译部 PASS"))

    elif pf_code == 1:

        m = re.search(r"RETURN:\s*(\S+)", pf_out)

        detail = m.group(1) if m else pf_out.splitlines()[-1][:80]

        steps.append(Step("2-5", "workflow preflight (produce)", "FAIL", f"RETURN {detail}"))

        _print_report(steps)

        return 1

    else:

        steps.append(Step("2-5", "workflow preflight (produce)", "FAIL", pf_out.splitlines()[-1][:120]))

        _print_report(steps)

        return 1



    # G-CAST DEMO (post-sign audit of existing output)

    gcast = check_style_demo_gcast()

    steps.append(Step("5", "STYLE DEMO G-CAST", gcast, "see 00_STYLE_DEMO audit"))

    if gcast == "FAIL" and not preview_ab:

        _print_report(steps)

        return 1



    # PDF archived

    if ARCHIVED_PILOT.is_file():

        steps.append(Step("7", "04 sample PDF", "SKIP", "V3.8 pilot ARCHIVED; rebuild after G-AB-JP"))

    else:

        steps.append(Step("7", "04 sample PDF", "BLOCKED_HUMAN", "not ready"))



    steps.append(Step("8", "G-AB-FULL", "BLOCKED_HUMAN", "needs illustrations + sample PDF + G-AB-JP"))

    steps.append(Step("9", "05 layout", "BLOCKED_HUMAN", "needs G-AB-FULL PASS"))



    _print_report(steps)

    if any(s.status == "FAIL" for s in steps):

        return 1

    if any(s.status == "BLOCKED_HUMAN" for s in steps) and not preview_ab:

        return 2

    return 0





def _safe(s: str) -> str:

    return s.encode("ascii", "replace").decode("ascii")





def _print_report(steps: list[Step]) -> None:

    print("=== A001 workflow trial ===")

    for s in steps:

        print(f"[{s.status:14}] Phase {s.phase} | { _safe(s.gate)}")

        if s.detail:

            print(f"                 {_safe(s.detail)}")

    print()

    blocked = [s for s in steps if s.status == "BLOCKED_HUMAN"]

    if blocked:

        print(f"First human gate: Phase {blocked[0].phase} | {_safe(blocked[0].gate)}")

    fails = [s for s in steps if s.status == "FAIL"]

    if fails:

        print(f"First FAIL: Phase {fails[0].phase} | {_safe(fails[0].gate)}")





def main() -> int:

    ap = argparse.ArgumentParser()

    ap.add_argument("--preview-ab", action="store_true", help="Deprecated; produce mode no longer blocks on M0-B")

    args = ap.parse_args()

    return trial(args.preview_ab)





if __name__ == "__main__":

    raise SystemExit(main())

