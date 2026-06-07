#!/usr/bin/env python3
"""Poll primary LLM quota (OpenAI), fallback to DeepSeek only when exhausted.

Usage:
  python run_live_when_ready.py --commit
  python run_live_when_ready.py --once --commit   # fail fast if no provider
"""
from __future__ import annotations

import argparse
import functools
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

print = functools.partial(print, flush=True)  # noqa: A001

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CONFIG_DIR, dump_json, load_json, run_id_now
from corpus_loader import load_corpus_from_quota
from eval_worker import live_evaluate
from llm_config import get_provider, resolve_model
from panel_health import assess_panel_health
from persona_factory import build_panel, write_personas
from provider_router import (
    FALLBACK_PROVIDER,
    PRIMARY_PROVIDER,
    ProviderQuotaExhaustedError,
    ProviderSelection,
    ProviderUnavailableError,
    select_provider,
)
from report import write_report

ROOT = Path(__file__).resolve().parents[1]
LIVE_RUNS = ROOT / "live_runs"
CHECKPOINT = LIVE_RUNS / "_checkpoint.json"


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for _ in range(12):
        if (p / ".git").exists():
            return p
        if p.parent == p:
            break
        p = p.parent
    raise RuntimeError("git repo root not found")


REPO_ROOT = find_repo_root(ROOT)
POLL_LOG = LIVE_RUNS / "_poll.log"


def log(msg: str) -> None:
    line = f"{datetime.now(timezone.utc).isoformat()} {msg}"
    print(line)
    LIVE_RUNS.mkdir(parents=True, exist_ok=True)
    with POLL_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return load_json(CHECKPOINT)
    return {"evaluations": [], "errors": [], "run_id": None, "out_dir": None, "active_provider": None}


def save_checkpoint(state: dict) -> None:
    LIVE_RUNS.mkdir(parents=True, exist_ok=True)
    dump_json(CHECKPOINT, state)


def resolve_provider_for_session(model: str | None, force: str | None) -> ProviderSelection:
    """Always probe primary first; deepseek only when primary quota exhausted."""
    return select_provider(model=model, force=force)


