#!/usr/bin/env python3
"""Vol1 expert-standard publication pack: Japanese PDF + proposal PPT.

Aligns with:
  - 00_项目总览/创作标准与验收流程.md
  - 11_检查项Skill包_v0.1.md (C03/V13/S18)
  - 15_出版全流程阶段状态.md · 样章包 13_试读PDF拼装说明
  - 品牌名称定稿 · 正典门禁 2026-06-04

Outputs (05_出版成果/):
  - 学堂奇事録_Vol1_正式出版成果_日本語_{date}.pdf
  - 学堂奇事録_Vol1_出版提案_{date}.pptx
  - 出版成果_门禁对照表_{date}.md
"""

from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
FORMAL = TOOLS.parents[1]  # 正式版/
OUT = FORMAL / "05_出版成果"
DISPLAY_TOOLS = FORMAL / "04_展示版" / "tools"
ILLUST_TOOLS = FORMAL / "02_插画" / "tools"

OUT_DATE = date.today().strftime("%Y%m%d")
PDF_NAME = f"学堂奇事録_Vol1_正式出版成果_日本語_{OUT_DATE}.pdf"
HTML_NAME = f"学堂奇事録_Vol1_正式出版成果_日本語_{OUT_DATE}.html"
PPT_NAME = f"学堂奇事録_Vol1_出版提案_{OUT_DATE}.pptx"
GATE_MD = f"出版成果_门禁对照表_{OUT_DATE}.md"

sys.path.insert(0, str(DISPLAY_TOOLS))
import build_display_edition as bde  # noqa: E402


def run_prep() -> None:
    subprocess.run([sys.executable, str(ILLUST_TOOLS / "generate_vol1_illustrations.py")], check=True)
    subprocess.run([sys.executable, str(DISPLAY_TOOLS / "assemble_jp_canon.py")], check=True)


def gate_rows() -> list[tuple[str, str, str, str]]:
    """id, category, status, note"""
    return [
        ("正典", "Vol1=Plan B A001–A005", "✅ LOCK", "非湿椅子 C001"),
        ("正典", "首市场=日本", "✅ LOCK", "学堂奇事録"),
        ("正典", "珣=しゅん / 瑆=ひかる", "✅ LOCK", "名称 LOCK 2026-06-05"),
        ("C03", "5案轻推理结构", "✅", "L1 尾钩串联"),
        ("C03b", "公平线索", "✅/🟡", "A001–A003 定稿 · A004–A005 初稿"),
        ("C03c", "卷级钩子", "✅", "壁报待续 → Vol2"),
        ("C04", "温柔真相", "✅", "无羞辱/无霸凌"),
        ("V13", "桥梁书年龄感", "✅/🟡", "V-S01 AI · V-S02–05 v0.9"),
        ("V14", "陸珣视觉入口", "✅", "侧后观察位"),
        ("S18", "校园怪异上限", "✅", "零恐怖"),
        ("S20", "红线", "✅", "无湿椅子主叙事"),
        ("E04", "日文文体", "🟡", "A001 JP_VOICE_v1 · ②–⑤初译"),
        ("E07", "田中校园五维", "⬜", "待全文督查"),
        ("E20", "试读反馈", "⬜", "本包可发专家/出版社"),
        ("L2", "Scorecard ≥180", "🟡", "A001 READY_FOR_SAMPLE"),
    ]


def gate_table_html(lang: str = "ja") -> str:
    title = "正典・专家门禁对照" if lang == "ja" else "正典与专家门禁"
    hdr = ["項目", "区分", "状態", "備考"] if lang == "ja" else ["项", "类别", "状态", "备注"]
    rows = gate_rows()
    trs = "".join(
        f"<tr><td>{a}</td><td>{b}</td><td class='st'>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows
    )
    return f"""
    <div class="page gate-page">
      <h2>{title}</h2>
      <p class="lead">依据 <code>11_检查项Skill包</code> · <code>创作标准与验收流程</code> · 专家池 E04/E07/E20</p>
      <table class="gate-table">
        <thead><tr>{''.join(f'<th>{h}</th>' for h in hdr)}</tr></thead>
        <tbody>{trs}</tbody>
      </table>
      <p class="note">⬜=待人审 · 🟡=Agent+初稿可发 · ✅=已过或正典锁定</p>
    </div>
    """


