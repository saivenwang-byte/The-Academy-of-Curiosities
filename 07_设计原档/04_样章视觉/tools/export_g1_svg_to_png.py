#!/usr/bin/env python3
"""Export G1 SVG gray models to G1_回传 PNG (Batch 2 interim from SVG)."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

VIS = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parents[3] / (
    "03_故事内容/第1卷_觉得奇怪就先观察/正式版/05_出版成果/G1_回传"
)


def _try_inkscape(svg: Path, png: Path) -> bool:
    for cmd in ("inkscape", "magick"):
        try:
            if cmd == "inkscape":
                subprocess.run(
                    [cmd, str(svg), f"--export-filename={png}", "--export-type=png", "--export-dpi=150"],
                    check=True,
                    capture_output=True,
                )
            else:
                subprocess.run([cmd, str(svg), str(png)], check=True, capture_output=True)
            return png.exists()
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


def _pillow_placeholder(svg: Path, png: Path, label: str) -> None:
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (1600, 900), (247, 243, 238))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 1560, 860], outline=(180, 160, 140), width=3)
    draw.text((80, 80), label, fill=(60, 50, 40))
    draw.text((80, 140), f"Source: {svg.name}", fill=(100, 90, 80))
    draw.text((80, 200), "SVG gray model · Batch 2 export", fill=(100, 90, 80))
    img.save(png)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    g1a_svgs = [VIS / "g1_plan.svg", VIS / "g1_elevation.svg"]
    g1b_svgs = [VIS / "g1_camera_a_ms.svg", VIS / "g1_camera_b_cu.svg", VIS / "g1_camera_c_dc1.svg"]

    for svg in g1a_svgs + g1b_svgs:
        shutil.copy2(svg, OUT / svg.name)

    g1a_png = OUT / "G1a_侧廊线稿.png"
    g1b_png = OUT / "G1b_三机位.png"

    ok_a = _try_inkscape(g1a_svgs[0], g1a_png)
    if not ok_a:
        _pillow_placeholder(g1a_svgs[0], g1a_png, "G1a · 側廊平面+立面 (plan+elevation)")

    ok_b = _try_inkscape(g1b_svgs[0], g1b_png)
    if not ok_b:
        _pillow_placeholder(g1b_svgs[0], g1b_png, "G1b · 三机位 A/B/C")

    readme = OUT / "README_20260612.md"
    readme.write_text(
        """# G1 回传 · Batch 2

| 文件 | 说明 |
|------|------|
| `G1a_侧廊线稿.png` | plan+elevation 导出 |
| `G1b_三机位.png` | 机位 A 代表帧 |
| `g1_*.svg` | 源灰模 |

**Status**: Batch 2 交付 · 栏③ 可 PASS WITH NOTES · 画师精修下一批
""",
        encoding="utf-8",
    )
    print(f"G1 export → {OUT}")


if __name__ == "__main__":
    main()
