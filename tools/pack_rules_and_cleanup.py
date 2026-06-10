#!/usr/bin/env python3
"""Pack V1.0 rule/spec MD into 11_规则与规范/ and delete process-version folders."""

from __future__ import annotations

import re
import shutil
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RULES_ROOT = REPO / "11_规则与规范"
VOL1 = REPO / "03_故事内容" / "第1卷_觉得奇怪就先观察"
UNIT1 = VOL1 / "单元1_第一单元_五案"

# Source roots for rule MD (relative categorization)
CATEGORY_RULES: list[tuple[str, Path]] = [
    ("01_项目治理", REPO / "00_项目总览"),
    ("01_项目治理", REPO / "00_项目概览"),
    ("02_创作与文学", REPO / "02_创作原则与世界观"),
    ("04_视觉与插画", REPO / "05_视觉设定"),
    ("04_视觉与插画", REPO / "07_设计原档"),
    ("04_视觉与插画", REPO / "08_测试与评审"),
    ("05_产品与出版", REPO / "04_产品与商业"),
    ("05_产品与出版", REPO / "08_全卷出版验证"),
    ("03_工作流与闸门", VOL1),
    ("03_工作流与闸门", UNIT1),
]

UNIT1_RULE_GLOB = (
    "00_*V1.0*.md",
    "00_Agent*.md",
    "00_硬拦截*.md",
    "00_AB*.md",
)

# Entire folders to remove (process / legacy / duplicate trees)
DELETE_DIRS = [
    VOL1 / "V2迁移",
    VOL1 / "_archive_legacy",
    VOL1 / "样章包",
    VOL1 / "正式版",
    VOL1 / "薄样张_试读",
    UNIT1 / "_archive_正文版本",
    UNIT1 / "_archive_插图绑定",
    UNIT1 / "正文",  # version shim tree
    UNIT1 / "插图",  # binding shim tree
    UNIT1 / "A001" / "03_插画" / "B4_CORRECT_试跑",
    UNIT1 / "A001" / "03_插画" / "_archive",
    UNIT1 / "A001" / "03_插画" / "_archive_废止画风引导",
    UNIT1 / "A001" / "04_样张" / "E20_pilot_A001_V3.8_20260609",
    UNIT1 / "A001" / "04_样张" / "E20_pilot_A001_20260608",
    UNIT1 / "A001" / "01_正文" / "_archive",
    UNIT1 / "A001" / "07_设计原档",  # stray duplicate path
    REPO / "10_视觉与插画规范",  # deprecated pointer only
]

V1_MD = re.compile(r"_V1\.0(?:_|\.|$)", re.I)
V0_MD = re.compile(r"_V0\.(?:\d|[\d_])|_V0\.1|_V0\.2|_V0\.3", re.I)
PROCESS_MD = re.compile(r"_V0\.|_V0\.1|_V0\.2|_V0\.3|_V2\.0\.md$|_V1\.1\.md$|_V3\.6\.|R17_V0", re.I)


def is_v1_rule_md(path: Path) -> bool:
    if path.suffix.lower() != ".md":
        return False
    name = path.name
    if "V1.0" not in name and "_V1.0" not in name:
        return False
    # exclude case deliverables / per-case storyboard copies in A00X subdirs
    parts = path.parts
    if "A001" in parts or "A002" in parts or "A003" in parts or "A004" in parts or "A005" in parts:
        if path.name.startswith("00_插画师分镜"):
            return False
        if "工作流跑通" in name or "测试启动" in name or "G-CAST" in name or "G-BRIEF" in name:
            return True
        if "审计" in name or "STYLE_DEMO" in name or "B4" in name or "M0-C" in name:
            return False
        if "prompts" in name.lower():
            return False
    return True


def collect_rule_files() -> list[tuple[str, Path]]:
    found: dict[str, tuple[str, Path]] = {}
    for cat, root in CATEGORY_RULES:
        if not root.is_dir():
            continue
        if root == UNIT1:
            for pattern in UNIT1_RULE_GLOB:
                for p in root.glob(pattern):
                    if p.is_file() and is_v1_rule_md(p):
                        found[str(p.resolve())] = (cat, p)
            continue
        for p in root.rglob("*.md"):
            if is_v1_rule_md(p):
                found[str(p.resolve())] = (cat, p)
    # V2迁移 V1.0 before delete
    v2 = VOL1 / "V2迁移"
    if v2.is_dir():
        for p in v2.rglob("*.md"):
            if is_v1_rule_md(p):
                found[str(p.resolve())] = ("03_工作流与闸门/原V2迁移", p)
    return list(found.values())


