#!/usr/bin/env python3
"""Generate Vol1 V-S02–V-S05 series illustrations (programmatic v0.9)."""

from __future__ import annotations

import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]  # 02_插画/
ASSETS = ROOT / "assets"
SAMPLE_ILLUST = ROOT.parents[1] / "样章包" / "插图"

W, H = 1536, 1024
PAPER = (247, 242, 233)
PENCIL = (72, 68, 64)
LIGHT = (180, 170, 155)
ACCENT = (196, 164, 116)
BLUE = (120, 150, 180)

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
]


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for p in FONT_CANDIDATES:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except OSError:
                continue
    return ImageFont.load_default()


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (W, H), PAPER)
    return im, ImageDraw.Draw(im)


def ruled_lines(d: ImageDraw.ImageDraw, top: int, bottom: int, gap: int = 36) -> None:
    y = top
    while y < bottom:
        d.line([(80, y), (W - 80, y)], fill=LIGHT, width=1)
        y += gap


def save(im: Image.Image, name: str) -> Path:
    ASSETS.mkdir(parents=True, exist_ok=True)
    out = ASSETS / name
    im.save(out, "PNG", optimize=True)
    SAMPLE_ILLUST.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out, SAMPLE_ILLUST / name)
    return out


def v_s02_diary() -> Path:
    im, d = new_canvas()
    f28, f22, f18 = font(28), font(22), font(18)
    d.rounded_rectangle([60, 40, W - 60, H - 40], radius=12, outline=PENCIL, width=2)
    ruled_lines(d, 100, H - 80)
    d.text((90, 55), "陸瑆（ひかる）のノート · 4月", fill=PENCIL, font=f22)
    lines = [
        "兄が言った。ポスターの端が、場所を変えてめくれる。",
        "お化けじゃない。風だ。",
        "",
        "（絵：簡単なポスター · 上から矢印 · 左の角がめくれる）",
    ]
    y = 120
    for line in lines:
        d.text((90, y), line, fill=PENCIL, font=f18)
        y += 38
    # sketch poster
    px, py = 900, 200
    d.rectangle([px, py, px + 280, py + 200], outline=PENCIL, width=3)
    d.line([(px + 220, py), (px + 280, py + 40)], fill=ACCENT, width=4)
    for i in range(3):
        d.ellipse([px + 40 + i * 50, py + 30, px + 70 + i * 50, py + 60], outline=PENCIL, width=2)
    for arr_y in range(py + 80, py + 180, 25):
        d.line([(px + 140, arr_y), (px + 140, arr_y + 18)], fill=BLUE, width=2)
        d.polygon([(px + 130, arr_y + 12), (px + 150, arr_y + 12), (px + 140, arr_y + 22)], fill=BLUE)
    d.text((90, H - 120), "毎日、違う辺でめくれるなら、あいさつしてる？", fill=ACCENT, font=f22)
    d.text((90, H - 75), "—— 瑆", fill=PENCIL, font=f28)
    return save(im, "V-S02_陸瑆日记页.png")


def v_s02_tail() -> Path:
    im, d = new_canvas()
    f20, f16 = font(20), font(16)
    d.text((80, 40), "壁報下書き · 第4欄 · 無署名の投稿", fill=PENCIL, font=f20)
    # clipboard board
    d.rounded_rectangle([100, 100, W - 100, H - 120], radius=8, outline=PENCIL, width=3, fill=(255, 253, 248))
    col_w = (W - 240) // 4
    for i in range(5):
        x = 120 + i * col_w
        d.line([(x, 120), (x, H - 140)], fill=LIGHT, width=2)
    headers = ["①めくれた", "②泥のあと", "③空欄", "④？"]
    for i, h in enumerate(headers):
        d.text((130 + i * col_w, 130), h, fill=PENCIL, font=f16)
    # empty 4th column + slip
    x4 = 120 + 3 * col_w
    d.rectangle([x4 + 15, 280, x4 + col_w - 25, 520], outline=LIGHT, width=2)
    d.rectangle([x4 + 30, 320, x4 + col_w - 40, 480], outline=ACCENT, width=2, fill=(255, 252, 240))
    d.text((x4 + 40, 350), "下駄箱三列目", fill=PENCIL, font=f16)
    d.text((x4 + 40, 390), "足跡がおかしい。", fill=PENCIL, font=f16)
    d.text((x4 + 40, 450), "（署名なし）", fill=LIGHT, font=f16)
    d.text((80, H - 70), "V-S02-TAIL · 投稿が空欄に入った", fill=ACCENT, font=f20)
    return save(im, "V-S02-TAIL_无署名窄条.png")


