#!/usr/bin/env python3
"""Assemble Vol1 formal display edition → HTML + PDF (A5).

Reads:
  01_正本/ 中文 .md + 日本語 .txt (assembled)
  03_笔记/ 中文 + 日本語
  02_插画/assets/*.png

Outputs:
  04_展示版/学堂奇事録_Vol1_展示版_日本語_{date}.pdf  (default)
  04_展示版/学堂趣事录_Vol1_展示版_中文_{date}.pdf      (--pdf-lang zh)
"""

from __future__ import annotations

import argparse
import base64
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # 正式版/
CANON_ZH = ROOT / "01_正本" / "学堂趣事录_Vol1_觉得奇怪就先观察_正本.md"
CANON_JP = ROOT / "01_正本" / "学堂趣事录_Vol1_觉得奇怪就先观察_正本_日本語.txt"
SAMPLE_A001 = ROOT.parent / "样章包" / "04_样章_序+案01_正文_日本語.txt"
CH_A002_005 = ROOT / "01_正本" / "Vol1_正本_日本語_A002-A005.txt"
NOTES_ZH = ROOT / "03_笔记" / "陆瑆笔记_Vol1.md"
NOTES_JP = ROOT / "03_笔记" / "陸瑆笔记_Vol1_日本語.md"
ILLUST = ROOT / "02_插画" / "assets"
OUT_DIR = ROOT / "04_展示版"
ASSEMBLE_JP = Path(__file__).resolve().parent / "assemble_jp_canon.py"
CHARS_ZH = ROOT.parent / "样章包" / "08_角色介绍_一页.md"

OUT_DATE = date.today().strftime("%Y%m%d")

FONT_ZH = [
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttf"),
    Path(r"C:\Windows\Fonts\simsun.ttc"),
]
FONT_JP = [
    Path(r"C:\Windows\Fonts\YuGothM.ttc"),
    Path(r"C:\Windows\Fonts\YuGothR.ttc"),
    Path(r"C:\Windows\Fonts\meiryo.ttc"),
    Path(r"C:\Windows\Fonts\msgothic.ttc"),
]

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

# (chapter_key, section_num|None, filename, css)
# chapter_key matched against current h2; section_num matched against ### N
ILLUST_RULES: list[tuple[str, str | None, str, str]] = [
    ("翘边的海报", None, "V-S01_侧廊海报.png", "half"),
    ("めくれたポスター", None, "V-S01_侧廊海报.png", "half"),
    ("翘边的海报", "4", "V-S01-TAIL_壁报草稿空栏.png", "quarter"),
    ("めくれたポスター", "4", "V-S01-TAIL_壁报草稿空栏.png", "quarter"),
    ("错位的泥印", None, "V-S02_陸瑆日记页.png", "quarter"),
    ("ズレた泥", None, "V-S02_陸瑆日记页.png", "quarter"),
    ("错位的泥印", "6", "V-S02-TAIL_无署名窄条.png", "quarter"),
    ("ズレた泥", "6", "V-S02-TAIL_无署名窄条.png", "quarter"),
    ("空着的那一栏", "6", "V-S03-TAIL_投稿背面路线.png", "quarter"),
    ("空いている欄", "6", "V-S03-TAIL_投稿背面路线.png", "quarter"),
    ("粉笔灰的圆圈", None, "V-S04_讲台粉笔灰圈.png", "half"),
    ("チョークの粉", None, "V-S04_讲台粉笔灰圈.png", "half"),
    ("粉笔灰的圆圈", "5", "V-S04-TAIL_中谷远景.png", "quarter"),
    ("チョークの粉", "5", "V-S04-TAIL_中谷远景.png", "quarter"),
    ("橡皮屑的方向", None, "V-S05_橡皮屑方向.png", "half"),
    ("消しゴムのカス", None, "V-S05_橡皮屑方向.png", "half"),
    ("橡皮屑的方向", "4", "V-S05-TAIL_瑆日记扶正书.png", "quarter"),
    ("消しゴムのカス", "4", "V-S05-TAIL_瑆日记扶正书.png", "quarter"),
]

