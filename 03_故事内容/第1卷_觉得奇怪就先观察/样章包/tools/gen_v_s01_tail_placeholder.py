"""Generate V-S01-TAIL placeholder PNG for sample pack."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "插图" / "V-S01-TAIL_壁报草稿空栏.png"
W, H = 1200, 900

img = Image.new("RGB", (W, H), (245, 240, 230))
d = ImageDraw.Draw(img)

d.rectangle([80, 60, W - 80, H - 60], fill=(255, 252, 245), outline=(120, 100, 80), width=3)
d.rectangle([100, 80, W - 100, 160], fill=(230, 225, 215), outline=(150, 130, 110), width=2)

try:
    font_sm = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
    font_tiny = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 18)
except OSError:
    font_sm = ImageFont.load_default()
    font_tiny = font_sm

d.text((120, 95), "今週の校内おもしろ · 下書き", fill=(60, 50, 40), font=font_sm)
d.text((120, 130), "めくれたポスター", fill=(80, 70, 60), font=font_tiny)

cols = 4
x0, y0 = 120, 200
cw, ch = (W - 240) // cols - 10, 420
labels = [
    ["見出し", "めくれた", "ポスター"],
    ["確認", "フォルダ", "で風遮"],
    ["目撃", "陸珣5-2", "風の側"],
]
for i in range(cols):
    x = x0 + i * (cw + 10)
    d.rectangle([x, y0, x + cw, y0 + ch], outline=(100, 90, 70), width=2)
    if i < 3:
        d.rectangle([x + 4, y0 + 4, x + cw - 4, y0 + ch - 4], fill=(250, 248, 242))
        for j, line in enumerate(labels[i]):
            d.text((x + 12, y0 + 20 + j * 36), line, fill=(50, 45, 40), font=font_tiny)
    else:
        d.rectangle([x + 4, y0 + 4, x + cw - 4, y0 + ch - 4], fill=(255, 255, 250))
        d.text((x + cw - 36, y0 + ch - 40), "?", fill=(180, 60, 60), font=font_sm)

d.text((120, H - 100), "V-S01-TAIL · trial placeholder · SC-01-5", fill=(140, 130, 120), font=font_tiny)
d.text((120, H - 70), "col4 empty · club wall newspaper draft", fill=(140, 130, 120), font=font_tiny)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print(f"saved {OUT} ({OUT.stat().st_size} bytes)")
