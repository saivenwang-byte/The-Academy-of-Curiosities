#!/usr/bin/env python3
"""Reorganize Unit1 into A001–A005 per-case folders with archive + compatibility shims."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # 第1卷_觉得奇怪就先观察
UNIT = ROOT / "单元1_第一单元_五案"
THIN = ROOT / "薄样张_试读"
DESIGN = Path(r"D:\【AI Project】\【The Academy of Curiosities】\07_设计原档\04_样章视觉")

CN_VER = "V3.1"
JP_VER = "V3.8"
ILL_VER = "V3.6"

CASES = [
    ("A001", "01", "全班都听见了他的声音"),
    ("A002", "02", "没有人写过的道歉"),
    ("A003", "03", "每个人都记得的海报"),
    ("A004", "04", "只出现在她抽屉里的失物"),
    ("A005", "05", "午休后消失的影子"),
]

ACTIVE_UNIT = "A001"
ACTIVE_PHASE = "样张"  # 样张 | 排版

LOG: list[str] = []


def log(msg: str) -> None:
    LOG.append(msg)
    print(msg)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def try_hardlink(src: Path, dst: Path) -> bool:
    ensure_dir(dst.parent)
    if dst.exists() or dst.is_symlink():
        return True
    try:
        os.link(src, dst)
        log(f"  HARDLINK: {dst.relative_to(UNIT)}")
        return True
    except OSError:
        return False


def try_junction(src: Path, dst: Path) -> bool:
    """Windows directory junction via mklink /J."""
    if dst.exists():
        if dst.is_dir() and not any(dst.iterdir()):
            dst.rmdir()
        else:
            return True
    ensure_dir(dst.parent)
    cmd = ["cmd", "/c", "mklink", "/J", str(dst), str(src)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        log(f"  JUNCTION: {dst.relative_to(UNIT)} -> {src.relative_to(UNIT)}")
        return True
    log(f"  JUNCTION-FAIL: {dst} ({r.stderr.strip()})")
    return False


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        log(f"  SKIP-MISSING: {src}")
        return
    ensure_dir(dst.parent)
    if dst.exists():
        return
    shutil.copy2(src, dst)
    log(f"  COPY: {src.name} -> {dst.relative_to(UNIT)}")


def move_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        log(f"  MOVE-SKIP-EXISTS: {dst}")
        return
    ensure_dir(dst.parent)
    shutil.move(str(src), str(dst))
    log(f"  MOVE-DIR: {src.relative_to(UNIT)} -> {dst.relative_to(UNIT)}")


def move_tree_contents(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    ensure_dir(dst)
    for item in src.iterdir():
        target = dst / item.name
        if target.exists():
            continue
        shutil.move(str(item), str(target))
        log(f"  MOVE: {item.name} -> {target.relative_to(UNIT)}")


def body_cn_path(case_num: str, title: str) -> Path:
    return UNIT / "正文" / CN_VER / "01_中文" / f"案{case_num}_{title}_HybridVoice_{CN_VER}.txt"


def body_jp_path(case_num: str, title: str) -> Path:
    return UNIT / "正文" / JP_VER / "02_日本語" / f"案{case_num}_{title}_HybridVoice_{JP_VER}_日本語.txt"


def create_case_skeleton(case_id: str, case_num: str, title: str) -> Path:
    base = UNIT / case_id
    for sub in ("01_正文", "02_分镜头", "03_插画", "04_样张", "05_排版", "_archive"):
        ensure_dir(base / sub)
    return base


def populate_canonical_body(case_id: str, case_num: str, title: str) -> None:
    base = UNIT / case_id / "01_正文"
    cn_src = body_cn_path(case_num, title)
    jp_src = body_jp_path(case_num, title)
    cn_dst = base / f"案{case_num}_{title}_HybridVoice_{CN_VER}.txt"
    jp_dst = base / f"案{case_num}_{title}_HybridVoice_{JP_VER}_日本語.txt"
    copy_file(cn_src, cn_dst)
    copy_file(jp_src, jp_dst)

    # version opinions copied later in copy_case_opinions()


def populate_illustrations(case_id: str) -> None:
    """Move active illustration bind folder into case; leave junction at old path."""
    old_bind = UNIT / "插图" / f"绑定正文_{ILL_VER}" / case_id
    new_ill = UNIT / case_id / "03_插画"
    has_content = new_ill.exists() and any(new_ill.iterdir())
    if old_bind.exists() and not has_content:
        move_tree_contents(old_bind, new_ill)
        ensure_dir(old_bind)
        try_junction(new_ill, old_bind)

    # compressed trial images
    old_comp = UNIT / "插图" / f"绑定正文_{ILL_VER}_试读压缩" / case_id
    new_comp = UNIT / case_id / "04_样张" / "插图压缩"
    if old_comp.exists():
        move_tree_contents(old_comp, new_comp)
        ensure_dir(old_comp)
        try_junction(new_comp, old_comp)


def populate_storyboard(case_id: str, case_num: str) -> None:
    sb_unit = UNIT / "正文" / "V3.6" / "04_分镜插画" / case_id
    sb_design = DESIGN / "分镜拆解" / f"{case_id}_分镜拆解_R17_V0.1.md"
    dst = UNIT / case_id / "02_分镜头"
    if sb_unit.exists():
        move_tree_contents(sb_unit, dst)
    if sb_design.exists():
        copy_file(sb_design, dst / sb_design.name)


def populate_sample_a001() -> None:
    """A001-only trial sheet materials."""
    dst = UNIT / "A001" / "04_样张"
    pilots = [
        THIN / "E20_pilot_A001_V3.8_20260609",
        THIN / "E20_pilot_A001_20260608",
        THIN / "A001_E20",
    ]
    for src in pilots:
        if not src.exists():
            continue
        target = dst / src.name
        if target.exists():
            continue
        shutil.copytree(src, target)
        log(f"  COPYTREE: {src.name} -> A001/04_样张/")


def copy_case_opinions() -> None:
    """After body archive, scatter version opinions into per-case _archive."""
    archive_body = UNIT / "_archive_正文版本" / "正文_历史按版本号"
    if not archive_body.exists():
        return
    for case_id, case_num, _title in CASES:
        dst = UNIT / case_id / "01_正文" / "_archive"
        for ver_dir in archive_body.glob("*/03_版本意见"):
            if not ver_dir.is_dir():
                continue
            for f in ver_dir.glob(f"*{case_id}*"):
                copy_file(f, dst / f.name)
            for f in ver_dir.glob(f"*案{case_num}_*"):
                copy_file(f, dst / f.name)


def archive_old_body_tree() -> None:
    old_body = UNIT / "正文"
    archive_root = UNIT / "_archive_正文版本" / "正文_历史按版本号"
    if old_body.exists() and not archive_root.exists():
        move_dir(old_body, archive_root)
    elif old_body.exists() and archive_root.exists():
        # merge any remaining
        for item in old_body.iterdir():
            target = archive_root / item.name
            if not target.exists():
                shutil.move(str(item), str(target))
                log(f"  MERGE-BODY: {item.name}")
        if not any(old_body.iterdir()):
            old_body.rmdir()


def archive_old_illustration_bindings() -> None:
    ill_root = UNIT / "插图"
    archive = UNIT / "_archive_插图绑定"
    ensure_dir(archive)
    if not ill_root.exists():
        return
    for item in list(ill_root.iterdir()):
        if item.name.startswith("绑定正文_") and item.is_dir():
            # skip active V3.6 case junctions - only top-level bind folders
            if item.name == f"绑定正文_{ILL_VER}":
                # keep shell; per-case are junctions
                continue
            if item.name == f"绑定正文_{ILL_VER}_试读压缩":
                continue
            target = archive / item.name
            if not target.exists():
                move_dir(item, target)
    # archive V2.0 entirely if still at top level
    v20 = ill_root / "绑定正文_V2.0"
    if v20.exists() and v20.is_dir() and not (archive / "绑定正文_V2.0").exists():
        move_dir(v20, archive / "绑定正文_V2.0")


def rebuild_compatibility_shims() -> None:
    """Recreate tool-expected paths as hardlinks/junctions to per-case canonical."""
    body_cn = UNIT / "正文" / CN_VER / "01_中文"
    body_jp = UNIT / "正文" / JP_VER / "02_日本語"
    ill_bind = UNIT / "插图" / f"绑定正文_{ILL_VER}"
    ill_comp = UNIT / "插图" / f"绑定正文_{ILL_VER}_试读压缩"
    ensure_dir(body_cn)
    ensure_dir(body_jp)
    ensure_dir(ill_bind)
    ensure_dir(ill_comp)

    archive_body = UNIT / "_archive_正文版本" / "正文_历史按版本号"

    for case_id, case_num, title in CASES:
        cn_name = f"案{case_num}_{title}_HybridVoice_{CN_VER}.txt"
        jp_name = f"案{case_num}_{title}_HybridVoice_{JP_VER}_日本語.txt"
        canon_cn = UNIT / case_id / "01_正文" / cn_name
        canon_jp = UNIT / case_id / "01_正文" / jp_name

        if canon_cn.exists():
            if not try_hardlink(canon_cn, body_cn / cn_name):
                copy_file(canon_cn, body_cn / cn_name)
        if canon_jp.exists():
            if not try_hardlink(canon_jp, body_jp / jp_name):
                copy_file(canon_jp, body_jp / jp_name)

        ill_case = UNIT / case_id / "03_插画"
        if ill_case.exists():
            try_junction(ill_case, ill_bind / case_id)
        comp_case = UNIT / case_id / "04_样张" / "插图压缩"
        if comp_case.exists():
            try_junction(comp_case, ill_comp / case_id)

    # restore archived version trees under 正文/ for tools that reference V3.6 etc.
    if archive_body.exists():
        for ver in ("V3.6", "V3.7", "V3.8"):
            src = archive_body / ver
            dst = UNIT / "正文" / ver
            if src.exists() and not dst.exists():
                try_junction(src, dst)


def write_stub(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")
    log(f"  STUB: {path.relative_to(ROOT)}")


def write_navigation_docs() -> None:
    today = date.today().isoformat()

    unit_nav = UNIT / "00_单元导航.md"
    unit_nav.write_text(
        f"""# 第一单元 · 单元导航（A001–A005）

