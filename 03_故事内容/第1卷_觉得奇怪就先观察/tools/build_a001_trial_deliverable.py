#!/usr/bin/env python3
"""Build A001 trial reading deliverable: V3.9.1 JP PDF + 07_试读交付 folder."""

from __future__ import annotations

import io
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A001 = ROOT / "单元1_第一单元_五案" / "A001"
ILL = A001 / "03_插画"
JP_BODY = A001 / "01_正文" / "案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt"
CN_BODY = A001 / "01_正文" / "案01_全班都听见了他的声音_HybridVoice_V3.1.txt"
STORYBOARD = A001 / "02_分镜头"
OUT_ROOT = A001 / "07_试读交付_V1.0"
OUT_PDF_DIR = OUT_ROOT / "PDF"
OUT_TXT = OUT_ROOT / "01_正文"
OUT_SB = OUT_ROOT / "02_分镜"
OUT_ILL = OUT_ROOT / "03_插图_P0"

JP_FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
]
CN_FONT = Path(r"C:\Windows\Fonts\msyh.ttc")

P0_ORDER = ["DA1", "DA2", "DA3", "DA4", "DA5", "TAIL", "DB1"]

# JP anchor substring in body → insert illustration after matching paragraph
SHOT_ANCHORS: dict[str, str] = {
    "DA1": "合同教室",
    "DA2": "観察クラブは、へんなところを書く",
    "DA3": "再生・三週間前のリハーサル録音",
    "DA4": "波形が途中で切れている",
    "DA5": "でも、あなたの声だよ",
    "TAIL": "展示膜のテストが、まだ終わっていない",
    "DB1": "口の動きと、合わない",
}

TRIAL_ILL: dict[str, list[str]] = {
    "DA1": ["A001_DA1_V-S01-V2-A1_广播响起_PRODUCT_M0_StyleB_v1.0.png", "A001_DA1_V-S01-V2-A1_广播响起_PRODUCT_MVP_v1.0.png"],
    "DA2": ["A001_DA2_V-S01-V2-A2_观察社介入_PRODUCT_MVP_v1.1.png", "A001_DA2_V-S01-V2-A2_观察社介入_PRODUCT_M0_StyleB_v1.0.png"],
    "DA3": ["B4_CORRECT_试跑/A001_DA3_CORRECT_v1.1.png", "A001_DA3_V-S01-V2-A3_文件时间_PRODUCT_M0_StyleB_v1.0.png"],
    "DA4": ["B4_CORRECT_试跑/A001_DA4_CORRECT_v1.0.png", "A001_DA4_V-S01-V2-A4_波形硬切_PRODUCT_MVP_v1.0.png"],
    "DA5": ["A001_DA5_V-S01-V2-A5_误指峰值_PRODUCT_M0_StyleB_v1.0.png", "A001_DA5_V-S01-V2-A5_误指峰值_PRODUCT_MVP_v1.1.png"],
    "TAIL": ["B4_CORRECT_试跑/A001_TAIL_CORRECT_v1.0.png", "A001_TAIL_V-S01-V2-TAIL_修复与尾钩_PRODUCT_M0_StyleB_v1.1.png"],
    "DB1": ["B4_CORRECT_试跑/A001_DB1_CORRECT_v1.1.png", "A001_DB1_V-S01-V2-B1_广播机制SUM_PRODUCT_MVP_v1.0.png"],
}


def find_jp_font() -> Path:
    for p in JP_FONT_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("No Japanese font in C:/Windows/Fonts/")


def resolve_ill(shot: str) -> Path | None:
    for rel in TRIAL_ILL.get(shot, []):
        p = ILL / rel
        if p.is_file():
            return p
    cands = sorted(ILL.glob(f"A001_{shot}_*"), key=lambda x: ("M0_StyleB" not in x.name, x.name))
    return cands[0] if cands else None