def v_s03_tail() -> Path:
    im, d = new_canvas()
    f20, f16 = font(20), font(16)
    d.text((80, 40), "投稿の裏 · 消し跡のルート", fill=PENCIL, font=f20)
    # paper back
    d.rounded_rectangle([140, 100, W - 140, H - 100], radius=6, outline=PENCIL, width=2, fill=(255, 254, 250))
    d.text((180, 130), "表：下駄箱三列目……（確認済）", fill=LIGHT, font=f16)
    # erased route
    pts = [(200, 700), (420, 620), (680, 580), (920, 420), (1100, 280)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(200, 195, 185), width=8)
        d.line([pts[i], pts[i + 1]], fill=PENCIL, width=3)
    d.text((200, 740), "側廊", fill=PENCIL, font=f16)
    d.text((1020, 240), "旧校舎方面", fill=ACCENT, font=f20)
    d.text((80, H - 60), "空欄は言葉を待つ · 裏は道を待つ", fill=ACCENT, font=f20)
    return save(im, "V-S03-TAIL_投稿背面路线.png")


def v_s04_chalk() -> Path:
    im, d = new_canvas()
    f20, f16 = font(20), font(16)
    d.text((80, 30), "5年2組 · 教壇 · チョーク粉の輪", fill=PENCIL, font=f20)
    # podium
    d.rectangle([200, 500, W - 200, H - 80], fill=(220, 210, 195), outline=PENCIL, width=2)
    d.rectangle([280, 420, W - 280, 500], fill=(200, 190, 175), outline=PENCIL, width=2)
    # chalk tray
    d.rectangle([320, 400, 520, 430], fill=(100, 100, 100), outline=PENCIL)
    # dust ring
    d.ellipse([300, 350, 540, 410], outline=ACCENT, width=3)
    random.seed(44)
    for _ in range(35):
        cx = 320 + random.randint(0, 200)
        cy = 360 + random.randint(0, 40)
        d.ellipse([cx, cy, cx + 4, cy + 4], fill=(200, 200, 195))
    # balloon demo inset
    d.ellipse([950, 200, 1100, 350], outline=BLUE, width=3, fill=(230, 240, 250))
    d.line([(1025, 350), (1025, 450)], fill=PENCIL, width=2)
    random.seed(45)
    for _ in range(12):
        sx = 970 + random.randint(0, 100)
        sy = 220 + random.randint(0, 100)
        d.line([(sx, sy), (980 + random.randint(0, 80), 240 + random.randint(0, 80))], fill=PENCIL, width=1)
    d.text((900, 470), "風船＋粉 · 静電気対照", fill=PENCIL, font=f16)
    d.text((80, H - 50), "掃除の順番＋風＋乾燥 · お化けじゃない", fill=ACCENT, font=f20)
    return save(im, "V-S04_讲台粉笔灰圈.png")


def v_s04_tail() -> Path:
    im, d = new_canvas()
    f20, f16 = font(20), font(16)
    # corridor perspective
    d.polygon([(0, H), (0, 300), (W, 200), (W, H)], fill=(235, 228, 218))
    d.line([(0, 300), (W, 200)], fill=LIGHT, width=2)
    d.text((80, 40), "側廊 · 遠景", fill=PENCIL, font=f20)
    # distant senpai
    d.ellipse([980, 320, 1040, 380], fill=(80, 70, 65))
    d.rectangle([990, 380, 1030, 520], fill=(100, 120, 150), outline=PENCIL)
    d.ellipse([1060, 480, 1120, 540], fill=ACCENT, outline=PENCIL, width=2)
    d.text((820, 560), "6年1組 · 中谷 · 半句だけ", fill=PENCIL, font=f16)
    d.text((700, 600), "「あの道、放課後は間違えない方がいい。」", fill=ACCENT, font=f20)
    return save(im, "V-S04-TAIL_中谷远景.png")


