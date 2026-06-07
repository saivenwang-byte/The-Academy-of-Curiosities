#!/usr/bin/env python3
"""Vol1 Reader Edition — 读者桥梁书 PDF（非 Review Pack）。

Scope:
  a001  — 序 + A001 试读 · 目标 ≤32p · 默认
  vol1  — 整卷（后续 · 144–160p）

Outputs:
  05_出版成果/Reader/学堂奇事録_Vol1_Reader_{scope}_日本語_{date}.pdf
  同名 .html

Reader-only: 无门禁表 · 无四栏审核 · 无 Shot Map 全表 · 无中文附录（默认）
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
FORMAL = TOOLS.parents[1]
SAMPLE = FORMAL.parent / "样章包"
OUT_DIR = FORMAL / "05_出版成果" / "Reader"
DISPLAY_TOOLS = FORMAL / "04_展示版" / "tools"
MASTER_CSS = TOOLS.resolve().parents[5] / "07_设计原档" / "05_读者版排版" / "reader_master.css"

BODY_DIR = FORMAL / "01_正文"
JP_A001 = BODY_DIR / "案01_めくれたポスター_V1.1定稿_日本語.txt"

CASE_JP: dict[str, tuple[str, str, str]] = {
    "a001": ("序+A001", "案01_めくれたポスター_V1.1定稿_日本語.txt", "めくれたポスター"),
    "a002": ("A002", "案02_ずれた泥のあと_V1.1定稿_日本語.txt", "ずれた泥のあと"),
    "a003": ("A003", "案03_空いているマス_V1.1定稿_日本語.txt", "空いているマス"),
    "a004": ("A004", "案04_チョークの粉の輪_V1.1定稿_日本語.txt", "チョークの粉の輪"),
    "a005": ("A005", "案05_消しゴムの屑の向き_V1.1定稿_日本語.txt", "消しゴムの屑の向き"),
}
DEPTH = SAMPLE / "插图" / "depth_anchor"
SUPP = DEPTH / "supplement"
ILLUST_SAMPLE = SAMPLE / "插图"
EXPERIMENT = SAMPLE / "12_案01_家庭实验页_样章.txt"
CLUE_MD = SAMPLE / "07_线索卡_设计稿.md"
HIKARU_SAMPLE = SAMPLE / "05_陸瑆日记页_样章.txt"

OUT_DATE = date.today().strftime("%Y%m%d")

# 段后插图（A 轨）— 对齐 V1.3 锁页 · stem 不含后缀
SHOT_SPECS: list[tuple[str, str | None, list[tuple[str, str, str, str]]]] = [
    ("序", None, [("V-S00_序钩_海报微翘", "fig-quarter", "V-S00 · 序 · ポスター", "V-S00")]),
    ("めくれたポスター", "1", [("V-S01-A1_侧廊发现", "fig-half", "DA1 · 側廊で発見", "DA1")]),
    ("めくれたポスター", "2", [
        ("V-S01-A2_误导搜查", "fig-half", "DA2 · 誤った捜査", "DA2"),
        ("V-S01-A2b_珣指风侧_MCU", "fig-inset", "DA2b · 風の側", "DA2b"),
    ]),
    ("めくれたポスター", "3", [
        ("V-S01-A3_风侧线索", "fig-half", "DA3 · 風側の手がかり", "DA3"),
        ("V-S01-A3b_胶带开边_ECUs", "fig-inset", "DA3b · テープの開き辺", "DA3b"),
    ]),
    ("めくれたポスター", "4", [
        ("V-S01-A4_验证收束", "fig-half", "DA4 · 検証と収束", "DA4"),
        ("V-S01-A4b_换贴对比_MCU", "fig-inset", "DA4b · 貼り方", "DA4b"),
        ("V-S01-TAIL_壁报空栏", "fig-quarter", "DC1 · 壁報の空欄", "DC1"),
    ]),
]

SUPPLEMENT_STEMS = {"V-S00_序钩_海报微翘", "V-S01-A2b_珣指风侧_MCU", "V-S01-A3b_胶带开边_ECUs", "V-S01-A4b_换贴对比_MCU"}

CAST_JP = """陸珣（りく しゅん）· 5年2組 · 転校生
伊藤光（いとう あきら）· 5年2組 · 学校おもしろ観察クラブ
加藤慧美（かとう けいみ）· 5年1組 · 記録
松本志郎（まつもと しろう）· 5年3組 · 検証
陸瑆（りく ひかる）· 4年2組 · 日記（B轨）"""

sys.path.insert(0, str(DISPLAY_TOOLS))
import build_display_edition as bde  # noqa: E402


def first_existing(candidates: list[Path]) -> Path | None:
    for p in candidates:
        if p.exists():
            return p
    return None


def asset_candidates(stem: str, tier: str) -> list[Path]:
    """Resolve depth/supplement PNG by tier: auto | g1draft | v0.2 | v1.0."""
    base_dir = SUPP if stem in SUPPLEMENT_STEMS else DEPTH
    if stem in SUPPLEMENT_STEMS:
        return [base_dir / f"{stem}_v0.1.png"]
    tiers = {
        "v1.0": [base_dir / f"{stem}_v1.0.png"],
        "g1draft": [base_dir / f"{stem}_G1draft.png"],
        "v0.2": [base_dir / f"{stem}_v0.2.png"],
        "legacy": [base_dir / f"{stem}.png"],
    }
    if tier == "auto":
        return tiers["v1.0"] + tiers["g1draft"] + tiers["v0.2"] + tiers["legacy"]
    if tier == "g1draft":
        return tiers["g1draft"] + tiers["v0.2"] + tiers["legacy"]
    if tier == "v0.2":
        return tiers["v0.2"] + tiers["legacy"]
    return tiers["v1.0"] + tiers["g1draft"] + tiers["v0.2"] + tiers["legacy"]


def shot_inject_for_tier(tier: str):
    out = []
    for ch_key, sec, figs in SHOT_SPECS:
        resolved = [(asset_candidates(stem, tier), css, cap, sid) for stem, css, cap, sid in figs]
        out.append((ch_key, sec, resolved))
    return out


def load_css() -> str:
    if MASTER_CSS.exists():
        return MASTER_CSS.read_text(encoding="utf-8")
    return "@page { size: A5; margin: 16mm; } body { font-size: 11pt; }"


def figure_html(paths: list[Path], css: str, caption: str) -> str:
    p = first_existing(paths)
    inner = (
        f'<img src="{bde.img_data_uri(p)}" alt="{caption}"/>'
        if p
        else f'<p class="cap">[{caption} · 画像待ち]</p>'
    )
    cap = f'<figcaption class="cap">{caption}</figcaption>' if p else ""
    return (
        f'<div class="figure-wrap">'
        f'<figure class="fig {css}">{inner}{cap}</figure>'
        f"</div>"
    )


def inject_shots(chapter: str, section: str | None, tier: str) -> str:
    parts: list[str] = []
    for ch_key, sec, figs in shot_inject_for_tier(tier):
        if ch_key not in chapter:
            continue
        if sec is not None and sec != section:
            continue
        for paths, css, cap, _sid in figs:
            parts.append(figure_html(paths, css, cap))
    return "\n".join(parts)


def prose_to_html(text: str, tier: str) -> str:
    blocks: list[str] = []
    current_chapter = ""
    pending_section: str | None = None
    section_paras: list[str] = []

    def flush_section() -> None:
        nonlocal pending_section, section_paras
        if pending_section is None:
            return
        sec_body = [f'<h3 class="section">{pending_section}</h3>']
        for para in section_paras:
            for p in para.split("\n"):
                p = p.strip()
                if p:
                    sec_body.append(f"<p>{p}</p>")
        fig = inject_shots(current_chapter, pending_section, tier)
        sec_html = "\n".join(sec_body)
        if fig:
            blocks.append(f'<div class="scene-block">{sec_html}{fig}<div class="clear"></div></div>')
        else:
            blocks.append(f'<div class="scene-block">{sec_html}</div>')
        pending_section = None
        section_paras = []

    for para in re.split(r"\n\s*\n", text.strip()):
        para = para.strip()
        if not para:
            continue
        if para.startswith("=") or para.startswith("【") or para.startswith("---"):
            continue
        if re.match(r"^『学堂", para) or re.match(r"^第1巻", para):
            continue
        lines = para.splitlines()
        if lines[0].startswith("序"):
            flush_section()
            current_chapter = "序"
            body = "\n".join(lines[1:]).strip()
            if body:
                blocks.append(f'<div class="scene-block"><h2 class="chapter">{lines[0]}</h2>')
                blocks.append(f"<p>{body.replace(chr(10), '</p><p>')}</p>")
                fig = inject_shots(current_chapter, None, tier)
                if fig:
                    blocks.append(f"{fig}<div class=\"clear\"></div></div>")
                else:
                    blocks.append("</div>")
            else:
                blocks.append(f'<h2 class="chapter">{lines[0]}</h2>')
            continue
        if re.match(r"^一、", lines[0]):
            flush_section()
            current_chapter = "めくれたポスター"
            blocks.append(
                '<div class="title-strip">'
                '<p class="case-no">第 1 起</p>'
                f'<h2>{lines[0]}</h2></div>'
            )
            continue
        if re.match(r"^###\s+(\d+)", lines[0]):
            flush_section()
            pending_section = re.match(r"^###\s+(\d+)", lines[0]).group(1)
            body = "\n".join(lines[1:]).strip()
            if body:
                section_paras.append(body)
            continue
        if pending_section is not None:
            section_paras.append(para)
            continue
        if lines[0].startswith("---"):
            continue
        blocks.append(f"<p>{para.replace(chr(10), '</p><p>')}</p>")
    flush_section()
    return "\n".join(blocks)


def clue_box_html() -> str:
    raw = bde.read_text(CLUE_MD) if CLUE_MD.exists() else ""
    m = re.search(r"```\n([\s\S]*?)```", raw)
    box = m.group(1).strip() if m else "观察社 · 线索卡 #01\n（版式 E22 待决）"
    return f'<pre class="clue-box">{box}</pre>'


def experiment_html() -> str:
    raw = bde.read_text(EXPERIMENT) if EXPERIMENT.exists() else ""
    raw = re.sub(r"^# .+\n", "", raw)
    raw = re.sub(r"^> .+\n", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"^---\n", "", raw, flags=re.MULTILINE)
    parts = []
    for para in re.split(r"\n\s*\n", raw.strip()):
        para = para.strip()
        if not para or para.startswith("（"):
            continue
        if para.startswith("**") and para.endswith("**"):
            parts.append(f"<h3>{para.strip('*')}</h3>")
        elif para.startswith("- "):
            items = "".join(f"<li>{ln[2:]}</li>" for ln in para.split("\n") if ln.startswith("- "))
            parts.append(f"<ul>{items}</ul>")
        else:
            parts.append(f"<p>{para.replace(chr(10), '<br/>')}</p>")
    return "\n".join(parts)


def hikaru_html() -> str:
    img = first_existing([
        ILLUST_SAMPLE / "V-S02_瑆日记页_v0.1.png",
        FORMAL / "02_插画" / "assets" / "V-S02_陸瑆日记页.png",
    ])
    img_part = figure_html([img], "fig-half", "V-S02 · 瑆のノート") if img else ""
    raw = bde.read_text(HIKARU_SAMPLE) if HIKARU_SAMPLE.exists() else ""
    raw = re.sub(r"^=+\n", "", raw)
    raw = re.sub(r"^【.+?\n", "", raw, flags=re.MULTILINE)
    lines = [ln for ln in raw.splitlines() if ln.strip() and not ln.startswith("---")]
    body = "".join(f"<p>{ln}</p>" for ln in lines if not ln.startswith("（画"))
    return f"{img_part}<div class=\"diary-page\">{body}</div>"


def post_story_html(tier: str) -> str:
    db1 = figure_html(
        asset_candidates("V-S01-B1_风侧机制图", tier),
        "fig-half",
        "DB1 · 風と湿度と貼り方",
    )
    return f"""
