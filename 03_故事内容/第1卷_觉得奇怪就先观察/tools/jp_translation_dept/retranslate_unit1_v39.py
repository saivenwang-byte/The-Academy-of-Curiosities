#!/usr/bin/env python3
"""Translation Dept · Unit1 CN V3.1 → JP V3.9 pipeline.

Steps per case (107 workflow post-translate):
  jp_v32_expert_polish → jp_tanaka_j10_pass → jp_kids_simplify → jp_shinpan_fix
  → fix_jp_m0_batch patterns → run_desk composite report
  → sync to A00X/01_正文 + 正文/V3.9/

Raw CN→JP translation is done by agent/human BEFORE calling --postprocess-only
or by placing files in 正文/V3.9/02_日本語/ then running --postprocess-only --all.

Usage:
  python retranslate_unit1_v39.py --postprocess-only --all
  python retranslate_unit1_v39.py --postprocess-only --case A001
  python retranslate_unit1_v39.py --verify-only --all
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 第1卷_觉得奇怪就先观察
UNIT = ROOT / "单元1_第一单元_五案"
TOOLS = ROOT / "tools"
DESK = TOOLS / "jp_tanaka_desk" / "run_desk.py"
V39 = "V3.9"
CN_VER = "V3.1"
CASES = ["A001", "A002", "A003", "A004", "A005"]

HEADER = """『学堂奇事録』

第1巻・へんなところ、先に見てみよう

> Hybrid Voice JP · **V3.9** · 翻译部全流程重译 · {date} · DESK pending 真人田中