def v_s05_crumbs() -> Path:
    im, d = new_canvas()
    f20, f16 = font(20), font(16)
    d.text((80, 40), "美術準備室 · 戸口の内側", fill=PENCIL, font=f20)
    # door frame
    d.rectangle([400, 120, 1100, H - 80], outline=PENCIL, width=4, fill=(250, 247, 240))
    d.rectangle([400, 120, 450, H - 80], fill=(180, 160, 130))
    d.text((720, 160), "美術 準備室", fill=LIGHT, font=f20)
    # threshold crumbs pointing inward
    random.seed(7)
    for i in range(25):
        x = 520 + i * 18 + random.randint(-3, 3)
        y = H - 200 + random.randint(-8, 8)
        d.line([(x, y), (x + 8, y - 5)], fill=PENCIL, width=2)
    d.polygon([(500, H - 180), (700, H - 220), (680, H - 160)], fill=ACCENT)
    d.text((500, H - 120), "← カスの向き · 戸の内側", fill=ACCENT, font=f20)
    d.text((80, H - 50), "摩擦の跡 · 盗みではない", fill=PENCIL, font=f16)
    return save(im, "V-S05_橡皮屑方向.png")


def v_s05_tail() -> Path:
    im, d = new_canvas()
    f22, f18 = font(22), font(18)
    d.rounded_rectangle([60, 40, W - 60, H - 40], radius=12, outline=PENCIL, width=2)
    ruled_lines(d, 100, H - 80)
    d.text((90, 55), "瑆 · 巻末 · 誤描", fill=PENCIL, font=f22)
    # bookshelf sketch
    d.rectangle([120, 200, 500, 520], outline=PENCIL, width=3)
    for sy in range(240, 500, 50):
        d.line([(120, sy), (500, sy)], fill=LIGHT, width=1)
    d.line([(480, 260), (520, 240)], fill=ACCENT, width=4)  # crooked corner
    # hand without face - only arm + ponytail hint
    d.line([(540, 280), (580, 260)], fill=PENCIL, width=5)
    d.line([(560, 250), (600, 320)], fill=PENCIL, width=4)
    d.arc([590, 200, 660, 300], 200, 340, fill=PENCIL, width=3)
    d.text((120, 560), "本の角を直した手 · 顔は描かない", fill=ACCENT, font=f18)
    d.text((120, H - 100), "兄：「どうしてわかった？」 瑆：「おかしいは場所を変えるでしょ。」", fill=PENCIL, font=f18)
    return save(im, "V-S05-TAIL_瑆日记扶正书.png")


def v_s03_wind() -> Path:
    im, d = new_canvas()
    f20 = font(20)
    d.text((80, 40), "補助 · 風の側（事件①復習）", fill=PENCIL, font=f20)
    d.rectangle([300, 200, 700, 500], outline=PENCIL, width=3)
    d.line([(300, 250), (700, 250)], fill=ACCENT, width=4)
    for arr_y in range(280, 480, 40):
        d.line([(500, arr_y), (500, arr_y + 25)], fill=BLUE, width=3)
        d.polygon([(490, arr_y + 18), (510, arr_y + 18), (500, arr_y + 30)], fill=BLUE)
    d.text((320, 520), "エアコン吹き出し", fill=PENCIL, font=f20)
    d.text((720, 350), "めくれる側＝風の側", fill=ACCENT, font=f20)
    return save(im, "V-S03_风侧示意图.png")


def main() -> None:
    makers = [
        v_s02_diary,
        v_s02_tail,
        v_s03_tail,
        v_s03_wind,
        v_s04_chalk,
        v_s04_tail,
        v_s05_crumbs,
        v_s05_tail,
    ]
    for fn in makers:
        path = fn()
        print(f"Wrote {path.name} ({path.stat().st_size // 1024} KB)")
    print(f"Synced to {SAMPLE_ILLUST}")


if __name__ == "__main__":
    main()
