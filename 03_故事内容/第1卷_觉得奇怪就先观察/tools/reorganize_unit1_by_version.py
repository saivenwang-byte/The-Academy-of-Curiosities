#!/usr/bin/env python3
"""Reorganize Unit1 body text + illustrations into versioned folder structure."""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # 第1卷_觉得奇怪就先观察
OLD_BODY = ROOT / "正式版" / "01_正文"
NEW_UNIT = ROOT / "单元1_第一单元_五案"
OLD_ILLUST = ROOT / "样章包" / "插图"
NEW_ILLUST = NEW_UNIT / "插图"

CURRENT_VERSION = "V3.1"

# --- file routing: (source glob pattern relative to OLD_BODY, version, subdir) ---
# subdir: cn | jp | opinion

MANIFEST: list[tuple[str, str, str]] = [
    # V1.1 旧案题 · 定稿
    ("案02_错位的泥印_HybridVoice_V1.1定稿.txt", "V1.1", "cn"),
    ("案02_ずれた泥のあと_V1.1定稿_日本語.txt", "V1.1", "jp"),
    ("案03_空着的那一栏_HybridVoice_V1.1定稿.txt", "V1.1", "cn"),
    ("案03_空いているマス_V1.1定稿_日本語.txt", "V1.1", "jp"),
    ("案04_粉笔灰的圆圈_HybridVoice_V1.1定稿.txt", "V1.1", "cn"),
    ("案04_チョークの粉の輪_V1.1定稿_日本語.txt", "V1.1", "jp"),
    ("案05_橡皮屑的方向_HybridVoice_V1.1定稿.txt", "V1.1", "cn"),
    ("案05_消しゴムの屑の向き_V1.1定稿_日本語.txt", "V1.1", "jp"),
    # V1.2 文学重写（CN only · 旧案题）
    ("案02_错位的泥印_HybridVoice_V1.2文学重写.txt", "V1.2", "cn"),
    ("案03_空着的那一栏_HybridVoice_V1.2文学重写.txt", "V1.2", "cn"),
    ("案04_粉笔灰的圆圈_HybridVoice_V1.2文学重写.txt", "V1.2", "cn"),
    ("案05_橡皮屑的方向_HybridVoice_V1.2文学重写.txt", "V1.2", "cn"),
    # V2.0
    ("案01_全班都听见了他的声音_HybridVoice_V2.0.txt", "V2.0", "cn"),
    ("案01_全班都听见了他的声音_HybridVoice_V2.0_日本語.txt", "V2.0", "jp"),
    ("案01_全班都听见了他的声音_HybridVoice_V2.0_R16_globalIP.md", "V2.0", "opinion"),
    ("案01_全班都听见了他的声音_HybridVoice_V2.0_R17_M1M2.md", "V2.0", "opinion"),
    ("案02_没有人写过的道歉_HybridVoice_V2.0.txt", "V2.0", "cn"),
    ("案02_没有人写过的道歉_HybridVoice_V2.0_日本語.txt", "V2.0", "jp"),
    ("案02_没有人写过的道歉_HybridVoice_V2.0_R16_globalIP.md", "V2.0", "opinion"),
    ("案02_没有人写过的道歉_HybridVoice_V2.0_R17_M1M2.md", "V2.0", "opinion"),
    ("案03_每个人都记得的海报_HybridVoice_V2.0.txt", "V2.0", "cn"),
    ("案03_每个人都记得的海报_HybridVoice_V2.0_日本語.txt", "V2.0", "jp"),
    ("案03_每个人都记得的海报_HybridVoice_V2.0_R16_globalIP.md", "V2.0", "opinion"),
    ("案03_每个人都记得的海报_HybridVoice_V2.0_R17_M1M2.md", "V2.0", "opinion"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt", "V2.0", "cn"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V2.0_日本語.txt", "V2.0", "jp"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V2.0_R16_globalIP.md", "V2.0", "opinion"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V2.0_R17_M1M2.md", "V2.0", "opinion"),
    ("案05_午休后消失的影子_HybridVoice_V2.0.txt", "V2.0", "cn"),
    ("案05_午休后消失的影子_HybridVoice_V2.0_日本語.txt", "V2.0", "jp"),
    ("案05_午休后消失的影子_HybridVoice_V2.0_R16_globalIP.md", "V2.0", "opinion"),
    ("案05_午休后消失的影子_HybridVoice_V2.0_R17_M1M2.md", "V2.0", "opinion"),
    # V2.1（A001 M-cut · 其余案同 V2.0 稍后补拷贝）
    ("案01_全班都听见了他的声音_HybridVoice_V2.1.txt", "V2.1", "cn"),
    ("案01_全班都听见了他的声音_HybridVoice_V2.1_日本語.txt", "V2.1", "jp"),
    ("案01_全班都听见了他的声音_HybridVoice_V2.1_R18_Mcut.md", "V2.1", "opinion"),
    ("案01_全班都听见了他的声音_A001_制作元数据.md", "V2.1", "opinion"),
    ("案01_全班都听见了他的声音_A001_卷末实验与FAQ.md", "V2.1", "opinion"),
    # V3.0
    ("案01_全班都听见了他的声音_HybridVoice_V3.0.txt", "V3.0", "cn"),
    ("案01_全班都听见了他的声音_HybridVoice_V3.0_日本語.txt", "V3.0", "jp"),
    ("案01_全班都听见了他的声音_V3.0_meta.md", "V3.0", "opinion"),
    ("案01_全班都听见了他的声音_V3.0_日本語_meta.md", "V3.0", "opinion"),
    ("案02_没有人写过的道歉_HybridVoice_V3.0.txt", "V3.0", "cn"),
    ("案02_没有人写过的道歉_HybridVoice_V3.0_日本語.txt", "V3.0", "jp"),
    ("案02_没有人写过的道歉_V3.0_meta.md", "V3.0", "opinion"),
    ("案03_每个人都记得的海报_HybridVoice_V3.0.txt", "V3.0", "cn"),
    ("案03_每个人都记得的海报_HybridVoice_V3.0_日本語.txt", "V3.0", "jp"),
    ("案03_每个人都记得的海报_V3.0_meta.md", "V3.0", "opinion"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V3.0.txt", "V3.0", "cn"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V3.0_日本語.txt", "V3.0", "jp"),
    ("案04_只出现在她抽屉里的失物_V3.0_meta.md", "V3.0", "opinion"),
    ("案05_午休后消失的影子_HybridVoice_V3.0.txt", "V3.0", "cn"),
    ("案05_午休后消失的影子_HybridVoice_V3.0_日本語.txt", "V3.0", "jp"),
    ("案05_午休后消失的影子_V3.0_meta.md", "V3.0", "opinion"),
    # V3.1 CURRENT
    ("案01_全班都听见了他的声音_HybridVoice_V3.1.txt", "V3.1", "cn"),
    ("案01_全班都听见了他的声音_HybridVoice_V3.1_日本語.txt", "V3.1", "jp"),
    ("案01_全班都听见了他的声音_V3.1_meta.md", "V3.1", "opinion"),
    ("案02_没有人写过的道歉_HybridVoice_V3.1.txt", "V3.1", "cn"),
    ("案02_没有人写过的道歉_HybridVoice_V3.1_日本語.txt", "V3.1", "jp"),
    ("案02_没有人写过的道歉_V3.1_meta.md", "V3.1", "opinion"),
    ("案03_每个人都记得的海报_HybridVoice_V3.1.txt", "V3.1", "cn"),
    ("案03_每个人都记得的海报_HybridVoice_V3.1_日本語.txt", "V3.1", "jp"),
    ("案03_每个人都记得的海报_V3.1_meta.md", "V3.1", "opinion"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V3.1.txt", "V3.1", "cn"),
    ("案04_只出现在她抽屉里的失物_HybridVoice_V3.1_日本語.txt", "V3.1", "jp"),
    ("案04_只出现在她抽屉里的失物_V3.1_meta.md", "V3.1", "opinion"),
    ("案05_午休后消失的影子_HybridVoice_V3.1.txt", "V3.1", "cn"),
    ("案05_午休后消失的影子_HybridVoice_V3.1_日本語.txt", "V3.1", "jp"),
    ("案05_午休后消失的影子_V3.1_meta.md", "V3.1", "opinion"),
]

UNIT_DOCS = [
    ("00_第一单元_V2_中文正文_阅读索引.md", "00_单元说明/00_阅读索引.md"),
    ("README_两轨说明_V0.1.md", "00_单元说明/README_两轨说明_V0.1.md"),
    ("00_第一单元_V2_Voice归一化摘要_V0.1.md", "00_单元说明/00_Voice归一化摘要_V0.1.md"),
    ("00_GPT_LOCK补丁_专家组复评_V0.1.md", "00_单元说明/00_GPT_LOCK补丁_专家组复评_V0.1.md"),
]

V21_COPY_FROM_V20 = [
    ("案02_没有人写过的道歉", "A002"),
    ("案03_每个人都记得的海报", "A003"),
    ("案04_只出现在她抽屉里的失物", "A004"),
    ("案05_午休后消失的影子", "A005"),
]

SUBDIR_MAP = {"cn": "01_中文", "jp": "02_日本語", "opinion": "03_版本意见"}

ILLUST_CASE_MAP = {
    "V-S01": "A001",
    "V-S02": "A002",
    "V-S03": "A003",
    "V-S04": "A004",
    "V-S05": "A005",
}

VERSION_NOTES = {
    "V1.1": "旧案题（错位的泥印等）· 定稿 + 部分日译 · 五案结构尚未统一为 V2 案号",
    "V1.2": "旧案题 · 文学重写（CN）· 无 A001 · 无日译",
    "V2.0": "五案 V2 结构确立 · HybridVoice · R16/R17 评审意见",
    "V2.1": "A001 M-cut 减法 · A002–A005 正文同 V2.0（本文件夹内已拷贝）",
    "V3.0": "HybridVoice 全卷重写 · meta 外置 · CN+JP 同步",
    "V3.1": "**当前工作稿** · doc81 真人编辑文字层补丁 · MoA-lite JP",
}


def ensure_dirs() -> None:
    for ver in VERSION_NOTES:
        for sub in SUBDIR_MAP.values():
            (NEW_UNIT / "正文" / ver / sub).mkdir(parents=True, exist_ok=True)
    (NEW_UNIT / "00_单元说明").mkdir(parents=True, exist_ok=True)
    for ver in ("V2.0", "V3.1"):
        for case in ILLUST_CASE_MAP.values():
            (NEW_ILLUST / f"绑定正文_{ver}" / case).mkdir(parents=True, exist_ok=True)
    (NEW_ILLUST / "绑定正文_V3.1").mkdir(parents=True, exist_ok=True)


def move_body_files() -> list[str]:
    log: list[str] = []
    for fname, ver, kind in MANIFEST:
        src = OLD_BODY / fname
        if not src.exists():
            log.append(f"SKIP missing: {fname}")
            continue
        dst_dir = NEW_UNIT / "正文" / ver / SUBDIR_MAP[kind]
        dst = dst_dir / fname
        if dst.exists():
            log.append(f"EXISTS: {dst.relative_to(ROOT)}")
            continue
        shutil.move(str(src), str(dst))
        log.append(f"MOVE: {fname} -> {ver}/{SUBDIR_MAP[kind]}/")
    return log


def copy_v21_from_v20() -> None:
    v20 = NEW_UNIT / "正文" / "V2.0"
    v21 = NEW_UNIT / "正文" / "V2.1"
    for prefix, _ in V21_COPY_FROM_V20:
        for sub in ("01_中文", "02_日本語"):
            for f in (v20 / sub).glob(f"{prefix}_HybridVoice_V2.0*"):
                if f.suffix == ".md":
                    continue
                dst = v21 / sub / f.name.replace("V2.0", "V2.0")  # keep V2.0 in filename
                if not dst.exists():
                    shutil.copy2(f, dst)
    note = v21 / "03_版本意见" / "00_A002-A005_同V2.0说明.md"
    if not note.exists():
        note.write_text(
            "# V2.1 单元说明 · A002–A005\n\n"
            "本版本仅 **A001** 有 V2.1 M-cut 修订。\n\n"
            "A002–A005 正文与 **V2.0** 相同，拷贝存放于本文件夹 `01_中文`/`02_日本語`，"
            "文件名仍含 `V2.0` 后缀以便 diff。\n",
            encoding="utf-8",
        )


def move_unit_docs() -> None:
    for src_name, rel_dst in UNIT_DOCS:
        src = OLD_BODY / src_name
        dst = NEW_UNIT / rel_dst
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))


