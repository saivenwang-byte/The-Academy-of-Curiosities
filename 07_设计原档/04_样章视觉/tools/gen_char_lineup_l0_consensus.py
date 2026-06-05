"""Generate L0 character lineup layout board for illustrators (expert consensus)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent.parent
OUT = OUT_DIR / "CHAR_lineup_L0_专家共识_画师参照.png"
W, H = 3840, 2160

SLOTS = [
    ("陆瑆", 132, (255, 200, 190), "4年2組·记录者", "日记 彩铅", "りく ひかる"),
    ("陆珣", 142, (80, 130, 200), "5年2組·主角", "路线本 指南针", "りく しゅん"),
    ("松本志郎", 145, (200, 80, 70), "5年3組·验证", "查证卡", "まつもと しろう"),
    ("伊藤光", 146, (255, 140, 50), "5年2組·行动", "橙围巾 哨子", "いとう ひかる"),
    ("山本理纱", 147, (70, 80, 120), "5年4組·秩序", "速写本", "やまもと りさ"),
    ("中谷琦", 152, (100, 120, 80), "6年1組·前辈", "相机", "なかたに き"),
    ("加藤慧美", 155, (240, 210, 80), "5年1組·采访", "采访本 银框镜", "かとう けいみ"),
    ("葛西泉藏", 158, (120, 100, 70), "社区长辈", "旧地图", "かさい せんzō"),
    ("陆美咲", 163, (220, 180, 160), "母亲·主厨", "便当", "りく みさき"),
    ("陆直人", 175, (60, 100, 160), "父亲·设计师", "钢笔", "りく なおと"),
]

SLOT_MARKS = "①②③④⑤⑥⑦⑧⑨⑩"
BG = (252, 248, 242)
MARGIN_L = 120
TOP_BANNER = 160
FOOT_Y = H - 280
SCALE_X = W - 180


def load_fonts():
    cn_bold = "C:/Windows/Fonts/msyhbd.ttc"
    cn = "C:/Windows/Fonts/msyh.ttc"
    jp = "C:/Windows/Fonts/meiryo.ttc"
    try:
        return (
            ImageFont.truetype(cn_bold, 68),
            ImageFont.truetype(cn, 42),
            ImageFont.truetype(jp, 36),
            ImageFont.truetype(cn, 28),
        )
    except OSError:
        d = ImageFont.load_default()
        return d, d, d, d


def height_to_y(cm: int) -> int:
    top, bottom = TOP_BANNER + 60, FOOT_Y - 30
    ratio = (cm - 100) / 80
    return int(bottom - ratio * (bottom - top))


def draw_person(d: ImageDraw.ImageDraw, cx: int, cm: int, color: tuple, adult: bool = False):
    head_r = 34 if not adult else 44
    hy = height_to_y(cm + 8)
    by = height_to_y(cm)
    shoulder = 52 if adult else (44 if cm >= 145 else 38)
    if 158 <= cm < 163:
        shoulder = 48
    d.ellipse([cx - head_r, hy - head_r * 2, cx + head_r, hy], fill=color, outline=(60, 50, 40), width=3)
    d.rounded_rectangle(
        [cx - shoulder, hy, cx + shoulder, by],
        radius=12,
        fill=tuple(min(c + 20, 255) for c in color),
        outline=(60, 50, 40),
        width=3,
    )
    d.line([cx - 18, by, cx - 18, by + 28], fill=(60, 50, 40), width=4)
    d.line([cx + 18, by, cx + 18, by + 28], fill=(60, 50, 40), width=4)


def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    title_f, name_f, jp_f, small_f = load_fonts()

    d.rectangle([0, TOP_BANNER, W, H], fill=(255, 253, 250))
    for i in range(0, W, 120):
        d.line([i, TOP_BANNER, i, H], fill=(245, 240, 235), width=1)

    d.rounded_rectangle([W // 2 - 680, 36, W // 2 + 680, 140], fill=(139, 90, 43), radius=16)
    d.text((W // 2, 78), "学堂趣事录", fill=(255, 250, 240), font=title_f, anchor="mm")
    d.text((W // 2, 118), "觉得奇怪，就先观察 · 学校おもしろ観察クラブ · L0 · Nagoya · spring", fill=(255, 235, 210), font=small_f, anchor="mm")

    d.line([SCALE_X, TOP_BANNER + 30, SCALE_X, FOOT_Y + 40], fill=(40, 38, 36), width=4)
    for cm in range(100, 181, 10):
        y = height_to_y(cm)
        d.line([SCALE_X - 22, y, SCALE_X + 22, y], fill=(40, 38, 36), width=3)
        d.text((SCALE_X + 34, y), f"{cm}cm", fill=(40, 38, 36), font=small_f, anchor="lm")

    d.line([MARGIN_L, FOOT_Y + 40, SCALE_X - 40, FOOT_Y + 40], fill=(120, 100, 80), width=3)

    n = len(SLOTS)
    step = (SCALE_X - MARGIN_L - 80) // n
    for i, (name, cm, color, role, props, jp) in enumerate(SLOTS):
        cx = MARGIN_L + step * i + step // 2
        adult = cm >= 163
        draw_person(d, cx, cm, color, adult=adult)

        y_cm = height_to_y(cm)
        d.line([cx, y_cm, SCALE_X - 30, y_cm], fill=(210, 190, 170), width=2)
        d.ellipse([cx - 6, y_cm - 6, cx + 6, y_cm + 6], fill=(200, 60, 60))

        pw, ph = 260, 110
        px, py = cx - pw // 2, FOOT_Y + 56
        d.rounded_rectangle([px, py, px + pw, py + ph], fill=(40, 38, 36), radius=8)
        d.text((cx, py + 28), jp, fill=(240, 240, 240), font=jp_f, anchor="mm")
        d.text((cx, py + 64), name, fill=(255, 255, 255), font=name_f, anchor="mm")
        d.text((cx, py + 96), f"{cm}cm · {role}", fill=(200, 200, 200), font=small_f, anchor="mm")
        d.text((cx, height_to_y(cm + 8) - 56), props, fill=(90, 80, 70), font=small_f, anchor="mm")
        d.text((cx, TOP_BANNER + 12), SLOT_MARKS[i], fill=(160, 140, 120), font=title_f, anchor="mm")

    notes = (
        "专家共识 L0 布局锁定 · 画师精修为温暖水彩 · 禁探案笔记/侦探团 · 葛西泉藏 · 中谷精瘦6年 · 父母成人"
        " · 右侧100-180cm身高线必留 · 名古屋淡背景≤15% · 工作稿非印厂文件 · 详见同目录 brief.md"
    )
    d.text((W // 2, H - 42), notes, fill=(140, 130, 120), font=small_f, anchor="mm")
    return img


def main():
    img = render()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
