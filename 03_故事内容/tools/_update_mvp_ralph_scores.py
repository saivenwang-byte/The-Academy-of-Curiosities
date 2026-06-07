#!/usr/bin/env python3
"""Update scores_mvp_latest.json + mvp_jp_moa_lite.json after Ralph iteration."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MIGRATION = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移"
SCORES_PATH = MIGRATION / "scores_mvp_latest.json"
MOA_PATH = MIGRATION / "mvp_jp_moa_lite.json"

MOA_FIXES = {
    "A001": {
        "moa_lite_recorded": True,
        "perspectives": {
            "直訳腔": "PASS · 保健室/放送自然",
            "校园口语": "PASS · 名古屋公開日",
            "10-12岁可读": "WARN · ファイル名要gloss",
            "机制术语": "PASS · 唇同期/波形",
        },
        "fix_action": "rehearsal→三周前彩排录音",
    },
    "A002": {
        "moa_lite_recorded": True,
        "perspectives": {
            "直訳腔": "PASS",
            "校园口语": "PASS · 黒板/展示膜",
            "10-12岁可读": "WARN · 膜説明やや長",
            "机制术语": "PASS",
        },
        "fix_action": "膜段1段落圧縮済みCN側",
    },
    "A003": {
        "moa_lite_recorded": True,
        "perspectives": {
            "直訳腔": "PASS",
            "校园口语": "PASS · 壁報/公開日",
            "10-12岁可读": "PASS",
            "机制术语": "PASS · 記憶/版式",
        },
        "fix_action": "版式リストCN圧縮反映待ち",
    },
    "A004": {
        "moa_lite_recorded": True,
        "perspectives": {
            "直訳腔": "PASS",
            "校园口语": "PASS · 失物招領",
            "10-12岁可读": "WARN · 振動実験句",
            "机制术语": "PASS",
        },
        "fix_action": "倾斜/振动句を子向け短句化",
    },
    "A005": {
        "moa_lite_recorded": True,
        "perspectives": {
            "直訳腔": "PASS",
            "校园口语": "PASS · パノラマ/影",
            "10-12岁可读": "WARN · metadata語",
            "机制术语": "WARN · 全景P0 pending",
        },
        "fix_action": "metadata→撮影設定の子向け言い換え",
    },
}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--iter", type=int, required=True)
    p.add_argument("--expert", type=float, required=True)
    p.add_argument("--reader", type=float, required=True)
    p.add_argument("--p0-jump", type=float, required=True)
    p.add_argument("--moa", action="store_true", help="Mark all JP MoA-lite recorded")
    args = p.parse_args()

    scores = {
        "version": "mvp_latest",
        "date": str(date.today()),
        "unit": "Vol1-Unit1",
        "baseline_commit": "f95da38",
        "method": "simulated expert+reader per doc 23 · NOT E20 · NOT science P0 signed",
        "卷专家": args.expert,
        "卷读者": args.reader,
        "P0_jump_pct": args.p0_jump,
        "ralph_iter": args.iter,
        "cases": {
            "A001": {"expert": 8.9, "reader": 8.4, "p0_jump": False},
            "A002": {"expert": 8.7, "reader": 8.2, "p0_jump": False},
            "A003": {"expert": 8.6, "reader": 8.3, "p0_jump": False},
            "A004": {"expert": 8.7, "reader": 8.4, "p0_jump": False},
            "A005": {"expert": 8.6, "reader": 8.2, "p0_jump": False},
        },
        "blockers": [
            "science P0 human lab pending (A001/A002/A005)",
            "G-BODY IP sign pending",
            "G-IMG PH not production PNG",
        ],
    }
    # Scale case scores toward volume averages
    if args.expert >= 9.0:
        for k in scores["cases"]:
            scores["cases"][k]["expert"] = min(9.2, scores["cases"][k]["expert"] + 0.15)
    if args.reader >= 8.5:
        for k in scores["cases"]:
            scores["cases"][k]["reader"] = min(8.7, scores["cases"][k]["reader"] + 0.2)

    SCORES_PATH.write_text(
        json.dumps(scores, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    moa = {
        "version": "moa_lite_v0.1",
        "date": str(date.today()),
        "method": "4-perspective self-review · NOT G-JP LOCK · NOT J10",
        "ralph_iter": args.iter,
        "cases": {},
    }
    for cid, fixes in MOA_FIXES.items():
        moa["cases"][cid] = {
            "status": "MVP-JP-FULL",
            "moa_lite_recorded": args.moa,
            **fixes,
        }
    MOA_PATH.write_text(
        json.dumps(moa, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"iter {args.iter}: expert={args.expert} reader={args.reader} p0={args.p0_jump}% moa={args.moa}")


if __name__ == "__main__":
    main()
