#!/usr/bin/env python3
"""Scan repo for 4年2組 canon drift; emit categorized markdown report."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "docs" / "canon_remap" / "4年2組_漂移扫描清单.md"

PATTERNS = [
    re.compile(r"4年2組"),
    re.compile(r"4年2组"),
    re.compile(r"四年二組"),
    re.compile(r"四年二组"),
    re.compile(r"4-2組"),
    re.compile(r"4-2组"),
    re.compile(r"4年2\s*組"),
]

SKIP_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".cursor",
}

# path fragment -> category override (first match wins)
PATH_RULES: list[tuple[str, str, str]] = [
    ("第1卷_总是湿的椅子", "DEPRECATED_ASSET", "方案 A 湿椅子素材库 · 非 Vol1 正典"),
    ("第2卷_谁偷了橡皮/完整文字稿", "NEEDS_REMAP", "Vol2 正文待改 5年跨班"),
    ("00_归档", "DEPRECATED_ASSET", "归档 · 只读"),
    ("_archive", "DEPRECATED_ASSET", "归档 · 只读"),
    ("05_创作对话记录", "DEPRECATED_ASSET", "历史对话 · 非正典"),
    ("PHASE2_", "NEEDS_REMAP", "旧 AI prompt · 待改年级举牌"),
    ("CLASSROOM_4-2", "NEEDS_REMAP", "文件名历史 · 内容应对齐 5-2"),
    ("volume_01_wet_chair", "DEPRECATED_ASSET", "湿椅子 Case 路径 · 素材"),
    ("volume_02_scene_cards", "NEEDS_REMAP", "Vol2 场景卡待改"),
    ("00_年级班级关系表_V1.0", "CANON_OK", "V1.0 正典 · 含瑆 4-2 对照表"),
    ("00_正典门禁", "CANON_OK", "门禁 · 瑆 4-2 为正确引用"),
    ("00_人物名称与表记", "CANON_OK", "人名表 · 瑆 4-2"),
    ("TANAKA_MIDORI", "CANON_OK", "顾问包 · 废止旧 4-2 简报说明"),
    ("00_character_canon_index", "CANON_OK", "角色索引 · 冲突处理说明"),
    ("canon_remap", "CANON_OK", "Remap 规则 · 含 G3 Gate"),
    ("4年2組_漂移扫描", "CANON_OK", "本扫描报告"),
    ("角色总览表_最终定稿", "CANON_OK", "含 V1.0 变更说明"),
    ("CHAR_lineup_L0_举牌手改清单", "NEEDS_REMAP", "旧举牌文案 · 待手改或废弃"),
    ("人物整体描述.txt", "NEEDS_REMAP", "角色总述 · 部分段落待 remap"),
    ("docs/season_01", "NEEDS_REMAP", "检查 Vol1 行是否已 remap"),
]

KEI_MARKERS = ("陆瑆", "陸瑆", "りく ひかる", "瑆", "Hikaru", "记录者", "非社员", "笔记")
DEPRECATED_KEI = ("りく けい", "Riku Kei", "けいちゃん")

TEXT_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".html", ".py", ".json", ".csv", ".tsx", ".ts", ".js"
}


@dataclass
class Hit:
    path: Path
    line_no: int
    line: str
    category: str
    note: str


@dataclass
class Report:
    hits: list[Hit] = field(default_factory=list)

    def add(self, hit: Hit) -> None:
        self.hits.append(hit)


def classify(rel: str, line: str) -> tuple[str, str]:
    for frag, cat, note in PATH_RULES:
        if frag in rel.replace("\\", "/"):
            return cat, note

    if any(m in line for m in DEPRECATED_KEI) and ("瑆" in line or "陆瑆" in line):
        return "NEEDS_REMAP", "陸瑆 废止读音 けい · 正典 ひかる"

    if any(m in line for m in KEI_MARKERS):
        return "CANON_KEI", "瑆 4年2組 · V1.0 正确"

    if "废止" in line or "已废止" in line or "非4年2組" in line or "5年跨班" in line:
        return "CANON_OK", "文档内已标注废止/正典对照"

    if "5年2組" in line or "5年1組" in line or "5年3組" in line:
        return "NEEDS_REMAP", "同段含新年级 · 检查上下文是否混用"

    return "NEEDS_REMAP", "待核对 · 可能为旧四人同班结构"


def scan_file(path: Path, report: Report) -> None:
    rel = str(path.relative_to(ROOT))
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for i, line in enumerate(text.splitlines(), 1):
        if not any(p.search(line) for p in PATTERNS):
            continue
        cat, note = classify(rel, line)
        report.add(Hit(path=path, line_no=i, line=line.strip()[:120], category=cat, note=note))


def iter_files() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if p.stat().st_size > 2_000_000:
            continue
        out.append(p)
    return out


def render(report: Report) -> str:
    order = ["DEPRECATED_ASSET", "NEEDS_REMAP", "CANON_KEI", "CANON_OK"]
    labels = {
        "DEPRECATED_ASSET": "废止素材（勿当正典引用）",
        "NEEDS_REMAP": "待改（正文/prompt/索引）",
        "CANON_KEI": "正典（瑆 · 4年2組 非社员）",
        "CANON_OK": "正典/说明（含废止标注或 Gate）",
    }
    by_cat: dict[str, list[Hit]] = {k: [] for k in order}
    for h in report.hits:
        by_cat.setdefault(h.category, []).append(h)

    lines = [
        "# 4年2組 · 正典漂移扫描清单",
        "",
        "> **生成**: `python scripts/canon_sweep_4-2.py`",
        "> **正典**: 观察社 **5年跨班** · 瑆 **4年2組非社员** · [`01_角色设定/00_年级班级关系表_V1.0.md`](../../01_角色设定/00_年级班级关系表_V1.0.md)",
        "",
        "## 汇总",
        "",
        "| 类别 | 命中行数 |",
        "|------|----------|",
    ]
    for cat in order:
        lines.append(f"| {labels[cat]} | {len(by_cat.get(cat, []))} |")
    lines.append(f"| **合计** | **{len(report.hits)}** |")
    lines.append("")

    for cat in order:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.extend([f"## {labels[cat]}", ""])
        current = ""
        for h in sorted(items, key=lambda x: (str(x.path), x.line_no)):
            rel = h.path.relative_to(ROOT).as_posix()
            if rel != current:
                lines.append(f"### `{rel}`")
                lines.append(f"> {h.note}")
                current = rel
            lines.append(f"- L{h.line_no}: `{h.line}`")
        lines.append("")

    lines.extend(
        [
            "## 处置优先级",
            "",
            "1. **P0** `NEEDS_REMAP` 中 Vol2 正文 · PHASE2 prompt · 举牌清单",
            "2. **P1** 标记 `DEPRECATED_ASSET` 目录 README 顶部加废止横幅",
            "3. **保留** `CANON_KEI` / `CANON_OK` — 勿删瑆年级",
            "",
            "## Vol01 → LOCKED（L1 后）",
            "",
            "见 [`Vol01_LOCK_门禁.md`](./Vol01_LOCK_门禁.md)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan 4年2組 canon drift")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    report = Report()
    for fp in iter_files():
        scan_file(fp, report)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(report), encoding="utf-8")
    print(f"scanned {len(report.hits)} hits -> {args.out}")


if __name__ == "__main__":
    main()
