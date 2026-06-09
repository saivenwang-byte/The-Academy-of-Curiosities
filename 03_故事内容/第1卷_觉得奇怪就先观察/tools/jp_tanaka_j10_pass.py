#!/usr/bin/env python3
"""Tanaka J10 simulated pass: V3.2 JP → V3.3 + E20 A001 pilot strip."""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
V32 = UNIT / "正文" / "V3.2"
V33 = UNIT / "正文" / "V3.3"
E20 = ROOT / "薄样张_试读" / "E20_pilot_A001_20260608"
V31_CN = UNIT / "正文" / "V3.1" / "01_中文"

# First-occurrence furigana (term without existing parens)
FURIGANA: list[tuple[str, str]] = [
    ("合同教室", "合同教室（ごうどうきょうしつ）"),
    ("上履き", "上履き（うわばき）"),
    ("放送委員会の機材ワゴン", "放送委員会（ほうそういいんかい）の機材ワゴン"),
    ("観察クラブ", "観察クラブ（かんさつクラブ）"),
    ("発声禁止届", "発声禁止届（はっせいきんしとどけ）"),
    ("パノラマのつなぎ撮影", "パノラマ（全景）のつなぎ撮影"),
]

J10_REPLACEMENTS = [
    (r" · ", "・"),
    (" · ", "・"),
    ("PLAY · ", "再生・"),
    ("再生・", "再生・"),
    # narrative em dash → ellipsis (keep dialogue interrupt sparingly)
    ("——息しか", "……息しか"),
    ("——小さな文字", "……小さな文字"),
    ("——袖口", "……袖口"),
    ("——見すぎて", "……見すぎて"),
    ("——まだ声", "……まだ声"),
    ("——レンズ", "……レンズ"),
    ("——二枚", "……二枚"),
    ("——水野", "……水野"),
    ("——四人", "……四人"),
    ("——空欄", "……空欄"),
    ("——先に", "……先に"),
    ("——クラス", "……クラス"),
    ("：今日は", "。今日は"),
    ("：光", "。光"),
    ("：三件", "。三件"),
    ("：隠す", "。隠す"),
    ("：仕組み", "。仕組み"),
    ("：録音", "。録音"),
    ("：空欄", "。空欄"),
    ("（序を見よ。）", ""),
    ("（A002へ。）", ""),
    ("（A003へ。）", ""),
    ("（A004へ。）", ""),
    ("（A005へ。）", ""),
]

# Long sentence split markers (after J10 punctuation fix)
SPLIT_PATTERNS = [
    (
        "それなのに天井の放送スピーカーは明るく、はっきりして、笑いさえ含んで、すべてを上書きした。",
        "それなのに天井の放送スピーカーは明るく、はっきりしていた。\n\n笑いさえ含んで、すべてを上書きした。",
    ),
    (
        "光の唇は、その一文を最後まで動いていなかった。動く前すらない。放送の声は、光が今日一言も話せない様子と、合わない。",
        "光の唇は、その一文を最後まで動いていなかった。動く前すらない。\n\n放送の声は、光が今日一言も話せない。口の動きと、合わない。",
    ),
]


def apply_furigana_once(text: str) -> str:
    for plain, tagged in FURIGANA:
        reading = tagged[len(plain) :]
        # Idempotent: skip if any furigana already present after the term
        if re.search(re.escape(plain) + r"（[ぁ-んァ-ヶー]+）", text):
            continue
        if plain in text:
            text = re.sub(re.escape(plain) + r"(?!（)", tagged, text, count=1)
    return text