def write_version_readmes() -> None:
    today = date.today().isoformat()
    for ver, note in VERSION_NOTES.items():
        p = NEW_UNIT / "正文" / ver / "00_版本说明.md"
        current = " · **CURRENT**" if ver == CURRENT_VERSION else ""
        p.write_text(
            f"# 第一单元正文 · {ver}{current}\n\n"
            f"> 归档日期：{today}\n\n"
            f"## 版本摘要\n\n{note}\n\n"
            f"## 文件夹结构\n\n"
            f"| 子文件夹 | 内容 |\n|----------|------|\n"
            f"| `01_中文` | 中文 HybridVoice 正文 |\n"
            f"| `02_日本語` | 日文正文（写完 CN 后同步） |\n"
            f"| `03_版本意见` | meta · 评审 · 修订 changelog |\n\n"
            f"## 版本号规则\n\n"
            f"- **小修**（措辞/语法/JP glossary）：+0.1（如 V3.0→V3.1）\n"
            f"- **大修**（结构/机制/公平线索）：+1.0（如 V3.x→V4.0）\n",
            encoding="utf-8",
        )


def write_master_nav() -> None:
    nav = NEW_UNIT / "00_版本导航.md"
    lines = [
        "# 第一单元 · 版本导航 SSOT",
        "",
        f"> **当前正文版本**：`{CURRENT_VERSION}`",
        f"> **路径根**：`单元1_第一单元_五案/`",
        f"> 更新：{date.today().isoformat()}",
        "",
        "## 快速入口",
        "",
        f"| 用途 | 路径 |",
        f"|------|------|",
        f"| **当前中文五案** | [`正文/{CURRENT_VERSION}/01_中文/`](./正文/{CURRENT_VERSION}/01_中文/) |",
        f"| **当前日文五案** | [`正文/{CURRENT_VERSION}/02_日本語/`](./正文/{CURRENT_VERSION}/02_日本語/) |",
        f"| 阅读索引 | [`00_单元说明/00_阅读索引.md`](./00_单元说明/00_阅读索引.md) |",
        f"| 插图（绑定 V2.0） | [`插图/绑定正文_V2.0/`](./插图/绑定正文_V2.0/) |",
        "",
        "## 正文版本沿革",
        "",
        "| 版本 | 说明 | 中文 | 日文 | 意见 |",
        "|------|------|------|------|------|",
    ]
    for ver, note in VERSION_NOTES.items():
        cur = " **← CURRENT**" if ver == CURRENT_VERSION else ""
        base = f"./正文/{ver}"
        lines.append(
            f"| {ver}{cur} | {note.split('·')[0].strip()} | "
            f"[01_中文]({base}/01_中文/) | [02_日本語]({base}/02_日本語/) | [03_版本意见]({base}/03_版本意见/) |"
        )
    lines += [
        "",
        "## 插图版本规则",
        "",
        "1. **先锁正文版本**（如 V3.1）",
        "2. 在 `插图/绑定正文_V3.1/A00X/` 下按 DA 编号存放 prompt + 成图",
        "3. 插图文件夹名 **必须** 与正文版本号一致",
        "4. 日译跟进：正文 JP 定稿（J10）后再更新 SUM 页等插图内日文",
        "",
        "## 工作流",
        "",
        "```",
        "CN 修订 → 新建 Vx.y 文件夹 → JP 同步 → 03_版本意见 记录 → 锁版本 → 插图绑定同版本号",
        "```",
        "",
    ]
    nav.write_text("\n".join(lines), encoding="utf-8")


