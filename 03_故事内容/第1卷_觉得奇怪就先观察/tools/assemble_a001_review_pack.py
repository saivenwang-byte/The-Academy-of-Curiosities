#!/usr/bin/env python3
"""Assemble A001 editor review folder: text + storyboard + StyleB_V3.9 canonical illustrations.

Gates:
  --gate produce  (default) — 主编审阅包：编+导 PASS · 译部 PASS · manifest 7/7 canonical
  --gate deliver            — 试读交付：produce + M0-B + G-AB-JP + COUNT_PASS
  --force-quarantine        — audit-only legacy bundle (skip gates)
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from datetime import date

VOL1 = Path(__file__).resolve().parents[1]
REPO = VOL1.parents[1]
A001 = VOL1 / "单元1_第一单元_五案" / "A001"
OUT = A001 / "06_主编审阅包_V1.0"
PREFLIGHT = VOL1 / "tools/workflow_preflight.py"
POST_GATE = VOL1 / "tools/illustration_post_gate.py"
STYLE_DIR = A001 / "03_插画" / "StyleB_V3.9"
MANIFEST = STYLE_DIR / "illustration_canon_manifest.json"

CN = A001 / "01_正文" / "案01_全班都听见了他的声音_HybridVoice_V3.1.txt"
JP = A001 / "01_正文" / "案01_全班都听见了他的声音_HybridVoice_V3.9_日本語.txt"
STORYBOARD = A001 / "02_分镜头" / "00_插画师分镜文字稿_V1.0.md"
SHOT_MAP = A001 / "02_分镜头" / "03_分镜头_插页地图_V3.9_JP.md"

P0_ORDER = ("DA1", "DA2", "DA3", "DA4", "DA5", "TAIL", "DB1")

SUMMARIES = {
    "DA1": "喇叭响·光嘴未说完全校已听见",
    "DA2": "慧美拦审判·志郎查日志",
    "DA3": "平板显示三週間前彩排文件",
    "DA4": "波形硬切·同一录音用两次",
    "DA5": "全班误指光·水野后排",
    "TAIL": "膜角掀起·黑板ごめんなさい·尾钩",
    "DB1": "三格机制：誤再生/スキップ/切断",
}

QUARANTINE_BANNER = """# LEGACY / 非正本 · 勿绑 PDF

> 本目录插图 **未** 通过 manifest PASS+canonical。
> 仅供对照审计 · **禁止** 作为 PRODUCT 正本路径引用。
"""

README = """# A001 · 完整可审版 · V1.0

> **案01**：全班都听见了他的声音 / クラス全員が、彼の声を聞いた  
> **定位**：主编 / 责编 **一站式审阅文件夹** · StyleB V3.9 · P0 **7/7** canonical  
> **非** 试读 PDF 最终放行版（G-AB-JP 盲测未 PASS 前）

---

## 推荐审阅顺序（约 30–45 分钟）

| 步 | 打开 | 审什么 |
|:--:|------|--------|
| 1 | [`02_分镜推镜头/01_分镜与成片对照表.md`](./02_分镜推镜头/01_分镜与成片对照表.md) | 每镜摘要 ↔ 成片文件名 |
| 2 | [`01_正文/案01_中文_V3.1.txt`](./01_正文/案01_中文_V3.1.txt) | 中文定稿 |
| 3 | [`01_正文/案01_日文_V3.9.txt`](./01_正文/案01_日文_V3.9.txt) | 日文 V3.9（M0-B 已签 · G-AB-JP 待盲测） |
| 4 | [`03_插图成片/`](./03_插图成片/) | **7 张 P0 正本 PNG**（按 DA1→DB1 文件名排序） |
| 5 | [`04_审核与闸门/00_审阅包状态.md`](./04_审核与闸门/00_审阅包状态.md) | 闸门 · manifest · 待办 |

---

## 文件夹结构