def positioning_html() -> str:
    return """
    <div class="page">
      <h2>IP定位 · 出版提案摘要</h2>
      <blockquote class="tagline">謎が、解ける日。</blockquote>
      <p><strong>対象</strong>：7–11歳（主 8–10）· 校园軽推理成長 IP</p>
      <p><strong>設計原則</strong>：かわいさで入る · 謎で留まる · キャラで戻る · 観察で続く</p>
      <p><strong>境界</strong>：硬科普/教辅/恐怖/大人破案 ✗ · 日常小異常+温柔真相 ✓</p>
      <p><strong>Vol1</strong>：Plan B · 5年2組 陸珣（しゅん）視点 · 観察クラブ入門 · 5事件合订</p>
      <p class="src">出典：B1 立项定位 · E1 观察社战略 · F1 Vol1结构 · 品牌名称定稿</p>
    </div>
    """


def case_overview_html() -> str:
    cases = [
        ("A001", "①", "めくれたポスター", "湿度·気流·貼り方", "✅"),
        ("A002", "②", "ズレた泥のあと", "動線·側門の土", "✅"),
        ("A003", "③", "空いている欄", "確認待ち·掲示規則", "✅"),
        ("A004", "④", "チョーク粉の輪", "静電·掃除順", "🟡"),
        ("A005", "⑤", "消しゴムのカス", "摩擦·入社", "🟡"),
    ]
    rows = "".join(
        f"<tr><td>{a}</td><td>{n}</td><td>{t}</td><td>{k}</td><td>{s}</td></tr>"
        for a, n, t, k, s in cases
    )
    return f"""
    <div class="page">
      <h2>事件一覧 · Case Card 要約</h2>
      <table class="case-table">
        <thead><tr><th>ID</th><th>案</th><th>タイトル</th><th>核心</th><th>稿</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <p>L1 尾钩：空欄→投稿→裏の路→中谷半句→瑆誤描 · L3 巻末壁報第2起</p>
    </div>
    """


def copyright_html() -> str:
    return f"""
    <div class="page copyright">
      <h2>出版成果声明</h2>
      <p><strong>『学堂奇事録』第1巻</strong><br/>
      おかしいと思ったら、まず見てみる</p>
      <ul>
        <li>種別：<strong>正式出版成果パック</strong>（提案/专家审稿用）</li>
        <li>版：{OUT_DATE} · 非売品 · 印厂原稿ではありません</li>
        <li>言語：本文日本語 · 正典中文併記は別ファイル</li>
        <li>著作：The Academy of Curiosities / 学堂趣事录 IP</li>
      </ul>
      <p>試読・专家审稿の際は <code>09_专家审稿表</code> を併用してください。</p>
    </div>
    """


def expert_appendix_html() -> str:
    return """
    <div class="page">
      <h2>专家审稿指引（附录）</h2>
      <h3>E05 軽推理 · E07 校园 · E04 日文 · E13 安全</h3>
      <ol>
        <li>解前に ≥3 公平线索是否可见？（Sobol）</li>
        <li>侧廊·クラブ·壁報流程是否可信？（E07）</li>
        <li>A004–A005 日文是否直译腔过重？（E04）</li>
        <li>家庭实验是否可安全模仿？（E13）</li>
        <li>V-S02–V05 v0.9 是否需画师升级？（E06/V13）</li>
      </ol>
      <p>填写模板：<code>样章包/09_专家审稿表_模板.md</code></p>
    </div>
    """