> **工作流 LOCK（2026-06-09）**：一案一案做 · **样张完成 → 排版** · 禁止五案批量并行  
> **当前活跃单元**：**{ACTIVE_UNIT}** · 阶段：**{ACTIVE_PHASE}**  
> 更新：{today}

## 五案入口

| 案 | 文件夹 | 中文正典 | 日文正典 | 阶段 |
|----|--------|----------|----------|------|
| A1 | [`A001/`](./A001/00_正典指针.md) | CN {CN_VER} | JP {JP_VER} | **ACTIVE · 样张** |
| A2 | [`A002/`](./A002/00_正典指针.md) | CN {CN_VER} | JP {JP_VER} | 等待 A001 样张 PASS |
| A3 | [`A003/`](./A003/00_正典指针.md) | CN {CN_VER} | JP {JP_VER} | 等待 |
| A4 | [`A004/`](./A004/00_正典指针.md) | CN {CN_VER} | JP {JP_VER} | 等待 |
| A5 | [`A005/`](./A005/00_正典指针.md) | CN {CN_VER} | JP {JP_VER} | 等待 |

## 单案文件夹结构

```
A00X/
├── 00_正典指针.md      ← 本案版本 SSOT
├── 01_正文/            ← 中文 + 日本語 正典稿
├── 02_分镜头/          ← 分镜拆解、场表
├── 03_插画/            ← prompts + 成图 + 清单
├── 04_样张/            ← 试读 PDF、E20 pilot、压缩图
├── 05_排版/            ← 样张签字后才开工
└── _archive/           ← 本案历史迭代
```

