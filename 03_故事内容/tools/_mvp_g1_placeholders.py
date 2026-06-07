#!/usr/bin/env python3
"""Generate labeled G1 placeholder PNGs for missing MVP keyframes."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPTH = (
    ROOT
    / "03_故事内容/第1卷_觉得奇怪就先观察/样章包/插图/depth_anchor"
)
MVP_ILL = (
    ROOT
    / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/05_出版成果/MVP_V2_20260608/03_插图"
)

# (filename, label line1, label line2, case folder)
PLACEHOLDERS = [
    ("V-S01-V2-A3_文件时间_G1draft_PH.png", "A001 DA3", "文件时间 · SC-05", "案01"),
    ("V-S01-V2-A4_波形硬切_G1draft_PH.png", "A001 DA4", "波形硬切 · SC-06", "案01"),
    ("V-S02-V2-A3_膜边反光_G1draft_PH.png", "A002 DA3", "膜边反光 · SC-05", "案02"),
    ("V-S02-V2-A4_对照实验_G1draft_PH.png", "A002 DA4", "对照实验 · SC-07", "案02"),
    ("V-S03-V2-A2_正式照无海报_G1draft_PH.png", "A003 DA2", "正式照无海报 · SC-03", "案03"),
    ("V-S03-V2-A4_远标题连线_G1draft_PH.png", "A003 DA4", "远标题连线 · SC-04", "案03"),
    ("V-S04-V2-A3_倾斜水泡_G1draft_PH.png", "A004 DA3", "倾斜水泡 · SC-05", "案04"),
    ("V-S04-V2-A4_振动复现_G1draft_PH.png", "A004 DA4", "振动复现 · SC-07", "案04"),
    ("V-S05-V2-A3_metadata三帧_G1draft_PH.png", "A005 DA3", "metadata三帧 · SC-05", "案05"),
    ("V-S05-V2-A6_重拍有影_G1draft_PH.png", "A005 DA6", "重拍有影 · SC-08", "案05"),
]

REAL_COPIES = [
    ("V-S01-V2-A1_广播响起_G1draft_c01.png", "案01"),
    ("V-S01-V2-DEMO_广播唇不同步.png", "案01"),
    ("V-S02-V2-DEMO_黑板对不起.png", "案02"),
    ("V-S03-V2-DEMO_空海报位.png", "案03"),
    ("V-S04-V2-DEMO_抽屉失物.png", "案04"),
    ("V-S05-V2-DEMO_仅水野无影.png", "案05"),
]


def _chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)


def make_placeholder_png(path: Path, line1: str, line2: str, w: int = 800, h: int = 450) -> None:
    """Minimal RGB PNG with flat fill — no PIL required."""
    bg = (0xF4, 0xEF, 0xE8)
    raw_rows = []
    for y in range(h):
        row = b"\x00"
        for x in range(w):
            # dashed border
            if x < 4 or y < 4 or x >= w - 4 or y >= h - 4:
                row += bytes((0xBB, 0xAA, 0x99))
            elif (x + y) // 12 % 2 == 0 and 40 < y < h - 40:
                row += bytes((0xE8, 0xE2, 0xDC))
            else:
                row += bytes(bg)
        raw_rows.append(row)
    compressed = zlib.compress(b"".join(raw_rows), 9)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", compressed)
    png += _chunk(b"IEND", b"")
    path.write_bytes(png)

    # Write sidecar label (PNG has no text layer without PIL)
    sidecar = path.with_suffix(".label.txt")
    sidecar.write_text(
        f"G1 PLACEHOLDER\n{line1}\n{line2}\nStatus: awaiting G1draft production\n",
        encoding="utf-8",
    )


def main() -> None:
    DEPTH.mkdir(parents=True, exist_ok=True)
    for fname, l1, l2, case in PLACEHOLDERS:
        out = DEPTH / fname
        if not out.exists():
            make_placeholder_png(out, l1, l2)
            print(f"placeholder {fname}")
        case_dir = MVP_ILL / case
        case_dir.mkdir(parents=True, exist_ok=True)
        import shutil

        shutil.copy2(out, case_dir / fname)
        if out.with_suffix(".label.txt").exists():
            shutil.copy2(out.with_suffix(".label.txt"), case_dir / out.with_suffix(".label.txt").name)

    import shutil

    for fname, case in REAL_COPIES:
        src = DEPTH / fname
        if src.exists():
            case_dir = MVP_ILL / case
            case_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, case_dir / fname)
            # flat copy for backward compat
            shutil.copy2(src, MVP_ILL / fname)
            print(f"copied {fname} -> {case}/")

    print(f"OK: {len(PLACEHOLDERS)} placeholders · {len(REAL_COPIES)} real copies")


if __name__ == "__main__":
    main()
