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

# 段后插图（A 轨）— 对齐 V1.3 锁页
SHOT_INJECT: list[tuple[str, str | None, list[tuple[list[Path], str, str, str]]]] = [
    ("序", None, [([SUPP / "V-S00_序钩_海报微翘_v0.1.png"], "fig-quarter", "V-S00 · 序 · ポスター", "V-S00")]),
    ("めくれたポスター", "1", [([DEPTH / "V-S01-A1_侧廊发现_v0.2.png", DEPTH / "V-S01-A1_侧廊发现.png"], "fig-half", "DA1 · 側廊で発見", "DA1")]),
    ("めくれたポスター", "2", [
        ([DEPTH / "V-S01-A2_误导搜查_v0.2.png", DEPTH / "V-S01-A2_误导搜查.png"], "fig-half", "DA2 · 誤った捜査", "DA2"),
        ([SUPP / "V-S01-A2b_珣指风侧_MCU_v0.1.png"], "fig-inset", "DA2b · 風の側", "DA2b"),
    ]),
    ("めくれたポスター", "3", [
        ([DEPTH / "V-S01-A3_风侧线索_v0.2.png", DEPTH / "V-S01-A3_风侧线索.png"], "fig-half", "DA3 · 風側の手がかり", "DA3"),
        ([SUPP / "V-S01-A3b_胶带开边_ECUs_v0.1.png"], "fig-inset", "DA3b · テープの開き辺", "DA3b"),
    ]),
    ("めくれたポスター", "4", [
        ([DEPTH / "V-S01-A4_验证收束_v0.2.png", DEPTH / "V-S01-A4_验证收束.png"], "fig-half", "DA4 · 検証と収束", "DA4"),
        ([SUPP / "V-S01-A4b_换贴对比_MCU_v0.1.png"], "fig-inset", "DA4b · 貼り方", "DA4b"),
        ([DEPTH / "V-S01-TAIL_壁报空栏_v0.2.png", DEPTH / "V-S01-TAIL_壁报空栏.png"], "fig-quarter", "DC1 · 壁報の空欄", "DC1"),
    ]),
]

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


def inject_shots(chapter: str, section: str | None) -> str:
    parts: list[str] = []
    for ch_key, sec, figs in SHOT_INJECT:
        if ch_key not in chapter:
            continue
        if sec is not None and sec != section:
            continue
        for paths, css, cap, _sid in figs:
            parts.append(figure_html(paths, css, cap))
    return "\n".join(parts)


def prose_to_html(text: str) -> str:
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
        fig = inject_shots(current_chapter, pending_section)
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
                fig = inject_shots(current_chapter, None)
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


def post_story_html() -> str:
    db1 = figure_html(
        [DEPTH / "V-S01-B1_风侧机制图_v0.2.png", DEPTH / "V-S01-B1_风侧机制图.png"],
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


def build_case_html(scope: str) -> str:
    css = load_css()
    label, fname, case_title = CASE_JP[scope]
    jp_path = BODY_DIR / fname
    jp_raw = bde.strip_txt_meta(bde.read_text(jp_path))
    body = prose_to_html(jp_raw)
    cover_img = first_existing([DEPTH / "V-S01-A1_侧廊发现_v0.2.png"])
    cover_uri = bde.img_data_uri(cover_img) if cover_img else ""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>学堂奇事録 · 第1巻 · 第1起（Reader）</title>
<style>{css}</style>
</head>
<body>

<div class="cover reader-break">
  <p class="badge-reader">Reader Edition · 橋渡し読み本 · 試読</p>
  <h1>学堂奇事録</h1>
  <p class="vol">第1巻 · おかしいと思ったら、まず見てみる<br/>第 1 起 · めくれたポスター</p>
  <p class="tagline">謎が、解ける日。</p>
  {"<img src='" + cover_uri + "' alt='cover'/>" if cover_uri else ""}
</div>

<div class="front-matter reader-break copyright">
  <h2>はじめに</h2>
  <p>この本は <strong>読者試読版</strong> です。おかしいと思ったら、まず見てみる——観察クラブの最初の一件。</p>
  <p style="font-size:9pt;color:#666;">© 学堂奇事録 · {OUT_DATE} · 非売品試読 · RGB</p>
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

{post_story_html()}

</body>
</html>
"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    if not bde.html_to_pdf_chrome(html_path, pdf_path):
        raise RuntimeError("Chrome/Edge headless PDF failed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Vol1 Reader Edition PDF")
    parser.add_argument("--scope", choices=["a001", "a002", "a003", "a004", "a005", "vol1"], default="a001")
    args = parser.parse_args()

    if args.scope == "vol1":
        print("vol1 整卷 Reader 尚未实现 · 请先 --scope a001", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    label, _, _ = CASE_JP[args.scope]
    stem = f"学堂奇事録_Vol1_Reader_{label}_日本語_{OUT_DATE}"
    html_path = OUT_DIR / f"{stem}.html"
    pdf_path = OUT_DIR / f"{stem}.pdf"

    html_path.write_text(build_case_html(args.scope), encoding="utf-8")
    print(f"Wrote {html_path}")

    try:
        html_to_pdf(html_path, pdf_path)
        print(f"Wrote {pdf_path}")
    except Exception as e:
        print(f"PDF failed ({e}) · open HTML in browser to print", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