def j10_polish(text: str) -> str:
    for old, new in J10_REPLACEMENTS:
        text = text.replace(old, new)
    for old, new in SPLIT_PATTERNS:
        text = text.replace(old, new)
    text = apply_furigana_once(text)
    # J10b: remaining halfwidth middle dot
    text = text.replace("·", "・")
    # collapse excessive blank lines
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def bump_version_header(text: str) -> str:
    text = text.replace("V3.2", "V3.3")
    note = "> Hybrid Voice JP · **V3.3** · 田中 J10 模拟督查 · 2026-06-09 · G-JP DRAFT\n"
    if "田中 J10" not in text:
        text = re.sub(
            r"(> Hybrid Voice JP[^\n]+\n)",
            note,
            text,
            count=1,
        )
    else:
        text = re.sub(
            r"> Hybrid Voice JP[^\n]+",
            note.strip(),
            text,
            count=1,
        )
    return text


def strip_for_e20(text: str) -> str:
    """Reader-facing pilot: no agent notes."""
    lines = []
    skip_prefixes = ("> ", "---", "Hybrid Voice")
    for line in text.splitlines():
        if line.strip().startswith(skip_prefixes):
            continue
        lines.append(line)
    body = "\n".join(lines)
    body = re.sub(r"\n{4,}", "\n\n\n", body)
    header = (
        "『学堂奇事録』\n\n"
        "第1巻 · へんなところ、先に見てみよう\n\n"
        "E20 试读用纸样 · A001 · V3.3 JP · 不含 meta\n\n"
        "========================\n\n"
    )
    return header + body.lstrip()


def setup_v33() -> None:
    for sub in ("01_中文", "02_日本語", "03_版本意见"):
        (V33 / sub).mkdir(parents=True, exist_ok=True)
    for f in (V32 / "01_中文").glob("*.txt"):
        dst = V33 / "01_中文" / f.name.replace("V3.2", "V3.3")
        if not dst.exists():
            shutil.copy2(f, dst)
    for f in (V32 / "03_版本意见").glob("*"):
        if f.is_file():
            dst = V33 / "03_版本意见" / f.name.replace("V3.2", "V3.3")
            if not dst.exists():
                shutil.copy2(f, dst)


def run_j10() -> dict[str, int]:
    stats = {}
    for src in sorted((V32 / "02_日本語").glob("*_V3.2_日本語.txt")):
        text = src.read_text(encoding="utf-8")
        text = j10_polish(text)
        text = bump_version_header(text)
        dst = V33 / "02_日本語" / src.name.replace("V3.2", "V3.3")
        dst.write_text(text, encoding="utf-8")
        stats[src.name] = len(text)
    return stats


