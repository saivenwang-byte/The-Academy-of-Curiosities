#!/usr/bin/env python3
"""Vol1 thin kid trial PDF — Japanese only · 序+案①+瑆+实验+问卷 (~20–30p).

Outputs:
  薄样张_试读/PDF/学堂奇事録_Vol1_薄样张_日本語_{date}.pdf
  薄样张_试读/PDF/学堂奇事録_Vol1_薄样张_日本語_{date}.html
"""

from __future__ import annotations

import base64
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
SAMPLE = TRIAL.parent / "样章包"
ILLUST = SAMPLE / "插图"
PDF_DIR = TRIAL / "PDF"
OUT_DATE = date.today().strftime("%Y%m%d")
PDF_NAME = f"学堂奇事録_Vol1_薄样张_日本語_{OUT_DATE}.pdf"
HTML_NAME = f"学堂奇事録_Vol1_薄样张_日本語_{OUT_DATE}.html"

JP_FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
]

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

EXPERIMENT_JP = """
## 風はどこから来ると、角はどこからめくれる？

**用意するもの**：厚紙1枚 · 布テープ · ドライヤー（**保護者と一緒**）

1. テープで紙の**一辺**を壁や扉に貼る。  
2. ドライヤーを**上から**10秒吹く。どの辺が先にめくれる？  
3. **左／右／上**に貼り直して、もう一度。めくれる辺は変わる？  
4. 浴室の前など、湿った場所でも試す（**滑らないように**）。

**考えてみよう**  
· 観察クラブのポスターと、どこが似ている？  
· いたずら？ それとも **風＋貼り方**？

※ 実験は**任意**。大人が電源を管理してください。
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_jp_prologue(raw: str) -> str:
    lines = raw.splitlines()
    body: list[str] = []
    started = False
    for line in lines:
        if not started:
            if line.startswith("序 ·") or line.startswith("序·"):
                started = True
                body.append(line)
            continue
        if line.strip().startswith("【") and "試読" in line:
            continue
        body.append(line)
    return "\n".join(body).strip()


def extract_kei_diary(notes_md: Path) -> str:
    raw = read_text(notes_md)
    m = re.search(
        r"## 事件① · .*?\n\n(.*?)\n\n---",
        raw,
        re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    return ""


def prose_to_html(text: str) -> str:
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
        if s.startswith("『学堂") or s.startswith("第1巻"):
            blocks.append(f'<h1 class="book-title">{s}</h1>')
            continue
        if re.match(r"^序 ·", s) or re.match(r"^一、", s):
            blocks.append(f'<h2 class="chapter">{s}</h2>')
            continue
        if re.match(r"^### \d", s):
            blocks.append(f'<h3 class="section">{s.replace("### ", "")}</h3>')
            continue
        if s.startswith("  "):
            para.append(f'<span class="indent">{s.strip()}</span>')
        else:
            para.append(s)
    if para:
        blocks.append("<p>" + "<br/>".join(para) + "</p>")
    return "\n".join(blocks)


def md_simple_to_html(md: str) -> str:
    html = md.strip()
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"^(\d+\. .+)$", r"<p>\1</p>", html, flags=re.MULTILINE)
    html = re.sub(r"^· (.+)$", r"<p>· \1</p>", html, flags=re.MULTILINE)
    html = re.sub(r"^※ (.+)$", r"<p class='note'>\1</p>", html, flags=re.MULTILINE)
    return html


def img_data_uri(path: Path) -> str:
    if not path.exists():
        return ""
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_html() -> str:
    jp_path = SAMPLE / "04_样章_序+案01_正文_日本語.txt"
    notes_path = TRIAL.parent / "正式版" / "03_笔记" / "陸瑆笔记_Vol1_日本語.md"
    body_raw = strip_jp_prologue(read_text(jp_path))
    body_html = prose_to_html(body_raw)
    diary_raw = extract_kei_diary(notes_path) if notes_path.exists() else ""
    diary_html = prose_to_html(diary_raw) if diary_raw else "<p>（瑆ノート · 試読ページ）</p>"

    imgs = {
        "s01": img_data_uri(ILLUST / "V-S01_侧廊海报.png"),
        "tail": img_data_uri(ILLUST / "V-S01-TAIL_壁报草稿空栏.png"),
        "s02": img_data_uri(ILLUST / "V-S02_陸瑆日记页.png"),
        "s03": img_data_uri(ILLUST / "V-S03_风侧示意图.png"),
    }

    if imgs["s01"]:
        body_html = body_html.replace(
            '<h3 class="section">1</h3>',
            '<h3 class="section">1</h3>'
            f'<figure class="illus half"><img src="{imgs["s01"]}" alt="側廊ポスター"/>'
            "<figcaption>側廊 · めくれた端</figcaption></figure>",
            1,
        )
    if imgs["tail"]:
        body_html = body_html.replace(
            '<h3 class="section">4</h3>',
            '<h3 class="section">4</h3>'
            f'<figure class="illus quarter"><img src="{imgs["tail"]}" alt="壁報空欄"/>'
            "<figcaption>壁報草稿 · 空いた欄</figcaption></figure>",
            1,
        )

    kei_fig = ""
    if imgs["s02"]:
        kei_fig = (
            f'<figure class="illus half"><img src="{imgs["s02"]}" alt="瑆の日記"/>'
            "<figcaption>陸瑆（4年2組）のノート</figcaption></figure>"
        )
    wind_fig = ""
    if imgs["s03"]:
        wind_fig = (
            f'<figure class="illus half"><img src="{imgs["s03"]}" alt="風の示意"/>'
            "<figcaption>風とめくれる辺</figcaption></figure>"
        )

    child_q = """
    <ol class="questionnaire">
      <li>どこがいちばん続きが読みたくなった？<span class="blank"></span></li>
      <li>ポスターはなぜめくれた？ 予想：<span class="blank short"></span><br/>
          □ 当たった □ 意外 □ 半分当たった</li>
      <li>いちばん好きな人？ □ 陸珣 □ 光 □ 慧美 □ 志郎 □ 瑆</li>
      <li>つまらないところ？<span class="blank"></span></li>
      <li>こわい／わからない言葉？<span class="blank"></span></li>
      <li>5つの事件の本があったら読みたい？ □ 読みたい □ 普通 □ いいえ</li>
    </ol>
    """

    parent_q = """
    <ol class="questionnaire">
      <li>内容は安全？ □ はい □ 心配</li>
      <li>参考書・推理教室っぽい？ □ 似ていない □ 少し □ 似ている</li>
      <li>買いたい？ □ 買いたい □ 価格次第 □ いいえ</li>
      <li>年齢 ___ 歳 · 自読／読み聞かせ<span class="blank short"></span></li>
      <li>観察クラブ設定 □ OK □ 修正要</li>
      <li>自由記述<span class="blank"></span></li>
    </ol>
    """

    cover_img = imgs["s01"] or ""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8"/>
<title>学堂奇事録 · Vol1 薄样张</title>
<style>
@page {{ size: A5; margin: 16mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: "Yu Gothic", "Meiryo", "Hiragino Sans", sans-serif;
  font-size: 11pt; line-height: 1.65; color: #222; max-width: 148mm; margin: 0 auto;
}}
.page {{ page-break-after: always; min-height: 230mm; padding: 6mm 0; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; min-height: 230mm; background: #f7f4ef;
}}
.cover h1 {{ font-size: 20pt; margin: 0.4em 0; }}
.cover h2 {{ font-size: 13pt; font-weight: normal; color: #444; }}
.cover .tag {{ font-size: 9pt; color: #666; margin-top: 1.5em; }}
.cover img {{ max-width: 75%; margin: 1em 0; border: 1px solid #ccc; }}
h1.book-title {{ font-size: 12pt; text-align: center; }}
h2.chapter {{ font-size: 11.5pt; border-bottom: 1px solid #ccc; padding-bottom: 0.25em; margin-top: 1em; }}
h3.section {{ font-size: 10pt; color: #555; }}
p {{ margin: 0.55em 0; text-indent: 1em; }}
p .indent {{ display: block; text-indent: 0; padding-left: 1.2em; }}
.notice {{ font-size: 8.5pt; color: #666; text-align: center; }}
.diary-page {{ background: #fffef8; padding: 0.8em; border-left: 3px solid #f0c8b0; }}
.diary-page p {{ text-indent: 0; }}
.clue-card {{ border: 2px solid #333; padding: 0.8em; border-radius: 3px; }}
.clue-card ul {{ list-style: none; padding-left: 0; }}
.clue-card li::before {{ content: "□ "; }}
.illus {{ text-align: center; margin: 0.8em 0; page-break-inside: avoid; }}
.illus img {{ max-width: 100%; height: auto; }}
.illus.half img {{ max-height: 85mm; }}
.illus.quarter img {{ max-height: 50mm; }}
.illus figcaption {{ font-size: 8.5pt; color: #666; }}
.questionnaire {{ padding-left: 1em; font-size: 10pt; }}
.questionnaire li {{ margin: 0.7em 0; }}
.blank {{ display: inline-block; min-width: 55%; border-bottom: 1px solid #999; height: 1.1em; }}
.blank.short {{ min-width: 28%; }}
.footer-note {{ font-size: 8pt; color: #888; text-align: center; margin-top: 1.5em; }}
.toc {{ list-style: none; padding: 0; }}
.toc li {{ padding: 0.35em 0; border-bottom: 1px dotted #ccc; font-size: 10.5pt; }}
.note {{ font-size: 9pt; color: #666; }}
@media print {{ body {{ max-width: none; }} .page {{ min-height: auto; }} }}
</style>
</head>
<body>

<div class="page cover">
  <p class="tag">試読版 · 非売品 · {OUT_DATE}</p>
  <h1>学堂奇事録</h1>
  <h2>第1巻 · おかしいと思ったら、まず見てみる</h2>
  {"<img src='" + cover_img + "' alt='表紙'/>" if cover_img else "<p>【表紙 · V-S01】</p>"}
  <p>試読：序 + 事件①「めくれたポスター」</p>
  <p class="tag">8–11歳 · 名古屋 · 観察 · 非参考書</p>
</div>

<div class="page">
  <p class="notice">試読版 · 非売品 · 家庭／教室試読専用<br/>
  フィードバックは改稿のみ · 未完成稿</p>
  <h2>目次</h2>
  <ul class="toc">
    <li>序 · 四月の第二月曜日</li>
    <li>事件① · めくれたポスター</li>
    <li>陸瑆（ひかる）のノート</li>
    <li>観察クラブ · 线索カード #01</li>
    <li>おうち実験（任意）</li>
    <li>アンケート</li>
  </ul>
</div>

<div class="page prose">
  {body_html}
</div>

<div class="page diary-page">
  <h2>陸瑆のノート · 試読</h2>
  {kei_fig}
  {diary_html}
  <p class="footer-note">陸瑆 · 4年2組 · 観察クラブには入っていない</p>
</div>

<div class="page">
  <div class="clue-card">
    <h2 style="text-align:center;margin-top:0;">観察クラブ · 线索カード #01</h2>
    <p><strong>事件：めくれたポスター</strong></p>
    <p>今日の「おかしい」：ポスターの端が、毎日違う側でめくれる。</p>
    <ul>
      <li>めくれた辺と、風の来る方向が同じ側</li>
      <li>雨の日はめくれやすい</li>
      <li>貼る人が、貼る向きを変えた</li>
    </ul>
    <p>あなたの予想：<span class="blank"></span></p>
    <p style="text-align:center;">—— 学校おもしろ観察クラブ ——</p>
  </div>
</div>

<div class="page">
  <h2>おうち実験（任意）</h2>
  {wind_fig}
  {md_simple_to_html(EXPERIMENT_JP)}
</div>

<div class="page">
  <h2>児童用アンケート</h2>
  {child_q}
</div>

<div class="page">
  <h2>保護者用アンケート</h2>
  {parent_q}
  <p class="footer-note">03_问卷_儿童家长_日本語_V1.0.md · E20</p>
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
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            return pdf_path.exists() and pdf_path.stat().st_size > 1000
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def main() -> int:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    html_path = PDF_DIR / HTML_NAME
    pdf_path = PDF_DIR / PDF_NAME
    html_path.write_text(build_html(), encoding="utf-8")
    print(f"HTML: {html_path}")
    if html_to_pdf_chrome(html_path, pdf_path):
        print(f"PDF:  {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
        return 0
    print("PDF: Chrome/Edge headless not available — HTML only", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