## 工作流程（必读）

1. **Phase 1 · 样张**（仅活跃单元）：正文锁版 → 分镜 → 插画 → 试读 PDF → E20/读者验收  
2. **Phase 2 · 排版**：样张 PASS 后，在 `05_排版/` 做全页排版  
3. **禁止**：在 A001 样张未 PASS 前启动 A002 插画/样张/排版  
4. **禁止**：五案批量出图、批量 PDF、全自动 `--full-auth` 跨案流水线

详细规则 → [`00_Agent工作流规则.md`](./00_Agent工作流规则.md)  
文件夹说明 → [`00_文件夹说明.md`](./00_文件夹说明.md)

## 卷级共享（非单案）

| 用途 | 路径 |
|------|------|
| V2 迁移报告 | [`../V2迁移/`](../V2迁移/) |
| 卷级试读工具 | [`../薄样张_试读/`](../薄样张_试读/README.md) |
| 设计原档（画风/L0） | [`../../../07_设计原档/04_样章视觉/`](../../../07_设计原档/04_样章视觉/) |
| 历史正文（按版本号） | [`_archive_正文版本/`](./_archive_正文版本/) |
| 历史插图绑定 | [`_archive_插图绑定/`](./_archive_插图绑定/) |
| 流水线工具 | [`../tools/`](../tools/) |

## 兼容旧路径（工具用）

