#!/usr/bin/env python3
"""Apply light JP MoA-lite fixes (child-friendly gloss, no LOCK)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BODY = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

FILES = {
    "A001": BODY / "案01_全班都听见了他的声音_HybridVoice_V2.0_日本語.txt",
    "A005": BODY / "案05_午休后消失的影子_HybridVoice_V2.0_日本語.txt",
}

SUBS = {
    "A001": [
        ("rehearsal_0328", "三週前のリハーサル録音"),
        ("rehearsal_0328.wav", "三週前のリハーサル録音"),
    ],
    "A005": [
        ("metadata", "撮影設定"),
        ("パノラマモード", "パノラマ撮影"),
    ],
}


def main() -> None:
    for cid, path in FILES.items():
        raw = path.read_text(encoding="utf-8")
        out = raw
        for old, new in SUBS.get(cid, []):
            out = out.replace(old, new)
        if out != raw:
            path.write_text(out, encoding="utf-8")
            print(f"JP MoA fix {cid}")
        else:
            print(f"No change {cid}")


if __name__ == "__main__":
    main()