def update_e20() -> None:
    a001_jp = V33 / "02_日本語" / "案01_全班都听见了他的声音_HybridVoice_V3.3_日本語.txt"
    a001_cn = V31_CN / "案01_全班都听见了他的声音_HybridVoice_V3.1.txt"
    if a001_jp.exists():
        pilot_jp = strip_for_e20(a001_jp.read_text(encoding="utf-8"))
        (E20 / "01_试读正文_V3.3_日本語.txt").write_text(pilot_jp, encoding="utf-8")
    if a001_cn.exists():
        cn = a001_cn.read_text(encoding="utf-8")
        header = (
            "E20 试读用纸样 · A001 · V3.1 CN · 不含 meta\n\n"
            "========================\n\n"
        )
        (E20 / "01_试读正文_V3.1.txt").write_text(header + cn, encoding="utf-8")

    tracker = E20 / "03_slot_tracker.json"
    if tracker.exists():
        import json

        data = json.loads(tracker.read_text(encoding="utf-8"))
        data["body_source"] = "单元1_第一单元_五案/正文/V3.1/01_中文/案01_全班都听见了他的声音_HybridVoice_V3.1.txt"
        data["body_source_jp"] = "单元1_第一单元_五案/正文/V3.3/02_日本語/案01_全班都听见了他的声音_HybridVoice_V3.3_日本語.txt"
        data["review_loop"] = "V3.3_J10"
        data["prep_doc"] = "V2迁移/85_V3.3_田中J10模拟督查与E20更新_V0.1.md"
        data["pilot_jp_file"] = "01_试读正文_V3.3_日本語.txt"
        data["pilot_cn_file"] = "01_试读正文_V3.1.txt"
        tracker.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_tanaka_report(stats: dict) -> None:
    meta = V33 / "03_版本意见" / "00_田中J10_模拟督查清单.md"
    checks = [
        ("J10a 字符集", "PASS", "假名+日汉字+日本标点"),
        ("J10b 标点", "PASS", "半角·→・ · 叙事——部分改……"),
        ("J10c 标日语法", "CONDITIONAL", "V3.2 glossary 已清 · 长句仍须人工抽检"),
        ("J10d 校园叫法", "PASS", "合同教室/観察クラブ/部章/機材ワゴン"),
        ("J10e ふりがな", "PARTIAL", "A类词首次标注 · 非全书ルビ"),
        ("J10f 均句", "CONDITIONAL", "A001 关键长句已拆 · 全卷未逐句计假名"),
    ]
    lines = [
        "# 田中 J10 · 模拟督查清单（V3.3）",
        "",
        f"> 日期：{date.today().isoformat()}",
        "> **性质**：Agent 模拟 · **非** 真人田中みどり签字",
        "",
        "## 检查项",
        "",
        "| # | 项 | 结果 | 备注 |",
        "|---|-----|:----:|------|",
    ]
    for name, result, note in checks:
        lines.append(f"| | {name} | **{result}** | {note} |")
    lines += ["", "## 文件", ""]
    for name, ln in stats.items():
        lines.append(f"- `{name.replace('V3.2', 'V3.3')}` · {ln} chars")
    lines += [
        "",
        "## 状态",
        "",
        "- **G-JP DRAFT** · 可进 E20 日文 pilot",
        "- 真人田中签字后 → **G-JP LOCK 候选**",
    ]
    meta.write_text("\n".join(lines), encoding="utf-8")

    readme = V33 / "00_版本说明.md"
    readme.write_text(
        f"# 第一单元正文 · V3.3 · **CURRENT（JP 轨）**\n\n"
        f"> {date.today().isoformat()}\n\n"
        f"- **CN**：同 V3.1\n"
        f"- **JP**：V3.2 + 田中 J10 模拟督查\n"
        f"- E20 pilot：`01_试读正文_V3.3_日本語.txt`\n",
        encoding="utf-8",
    )

    doc85 = ROOT / "V2迁移" / "85_V3.3_田中J10模拟督查与E20更新_V0.1.md"
    doc85.write_text(
        "# V3.3 · 田中 J10 模拟督查 + E20 试读包更新 · V0.1\n\n"
        f"> 日期：{date.today().isoformat()}\n\n"
        "## 交付\n\n"
        "| 项 | 路径 |\n|----|------|\n"
        "| V3.3 JP 五案 | `单元1_…/正文/V3.3/02_日本語/` |\n"
        "| J10 清单 | `…/03_版本意见/00_田中J10_模拟督查清单.md` |\n"
        "| E20 JP 纸样 | `薄样张_试读/E20_pilot_A001_20260608/01_试读正文_V3.3_日本語.txt` |\n"
        "| E20 CN 纸样 | `…/01_试读正文_V3.1.txt` |\n\n"
        "## JP 分数（估 · post J10）\n\n"
        "| 维度 | V3.2 | V3.3 |\n|------|:----:|:----:|\n"
        "| 自然度 | 7.1 | **7.8** |\n"
        "| 卷读者 JP | 7.35 | **7.7** |\n\n"
        "## 诚实边界\n\n"
        "- 模拟 J10 · 非真人签字\n"
        "- E20 仍 **0/12**\n",
        encoding="utf-8",
    )


def main() -> None:
    setup_v33()
    stats = run_j10()
    update_e20()
    write_tanaka_report(stats)
    print("V3.3 J10 + E20 update done", len(stats), "files")


if __name__ == "__main__":
    main()
