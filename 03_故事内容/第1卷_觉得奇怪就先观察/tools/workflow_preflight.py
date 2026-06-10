#!/usr/bin/env python3
"""Vol1 unit1 workflow preflight — produce vs deliver gates.

Usage (repo root):
  python "03_故事内容/第1卷_觉得奇怪就先观察/tools/workflow_preflight.py"
  python ".../workflow_preflight.py" --mode produce
  python ".../workflow_preflight.py" --mode deliver --phase review-pack
  python ".../workflow_preflight.py" --mode produce --phase generate-image --prompt A001/02_分镜头/prompts/DA2.md --case A001

Exit codes (2026-06-11 · 只过/退回，不卡 pending):
  0 PASS
  1 RETURN/FAIL — 退回上一工位或修内容后重跑（含译部须给 PASS/RETURN）
  2 legacy — deliver 模式极少用；produce 模式不产生 exit 2
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
AB_VERDICT = UNIT / "A001/01_正文/_ab_test/G-AB-JP_汇总裁决_A001.md"
UNIT_REVIEW = UNIT / "00_译部分镜审核_单元1_V1.0.md"
UNIT_JOINT = UNIT / "00_导演组编辑组_分镜插画文字版审定_V1.0.md"
GCAST_GATE = VOL1 / "tools/g_cast_prompt_gate.py"
POST_GATE = VOL1 / "tools/illustration_post_gate.py"

VERDICT_PASS_RE = re.compile(r"\bPASS\b|✅|已签|verdict:\s*PASS|_verdict:\s*PASS", re.I)
VERDICT_RETURN_RE = re.compile(r"\bRETURN\b|↩|退回|verdict:\s*RETURN|_verdict:\s*RETURN", re.I)
VERDICT_PENDING_RE = re.compile(r"\bpending\b|⬜|待审|NOT_STARTED|\[ \]", re.I)
SIGNED_RE = re.compile(r"\[x\]|✅|\bPASS\b|signed:\s*true", re.I)
COUNT_PASS_RE = re.compile(r"COUNT_PASS.*?→\s*(.+)$", re.M)


@dataclass
class GateResult:
    gate: str
    status: str  # PASS | RETURN | FAIL | SKIP
    code: str
    detail: str


def _pass(gate: str, detail: str = "ok") -> GateResult:
    return GateResult(gate, "PASS", "OK", detail)


def _return(code: str, gate: str, detail: str) -> GateResult:
    return GateResult(gate, "RETURN", code, detail)


def _fail(code: str, gate: str, detail: str) -> GateResult:
    return GateResult(gate, "FAIL", code, detail)


def _read_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end]
    out: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip()
    return out


def _verdict_from_fm(fm: dict[str, str], key: str) -> str | None:
    v = fm.get(key, "").strip()
    if not v:
        legacy = {"editorial_verdict": "editorial_signed", "translation_verdict": "translation_signed"}
        lk = legacy.get(key)
        if lk and fm.get(lk, "").lower() == "true":
            return "PASS"
        return None
    u = v.upper()
    if u == "PASS" or VERDICT_PASS_RE.fullmatch(v):
        return "PASS"
    if u == "RETURN" or VERDICT_RETURN_RE.search(v):
        return "RETURN"
    if u == "PENDING" or VERDICT_PENDING_RE.search(v):
        return "PENDING"
    return None


def _case_paths(case: str) -> dict[str, Path]:
    base = UNIT / case / "02_分镜头"
    return {
        "gbrief": base / f"00_G-BRIEF_双签_{case}_V1.0.md",
        "director": base / f"00_G-CAST_导演审定表_{case}_V1.0.md",
        "storyboard": base / "00_插画师分镜文字稿_V1.0.md",
    }


def check_editorial_submit(case: str) -> GateResult:
    paths = _case_paths(case)
    gbrief = paths["gbrief"]
    if gbrief.is_file():
        fm = _read_frontmatter(gbrief.read_text(encoding="utf-8"))
        v = _verdict_from_fm(fm, "editorial_verdict")
        if v == "PASS":
            return _pass("Editorial brief submit", f"{case} G-BRIEF editorial PASS")
        if v == "RETURN":
            return _return("EDITORIAL_RETURN", "Editorial brief submit", f"{case} 编+导 RETURN — 修 brief 后重提")
        if v == "PENDING":
            return _return(
                "EDITORIAL_REVIEW_REQUIRED",
                "Editorial brief submit",
                f"{case} 编+导须给出 PASS 或 RETURN（不可留空）",
            )
    if UNIT_JOINT.is_file():
        text = UNIT_JOINT.read_text(encoding="utf-8")
        if re.search(r"编\+导.*?verdict:\s*PASS|编辑部.*?verdict:\s*PASS", text, re.I):
            return _pass("Editorial brief submit", "unit joint editorial PASS")
        if re.search(r"编\+导.*?verdict:\s*RETURN|编辑部.*?RETURN", text, re.I):
            return _return("EDITORIAL_RETURN", "Editorial brief submit", "单元审定 编+导 RETURN")
    return _return(
        "EDITORIAL_REVIEW_REQUIRED",
        "Editorial brief submit",
        f"{case} 设 frontmatter editorial_verdict: PASS 或单元审定 §五 编+导 PASS",
    )


def check_translation_review(case: str) -> GateResult:
    paths = _case_paths(case)
    gbrief = paths["gbrief"]
    if gbrief.is_file():
        fm = _read_frontmatter(gbrief.read_text(encoding="utf-8"))
        v = _verdict_from_fm(fm, "translation_verdict")
        notes = fm.get("return_notes", "") or fm.get("translation_return_notes", "")
        if v == "PASS":
            return _pass("Translation storyboard review", f"{case} 译部 PASS")
        if v == "RETURN":
            return _return(
                "TRANSLATION_REVIEW_RETURN",
                "Translation storyboard review",
                f"{case} 译部 RETURN → 编+导改 brief" + (f" · {notes}" if notes else ""),
            )
        if v == "PENDING" or v is None:
            return _return(
                "TRANSLATION_REVIEW_REQUIRED",
                "Translation storyboard review",
                f"{case} 译部须 48h 内给 PASS 或 RETURN（不可 pending 卡线）",
            )
    if UNIT_REVIEW.is_file():
        text = UNIT_REVIEW.read_text(encoding="utf-8")
        row = re.search(rf"\|\s*{case}\s*\|([^|\n]+)\|([^|\n]+)\|", text)
        if row:
            ed, tr = row.group(1).strip(), row.group(2).strip()
            if VERDICT_RETURN_RE.search(tr):
                return _return(
                    "TRANSLATION_REVIEW_RETURN",
                    "Translation storyboard review",
                    f"{case} 单元审核表 译部 RETURN",
                )
            if VERDICT_PASS_RE.search(tr):
                return _pass("Translation storyboard review", f"{case} 单元审核表 译部 PASS")
            return _return(
                "TRANSLATION_REVIEW_REQUIRED",
                "Translation storyboard review",
                f"{case} 单元审核表 译部须 PASS/RETURN",
            )
    return _return(
        "TRANSLATION_REVIEW_REQUIRED",
        "Translation storyboard review",
        f"{case} 缺 G-BRIEF translation_verdict 或单元审核表行",
    )


def check_m0b_deliver() -> GateResult:
    if not AB_VERDICT.is_file():
        return _return("DELIVER_RETURN_M0B", "M0-B Tanaka sign", "缺 G-AB-JP 汇总裁决 → 退回翻译部")
    text = AB_VERDICT.read_text(encoding="utf-8")
    if re.search(r"M0-B.*✅|M0-B.*PASS", text):
        return _pass("M0-B Tanaka sign", "verdict signed")
    return _return(
        "DELIVER_RETURN_M0B",
        "M0-B Tanaka sign",
        "M0-B 未 PASS → 退回翻译部完成 M0-B（试读 PDF 前）",
    )


def check_g_ab_jp_deliver() -> GateResult:
    if not AB_VERDICT.is_file():
        return _return("DELIVER_RETURN_GAB", "G-AB-JP blind test", "缺 verdict → 退回翻译部")
    text = AB_VERDICT.read_text(encoding="utf-8")
    if "**PASS**" in text and "G-AB-JP" in text and "放行" in text:
        return _pass("G-AB-JP blind test", "verdict PASS")
    return _return(
        "DELIVER_RETURN_GAB",
        "G-AB-JP blind test",
        "G-AB-JP 未 PASS → 退回翻译部修稿重测（试读交付前）",
    )


def check_count_pass(case: str = "A001") -> GateResult:
    director = _case_paths(case)["director"]
    if not director.is_file():
        return _return("GCAST_COUNT_RETURN", "G-CAST COUNT_PASS", "缺导演审定表 → 退回设计部数人头")
    text = director.read_text(encoding="utf-8")
    fm = _read_frontmatter(text)
    if fm.get("count_pass", "").lower() == "true":
        return _pass("G-CAST COUNT_PASS", "frontmatter count_pass true")
    m = COUNT_PASS_RE.search(text)
    if m and SIGNED_RE.search(m.group(1)):
        return _pass("G-CAST COUNT_PASS", "COUNT_PASS signed")
    return _return(
        "GCAST_COUNT_RETURN",
        "G-CAST COUNT_PASS",
        "成图人头未 COUNT_PASS → 退回设计部/导演组复核",
    )


def check_prompt_gate(prompt: Path) -> GateResult:
    if not prompt.is_file():
        p = UNIT / "A001" / "02_分镜头" / prompt
        if p.is_file():
            prompt = p
        else:
            return _fail("GCAST_PROMPT_FAIL", "G-CAST prompt gate", f"missing {prompt}")
    if not GCAST_GATE.is_file():
        return _fail("GCAST_PROMPT_FAIL", "G-CAST prompt gate", "g_cast_prompt_gate.py missing")
    r = subprocess.run(
        [sys.executable, str(GCAST_GATE), str(prompt.resolve())],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return _fail("GCAST_PROMPT_FAIL", "G-CAST prompt gate", out or "prompt gate FAIL")
    return _pass("G-CAST prompt gate", prompt.name)


def check_post_image_gate(case: str, shot: str, filename: str | None) -> GateResult:
    if not POST_GATE.is_file():
        return _fail("ILLUSTRATION_POST_FAIL", "Post-image gate", "illustration_post_gate.py missing")
    cmd = [sys.executable, str(POST_GATE), "--case", case, "--shot", shot]
    if filename:
        cmd.extend(["--file", filename])
    r = subprocess.run(
        cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode != 0:
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return _return("ILLUSTRATION_POST_FAIL", "Post-image manifest gate", out or f"{shot} not PASS in manifest")
    return _pass("Post-image manifest gate", f"{case}/{shot} canonical PASS")


def run_produce(phase: str, prompt: Path | None, case: str, shot: str | None = None, png_file: str | None = None) -> int:
    results: list[GateResult] = []
    results.append(check_editorial_submit(case))
    if results[-1].status != "PASS":
        _print(results, "produce")
        return 1
    results.append(check_translation_review(case))
    if results[-1].status != "PASS":
        _print(results, "produce")
        return 1
    if phase in ("generate-image", "all") and prompt:
        results.append(check_prompt_gate(prompt))
        if results[-1].status != "PASS":
            _print(results, "produce")
            return 1
    if phase in ("post-image", "all") and shot:
        results.append(check_post_image_gate(case, shot.upper(), png_file))
        if results[-1].status != "PASS":
            _print(results, "produce")
            return 1
    _print(results, "produce")
    return 0


def run_deliver(phase: str, case: str) -> int:
    results: list[GateResult] = []
    results.append(check_editorial_submit(case))
    if results[-1].status != "PASS":
        _print(results, "deliver")
        return 1
    results.append(check_translation_review(case))
    if results[-1].status != "PASS":
        _print(results, "deliver")
        return 1
    results.append(check_m0b_deliver())
    if results[-1].status != "PASS":
        _print(results, "deliver")
        return 1
    results.append(check_g_ab_jp_deliver())
    if results[-1].status != "PASS":
        _print(results, "deliver")
        return 1
    if phase in ("review-pack", "all", "trial-deliverable"):
        results.append(check_count_pass(case))
        if results[-1].status != "PASS":
            _print(results, "deliver")
            return 1
    _print(results, "deliver")
    return 0


def _print(results: list[GateResult], mode: str) -> None:
    print(f"=== workflow preflight ({mode}) ===")
    for r in results:
        print(f"[{r.status:14}] {r.code:28} | {r.gate}")
        if r.detail:
            print(f"                 {r.detail}")
    ret = next((r for r in results if r.status == "RETURN"), None)
    if ret:
        print(f"\nRETURN: {ret.code} — {ret.detail}")
    fail = next((r for r in results if r.status == "FAIL"), None)
    if fail:
        print(f"\nFAIL: {fail.code} — {fail.detail}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Vol1 workflow preflight · produce | deliver")
    ap.add_argument(
        "--mode",
        choices=("produce", "deliver"),
        default="produce",
        help="produce=出图并行 · deliver=试读PDF/审阅包",
    )
    ap.add_argument(
        "--phase",
        choices=("default", "generate-image", "post-image", "review-pack", "trial-deliverable", "all"),
        default="default",
    )
    ap.add_argument("--prompt", type=Path, help="Prompt md for generate-image")
    ap.add_argument("--case", default="A001", help="Case id A001–A005")
    ap.add_argument("--shot", help="Shot id DA1/TAIL for post-image gate")
    ap.add_argument("--png-file", help="PNG basename for manifest match")
    ap.add_argument(
        "--preview",
        action="store_true",
        help="Deprecated alias for --mode produce (no M0-B block)",
    )
    args = ap.parse_args()
    mode = "produce" if args.preview else args.mode

    if args.phase == "generate-image" and not args.prompt:
        print("FAIL: --phase generate-image requires --prompt PATH")
        return 1
    if args.phase == "post-image" and not args.shot:
        print("FAIL: --phase post-image requires --shot DA1|DA2|...")
        return 1

    if mode == "produce":
        return run_produce(args.phase, args.prompt, args.case.upper(), args.shot, args.png_file)
    return run_deliver(args.phase, args.case.upper())


if __name__ == "__main__":
    raise SystemExit(main())