def reorganize_illustrations() -> list[str]:
    log: list[str] = []
    if not OLD_ILLUST.exists():
        return ["SKIP: old illustration folder missing"]

    bind_v20 = NEW_ILLUST / "绑定正文_V2.0"
    # depth_anchor + top-level case assets
    sources = list(OLD_ILLUST.glob("depth_anchor/*")) + [
        f for f in OLD_ILLUST.iterdir() if f.is_file()
    ]
    for src in sources:
        if src.is_dir():
            continue
        name = src.name
        case = None
        for prefix, c in ILLUST_CASE_MAP.items():
            if name.startswith(prefix):
                case = c
                break
        if not case:
            continue
        dst_dir = bind_v20 / case
        dst = dst_dir / name
        if dst.exists():
            continue
        shutil.copy2(src, dst)
        log.append(f"ILLUST copy: {name} -> V2.0/{case}/")

    # prompts at illust root
    for src in OLD_ILLUST.glob("prompts_*.md"):
        name = src.name
        case = "A001" if "V-S01" in name or "A001" in name else None
        if not case:
            for prefix, c in ILLUST_CASE_MAP.items():
                if prefix.replace("V-S0", "V-S0") in name or c in name:
                    case = c
                    break
        if not case:
            # split by V-S02 etc in content - fallback A001 shared
            m = re.search(r"V-S0([1-5])", name)
            if m:
                case = f"A00{m.group(1)}"
            else:
                case = "_共用"
        dst_dir = bind_v20 / case
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / name
        if not dst.exists():
            shutil.copy2(src, dst)
            log.append(f"ILLUST prompt: {name} -> V2.0/{case}/")

    # 样张确认
    sample_dir = OLD_ILLUST / "样张确认"
    if sample_dir.exists():
        for src in sample_dir.iterdir():
            if src.is_file():
                dst = bind_v20 / "A002" / src.name
                if not dst.exists():
                    shutil.copy2(src, dst)
                    log.append(f"ILLUST sample: {src.name} -> V2.0/A002/")

    # V3.1 placeholder
    v31_readme = NEW_ILLUST / "绑定正文_V3.1" / "00_待绑定说明.md"
    if not v31_readme.exists():
        for c in ILLUST_CASE_MAP.values():
            (NEW_ILLUST / "绑定正文_V3.1" / c).mkdir(parents=True, exist_ok=True)
        v31_readme.write_text(
            "# 插图 · 绑定正文 V3.1\n\n"
            "**状态**：待正文 V3.1 G-BODY 签核后启动分镜。\n\n"
            "流程：\n"
            "1. 确认 `正文/V3.1/` CN+JP 为插图 SSOT\n"
            "2. 按 A001–A005 子文件夹写入 prompts + 成图\n"
            "3. DA 编号与 SC 场号对齐 doc72\n",
            encoding="utf-8",
        )

    illust_nav = NEW_ILLUST / "00_插图版本导航.md"
    illust_nav.write_text(
        "# 插图 · 版本导航\n\n"
        "| 绑定正文版本 | 路径 | 状态 |\n|-------------|------|------|\n"
        "| V2.0 | [`绑定正文_V2.0/`](./绑定正文_V2.0/) | 样章/depth_anchor 已归类 |\n"
        "| V3.1 | [`绑定正文_V3.1/`](./绑定正文_V3.1/) | 待锁正文后开工 |\n\n"
        "## 案号对照\n\n"
        "| 案 | 插图前缀 |\n|:--:|----------|\n"
        "| A001 | V-S01 |\n| A002 | V-S02 |\n| A003 | V-S03 |\n| A004 | V-S04 |\n| A005 | V-S05 |\n",
        encoding="utf-8",
    )
    return log


