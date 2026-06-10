#!/usr/bin/env python3
"""
Shinpan / trial-voice fix pass: V3.6 JP → V3.7 · doc87 P0 审判腔收尾.

Usage:
  python jp_shinpan_fix_pass.py --all --cn-version V3.1 --jp-in-version V3.6 --jp-out-version V3.7
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

# Safe narrative replacements (EDITOR-SHO · doc87 §5)
REPLACEMENTS: list[tuple[str, str]] = [
    ("確認したこと：", "観察メモ："),
    ("確認したこと……", "観察メモ……"),
    ("「確認したこと：", "「観察メモ："),
    ("ひとつの決めつけに、全部を押し込んではいけない", "ひとつに当てはめて、全部を押し込んではいけない"),
    ("決めつけの言葉は、手順のメモに下げた", "当てはめる言葉は、手順メモには書かなかった"),
    ("物語をつなぐ", "話をつなぐ"),
    ("空欄を埋める", "空白を埋める"),
]

SHINPAN_SCAN = [
    (r"決めつけ", "审判腔 決めつけ"),
    (r"確認したこと", "确认栏语气"),
    (r"物語をつなぐ", "研讨会用语"),
    (r"空欄を埋める", "研讨会用语"),
    (r"裁判", "审判词 裁判"),
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
    return s.startswith("「") or s.startswith("『")


def split_long_paragraphs(text: str, threshold: int = 70) -> tuple[str, int]:
    splits = 0
    out: list[str] = []
    for para in text.split("\n\n"):
        p = para.strip()
        if not p or p.startswith((">", "==")) or is_dialogue_line(p):
            out.append(para)
            continue
        if count_kana(p.replace("\n", "")) <= threshold:
            out.append(para)
            continue
        lines = para.splitlines()
        if len(lines) > 1:
            out.append(para)
            continue
        parts: list[str] = []
        buf = ""
        for seg in re.split(r"(、|。)", p):
            if seg in ("、", "。"):
                buf += seg
                if count_kana(buf) >= 35 and seg == "、":
                    parts.append(buf.rstrip("、"))
                    buf = ""
                continue
            buf += seg
        if buf:
            parts.append(buf)
        if len(parts) > 1:
            splits += 1
            out.append("\n\n".join(x.strip() for x in parts if x.strip()))
        else:
            out.append(para)
    return "\n\n".join(out), splits


def apply_shinpan_fix(text: str) -> tuple[str, dict]:
    stats = {"replacements": {}, "splits": 0}
    for old, new in REPLACEMENTS:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            stats["replacements"][old[:12] + "…"] = n
    text, splits = split_long_paragraphs(text)
    stats["splits"] = splits
    return text, stats


def scan_flags(text: str) -> list[str]:
    found: list[str] = []
    for pat, label in SHINPAN_SCAN:
        if re.search(pat, text):
            found.append(label)
    return found


def bump_header(text: str, jp_in: str, jp_out: str) -> str:
    text = text.replace(jp_in, jp_out)
    note = f"> Hybrid Voice JP・**{jp_out}**・shinpan fix pass・{date.today().isoformat()}・G-JP DRAFT"
    if re.search(r"> Hybrid Voice JP", text):
        text = re.sub(r"> Hybrid Voice JP[^\n]+", note, text, count=1)
    return text


def write_report(case: str, out_op: Path, stats: dict, flags: list[str], cn: str, jp_in: str, jp_out: str) -> None:
    lines = [
        f"# SHINPAN-FIX · 审判腔收尾报告 · {case}",
        "",
        f"> 日期：{date.today().isoformat()}",
        f"> CN `{cn}` · JP `{jp_in}` → `{jp_out}`",
        f"> 依据：doc87 §5 P0 · 插画验收后启动",
        "",
        "## 自动修复",
        "",
    ]
    if stats.get("replacements"):
        for k, v in stats["replacements"].items():
            lines.append(f"- `{k}` × {v}")
    else:
        lines.append("- 句式替换：无命中")
    lines.append(f"- 长段拆分：{stats.get('splits', 0)} 段")
    lines.append("")
    lines.append("## 残留标记")
    lines.append("")
    if flags:
        for f in flags:
            lines.append(f"- {f}")
    else:
        lines.append("- 无")
    lines.append("")
    out_op.mkdir(parents=True, exist_ok=True)
    (out_op / f"00_SHINPAN-FIX_报告_{case}.md").write_text("\n".join(lines), encoding="utf-8")


def process_case(case: str, cn: str, jp_in: str, jp_out: str) -> dict:
    out_base = UNIT / "正文" / jp_out
    out_cn, out_jp, out_op = out_base / "01_中文", out_base / "02_日本語", out_base / "03_版本意见"
    for d in (out_cn, out_jp, out_op):
        d.mkdir(parents=True, exist_ok=True)

    cn_src = find_case_file(UNIT / "正文" / cn / "01_中文", case, "cn")
    jp_src = find_case_file(UNIT / "正文" / jp_in / "02_日本語", case, "jp")
    if not jp_src:
        return {"case": case, "error": "missing JP input"}

    if cn_src:
        shutil.copy2(cn_src, out_cn / cn_src.name.replace(cn, jp_out))

    text = jp_src.read_text(encoding="utf-8")
    text, stats = apply_shinpan_fix(text)
    text = bump_header(text, jp_in, jp_out)
    flags = scan_flags(text)
    out_name = jp_src.name.replace(jp_in, jp_out)
    (out_jp / out_name).write_text(text, encoding="utf-8")
    write_report(case, out_op, stats, flags, cn, jp_in, jp_out)
    return {"case": case, "stats": stats, "flags": flags, "out": str(out_jp / out_name)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cn-version", default="V3.1")
    ap.add_argument("--jp-in-version", default="V3.6")
    ap.add_argument("--jp-out-version", default="V3.7")
    args = ap.parse_args()
    cases = CASES if args.all else [args.case]
    if not cases:
        ap.error("use --all or --case")

    results = [process_case(c, args.cn_version, args.jp_in_version, args.jp_out_version) for c in cases]
    readme = UNIT / "正文" / args.jp_out_version / "00_版本说明.md"
    readme.write_text(
        f"# {args.jp_out_version} · 审判腔收尾 · JP CURRENT（文本轨）\n\n"
        f"> {date.today().isoformat()}\n\n"
        f"- 自 {args.jp_in_version} + `jp_shinpan_fix_pass.py`\n"
        f"- 插画仍绑定 **V3.6**（用户已验收 V3.6.3_USERSTYLE）\n"
        f"- 下一：TANAKA-DESK → V3.8\n",
        encoding="utf-8",
    )
    summary = ROOT / "V2迁移" / f"scores_{args.jp_out_version.lower()}_shinpan.json"
    summary.write_text(json.dumps({"date": date.today().isoformat(), "cases": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
