#!/usr/bin/env python3
"""Calibrate SUM03 陸瑆笔记层 · date/grade/mechanism copy (v2 · wider patches)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ASSETS = Path(r"C:\Users\Lenovo\.cursor\projects\d-AI-Project-The-Academy-of-Curiosities\assets")
VOL1 = Path(r"d:\【AI Project】\【The Academy of Curiosities】\03_故事内容\第1卷_总是湿的椅子\插图")
# use original before v1 overlay if re-run needed; else start from current
SRC = ASSETS / "11_summary_hikaru_sketch.png"
BACKUP = ASSETS / "11_summary_hikaru_sketch_v1_raw.png"
KRAFT = (245, 237, 224)
INK = (55, 90, 130)
FONT = r"C:\Windows\Fonts\YuGothR.ttc"


def load_src() -> Image.Image:
    if not BACKUP.exists():
        raw = ASSETS / "11_summary_hikaru_sketch.png"
        # first run: keep pristine in assets folder name from batch
        alt = Path(__file__).resolve().parents[4] / "assets" / "11_summary_hikaru_sketch.png"
        for p in [ASSETS / "11_summary_hikaru_sketch_v0.png", alt]:
            if p.exists() and p != SRC:
                import shutil
                shutil.copy2(p, BACKUP)
                return Image.open(p).convert("RGB")
    if BACKUP.exists():
        return Image.open(BACKUP).convert("RGB")
    return Image.open(SRC).convert("RGB")


def draw_block(draw, box, lines, size, color=INK, fill=KRAFT):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=fill)
    font = ImageFont.truetype(FONT, size, index=0)
    ty = y0 + 6
    for line in lines:
        draw.text((x0 + 10, ty), line, fill=color, font=font)
        bbox = draw.textbbox((0, 0), line, font=font)
        ty += bbox[3] - bbox[1] + 5


def main() -> None:
    img = load_src()
    draw = ImageDraw.Draw(img)

    # header
    draw_block(draw, (35, 50, 430, 130), ["きょうの 観察メモ", "4月12日（金）　くもり"], 20)

    # replace old main paragraph + bubble
    draw_block(
        draw,
        (40, 140, 540, 400),
        [
            "きょうは、教室の窓枠のまわりが",
            "ひんやりしているのを 気づいた。",
            "",
            "お兄ちゃんの いすの背もたれが、",
            "窓枠に ぴったり くっついている。",
            "その ふれている ところだけ、",
            "手を あてると ヒヤ～っと した。",
        ],
        15,
    )

    # right label
    draw_block(draw, (660, 400, 990, 460), ["窓枠との すきま"], 16)

    # bottom thought — cover old「冷たい風」
    draw_block(
        draw,
        (35, 680, 500, 820),
        [
            "どうしてかな？",
            "「冷たい風」じゃなくて、",
            "窓枠そのものが ひんやり？",
        ],
        15,
    )

    # cover old bottom-right callout if conflicting
    draw_block(
        draw,
        (680, 720, 1020, 820),
        ["ふれている ところだけ", "ひんやりしていた！"],
        14,
    )

    for out in [ASSETS / "11_summary_hikaru_sketch.png", VOL1 / "11_summary_hikaru_sketch.png"]:
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, quality=95)
        print(f"Saved: {out}")


if __name__ == "__main__":
    main()
