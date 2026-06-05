#!/usr/bin/env python3
"""Assemble a COMPLETE single-case unit book: cover · storyboard · prose · all illus · notes · experiment."""

from __future__ import annotations

import argparse
import base64
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / "03_故事内容"

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

OUT_DATE = date.today().strftime("%Y%m%d")


@dataclass
class Shot:
    file: str
    caption: str
    sc_id: str = ""


@dataclass
class Chapter:
    title: str
    body: str
    shots: list[Shot] = field(default_factory=list)


@dataclass
class UnitConfig:
    slug: str
    title_cn: str
    subtitle: str
    tagline: str
    prose_path: Path
    illust_dir: Path
    out_dir: Path
    pdf_name: str
    notice: str
    storyboard_rows: list[tuple[str, str, str, str]]  # sc, beat, caption, file
    chapter_shots: list[tuple[str, list[Shot]]]  # chapter title prefix → shots after chapter
    extra_pages: dict[str, str]  # key → relative path or empty for inline html id
    diary_text: str = ""
    diary_image: str = ""
    experiment_html: str = ""
    clue_html: str = ""
    principle_html: str = ""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def img_uri(base: Path, name: str) -> str:
    p = base / name
    if not p.exists():
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def strip_prose_meta(raw: str) -> str:
    lines = raw.splitlines()
    body: list[str] = []
    for line in lines:
        if line.strip().startswith("【定稿自检】") or line.strip().startswith("【你可以这样做】"):
            break
        if line.strip().startswith("════════════════"):
            break
        if line.strip() == "---":
            break
        if line.startswith("【定稿信息】") or line.startswith("  ·"):
            continue
        if line.strip().startswith("【样章包") or line.strip().startswith("【语感编辑"):
            break
        if line.strip().startswith("【写作备注"):
            break
        body.append(line)
    while body and not body[-1].strip():
        body.pop()
    return "\n".join(body).strip()


def parse_chapters(text: str) -> list[Chapter]:
    pattern = re.compile(
        r"^(序 · .+|一、.+|二、.+|三、.+|四、.+|五、.+|六、.+|七、.+)$",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(text))
    chapters: list[Chapter] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end].strip()
        lines = block.splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        body = re.sub(r"^-{3,}$", "", body, flags=re.MULTILINE).strip()
        chapters.append(Chapter(title=title, body=body))
    return chapters


def prose_block_to_html(body: str) -> str:
    parts: list[str] = []
    para: list[str] = []
    for line in body.splitlines():
        s = line.rstrip()
        if not s:
            if para:
                parts.append("<p>" + "<br/>".join(para) + "</p>")
                para = []
            continue
        if re.match(r"^={3,}$", s):
            continue
        if s.startswith("### "):
            if para:
                parts.append("<p>" + "<br/>".join(para) + "</p>")
                para = []
            parts.append(f'<h3 class="beat">{s[4:]}</h3>')
            continue
        if s.startswith("  ") and not s.startswith("  http"):
            para.append(f'<span class="hang">{s.strip()}</span>')
        elif s.startswith("　　"):
            para.append(s)
        else:
            para.append(s)
    if para:
        parts.append("<p>" + "<br/>".join(para) + "</p>")
    return "\n".join(parts)


def shots_html(illust_dir: Path, shots: list[Shot], layout: str = "spread") -> str:
    if not shots:
        return ""
    blocks: list[str] = []
    for sh in shots:
        uri = img_uri(illust_dir, sh.file)
        if not uri:
            continue
        sc = f'<span class="sc-badge">{sh.sc_id}</span>' if sh.sc_id else ""
        cls = "illus spread" if layout == "spread" else "illus half"
        blocks.append(
            f'<figure class="{cls}">{sc}'
            f'<img src="{uri}" alt="{sh.caption}"/>'
            f'<figcaption>{sh.caption}</figcaption></figure>'
        )
    return "\n".join(blocks)


def storyboard_table(illust_dir: Path, rows: list[tuple[str, str, str, str]]) -> str:
    trs = []
    for sc, beat, cap, fname in rows:
        uri = img_uri(illust_dir, fname)
        thumb = f'<img class="thumb" src="{uri}" alt=""/>' if uri else "—"
        trs.append(
            f"<tr><td><strong>{sc}</strong></td><td>{beat}</td>"
            f"<td>{cap}</td><td class='thumb-cell'>{thumb}</td></tr>"
        )
    return (
        "<table class='storyboard'><thead><tr>"
        "<th>镜头</th><th>节拍</th><th>画面</th><th>缩略</th>"
        "</tr></thead><tbody>" + "".join(trs) + "</tbody></table>"
    )


