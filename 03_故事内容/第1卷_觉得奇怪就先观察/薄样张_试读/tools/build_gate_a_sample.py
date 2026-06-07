#!/usr/bin/env python3
"""Gate A 样张 MVP — 序+A001 Reader · G1draft 六帧 · 非出版清样。

Outputs:
  薄样张_试读/GateA_样张MVP_{date}/
    学堂奇事録_Vol1_Reader_序+A001_日本語_GateA_{date}.html
    学堂奇事録_Vol1_Reader_序+A001_日本語_GateA_{date}.pdf
    README.md
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

TRIAL = Path(__file__).resolve().parents[1]
FORMAL_TOOLS = TRIAL.parent / "正式版" / "05_出版成果" / "tools"
BUILD_READER = FORMAL_TOOLS / "build_reader_edition.py"
DEFAULT_DATE = "20260610"


def readme_text(stamp: str, html_name: str, pdf_name: str) -> str:
    return f"""# Gate A 样张 MVP · 序+A001 · {stamp}

> **水印**：Gate A MVP · 非出版清样  
> **插图**：G1draft 六帧 LOCK（DA1–DA4 · DB1 · DC1）  
> **范围**：序 + 第 1 起「めくれたポスター」  
> **状态**：内审/E20 试读 · **非** E06 PASS · **非** 出版清样

---

## 打开试看

| 格式 | 文件 |
|------|------|
| **HTML（双击）** | `{html_name}` |
| **PDF** | `{pdf_name}` |

含：序 · A001 正文 · G1draft depth 插图 · DB1 机制 · 线索卡 · 家庭实验 · 陸瑆笔记

---

## 重建

```powershell
python "03_故事内容/第1卷_觉得奇怪就先观察/薄样张_试读/tools/build_gate_a_sample.py"
```

或：

```powershell
python "03_故事内容/第1卷_觉得奇怪就先观察/正式版/05_出版成果/tools/build_reader_edition.py" `
  --scope a001 --gate-a --date {stamp} `
  --out-dir "03_故事内容/第1卷_觉得奇怪就先观察/薄样张_试读/GateA_样张MVP_{stamp}"
```

---

## 插图源

`样章包/插图/depth_anchor/V-S01-*_G1draft.png`（非 v0.2）

吸收清单：`样章包/06_A001_G1draft_优选与v0.2吸收清单_20260611.md`

---

## 取代

本包取代 `MVP_试看_20260609/`（v0.2 内审 · 已标 SUPERSEDED）

入口索引：`MVP_读者试看_入口_{stamp}.md`

---

| 版本 | {stamp} · Gate A Phase 3 |
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Gate A sample MVP pack")
    parser.add_argument("--date", default=DEFAULT_DATE, help="YYYYMMDD folder stamp")
    args = parser.parse_args()
    stamp = args.date
    out_dir = TRIAL / f"GateA_样张MVP_{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(BUILD_READER),
        "--scope",
        "a001",
        "--gate-a",
        "--date",
        stamp,
        "--out-dir",
        str(out_dir),
    ]
    print(">>>", " ".join(cmd))
    result = subprocess.run(cmd, cwd=BUILD_READER.parents[5])
    if result.returncode != 0:
        return result.returncode

    html_name = f"学堂奇事録_Vol1_Reader_序+A001_日本語_GateA_{stamp}.html"
    pdf_name = f"学堂奇事録_Vol1_Reader_序+A001_日本語_GateA_{stamp}.pdf"
    readme_path = out_dir / "README.md"
    readme_path.write_text(readme_text(stamp, html_name, pdf_name), encoding="utf-8")
    print(f"Wrote {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
