#!/usr/bin/env python3
"""Panel match stats + quota validation."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from persona_factory import build_panel, validate_panel_quotas


def main() -> None:
    seed = 20260614
    panel = build_panel(seed)
    personas = panel
    children = [p for p in personas if p["panel"] == "child_experience"]
    low = sum(1 for p in children if p.get("low_reading_motivation"))
    quota_v = validate_panel_quotas(panel)
    stats = {
        "panel_counts": {
            "total": len(personas),
            "child_experience": len(children),
            "adult_gate": sum(1 for p in personas if p["panel"] == "adult_gate"),
            "pro_diagnosis": sum(1 for p in personas if p["panel"] == "pro_diagnosis"),
            "anchors": sum(1 for p in personas if p.get("is_anchor")),
        },
        "child_attributes": {
            "low_reading_motivation_ratio": round(low / len(children), 3),
            "age_distribution": dict(Counter(p.get("age") for p in children)),
            "competitor_familiarity_gte_0_6": sum(
                1 for p in children if float(p.get("competitor_familiarity", 0)) >= 0.6
            ),
            "visual_dependency_gte_0_7": sum(
                1 for p in children if float(p.get("visual_dependency", 0)) >= 0.7
            ),
            "mystery_affinity_gte_0_7": sum(
                1 for p in children if float(p.get("mystery_affinity", 0)) >= 0.7
            ),
            "reading_level_low": sum(1 for p in children if p.get("reading_level") == "low"),
        },
        "quota_validation": quota_v,
        "project_fit_checks": {
            "target_age_9_13": all(9 <= p.get("age", 0) <= 13 for p in children),
            "low_motivation_gte_25pct": (low / len(children)) >= 0.25,
            "quota_30_13_7": len(children) == 30,
            "quota_exact_valid": quota_v["valid"],
            "jp_primary_language": sum(
                1 for p in personas if p.get("language_background") == "ja"
            )
            / len(personas),
        },
    }
    out = ROOT / "live_runs" / "panel_match_stats.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
