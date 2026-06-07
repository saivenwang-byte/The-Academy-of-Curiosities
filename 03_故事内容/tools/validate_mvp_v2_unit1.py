#!/usr/bin/env python3
"""MVP V2 Unit1 machine gate — exit 0 = pass, 1 = hard fail.

Usage:
  python 03_故事内容/tools/validate_mvp_v2_unit1.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BODY = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"
MVP = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/05_出版成果/MVP_V2_20260608"
ILLUS = MVP / "03_插图"
SCORES = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移/scores_mvp_latest.json"
MIGRATION = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移"

CN_MIN = 3000
JP_MIN = 4000
PNG_MIN_TOTAL = 10
PNG_MIN_PER_CASE = 2
EXPERT_MIN = 9.5
READER_MIN = 9.5
P0_JUMP_MAX = 5.0
CASE_SCORE_MIN = 9.5

CN_FILES = sorted(BODY.glob("案0*_HybridVoice_V2.0.txt"))
JP_FILES = sorted(BODY.glob("案0*_HybridVoice_V2.0_日本語.txt"))

PDF_JP = MVP / "学堂趣事录_第1单元_MVP试读_V2.0_20260608.pdf"
PDF_CN = MVP / "学堂趣事录_CN_第1单元_MVP试读_V2.0_20260608.pdf"
PDF_FULL_CN = MVP / "学堂趣事录_第1单元_读者试读_FULL_V2.0.pdf"
PPT = MVP / "第1单元_MVP路演_V2.0_20260608.pptx"


def count_cn_narrative(raw: str) -> int:
    starts = []
    for pat in [r"^序\s*[·・]", r"^[一二三四五六]、"]:
        m = re.search(pat, raw, re.M)
        if m:
            starts.append(m.start())
    if starts:
        raw = raw[min(starts) :]
    for marker in ["【语感编辑", "---\n【", "（案"]:
        idx = raw.find(marker)
        if idx > 0:
            raw = raw[:idx]
    raw = re.sub(r"\*\*", "", raw)
    return len(re.findall(r"[\u4e00-\u9fff]", raw))


def count_jp_narrative(raw: str) -> int:
    starts = []
    for pat in [r"^序\s*[·・]", r"^(序・|一、|二、|三、|四、|五、)"]:
        m = re.search(pat, raw, re.M)
        if m:
            starts.append(m.start())
    if starts:
        raw = raw[min(starts) :]
    for marker in ["【E04", "【日本語", "---\n【", "（事件", "（案"]:
        idx = raw.find(marker)
        if idx > 0:
            raw = raw[:idx]
    raw = re.sub(r"\s+", "", raw)
    return len(
        re.findall(
            r"[\u3040-\u30ff\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]",
            raw,
        )
    )


def narrative_slice(raw: str, ratio: float = 0.8) -> str:
    end = int(len(raw) * ratio)
    for marker in ["---\n【", "（案", "【读者可以试"]:
        idx = raw.find(marker)
        if 0 < idx < end:
            end = idx
    return raw[:end]


def check_editor_pollution(text: str) -> list[str]:
    hits = []
    if re.search(r"^### SC-\d+", text, re.M):
        hits.append("### SC-XX header in narrative")
    fc = re.findall(r"【FC-\d+[^】]*】", text)
    if fc:
        hits.append(f"FC tags: {', '.join(fc[:5])}")
    inline_fc = re.findall(r"(?<![【\w])FC-\d+", text)
    if inline_fc:
        hits.append(f"inline FC refs: {', '.join(inline_fc[:5])}")
    return hits


def png_counts() -> dict:
    all_png = list(ILLUS.rglob("*.png")) if ILLUS.exists() else []
    by_case: dict[str, int] = {}
    for i in range(1, 6):
        case_dir = ILLUS / f"案0{i}"
        n = len(list(case_dir.glob("*.png"))) if case_dir.exists() else 0
        by_case[f"A00{i}"] = n
    return {
        "total": len(all_png),
        "by_case": by_case,
        "per_case_ok": all(v >= PNG_MIN_PER_CASE for v in by_case.values()),
    }


def weakest_dimension(summary: dict) -> str:
    dims = []
    if summary["cn"]["fail"]:
        dims.append(("cn", len(summary["cn"]["fail"])))
    if summary["jp"]["fail"]:
        dims.append(("jp", len(summary["jp"]["fail"])))
    if summary["deliverables"]["fail"]:
        dims.append(("pdf", len(summary["deliverables"]["fail"])))
    if summary["illustrations"]["fail"]:
        dims.append(("illustration", len(summary["illustrations"]["fail"])))
    if summary["editor_pollution"]["fail"]:
        dims.append(("editor_pollution", len(summary["editor_pollution"]["fail"])))
    if summary["scores"]["fail"]:
        dims.append(("scores", len(summary["scores"]["fail"])))
    if summary["jp_moa"]["fail"]:
        dims.append(("jp_moa", len(summary["jp_moa"]["fail"])))
    if not dims:
        return "none"
    dims.sort(key=lambda x: -x[1])
    return dims[0][0]


def main() -> int:
    summary: dict = {
        "baseline_commit": "f95da38",
        "cn": {"pass": [], "fail": [], "chars": {}},
        "jp": {"pass": [], "fail": [], "chars": {}},
        "deliverables": {"pass": [], "fail": []},
        "illustrations": {"pass": [], "fail": [], "counts": {}},
        "editor_pollution": {"pass": [], "fail": []},
        "scores": {"pass": [], "fail": [], "values": {}},
        "jp_moa": {"pass": [], "fail": []},
        "weakest": "",
        "pass": False,
    }

    # CN bodies
    if len(CN_FILES) != 5:
        summary["cn"]["fail"].append(f"expected 5 CN files, got {len(CN_FILES)}")
    for f in CN_FILES:
        n = count_cn_narrative(f.read_text(encoding="utf-8"))
        summary["cn"]["chars"][f.name] = n
        if n >= CN_MIN:
            summary["cn"]["pass"].append(f.name)
        else:
            summary["cn"]["fail"].append(f"{f.name}: {n} < {CN_MIN} CJK")

    # JP bodies
    if len(JP_FILES) != 5:
        summary["jp"]["fail"].append(f"expected 5 JP files, got {len(JP_FILES)}")
    for f in JP_FILES:
        n = count_jp_narrative(f.read_text(encoding="utf-8"))
        summary["jp"]["chars"][f.name] = n
        if n >= JP_MIN:
            summary["jp"]["pass"].append(f.name)
        else:
            summary["jp"]["fail"].append(f"{f.name}: {n} < {JP_MIN} kana/CJK")

    # PDF/PPT
    for label, path in [
        ("PDF_JP", PDF_JP),
        ("PDF_CN", PDF_CN),
        ("PDF_FULL_CN", PDF_FULL_CN),
        ("PPT", PPT),
    ]:
        if path.exists() and path.stat().st_size > 1000:
            summary["deliverables"]["pass"].append(label)
        else:
            summary["deliverables"]["fail"].append(f"{label} missing or empty: {path.name}")

    # Illustrations
    png = png_counts()
    summary["illustrations"]["counts"] = png
    if png["total"] >= PNG_MIN_TOTAL:
        summary["illustrations"]["pass"].append(f"total_png={png['total']}")
    else:
        summary["illustrations"]["fail"].append(
            f"total_png={png['total']} < {PNG_MIN_TOTAL}"
        )
    if png["per_case_ok"]:
        summary["illustrations"]["pass"].append("per_case>=2")
    else:
        bad = {k: v for k, v in png["by_case"].items() if v < PNG_MIN_PER_CASE}
        summary["illustrations"]["fail"].append(f"per_case low: {bad}")

    # Editor pollution (first 80% narrative)
    for f in CN_FILES:
        raw = f.read_text(encoding="utf-8")
        hits = check_editor_pollution(narrative_slice(raw))
        if hits:
            summary["editor_pollution"]["fail"].append(f"{f.name}: {'; '.join(hits)}")
        else:
            summary["editor_pollution"]["pass"].append(f.name)

    # Scores file
    if SCORES.exists():
        data = json.loads(SCORES.read_text(encoding="utf-8"))
        expert = float(data.get("卷专家", data.get("expert_avg", 0)))
        reader = float(data.get("卷读者", data.get("reader_avg", 0)))
        p0 = float(data.get("P0_jump_pct", data.get("p0_jump_pct", 100)))
        summary["scores"]["values"] = {
            "卷专家": expert,
            "卷读者": reader,
            "P0_jump_pct": p0,
        }
        if expert >= EXPERT_MIN:
            summary["scores"]["pass"].append(f"expert={expert}")
        else:
            summary["scores"]["fail"].append(f"expert={expert} < {EXPERT_MIN}")
        if reader >= READER_MIN:
            summary["scores"]["pass"].append(f"reader={reader}")
        else:
            summary["scores"]["fail"].append(f"reader={reader} < {READER_MIN}")
        if p0 <= P0_JUMP_MAX:
            summary["scores"]["pass"].append(f"P0_jump={p0}%")
        else:
            summary["scores"]["fail"].append(f"P0_jump={p0}% > {P0_JUMP_MAX}%")
        cases = data.get("cases", {})
        for cid in ["A001", "A002", "A003", "A004", "A005"]:
            if cid not in cases:
                summary["scores"]["fail"].append(f"{cid}: missing in scores")
                continue
            ce = float(cases[cid].get("expert", 0))
            cr = float(cases[cid].get("reader", 0))
            if ce >= CASE_SCORE_MIN and cr >= CASE_SCORE_MIN:
                summary["scores"]["pass"].append(f"{cid}={ce}/{cr}")
            else:
                if ce < CASE_SCORE_MIN:
                    summary["scores"]["fail"].append(
                        f"{cid} expert={ce} < {CASE_SCORE_MIN}"
                    )
                if cr < CASE_SCORE_MIN:
                    summary["scores"]["fail"].append(
                        f"{cid} reader={cr} < {CASE_SCORE_MIN}"
                    )
    else:
        summary["scores"]["fail"].append(f"missing {SCORES.relative_to(REPO)}")

    # JP MoA-lite recorded per case
    moa_path = MIGRATION / "mvp_jp_moa_lite.json"
    if moa_path.exists():
        moa = json.loads(moa_path.read_text(encoding="utf-8"))
        cases = moa.get("cases", {})
        for cid in ["A001", "A002", "A003", "A004", "A005"]:
            if cid in cases and cases[cid].get("status") == "MVP-JP-FULL":
                if cases[cid].get("moa_lite_recorded"):
                    summary["jp_moa"]["pass"].append(cid)
                else:
                    summary["jp_moa"]["fail"].append(f"{cid}: moa_lite missing")
            else:
                summary["jp_moa"]["fail"].append(f"{cid}: not MVP-JP-FULL")
    else:
        summary["jp_moa"]["fail"].append(f"missing {moa_path.relative_to(REPO)}")

    summary["weakest"] = weakest_dimension(summary)
    hard_fail = any(
        [
            summary["cn"]["fail"],
            summary["jp"]["fail"],
            summary["deliverables"]["fail"],
            summary["illustrations"]["fail"],
            summary["editor_pollution"]["fail"],
            summary["scores"]["fail"],
            summary["jp_moa"]["fail"],
        ]
    )
    summary["pass"] = not hard_fail

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