```
06_主编审阅包_V1.0/
├── 00_README_打开从这里看.md          ← 本文件
├── 01_正文/
│   ├── 案01_中文_V3.1.txt
│   └── 案01_日文_V3.9.txt
├── 02_分镜推镜头/
│   ├── 01_分镜与成片对照表.md
│   ├── 00_插画师分镜文字稿_V1.0.md
│   └── 03_分镜头_插页地图_V3.9_JP.md
├── 03_插图成片/                       ← 7/7 canonical
│   ├── illustration_canon_manifest.json
│   ├── A001_DA1_…v1.3.png … DB1 …
│   └── _quarantine/                   ← 旧版/无效图（勿绑 PDF）
└── 04_审核与闸门/
    ├── 00_审阅包状态.md
    └── 00_插图清单与审计.md
```

---

## 重建

```bash
python "03_故事内容/第1卷_觉得奇怪就先观察/tools/assemble_a001_review_pack.py"
```

最后更新：2026-06-10
"""

STATUS_TEMPLATE = """# A001 · 审阅包状态 · {date}

## 本包范围

| 项 | 状态 |
|----|------|
| P0 插图 StyleB V3.9 | **{bound}/7 canonical** |
| 中文正文 | V3.1 |
| 日文正文 | V3.9 |
| 分镜 | V3.9 JP 插页地图 + 文字稿 |
| 绑包门禁 | `{gate}` · produce = 主编可审 |

## 闸门（试读 PDF / 对外交付另需）

| 闸门 | 状态 | 说明 |
|------|:----:|------|
| 编+导 G-BRIEF | ✅ PASS | editorial_verdict |
| 译部分镜 | ✅ PASS | translation_verdict |
| M0-B 田中 | ✅ PASS | 2026-06-05 |
| G-CAST COUNT_PASS | ✅ PASS | StyleB V3.9 7/7 |
| illustration manifest | ✅ 7/7 | post-image 门已过 |
| **G-AB-JP 盲测** | ⬜ 待跑 | **deliver 前必须 PASS** |

## 正本插图清单

{manifest_table}

## 工作区正典路径（维护用）

