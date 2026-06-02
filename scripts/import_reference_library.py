#!/usr/bin/env python3
"""
Reference library inventory for 09_日本参考资料库.

Read-only scan: file list, size, INDEX.md cross-check, optional tag grep.

Usage:
  python scripts/import_reference_library.py
  python scripts/import_reference_library.py --write-report
  python scripts/import_reference_library.py --vol 2
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF_ROOT = ROOT / "09_日本参考资料库"
INDEX_MD = REF_ROOT / "INDEX.md"
QUICK_REF = REF_ROOT / "11_写作素材速查" / "按卷可用的元素清单.txt"
REPORT_PATH = ROOT / "docs" / "reference_import" / "00_last_inventory.md"

FACT_TAGS = (
    "VERIFIED_SOURCE",
    "CONSULTANT_CONFIRMED",
    "LOCAL_VARIATION",
    "SEASONAL_VARIATION",
    "CREATOR_CURATED_PENDING_SOURCE_LINK",
    "NEEDS_VERIFICATION",
    "DO_NOT_USE",
)


@dataclass
class InventoryResult:
    files: list[Path] = field(default_factory=list)
    missing_from_index: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.warnings or all("WARN" in w for w in self.warnings)


def collect_ref_files() -> list[Path]:
    if not REF_ROOT.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(REF_ROOT.rglob("*")):
        if not p.is_file():
            continue
        if p.name.startswith("."):
            continue
        if p.suffix.lower() in (".txt", ".md", ".html"):
            out.append(p)
    return out


def index_backtick_paths(index_text: str) -> set[str]:
    """Paths mentioned in INDEX.md as `path` or `dir/`."""
    found: set[str] = set()
    for m in re.finditer(r"`([^`]+)`", index_text):
        token = m.group(1).strip()
        if "/" in token or token.endswith(".txt") or token.endswith(".md"):
            found.add(token.replace("\\", "/"))
    return found


def file_index_key(path: Path) -> str:
    rel = path.relative_to(REF_ROOT).as_posix()
    return rel


def scan_tags(files: list[Path]) -> dict[str, int]:
    counts = {t: 0 for t in FACT_TAGS}
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for tag in FACT_TAGS:
            if tag in text:
                counts[tag] += 1
    return counts


def vol_hints(vol: int, quick_ref_text: str) -> list[str]:
    if not quick_ref_text:
        return []
    lines = []
    pattern = re.compile(rf"第?\s*{vol}\s*卷|Vol\s*0?{vol}\b|Vol{vol:02d}", re.I)
    for line in quick_ref_text.splitlines():
        if pattern.search(line):
            lines.append(line.strip())
    return lines[:20]


def run_inventory(write_report: bool, vol: int | None) -> InventoryResult:
    result = InventoryResult()
    result.files = collect_ref_files()

    if not result.files:
        result.warnings.append("ERROR: 09_日本参考资料库 未找到或为空")
        return result

    index_text = INDEX_MD.read_text(encoding="utf-8") if INDEX_MD.is_file() else ""
    indexed = index_backtick_paths(index_text) if index_text else set()

    for p in result.files:
        key = file_index_key(p)
        # Only flag top-level category files not obviously in INDEX
        if p.parent != REF_ROOT and p.suffix in (".txt", ".md"):
            basename = p.name
            parent = p.parent.name + "/"
            if basename not in index_text and parent not in index_text:
                if key not in indexed and len(key) < 120:
                    result.missing_from_index.append(key)

    if len(result.missing_from_index) > 15:
        result.warnings.append(
            f"WARN: {len(result.missing_from_index)} 文件可能未在 INDEX.md 列出（抽样检查）"
        )

    tag_counts = scan_tags(result.files)
    if tag_counts.get("NEEDS_VERIFICATION", 0) == 0 and tag_counts.get("VERIFIED_SOURCE", 0) == 0:
        result.warnings.append("WARN: 未在 09_ 中检测到来源标签（可能仅 L2 原文）")

    quick = QUICK_REF.read_text(encoding="utf-8") if QUICK_REF.is_file() else ""

    lines = [
        f"# 09_ 参考资料库盘点 · {date.today().isoformat()}",
        "",
        f"> 生成：`python scripts/import_reference_library.py --write-report`",
        "",
        "## 汇总",
        "",
        f"| 指标 | 值 |",
        f"|------|-----|",
        f"| 文本文件数 | {len(result.files)} |",
        f"| INDEX.md | {'存在' if INDEX_MD.is_file() else '缺失'} |",
        f"| 导入协议 | `docs/02_REFERENCE_LIBRARY_IMPORT_PROTOCOL.md` · HYBRID_MERGE_COMPLETE |",
        "",
        "## 来源标签出现次数（文件级）",
        "",
        "| 标签 | 文件数 |",
        "|------|--------|",
    ]
    for tag in FACT_TAGS:
        lines.append(f"| {tag} | {tag_counts.get(tag, 0)} |")

    if vol is not None:
        hints = vol_hints(vol, quick)
        lines.extend(["", f"## Vol{vol:02d} 速查摘录", ""])
        if hints:
            lines.extend(f"- {h}" for h in hints)
        else:
            lines.append("（按卷清单中无匹配行 · 见卷任务包调度单）")

    lines.extend(["", "## 文件清单", ""])
    for p in result.files:
        rel = p.relative_to(ROOT).as_posix()
        size_kb = p.stat().st_size // 1024
        lines.append(f"- `{rel}` ({size_kb} KB)")

    if result.missing_from_index:
        lines.extend(["", "## 可能未索引（抽查）", ""])
        for key in result.missing_from_index[:30]:
            lines.append(f"- `{key}`")

    report = "\n".join(lines) + "\n"

    if write_report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(report, encoding="utf-8")

    try:
        print(report)
    except UnicodeEncodeError:
        rel = REPORT_PATH.relative_to(ROOT) if REPORT_PATH.is_file() else REPORT_PATH
        print(f"Inventory: {len(result.files)} files. Full report: {rel} (--write-report)")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory 09_ reference library")
    parser.add_argument("--write-report", action="store_true", help="Write docs/reference_import/00_last_inventory.md")
    parser.add_argument("--vol", type=int, help="Append vol-specific hints from 按卷清单")
    args = parser.parse_args()

    result = run_inventory(write_report=args.write_report, vol=args.vol)
    if any(w.startswith("ERROR") for w in result.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