ILLUST_CAPTIONS: dict[str, dict[str, str]] = {
    "V-S01_侧廊海报.png": {"zh": "侧廊 · 海报翘边", "ja": "側廊 · めくれたポスター"},
    "V-S01-TAIL_壁报草稿空栏.png": {"zh": "壁报草稿 · 留空的一栏", "ja": "壁報下書き · 空欄"},
    "V-S02_陸瑆日记页.png": {"zh": "陸瑆日记 · 风与海报", "ja": "瑆のノート · 風とポスター"},
    "V-S02-TAIL_无署名窄条.png": {"zh": "空栏内的无署名投稿", "ja": "空欄の無署名投稿"},
    "V-S03-TAIL_投稿背面路线.png": {"zh": "投稿背面 · 擦痕路线", "ja": "投稿の裏 · 消し跡のルート"},
    "V-S04_讲台粉笔灰圈.png": {"zh": "讲台 · 粉笔灰圈与对照", "ja": "教壇 · 粉の輪と対照"},
    "V-S04-TAIL_中谷远景.png": {"zh": "侧廊 · 中谷远景半句", "ja": "側廊 · 中谷の半句"},
    "V-S05_橡皮屑方向.png": {"zh": "美术室门 · 橡皮屑方向", "ja": "美術室 · カスの向き"},
    "V-S05-TAIL_瑆日记扶正书.png": {"zh": "瑆日记 · 扶正书角误画", "ja": "瑆 · 本の角を直す誤描"},
}

