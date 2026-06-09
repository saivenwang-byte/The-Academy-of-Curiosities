#!/usr/bin/env python3
"""M0 batch fix for V3.8 JP trial body — template corruption, CN residue, internal codes."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"

# Canonical + per-case copies
GLOBS = [
    UNIT / "正文" / "V3.8" / "02_日本語" / "案*_HybridVoice_V3.8_日本語.txt",
    UNIT / "A001" / "01_正文" / "案01_*_日本語.txt",
    UNIT / "A002" / "01_正文" / "案02_*_日本語.txt",
    UNIT / "A003" / "01_正文" / "案03_*_日本語.txt",
    UNIT / "A004" / "01_正文" / "案04_*_日本語.txt",
    UNIT / "A005" / "01_正文" / "案05_*_日本語.txt",
]

CORRUPT = "学校学校学校学校公開日と学習発表会と学習発表会と学習発表会と学習発表会"
CORRUPT_RE = re.compile(
    r"学校学校(?:学校学校)*(?:公開日と学習発表会(?:と学習発表会)*)+"
)

REPLACEMENTS: list[tuple[str, str]] = [
    (CORRUPT, "公開日と学習発表会"),
    ("三周前", "三週間前"),
    ("椅背", "背もたれ"),
    ("瑆笔记", "ひかるのノート"),
    ("瑆笔", "ひかるのノート"),
    ("午後可能有小雨", "午後は小雨かもしれない"),
    ("十几本", "十数本"),
    ("詞を忘れる", "セリフを忘れる"),
    ("那天", "あの日"),
    ("画面灰字", "画面の灰色の文字"),
    ("提醒みたいに", "知らせるみたいに"),
    ("（がっどうきょうしつ）", "（ごうどうきょうしつ）"),
    # 骂 (CN) → けなし系
    ("骂り方", "言い方"),
    ("骂った", "けなした"),
    ("骂ってる", "けなしてる"),
    ("骂れない", "言い返せない"),
    ("骂る声", "言い返す声"),
    ("骂らない", "けならない"),
    ("「骂」", "「けなす」"),
    ("笔画", "筆画"),
]

END_CASE = {
    "……第一案完……": "……1話め、おしまい。……",
    "……第二案完……": "……2話め、おしまい。……",
    "……第三案完……": "……3話め、おしまい。……",
    "……第四案完……": "……4話め、おしまい。……",
    "……第五案完……": "……5話め、おしまい。……",
    "……第一単元完……": "……この単元、おしまい。……",
}

# Whole-line removals (internal link codes)
REMOVE_LINE_PATTERNS = [
    re.compile(r"^（案[①②③④⑤].*収束.*）\s*$"),
]


def collect_files() -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    dirs = [
        UNIT / "正文" / "V3.8" / "02_日本語",
        UNIT / "正文" / "V3.9" / "02_日本語",
        UNIT / "A001" / "01_正文",
        UNIT / "A002" / "01_正文",
        UNIT / "A003" / "01_正文",
        UNIT / "A004" / "01_正文",
        UNIT / "A005" / "01_正文",
    ]
    for d in dirs:
        if not d.exists():
            continue
        for p in sorted(d.glob("*_V3.8_日本語.txt")) + sorted(d.glob("*_V3.9_日本語.txt")):
            rp = p.resolve()
            if rp not in seen:
                seen.add(rp)
                out.append(p)
    return out


def fix_text(text: str) -> tuple[str, int]:
    n = 0
    new_text, c = CORRUPT_RE.subn("公開日と学習発表会", text)
    if c:
        text = new_text
        n += c
    for old, new in REPLACEMENTS:
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    for old, new in END_CASE.items():
        c = text.count(old)
        if c:
            text = text.replace(old, new)
            n += c
    lines = text.splitlines()
    new_lines: list[str] = []
    for line in lines:
        drop = any(p.match(line.strip()) for p in REMOVE_LINE_PATTERNS)
        if drop:
            n += 1
            continue
        new_lines.append(line)
    return "\n".join(new_lines), n


def main() -> None:
    files = collect_files()
    total = 0
    for fp in files:
        raw = fp.read_text(encoding="utf-8")
        fixed, n = fix_text(raw)
        if n:
            fp.write_text(fixed, encoding="utf-8")
            print(f"  {fp.name}: {n} fixes")
            total += n
        else:
            print(f"  {fp.name}: ok")
    print(f"Done: {len(files)} files, {total} replacements")


if __name__ == "__main__":
    main()