| 旧路径 | 指向 |
|--------|------|
| `正文/{CN_VER}/01_中文/` | 五案正典 hardlink |
| `正文/{JP_VER}/02_日本語/` | 五案正典 hardlink |
| `插图/绑定正文_{ILL_VER}/A00X/` | junction → `A00X/03_插画/` |
""",
        encoding="utf-8",
    )
    log(f"  DOC: {unit_nav.name}")

    folder_doc = UNIT / "00_文件夹说明.md"
    folder_doc.write_text(
        f"""# 第一单元 · 文件夹说明

更新：{today}

## 设计原则

1. **按案（A001–A005）组织**，不再按 `正文/V3.x` 横向堆版本号  
2. **一案一路径**：写作、分镜、插画、样张、排版都在同一 `A00X/` 下  
3. **版本号只留指针**：每案 `00_正典指针.md` 写明 CN/JP/插图版本；历史进 `_archive`  
4. **卷级归档**：`_archive_正文版本/`、`_archive_插图绑定/` 存放旧结构，不删文件  
5. **兼容层**：`正文/`、`插图/绑定正文_*` 保留 junction/hardlink 供 PDF 脚本使用

## 顶层一览

```
单元1_第一单元_五案/
├── 00_单元导航.md           ← 入口（工作流 + 五案表）
├── 00_文件夹说明.md         ← 本文件
├── 00_Agent工作流规则.md    ← Agent 禁令与阶段
├── 00_版本导航.md           ← 兼容旧链接（指向新结构）
├── 00_单元说明/             ← 单元级说明（保留）
├── A001/ … A005/            ← ★ 主工作区
├── _archive_正文版本/       ← 旧 正文/V1.1…V3.8 整树
├── _archive_插图绑定/       ← 旧 绑定正文_V2.0 等
├── 正文/                    ← 工具兼容 shim（hardlink）
└── 插图/                    ← 工具兼容 shim（junction）
```

## 各子文件夹职责

| 子目录 | 内容 | 何时写入 |
|--------|------|----------|
| `01_正文/` | 中文 + 日本語正典 `.txt` | 正文锁版时 |
| `02_分镜头/` | 分镜拆解 md、场级插画地图 | 正文后、出图前 |
| `03_插画/` | prompts、成图 PNG、`00_插图清单` | 样张阶段 |
| `04_样张/` | E20 pilot、试读 PDF、压缩插图 | 样张阶段 |
| `05_排版/` | 全页排版稿、印刷 PDF | **样张 PASS 后** |
| `_archive/` | 本案废弃稿 | 迭代时 |

## 旧路径对照

| 旧位置 | 新位置 |
|--------|--------|
| `正文/V3.1/01_中文/案01_…` | `A001/01_正文/案01_…` |
| `正文/V3.8/02_日本語/案01_…` | `A001/01_正文/案01_…_日本語` |
| `插图/绑定正文_V3.6/A001/` | `A001/03_插画/` |
| `薄样张_试读/E20_pilot_A001_V3.8_…` | `A001/04_样张/E20_pilot_A001_V3.8_…`（副本） |
| `07_设计原档/04_样章视觉/分镜拆解/A001_…` | 复制到 `A001/02_分镜头/` |

## 不要做的事

- 不要在根下新建 `正文/V3.9` 横向文件夹；新版本写在 `A00X/01_正文/_archive/` + 更新指针  
- 不要跨 A001–A005 批量跑插画或 PDF  
- 不要删除 `_archive_*` 内文件
""",
        encoding="utf-8",
    )

    agent_rules = UNIT / "00_Agent工作流规则.md"
    agent_rules.write_text(
        f"""# Agent 工作流规则 · 第一单元

> **强制执行** · 违反 = 浪费算力 + 无效交付  
> 更新：{today}

## 核心规则：一案一时

| # | 规则 |
|---|------|
| R1 | 同时只 **ACTIVE** 一个单元文件夹（当前：**{ACTIVE_UNIT}**） |
| R2 | **Phase 1 样张** 做完并 PASS 后，才进入 **Phase 2 排版** |
| R3 | A001 样张未 PASS → **禁止** A002–A005 的插画、样张、排版 |
| R4 | **禁止** 五案批量：批量出图、批量日译、批量 PDF、`vol1_auto_pipeline --full-auth` 跨案 |
| R5 | 新版本写入 `A00X/对应子目录`，更新 `00_正典指针.md`，旧文件进 `_archive/` |

## Phase 1 · 样张（单案）

```
01_正文 锁版 → 02_分镜头 → 03_插画（本案 only）→ 04_样张（试读 PDF）→ 验收
```