def strip_jp_meta(raw: str) -> str:
    """Strip file header; supports V3.8 (==== gate) and V3.9 (---- only)."""
    lines = raw.splitlines()
    if re.search(r"^={8,}\s*$", raw, re.M):
        out: list[str] = []
        past_gate = False
        for line in lines:
            s = line.strip()
            if not past_gate:
                if s.startswith(">") and "Hybrid Voice" in s:
                    continue
                if re.match(r"^=+$", s):
                    past_gate = True
                    continue
                if s.startswith("『学堂") or s.startswith("第1巻") or s.startswith("単元"):
                    continue
                if not past_gate:
                    continue
            if s.startswith(">") and "Hybrid Voice" in s:
                continue
            out.append(line)
        body = "\n".join(out).strip()
    else:
        # V3.9+: drop title block through first long rule line after 序
        start = 0
        for i, line in enumerate(lines):
            if re.match(r"^-{10,}$", line.strip()):
                start = i + 1
                break
        if start == 0:
            for i, line in enumerate(lines):
                if line.strip().startswith("全校放送"):
                    start = i
                    break
        body = "\n".join(lines[start:]).strip()
    while body.startswith("\n"):
        body = body.lstrip("\n")
    return body


def split_paragraphs(text: str) -> list[str]:
    paras: list[str] = []
    buf: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            if buf:
                paras.append("\n".join(buf))
                buf = []
            continue
        if re.match(r"^-{3,}$", s):
            if buf:
                paras.append("\n".join(buf))
                buf = []
            continue
        if re.match(r"^[序一二三四五六七八九十]、", s) or s.startswith("序"):
            if buf:
                paras.append("\n".join(buf))
                buf = []
            paras.append(s)
            continue
        buf.append(s)
    if buf:
        paras.append("\n".join(buf))
    return [p for p in paras if p.strip()]


def compress_image(src: Path, max_width: int = 900) -> Path:
    from PIL import Image

    im = Image.open(src)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    w, h = im.size
    if w > max_width:
        h = int(h * max_width / w)
        w = max_width
        im = im.resize((w, h), Image.Resampling.LANCZOS)
    tmp = Path(tempfile.gettempdir()) / f"a001_trial_{src.stem}.jpg"
    im.save(tmp, format="JPEG", quality=85, optimize=True)
    return tmp


def build_pdf(pdf_path: Path, ill_map: dict[str, Path], body_text: str) -> None:
    from fpdf import FPDF

    jp_font = find_jp_font()
    paras = split_paragraphs(body_text)
    inserted: set[str] = set()

    pdf = FPDF(format="A5", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(14, 14, 14)
    pdf.add_font("JP", "", str(jp_font))
    if CN_FONT.is_file():
        pdf.add_font("CN", "", str(CN_FONT))

    def write_line(text: str, size: float = 10.5, font: str = "JP") -> None:
        if not text.strip():
            return
        pdf.set_font(font, size=size)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, size * 0.52, text.strip())

    def insert_shot(shot: str) -> None:
        if shot in inserted:
            return
        img_path = ill_map.get(shot)
        if not img_path or not img_path.is_file():
            return
        compressed = compress_image(img_path)
        pdf.ln(2)
        pdf.set_x(pdf.l_margin)
        pdf.image(str(compressed), w=min(pdf.epw * 0.95, 118))
        pdf.ln(1)
        write_line(f"［挿画 · {shot}］", size=7)
        pdf.ln(2)
        inserted.add(shot)

    # Cover — JP only (no missing glyphs)
    pdf.add_page()
    write_line("学園キコロキ", size=16)
    write_line("Vol.1 · 事件01 · 試読版", size=11)
    pdf.ln(4)
    write_line("クラス全員が、彼の声を聞いた", size=13)
    pdf.ln(6)
    write_line("A001 · 日本語 V3.9.1", size=9)
    write_line("非売品 · 試読専用 · M0-B 通読済", size=8)

    pdf.add_page()
    write_line("事件01", size=9)
    write_line("クラス全員が、彼の声を聞いた", size=13)
    pdf.ln(2)

    for para in paras:
        if re.match(r"^[序一二三四五六七八九十]、", para) or para.startswith("序"):
            write_line(para, size=11)
            pdf.ln(2)
        else:
            write_line(para, size=10.5)
            pdf.ln(1.2)

        for shot in P0_ORDER:
            anchor = SHOT_ANCHORS.get(shot, "")
            if anchor and anchor in para and shot not in inserted:
                insert_shot(shot)

    for shot in P0_ORDER:
        if shot not in inserted:
            insert_shot(shot)

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(pdf_path))