def run_resumable_live(
    personas: list[dict],
    run_id: str,
    out_dir: Path,
    model: str | None,
    concurrency: int,
    force_provider: str | None = None,
) -> tuple[list[dict], list[dict], bool]:
    """Sequential live eval with checkpoint and primary-first provider routing."""
    corpus = load_corpus_from_quota()
    state = load_checkpoint()
    if state.get("run_id") == run_id and state.get("out_dir") == str(out_dir):
        done_ids = {e["persona_id"] for e in state.get("evaluations", [])}
        evaluations = list(state.get("evaluations", []))
        errors = list(state.get("errors", []))
    else:
        done_ids = set()
        evaluations = []
        errors = []

    selection = resolve_provider_for_session(model, force_provider)
    active_provider = selection.provider
    log(
        f"provider: {active_provider} ({selection.reason}) · "
        f"primary_ok={selection.primary_ok} · fallback={selection.fallback_used}"
    )

    pending = [p for p in personas if p["persona_id"] not in done_ids]
    log(f"live eval: {len(evaluations)} done, {len(pending)} pending, corpus={corpus.corpus_id}")

    delay = max(1.0, 1.0 / max(concurrency, 1))
    for i, p in enumerate(pending):
        pid = p["persona_id"]
        if active_provider == FALLBACK_PROVIDER and force_provider in (None, "auto", ""):
            selection = resolve_provider_for_session(model, force=None)
            if selection.provider == PRIMARY_PROVIDER:
                active_provider = PRIMARY_PROVIDER
                log(f"primary recovered — switching back from {FALLBACK_PROVIDER}")

        try:
            evaluations.append(
                live_evaluate(p, corpus, run_id, model=model, provider=active_provider)
            )
            log(f"  OK [{i+1}/{len(pending)}] {pid} via {active_provider}")
        except ProviderQuotaExhaustedError as e:
            if active_provider == PRIMARY_PROVIDER and force_provider in (None, "auto", ""):
                try:
                    fb = select_provider(model=model, force=None)
                except ProviderUnavailableError:
                    fb = None
                if fb and fb.provider == FALLBACK_PROVIDER:
                    active_provider = FALLBACK_PROVIDER
                    log(f"primary quota exhausted — switching to {FALLBACK_PROVIDER}")
                    try:
                        evaluations.append(
                            live_evaluate(p, corpus, run_id, model=model, provider=active_provider)
                        )
                        log(f"  OK [{i+1}/{len(pending)}] {pid} via {active_provider} (after failover)")
                    except Exception as retry_e:
                        err = str(retry_e)
                        errors.append({"persona_id": pid, "error": err})
                        log(f"  FAIL [{i+1}/{len(pending)}] {pid}: {err[:120]}")
                        save_checkpoint(
                            {
                                "run_id": run_id,
                                "out_dir": str(out_dir),
                                "evaluations": evaluations,
                                "errors": errors,
                                "active_provider": active_provider,
                            }
                        )
                        return evaluations, errors, False
                else:
                    err = str(e)
                    errors.append({"persona_id": pid, "error": err})
                    log(f"  FAIL [{i+1}/{len(pending)}] {pid}: quota exhausted, no fallback")
                    save_checkpoint(
                        {
                            "run_id": run_id,
                            "out_dir": str(out_dir),
                            "evaluations": evaluations,
                            "errors": errors,
                            "active_provider": active_provider,
                        }
                    )
                    return evaluations, errors, False
            else:
                err = str(e)
                errors.append({"persona_id": pid, "error": err})
                log(f"  FAIL [{i+1}/{len(pending)}] {pid}: {err[:120]}")
                save_checkpoint(
                    {
                        "run_id": run_id,
                        "out_dir": str(out_dir),
                        "evaluations": evaluations,
                        "errors": errors,
                        "active_provider": active_provider,
                    }
                )
                return evaluations, errors, False
        except Exception as e:
            err = str(e)
            errors.append({"persona_id": pid, "error": err})
            log(f"  FAIL [{i+1}/{len(pending)}] {pid}: {err[:120]}")
            save_checkpoint(
                {
                    "run_id": run_id,
                    "out_dir": str(out_dir),
                    "evaluations": evaluations,
                    "errors": errors,
                    "active_provider": active_provider,
                }
            )
            return evaluations, errors, False

        save_checkpoint(
            {
                "run_id": run_id,
                "out_dir": str(out_dir),
                "evaluations": evaluations,
                "errors": errors,
                "active_provider": active_provider,
            }
        )
        time.sleep(delay)

    complete = len(evaluations) == len(personas) and not errors
    return evaluations, errors, complete