验收门：E20 / 读者试读 / PRODUCT-GATE 清单

## Phase 2 · 排版（单案）

前置：本案 `04_样张/` 已签字  
产出：`05_排版/` 全页排版 PDF

## 活跃单元切换条件

- A001 `04_样张/` PASS → 更新 `00_单元导航.md` 活跃单元为 A002  
- 以此类推 A003 → A004 → A005

## 工具调用

| 工具 | 适用范围 |
|------|----------|
| `build_a001_e20_pilot_pdf.py` | 仅 A001 |
| `build_unit1_trial_pdf.py` | **暂停** 五案批量；单案 PDF 待拆 |
| `vol1_auto_pipeline/run.py` | **禁止** `--full-auth` 跨案；仅 DESK/KIDS 等文稿步骤可按案调用 |

## 读路径顺序

1. `A00X/00_正典指针.md`  
2. `A00X/01_正文/`  
3. `00_单元导航.md`
""",
        encoding="utf-8",
    )

    # per-case pointer
    for case_id, case_num, title in CASES:
        status = "ACTIVE · 样张" if case_id == ACTIVE_UNIT else "WAIT · A001 样张未 PASS"
        ptr = UNIT / case_id / "00_正典指针.md"
        ptr.write_text(
            f"""# {case_id} · 正典指针

> 案{case_num}：{title}  
> 状态：**{status}**  
> 更新：{today}

## 当前正典版本

| 轨 | 版本 | 文件 |
|----|------|------|
| 中文 | {CN_VER} | [`01_正文/案{case_num}_{title}_HybridVoice_{CN_VER}.txt`](./01_正文/案{case_num}_{title}_HybridVoice_{CN_VER}.txt) |
| 日本語 | {JP_VER} | [`01_正文/案{case_num}_{title}_HybridVoice_{JP_VER}_日本語.txt`](./01_正文/案{case_num}_{title}_HybridVoice_{JP_VER}_日本語.txt) |
| 插图 | {ILL_VER} USERSTYLE | [`03_插画/`](./03_插画/) |

## 工作阶段

| 阶段 | 目录 | 状态 |
|------|------|------|
| 样张 | `04_样张/` | {"进行中" if case_id == ACTIVE_UNIT else "未启动"} |
| 排版 | `05_排版/` | 等待样张 PASS |

## 导航

- 单元入口：[`../00_单元导航.md`](../00_单元导航.md)
- Agent 规则：[`../00_Agent工作流规则.md`](../00_Agent工作流规则.md)
""",
            encoding="utf-8",
        )

    # update old version nav
    old_nav = UNIT / "00_版本导航.md"
    old_nav.write_text(
        f"""# 第一单元 · 版本导航（兼容入口）

> ⚠️ **结构已迁移**（{today}）→ 请用 [`00_单元导航.md`](./00_单元导航.md)  
> 旧「按版本号横向文件夹」已归档至 [`_archive_正文版本/`](./_archive_正文版本/)

## 当前正典（按案）

| 案 | 路径 | CN | JP |
|----|------|----|----|
| A001 | [`A001/`](./A001/00_正典指针.md) | {CN_VER} | {JP_VER} |
| A002 | [`A002/`](./A002/00_正典指针.md) | {CN_VER} | {JP_VER} |
| A003 | [`A003/`](./A003/00_正典指针.md) | {CN_VER} | {JP_VER} |
| A004 | [`A004/`](./A004/00_正典指针.md) | {CN_VER} | {JP_VER} |
| A005 | [`A005/`](./A005/00_正典指针.md) | {CN_VER} | {JP_VER} |

## 历史版本

全部在 [`_archive_正文版本/正文_历史按版本号/`](./_archive_正文版本/正文_历史按版本号/)（V1.1 … {JP_VER}）

## 工作流

**样张 → 排版 · 一案一时** → [`00_Agent工作流规则.md`](./00_Agent工作流规则.md)
""",
        encoding="utf-8",
    )

    # vol entry
    vol_nav = ROOT / "00_版本导航_卷入口.md"
    vol_nav.write_text(
        f"""# 第1卷 · 版本导航（卷入口）

> **结构已迁移至按案文件夹**（{today}）  
> SSOT：[`单元1_第一单元_五案/00_单元导航.md`](./单元1_第一单元_五案/00_单元导航.md)