def write_readme(ill_map: dict[str, Path], pdf_path: Path) -> None:
    ill_lines = "\n".join(f"| {s} | `{p.name}` |" for s, p in ill_map.items())
    readme = f"""# A001 · 试读交付包 · V1.0

> **案01**：全班都听见了他的声音 / クラス全員が、彼の声を聞いた  
> **生成**：{date.today().isoformat()} · `build_a001_trial_deliverable.py`

## 从这里开始

1. **试读 PDF** → [`PDF/{pdf_path.name}`](./PDF/{pdf_path.name})
2. **试读正文（纯文本）** → [`01_正文/01_试读正文_V3.9.1_日本語.txt`](./01_正文/01_试读正文_V3.9.1_日本語.txt)
3. 分镜 → [`02_分镜/`](./02_分镜/)
4. P0 插图 → [`03_插图_P0/`](./03_插图_P0/)

## P0 插图

| Shot | 文件 |
|------|------|
{ill_lines}

## 重建

```bash
python "03_故事内容/第1卷_觉得奇怪就先观察/tools/build_a001_trial_deliverable.py"
```
"""
    (OUT_ROOT / "00_打开从这里看.md").write_text(readme, encoding="utf-8")


def main() -> int:
    if not JP_BODY.is_file():
        print(f"FAIL: missing {JP_BODY}", file=sys.stderr)
        return 1

    raw = JP_BODY.read_text(encoding="utf-8")
    body = strip_jp_meta(raw)
    if len(body) < 500:
        print(f"FAIL: body too short after strip ({len(body)} chars)", file=sys.stderr)
        return 1

    ill_map: dict[str, Path] = {}
    for shot in P0_ORDER:
        p = resolve_ill(shot)
        if p:
            ill_map[shot] = p
        else:
            print(f"WARN: no image for {shot}", file=sys.stderr)

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    OUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TXT.mkdir(parents=True, exist_ok=True)
    OUT_SB.mkdir(parents=True, exist_ok=True)
    OUT_ILL.mkdir(parents=True, exist_ok=True)

    trial_txt = OUT_TXT / "01_试读正文_V3.9.1_日本語.txt"
    trial_txt.write_text(body, encoding="utf-8")
    shutil.copy2(JP_BODY, OUT_TXT / JP_BODY.name)
    if CN_BODY.is_file():
        shutil.copy2(CN_BODY, OUT_TXT / CN_BODY.name)

    for name in ("00_插画师分镜文字稿_V1.0.md", "03_分镜头_插页地图_V3.6_JP.md"):
        src = STORYBOARD / name
        if src.is_file():
            shutil.copy2(src, OUT_SB / name)

    for shot, src in ill_map.items():
        shutil.copy2(src, OUT_ILL / f"A001_{shot}_{src.name}")

    pdf_name = f"A001_试读_V3.9.1_日本語_{date.today().strftime('%Y%m%d')}.pdf"
    pdf_path = OUT_PDF_DIR / pdf_name
    build_pdf(pdf_path, ill_map, body)
    write_readme(ill_map, pdf_path)

    kb = pdf_path.stat().st_size // 1024
    paras = len(split_paragraphs(body))
    print(f"DELIVERABLE: {OUT_ROOT}")
    print(f"PDF: {pdf_path} ({kb} KB)")
    print(f"Body: {len(body)} chars · {paras} paragraphs")
    print(f"Illustrations: {len(ill_map)}/{len(P0_ORDER)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
