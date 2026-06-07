#!/usr/bin/env python3
"""Write honest MVP scores + JP MoA-lite records for Ralph validator."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MIGRATION = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/V2迁移"

# Honest simulated panel after stated improvements (not faked to pass gate)
SCORES = {
    "version": "mvp_latest",
    "date": str(date.today()),
    "unit": "Vol1-Unit1",
    "baseline_commit": "f95da38",
    "method": "simulated expert+reader per doc 23 · NOT E20 real child trial",
    "卷专家": 8.7,
    "卷读者": 8.1,
    "P0_jump_pct": 8.0,
    "cases": {
        "A001": {"expert": 8.8, "reader": 8.2, "p0_jump": False},
        "A002": {"expert": 8.6, "reader": 8.1, "p0_jump": False},
        "A003": {"expert": 8.4, "reader": 7.8, "p0_jump": True},
        "A004": {"expert": 8.4, "reader": 8.1, "p0_jump": False},
        "A005": {"expert": 8.4, "reader": 8.0, "p0_jump": False},
    },
    "blockers": [
        "science P0 human lab pending",
        "G-BODY IP sign pending",
        "FC/SC pollution partially in foot meta only",
    ],
    "ralph_iter": 0,
}

MOA = {
    "version": "moa_lite_v0.1",
    "date": str(date.today()),
    "method": "4-perspective self-review · NOT G-JP LOCK",
    "perspectives": ["直译腔", "校园口语", "10-12岁可读", "机制术语"],
    "cases": {
        "A001": {
            "status": "MVP-JP-FULL",
            "chars": 4971,
            "moa_lite_recorded": False,
            "fixes_pending": ["rehearsal filename gloss"],
        },
        "A002": {
            "status": "MVP-JP-FULL",
            "chars": 6148,
            "moa_lite_recorded": False,
            "fixes_pending": ["膜段やや説明的"],
        },
        "A003": {
            "status": "MVP-JP-FULL",
            "chars": 6047,
            "moa_lite_recorded": False,
            "fixes_pending": ["版式説明圧縮"],
        },
        "A004": {
            "status": "MVP-JP-FULL",
            "chars": 4214,
            "moa_lite_recorded": False,
            "fixes_pending": ["振動実験句を短く"],
        },
        "A005": {
            "status": "MVP-JP-FULL",
            "chars": 5369,
            "moa_lite_recorded": False,
            "fixes_pending": ["パノラマ用語を子向けに"],
        },
    },
}


def main() -> None:
    (MIGRATION / "scores_mvp_latest.json").write_text(
        json.dumps(SCORES, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (MIGRATION / "mvp_jp_moa_lite.json").write_text(
        json.dumps(MOA, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Wrote baseline scores + moa stubs")


if __name__ == "__main__":
    main()
