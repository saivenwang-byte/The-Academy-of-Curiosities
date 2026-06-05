#!/usr/bin/env python3
"""Assemble Vol1 sample reading pack → HTML + PDF (A5)."""

from __future__ import annotations

import base64
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "PDF"
ILLUST = ROOT / "插图"
OUT_DATE = date.today().strftime("%Y%m%d")
PDF_NAME = f"学堂趣事录_Vol1_样章试读_{OUT_DATE}.pdf"
HTML_NAME = f"学堂趣事录_Vol1_样章试读_{OUT_DATE}.html"

FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttf"),
    Path(r"C:\Windows\Fonts\simsun.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
]

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_hybridvoice_body(raw: str) -> str:
    """Remove header meta and editor notes (lines 181+)."""
    lines = raw.splitlines()
    body: list[str] = []
    for line in lines:
        if line.strip().startswith("---") and body:
            break
        if line.startswith("【样章包") or line.startswith("  ·"):
            continue
        body.append(line)
    # trim trailing meta block marker
    while body and body[-1].strip() == "":
        body.pop()
    return "\n".join(body).strip()


def prose_to_html(text: str) -> str:
    """Minimal prose → HTML paragraphs."""
    blocks: list[str] = []
    para: list[str] = []
    for line in text.splitlines():
        s = line.rstrip()
        if not s:
            if para:
                blocks.append("<p>" + "<br/>".join(para) + "</p>")
                para = []
            continue
        if re.match(r"^={3,}$", s) or re.match(r"^-{3,}$", s):
            continue
        if s.startswith("《学堂趣事录》") or s.startswith("第1卷"):
            blocks.append(f'<h1 class="book-title">{s}</h1>')
            continue
        if re.match(r"^序 ·", s) or re.match(r"^一、", s):
            blocks.append(f'<h2 class="chapter">{s}</h2>')
            continue
        if re.match(r"^### \d", s):
            blocks.append(f'<h3 class="section">{s.replace("### ", "")}</h3>')
            continue
        if s.startswith("  ") and not s.startswith("  http"):
            para.append(f'<span class="indent">{s.strip()}</span>')
        else:
            para.append(s)
    if para:
        blocks.append("<p>" + "<br/>".join(para) + "</p>")
    return "\n".join(blocks)


