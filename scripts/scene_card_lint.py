#!/usr/bin/env python3
"""
Scene Card lint for 《学堂趣事录》.

Parses docs/volume_planning/*_scene_cards.md (## SC-XX sections + tables).

Usage:
  python scripts/scene_card_lint.py
  python scripts/scene_card_lint.py --file docs/volume_planning/volume_01_scene_cards.md
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOLUME_PLANNING = ROOT / "docs" / "volume_planning"

# Minimum fields per scene (aliases for table keys)
SCENE_REQUIRED: dict[str, list[str]] = {
    "月/时": ["月/时", "月份", "时刻", "月", "时间"],
    "地点": ["地点", "場所"],
}

SCENE_RECOMMENDED: dict[str, list[str]] = {
    "气温/湿度": ["气温/湿度", "气温", "湿度"],
    "光线": ["光线", "光线方向", "日照"],
    "人物": ["人物", "人物理由"],
    "制度": ["制度", "涉及校园制度"],
    "线索/机制": ["线索", "机制", "科学", "可被儿童观察"],
    "来源标签": ["来源标签", "标签"],
}


@dataclass
class SceneLint:
    scene_id: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


@dataclass
class FileLintResult:
    path: Path
    scenes: list[SceneLint] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        if self.errors:
            return False
        return all(s.ok for s in self.scenes)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_table_rows(block: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [_normalize(p) for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        key, val = parts[0], parts[1]
        if key in ("项", "字段") or set(key) <= {"-"} or val in ("值", "内容", "---"):
            continue
        rows[key] = val
    return rows


def _find(rows: dict[str, str], aliases: list[str]) -> str | None:
    for k, v in rows.items():
        for a in aliases:
            if a in k or k in a:
                return v
    return None


def parse_scene_cards(content: str) -> list[tuple[str, dict[str, str]]]:
    scenes: list[tuple[str, dict[str, str]]] = []
    parts = re.split(r"(?=^##\s+SC[-\s]?\d+)", content, flags=re.MULTILINE)
    for part in parts:
        m = re.match(r"^##\s+(SC[-\s]?\d+[^\n]*)", part.strip())
        if not m:
            continue
        scene_id = m.group(1).strip()
        rows = parse_table_rows(part)
        if rows:
            scenes.append((scene_id, rows))
    return scenes


def lint_scene_file(path: Path) -> FileLintResult:
    result = FileLintResult(path=path)
    if not path.is_file():
        result.errors.append(f"文件不存在: {path}")
        return result

    content = path.read_text(encoding="utf-8")
    scenes = parse_scene_cards(content)
    if not scenes:
        result.errors.append("未解析到 ## SC-XX 场景块（需表格 | 项 | 值 |）")
        return result

    for scene_id, rows in scenes:
        sl = SceneLint(scene_id=scene_id)
        for canonical, aliases in SCENE_REQUIRED.items():
            val = _find(rows, aliases)
            if val is None:
                sl.errors.append(f"缺少: {canonical}")
            elif not val or val.upper() == "TBD":
                sl.errors.append(f"为空: {canonical}")

        for canonical, aliases in SCENE_RECOMMENDED.items():
            val = _find(rows, aliases)
            if val is None:
                sl.warnings.append(f"建议补充: {canonical}")

        result.scenes.append(sl)

    return result


def discover_scene_files() -> list[Path]:
    if not VOLUME_PLANNING.is_dir():
        return []
    return sorted(VOLUME_PLANNING.glob("*_scene_cards.md"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Scene Card markdown files")
    parser.add_argument("--file", type=Path, help="Single scene cards file")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    paths: list[Path]
    if args.file:
        p = args.file if args.file.is_absolute() else ROOT / args.file
        paths = [p]
    else:
        paths = discover_scene_files()

    if not paths:
        print("No *_scene_cards.md found.", file=sys.stderr)
        return 1

    failed = 0
    verbose = not args.quiet

    for path in paths:
        r = lint_scene_file(path)
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        if not r.ok:
            failed += 1
            print(f"\n[FAIL] {rel}")
        elif verbose:
            print(f"\n[PASS] {rel}")

        for err in r.errors:
            print(f"  ERROR: {err}")
        for sl in r.scenes:
            if sl.errors or (verbose and sl.warnings):
                print(f"  [{sl.scene_id}]")
                for e in sl.errors:
                    print(f"    ERROR: {e}")
                if verbose:
                    for w in sl.warnings:
                        print(f"    WARN:  {w}")

    if failed:
        print(f"\n{failed} file(s) failed.")
        return 1
    print("\nAll scene checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
