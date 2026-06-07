"""Generate four-category markdown report from evaluations."""
from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from common import dump_json


def _avg_scores(evals: list[dict], dim: str) -> float | None:
    vals = []
    for ev in evals:
        v = ev.get("structured_scores", {}).get(dim)
        if isinstance(v, (int, float)):
            vals.append(float(v))
    if not vals:
        return None
    return round(sum(vals) / len(vals), 2)


def _panel_filter(evals: list[dict], personas: list[dict], panel: str) -> list[dict]:
    ids = {p["persona_id"] for p in personas if p["panel"] == panel}
    return [e for e in evals if e["persona_id"] in ids]


def build_summary(evaluations: list[dict], personas: list[dict], health: dict) -> dict[str, Any]:
    child_e = _panel_filter(evaluations, personas, "child_experience")
    adult_e = _panel_filter(evaluations, personas, "adult_gate")
    pro_e = _panel_filter(evaluations, personas, "pro_diagnosis")

    child_dims = ["story_appeal", "continue_will", "skip_risk", "puzzle_engagement"]
    adult_dims = ["safety", "purchase_intent", "school_recommend"]
    pro_dims = ["structure_pace", "mystery_fairness", "serialization_potential", "market_differentiation"]

    panel_averages: dict[str, float] = {}
    for d in child_dims + adult_dims + pro_dims:
        v = _avg_scores(evaluations, d)
        if v is not None:
            panel_averages[d] = v

    p0 = []
    for ev in evaluations:
        for c in ev.get("evidence_citations", []):
            if c.get("severity") == "P0":
                p0.append({"persona_id": ev["persona_id"], **c})

    continue_yes = sum(
        1
        for ev in child_e
        if ev.get("reading_experience", {}).get("continue_next") is True
        or ev.get("behavioral_intent", {}).get("continue_next_chapter") == "想读"
    )
    child_continue_rate = round(continue_yes / len(child_e), 3) if child_e else None

    return {
        "status": "SIMULATION",
        "counts": {
            "total": len(evaluations),
            "child": len(child_e),
            "adult": len(adult_e),
            "pro": len(pro_e),
        },
        "four_scores": {
            "child_reading_experience": {d: _avg_scores(child_e, d) for d in child_dims},
            "adult_acceptance": {d: _avg_scores(adult_e, d) for d in adult_dims},
            "pro_production_quality": {d: _avg_scores(pro_e, d) for d in pro_dims},
            "market_series_potential": {
                "serialization_potential": _avg_scores(pro_e, "serialization_potential"),
                "market_differentiation": _avg_scores(pro_e, "market_differentiation"),
                "first_impression": _avg_scores(pro_e, "first_impression"),
            },
        },
        "panel_averages": panel_averages,
        "child_continue_rate": child_continue_rate,
        "p0_issues": p0[:15],
        "panel_health": health,
    }


def render_markdown(summary: dict, run_id: str) -> str:
    fs = summary["four_scores"]
    health = summary["panel_health"]
    lines = [
        f"# 読者百景 · Phase 1 报告 · {run_id}",
        "",
        "> **Status**: **SIMULATION · 50人方法验证 · 非市场调查**",
        "",
        "## 面板构成",
        "",
        f"- 合计 **{summary['counts']['total']}** 人（儿童 {summary['counts']['child']} · 成人 {summary['counts']['adult']} · 专业 {summary['counts']['pro']}）",
        "",
        "## 四类分（禁止简单平均）",
        "",
        "### 儿童阅读体验",
        "",
    ]
    for k, v in fs["child_reading_experience"].items():
        lines.append(f"- **{k}**: {v if v is not None else 'N/A'}")
    lines += ["", "### 成人接受与推荐", ""]
    for k, v in fs["adult_acceptance"].items():
        lines.append(f"- **{k}**: {v if v is not None else 'N/A'}")
    lines += ["", "### 专业制作质量", ""]
    for k, v in fs["pro_production_quality"].items():
        lines.append(f"- **{k}**: {v if v is not None else 'N/A'}")
    lines += ["", "### 市场与系列潜力", ""]
    for k, v in fs["market_series_potential"].items():
        lines.append(f"- **{k}**: {v if v is not None else 'N/A'}")

    lines += [
        "",
        f"**儿童续读率（合成）**: {summary.get('child_continue_rate')}",
        "",
        "## 面板健康度",
        "",
        f"- **判定**: {health['status']}",
        f"- duplicate_ratio: {health['duplicate_ratio']}",
        f"- score_std: {health.get('score_std')}",
        "",
        "## P0 改稿线索（页码级）",
        "",
    ]
    if summary["p0_issues"]:
        for item in summary["p0_issues"]:
            lines.append(f"- [{item['persona_id']}] {item.get('location')} — {item.get('observation')}")
    else:
        lines.append("- （本轮 dry-run 无 P0 或未标注）")

    lines += [
        "",
        "## 真人校准",
        "",
        "并行填写 [`E20_真实读者招募槽位`](../E20_真实读者招募槽位_20260613.md)，运行：",
        "",
        "```bash",
        "python tools/calibration.py --synthetic-summary runs/<run>/summary.json --human-dir ../E20_真实校准",
        "```",
        "",
        "| 版本 | SIMULATION · Phase 1 |",
    ]
    return "\n".join(lines)


def write_report(
    evaluations: list[dict],
    personas: list[dict],
    health: dict,
    run_dir: Path,
    run_id: str,
) -> tuple[Path, Path]:
    summary = build_summary(evaluations, personas, health)
    json_path = run_dir / "summary.json"
    md_path = run_dir / "report.md"
    dump_json(json_path, summary)
    md_path.write_text(render_markdown(summary, run_id), encoding="utf-8")
    return json_path, md_path