def img_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_html() -> str:
    hybrid = strip_hybridvoice_body(read_text(ROOT / "04_样章_序+案01_正文_HybridVoice.txt"))
    diary = read_text(ROOT / "05_陸瑆日记页_样章.txt")
    diary_body = re.split(r"---", diary)[0].strip()
    diary_html = prose_to_html(diary_body)

    chars_md = read_text(ROOT / "08_角色介绍_一页.md")
    # strip md front matter blocks
    chars_html = re.sub(r"^# .+\n", "", chars_md, count=1)
    chars_html = re.sub(r"^> .+\n", "", chars_html, flags=re.MULTILINE)
    chars_html = re.sub(r"^---\n", "", chars_html, flags=re.MULTILINE)
    chars_html = chars_html.replace("|", " ").replace("---", "")

    experiment = read_text(ROOT / "12_案01_家庭实验页_样章.txt")
    exp_html = prose_to_html(re.sub(r"^# .+\n", "", experiment))

    v_s01 = img_data_uri(ILLUST / "V-S01_侧廊海报.png")
    v_tail = img_data_uri(ILLUST / "V-S01-TAIL_壁报草稿空栏.png")

    body_html = prose_to_html(hybrid)

    # inject illustrations after section markers (rough placement per 13_)
    body_html = body_html.replace(
        '<h3 class="section">1</h3>',
        '<h3 class="section">1</h3>'
        + (f'<figure class="illus half"><img src="{v_s01}" alt="侧廊海报"/><figcaption>侧廊 · 海报翘边的那一边</figcaption></figure>' if v_s01 else ""),
        1,
    )
    body_html = body_html.replace(
        '<h3 class="section">4</h3>',
        '<h3 class="section">4</h3>'
        + (f'<figure class="illus quarter"><img src="{v_tail}" alt="壁报草稿空栏"/><figcaption>壁报草稿 · 留空的一栏</figcaption></figure>' if v_tail else ""),
        1,
    )

    placeholder_illus = "\n".join(
        f'<div class="placeholder-illus"><span>插图占位 · 全卷预告 {i}/9</span></div>'
        for i in range(1, 10)
    )

    child_q = """
    <ol class="questionnaire">
      <li>哪里最想继续读下去？<span class="blank"></span></li>
      <li>海报为什么翘边？你的猜想：<span class="blank short"></span><br/>
          读完后：□ 猜对了 □ 没想到 □ 一半对</li>
      <li>最喜欢谁？ □ 陸珣 □ 光 □ 慧美 □ 志郎 □ 瑆</li>
      <li>有没有 boring 的地方？<span class="blank"></span></li>
      <li>有没有 scary 或不懂的词？<span class="blank"></span></li>
      <li>如果有一整本书 5 个小故事，你想读吗？ □ 想 □ 一般 □ 不想</li>
      <li>若下一个是「橡皮屑谜题」，你想读吗？ □ 想 □ 不想</li>
    </ol>
    """

    parent_q = """
    <ol class="questionnaire">
      <li>内容是否安全？ □ 是 □ 有顾虑</li>
      <li>是否像教辅/推理培训？ □ 不像 □ 有点像 □ 像</li>
      <li>是否愿意购买类似童书？ □ 愿意 □ 看价格 □ 不愿意</li>
      <li>年龄 ___ 岁 · 自读/共读？<span class="blank short"></span></li>
      <li>「观察社」设定是否接受？ □ 接受 □ 需修改</li>
      <li>自由建议<span class="blank"></span></li>
    </ol>
    """

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>学堂趣事录 · Vol1 样章试读</title>
<style>
@page {{ size: A5; margin: 18mm 16mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif;
  font-size: 11.5pt; line-height: 1.55; color: #222; max-width: 148mm; margin: 0 auto;
}}
.page {{ page-break-after: always; min-height: 240mm; padding: 8mm 0; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; min-height: 240mm; background: #f7f4ef;
}}
.cover h1 {{ font-size: 22pt; margin: 0.5em 0; letter-spacing: 0.08em; }}
.cover h2 {{ font-size: 14pt; font-weight: normal; color: #444; }}
.cover .tag {{ margin-top: 2em; font-size: 9pt; color: #666; }}
.cover img {{ max-width: 70%; margin: 1.5em 0; border: 1px solid #ccc; }}
h1.book-title {{ font-size: 13pt; text-align: center; margin-bottom: 0.2em; }}
h2.chapter {{ font-size: 12pt; border-bottom: 1px solid #ccc; padding-bottom: 0.3em; margin-top: 1.2em; }}
h3.section {{ font-size: 10pt; color: #555; margin-top: 1em; }}
p {{ margin: 0.6em 0; text-indent: 2em; }}
p .indent {{ display: block; text-indent: 0; padding-left: 1.5em; font-family: inherit; }}
.notice {{ font-size: 9pt; color: #666; text-align: center; margin-top: 4em; }}
.chars {{ font-size: 10.5pt; }}
.chars table {{ width: 100%; border-collapse: collapse; font-size: 10pt; }}
.chars td, .chars th {{ border-bottom: 1px solid #eee; padding: 0.4em; vertical-align: top; }}
.toc {{ list-style: none; padding: 0; }}
.toc li {{ padding: 0.4em 0; border-bottom: 1px dotted #ccc; }}
.diary-page {{ background: linear-gradient(#fffef8, #fffef8), repeating-linear-gradient(#0000 0 1.4em, #e8e4dc 1.4em 1.41em); background-blend-mode: normal; padding: 1em; }}
.diary-page p {{ text-indent: 0; }}
.clue-card {{
  border: 2px solid #333; padding: 1em; border-radius: 4px;
}}
.clue-card h2 {{ text-align: center; margin-top: 0; }}
.clue-card ul {{ list-style: none; padding-left: 0; }}
.clue-card li::before {{ content: "□ "; }}
.illus {{ text-align: center; margin: 1em 0; page-break-inside: avoid; }}
.illus img {{ max-width: 100%; height: auto; }}
.illus.half img {{ max-height: 90mm; }}
.illus.quarter img {{ max-height: 55mm; }}
.illus figcaption {{ font-size: 9pt; color: #666; margin-top: 0.3em; }}
.placeholder-illus {{
  border: 2px dashed #bbb; height: 120mm; display: flex; align-items: center;
  justify-content: center; color: #999; font-size: 11pt; margin: 1em 0;
}}
.questionnaire {{ padding-left: 1.2em; }}
.questionnaire li {{ margin: 0.8em 0; }}
.blank {{ display: inline-block; min-width: 60%; border-bottom: 1px solid #999; height: 1.2em; }}
.blank.short {{ min-width: 30%; }}
.footer-note {{ font-size: 8pt; color: #888; text-align: center; margin-top: 2em; }}
@media print {{ body {{ max-width: none; }} .page {{ min-height: auto; }} }}
</style>
</head>
<body>

<div class="page cover">
  <p class="tag">试读版 · 非卖品 · {OUT_DATE}</p>
  <h1>学堂趣事录</h1>
  <h2>第1卷 · 觉得奇怪，就先观察</h2>
  {"<img src='" + v_s01 + "' alt='封面插图'/>" if v_s01 else "<p>【封面 · V-S01】</p>"}
  <p>样章：序 + 案①《翘边的海报》</p>
  <p class="tag">8–11 岁 · 校园趣事观察 · 非教辅</p>
</div>

<div class="page">
  <p class="notice">试读版 · 非卖品 · 仅供出版社提案 / 家庭试读 / 专家审稿<br/>
  反馈请联系项目组 · 内容未完成出版定稿</p>
</div>

<div class="page chars">
  <h2>角色介绍</h2>
  <pre style="white-space: pre-wrap; font-family: inherit; font-size: 10.5pt;">{chars_html.strip()}</pre>
</div>

<div class="page">
  <h2>试读目录</h2>
  <ul class="toc">
    <li>序 · 四月第二个星期一</li>
    <li>案① · 翘边的海报</li>
    <li>陸瑆的笔记</li>
    <li>观察社 · 线索卡 #01</li>
    <li>家庭小实验 · 风从哪边来</li>
    <li>试读问卷（儿童 / 家长）</li>
  </ul>
</div>

<div class="page prose">
  {body_html}
</div>

<div class="page diary-page">
  <h2>陸瑆的笔记 · 样章</h2>
  {diary_html}
  <p class="footer-note">陸瑆 · 4年2組 · 不在观察社，但会把哥哥的故事画进日记</p>
</div>

<div class="page">
  <div class="clue-card">
    <h2>观察社 · 线索卡 #01</h2>
    <p><strong>案：翘边的海报</strong></p>
    <p>今天奇怪的事：海报的边，每天翘在不同侧。</p>
    <p>你已经看见的线索：（可勾选）</p>
    <ul>
      <li>翘边和风来的方向在同一侧</li>
      <li>下雨的日子更容易翘</li>
      <li>贴海报的人，换过贴的方向</li>
    </ul>
    <p>你的猜想：<span class="blank"></span></p>
    <p style="text-align:center;margin-top:1.5em;">（答案在故事里 — 先自己想想！）</p>
    <p style="text-align:center;">观察社还留了一格空白 —— 下一周，谁会把它填满？</p>
    <p style="text-align:center;font-size:9pt;">—— 学校おもしろ観察クラブ ——</p>
  </div>
</div>

<div class="page">
  <h2>家庭小实验</h2>
  {exp_html}
</div>

<div class="page">
  <h2>插图占位 · 全卷预告</h2>
  {placeholder_illus}
</div>

<div class="page">
  <h2>儿童问卷（8–10 岁）</h2>
  {child_q}
</div>

<div class="page">
  <h2>家长问卷</h2>
  {parent_q}
  <p class="footer-note">问卷模板来源：10_试读协议与反馈表.md · E20 试读</p>
</div>

</body>
</html>
"""


def html_to_pdf_chrome(html_path: Path, pdf_path: Path) -> bool:
    for chrome in CHROME_CANDIDATES:
        if not chrome.exists():
            continue
        url = html_path.resolve().as_uri()
        cmd = [
            str(chrome),
            "--headless=new",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path.resolve()}",
            "--no-pdf-header-footer",
            url,
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=90)
            return pdf_path.exists() and pdf_path.stat().st_size > 1000
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def html_to_pdf_fpdf(html_path: Path, pdf_path: Path) -> bool:
    try:
        from fpdf import FPDF
    except ImportError:
        return False

    font_path = next((p for p in FONT_CANDIDATES if p.exists()), None)
    if not font_path:
        return False

    hybrid = strip_hybridvoice_body(read_text(ROOT / "04_样章_序+案01_正文_HybridVoice.txt"))
    diary = read_text(ROOT / "05_陸瑆日记页_样章.txt").split("---")[0].strip()
    experiment = read_text(ROOT / "12_案01_家庭实验页_样章.txt")

    pdf = FPDF(format="A5", unit="mm")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("cn", "", str(font_path))
    pdf.add_font("cn", "B", str(font_path))

    def add_page_title(title: str) -> None:
        pdf.add_page()
        pdf.set_font("cn", "B", 14)
        pdf.multi_cell(0, 8, title, align="C")
        pdf.ln(4)

    def add_body(text: str, size: int = 11) -> None:
        pdf.set_font("cn", "", size)
        w = pdf.epw
        for para in text.split("\n\n"):
            para = para.strip()
            if not para:
                continue
            if para.startswith("=") or para.startswith("-"):
                continue
            pdf.multi_cell(w, 6, para)
            pdf.ln(2)

    # cover
    pdf.add_page()
    pdf.set_font("cn", "B", 18)
    pdf.ln(40)
    pdf.multi_cell(0, 10, "学堂趣事录", align="C")
    pdf.set_font("cn", "", 12)
    pdf.multi_cell(0, 8, "第1卷 · 觉得奇怪，就先观察", align="C")
    pdf.ln(10)
    pdf.set_font("cn", "", 9)
    pdf.multi_cell(0, 6, f"试读版 · 非卖品 · {OUT_DATE}", align="C")

    add_page_title("试读声明")
    pdf.set_font("cn", "", 10)
    pdf.multi_cell(0, 6, "试读版 · 非卖品 · 仅供出版社提案 / 家庭试读 / 专家审稿。")

    add_page_title("正文 · 序 + 案①")
    add_body(hybrid)

    add_page_title("陸瑆的笔记")
    add_body(diary)

    add_page_title("家庭小实验")
    add_body(experiment)

    v_s01 = ILLUST / "V-S01_侧廊海报.png"
    if v_s01.exists():
        pdf.add_page()
        pdf.set_font("cn", "B", 12)
        pdf.cell(0, 8, "插图 · 侧廊海报", ln=True, align="C")
        pdf.image(str(v_s01), x=15, w=120)

    pdf.output(str(pdf_path))
    return pdf_path.exists() and pdf_path.stat().st_size > 1000


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    html_path = PDF_DIR / HTML_NAME
    pdf_path = PDF_DIR / PDF_NAME

    html = build_html()
    html_path.write_text(html, encoding="utf-8")
    print(f"Wrote HTML: {html_path}")

    ok = html_to_pdf_chrome(html_path, pdf_path)
    method = "chrome"
    if not ok:
        ok = html_to_pdf_fpdf(html_path, pdf_path)
        method = "fpdf2"
    if not ok:
        print("PDF auto-export failed. Open HTML in browser → Print → Save as PDF.", file=sys.stderr)
        print(f"  {html_path}")
        return 1

    print(f"Wrote PDF ({method}): {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
