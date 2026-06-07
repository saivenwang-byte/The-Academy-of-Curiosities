"""Panel health checks: concentration, duplicates, role violations."""
from __future__ import annotations

import statistics
from typing import Any

from diversity_check import duplicate_pairs, duplicate_ratio

ADULT_TERMS = ["市場定位", "系列化", "认知负荷", "差异化", "出版", "編集"]


def _numeric_scores(evaluations: list[dict]) -> list[float]:
    vals: list[float] = []
    for ev in evaluations:
        for v in ev.get("structured_scores", {}).values():
            if isinstance(v, (int, float)):
                vals.append(float(v))
    return vals


def score_concentration_fail(evaluations: list[dict], std_min: float = 0.8) -> bool:
    vals = _numeric_scores(evaluations)
    if len(vals) < 10:
        return False
    return statistics.pstdev(vals) < std_min


def child_adult_voice_fail(evaluations: list[dict], personas_by_id: dict[str, dict]) -> list[str]:
    bad: list[str] = []
    for ev in evaluations:
        pid = ev["persona_id"]
        p = personas_by_id.get(pid, {})
        if p.get("panel") != "child_experience":
            continue
        blob = " ".join(
            str(ev.get("reading_experience", {}).get(k, ""))
            for k in ("hook", "dropout_point", "favorite_moment", "boring_moment")
        )
        if any(t in blob for t in ADULT_TERMS):
            bad.append(pid)
    return bad


def assess_panel_health(
    evaluations: list[dict],
    personas: list[dict],
    dup_threshold: float = 0.92,
    dup_ratio_max: float = 0.40,
) -> dict[str, Any]:
    personas_by_id = {p["persona_id"]: p for p in personas}
    dup_r = duplicate_ratio(evaluations, dup_threshold)
    dup_pairs = duplicate_pairs(evaluations, dup_threshold)
    concentration = score_concentration_fail(evaluations)
    child_voice = child_adult_voice_fail(evaluations, personas_by_id)

    checks = {
        "duplicate_ratio_ok": dup_r <= dup_ratio_max,
        "score_spread_ok": not concentration,
        "child_voice_ok": len(child_voice) == 0,
    }
    passed = all(checks.values())

    return {
        "status": "PASS" if passed else "FAIL",
        "checks": checks,
        "duplicate_ratio": round(dup_r, 4),
        "duplicate_pairs_count": len(dup_pairs),
        "duplicate_pairs_sample": dup_pairs[:5],
        "score_std": round(statistics.pstdev(_numeric_scores(evaluations)), 3)
        if len(_numeric_scores(evaluations)) >= 2
        else None,
        "child_adult_voice_violations": child_voice,
        "label": "SIMULATION · panel health · not market survey",
    }
