#!/usr/bin/env python3
"""
Case Card & story asset lint for 《学堂趣事录》.

Checks markdown Case Cards under docs/volume_planning/ against
docs/world_reference/08_CASE_CARD_TEMPLATE.md required fields.

Usage:
  python scripts/case_card_lint.py
  python scripts/case_card_lint.py --file docs/volume_planning/volume_01_wet_chair_case_card.md
  python scripts/case_card_lint.py --visual vol1
  python scripts/case_card_lint.py --story-table
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOLUME_PLANNING = ROOT / "docs" / "volume_planning"
STORY_TABLE = ROOT / "docs" / "story_database" / "00_story_asset_table.md"
VISUAL_INDEX = ROOT / "docs" / "assets_index" / "visual_asset_index.md"

# Each entry: canonical name -> acceptable table header aliases (substring match)
REQUIRED_FIELDS: dict[str, list[str]] = {
    "卷目": ["卷目"],
    "核心异常": ["核心异常"],
    "表层误会": ["表层误会"],
    "真实机制": ["真实机制"],
    "核心知识": ["核心知识"],
    "交叉知识": ["交叉知识"],
    "公平线索 1": ["公平线索 1", "公平线索1"],
    "公平线索 2": ["公平线索 2", "公平线索2"],
    "公平线索 3": ["公平线索 3", "公平线索3"],
    "儿童可复现实验": ["儿童可复现实验", "儿童实验", "儿童可复现"],
    "日本校园成立理由": ["日本校园成立", "校园成立", "日本校园成立理由"],
    "名古屋环境成立理由": ["名古屋环境成立", "环境成立", "名古屋环境成立理由"],
    "零超自然": ["零超自然", "最终解释零超自然"],
}

OPTIONAL_FIELDS: dict[str, list[str]] = {
    "月份": ["月份"],
    "城市": ["城市"],
    "来源标签": ["来源标签"],
}

VOL1_CANONICAL_PNGS = [
    "01_scene_wet_chair.png",
    "02_scene_four_chairs.png",
    "03_scene_rumor_search.png",
    "04_scene_window_frame.png",
    "05_scene_experiment_setup.png",
    "06_scene_dew_map.png",
    "07_scene_one_fist_gap.png",
    "08_scene_case_logbook.png",
    "09_summary_three_principles.png",
    "10_summary_home_experiment.png",
    "11_summary_hikaru_sketch.png",
    "12_summary_april_daily.png",
]

VOL1_ILLUST_DIR = ROOT / "03_故事内容" / "第1卷_总是湿的椅子" / "插图"


@dataclass
class LintResult:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _normalize_cell(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_markdown_table(content: str) -> dict[str, str]:
    """Extract | key | value | rows from markdown tables."""
    rows: dict[str, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [_normalize_cell(p) for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        key, val = parts[0], parts[1]
        if key in ("项", "字段", "---", "----") or set(key) <= {"-"}:
            continue
        if val in ("内容", "说明", "---"):
            continue
        rows[key] = val
    return rows


def _find_value(rows: dict[str, str], aliases: list[str]) -> str | None:
    for row_key, row_val in rows.items():
        for alias in aliases:
            if alias in row_key or row_key in alias:
                return row_val
    return None


def lint_case_card(path: Path) -> LintResult:
    result = LintResult(path=path)
    if not path.is_file():
        result.errors.append(f"文件不存在: {path}")
        return result

    content = path.read_text(encoding="utf-8")
    rows = parse_markdown_table(content)

    if not rows:
        result.errors.append("未解析到 Case Card 表格（需 | 项 | 内容 | 格式）")
        return result

    for canonical, aliases in REQUIRED_FIELDS.items():
        val = _find_value(rows, aliases)
        if val is None:
            result.errors.append(f"缺少必填字段: {canonical}")
        elif not val or val.upper() == "TBD":
            result.errors.append(f"字段为空或未填: {canonical}")
        elif canonical == "零超自然" and val.upper() not in ("YES", "Y", "是"):
            result.errors.append(f"零超自然须为 YES，当前: {val}")

    for canonical, aliases in OPTIONAL_FIELDS.items():
        val = _find_value(rows, aliases)
        if val is None:
            result.warnings.append(f"建议补充: {canonical}")

    # Fair clues should not be placeholder
    for i in range(1, 4):
        val = _find_value(rows, REQUIRED_FIELDS[f"公平线索 {i}"])
        if val and len(val) < 4:
            result.warnings.append(f"公平线索 {i} 过短，可能未写完整")

    # Cross-knowledge count hint
    cross = _find_value(rows, REQUIRED_FIELDS["交叉知识"])
    if cross:
        parts = re.split(r"[·、,，/]", cross)
        if len([p for p in parts if p.strip()]) < 2:
            result.warnings.append("交叉知识建议 ≥3 项（模板要求）")

    # Scorecard reference
    scorecard_match = re.search(r"\[volume_\d+_scorecard\.yaml\]", content)
    if scorecard_match:
        yaml_name = re.search(r"volume_\d+_scorecard\.yaml", content)
        if yaml_name:
            yaml_path = path.parent / yaml_name.group(0)
            if not yaml_path.is_file():
                result.warnings.append(f"引用的 scorecard 不存在: {yaml_path.name}")

    return result


def discover_case_cards() -> list[Path]:
    if not VOLUME_PLANNING.is_dir():
        return []
    return sorted(VOLUME_PLANNING.glob("*_case_card.md"))


def lint_story_table() -> LintResult:
    result = LintResult(path=STORY_TABLE)
    if not STORY_TABLE.is_file():
        result.errors.append(f"故事资产表不存在: {STORY_TABLE}")
        return result

    content = STORY_TABLE.read_text(encoding="utf-8")
    if "Vol01" not in content:
        result.warnings.append("主表未见 Vol01 示例行")

    # Parse data rows in ## 主表 section only
    data_rows = []
    in_main = False
    for line in content.splitlines():
        if line.strip() == "## 主表":
            in_main = True
            continue
        if in_main and line.startswith("## "):
            break
        if not in_main:
            continue
        if line.startswith("| id |"):
            continue
        if line.startswith("|----"):
            continue
        if line.startswith("| Vol"):
            status_markers = ("PENDING", "READY_", "IDEA", "DRAFT", "OUTLINE", "LOCKED")
            if any(m in line for m in status_markers):
                data_rows.append(line)

    if not data_rows:
        result.warnings.append("主表无 Vol* 数据行")

    for row in data_rows:
        cols = [_normalize_cell(c) for c in row.strip("|").split("|")]
        if len(cols) < 14:
            result.errors.append(f"故事表列数不足 ({len(cols)}/14): {row[:80]}...")
            continue
        (
            vol_id,
            _title_cn,
            _title_jp,
            status,
            month,
            science,
            clues,
            _exp,
            _chars,
            l1c,
            l1e,
            l1f,
            paths,
            _notes,
        ) = cols[:14]
        if status.startswith("READY_") and not all(x.upper().startswith("Y") for x in (l1c, l1e, l1f)):
            result.errors.append(f"{vol_id}: status={status} 但 L1 未全 Y")
        if not month or month == "—":
            result.warnings.append(f"{vol_id}: 缺少 month_nagoya")
        if not science:
            result.errors.append(f"{vol_id}: science_core 为空")
        if clues.count(";") + clues.count("；") < 2:
            result.warnings.append(f"{vol_id}: fair_clues 建议 ≥3 条（分号分隔）")
        case_card = VOLUME_PLANNING / f"volume_{vol_id.replace('Vol', '').zfill(2)}_wet_chair_case_card.md"
        # Generic: any case card matching volume number
        vol_num = vol_id.replace("Vol", "").lstrip("0") or "1"
        candidates = list(VOLUME_PLANNING.glob(f"volume_{int(vol_num):02d}_*_case_card.md"))
        if vol_id == "Vol01" and not candidates:
            if not (VOLUME_PLANNING / "volume_01_wet_chair_case_card.md").is_file():
                result.warnings.append(f"{vol_id}: 无对应 case_card 文件")

    # Case card index should not say 待链
    if "待链具体文件名" in content:
        result.warnings.append("Case Card 索引仍为「待链具体文件名」，请更新为实际路径")

    return result


def lint_vol1_visuals() -> LintResult:
    result = LintResult(path=VOL1_ILLUST_DIR)
    if not VOL1_ILLUST_DIR.is_dir():
        result.errors.append(f"插图目录不存在: {VOL1_ILLUST_DIR}")
        return result

    missing = []
    empty = []
    for name in VOL1_CANONICAL_PNGS:
        p = VOL1_ILLUST_DIR / name
        if not p.is_file():
            missing.append(name)
        elif p.stat().st_size < 10_000:
            empty.append(name)

    if missing:
        result.errors.append(f"Vol1 缺 PNG ({len(missing)}): " + ", ".join(missing))
    if empty:
        result.errors.append(f"Vol1 PNG 过小可能损坏: " + ", ".join(empty))

    prompts = VOL1_ILLUST_DIR / "prompts_插图Vol1.md"
    if not prompts.is_file():
        result.warnings.append("缺少 prompts_插图Vol1.md")
    else:
        prompt_text = prompts.read_text(encoding="utf-8")
        for name in VOL1_CANONICAL_PNGS:
            if name not in prompt_text:
                result.warnings.append(f"prompts 未引用: {name}")

    if not VISUAL_INDEX.is_file():
        result.warnings.append(f"视觉索引不存在: {VISUAL_INDEX.relative_to(ROOT)}")

    return result


def print_result(result: LintResult, verbose: bool) -> None:
    rel = result.path.relative_to(ROOT) if result.path.is_relative_to(ROOT) else result.path
    status = "PASS" if result.ok else "FAIL"
    print(f"\n[{status}] {rel}")
    for err in result.errors:
        print(f"  ERROR: {err}")
    if verbose or result.warnings:
        for warn in result.warnings:
            print(f"  WARN:  {warn}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Case Cards and related assets")
    parser.add_argument(
        "--file",
        type=Path,
        help="Single case card markdown path",
    )
    parser.add_argument(
        "--story-table",
        action="store_true",
        help="Lint docs/story_database/00_story_asset_table.md",
    )
    parser.add_argument(
        "--visual",
        choices=["vol1"],
        help="Lint visual assets for a volume",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Only show failures")
    args = parser.parse_args()

    results: list[LintResult] = []

    if args.file:
        p = args.file if args.file.is_absolute() else ROOT / args.file
        results.append(lint_case_card(p))
    else:
        cards = discover_case_cards()
        if not cards:
            r = LintResult(path=VOLUME_PLANNING)
            r.warnings.append("未找到 *_case_card.md")
            results.append(r)
        for card in cards:
            results.append(lint_case_card(card))

    if args.story_table:
        results.append(lint_story_table())

    if args.visual == "vol1":
        results.append(lint_vol1_visuals())

    verbose = not args.quiet
    failed = 0
    for r in results:
        if r.errors or r.warnings or not args.quiet:
            print_result(r, verbose=verbose)
        if not r.ok:
            failed += 1

    if failed:
        print(f"\n{failed} check(s) failed.")
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
