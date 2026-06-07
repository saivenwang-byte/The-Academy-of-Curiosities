#!/usr/bin/env python3
"""Generate 3 cover exploration mockups (internal · not final art)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1]
W, H = 1200, 1800
BG = (247, 243, 238)
ACCENT = (230, 120, 60)
BLUE = (70, 130, 180)


def _font(size: int):
    for name in ("arial.ttf", "YuGothM.ttc", "msgothic.ttc"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_cover(path: Path, title: str, hook: str, badge: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([60, 60, W - 60, H - 60], outline=ACCENT, width=4)
    d.polygon([(W // 2 - 80, 420), (W // 2 + 80, 420), (W // 2, 320)], fill=ACCENT)
    d.line([(W // 2 - 120, 500), (W // 2 + 40, 500)], fill=BLUE, width=8)
    d.ellipse([W - 220, 100, W - 100, 220], outline=ACCENT, width=3)
    f1, f2, f3 = _font(52), _font(36), _font(28)
    d.text((100, 120), title, fill=(40, 40, 40), font=f1)
    d.text((100, 620), hook, fill=(80, 80, 80), font=f2)
    d.text((100, H - 200), badge, fill=ACCENT, font=f3)
    d.text((100, 200), "学校おもしろ観察クラブ", fill=BLUE, font=f3)
    img.save(path)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    variants = [
        ("COVER_A_翘边海报钩子.png", "めくれたポスター", "翘边海报 · 侧廊 MS", "A · 观察クラブ徽章"),
        ("COVER_B_风侧图形钩子.png", "風の向き", "风侧箭头 · 窗缝 CU", "D · 风侧事件图形"),
        ("COVER_C_双锚组合推荐.png", "観察、はじめ。", "徽章 + 翘边 + 四人侧影", "A+D · IP 推荐"),
    ]
    for fname, t, h, b in variants:
        draw_cover(OUT / fname, t, h, b)
    print("Wrote 3 covers to", OUT)


if __name__ == "__main__":
    main()