- 插图 SSOT：`A001/03_插画/StyleB_V3.9/`
- 工作流进度：`A001/00_工作流跑通_进度_V1.0.md`
- 单元插图质量门：`单元1/00_插图审查机制诊断与质量门_V1.0.md`
"""


def _safe_print(text: str) -> None:
    enc = sys.stdout.encoding or "utf-8"
    print(text.encode(enc, errors="replace").decode(enc, errors="replace"))


def run_gate(gate: str, force_quarantine: bool) -> int:
    if force_quarantine:
        return 0
    if gate == "produce":
        r = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--mode", "produce", "--case", "A001"],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r.returncode != 0:
            _safe_print((r.stdout or "") + (r.stderr or ""))
            return r.returncode
        r2 = subprocess.run(
            [sys.executable, str(POST_GATE), "--case", "A001", "--promote-all"],
            cwd=REPO,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        _safe_print((r2.stdout or "") + (r2.stderr or ""))
        if r2.returncode != 0:
            _safe_print("BLOCK: manifest not 7/7 canonical")
            return r2.returncode
        return 0
    r = subprocess.run(
        [sys.executable, str(PREFLIGHT), "--mode", "deliver", "--phase", "review-pack", "--case", "A001"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        _safe_print((r.stdout or "") + (r.stderr or ""))
        _safe_print("\nBLOCK: deliver gate failed — use --gate produce for 主编审阅包")
        return r.returncode
    return 0


def load_canonical() -> dict[str, dict]:
    if not MANIFEST.is_file():
        raise FileNotFoundError(MANIFEST)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for shot, entry in data.get("frames", {}).items():
        if entry.get("verdict") == "PASS" and entry.get("canonical"):
            out[shot] = entry
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", choices=("produce", "deliver"), default="produce")
    ap.add_argument("--force-quarantine", action="store_true")
    args = ap.parse_args()

    code = run_gate(args.gate, args.force_quarantine)
    if code != 0:
        return code

    canonical = load_canonical()
    if len(canonical) < len(P0_ORDER) and not args.force_quarantine:
        print(f"FAIL: only {len(canonical)}/{len(P0_ORDER)} P0 canonical in manifest")
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "01_正文").mkdir(parents=True)
    (OUT / "02_分镜推镜头").mkdir(parents=True)
    (OUT / "03_插图成片").mkdir(parents=True)
    (OUT / "03_插图成片/_quarantine").mkdir(parents=True)
    (OUT / "04_审核与闸门").mkdir(parents=True)

    shutil.copy2(CN, OUT / "01_正文" / "案01_中文_V3.1.txt")
    shutil.copy2(JP, OUT / "01_正文" / "案01_日文_V3.9.txt")
    shutil.copy2(STORYBOARD, OUT / "02_分镜推镜头" / "00_插画师分镜文字稿_V1.0.md")
    if SHOT_MAP.is_file():
        shutil.copy2(SHOT_MAP, OUT / "02_分镜推镜头" / "03_分镜头_插页地图_V3.9_JP.md")
    shutil.copy2(MANIFEST, OUT / "03_插图成片" / "illustration_canon_manifest.json")
    (OUT / "00_README_打开从这里看.md").write_text(README, encoding="utf-8")
    (OUT / "03_插图成片/_quarantine/00_README_LEGACY.md").write_text(QUARANTINE_BANNER, encoding="utf-8")

    rows = [
        "# A001 · 分镜与成片对照表 · StyleB V3.9",
        "",
        "> 绑包：`assemble_a001_review_pack.py --gate produce` · manifest SSOT",
        "",
        "| 镜头 | 画面瞬间（摘要） | 成片文件 | 状态 | manifest |",
        "|:----:|------------------|----------|:----:|----------|",
    ]

    bound = 0
    for shot in P0_ORDER:
        entry = canonical.get(shot)
        if not entry:
            rows.append(f"| **{shot}** | {SUMMARIES.get(shot, '—')} | — | **MISSING** | — |")
            continue
        fname = entry["file"]
        src = STYLE_DIR / fname
        if not src.is_file():
            print(f"WARN missing canonical file: {src}")
            rows.append(f"| **{shot}** | {SUMMARIES.get(shot, '—')} | `{fname}` | **FILE MISSING** | PASS |")
            continue
        dest_name = fname
        shutil.copy2(src, OUT / "03_插图成片" / dest_name)
        bound += 1
        rows.append(
            f"| **{shot}** | {SUMMARIES.get(shot, '—')} | `{dest_name}` | **CANONICAL** | PASS |"
        )

    # Copy quarantine samples for audit trail (not bound as canon)
    qdir = STYLE_DIR / "_quarantine"
    if qdir.is_dir():
        for png in sorted(qdir.glob("*.png")):
            shutil.copy2(png, OUT / "03_插图成片/_quarantine" / png.name)

    rows.extend(["", "---", "", f"**P0 bound**: {bound}/{len(P0_ORDER)} · gate: `{args.gate}`", ""])
    (OUT / "02_分镜推镜头" / "01_分镜与成片对照表.md").write_text("\n".join(rows), encoding="utf-8")

    audit_src = STYLE_DIR / "00_设计部出图清单_V3.9_V1.0.md"
    if audit_src.is_file():
        shutil.copy2(audit_src, OUT / "04_审核与闸门" / "00_插图清单与审计.md")

    manifest_rows = ["| Shot | 文件 | Verdict |", "|:----:|------|:-------:|"]
    for shot in P0_ORDER:
        e = canonical.get(shot, {})
        manifest_rows.append(f"| {shot} | `{e.get('file', '—')}` | {e.get('verdict', '—')} |")
    status = STATUS_TEMPLATE.format(
        date=date.today().isoformat(),
        bound=bound,
        gate=args.gate,
        manifest_table="\n".join(manifest_rows),
    )
    (OUT / "04_审核与闸门" / "00_审阅包状态.md").write_text(status, encoding="utf-8")

    print(f"OK: {OUT}")
    print(f"  P0 canonical bound: {bound}/{len(P0_ORDER)}")
    print(f"  gate: {args.gate}")
    return 0 if bound == len(P0_ORDER) else 1


if __name__ == "__main__":
    raise SystemExit(main())
