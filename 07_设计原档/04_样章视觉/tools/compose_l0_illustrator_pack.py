"""Compose illustrator-ready L0 lineup from spring art + expert consensus overlay."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "CHAR_lineup_L1_spring.png"
OUT = ROOT / "CHAR_lineup_L0_专家共识_画师发包.png"
OUT_HD = ROOT / "CHAR_lineup_L0_专家共识_画师发包_3840.png"

W, H = 1536, 1024
HD_W, HD_H = 3840, 2160

# x centers for 1536px (from lineup_text_canon XS_L0)
XS = [82, 214, 346, 478, 610, 742, 874, 1006, 1138, 1270]

SLOTS = [
    ("りく ひかる", "陆瑆", "132cm", "4年2組·记录者"),
    ("りく しゅん", "陆珣", "142cm", "5年2組·主角"),
    ("まつもと しろう", "松本志郎", "145cm", "5年3組·验证"),
    ("いとう ひかる", "伊藤光", "146cm", "5年2組·行动"),
    ("やまもと りさ", "山本理纱", "147cm", "5年4組·秩序"),
    ("なかたに き", "中谷琦", "152cm", "6年1組·前辈"),
    ("かとう けいみ", "加藤慧美", "155cm", "5年1組·采访"),
    ("かさい せんzō", "葛西泉藏", "158cm", "社区长辈"),
    ("りく みさき", "陆美咲", "163cm", "母亲·主厨"),
    ("りく なおと", "陆直人", "175cm", "父亲·设计师"),
]

SIGN_Y = 322
FOOTER_WIPE_Y = 780
FOOTER_Y = 868


def fonts(scale: float = 1.0):
    cn_b = "C:/Windows/Fonts/msyhbd.ttc"
    cn = "C:/Windows/Fonts/msyh.ttc"
    jp = "C:/Windows/Fonts/meiryo.ttc"
    s = scale
    try:
        return (
            ImageFont.truetype(cn_b, int(36 * s)),
            ImageFont.truetype(cn, int(22 * s)),
            ImageFont.truetype(jp, int(18 * s)),
            ImageFont.truetype(cn, int(14 * s)),
        )
    except OSError:
        d = ImageFont.load_default()
        return d, d, d, d


def height_y(cm: int, top: int, foot: int) -> int:
    ratio = (cm - 100) / 80
    return int(foot - ratio * (foot - top))


def compose(base: Image.Image, scale: float = 1.0) -> Image.Image:
    img = base.convert("RGBA")
    w, h = img.size
    sx = w / W
    sy = h / H
    d = ImageDraw.Draw(img)
    title_f, name_f, jp_f, small_f = fonts(scale * sx)

    # cover magnifying glass / 探案笔记 (top-right)
    d.rectangle([int(w * 0.78), 0, w, int(h * 0.22)], fill=(255, 252, 248, 255))
    d.rounded_rectangle(
        [int(w * 0.80), int(h * 0.02), w - int(16 * sx), int(h * 0.18)],
        radius=int(8 * sx),
        fill=(139, 90, 43, 255),
    )
    d.text(
        (int(w * 0.89), int(h * 0.07)),
        "観察クラブ",
        fill=(255, 250, 240),
        font=title_f,
        anchor="mm",
    )
    d.text(
        (int(w * 0.89), int(h * 0.13)),
        "L0 · spring",
        fill=(255, 235, 210),
        font=small_f,
        anchor="mm",
    )

    # title strip top center
    d.rounded_rectangle(
        [int(w * 0.22), int(h * 0.01), int(w * 0.72), int(h * 0.09)],
        radius=int(10 * sx),
        fill=(139, 90, 43, 230),
    )
    d.text(
        (w // 2, int(h * 0.035)),
        "学堂趣事录",
        fill=(255, 250, 240),
        font=title_f,
        anchor="mm",
    )
    d.text(
        (w // 2, int(h * 0.065)),
        "觉得奇怪，就先观察",
        fill=(255, 235, 210),
        font=small_f,
        anchor="mm",
    )

    # wipe old footers + signs area refresh
    d.rectangle([0, int(FOOTER_WIPE_Y * sy), w, h], fill=(255, 255, 255, 255))

    top_band = int(h * 0.12)
    foot_band = int(FOOTER_WIPE_Y * sy) - int(20 * sy)

    # height scale right edge
    scale_x = w - int(28 * sx)
    d.line([scale_x, top_band, scale_x, foot_band], fill=(40, 38, 36), width=max(2, int(2 * sx)))
    for cm in range(100, 181, 10):
        y = height_y(cm, top_band, foot_band)
        d.line([scale_x - int(10 * sx), y, scale_x + int(10 * sx), y], fill=(40, 38, 36), width=2)
        d.text((scale_x + int(14 * sx), y), f"{cm}", fill=(60, 55, 50), font=small_f, anchor="lm")

    ground = int(FOOTER_WIPE_Y * sy) - int(8 * sy)
    d.line([int(20 * sx), ground, scale_x - int(20 * sx), ground], fill=(180, 170, 160), width=2)

    for i, (xs, slot) in enumerate(zip(XS, SLOTS)):
        cx = int(xs * sx)
        jp, cn, cm, role = slot
        y_cm = height_y(int(cm.replace("cm", "")), top_band, foot_band)
        d.line([cx, y_cm, scale_x - int(16 * sx), y_cm], fill=(220, 210, 200), width=1)
        d.ellipse(
            [cx - 4, y_cm - 4, cx + 4, y_cm + 4],
            fill=(200, 60, 60),
        )

        sw, sh = int(118 * sx), int(52 * sy)
        sy_sign = int(SIGN_Y * sy)
        # wipe old chest signs from base art
        d.rectangle(
            [cx - sw // 2 - int(8 * sx), sy_sign - int(12 * sy), cx + sw // 2 + int(8 * sx), sy_sign + sh + int(8 * sy)],
            fill=(255, 255, 255, 255),
        )

        # name sign (hand)
        d.rounded_rectangle(
            [cx - sw // 2, sy_sign, cx + sw // 2, sy_sign + sh],
            radius=6,
            fill=(30, 28, 26, 255),
        )
        d.text((cx, sy_sign + int(14 * sy)), jp, fill=(240, 240, 240), font=jp_f, anchor="mm")
        d.text((cx, sy_sign + int(32 * sy)), cn, fill=(255, 255, 255), font=name_f, anchor="mm")

        # footer plate
        fw, fh = int(130 * sx), int(48 * sy)
        fy = int(FOOTER_Y * sy)
        d.rounded_rectangle(
            [cx - fw // 2, fy, cx + fw // 2, fy + fh],
            fill=(245, 243, 240, 255),
            outline=(200, 195, 190),
            width=1,
        )
        d.text((cx, fy + int(14 * sy)), f"{cm} · {role}", fill=(80, 70, 60), font=small_f, anchor="mm")
        slot_num = "①②③④⑤⑥⑦⑧⑨⑩"[i]
        d.text((cx, fy + int(32 * sy)), slot_num, fill=(160, 140, 120), font=small_f, anchor="mm")

    note = "专家共识发包 · 温暖水彩精修定稿向 · 禁探案笔记 · 葛西泉藏 · 详 brief.md"
    d.text((w // 2, h - int(12 * sy)), note, fill=(140, 130, 120), font=small_f, anchor="mm")

    return img.convert("RGB")


def main():
    if not SRC.exists():
        raise SystemExit(f"missing source: {SRC}")
    base = Image.open(SRC)
    pack = compose(base, scale=1.0)
    pack.save(OUT, "PNG", optimize=True)

    hd = pack.resize((HD_W, HD_H), Image.Resampling.LANCZOS)
    hd.save(OUT_HD, "PNG", optimize=True)
    print(f"saved {OUT} ({OUT.stat().st_size} bytes)")
    print(f"saved {OUT_HD} ({OUT_HD.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