CSS = """
@page { size: A5; margin: 14mm 13mm; }
* { box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "PingFang SC", "Hiragino Sans GB", "Noto Sans SC", sans-serif;
  font-size: 11pt; line-height: 1.58; color: #1a1a1a; margin: 0; padding: 0;
}
.page { page-break-after: always; padding: 6mm 0; min-height: 252mm; position: relative; }
.page:last-child { page-break-after: auto; }
.cover {
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; min-height: 260mm; background: linear-gradient(165deg, #f8f5ef 0%, #ebe6dc 100%);
  padding: 12mm;
}
.cover .series { font-size: 10pt; letter-spacing: 0.35em; color: #666; margin-bottom: 1em; }
.cover h1 { font-size: 21pt; margin: 0.2em 0; font-weight: 700; }
.cover h2 { font-size: 13pt; font-weight: 400; color: #444; margin: 0.5em 0 1.2em; }
.cover .cover-art { max-width: 88%; max-height: 110mm; margin: 1em 0; box-shadow: 0 4px 20px rgba(0,0,0,0.12); }
.cover .meta { font-size: 9pt; color: #555; margin-top: 2em; line-height: 1.6; }
.chapter-title {
  font-size: 14pt; border-left: 4px solid #3d5a4a; padding-left: 0.6em;
  margin: 0 0 0.8em; line-height: 1.3;
}
h3.beat { font-size: 10pt; color: #3d5a4a; margin: 1.2em 0 0.4em; letter-spacing: 0.05em; }
p { margin: 0.55em 0; text-indent: 2em; }
p .hang { display: block; text-indent: 0; padding-left: 1.2em; font-style: normal; }
.toc { list-style: none; padding: 0; margin: 1em 0; }
.toc li { padding: 0.45em 0; border-bottom: 1px dotted #ccc; display: flex; justify-content: space-between; }
.toc .dots { flex: 1; border-bottom: 1px dotted #bbb; margin: 0 0.5em 0.3em; }
.storyboard { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 0.8em 0; }
.storyboard th, .storyboard td { border: 1px solid #ccc; padding: 0.35em 0.45em; vertical-align: top; }
.storyboard th { background: #f0ebe3; }
.thumb { max-width: 42mm; max-height: 28mm; object-fit: cover; border: 1px solid #ddd; }
.thumb-cell { text-align: center; width: 48mm; }
.illus { text-align: center; margin: 1em 0; page-break-inside: avoid; }
.illus img { max-width: 100%; height: auto; border-radius: 2px; }
.illus.spread img { max-height: 95mm; }
.illus.half img { max-height: 72mm; }
.illus figcaption { font-size: 8.5pt; color: #555; margin-top: 0.35em; font-style: italic; }
.sc-badge {
  display: inline-block; background: #3d5a4a; color: #fff; font-size: 7.5pt;
  padding: 0.15em 0.5em; border-radius: 2px; margin-bottom: 0.3em;
}
.diary-page {
  background: #fffef6;
  background-image: repeating-linear-gradient(transparent, transparent 1.45em, #e8e2d8 1.45em, #e8e2d8 1.46em);
  padding: 8mm;
}
.diary-page p { text-indent: 0; }
.diary-illus { float: right; max-width: 45%; margin: 0 0 0.5em 1em; }
.diary-illus img { max-width: 100%; }
.info-box {
  border: 1px solid #3d5a4a; padding: 1em; margin: 1em 0;
  background: #f7faf8; page-break-inside: avoid;
}
.info-box h2 { margin-top: 0; font-size: 12pt; text-align: center; }
.clue-card { border: 2px solid #333; padding: 1em; border-radius: 3px; }
.clue-card ul { list-style: none; padding: 0; }
.clue-card li::before { content: "□ "; }
.page-num { position: absolute; bottom: 4mm; right: 0; font-size: 8pt; color: #999; }
.notice { font-size: 9pt; color: #666; text-align: center; margin-top: 3em; line-height: 1.7; }
.section-label {
  font-size: 8pt; letter-spacing: 0.2em; color: #888; text-transform: uppercase;
  border-bottom: 1px solid #ddd; padding-bottom: 0.3em; margin-bottom: 0.8em;
}
@media print { .page { min-height: auto; } }
"""