| 要找什么 | 路径 |
|----------|------|
| **五案导航 + 工作流** | [`单元1/00_单元导航.md`](./单元1_第一单元_五案/00_单元导航.md) |
| **文件夹说明** | [`单元1/00_文件夹说明.md`](./单元1_第一单元_五案/00_文件夹说明.md) |
| **Agent 规则** | [`单元1/00_Agent工作流规则.md`](./单元1_第一单元_五案/00_Agent工作流规则.md) |
| **当前活跃单元** | [`A001/`](./单元1_第一单元_五案/A001/00_正典指针.md) |
| V2 迁移 | [`V2迁移/`](./V2迁移/) |
| 卷级试读 | [`薄样张_试读/`](./薄样张_试读/README.md) |

**旧路径** `正式版/01_正文/` · `单元1/正文/Vx.y/`（横向版本）→ 见各目录 README 指向新位置。
""",
        encoding="utf-8",
    )


def write_stubs() -> None:
    stubs = {
        UNIT / "正文" / "README.md": (
            f"# 正文 · 兼容层\n\n"
            f"正典已迁至 **`A001/`–`A005/01_正文/`**。\n\n"
            f"- 导航：[`../00_单元导航.md`](../00_单元导航.md)\n"
            f"- 历史版本：[`../_archive_正文版本/`](../_archive_正文版本/)\n\n"
            f"本目录保留 **hardlink/junction** 供 `tools/build_*_pdf.py` 使用。\n"
        ),
        UNIT / "插图" / "README.md": (
            f"# 插图 · 兼容层\n\n"
            f"正典已迁至 **`A001/`–`A005/03_插画/`**。\n\n"
            f"- `绑定正文_{ILL_VER}/A00X/` → junction 到 `A00X/03_插画/`\n"
            f"- 历史：[`../_archive_插图绑定/`](../_archive_插图绑定/)\n"
        ),
        THIN / "README.md": (
            "# 薄样张_试读 · 卷级试读\n\n"
            "> 单案样张材料优先放在 `单元1_第一单元_五案/A00X/04_样张/`\n\n"
            "本目录保留卷级工具（読者百景、GateA MVP、问卷模板）。\n\n"
            "| 单案 | 新路径 |\n|------|--------|\n"
            "| A001 E20 pilot | [`../单元1_第一单元_五案/A001/04_样张/`](../单元1_第一单元_五案/A001/04_样张/) |\n"
        ),
        ROOT / "正式版" / "README.md": (
            "# 正式版 · 已弃用\n\n"
            "正文正典 → [`../单元1_第一单元_五案/A001/`](../单元1_第一单元_五案/00_单元导航.md)（按案）\n"
        ),
    }
    for path, content in stubs.items():
        if path.exists() and path.name == "README.md":
            # merge if thin sample readme exists - overwrite with pointer header
            pass
        write_stub(path, content)


def write_report() -> None:
    report = ROOT / "V2迁移" / "103_单元1_A001-A005按案重组报告_V0.1.md"
    ensure_dir(report.parent)
    report.write_text(
        "# 单元1 · A001–A005 按案重组报告 V0.1\n\n"
        f"日期：{date.today().isoformat()}\n\n"
        "## 新结构根\n\n"
        "`单元1_第一单元_五案/A001/` … `A005/`\n\n"
        "## 操作日志\n\n"
        + "\n".join(f"- {line}" for line in LOG)
        + "\n",
        encoding="utf-8",
    )
    log(f"  REPORT: {report.name}")

    manifest = UNIT / "_reorganize_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "active_unit": ACTIVE_UNIT,
                "canonical": {"cn": CN_VER, "jp": JP_VER, "illustration": ILL_VER},
                "cases": [c[0] for c in CASES],
                "log_count": len(LOG),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    log("=== Unit1 reorganization: A001–A005 ===")

    # 1. skeleton
    for case_id, case_num, title in CASES:
        create_case_skeleton(case_id, case_num, title)

    # 2. populate canonical from existing body (before archive move)
    for case_id, case_num, title in CASES:
        populate_canonical_body(case_id, case_num, title)

    # 3. illustrations + storyboards (before archive)
    for case_id, case_num, title in CASES:
        populate_illustrations(case_id)
        populate_storyboard(case_id, case_num)

    populate_sample_a001()

    # 4. archive old trees
    archive_old_illustration_bindings()
    archive_old_body_tree()
    copy_case_opinions()

    # 5. compatibility shims
    rebuild_compatibility_shims()

    # 6. docs + stubs
    write_navigation_docs()
    write_stubs()
    write_report()

    log(f"=== Done. {len(LOG)} operations ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