def write_old_stub() -> None:
    stub = OLD_BODY / "README_已迁移至版本文件夹.md"
    stub.write_text(
        "# 01_正文 · 已迁移\n\n"
        "所有正文版本已迁入：\n\n"
        "```\n"
        "03_故事内容/第1卷_觉得奇怪就先观察/单元1_第一单元_五案/\n"
        "```\n\n"
        "**当前版本**：V3.1\n\n"
        "- 导航：[`../单元1_第一单元_五案/00_版本导航.md`](../单元1_第一单元_五案/00_版本导航.md)\n"
        "- 当前中文：[`../单元1_第一单元_五案/正文/V3.1/01_中文/`](../单元1_第一单元_五案/正文/V3.1/01_中文/)\n"
        "- 当前日文：[`../单元1_第一单元_五案/正文/V3.1/02_日本語/`](../单元1_第一单元_五案/正文/V3.1/02_日本語/)\n",
        encoding="utf-8",
    )


def patch_reading_index() -> None:
    idx = NEW_UNIT / "00_单元说明" / "00_阅读索引.md"
    if not idx.exists():
        return
    text = idx.read_text(encoding="utf-8")
    # Point links to V3.1 folder paths
    text = text.replace("./案01_", "./../正文/V3.1/01_中文/案01_")
    text = text.replace("./案02_", "./../正文/V3.1/01_中文/案02_")
    text = text.replace("./案03_", "./../正文/V3.1/01_中文/案03_")
    text = text.replace("./案04_", "./../正文/V3.1/01_中文/案04_")
    text = text.replace("./案05_", "./../正文/V3.1/01_中文/案05_")
    # JP links - fix mixed paths
    for case in ("01", "02", "03", "04", "05"):
        text = re.sub(
            rf"\(\./案{case}_(.+?)_HybridVoice_V3\.1_日本語\.txt\)",
            rf"(../正文/V3.1/02_日本語/案{case}_\1_HybridVoice_V3.1_日本語.txt)",
            text,
        )
        text = re.sub(
            rf"\(\./案{case}_(.+?)_V3\.1_meta\.md\)",
            rf"(../正文/V3.1/03_版本意见/案{case}_\1_V3.1_meta.md)",
            text,
        )
    header = (
        "> **路径 SSOT**：[`../00_版本导航.md`](../00_版本导航.md) · "
        f"当前正文 **`正文/{CURRENT_VERSION}/`**\n\n"
    )
    if "路径 SSOT" not in text:
        text = text.replace("---\n\n## 审阅顺序", header + "---\n\n## 审阅顺序", 1)
    idx.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    body_log = move_body_files()
    copy_v21_from_v20()
    move_unit_docs()
    write_version_readmes()
    write_master_nav()
    illust_log = reorganize_illustrations()
    write_old_stub()
    patch_reading_index()

    report = ROOT / "V2迁移" / "83_单元1_版本文件夹重组报告_V0.1.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# 单元1 · 版本文件夹重组报告 V0.1\n\n"
        f"日期：{date.today().isoformat()}\n\n"
        f"## 新根路径\n\n`单元1_第一单元_五案/`\n\n"
        f"## 当前版本\n\n**{CURRENT_VERSION}**\n\n"
        "## 正文迁移\n\n" + "\n".join(f"- {x}" for x in body_log) + "\n\n"
        "## 插图归类\n\n" + "\n".join(f"- {x}" for x in illust_log) + "\n",
        encoding="utf-8",
    )
    print(f"Done. Nav: {NEW_UNIT / '00_版本导航.md'}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
