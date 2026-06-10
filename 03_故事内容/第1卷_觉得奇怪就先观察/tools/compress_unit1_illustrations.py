#!/usr/bin/env python3
"""Compress 绑定正文_V3.6 PNGs for trial PDF (max width, JPEG quality)."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
SRC = UNIT / "插图" / "绑定正文_V3.6"
DST = UNIT / "插图" / "绑定正文_V3.6_试读压缩"


def compress_one(src: Path, dst: Path, max_w: int, quality: int) -> tuple[int, int]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    w, h = im.size
    if w > max_w:
        nh = int(h * max_w / w)
        im = im.resize((max_w, nh), Image.Resampling.LANCZOS)
    im.save(dst, "JPEG", quality=quality, optimize=True)
    return src.stat().st_size, dst.stat().st_size


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-width", type=int, default=1200)
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    if not SRC.exists():
        raise SystemExit(f"Missing: {SRC}")

    total_in = total_out = 0
    n = 0
    for png in sorted(SRC.rglob("*.png")):
        rel = png.relative_to(SRC)
        out = DST / rel.with_suffix(".jpg")
        si, so = compress_one(png, out, args.max_width, args.quality)
        total_in += si
        total_out += so
        n += 1
        print(f"  {rel}: {si//1024}KB -> {so//1024}KB")

    manifest = DST / "00_压缩清单.md"
    manifest.write_text(
        f"# 绑定正文 V3.6 试读压缩\n\n"
        f"- 源：`绑定正文_V3.6/`\n"
        f"- 输出：`绑定正文_V3.6_试读压缩/`（JPEG max_w={args.max_width} q={args.quality}）\n"
        f"- 文件数：{n}\n"
        f"- 体积：{total_in//1024//1024}MB → {total_out//1024//1024}MB\n",
        encoding="utf-8",
    )
    print(f"Done: {n} files, {total_in//1024//1024}MB -> {total_out//1024//1024}MB")


if __name__ == "__main__":
    main()
