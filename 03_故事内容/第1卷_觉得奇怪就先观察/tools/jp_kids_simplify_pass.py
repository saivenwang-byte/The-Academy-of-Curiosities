#!/usr/bin/env python3
"""
Kids simplify pass: V3.4 JP → V3.5 · doc81 3.5 naturalness · Plan A internal tool.

Usage:
  python jp_kids_simplify_pass.py --case A001 --cn-version V3.1 --jp-in-version V3.4 --jp-out-version V3.5
  python jp_kids_simplify_pass.py --all --cn-version V3.1 --jp-in-version V3.4 --jp-out-version V3.5
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
CASES = ["A001", "A002", "A003", "A004", "A005"]

# Flag-only patterns (doc81 · EDITOR-SHO · 敬语/审判腔)
KEIGO_PATTERNS: list[tuple[str, str]] = [
    (r"ございます", "敬语 ございます"),
    (r"申し上げ", "敬语 申し上げ"),
    (r"いたします", "敬语 いたします"),
    (r"おっしゃ", "敬语 おっしゃ"),
    (r"参り", "敬语 参り"),
    (r"でござい", "敬语 でござい"),
    (r"であることから", "论文体 であることから"),
    (r"結論として", "论文体 結論として"),
    (r"重要なのは", "AI/论文 hype 句"),
]

SHINPAN_PATTERNS: list[tuple[str, str]] = [
    (r"決めつけ", "审判腔 決めつけ"),
    (r"確認したこと", "确认栏/script 语气"),
    (r"物語をつなぐ", "研讨会用语"),
    (r"空欄を埋める", "研讨会用语"),
    (r"裁判", "审判词 裁判"),
    (r"誰がやった", "重复追问 誰がやった"),
    (r"犯人", "审判词 犯人"),
    (r"修復の動作", "直译 metadata 残留"),
]

KANA_RE = re.compile(r"[ぁ-んァ-ヶー]")


def find_case_file(folder: Path, case: str, lang: str) -> Path | None:
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


def count_kana(s: str) -> int:
    return len(KANA_RE.findall(s))


def is_dialogue_line(line: str) -> bool:
    s = line.strip()
    return s.startswith("「") or s.startswith("『") or (s.startswith("「") and "」" in s)


def fix_punctuation(text: str) -> tuple[str, dict[str, int]]:
    stats = {"em_dash": 0, "halfwidth_dot": 0}
    # half-width middle dot → full-width
    n_dot = text.count("·")
    if n_dot:
        text = text.replace("·", "・")
        stats["halfwidth_dot"] = n_dot
    # Chinese em-dash in narrative → ellipsis (dialogue may keep sparingly)
    def repl_dash(m: re.Match) -> str:
        stats["em_dash"] += 1
        before = m.group(0)
        # trailing clause → period if looks like sentence break
        if before.endswith("——") and m.start() > 0:
            ctx = text[max(0, m.start() - 20) : m.start()]
            if "「" in ctx[-10:]:
                return "……"
        return "……"

    text = re.sub(r"——+", repl_dash, text)
    # lone em dash variants
    text = text.replace("—", "……")
    return text, stats


def split_long_narrative_sentences(text: str, threshold: int = 80) -> tuple[str, int]:
    """Split narrative sentences > threshold kana at 、 or 。 where possible."""
    splits = 0
    lines_out: list[str] = []
    for line in text.splitlines():
        if is_dialogue_line(line) or line.strip().startswith((">", "-", "==")):
            lines_out.append(line)
            continue
        if count_kana(line) <= threshold:
            lines_out.append(line)
            continue
        # try split on 、 after ~40 kana
        parts: list[str] = []
        buf = ""
        for seg in re.split(r"(、|。)", line):
            if seg in ("、", "。"):
                buf += seg
                if count_kana(buf) >= 40 and seg == "、":
                    parts.append(buf.rstrip("、"))
                    buf = ""
                continue
            buf += seg
        if buf:
            parts.append(buf)
        if len(parts) > 1:
            splits += 1
            lines_out.append("\n\n".join(p.strip() for p in parts if p.strip()))
        else:
            lines_out.append(line)
    return "\n".join(lines_out), splits


def scan_flags(text: str) -> dict[str, list[str]]:
    flags: dict[str, list[str]] = {"keigo": [], "shinpan": [], "long_para": []}
    for pat, label in KEIGO_PATTERNS:
        if re.search(pat, text):
            flags["keigo"].append(label)
    for pat, label in SHINPAN_PATTERNS:
        if re.search(pat, text):
            flags["shinpan"].append(label)
    for para in text.split("\n\n"):
        p = para.replace("\n", "").strip()
        if len(p) > 120 and not p.startswith("「"):
            flags["long_para"].append(f"长段 ({len(p)}字): {p[:36]}…")
            if len(flags["long_para"]) >= 5:
                break
    return flags


def apply(text: str) -> tuple[str, dict]:
    """Deterministic kids-simplify fixes."""
    meta: dict = {"punct": {}, "splits": 0}
    text, punct = fix_punctuation(text)
    meta["punct"] = punct
    text, splits = split_long_narrative_sentences(text)
    meta["splits"] = splits
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text, meta


def bump_version_header(text: str, jp_in: str, jp_out: str) -> str:
    text = text.replace(jp_in, jp_out)
    note = (
        f"> Hybrid Voice JP・**{jp_out}**・kids simplify pass・{date.today().isoformat()}・G-JP DRAFT\n"
    )
    if re.search(r"> Hybrid Voice JP", text):
        text = re.sub(r"> Hybrid Voice JP[^\n]+", note.strip(), text, count=1)
    return text


def synthesize_verdict(flags: dict[str, list[str]], meta: dict) -> str:
    n_flags = len(flags.get("keigo", [])) + len(flags.get("shinpan", []))
    n_long = len(flags.get("long_para", []))
    if n_flags >= 4:
        return "KIDS_PENDING_HUMAN"
    if n_flags >= 2 or n_long >= 3:
        return "KIDS_CONDITIONAL"
    if meta.get("punct", {}).get("em_dash", 0) > 0 or meta.get("splits", 0) > 0:
        return "KIDS_SIMPLIFY_PASS"
    return "KIDS_SIMPLIFY_PASS"


def write_case_report(
    case: str,
    out_opinion: Path,
    flags: dict[str, list[str]],
    meta: dict,
    synth: str,
    cn_ver: str,
    jp_in: str,
    jp_out: str,
) -> None:
    lines = [
        f"# KIDS-SIMPLIFY · 儿童简化报告 · {case}",
        "",
        f"> 日期：{date.today().isoformat()}",
        f"> CN `{cn_ver}` · JP in `{jp_in}` → out `{jp_out}`",
        f"> **汇总判定**：**{synth}**",
        f"> 依据：doc81 JP 3.5 · `kids_simplify_ip` · Plan A",
        "",
        "## 自动修复",
        "",
        f"- 中文破折号 **——** → ……/。：{meta.get('punct', {}).get('em_dash', 0)} 处",
        f"- 半角 **·** → **・**：{meta.get('punct', {}).get('halfwidth_dot', 0)} 处",
        f"- 长句拆分（>80 假名叙事）：{meta.get('splits', 0)} 段",
        "",
        "## 标记项（未自动改）",
        "",
    ]
    if flags.get("keigo"):
        lines.append("### 敬语/论文体")
        for f in flags["keigo"]:
            lines.append(f"- {f}")
    else:
        lines.append("- 敬语/论文体：无")
    lines.append("")
    if flags.get("shinpan"):
        lines.append("### 审判腔/研讨会语气")
        for f in flags["shinpan"]:
            lines.append(f"- {f}")
    else:
        lines.append("- 审判腔：无")
    lines.append("")
    if flags.get("long_para"):
        lines.append("### 长段落（>120 字）")
        for f in flags["long_para"]:
            lines.append(f"- {f}")
    else:
        lines.append("- 长段落：抽检 OK")
    lines += [
        "",
        "## 状态",
        "",
        f"- Agent kids simplify：**{synth}**",
        "- 科学词：保留 JP_PROSE_LEXICON · 不幼化",
        "- 下一可选步：TANAKA-DESK 复跑 或 真人田中",
        "",
    ]
    out_opinion.mkdir(parents=True, exist_ok=True)
    (out_opinion / f"00_KIDS-SIMPLIFY_报告_{case}.md").write_text("\n".join(lines), encoding="utf-8")


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
        return {"case": case, "error": "JP input missing", "synth": "ERROR"}

    if cn_src:
        cn_dst = out_cn / cn_src.name.replace(cn_ver, jp_out_ver)
        shutil.copy2(cn_src, cn_dst)

    text = jp_src.read_text(encoding="utf-8")
    text, meta = apply(text)
    text = bump_version_header(text, jp_in_ver, jp_out_ver)
    flags = scan_flags(text)

    out_name = jp_src.name.replace(jp_in_ver, jp_out_ver)
    (out_jp / out_name).write_text(text, encoding="utf-8")

    synth = synthesize_verdict(flags, meta)
    write_case_report(case, out_op, flags, meta, synth, cn_ver, jp_in_ver, jp_out_ver)

    return {
        "case": case,
        "synth": synth,
        "chars": len(text),
        "fixes": meta,
        "flags": {k: len(v) for k, v in flags.items()},
        "out": str(out_jp / out_name),
    }


def write_version_readme(jp_out_ver: str, cn_ver: str, jp_in_ver: str) -> None:
    readme = UNIT / "正文" / jp_out_ver / "00_版本说明.md"
    readme.write_text(
        f"# 第一单元正文 · {jp_out_ver} · **CURRENT（JP 轨）**\n\n"
        f"> {date.today().isoformat()}\n\n"
        f"## 版本摘要\n\n"
        f"- **CN**：同 {cn_ver}（`01_中文/`）\n"
        f"- **JP**：{jp_in_ver} + kids simplify pass（doc81 3.5 自然度）\n"
        f"- **工具**：`tools/jp_kids_simplify_pass.py`\n"
        f"- **03_版本意见**：`00_KIDS-SIMPLIFY_报告_A00X.md`\n\n"
        f"## 流水线位置\n\n"
        f"V3.3 J10 → V3.4 TANAKA-DESK → **{jp_out_ver} KIDS-SIMPLIFY** → 可选 DESK 复跑 → 真人田中\n",
        encoding="utf-8",
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="JP kids simplify pass (Plan A)")
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cn-version", default="V3.1")
    ap.add_argument("--jp-in-version", default="V3.4")
    ap.add_argument("--jp-out-version", default="V3.5")
    args = ap.parse_args()

    cases = CASES if args.all else [args.case]
    if not cases or (not args.all and not args.case):
        ap.error("specify --case A00X or --all")

    results = [process_case(c, args.cn_version, args.jp_in_version, args.jp_out_version) for c in cases]
    write_version_readme(args.jp_out_version, args.cn_version, args.jp_in_version)

    summary_path = ROOT / "V2迁移" / "scores_kids_simplify_latest.json"
    summary_path.write_text(
        json.dumps(
            {
                "pass": "KIDS-SIMPLIFY",
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