"""


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def case_paths(case: str) -> dict[str, Path]:
    n = int(case.replace("A", ""))
    cn_name = None
    jp_name = None
    for f in (UNIT / case / "01_正文").glob("案0*_*"):
        if "_日本語" not in f.name and f.suffix == ".txt":
            cn_name = f.name
        elif "_日本語" in f.name and "V3.1" not in f.name:
            pass
    cn_src = UNIT / case / "01_正文" / f"案0{n}_" + _slug(case)
    # discover by glob
    cn_g = list((UNIT / case / "01_正文").glob(f"案0{n}_*.txt"))
    cn_g = [f for f in cn_g if "_日本語" not in f.name and "V3.1" in f.name or (
        "_日本語" not in f.name and "HybridVoice" in f.name
    )]
    cn_file = next((f for f in cn_g if "_日本語" not in f.name), None)
    if not cn_file:
        cn_file = list((UNIT / case / "01_正文").glob(f"案0{n}_*.txt"))
        cn_file = [f for f in cn_file if "_日本語" not in f.name][0]

    base = cn_file.stem.rsplit("_HybridVoice", 1)[0]
    jp_out_name = f"{base}_HybridVoice_{V39}_日本語.txt"

    v39_jp = UNIT / "正文" / V39 / "02_日本語" / jp_out_name
    v39_cn = UNIT / "正文" / V39 / "01_中文" / cn_file.name.replace(CN_VER, V39) if CN_VER in cn_file.name else cn_file.name
    case_jp = UNIT / case / "01_正文" / jp_out_name
    return {
        "cn_src": cn_file,
        "jp_v39": v39_jp,
        "jp_case": case_jp,
        "jp_name": jp_out_name,
        "report_dir": UNIT / case / "01_正文" / "_archive" / f"00_翻译部_{V39}",
    }


def _slug(case: str) -> str:
    return ""


def discover(case: str) -> dict[str, Path]:
    n = int(case.replace("A", ""))
    cn_files = [f for f in (UNIT / case / "01_正文").glob(f"案0{n}_*.txt") if "_日本語" not in f.name]
    cn_file = cn_files[0]
    prefix = cn_file.name.split("_HybridVoice")[0]
    jp_name = f"{prefix}_HybridVoice_{V39}_日本語.txt"
    return {
        "cn_src": cn_file,
        "jp_v39": UNIT / "正文" / V39 / "02_日本語" / jp_name,
        "jp_case": UNIT / case / "01_正文" / jp_name,
        "jp_name": jp_name,
        "report_dir": UNIT / case / "01_正文" / "_archive" / f"00_翻译部_{V39}",
        "v39_cn": UNIT / "正文" / V39 / "01_中文" / cn_file.name,
    }


def postprocess_text(text: str) -> str:
    v32 = _load("jp_v32", TOOLS / "jp_v32_expert_polish.py")
    j10 = _load("jp_j10", TOOLS / "jp_tanaka_j10_pass.py")
    kids = _load("jp_kids", TOOLS / "jp_kids_simplify_pass.py")
    shin = _load("jp_shin", TOOLS / "jp_shinpan_fix_pass.py")
    text = v32.polish(text)
    text = j10.j10_polish(text)
    if hasattr(kids, "simplify"):
        text = kids.simplify(text)
    if hasattr(shin, "shinpan_fix"):
        text = shin.shinpan_fix(text)
    return text


def ensure_header(text: str) -> str:
    if "V3.9" in text[:500]:
        return text
    # strip old headers until first ==== or 序
    lines = text.splitlines()
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("序") or line.strip().startswith("一、") or line.strip().startswith("一."):
            body_start = i
            break
    body = "\n".join(lines[body_start:])
    return HEADER.format(date=date.today().isoformat()) + body


def grep_verify(text: str) -> list[str]:
    bad = []
    for pat in [
        r"学校学校",
        r"(?:と学習発表会){2,}",
        r"（[ぁ-んァ-ヶー]+）（[ぁ-んァ-ヶー]+）",
        r"がっどうきょうしつ",
        r"三周前",
        r"案[①②③④⑤]",
        r"淡い一块",
        r"第一案完",
    ]:
        if re.search(pat, text):
            bad.append(pat)
    return bad


def sync_case(case: str, paths: dict[str, Path]) -> None:
    paths["jp_v39"].parent.mkdir(parents=True, exist_ok=True)
    paths["v39_cn"].parent.mkdir(parents=True, exist_ok=True)
    if not paths["v39_cn"].exists():
        shutil.copy2(paths["cn_src"], paths["v39_cn"])
    shutil.copy2(paths["jp_v39"], paths["jp_case"])


def run_desk(case: str) -> dict:
    cmd = [
        sys.executable,
        str(DESK),
        "--case",
        case,
        "--cn-version",
        CN_VER,
        "--jp-in-version",
        V39,
        "--jp-out-version",
        V39,
    ]
    out = subprocess.check_output(
        cmd, text=True, encoding="utf-8", errors="replace", env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    return json.loads(out)[0]


def process_case(case: str) -> dict:
    paths = discover(case)
    if not paths["jp_v39"].exists():
        return {"case": case, "error": f"missing {paths['jp_v39']}"}

    raw = paths["jp_v39"].read_text(encoding="utf-8")
    text = postprocess_text(raw)
    text = ensure_header(text)

    # inline M0-A fixes
    fix_mod = _load("fix_m0", TOOLS / "fix_jp_m0_batch.py")
    text, _ = fix_mod.fix_text(text)

    paths["jp_v39"].write_text(text, encoding="utf-8")
    sync_case(case, paths)

    grep_fail = grep_verify(text)
    desk = run_desk(case)

    manifest = {
        "case": case,
        "jp": str(paths["jp_case"]),
        "chars": len(text),
        "grep_fail": grep_fail,
        "desk": desk.get("synth"),
        "grep_pass": len(grep_fail) == 0,
    }
    paths["report_dir"].mkdir(parents=True, exist_ok=True)
    (paths["report_dir"] / "00_流水线_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def write_version_readme(results: list[dict]) -> None:
    readme = UNIT / "正文" / V39 / "00_版本说明.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# 正文 · {V39} · 翻译部全流程重译",
        "",
        f"> {date.today().isoformat()}",
        "",
        f"- CN 源：`{CN_VER}` · A001–A005",
        f"- 流水线：CN 重译 → MoA polish → J10 → kids → shinpan → M0-A → TANAKA-DESK",
        f"- 分工：[`107_JP翻译台_专家组分工_V1.0.md`](../../V2迁移/107_JP翻译台_专家组分工_V1.0.md)",
        "",
        "## 各案状态",
        "",
        "| 案 | grep | DESK |",
        "|:--:|:----:|:----:|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['case']} | — | **ERROR** |")
        else:
            g = "PASS" if r.get("grep_pass") else "FAIL"
            lines.append(f"| {r['case']} | {g} | {r.get('desk', '—')} |")
    lines += [
        "",
        "## 真人评委",
        "",
        "本版本供 E20 / 真人打分 · Agent DESK ≠ 田中 M0-B 最终签字。",
        "",
    ]
    readme.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--postprocess-only", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()
    cases = CASES if args.all else ([args.case] if args.case else [])
    if not cases:
        ap.error("use --case A00X or --all")

    results = []
    for c in cases:
        if args.verify_only:
            p = discover(c)
            if p["jp_v39"].exists():
                t = p["jp_v39"].read_text(encoding="utf-8")
                results.append({"case": c, "grep_fail": grep_verify(t), "grep_pass": not grep_verify(t)})
            else:
                results.append({"case": c, "error": "missing jp"})
        else:
            results.append(process_case(c))

    write_version_readme(results)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