<section class="post-story">
  <h2>このあと · 確かめてみよう</h2>
  <p class="lead">物語のあとに読む · 仕組み · 手がかり · 実験 · 瑆のノート</p>
  <h3>風の向きとポスター</h3>
  {db1}
  <h3>観察クラブ · 手がかりカード #01</h3>
  {clue_box_html()}
  <h3>おうちで試せる</h3>
  {experiment_html()}
  <h3>陸瑆（ひかる）のノート</h3>
  {hikaru_html()}
</section>
"""


GATE_A_WATERMARK_CSS = """
body.gate-a-mvp::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background: repeating-linear-gradient(
    -35deg,
    transparent,
    transparent 180px,
    rgba(180, 60, 40, 0.06) 180px,
    rgba(180, 60, 40, 0.06) 181px
  );
}
.watermark-banner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-28deg);
  font-size: 22pt;
  font-weight: 600;
  color: rgba(160, 50, 35, 0.14);
  white-space: nowrap;
  pointer-events: none;
  z-index: 9998;
  letter-spacing: 0.12em;
}
.badge-gate-a {
  display: inline-block;
  background: #8b3a2a;
  color: #fff;
  font-size: 8pt;
  padding: 0.25em 0.6em;
  border-radius: 2px;
  margin-bottom: 0.6em;
}
"""


def build_case_html(
    scope: str,
    *,
    tier: str = "auto",
    out_date: str | None = None,
    gate_a: bool = False,
) -> str:
    css = load_css()
    if gate_a:
        css += GATE_A_WATERMARK_CSS
    stamp = out_date or OUT_DATE
    label, fname, case_title = CASE_JP[scope]
    jp_path = BODY_DIR / fname
    jp_raw = bde.strip_txt_meta(bde.read_text(jp_path))
    body = prose_to_html(jp_raw, tier)
    cover_img = first_existing(asset_candidates("V-S01-A1_侧廊发现", tier))
    cover_uri = bde.img_data_uri(cover_img) if cover_img else ""
    body_class = ' class="gate-a-mvp"' if gate_a else ""
    wm_div = '<div class="watermark-banner">Gate A MVP · 非出版清样</div>' if gate_a else ""
    badge = (
        '<p class="badge-gate-a">Gate A MVP · 非出版清样</p>'
        if gate_a
        else '<p class="badge-reader">Reader Edition · 橋渡し読み本 · 試読</p>'
    )
    intro = (
        "この本は <strong>Gate A 样张 MVP</strong> です。G1draft 六帧 · 内审/E20 试读 · <strong>非</strong> 出版清样。"
        if gate_a
        else "この本は <strong>読者試読版</strong> です。おかしいと思ったら、まず見てみる——観察クラブの最初の一件。"
    )
    rights = (
        f"© 学堂奇事録 · {stamp} · Gate A MVP · 非出版清样 · RGB"
        if gate_a
        else f"© 学堂奇事録 · {stamp} · 非売品試読 · RGB"
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>学堂奇事録 · 第1巻 · 第1起（Reader）</title>
<style>{css}</style>
</head>
<body{body_class}>
{wm_div}

<div class="cover reader-break">
  {badge}
  <h1>学堂奇事録</h1>
  <p class="vol">第1巻 · おかしいと思ったら、まず見てみる<br/>第 1 起 · めくれたポスター</p>
  <p class="tagline">謎が、解ける日。</p>
  {"<img src='" + cover_uri + "' alt='cover'/>" if cover_uri else ""}
</div>

<div class="front-matter reader-break copyright">
  <h2>はじめに</h2>
  <p>{intro}</p>
  <p style="font-size:9pt;color:#666;">{rights}</p>
  <h2>登場人物</h2>
  <pre class="cast">{CAST_JP}</pre>
  <h2>目次</h2>
  <ul class="toc">
    <li>序 · 四月の第二月曜日</li>
    <li>第 1 起 · めくれたポスター</li>
  </ul>
</div>

<div class="prose-flow">
{body}
</div>

{post_story_html(tier)}

</body>
</html>
"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    if not bde.html_to_pdf_chrome(html_path, pdf_path):
        raise RuntimeError("Chrome/Edge headless PDF failed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vol1 Reader Edition PDF")
    parser.add_argument("--scope", choices=["a001", "a002", "a003", "a004", "a005", "vol1"], default="a001")
    parser.add_argument("--tier", choices=["auto", "g1draft", "v0.2", "v1.0"], default="auto")
    parser.add_argument("--gate-a", action="store_true", help="Gate A MVP: g1draft tier + watermark + 非出版清样")
    parser.add_argument("--out-dir", type=Path, default=None, help="Override output directory")
    parser.add_argument("--date", default=None, help="YYYYMMDD stamp for filenames (default: today)")
    args = parser.parse_args()

    if args.scope == "vol1":
        print("vol1 整卷 Reader 尚未实现 · 请先 --scope a001", file=sys.stderr)
        return 1

    tier = "g1draft" if args.gate_a else args.tier
    gate_a = args.gate_a
    stamp = args.date or OUT_DATE
    out_dir = args.out_dir or OUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    label, _, _ = CASE_JP[args.scope]
    suffix = "_GateA" if gate_a else ""
    stem = f"学堂奇事録_Vol1_Reader_{label}_日本語{suffix}_{stamp}"
    html_path = out_dir / f"{stem}.html"
    pdf_path = out_dir / f"{stem}.pdf"

    html_path.write_text(
        build_case_html(args.scope, tier=tier, out_date=stamp, gate_a=gate_a),
        encoding="utf-8",
    )
    print(f"Wrote {html_path} (tier={tier}, gate_a={gate_a})")

    try:
        html_to_pdf(html_path, pdf_path)
        print(f"Wrote {pdf_path}")
    except Exception as e:
        print(f"PDF failed ({e}) · open HTML in browser to print", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
