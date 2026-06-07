#!/usr/bin/env python3
"""読者百景 Phase 1 orchestrator."""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Allow running as script from tools/
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CONFIG_DIR, RUNS_DIR, dump_json, load_json, run_id_now
from corpus_loader import load_corpus_from_quota
from eval_worker import dry_run_evaluate, live_evaluate
from panel_health import assess_panel_health
from persona_factory import build_panel, validate_low_motivation_ratio, write_personas
from report import write_report


def run_personas(seed: int) -> tuple[list[dict], Path]:
    panel = build_panel(seed)
    path = write_personas(panel, seed)
    low_ok = validate_low_motivation_ratio(panel, 0.25)
    print(f"personas: {len(panel)} · anchors={sum(1 for p in panel if p['is_anchor'])} · low_motivation_ok={low_ok}")
    return panel, path


def run_evaluations(
    personas: list[dict],
    run_id: str,
    dry_run: bool = True,
    concurrency: int = 4,
    model: str = "gpt-4o-mini",
) -> tuple[list[dict], list[dict]]:
    corpus = load_corpus_from_quota()
    print(f"corpus: {corpus.corpus_id} · chars={corpus.char_count}")

    def one(persona: dict) -> dict:
        if dry_run:
            return dry_run_evaluate(persona, corpus, run_id)
        return live_evaluate(persona, corpus, run_id, model=model)

    results: list[dict] = []
    errors: list[dict] = []

    if dry_run or concurrency <= 1:
        for p in personas:
            try:
                results.append(one(p))
            except Exception as e:
                errors.append({"persona_id": p["persona_id"], "error": str(e)})
    else:
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futs = {ex.submit(one, p): p for p in personas}
            for fut in as_completed(futs):
                p = futs[fut]
                try:
                    results.append(fut.result())
                except Exception as e:
                    errors.append({"persona_id": p["persona_id"], "error": str(e)})
        results.sort(key=lambda e: e["persona_id"])

    if errors:
        print(f"WARN: {len(errors)} evaluation(s) failed", file=sys.stderr)
        for err in errors[:3]:
            print(f"  - {err['persona_id']}: {err['error'][:200]}", file=sys.stderr)
    if not results:
        raise RuntimeError("All evaluations failed; see errors above")

    return results, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="読者百景 Phase 1")
    parser.add_argument("--seed", type=int, default=20260614)
    parser.add_argument("--step", choices=["personas", "full"], default="full")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--live", action="store_true", help="Use OpenAI API")
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--model", default="gpt-4o-mini")
    args = parser.parse_args()

    dry = not args.live
    if args.live:
        args.dry_run = False

    quota = load_json(CONFIG_DIR / "quota_phase1.json")
    seed = args.seed or quota.get("seed_default", 20260614)

    personas, persona_path = run_personas(seed)
    if args.step == "personas":
        print(f"Done: {persona_path}")
        return

    run_id = run_id_now("hyakkei")
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    evaluations, eval_errors = run_evaluations(personas, run_id, dry_run=dry, concurrency=args.concurrency, model=args.model)
    eval_path = run_dir / "evaluations.json"
    dump_json(
        eval_path,
        {
            "run_id": run_id,
            "mode": "dry_run" if dry else "live",
            "evaluations": evaluations,
            "errors": eval_errors,
        },
    )

    health = assess_panel_health(evaluations, personas)
    dump_json(run_dir / "panel_health.json", health)

    summary_path, report_path = write_report(evaluations, personas, health, run_dir, run_id)

    meta = {
        "run_id": run_id,
        "seed": seed,
        "personas_file": str(persona_path.relative_to(persona_path.parent.parent)),
        "mode": "SIMULATION",
        "dry_run": dry,
        "panel_health": health["status"],
    }
    dump_json(run_dir / "run_meta.json", meta)

    print(f"evaluations: {eval_path}")
    print(f"panel_health: {health['status']} (dup_ratio={health['duplicate_ratio']})")
    print(f"report: {report_path}")
    print(f"summary: {summary_path}")


if __name__ == "__main__":
    main()
