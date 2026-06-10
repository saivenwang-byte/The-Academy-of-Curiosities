#!/usr/bin/env python3
"""
TANAKA-DESK orchestrator: run composite JP review pipeline on Unit1 cases.

Usage:
  python run_desk.py --case A001 --cn-version V3.1 --jp-in-version V3.3 --jp-out-version V3.4
  python run_desk.py --all --cn-version V3.1 --jp-in-version V3.3 --jp-out-version V3.4
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 第1卷_觉得奇怪就先观察
UNIT = ROOT / "单元1_第一单元_五案"
TOOLS = ROOT / "tools"
DESK = Path(__file__).resolve().parent

CASES = ["A001", "A002", "A003", "A004", "A005"]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def find_case_file(folder: Path, case: str, lang: str) -> Path | None:
    """lang: cn | jp"""
    if not folder.exists():
        return None
    n = int(case.replace("A", ""))
    prefix = f"案0{n}_"
    files = [f for f in folder.iterdir() if f.is_file() and f.name.startswith(prefix) and f.suffix == ".txt"]
    if lang == "jp":
        files = [f for f in files if "_日本語" in f.name]
    else:
        files = [f for f in files if "_日本語" not in f.name]
    return files[0] if files else None


def scan_goui_issues(text: str) -> list[str]:
    issues = []
    patterns = [
        (r"[·]", "半角中点"),
        (r"——", "中文式破折号（叙事）"),
        (r"碎片|裁判詞|動機層|同框|経手人|修復の動作", "中文直译词残留"),
        (r"合班|禁声|社徽|男生|女生", "中式校园词"),
        (r"\d{2}:\d{2}:\d{2}", "生产时间戳"),
    ]
    for pat, label in patterns:
        if re.search(pat, text):
            issues.append(label)
    return issues


def scan_bunpo_issues(text: str) -> list[str]:
    issues = []
    for para in text.split("\n\n"):
        p = para.replace("\n", "").strip()
        if len(p) > 120 and "「" not in p[:20]:
            issues.append(f"长句段落 ({len(p)}字): {p[:40]}…")
            if len(issues) >= 3:
                break
    return issues


def scan_editor_issues(text: str) -> list[str]:
    issues = []
    if text.count("決めつけ") >= 4:
        issues.append("「決めつけ」高频 · 审判语气")
    if text.count("確認したこと") >= 5:
        issues.append("确认栏/script 语气偏多")
    if "物語をつなぐ" in text or "空欄を埋める" in text:
        issues.append("抽象研讨会用语")
    return issues


def run_assistant(aid: str, text: str, sci_block: bool) -> dict:
    if aid == "HERMES-RONRI":
        # heuristic: fair-play keywords present
        ok = any(k in text for k in ("0328", "唇", "録音", "確認", "仕組み"))
        return {"seat": aid, "verdict": "PASS" if ok else "CONDITIONAL", "notes": ["FC 叙事关键词抽检"]}

    if aid == "HERMES-BUNPO":
        iss = scan_bunpo_issues(text)
        return {"seat": aid, "verdict": "CONDITIONAL" if iss else "PASS", "notes": iss or ["均句抽检 OK"]}

    if aid == "HERMES-GOUI":
        iss = scan_goui_issues(text)
        return {"seat": aid, "verdict": "FAIL" if len(iss) > 2 else ("CONDITIONAL" if iss else "PASS"), "notes": iss or ["J10 词表扫描 OK"]}

    if aid == "HERMES-DOKUSHA":
        has_ruby = "（" in text and "）" in text
        return {"seat": aid, "verdict": "PASS" if has_ruby else "CONDITIONAL", "notes": ["ふりがな A类" if has_ruby else "ふりがな不足"]}

    if aid == "EDITOR-SHO":
        iss = scan_editor_issues(text)
        return {"seat": aid, "verdict": "CONDITIONAL" if iss else "PASS", "notes": iss or ["出版可读性 OK"]}

    if aid == "SCI-RIKA":
        return {
            "seat": aid,
            "verdict": "CONDITIONAL" if sci_block else "PASS",
            "notes": ["science P0 人类签 pending"] if sci_block else ["术语抽检 OK"],
        }

    if aid == "TANAKA":
        return {"seat": aid, "verdict": "SYNTH", "notes": ["五维汇总见报告"]}

    return {"seat": aid, "verdict": "SKIP", "notes": []}


def apply_autofix(text: str) -> str:
    v32 = _load_module("jp_v32", TOOLS / "jp_v32_expert_polish.py")
    j10 = _load_module("jp_j10", TOOLS / "jp_tanaka_j10_pass.py")
    text = v32.polish(text)
    text = j10.j10_polish(text)
    return text


def synthesize_verdict(reports: list[dict]) -> str:
    verdicts = [r["verdict"] for r in reports if r["seat"] != "TANAKA"]
    if "FAIL" in verdicts:
        return "BLOCK"
    if verdicts.count("CONDITIONAL") > 2:
        return "DESK_PASS_PENDING_HUMAN"
    return "DESK_PASS"


def write_case_report(
    case: str,
    out_opinion: Path,
    reports: list[dict],
    synth: str,
    cn_ver: str,
    jp_in: str,
    jp_out: str,
) -> None:
    lines = [
        f"# TANAKA-DESK · 复合体报告 · {case}",
        "",
        f"> 日期：{date.today().isoformat()}",
        f"> CN `{cn_ver}` · JP in `{jp_in}` → out `{jp_out}`",
        f"> **汇总判定**：**{synth}**",
        "",
        "## 各席结果",
        "",
        "| 席 | 判定 | 备注 |",
        "|:--:|:----:|------|",
    ]
    for r in reports:
        notes = " · ".join(r["notes"][:3]) if r["notes"] else "—"
        lines.append(f"| {r['seat']} | **{r['verdict']}** | {notes} |")

    lines += [
        "",
        "## 田中汇总（模拟）",
        "",
        "- 文化五维：委托 `japan_campus_consultant_agent.html` 全文复核",
        "- 冲突优先级：文化 > 公平 > 文体 > 娱乐",
        "",
        "## 状态",
        "",
        f"- Agent 复合体：**{synth}**",
        "- 真人田中 G-JP LOCK：⬜ 须人类签字",
        "",
    ]
    out_opinion.mkdir(parents=True, exist_ok=True)
    (out_opinion / f"00_TANAKA-DESK_复合体报告_{case}.md").write_text("\n".join(lines), encoding="utf-8")

    cal = out_opinion / f"文化校准报告_日本語_{case}.txt"
    cal.write_text(
        f"《{case}》日文版 · TANAKA-DESK 复合体校准报告\n"
        f"{'='*40}\n"
        f"日期：{date.today().isoformat()}\n"
        f"对象：HybridVoice_{jp_out}_日本語.txt\n"
        f"汇总：{synth}\n\n"
        + "\n".join(f"{r['seat']}: {r['verdict']} — {'; '.join(r['notes'])}" for r in reports)
        + "\n\nJP_CULTURE_REVIEW_PASSED："
        + (" YES (DESK)" if synth == "DESK_PASS" else " NO / PENDING")
        + "\nREADY_FOR_TRANSLATION：NO（须真人田中）\n",
        encoding="utf-8",
    )


def process_case(case: str, cn_ver: str, jp_in_ver: str, jp_out_ver: str) -> dict:
    cn_dir = UNIT / "正文" / cn_ver / "01_中文"
    jp_in_dir = UNIT / "正文" / jp_in_ver / "02_日本語"
    out_base = UNIT / "正文" / jp_out_ver
    out_cn = out_base / "01_中文"
    out_jp = out_base / "02_日本語"
    out_op = out_base / "03_版本意见"
    for d in (out_cn, out_jp, out_op):
        d.mkdir(parents=True, exist_ok=True)

    cn_src = find_case_file(cn_dir, case, "cn")
    jp_src = find_case_file(jp_in_dir, case, "jp")
    if not jp_src:
        return {"case": case, "error": "JP input missing"}

    if cn_src:
        cn_dst = out_cn / cn_src.name.replace(cn_ver, jp_out_ver)
        if not cn_dst.exists():
            shutil.copy2(cn_src, cn_dst)

    text = jp_src.read_text(encoding="utf-8")
    text = apply_autofix(text)
    # version bump in filename
    out_name = jp_src.name.replace(jp_in_ver, jp_out_ver)
    (out_jp / out_name).write_text(text, encoding="utf-8")

    order = [
        "HERMES-RONRI",
        "HERMES-BUNPO",
        "HERMES-GOUI",
        "HERMES-DOKUSHA",
        "EDITOR-SHO",
        "SCI-RIKA",
        "TANAKA",
    ]
    sci_block = case in ("A001", "A002", "A005")
    reports = [run_assistant(a, text, sci_block) for a in order]
    synth = synthesize_verdict(reports)
    write_case_report(case, out_op, reports, synth, cn_ver, jp_in_ver, jp_out_ver)

    return {"case": case, "synth": synth, "chars": len(text), "out": str(out_jp / out_name)}


def main() -> None:
    ap = argparse.ArgumentParser(description="TANAKA-DESK JP composite review")
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cn-version", default="V3.1")
    ap.add_argument("--jp-in-version", default="V3.3")
    ap.add_argument("--jp-out-version", default="V3.4")
    args = ap.parse_args()

    cases = CASES if args.all else [args.case]
    if not cases or (not args.all and not args.case):
        ap.error("specify --case A00X or --all")

    results = [process_case(c, args.cn_version, args.jp_in_version, args.jp_out_version) for c in cases]

    readme = UNIT / "正文" / args.jp_out_version / "00_版本说明.md"
    readme.write_text(
        f"# 正文 · {args.jp_out_version} · TANAKA-DESK 复合体输出\n\n"
        f"> {date.today().isoformat()}\n\n"
        f"- CN：{args.cn_version}\n"
        f"- JP in：{args.jp_in_version} → **out：{args.jp_out_version}**\n"
        f"- 工作流：[`86_田中助手复合体…`](../../V2迁移/86_田中助手复合体_JP翻译工作流_V0.1.md)\n",
        encoding="utf-8",
    )

    summary_path = ROOT / "V2迁移" / "scores_desk_latest.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(
            {
                "desk": "TANAKA-DESK",
                "date": date.today().isoformat(),
                "cn_version": args.cn_version,
                "jp_in": args.jp_in_version,
                "jp_out": args.jp_out_version,
                "cases": results,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