def prose_with_beats_to_html(body: str, illust_dir: Path, beat_shots: dict[str, list[Shot]]) -> str:
    """Split on ### beats and inject illustrations after matching sections."""
    if not beat_shots:
        return prose_block_to_html(body)
    parts: list[str] = []
    chunks = re.split(r"(### \d+)", body)
    i = 0
    while i < len(chunks):
        chunk = chunks[i]
        if re.match(r"^### \d+$", chunk.strip()):
            key = chunk.strip()
            i += 1
            text = chunks[i] if i < len(chunks) else ""
            i += 1
            parts.append(f'<h3 class="beat">{key[4:]}</h3>')
            parts.append(prose_block_to_html(text))
            shots = beat_shots.get(key, [])
            parts.append(shots_html(illust_dir, shots))
        else:
            if chunk.strip():
                parts.append(prose_block_to_html(chunk))
            i += 1
    return "\n".join(parts)


def build_html(cfg: UnitConfig) -> str:
    raw = strip_prose_meta(read_text(cfg.prose_path))
    chapters = parse_chapters(raw)
    shot_map = {k: v for k, v in cfg.chapter_shots}
    beat_shots = {k: v for k, v in shot_map.items() if k.startswith("###")}

    def match_shots(title: str) -> list[Shot]:
        for prefix, shots in shot_map.items():
            if prefix.startswith("###"):
                continue
            if title.startswith(prefix) or prefix in title:
                return shots
        return []

    cover_uri = ""
    for _, shots in cfg.chapter_shots:
        if shots:
            cover_uri = img_uri(cfg.illust_dir, shots[0].file)
            break

    toc_items = [
        ("分镜头总览", ""),
        *[(c.title.split("\n")[0], "") for c in chapters],
    ]
    if cfg.principle_html:
        toc_items.append(("科学原理图", ""))
    if cfg.diary_text:
        toc_items.append(("陸瑆笔记", ""))
    if cfg.clue_html:
        toc_items.append(("观察社 · 线索卡", ""))
    if cfg.experiment_html:
        toc_items.append(("家庭小实验", ""))
    toc_items.append(("封底", ""))

    toc_html = "<ul class='toc'>" + "".join(
        f"<li><span>{t}</span><span class='dots'></span></li>" for t, _ in toc_items
    ) + "</ul>"

    story_pages = ""
    for ch in chapters:
        shots = match_shots(ch.title)
        body_html = (
            prose_with_beats_to_html(ch.body, cfg.illust_dir, beat_shots)
            if beat_shots and ("一、" in ch.title or "翘边" in ch.title)
            else prose_block_to_html(ch.body)
        )
        story_pages += f"""
<div class="page prose-page">
  <p class="section-label">正文</p>
  <h2 class="chapter-title">{ch.title}</h2>
  {body_html}
  {shots_html(cfg.illust_dir, shots) if not beat_shots else ""}
</div>
"""

    diary_section = ""
    if cfg.diary_text:
        d_uri = img_uri(cfg.illust_dir, cfg.diary_image) if cfg.diary_image else ""
        img_block = (
            f'<div class="diary-illus"><img src="{d_uri}" alt="瑆笔记"/></div>' if d_uri else ""
        )
        diary_section = f"""
<div class="page diary-page">
  <p class="section-label">原理世界 · 读者笔记层</p>
  <h2 class="chapter-title">陸瑆笔记</h2>
  {img_block}
  {prose_block_to_html(cfg.diary_text)}
</div>
"""

    principle_section = ""
    if cfg.principle_html:
        principle_section = f"""
<div class="page">
  <p class="section-label">科学 · 原理图</p>
  <h2 class="chapter-title">为什么会这样？</h2>
  {cfg.principle_html}
</div>
"""

    clue_section = ""
    if cfg.clue_html:
        clue_section = f"""
<div class="page">
  <p class="section-label">互动</p>
  {cfg.clue_html}
</div>
"""

    exp_section = ""
    if cfg.experiment_html:
        exp_section = f"""
<div class="page">
  <p class="section-label">动手 · 家庭实验</p>
  <h2 class="chapter-title">你可以这样做</h2>
  {cfg.experiment_html}
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<title>{cfg.title_cn} · 完整单元书</title>
<style>{CSS}</style>
</head>
<body>

<div class="page cover">
  <p class="series">学堂趣事录 · 完整单元书</p>
  <h1>{cfg.title_cn}</h1>
  <h2>{cfg.subtitle}</h2>
  {"<img class='cover-art' src='" + cover_uri + "' alt='封面'/>" if cover_uri else ""}
  <p class="meta">{cfg.tagline}<br/>{cfg.notice}<br/>{OUT_DATE}</p>
</div>

<div class="page">
  <p class="notice">{cfg.notice}<br/>本 PDF 为内部形态参考 · 竖版 A5 · 单页纵向翻页（桥梁书）</p>
</div>

<div class="page">
  <h2 class="chapter-title">目录</h2>
  {toc_html}
</div>

<div class="page">
  <p class="section-label">出厂层 · 分镜头</p>
  <h2 class="chapter-title">分镜头与插页地图</h2>
  <p style="text-indent:0;font-size:9.5pt;color:#555;">每一格 = 一个 Scene Card · 缩略图 = 成稿插图 · 页码在排版阶段锁定</p>
  {storyboard_table(cfg.illust_dir, cfg.storyboard_rows)}
</div>

{story_pages}
{principle_section}
{diary_section}
{clue_section}
{exp_section}

<div class="page cover" style="min-height:200mm;">
  <p class="series">— 单元完 —</p>
  <h2 style="font-size:12pt;">觉得奇怪，就先观察</h2>
  <p class="meta">不是侦探 · 是观察<br/>奇怪未必是怪，有时只是冷与湿的碰面</p>
</div>

</body>
</html>
"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> bool:
    for chrome in CHROME_CANDIDATES:
        if not chrome.exists():
            continue
        cmd = [
            str(chrome),
            "--headless=new",
            "--disable-gpu",
            f"--print-to-pdf={pdf_path.resolve()}",
            "--no-pdf-header-footer",
            html_path.resolve().as_uri(),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            if pdf_path.exists() and pdf_path.stat().st_size > 5000:
                return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            continue
    return False


def wet_chair_config() -> UnitConfig:
    root = CONTENT / "第1卷_总是湿的椅子"
    ill = root / "插图"
    diary_raw = read_text(root / "完整文字稿.txt")
    diary_m = re.search(
        r"════+\s*\n陸瑆笔记 ·(.+?)——瑆",
        diary_raw,
        re.DOTALL,
    )
    diary = diary_m.group(0) if diary_m else ""
    diary = re.sub(r"^═+\s*\n", "", diary).strip()
    diary = diary.replace("——瑆", "").strip()

    exp_from_story = ""
    exp_m = re.search(r"【你可以这样做】凝结小实验\s*\n-+\s*\n(.+?)════", diary_raw, re.DOTALL)
    if exp_m:
        exp_from_story = exp_m.group(1).strip()

    sum01 = img_uri(ill, "09_summary_three_principles.png")
    principle = (
        f'<figure class="illus spread"><img src="{sum01}" alt="三原理"/>'
        f'<figcaption>热传导 × 湿度 × 露点 — 三样凑齐，水才会在椅子上集合</figcaption></figure>'
        if sum01
        else ""
    )

    exp_sum = img_uri(ill, "10_summary_home_experiment.png")
    experiment = (
        f'<figure class="illus spread"><img src="{exp_sum}" alt="实验步骤"/></figure>'
        f"<div class='info-box'>{prose_block_to_html(exp_from_story)}</div>"
        if exp_sum
        else prose_block_to_html(exp_from_story)
    )

    rows = [
        ("SC01", "钩子", "光按湿椅背 · 四月窗樱", "01_scene_wet_chair.png"),
        ("SC02", "公平线索①", "四椅仅一把贴窗", "02_scene_four_chairs.png"),
        ("SC03", "误导", "全班搜证无果", "03_scene_rumor_search.png"),
        ("SC04", "转折", "窓枠に当たってる", "04_scene_window_frame.png"),
        ("SC05", "验证准备", "铁片+载玻片过夜", "05_scene_experiment_setup.png"),
        ("SC06", "揭晓", "铁片水珠地图", "06_scene_dew_map.png"),
        ("SC07", "处理", "椅背离窗框一拳", "07_scene_one_fist_gap.png"),
        ("SC08", "系列伏笔", "硬壳本 · 第1起", "08_scene_case_logbook.png"),
        ("SUM01", "原理", "三原理信息图", "09_summary_three_principles.png"),
        ("SUM02", "实验", "家庭可复现步骤", "10_summary_home_experiment.png"),
        ("SUM03", "瑆视角", "妹妹涂鸦笔记", "11_summary_hikaru_sketch.png"),
        ("SUM04", "意象", "干椅+凉窗框", "12_summary_april_daily.png"),
    ]

    return UnitConfig(
        slug="wet_chair",
        title_cn="总是湿的椅子",
        subtitle="C001 · 完整单元书 · 形态参考样张",
        tagline="8–11 岁 · 名古屋校园 · 科学观察轻推理",
        prose_path=root / "完整文字稿.txt",
        illust_dir=ill,
        out_dir=root / "PDF",
        pdf_name=f"学堂趣事录_C001_湿椅子_完整单元书_{OUT_DATE}.pdf",
        notice="【C001 素材库 · 非 Vol1 正典】本册展示「一案一书」出厂形态：分镜→正文→原理→笔记→实验",
        storyboard_rows=rows,
        chapter_shots=[
            ("序", []),
            (
                "一、",
                [
                    Shot("01_scene_wet_chair.png", "SC01 · 又湿了", "SC01"),
                    Shot("02_scene_four_chairs.png", "SC02 · 只有这一把贴住窗框", "SC02"),
                ],
            ),
            (
                "二、",
                [
                    Shot("03_scene_rumor_search.png", "SC03 · 传言比水先到场", "SC03"),
                    Shot("04_scene_window_frame.png", "SC04 · 贴着窗框", "SC04"),
                ],
            ),
            ("三、", [Shot("03_scene_rumor_search.png", "SC03 · 志郎：就是恶作剧！", "SC03")]),
            ("四、", [Shot("05_scene_experiment_setup.png", "SC05 · 铁片贴窗框，试一夜", "SC05")]),
            (
                "五、",
                [
                    Shot("06_scene_dew_map.png", "SC06 · 铁片上的地图", "SC06"),
                    Shot("07_scene_one_fist_gap.png", "SC07 · 留一拳，路断了", "SC07"),
                ],
            ),
            (
                "六、",
                [
                    Shot("08_scene_case_logbook.png", "SC08 · 学堂趣事录 · 第1起", "SC08"),
                    Shot("12_summary_april_daily.png", "SUM04 · 干的椅子", "SUM04"),
                ],
            ),
        ],
        extra_pages={},
        diary_text=diary,
        diary_image="11_summary_hikaru_sketch.png",
        experiment_html=experiment,
        clue_html="",
        principle_html=principle,
    )


def case_a001_config() -> UnitConfig:
    vol_root = CONTENT / "第1卷_觉得奇怪就先观察"
    root = vol_root / "样章包"
    ill = root / "插图"
    diary = read_text(root / "05_陸瑆日记页_样章.txt").split("---")[0].strip()
    diary = re.sub(r"^=+\s*\n", "", diary, flags=re.MULTILINE).strip()
    exp = read_text(root / "12_案01_家庭实验页_样章.txt")
    exp = re.sub(r"^# .+\n", "", exp)
    exp = re.sub(r"^> .+\n", "", exp, flags=re.MULTILINE)
    exp = re.sub(r"^---\n", "", exp, flags=re.MULTILINE)

    v03 = img_uri(ill, "V-S03_风侧示意图.png")
    principle = (
        f'<figure class="illus spread"><img src="{v03}" alt="风侧示意"/>'
        f'<figcaption>风从出风栅下来 · 先吹到的外角先翘 · 不是恶作剧</figcaption></figure>'
        if v03
        else ""
    )
    experiment = prose_block_to_html(exp)

    clue = """