def pack_rules(items: list[tuple[str, Path]]) -> list[str]:
    manifest: list[str] = []
    for cat, src in sorted(items, key=lambda x: (x[0], x[1].name)):
        dest_dir = RULES_ROOT / cat
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        if dest.exists() and dest.read_bytes() == src.read_bytes():
            manifest.append(f"| {cat} | `{src.relative_to(REPO)}` | `{dest.relative_to(REPO)}` | 已存在 |")
            continue
        shutil.copy2(src, dest)
        manifest.append(f"| {cat} | `{src.relative_to(REPO)}` | `{dest.relative_to(REPO)}` | 已复制 |")
    return manifest


def delete_process_md() -> list[str]:
    removed: list[str] = []
    scan_roots = [VOL1, REPO / "00_项目总览", REPO / "05_视觉设定"]
    for root in scan_roots:
        if not root.is_dir():
            continue
        for p in list(root.rglob("*.md")):
            if V1_MD.search(p.name):
                continue
            if PROCESS_MD.search(p.name) or "_V0." in p.name:
                try:
                    p.unlink()
                    removed.append(str(p.relative_to(REPO)))
                except OSError as e:
                    removed.append(f"FAIL {p}: {e}")
    return removed


def delete_dirs() -> list[str]:
    log: list[str] = []
    for d in DELETE_DIRS:
        if not d.exists():
            log.append(f"SKIP (missing): {d.relative_to(REPO)}")
            continue
        try:
            shutil.rmtree(d)
            log.append(f"DELETED: {d.relative_to(REPO)}")
        except OSError as e:
            log.append(f"FAIL {d.relative_to(REPO)}: {e}")
    return log


def write_index(manifest: list[str], deleted_dirs: list[str], removed_md: list[str]) -> None:
    RULES_ROOT.mkdir(parents=True, exist_ok=True)
    index = f"""# 规则与规范 · 总索引 · V1.0

> **唯一入口**：项目一级文件夹 `11_规则与规范/`  
> **原则**：只收 **V1.0** 规范 MD · 过程版（V0.x / 迁移报告）已清除  
> **生成**：{date.today().isoformat()} · `tools/pack_rules_and_cleanup.py`

---

## 子目录

| 目录 | 内容 |
|------|------|
| [01_项目治理](./01_项目治理/) | 门禁、索引、专家组、Gate、目录架构 |
| [02_创作与文学](./02_创作与文学/) | L0 红线、文学标准、Hybrid Voice |
| [03_工作流与闸门](./03_工作流与闸门/) | Agent 规则、AB 盲测、G-CAST、单元1 三部门 |
| [04_视觉与插画](./04_视觉与插画/) | 05_视觉设定 + 07_设计原档 规范 V1.0 |
| [05_产品与出版](./05_产品与出版/) | 200 案架构、出版验证 |

**正文/分镜/成稿 SSOT** 仍在 `03_故事内容/…/单元1/A00X/` · 不在此包内。

---

## 已打包文件（{len(manifest)}）

| 分类 | 源路径 | 包内路径 | 状态 |
|------|--------|----------|------|
"""
    index += "\n".join(manifest)
    index += f"""

---

## 已删除过程文件夹（{len(deleted_dirs)}）

"""
    index += "\n".join(f"- {line}" for line in deleted_dirs)
    index += f"""

---

## 已删除过程 MD（{len(removed_md)} 个）

<details>
<summary>展开列表</summary>

"""
    index += "\n".join(f"- `{x}`" for x in removed_md[:200])
    if len(removed_md) > 200:
        index += f"\n\n… 另有 {len(removed_md) - 200} 个"
    index += "\n</details>\n"
    (RULES_ROOT / "00_总索引_V1.0.md").write_text(index, encoding="utf-8")

    stub = f"""# 10_视觉与插画规范 · 已迁移

> **SSOT** → [`11_规则与规范/00_总索引_V1.0.md`](../11_规则与规范/00_总索引_V1.0.md)  
> 视觉规范见 `11_规则与规范/04_视觉与插画/`
"""
    (REPO / "10_视觉与插画规范").mkdir(exist_ok=True)
    (REPO / "10_视觉与插画规范" / "README.md").write_text(stub, encoding="utf-8")


def main() -> int:
    items = collect_rule_files()
    print(f"Collect V1.0 rules: {len(items)}")
    manifest = pack_rules(items)
    removed_md = delete_process_md()
    print(f"Removed process MD: {len(removed_md)}")
    deleted_dirs = delete_dirs()
    print(f"Deleted dirs: {len([d for d in deleted_dirs if d.startswith('DELETED')])}")
    write_index(manifest, deleted_dirs, removed_md)

    # Update vol1 navigation stub
    nav_stub = VOL1 / "V2迁移_README_已清除.md"
    nav_stub.write_text(
        f"""# V2迁移 · 已清除

> 过程报告文件夹已删除 · **V1.0 规范** 见 [`11_规则与规范/00_总索引_V1.0.md`](../../11_规则与规范/00_总索引_V1.0.md)  
> 日期：{date.today().isoformat()}
""",
        encoding="utf-8",
    )
    print(f"INDEX: {RULES_ROOT / '00_总索引_V1.0.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
