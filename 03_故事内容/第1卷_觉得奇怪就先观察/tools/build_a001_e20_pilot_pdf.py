#!/usr/bin/env python3
"""A001-only E20 pilot PDF — V3.8 JP text + V3.6.3 USERSTYLE illustrations."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
PILOT = ROOT / "薄样张_试读" / "E20_pilot_A001_V3.8_20260609"
BODY_JP = PILOT / "01_试读正文_V3.8_日本語.txt"
BODY_JP_FALLBACK = UNIT / "正文" / "V3.8" / "02_日本語" / "案01_全班都听见了他的声音_HybridVoice_V3.8_日本語.txt"
ILL_V36 = UNIT / "插图" / "绑定正文_V3.6" / "A001"
ILL_COMPRESSED = UNIT / "插图" / "绑定正文_V3.6_试读压缩" / "A001"
OUT_DIR = PILOT / "PDF"
OUT_PDF = OUT_DIR / "A001_E20_试读_V3.8_日本語.pdf"

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
]

P0_ORDER = ["DA1", "DA2", "DA3", "DA4", "DA5", "TAIL", "DB1"]


def resolve_jp_path() -> Path:
    if BODY_JP.exists():
        return BODY_JP
    if BODY_JP_FALLBACK.exists():
        return BODY_JP_FALLBACK
    raise FileNotFoundError(f"Missing JP body: {BODY_JP}")


def find_font() -> Path:
    for p in FONT_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("No Japanese font found in C:/Windows/Fonts/")


def strip_jp_meta(raw: str) -> str:
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


def find_illustration(shot: str) -> Path | None:
    """Prefer V3.6.3 USERSTYLE > V3.6.2 > V3.6.1, compressed JPEG then PNG."""
    for root in (ILL_COMPRESSED, ILL_V36):
        if not root.exists():
            continue
        prefix = f"A001_{shot}_"
        cands = list(root.glob(f"{prefix}*"))
        if not cands:
            continue
        cands.sort(key=lambda p: (
            "M0_StyleB" not in p.name,
            "V3.6.3" not in p.name,
            "V3.6.2" not in p.name,
            "V3.6.1" not in p.name,
            "PH" not in p.name,
            p.suffix != ".jpg",
            p.name,
        ))
        return cands[0]
    return None


def build_pdf() -> Path:
    from fpdf import FPDF

    jp_path = resolve_jp_path()
    font_path = find_font()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pdf = FPDF(format="A5", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(14, 16, 14)
    pdf.add_font("JP", "", str(font_path))

    def jp(text: str, size: float = 10.5, style: str = "") -> None:
        if not text or not text.strip():
            return
        pdf.set_font("JP", style=style, size=size)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(pdf.epw, size * 0.52, text.strip())

    pdf.add_page()
    jp("学堂奇事録", size=18)
    jp("Vol1 · 事件01 · 試読版 V3.8", size=12)
    pdf.ln(4)
    jp("クラス全員が、彼の声を聞いた", size=11)
    pdf.ln(6)
    jp("A001 · E20 Pilot · 日本語", size=10)
    jp("非売品 · 内部試読 · G1DRAFT 挿画", size=9)
    jp("非 G-JP LOCK · 田中校阅前", size=8)

    raw = jp_path.read_text(encoding="utf-8")
    body = strip_jp_meta(raw)
    paras = split_paragraphs(body)

    pdf.add_page()
    jp("事件01", size=9)
    jp("クラス全員が、彼の声を聞いた", size=14)
    jp("（A001 · V3.8 · E20 Pilot）", size=8)
    pdf.ln(2)

    ill_idx = 0
    insert_every = max(len(paras) // (len(P0_ORDER) + 1), 3)

    for i, para in enumerate(paras):
        if re.match(r"^[序一二三四五六七八九十]、", para) or para.startswith("序"):
            jp(para, size=11)
            pdf.ln(2)
        else:
            jp(para, size=10.5)
            pdf.ln(1.5)

        if ill_idx < len(P0_ORDER) and (i + 1) % insert_every == 0:
            img_path = find_illustration(P0_ORDER[ill_idx])
            if img_path and img_path.exists():
                pdf.ln(2)
                pdf.set_x(pdf.l_margin)
                img_w = min(pdf.epw * 0.92, 110)
                pdf.image(str(img_path), w=img_w)
                pdf.ln(2)
                jp(f"［挿画 · {P0_ORDER[ill_idx]} · G1DRAFT］", size=7)
                pdf.ln(2)
            ill_idx += 1

    while ill_idx < len(P0_ORDER):
        img_path = find_illustration(P0_ORDER[ill_idx])
        if img_path and img_path.exists():
            pdf.add_page()
            pdf.set_x(pdf.l_margin)
            img_w = min(pdf.epw * 0.92, 110)
            pdf.image(str(img_path), w=img_w)
            pdf.ln(2)
            jp(f"［挿画 · {P0_ORDER[ill_idx]} · G1DRAFT］", size=7)
        ill_idx += 1

    pdf.output(str(OUT_PDF))
    return OUT_PDF


def main() -> int:
    try:
        out = build_pdf()
        size_kb = out.stat().st_size // 1024
        print(f"PDF: {out} ({size_kb} KB)")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