<div class="clue-card">
  <h2 style="text-align:center;margin-top:0;">观察社 · 线索卡 #01</h2>
  <p><strong>案：翘边的海报</strong></p>
  <p>今天奇怪的事：海报的边，每天翘在不同侧。</p>
  <p>你已经看见的线索：</p>
  <ul>
    <li>翘边和风来的方向在同一侧</li>
    <li>下雨的日子更容易翘</li>
    <li>贴海报的人，换过贴的方向</li>
  </ul>
  <p>你的猜想：________________</p>
  <p style="text-align:center;margin-top:1.2em;">（答案在故事里 — 先自己想想！）</p>
  <p style="text-align:center;font-size:9pt;">观察社还留了一格空白 —— 下一周，谁会把它填满？</p>
</div>
"""

    rows = [
        ("SC-00", "序钩", "新名札 · 海报右缘微翘", "V-S01_侧廊海报.png"),
        ("SC-01-1", "发现", "四人 · 整条翘边", "V-S01_侧廊海报.png"),
        ("SC-01-2", "误导", "恶作剧？查监控", "V-S01_侧廊海报.png"),
        ("SC-01-3", "线索", "风侧=翘侧 · 雨天", "V-S03_风侧示意图.png"),
        ("SC-01-4", "收束", "换方向贴 · 文件夹挡风", "V-S01_侧廊海报.png"),
        ("SC-01-TAIL", "卷钩", "壁报第4栏空白", "V-S01-TAIL_壁报草稿空栏.png"),
        ("V-S02", "瑆笔记", "风从上面吹，角就翘", "V-S02_陸瑆日记页.png"),
        ("V-S03", "原理", "气流+贴法示意", "V-S03_风侧示意图.png"),
    ]

    return UnitConfig(
        slug="case_a001",
        title_cn="翘边的海报",
        subtitle="Vol1 · 案① · 完整单元书",
        tagline="8–11 岁 · 觉得奇怪，就先观察",
        prose_path=vol_root / "正式版" / "01_正文" / "案01_翘边的海报_HybridVoice_V1.1定稿.txt",
        illust_dir=ill,
        out_dir=vol_root / "样章包" / "PDF",
        pdf_name=f"学堂趣事录_Vol1_案01_完整单元书_V1.1_{OUT_DATE}.pdf",
        notice="【Vol1 正典 · A001】序+案① · 含分镜头表 · 全插图锚点 · 瑆笔记 · 线索卡 · 实验",
        storyboard_rows=rows,
        chapter_shots=[
            ("序", []),
            (
                "### 1",
                [
                    Shot("V-S01_侧廊海报.png", "SC-01-1 · 侧廊 · 翘边换到左边", "SC-01-1"),
                ],
            ),
            ("### 2", []),
            (
                "### 3",
                [
                    Shot("V-S03_风侧示意图.png", "SC-01-3 · 风侧 = 翘侧", "SC-01-3"),
                ],
            ),
            (
                "### 4",
                [
                    Shot("V-S01-TAIL_壁报草稿空栏.png", "SC-01-TAIL · 第4栏留空", "SC-01-TAIL"),
                ],
            ),
        ],
        extra_pages={},
        diary_text=diary,
        diary_image="V-S02_陸瑆日记页.png",
        experiment_html=experiment,
        clue_html=clue,
        principle_html=principle,
    )


def build_unit(cfg: UnitConfig) -> tuple[Path, Path]:
    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    html_path = cfg.out_dir / cfg.pdf_name.replace(".pdf", ".html")
    pdf_path = cfg.out_dir / cfg.pdf_name
    html_path.write_text(build_html(cfg), encoding="utf-8")
    ok = html_to_pdf(html_path, pdf_path)
    return html_path, pdf_path if ok else html_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build complete unit book PDF")
    parser.add_argument(
        "unit",
        nargs="?",
        default="all",
        choices=["all", "wet_chair", "case_a001"],
    )
    args = parser.parse_args()
    units = []
    if args.unit in ("all", "wet_chair"):
        units.append(wet_chair_config())
    if args.unit in ("all", "case_a001"):
        units.append(case_a001_config())

    for cfg in units:
        html_path, out = build_unit(cfg)
        if out.suffix == ".pdf":
            print(f"OK [{cfg.slug}] PDF: {out} ({out.stat().st_size // 1024} KB)")
            print(f"    HTML: {html_path}")
        else:
            print(f"WARN [{cfg.slug}] PDF failed — open HTML: {html_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
