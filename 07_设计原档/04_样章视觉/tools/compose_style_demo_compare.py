"""Side-by-side: Style B LOCK (left) vs DEMO output (right) for IP sign-off."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "CHAR_lineup_L0_StyleB_马克笔_V0.2.png"


def _font(size: int):
    for p in (
        "C:/Windows/Fonts/meiryo.ttc",
        "C:/Windows/Fonts/msyh.ttc",
    ):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def compose(demo: Path, out: Path, label_demo: str = "DEMO") -> Path:
    lock = Image.open(LOCK).convert("RGBA")
    demo_img = Image.open(demo).convert("RGBA")

    target_h = 900
    lock_sc = target_h / lock.height
    demo_sc = target_h / demo_img.height
    lock_r = lock.resize((int(lock.width * lock_sc), target_h), Image.Resampling.LANCZOS)
    demo_r = demo_img.resize((int(demo_img.width * demo_sc), target_h), Image.Resampling.LANCZOS)

    gap = 24
    header = 56
    w = lock_r.width + gap + demo_r.width
    h = header + target_h + 16
    canvas = Image.new("RGB", (w, h), (250, 247, 242))
    draw = ImageDraw.Draw(canvas)
    title_f = _font(22)
    draw.text((w // 2, 28), "Style B 画风对照 · IP 签字用", fill=(42, 24, 16), font=title_f, anchor="mm")

    canvas.paste(lock_r, (0, header), lock_r if lock_r.mode == "RGBA" else None)
    canvas.paste(demo_r, (lock_r.width + gap, header), demo_r if demo_r.mode == "RGBA" else None)

    cap = _font(16)
    draw.text((lock_r.width // 2, header + target_h + 8), "← LOCK（唯一垫图）", fill=(80, 60, 40), font=cap, anchor="mm")
    draw.text(
        (lock_r.width + gap + demo_r.width // 2, header + target_h + 8),
        f"→ {label_demo}",
        fill=(80, 60, 40),
        font=cap,
        anchor="mm",
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=92)
    return out


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: compose_style_demo_compare.py <demo.png> <out.png>")
        return 2
    demo = Path(sys.argv[1])
    out = Path(sys.argv[2])
    compose(demo, out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