def build_expert_html() -> str:
    m = bde.META["ja"]
    bde.ensure_jp_canon()
    canon_raw = bde.strip_txt_meta(bde.read_text(bde.CANON_JP))
    body_html = bde.md_prose_to_html(canon_raw, "ja")
    notes_html = bde.notes_to_html(bde.read_text(bde.NOTES_JP), "ja")
    gallery = bde.illust_gallery_html("ja")

    v_s01 = ""
    p = bde.ILLUST / "V-S01_侧廊海报.png"
    if p.exists():
        v_s01 = bde.img_data_uri(p)

    toc = "".join(f"<li>{item}</li>" for item in m["toc"])
    chars = (
        "陸珣（りく しゅん）· 5年2組 · 転校生\n"
        "伊藤光 · 5年2組 · おもしろ観察クラブ\n"
        "加藤慧美（けいみ）· 5年1組 · 記録\n"
        "松本志郎 · 5年3組 · 検証\n"
        "陸瑆（ひかる）· 4年2組 · 日記\n"
        "中谷琦 · 6年1組 · 半句"
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>学堂奇事録 Vol1 正式出版成果</title>
<style>
@page {{ size: A5; margin: 14mm 12mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: {m["font_stack"]};
  font-size: 10.5pt; line-height: 1.58; color: #1a1a1a; max-width: 148mm; margin: 0 auto;
}}
.page {{ page-break-after: always; padding: 4mm 0; min-height: 220mm; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{
  display:flex; flex-direction:column; justify-content:center; align-items:center;
  text-align:center; min-height:240mm;
  background: linear-gradient(165deg, #faf7f2 0%, #e8e0d4 100%);
}}
.cover .series {{ font-size: 11pt; letter-spacing: 0.2em; color: #666; }}
.cover h1 {{ font-size: 24pt; margin: 0.3em 0; }}
.cover h2 {{ font-size: 13pt; font-weight: normal; color: #333; }}
.cover .tag {{ font-size: 12pt; color: #8a6d4b; margin-top: 1em; font-style: italic; }}
.cover .badge {{ margin-top: 1.2em; font-size: 9pt; border: 1px solid #999; padding: 0.3em 0.8em; }}
.cover img {{ max-width: 70%; margin: 1em 0; border: 1px solid #ccc; }}
h2 {{ font-size: 12pt; border-bottom: 1px solid #bbb; padding-bottom: 0.2em; }}
h3 {{ font-size: 10.5pt; color: #444; }}
.lead {{ font-size: 9pt; color: #666; }}
blockquote.tagline {{ font-size: 14pt; text-align:center; border:none; color:#6a5040; margin:1em 0; }}
.gate-table, .case-table {{ width:100%; border-collapse: collapse; font-size: 9pt; margin: 0.8em 0; }}
.gate-table th, .gate-table td, .case-table th, .case-table td {{
  border: 1px solid #ccc; padding: 0.35em 0.45em; vertical-align: top;
}}
.gate-table .st {{ font-weight: bold; white-space: nowrap; }}
.note, .src {{ font-size: 8.5pt; color: #777; }}
.copyright ul {{ font-size: 9.5pt; line-height: 1.6; }}
.toc {{ list-style: none; padding: 0; }}
.toc li {{ padding: 0.3em 0; border-bottom: 1px dotted #ccc; }}
.prose h2.chapter {{ page-break-before: auto; }}
h2.chapter {{ font-size: 11.5pt; margin-top: 0.9em; page-break-after: avoid; }}
h3.section {{ font-size: 10pt; color: #555; }}
p {{ margin: 0.5em 0; }}
.illus {{ text-align:center; margin: 0.6em 0; page-break-inside: avoid; }}
.illus img {{ max-width: 100%; height: auto; }}
.illus.half img {{ max-height: 80mm; }}
.illus.quarter img {{ max-height: 48mm; }}
.illus figcaption {{ font-size: 8pt; color: #666; }}
.diary-page {{
  background: #fffef8; padding: 1em; border-left: 3px solid #d4c4a8;
  background-image: repeating-linear-gradient(#0000 0 1.3em, #e8e4dc 1.3em 1.31em);
}}
hr.scene-break {{ border: none; border-top: 1px dotted #ccc; margin: 1em 0; }}
.colophon {{ text-align:center; font-size: 8pt; color: #888; margin-top: 2em; }}
@media print {{ body {{ max-width: none; }} }}
</style>
</head>
<body>

<div class="page cover">
  <p class="series">がくどう きじろく · Gakudō Kijiroku</p>
  <h1>学堂奇事録</h1>
  <h2>第1巻 · おかしいと思ったら、まず見てみる</h2>
  <p class="tag">謎が、解ける日。</p>
  {"<img src='" + v_s01 + "' alt='cover'/>" if v_s01 else ""}
  <p class="badge">正式出版成果 · 日本語 · {OUT_DATE}<br/>专家库标准 · IP正典 Plan B</p>
</div>

{copyright_html()}
{gate_table_html()}
{positioning_html()}
{case_overview_html()}

<div class="page">
  <h2>{m["chars_title"]}</h2>
  <pre style="white-space:pre-wrap;font-family:inherit;font-size:10pt;">{chars}</pre>
</div>

<div class="page">
  <h2>{m["toc_title"]}</h2>
  <ul class="toc">{toc}</ul>
</div>

<div class="page prose">
  {body_html}
</div>

<div class="page diary-page">
  <h2>{m["notes_title"]}</h2>
  {notes_html}
</div>

<div class="page">
  <h2>挿画一覧 · V-S01–V-S05</h2>
  <p class="lead">V-S01/01-TAIL：样章 AI 成图 · V-S02–05：v0.9（可画师替换同名文件）</p>
  {gallery}
</div>

{expert_appendix_html()}

<div class="page">
  <p class="colophon">
    『学堂奇事録』Vol1 正式出版成果 · {OUT_DATE}<br/>
    rebuild: python 05_出版成果/tools/build_expert_publication_pack.py
  </p>
</div>

</body>
</html>
"""


def write_gate_md() -> Path:
    lines = [
        f"# Vol1 出版成果 · 门禁对照表 · {OUT_DATE}",
        "",
        "| 项 | 类别 | 状态 | 备注 |",
        "|----|------|------|------|",
    ]
    for a, b, c, d in gate_rows():
        lines.append(f"| {a} | {b} | {c} | {d} |")
    lines.extend(["", "生成：`build_expert_publication_pack.py`", ""])
    path = OUT / GATE_MD
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_ppt(pdf_hint: Path) -> Path | None:
    try:
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "python-pptx", "-q"], check=True)
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.enum.text import PP_ALIGN

    # 16:9 widescreen (1920×1080 equivalent · 16in × 9in)
    W16 = Inches(16)
    H9 = Inches(9)
    MX = Inches(0.65)
    MY = Inches(0.45)
    CW = W16 - 2 * MX  # content width

    prs = Presentation()
    prs.slide_width = W16
    prs.slide_height = H9
    blank = prs.slide_layouts[6]

    def add_title_slide(title: str, subtitle: str = "", tagline: str = "") -> None:
        s = prs.slides.add_slide(blank)
        box = s.shapes.add_textbox(MX, Inches(2.0), CW, Inches(4.5))
        tf = box.text_frame
        tf.text = title
        tf.paragraphs[0].font.size = Pt(40)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        if tagline:
            p = tf.add_paragraph()
            p.text = tagline
            p.font.size = Pt(22)
            p.font.italic = True
            p.alignment = PP_ALIGN.CENTER
        if subtitle:
            p = tf.add_paragraph()
            p.text = subtitle
            p.font.size = Pt(18)
            p.alignment = PP_ALIGN.CENTER
        # footer badge
        foot = s.shapes.add_textbox(MX, Inches(8.35), CW, Inches(0.4))
        foot.text_frame.text = f"16:9 出版提案 · {OUT_DATE}"
        foot.text_frame.paragraphs[0].font.size = Pt(10)
        foot.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    def add_bullets(title: str, lines: list[str], cols: int = 1) -> None:
        s = prs.slides.add_slide(blank)
        title_box = s.shapes.add_textbox(MX, MY, CW, Inches(0.7))
        title_box.text_frame.text = title
        title_box.text_frame.paragraphs[0].font.size = Pt(30)
        title_box.text_frame.paragraphs[0].font.bold = True
        col_w = (CW - Inches(0.4)) / cols if cols > 1 else CW
        for ci in range(cols):
            chunk = lines[ci :: cols] if cols > 1 else lines
            left = MX + ci * (col_w + Inches(0.4))
            tb = s.shapes.add_textbox(left, Inches(1.15), col_w, Inches(7.2))
            tf = tb.text_frame
            tf.word_wrap = True
            for i, line in enumerate(chunk):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = line
                p.font.size = Pt(17 if cols == 1 else 15)
                p.space_after = Pt(6)

    add_title_slide(
        "学堂奇事録",
        f"第1巻 · おかしいと思ったら、まず見てみる",
        "謎が、解ける日。",
    )
    add_title_slide(
        "出版提案 · 首市场日本",
        "7–11歳（主 8–10）· 名古屋 · 校园軽推理 · Plan B",
    )

    add_bullets(
        "IP定位（B1 / E1 / 品牌定稿）",
        [
            "• 日常の「小異常」→ 観察 → 温柔な真相",
            "• かわいさで入る · 謎で留まる · キャラで戻る · 観察で続く",
            "• 硬科普/教辅/恐怖/大人破案 ✗",
            "• 子どもが読みたい · 親が成長を認める · シリーズ化可",
            "• Vol1：5年2組 陸珣（しゅん）· 観察クラブ入門 · 5事件合订",
        ],
    )

    case_lines = [
        "A001 ① めくれたポスター · 湿度/気流 ✅",
        "A002 ② ズレた泥のあと · 動線/側門 ✅",
        "A003 ③ 空いている欄 · 確認待ち ✅",
        "A004 ④ チョーク粉の輪 · 静電/掃除 🟡",
        "A005 ⑤ 消しゴムのカス · 摩擦/入社 🟡",
        "L1 尾钩：空欄→投稿→裏の路→中谷半句→瑆誤描",
        "L3 巻末：壁報第2起 → Vol2",
    ]
    add_bullets("事件 A001–A005 · Case Card", case_lines, cols=2)

    img_path = bde.ILLUST / "V-S01_侧廊海报.png"
    if img_path.exists():
        s = prs.slides.add_slide(blank)
        tbox = s.shapes.add_textbox(MX, MY, Inches(5.5), Inches(0.6))
        tbox.text_frame.text = "主视觉 · V-S01"
        tbox.text_frame.paragraphs[0].font.size = Pt(26)
        tbox.text_frame.paragraphs[0].font.bold = True
        tb = s.shapes.add_textbox(MX, Inches(1.1), Inches(5.2), Inches(7.5))
        tf = tb.text_frame
        for i, line in enumerate(
            [
                "側廊 · 手描きポスター",
                "めくれる辺 = 風の側",
                "桥梁书 · 8–10歳可读线索",
                "V-S02–V05 同系列嵌入",
            ]
        ):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = "• " + line
            p.font.size = Pt(16)
        pic_w = Inches(9.2)
        pic_left = MX + Inches(5.8)
        s.shapes.add_picture(str(img_path), pic_left, Inches(0.85), width=pic_w)

    gate_lines = [f"{a} · {b} · {c} · {d}" for a, b, c, d in gate_rows()]
    add_bullets("正典 · 专家门禁（11_检查项 / E04·E07·E20）", gate_lines, cols=2)

    add_title_slide(
        "成果物",
        f"PDF：{pdf_hint.name}\n"
        f"PPT：{PPT_NAME}（16:9）\n"
        "待：E07 田中 · E04 全文推敲 · 画师终稿 V-S02–05",
    )

    out = OUT / PPT_NAME
    prs.save(str(out))
    return out


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    run_prep()

    html = build_expert_html()
    html_path = OUT / HTML_NAME
    html_path.write_text(html, encoding="utf-8")
    print(f"HTML: {html_path}")

    pdf_path = OUT / PDF_NAME
    ok = bde.html_to_pdf_chrome(html_path, pdf_path)
    if not ok:
        print("PDF export failed — open HTML and print", file=sys.stderr)
        return 1
    print(f"PDF: {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")

    gate_path = write_gate_md()
    print(f"Gate MD: {gate_path}")

    ppt_path = build_ppt(pdf_path)
    if ppt_path:
        print(f"PPT: {ppt_path} ({ppt_path.stat().st_size // 1024} KB)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
