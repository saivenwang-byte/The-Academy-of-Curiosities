#!/usr/bin/env python3
"""Unit1 V3.6 trial reading PDF — JP text + PRODUCT illustrations (A001–A005)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
BODY_JP = UNIT / "正文" / "V3.8" / "02_日本語"
BODY_JP_FALLBACK = UNIT / "正文" / "V3.6" / "02_日本語"
ILL_V36 = UNIT / "插图" / "绑定正文_V3.6"
ILL_COMPRESSED = UNIT / "插图" / "绑定正文_V3.6_试读压缩"
OUT_DIR = ROOT / "薄样张_试读" / "Unit1_V3.6_五案试读" / "PDF"
OUT_PDF = OUT_DIR / "学堂奇事録_Vol1_单元1_试读_V3.6_日本語.pdf"
OUT_PDF_LITE = OUT_DIR / "学堂奇事録_Vol1_单元1_试读_V3.6_日本語_軽量版.pdf"

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
]

CASES = [
    ("A001", "01", "クラス全員が、彼の声を聞いた", "案01_全班都听见了他的声音_HybridVoice_V3.6_日本語.txt"),
    ("A002", "02", "誰も書いていない「ごめんなさい」", "案02_没有人写过的道歉_HybridVoice_V3.6_日本語.txt"),
    ("A003", "03", "みんなが覚えているポスター", "案03_每个人都记得的海报_HybridVoice_V3.6_日本語.txt"),
    ("A004", "04", "彼女の引き出しにだけあった失物", "案04_只出现在她抽屉里的失物_HybridVoice_V3.6_日本語.txt"),
    ("A005", "05", "昼休みのあと、消えた影", "案05_午休后消失的影子_HybridVoice_V3.6_日本語.txt"),
]

# P0 shot order per case -> image prefix in bound folder
P0_ORDER = {
    # A001 MVP: 6 depth anchors + DB1 SUM + VS02 diary (8); P1 augments omitted from trial PDF
    "A001": ["DA1", "DA2", "DA3", "DA4", "DA5", "TAIL", "DB1", "VS02"],
    "A002": ["DA1", "DA2", "DA3", "DA4", "DA5", "TAIL", "DB1"],
    "A003": ["DA1", "DA2", "DA4", "DA5", "TAIL"],
    "A004": ["DA1", "DA3", "DA4", "DA5", "TAIL"],
    "A005": ["DA1", "DA3", "DA6", "TAIL"],
}


def resolve_jp_path(fname: str, case_id: str | None = None) -> Path:
    """Pick latest JP body: A00X/01_正文 first, then shim V3.8/V3.6."""
    if case_id:
        case_body = UNIT / case_id / "01_正文"
        if case_body.is_dir():
            n = fname.split("_")[0]
            cands = sorted(case_body.glob(f"{n}_*_日本語.txt"), reverse=True)
            if cands:
                return cands[0]
    for root in (BODY_JP, BODY_JP_FALLBACK):
        direct = root / fname
        if direct.exists():
            return direct
        # same stem, any HybridVoice_*_日本語.txt for this case
        n = fname.split("_")[0]  # 案01
        cands = sorted(root.glob(f"{n}_*_日本語.txt"), reverse=True)
        if cands:
            return cands[0]
    return BODY_JP / fname


def find_font() -> Path:
    for p in FONT_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("No Japanese font found in C:/Windows/Fonts/")


def strip_jp_meta(raw: str) -> str:
    """Remove lines before body: meta, ====, Hybrid Voice header, book title block."""
    lines = raw.splitlines()
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
    # drop leading empty / duplicate title lines until 序 or numbered section
    while out and not out[0].strip():
        out.pop(0)
    return "\n".join(out).strip()


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
        if re.match(r"^[序一二三四五六七八九十]、", s) or s.startswith("序·") or s.startswith("序 ·"):
            if buf:
                paras.append("\n".join(buf))
                buf = []
            paras.append(s)
            continue
        buf.append(s)
    if buf:
        paras.append("\n".join(buf))
    return paras


def find_illustration(case: str, shot: str) -> Path | None:
    """Prefer PRODUCT_v1.0 > V3.6.3 USERSTYLE > V3.6.2 > V3.6.1; never prefer PH placeholders."""
    for root in (ILL_COMPRESSED, ILL_V36):
        d = root / case
        if not d.exists():
            continue
        prefix = f"{case}_{shot}_"
        cands = [p for p in d.glob(f"{prefix}*") if "PH" not in p.name or "PRODUCT" in p.name]
        if not cands:
            continue
        cands.sort(key=lambda p: (
            "M0_StyleB" not in p.name,
            "PRODUCT_MVP_v1.1" not in p.name,
            "PRODUCT_MVP_v1.0" not in p.name,
            "PRODUCT_v1.2" not in p.name,
            "PRODUCT_v1.1" not in p.name,
            "PRODUCT_v1.0" not in p.name,
            "V3.6.3" not in p.name,
            "V3.6.2" not in p.name,
            "V3.6.1" not in p.name,
            "PH" in p.name,
            p.name,
        ))
        return cands[0]
    return None


def build_pdf(use_compressed: bool = True) -> Path:
    from fpdf import FPDF

    font_path = find_font()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_PDF_LITE if use_compressed and ILL_COMPRESSED.exists() else OUT_PDF

    pdf = FPDF(format="A5", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 16, 14)

    if font_path.suffix.lower() == ".ttc":
        pdf.add_font("JP", "", str(font_path))
    else:
        pdf.add_font("JP", "", str(font_path))

    def jp(text: str, size: float = 10.5, style: str = "") -> None:
        if not text or not text.strip():
            return
        pdf.set_font("JP", style=style, size=size)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, size * 0.52, text.strip())

    # Cover
    pdf.add_page()
    jp("学堂奇事録", size=18, style="")
    jp("Vol1 · 単元1 · 試読版 V3.6", size=12)
    pdf.ln(4)
    jp("へんなところ、先に見てみよう", size=11)
    pdf.ln(8)
    jp("五事件試読 · 日本語", size=10)
    jp("非売品 · 家庭／教室試読専用", size=9)
    pdf.ln(6)
    jp("A001–A005 · PRODUCT 挿画" + (" · 軽量" if out_path == OUT_PDF_LITE else ""), size=8)

    for case_id, num, title_jp, fname in CASES:
        jp_path = resolve_jp_path(fname, case_id)
        if not jp_path.exists():
            print(f"WARN missing text: {jp_path}", file=sys.stderr)
            continue

        raw = jp_path.read_text(encoding="utf-8")
        body = strip_jp_meta(raw)
        paras = split_paragraphs(body)

        # Case title page
        pdf.add_page()
        jp(f"事件{num}", size=9)
        jp(title_jp, size=14, style="")
        pdf.ln(2)
        jp(f"（{case_id} · V3.8）", size=8)

        ill_idx = 0
        shots = P0_ORDER.get(case_id, [])
        insert_every = max(len(paras) // (len(shots) + 1), 3) if shots else 999

        for i, para in enumerate(paras):
            if re.match(r"^[序一二三四五六七八九十]、", para) or para.startswith("序"):
                jp(para, size=11, style="")
                pdf.ln(2)
            else:
                jp(para, size=10.5)
                pdf.ln(1.5)

            if shots and ill_idx < len(shots) and (i + 1) % insert_every == 0:
                img_path = find_illustration(case_id, shots[ill_idx])
                if img_path and img_path.exists():
                    pdf.ln(2)
                    pdf.set_x(pdf.l_margin)
                    img_w = min(pdf.epw * 0.92, 110)
                    pdf.image(str(img_path), w=img_w)
                    pdf.ln(2)
                    jp(f"［挿画］", size=7)
                    pdf.ln(2)
                ill_idx += 1

        while ill_idx < len(shots):
            img_path = find_illustration(case_id, shots[ill_idx])
            if img_path and img_path.exists():
                pdf.add_page()
                pdf.set_x(pdf.l_margin)
                img_w = min(pdf.epw * 0.92, 110)
                pdf.image(str(img_path), w=img_w)
                pdf.ln(2)
                jp(f"［挿画］", size=7)
            ill_idx += 1

    pdf.output(str(out_path))
    return out_path


def main() -> int:
    try:
        out = build_pdf()
        size_kb = out.stat().st_size // 1024
        print(f"PDF: {out} ({size_kb} KB)")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