META = {
    "zh": {
        "html_lang": "zh-CN",
        "title": "学堂趣事录 · Vol1 展示版（中文）",
        "cover_edition": "正式展示版 · 中文",
        "book": "学堂趣事录",
        "vol": "第1卷 · 觉得奇怪，就先观察",
        "subtitle": "序 + 案①–⑤ · 8–11 岁 · 校园趣事观察",
        "toc_title": "目录",
        "toc": [
            "序 · 四月第二个星期一",
            "案① · 翘边的海报",
            "案② · 错位的泥印",
            "案③ · 空着的那一栏",
            "案④ · 粉笔灰的圆圈",
            "案⑤ · 橡皮屑的方向",
            "陸瑆的笔记",
            "家庭小实验 · Vol1 汇总",
        ],
        "colophon_chapters": "A001–A005 · Plan B · 5年2組陸珣视角",
        "chars_title": "角色介绍",
        "notes_title": "陸瑆的笔记",
        "notes_footer": "陸瑆 · 4年2組 · 不在观察社，但会把哥哥的故事画进日记",
        "illus_title": "插图 · 全卷一览",
        "illus_note": "V-S01–V-S05 系列已嵌入正文。辅助图 V-S03 见 assets。",
        "placeholder": "插图占位",
        "footer": "《学堂趣事录》Vol1 正式展示版（中文）· 非最终印厂文件",
        "pdf_name": f"学堂趣事录_Vol1_展示版_中文_{OUT_DATE}.pdf",
        "html_name": f"学堂趣事录_Vol1_展示版_中文_{OUT_DATE}.html",
        "font_stack": '"Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif',
    },
    "ja": {
        "html_lang": "ja",
        "title": "学堂奇事録 · Vol1 展示版（日本語）",
        "cover_edition": "正式展示版 · 日本語",
        "book": "学堂奇事録",
        "vol": "第1巻 · おかしいと思ったら、まず見てみる",
        "subtitle": "序 · 事件①–⑤ · 8–11歳 · 校园おもしろ観察",
        "toc_title": "目次",
        "toc": [
            "序 · 四月の第二月曜日",
            "事件① · めくれたポスター",
            "事件② · ズレた泥のあと",
            "事件③ · 空いている欄",
            "事件④ · チョークの粉の輪",
            "事件⑤ · 消しゴムのカス",
            "陸瑆（ひかる）のノート",
            "家庭実験 · Vol1 まとめ",
        ],
        "colophon_chapters": "A001–A005 · Plan B · 5年2組 陸珣（しゅん）視点",
        "chars_title": "登場人物",
        "notes_title": "陸瑆（ひかる）のノート",
        "notes_footer": "陸瑆 · 4年2組 · 観察クラブには入っていないが、兄の話を日記に描く",
        "illus_title": "挿画 · 全巻一覧",
        "illus_note": "V-S01–V-S05 を本文に嵌入済み。",
        "placeholder": "挿画プレースホルダ",
        "footer": "『学堂奇事録』Vol1 正式展示版（日本語）· 非印厂原稿",
        "pdf_name": f"学堂奇事録_Vol1_展示版_日本語_{OUT_DATE}.pdf",
        "html_name": f"学堂奇事録_Vol1_展示版_日本語_{OUT_DATE}.html",
        "font_stack": '"Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans JP", sans-serif',
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_jp_canon() -> None:
    newer = (
        CANON_JP.exists()
        and SAMPLE_A001.exists()
        and CH_A002_005.exists()
        and CANON_JP.stat().st_mtime
        >= max(SAMPLE_A001.stat().st_mtime, CH_A002_005.stat().st_mtime, ASSEMBLE_JP.stat().st_mtime)
    )
    if newer:
        return
    subprocess.run([sys.executable, str(ASSEMBLE_JP)], check=True)


def strip_md_meta(raw: str) -> str:
    lines: list[str] = []
    for line in raw.splitlines():
        if line.strip().startswith("> **正本状态**"):
            continue
        if line.strip().startswith("> **状态**：FORMAL_DRAFT"):
            continue
        if re.match(r"^> \*\*", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def strip_txt_meta(raw: str) -> str:
    lines: list[str] = []
    for line in raw.splitlines():
        if line.strip().startswith("【正式版") or line.strip().startswith("【試読"):
            continue
        if re.match(r"^  · ", line):
            continue
        if line.strip().startswith("=") and len(line.strip()) > 10:
            continue
        if line.strip() == "『学堂奇事録』（学堂趣事録）":
            continue
        if line.strip().startswith("第1巻 ·"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def inject_illust(chapter: str, section: str | None, lang: str) -> str:
    sec_num = None
    if section and section[0].isdigit():
        sec_num = section.split()[0]
    for key, rule_sec, fname, css in ILLUST_RULES:
        if key not in chapter:
            continue
        if rule_sec is None and section is not None:
            continue
        if rule_sec is not None and sec_num != rule_sec:
            continue
        cap = ILLUST_CAPTIONS.get(fname, {}).get(lang, fname)
        return illust_figure(fname, cap, css, META[lang]["placeholder"])
    return ""


def md_prose_to_html(text: str, lang: str) -> str:
    blocks: list[str] = []
    para: list[str] = []
    current_chapter = ""

    for line in text.splitlines():
        s = line.rstrip()
        if not s:
            if para:
                blocks.append("<p>" + "<br/>".join(para) + "</p>")
                para = []
            continue
        if s == "---":
            blocks.append('<hr class="scene-break"/>')
            continue
        if s.startswith("# "):
            blocks.append(f'<h1 class="book-title">{s[2:]}</h1>')
            continue
        if s.startswith("## "):
            current_chapter = s[3:]
            blocks.append(f'<h2 class="chapter">{current_chapter}</h2>')
            fig = inject_illust(current_chapter, None, lang)
            if fig:
                blocks.append(fig)
            continue
        if re.match(r"^(序|一、|二、|三、|四、|五、|巻末)", s) and not s.startswith("---"):
            current_chapter = s.split("-")[0].strip()
            blocks.append(f'<h2 class="chapter">{current_chapter}</h2>')
            fig = inject_illust(current_chapter, None, lang)
            if fig:
                blocks.append(fig)
            continue
        if s.startswith("### "):
            sec = s[4:]
            blocks.append(f'<h3 class="section">{sec}</h3>')
            fig = inject_illust(current_chapter, sec, lang)
            if fig:
                blocks.append(fig)
            continue
        if s.startswith("> "):
            continue
        if s.startswith("  ") and not s.startswith("  http"):
            para.append(f'<span class="indent">{s.strip()}</span>')
        elif s.startswith("*") and s.endswith("*") and not s.startswith("**"):
            blocks.append(f'<p class="caption">{s.strip("*")}</p>')
        elif re.match(r"^-{4,}$", s):
            continue
        else:
            clean = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
            if clean.strip():
                para.append(clean)
    if para:
        blocks.append("<p>" + "<br/>".join(para) + "</p>")
    return "\n".join(blocks)


def illust_figure(fname: str, caption: str, css: str, placeholder: str) -> str:
    path = ILLUST / fname
    if path.exists():
        uri = img_data_uri(path)
        return (
            f'<figure class="illus {css}"><img src="{uri}" alt="{caption}"/>'
            f'<figcaption>{caption}</figcaption></figure>'
        )
    return f'<div class="placeholder-illus"><span>{placeholder} · {fname}</span></div>'


def img_data_uri(path: Path) -> str:
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def notes_to_html(raw: str, lang: str) -> str:
    parts = re.split(r"\n---\n", raw)
    html_parts: list[str] = []
    skip_kw = "排版说明" if lang == "zh" else "排版"
    for part in parts:
        part = part.strip()
        if not part or part.startswith("# 陸") or skip_kw in part:
            continue
        if part.startswith("## "):
            lines = part.splitlines()
            title = lines[0][3:]
            body = "\n".join(lines[1:]).strip()
            html_parts.append(f'<h3 class="diary-chapter">{title}</h3>')
            html_parts.append(md_prose_to_html(body, lang))
    return "\n".join(html_parts)


def illust_gallery_html(lang: str) -> str:
    parts: list[str] = []
    seen: set[str] = set()
    for _key, _sec, fname, css in ILLUST_RULES:
        if fname in seen:
            continue
        seen.add(fname)
        cap = ILLUST_CAPTIONS.get(fname, {}).get(lang, fname)
        parts.append(illust_figure(fname, cap, css, META[lang]["placeholder"]))
    aux = ILLUST / "V-S03_风侧示意图.png"
    if aux.exists():
        cap = "风侧示意图" if lang == "zh" else "風の側（補助）"
        parts.append(illust_figure(aux.name, cap, "quarter", META[lang]["placeholder"]))
    return "\n".join(parts)


def build_html(lang: str) -> str:
    m = META[lang]
    if lang == "ja":
        ensure_jp_canon()
        canon_raw = strip_txt_meta(read_text(CANON_JP))
        notes_raw = read_text(NOTES_JP)
    else:
        canon_raw = strip_md_meta(read_text(CANON_ZH))
        notes_raw = read_text(NOTES_ZH)

    body_html = md_prose_to_html(canon_raw, lang)
    notes_html = notes_to_html(notes_raw, lang)

    v_s01 = (
        img_data_uri(ILLUST / "V-S01_侧廊海报.png")
        if (ILLUST / "V-S01_侧廊海报.png").exists()
        else ""
    )

    chars_text = ""
    if lang == "zh" and CHARS_ZH.exists():
        chars_text = read_text(CHARS_ZH)
        chars_text = re.sub(r"^# .+\n", "", chars_text, count=1)
        chars_text = re.sub(r"^> .+\n", "", chars_text, flags=re.MULTILINE)
        chars_text = re.sub(r"^---\n", "", chars_text, flags=re.MULTILINE)
    elif lang == "ja":
        chars_text = (
            "陸珣（りく しゅん）· 5年2組 · 転校生 · 観察は先にノートへ\n"
            "伊藤光（いとう ひかる）· 5年2組 · 学校おもしろ観察クラブ\n"
            "加藤慧美（けいみ）· 5年1組 · 記録・取材\n"
            "松本志郎（しろう）· 5年3組 · 検証・大声\n"
            "陸瑆（ひかる）· 4年2組 · 兄の話を日記に描く\n"
            "中谷琦 · 6年1組 · 半句だけ落とす先輩"
        )

    toc = "\n".join(f"<li>{item}</li>" for item in m["toc"])
    missing_illus = illust_gallery_html(lang)

    return f"""<!DOCTYPE html>
<html lang="{m["html_lang"]}">
<head>
<meta charset="utf-8"/>
<title>{m["title"]}</title>
<style>
@page {{ size: A5; margin: 16mm 14mm; }}
* {{ box-sizing: border-box; }}
body {{
  font-family: {m["font_stack"]};
  font-size: 11pt; line-height: 1.62; color: #1a1a1a; max-width: 148mm; margin: 0 auto;
}}
.page {{ page-break-after: always; min-height: 230mm; padding: 6mm 0; }}
.page:last-child {{ page-break-after: auto; }}
.cover {{
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; min-height: 230mm; background: linear-gradient(180deg, #f7f4ef 0%, #efeae2 100%);
}}
.cover h1 {{ font-size: 21pt; margin: 0.4em 0; letter-spacing: 0.08em; }}
.cover h2 {{ font-size: 13pt; font-weight: normal; color: #444; }}
.cover .edition {{ margin-top: 1.5em; font-size: 9pt; color: #666; }}
.cover img {{ max-width: 72%; margin: 1.2em 0; border: 1px solid #ccc; }}
h1.book-title {{ font-size: 12pt; text-align: center; }}
h2.chapter {{ font-size: 12pt; border-bottom: 1px solid #bbb; padding-bottom: 0.25em; margin-top: 1.1em; page-break-after: avoid; }}
h3.section {{ font-size: 10pt; color: #555; margin-top: 0.9em; page-break-after: avoid; }}
p {{ margin: 0.55em 0; text-indent: 0; }}
p.caption {{ text-indent: 0; text-align: center; font-size: 9pt; color: #666; }}
p .indent {{ display: block; padding-left: 1.5em; }}
hr.scene-break {{ border: none; border-top: 1px dotted #ccc; margin: 1.2em 0; }}
.toc {{ list-style: none; padding: 0; }}
.toc li {{ padding: 0.35em 0; border-bottom: 1px dotted #ccc; }}
.illus {{ text-align: center; margin: 0.8em 0; page-break-inside: avoid; }}
.illus img {{ max-width: 100%; height: auto; }}
.illus.half img {{ max-height: 85mm; }}
.illus.quarter img {{ max-height: 52mm; }}
.illus figcaption {{ font-size: 8.5pt; color: #666; margin-top: 0.25em; }}
.placeholder-illus {{
  border: 2px dashed #bbb; min-height: 45mm; display: flex; align-items: center;
  justify-content: center; color: #999; font-size: 10pt; margin: 0.8em 0;
}}
.placeholder-illus.small {{ min-height: 28mm; }}
.diary-page {{
  background: #fffef8; padding: 1em 1.2em; border-left: 3px solid #d4c4a8;
  background-image: repeating-linear-gradient(#0000 0 1.35em, #e8e4dc 1.35em 1.36em);
}}
.diary-page h2 {{ border: none; font-size: 11pt; color: #5a4a3a; }}
.diary-page h3.diary-chapter {{ font-size: 10pt; color: #6a5a4a; margin-top: 1em; }}
.diary-page p {{ text-indent: 0; }}
.chars pre {{ white-space: pre-wrap; font-family: inherit; font-size: 10pt; }}
.footer-note {{ font-size: 8pt; color: #888; text-align: center; margin-top: 1.5em; }}
.colophon {{ font-size: 8.5pt; color: #666; text-align: center; margin-top: 3em; }}
@media print {{ body {{ max-width: none; }} .page {{ min-height: auto; }} }}
</style>
</head>
<body>

<div class="page cover">
  <p class="edition">{m["cover_edition"]} · {OUT_DATE}</p>
  <h1>{m["book"]}</h1>
  <h2>{m["vol"]}</h2>
  {"<img src='" + v_s01 + "' alt='cover'/>" if v_s01 else "<p>【V-S01】</p>"}
  <p class="edition">{m["subtitle"]}</p>
</div>

<div class="page">
  <h2>{m["toc_title"]}</h2>
  <ul class="toc">{toc}</ul>
  <p class="colophon">{m["colophon_chapters"]}</p>
</div>

<div class="page chars">
  <h2>{m["chars_title"]}</h2>
  <pre style="white-space: pre-wrap; font-family: inherit;">{chars_text.strip()}</pre>
</div>

<div class="page prose">
  {body_html}
</div>

<div class="page diary-page">
  <h2>{m["notes_title"]}</h2>
  {notes_html}
  <p class="footer-note">{m["notes_footer"]}</p>
</div>

<div class="page">
  <h2>{m["illus_title"]}</h2>
  <p style="font-size:9.5pt;color:#666;">{m["illus_note"]}</p>
  {missing_illus}
</div>

<div class="page">
  <p class="colophon">
    {m["footer"]}<br/>
    python 04_展示版/tools/build_display_edition.py --pdf-lang {lang}
  </p>
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
            subprocess.run(cmd, check=True, capture_output=True, timeout=180)
            return pdf_path.exists() and pdf_path.stat().st_size > 1000
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def build_one(lang: str) -> int:
    m = META[lang]
    canon = CANON_JP if lang == "ja" else CANON_ZH
    if lang == "ja":
        ensure_jp_canon()
    if not canon.exists():
        print(f"Missing canon ({lang}): {canon}", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUT_DIR / m["html_name"]
    pdf_path = OUT_DIR / m["pdf_name"]

    html = build_html(lang)
    html_path.write_text(html, encoding="utf-8")
    print(f"[{lang}] HTML: {html_path}")

    ok = html_to_pdf_chrome(html_path, pdf_path)
    if not ok:
        print(f"[{lang}] PDF failed — open HTML and Print to PDF", file=sys.stderr)
        return 1

    print(f"[{lang}] PDF: {pdf_path} ({pdf_path.stat().st_size // 1024} KB)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Vol1 display edition PDF")
    parser.add_argument(
        "--pdf-lang",
        choices=("ja", "zh", "both"),
        default="ja",
        help="PDF language (default: ja per publishing target)",
    )
    args = parser.parse_args()

    langs = ["ja", "zh"] if args.pdf_lang == "both" else [args.pdf_lang]
    rc = 0
    for lang in langs:
        rc |= build_one(lang)
    return rc


if __name__ == "__main__":
    sys.exit(main())
