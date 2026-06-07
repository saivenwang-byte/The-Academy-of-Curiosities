#!/usr/bin/env python3
"""Assemble full G-JP A002-A005 from per-case modules into 正式版/01_正文."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
BODY = TOOLS.parents[1] / "第1卷_觉得奇怪就先观察/正式版/01_正文"

HEADER_TMPL = """『学堂奇事録』

第1巻 · へんなところ、先に見てみよう

========================

【G-JP MVP · Hybrid Voice · V2.0 · {case_id}】

  · 状態：MVP-JP FULL 2026-06-08 · **非 G-JP LOCK**
  · 品質：CN R3 構造対応 · MoA-lite 未 · 田中 J10 未
  · 参照：CN_BODY R3 · academy-jp-voice-editor

========================

"""

FOOTER_TMPL = """
---

【G-JP · EDITOR · 2026-06-08】
· 状態：G-JP MVP FULL {case_id} · **非 G-JP LOCK**
· G-BODY 後：MoA-lite 四視角 + J10 標日字符検
"""

CASES = [
    ("A002", "案02_没有人写过的道歉_HybridVoice_V2.0_日本語.txt", "a002_body"),
    ("A003", "案03_每个人都记得的海报_HybridVoice_V2.0_日本語.txt", "a003_body"),
    ("A004", "案04_只出现在她抽屉里的失物_HybridVoice_V2.0_日本語.txt", "a004_body"),
    ("A005", "案05_午休后消失的影子_HybridVoice_V2.0_日本語.txt", "a005_body"),
]


def load_body(module_name: str) -> str:
    path = TOOLS / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod.BODY


def main() -> None:
    for case_id, filename, mod in CASES:
        body = load_body(mod)
        content = HEADER_TMPL.format(case_id=case_id) + body.strip() + FOOTER_TMPL.format(case_id=case_id)
        out = BODY / filename
        out.write_text(content.strip() + "\n", encoding="utf-8")
        kana = sum(1 for c in content if "\u3040" <= c <= "\u30ff" or "\u4e00" <= c <= "\u9fff")
        print(f"Wrote {out.name}: {len(content)} chars, kana/cjk={kana}")


if __name__ == "__main__":
    main()
