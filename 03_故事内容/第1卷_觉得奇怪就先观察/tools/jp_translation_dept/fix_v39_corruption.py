#!/usr/bin/env python3
"""One-shot + idempotent fix for V3.9 JP corruption (C1/C2).

Applies R1/R2 from human editor patch doc, syncs 正文/V3.9 ↔ A00X/01_正文.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNIT = ROOT / "单元1_第一单元_五案"
CANON = "公開日と学習発表会"

# C1: any corruption variant → canonical event name
EVENT_CORRUPT_RE = re.compile(
    r"(?:学校)+(?:学校)?公開日と(?:学習発表会と)+学習発表会"
    r"|学校公開日と(?:学習発表会と)+学習発表会"
)

# C2: collapse duplicate furigana on 合同教室
GOUDOU_FURIGANA_RE = re.compile(
    r"合同教室(?:（[ぁ-んァ-ヶー]+）)+"
)

# R1 の polish (idempotent — skips if の/に already present)
PARTICLE_FIXES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"公開日と学習発表会リハーサル"), "公開日と学習発表会のリハーサル"),
    (re.compile(r"公開日と学習発表会不参加"), "公開日と学習発表会に不参加"),
    (re.compile(r"公開日と学習発表会展示前"), "公開日と学習発表会の展示前"),
    (re.compile(r"公開日と学習発表会展示"), "公開日と学習発表会の展示"),
    (re.compile(r"公開日と学習発表会前に"), "公開日と学習発表会の前に"),
    (re.compile(r"公開日と学習発表会クラス"), "公開日と学習発表会のクラス"),
    (re.compile(r"公開日と学習発表会案内板"), "公開日と学習発表会の案内板"),
    (re.compile(r"公開日と学習発表会バッジ"), "公開日と学習発表会のバッジ"),
    (re.compile(r"公開日と学習発表会カウントダウン"), "公開日と学習発表会のカウントダウン"),
    (re.compile(r"公開日と学習発表会破壊"), "公開日と学習発表会の破壊"),
    (re.compile(r"公開日と学習発表会プレビュー"), "公開日と学習発表会のプレビュー"),
]


def fix_text(text: str) -> tuple[str, int]:
    n = 0

    def sub_event(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return CANON

    text, c = EVENT_CORRUPT_RE.subn(sub_event, text)
    n += c

    def sub_goudou(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return "合同教室（ごうどうきょうしつ）"

    text, c = GOUDOU_FURIGANA_RE.subn(sub_goudou, text)
    n += c

    for pat, repl in PARTICLE_FIXES:
        text, c = pat.subn(repl, text)
        n += c

    return text, n


def collect_files() -> list[Path]:
    paths: list[Path] = []
    for sub in (
        UNIT / "正文" / "V3.9" / "02_日本語",
        UNIT / "A001" / "01_正文",
        UNIT / "A002" / "01_正文",
        UNIT / "A003" / "01_正文",
        UNIT / "A004" / "01_正文",
        UNIT / "A005" / "01_正文",
    ):
        if sub.exists():
            paths.extend(sorted(sub.glob("*_V3.9_日本語.txt")))
    seen: set[Path] = set()
    out: list[Path] = []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(p)
    return out


def sync_v39_to_cases() -> None:
    src_dir = UNIT / "正文" / "V3.9" / "02_日本語"
    if not src_dir.exists():
        return
    for src in sorted(src_dir.glob("*_V3.9_日本語.txt")):
        case_num = src.name[2]  # 案01 → 1
        case = f"A00{case_num}"
        dst = UNIT / case / "01_正文" / src.name
        if dst.resolve() != src.resolve():
            shutil.copy2(src, dst)


def main() -> None:
    files = collect_files()
    total = 0
    for fp in files:
        raw = fp.read_text(encoding="utf-8")
        fixed, n = fix_text(raw)
        if n:
            fp.write_text(fixed, encoding="utf-8")
            print(f"  {fp.relative_to(ROOT)}: {n} fix(es)")
            total += n
        else:
            print(f"  {fp.relative_to(ROOT)}: ok")
    sync_v39_to_cases()
    print(f"Done: {len(files)} files, {total} replacements; synced V3.9 → A00X")


if __name__ == "__main__":
    main()
