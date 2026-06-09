#!/usr/bin/env python3
"""Bootstrap raw JP V3.9 from CN V3.1 SSOT + V3.8 tone reference.

Agent/human fresh translation should replace this; bootstrap copies V3.8 body,
strips old headers, fixes internal codes, writes to 正文/V3.9/02_日本語/.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 第1卷_觉得奇怪就先观察
UNIT = ROOT / "单元1_第一单元_五案"
V39 = "V3.9"
CASES = ["A001", "A002", "A003", "A004", "A005"]

# Strip V3.x metadata headers until 序 or section
BODY_START = re.compile(r"^(序|一、|一\.|二、|三、|四、|五、)")


def discover(case: str) -> tuple[Path, Path]:
    n = int(case.replace("A", ""))
    cn_files = [
        f
        for f in (UNIT / case / "01_正文").glob(f"案0{n}_*.txt")
        if "_日本語" not in f.name
    ]
    cn_file = cn_files[0]
    prefix = cn_file.name.split("_HybridVoice")[0]
    jp_name = f"{prefix}_HybridVoice_{V39}_日本語.txt"
    v38 = UNIT / "正文" / "V3.8" / "02_日本語" / f"{prefix}_HybridVoice_V3.8_日本語.txt"
    v39 = UNIT / "正文" / V39 / "02_日本語" / jp_name
    return v38, v39


def strip_header(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if BODY_START.match(line.strip()):
            return "\n".join(lines[i:])
    return text


RAW_REPLACEMENTS: list[tuple[str, str]] = [
    ("前の案の画面", "前の一件の画面"),
    ("前の案", "前の一件"),
    ("案①", "前の放送"),
    ("案②", "黒板の一件"),
    ("案③", "ポスターの一件"),
    ("案④", "引き出しの一件"),
    ("案⑤", "影の一件"),
    ("（案① 收束 · L1 → 案② · shared_source）", ""),
    ("（案② 收束 · L2 → 案③ · mirror）", ""),
    ("（案③ 收束 · L3 → 案④ · puzzle_piece）", ""),
    ("（案④ 收束 · L4 → 案⑤ · 卷终）", ""),
    ("（案⑤ 收束 · 卷终 · 第一单元完）", ""),
    (
        "物語はもう組み上がっている：A001 放送で辱める・A002 志郎が字を書く・A003 慧美が原稿削除・A004 水野が盗む・A005 無影共謀……五つの本当、一つの偽物語。",
        "物語はもう組み上がっている：放送で辱める・黒板の字・原稿削除・盗み・無影共謀……五つの本当、一つの偽物語。",
    ),
    (
        "観察メモ：A001 旧録音誤放送＋発声禁止日・A002 膜現字・A003 実体なしポスター・A004 振動滑入・A005 パノラマで水野の影だけずれ",
        "観察メモ：旧録音誤放送＋発声禁止日・膜現字・実体なしポスター・振動滑入・パノラマで水野の影だけずれ",
    ),
    ("五案", "五つのへんなこと"),
    ("五案记录", "五件の記録"),
    ("五案机制", "五件の仕組み"),
    ("五案串成", "五件をつなげ"),
    ("把五案串成", "五件をつなげ"),
    ("五案的路", "五件の道"),
    ("五案的答案", "五件の答え"),
    ("五案记录夹", "五件の記録ファイル"),
    ("案①三周前", "三週間前"),
    ("申请表角压着案①", "申請書の角に三週間前"),
]


def clean_body(body: str) -> str:
    for old, new in RAW_REPLACEMENTS:
        body = body.replace(old, new)
    # Remove empty lines from deleted收束 markers (max 2 consecutive blanks kept)
    lines = body.splitlines()
    out: list[str] = []
    blank_run = 0
    for line in lines:
        if not line.strip():
            blank_run += 1
            if blank_run <= 2:
                out.append(line)
        else:
            blank_run = 0
            out.append(line)
    return "\n".join(out).strip() + "\n"


def main() -> None:
    for case in CASES:
        v38, v39 = discover(case)
        if not v38.exists():
            raise SystemExit(f"missing V3.8: {v38}")
        raw = v38.read_text(encoding="utf-8")
        body = strip_header(raw)
        body = clean_body(body)
        v39.parent.mkdir(parents=True, exist_ok=True)
        v39.write_text(body, encoding="utf-8")
        print(f"  {case} -> {v39.name} ({len(body)} chars)")


if __name__ == "__main__":
    main()
