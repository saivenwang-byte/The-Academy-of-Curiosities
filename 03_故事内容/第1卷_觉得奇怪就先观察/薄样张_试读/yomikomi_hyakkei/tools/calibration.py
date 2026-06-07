"""Compare synthetic runs with human E20 feedback (stub + JSON import)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common import ROOT, dump_json, load_json


def load_human_records(human_dir: Path) -> list[dict]:
    records: list[dict] = []
    if not human_dir.exists():
        return records
    for p in sorted(human_dir.glob("*.json")):
        records.append(load_json(p))
    return records


def compare_dimensions(synthetic_summary: dict, human_records: list[dict]) -> dict[str, Any]:
    """Minimal calibration report when human JSON uses {dimension, score} entries."""
    if not human_records:
        return {
            "status": "PENDING",
            "message": "无真人记录 · 请填入 E20_真实读者招募槽位 并导出 JSON",
            "human_count": 0,
        }

    human_scores: dict[str, list[float]] = {}
    for rec in human_records:
        for item in rec.get("scores", []):
            dim = item.get("dimension")
            val = item.get("score")
            if dim and isinstance(val, (int, float)):
                human_scores.setdefault(dim, []).append(float(val))

    sim_scores = synthetic_summary.get("panel_averages", {})
    deltas: dict[str, Any] = {}
    for dim, sim_val in sim_scores.items():
        if dim not in human_scores:
            continue
        h_avg = sum(human_scores[dim]) / len(human_scores[dim])
        deltas[dim] = {
            "synthetic": sim_val,
            "human": round(h_avg, 2),
            "delta": round(float(sim_val) - h_avg, 2),
        }

    return {
        "status": "OK" if deltas else "PARTIAL",
        "human_count": len(human_records),
        "deltas": deltas,
        "label": "calibration · human_required for external claims",
    }


def write_calibration_template(out_path: Path) -> None:
    template = {
        "reader_id": "R1",
        "source": "E20_real",
        "scores": [
            {"dimension": "continue_will", "score": 8},
            {"dimension": "story_appeal", "score": 7},
            {"dimension": "safety", "score": 9},
        ],
        "notes": "从 E20_试读反馈记录_真实_R{n} 手工转录",
    }
    dump_json(out_path, template)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="読者百景 calibration")
    parser.add_argument("--human-dir", type=Path, default=ROOT.parent / "E20_真实校准")
    parser.add_argument("--synthetic-summary", type=Path, required=True)
    parser.add_argument("--write-template", action="store_true")
    args = parser.parse_args()

    if args.write_template:
        args.human_dir.mkdir(parents=True, exist_ok=True)
        write_calibration_template(args.human_dir / "human_template.json")
        print(f"Wrote template to {args.human_dir / 'human_template.json'}")
        return

    syn = load_json(args.synthetic_summary)
    humans = load_human_records(args.human_dir)
    report = compare_dimensions(syn, humans)
    out = args.synthetic_summary.parent / "calibration_report.json"
    dump_json(out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