def finalize_run(
    out_dir: Path,
    run_id: str,
    seed: int,
    personas: list[dict],
    evaluations: list[dict],
    errors: list[dict],
    persona_path: Path,
    provider: str,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    dump_json(
        out_dir / "evaluations.json",
        {
            "run_id": run_id,
            "mode": "live",
            "llm_provider": provider,
            "evaluations": evaluations,
            "errors": errors,
        },
    )
    health = assess_panel_health(evaluations, personas)
    dump_json(out_dir / "panel_health.json", health)
    write_report(evaluations, personas, health, out_dir, run_id)
    dump_json(
        out_dir / "run_meta.json",
        {
            "run_id": run_id,
            "seed": seed,
            "mode": "SIMULATION",
            "live": True,
            "llm_provider": provider,
            "corpus_id": load_json(CONFIG_DIR / "quota_phase1.json")["corpus"]["id"],
            "personas_file": str(persona_path.relative_to(ROOT)),
            "panel_health": health["status"],
            "completed_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    readme = out_dir / "README.md"
    readme.write_text(
        f"""# 読者百景 · Live Run · {run_id}

> **Status**: **SIMULATION · live API · 非真人 E20**  
> **Corpus**: GateA 序+A001  
> **Readers**: 50（12 锚点 + 38 生成）  
> **Provider**: {provider}（首选 {PRIMARY_PROVIDER}，配额耗尽时 {FALLBACK_PROVIDER}）

| 文件 | 说明 |
|------|------|
| report.md | 四类分报告 |
| summary.json | 结构化摘要 |
| panel_health.json | 面板健康度 |
| evaluations.json | 全量评价 |

**禁止**填入 E20 真实读者招募槽位。
""",
        encoding="utf-8",
    )
    log(f"finalized: {out_dir}")


def git_commit_live_run(out_dir: Path, run_id: str) -> None:
    rel = out_dir.relative_to(REPO_ROOT)
    tool_script = (ROOT / "tools" / "run_live_when_ready.py").relative_to(REPO_ROOT)
    subprocess.run(["git", "add", str(rel), str(tool_script)], cwd=REPO_ROOT, check=True)
    msg = f"E20 data: add live reader lab run GateA preface+A001 ({run_id})."
    subprocess.run(["git", "commit", "-m", msg], cwd=REPO_ROOT, check=True)
    log(f"committed: {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Poll quota and run live Phase 1 (primary-first routing)")
    parser.add_argument("--seed", type=int, default=20260614)
    parser.add_argument("--poll-interval", type=int, default=300, help="Seconds between provider probes")
    parser.add_argument("--max-wait-hours", type=float, default=72.0)
    parser.add_argument("--once", action="store_true", help="Single probe, no polling loop")
    parser.add_argument("--commit", action="store_true", help="Git commit live_runs on success")
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--model", default=None, help="Override model (default per provider)")
    parser.add_argument(
        "--provider",
        default="auto",
        choices=["auto", "openai", "deepseek"],
        help="auto=probe OpenAI first, DeepSeek only on quota exhaustion (default)",
    )
    parser.add_argument("--push", action="store_true", help="Git push after commit")
    args = parser.parse_args()

    force = None if args.provider == "auto" else args.provider

    quota = load_json(CONFIG_DIR / "quota_phase1.json")
    seed = args.seed or quota.get("seed_default", 20260614)
    run_id = run_id_now("hyakkei_live")
    out_dir = LIVE_RUNS / f"gatea_a001_{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    deadline = time.time() + args.max_wait_hours * 3600
    selection: ProviderSelection | None = None
    while True:
        try:
            selection = resolve_provider_for_session(args.model, force)
            prov = get_provider(selection.provider)
            model_label = resolve_model(prov, args.model)
            log(
                f"probe OK: {selection.provider} ({model_label}) — {selection.reason} — starting live run"
            )
            break
        except ProviderUnavailableError as e:
            log(f"probe: waiting ({str(e)[:200]})")
            if args.once:
                sys.exit(1)
            if time.time() >= deadline:
                log("Max wait exceeded; exiting")
                sys.exit(1)
            time.sleep(args.poll_interval)

    assert selection is not None
    personas = build_panel(seed)
    persona_path = write_personas(personas, seed)

    evaluations, errors, complete = run_resumable_live(
        personas, run_id, out_dir, args.model, args.concurrency, force_provider=force
    )

    if not complete:
        log(f"Incomplete: {len(evaluations)}/{len(personas)} evaluations; checkpoint saved")
        sys.exit(2)

    active = selection.provider
    if evaluations:
        active = evaluations[-1].get("llm_provider", active)
    finalize_run(out_dir, run_id, seed, personas, evaluations, errors, persona_path, active)

    if CHECKPOINT.exists():
        CHECKPOINT.unlink()

    if args.commit:
        git_commit_live_run(out_dir, run_id)
        if args.push:
            subprocess.run(["git", "push", "origin", "HEAD"], cwd=REPO_ROOT, check=True)
            log("pushed to origin")

    log("done")


if __name__ == "__main__":
    main()
