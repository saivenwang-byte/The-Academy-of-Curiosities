#!/usr/bin/env python3
"""Overlay LOCKED sign + footer text on CHAR_lineup L0–L4."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from lineup_text_canon import FOOTERS, LINEUP_VARIANTS, SIGNS

ROOT = Path(__file__).resolve().parents[1]
ASSETS = Path(r"C:\Users\Lenovo\.cursor\projects\d-AI-Project-The-Academy-of-Curiosities\assets")
FONT_JP = r"C:\Windows\Fonts\YuGothR.ttc"
FONT_CN = r"C:\Windows\Fonts\msyh.ttc"
KRAFT = (245, 237, 224)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size, index=0)


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_sign(draw: ImageDraw.ImageDraw, cx: int, cy: int, line1: str, line2: str) -> None:
    font_kana = load_font(FONT_JP, 10)
    font_han = load_font(FONT_CN, 12)
    w1, h1 = text_size(draw, line1, font_kana)
    w2, h2 = text_size(draw, line2, font_han)
    pad_x, pad_y = 7, 4
    box_w = max(w1, w2) + pad_x * 2
    box_h = h1 + h2 + pad_y * 3
    x0, y0 = cx - box_w // 2, cy - box_h // 2
    draw.rectangle([x0 - 4, y0 - 18, x0 + box_w + 4, y0 + box_h + 4], fill=(255, 255, 255))
    draw.rectangle([x0, y0, x0 + box_w, y0 + box_h], fill=(18, 18, 18))
    draw.text((cx - w1 // 2, y0 + pad_y), line1, fill=(255, 255, 255), font=font_kana)
    draw.text((cx - w2 // 2, y0 + pad_y + h1 + 2), line2, fill=(255, 255, 255), font=font_han)


def draw_footer_column(
    draw: ImageDraw.ImageDraw, cx: int, y0: int, line1: str, line2: str, col_half: int = 66
) -> None:
    font = load_font(FONT_JP, 8)
    w1, h1 = text_size(draw, line1, font)
    w2, h2 = text_size(draw, line2, font)
    draw.rectangle([cx - col_half, y0 - 2, cx + col_half, y0 + h1 + h2 + 8], fill=(255, 255, 255))
    draw.text((cx - w1 // 2, y0), line1, fill=(35, 35, 35), font=font)
    draw.text((cx - w2 // 2, y0 + h1 + 2), line2, fill=(35, 35, 35), font=font)


def overlay_variant(key: str) -> Path:
    cfg = LINEUP_VARIANTS[key]
    src = ASSETS / cfg["src"]
    if not src.exists():
        src = ROOT / cfg["src"]
    img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, cfg["footer_wipe_y"], 1420, 1024], fill=(255, 255, 255))
    for i, cx in enumerate(cfg["xs"]):
        draw_sign(draw, cx, cfg["sign_y"], SIGNS[i][0], SIGNS[i][1])
        half = 72 if i in (4, 5, 8, 9) else 66
        draw_footer_column(draw, cx, cfg["footer_y"], FOOTERS[i][0], FOOTERS[i][1], col_half=half)
    out = ROOT / cfg["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=95)
    img.save(ASSETS / cfg["out"], quality=95)
    print(f"Saved: {out}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "variants",
        nargs="*",
        default=["L0"],
        choices=list(LINEUP_VARIANTS.keys()) + ["ALL"],
    )
    args = parser.parse_args()
    keys = list(LINEUP_VARIANTS.keys()) if "ALL" in args.variants else args.variants
    for key in keys:
        overlay_variant(key)


if __name__ == "__main__":
    main()
