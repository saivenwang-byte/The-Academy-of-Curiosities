#!/usr/bin/env python3
"""Poll OpenAI quota, run live Phase 1 when ready, commit live_runs to git.

Usage:
  python run_live_when_ready.py --commit
  python run_live_when_ready.py --once --commit   # no poll, fail fast if no quota
"""
from __future__ import annotations

import functools

print = functools.partial(print, flush=True)  # noqa: A001
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CONFIG_DIR, dump_json, load_json, run_id_now
from corpus_loader import load_corpus_from_quota
from eval_worker import live_evaluate
from panel_health import assess_panel_health
from persona_factory import build_panel, write_personas
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


def probe_openai(model: str = "gpt-4o-mini") -> tuple[bool, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return False, "OPENAI_API_KEY not set"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "reply ok"}],
        "max_tokens": 5,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
        return True, "ok"
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return False, body
    except Exception as e:
        return False, str(e)


def load_checkpoint() -> dict:
    if CHECKPOINT.exists():
        return load_json(CHECKPOINT)
    return {"evaluations": [], "errors": [], "run_id": None, "out_dir": None}


def save_checkpoint(state: dict) -> None:
    LIVE_RUNS.mkdir(parents=True, exist_ok=True)
    dump_json(CHECKPOINT, state)


def run_resumable_live(
    personas: list[dict],
    run_id: str,
    out_dir: Path,
    model: str,
    concurrency: int,
) -> tuple[list[dict], list[dict], bool]:
    """Sequential live eval with checkpoint; concurrency capped at 2 for stability."""
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

    pending = [p for p in personas if p["persona_id"] not in done_ids]
    log(f"live eval: {len(evaluations)} done, {len(pending)} pending, corpus={corpus.corpus_id}")

    delay = max(1.0, 1.0 / max(concurrency, 1))
    for i, p in enumerate(pending):
        pid = p["persona_id"]
        try:
            evaluations.append(live_evaluate(p, corpus, run_id, model=model))
            log(f"  OK [{i+1}/{len(pending)}] {pid}")
        except Exception as e:
            err = str(e)
            errors.append({"persona_id": pid, "error": err})
            log(f"  FAIL [{i+1}/{len(pending)}] {pid}: {err[:120]}")
            if "insufficient_quota" in err:
                save_checkpoint(
                    {
                        "run_id": run_id,
                        "out_dir": str(out_dir),
                        "evaluations": evaluations,
                        "errors": errors,
                    }
                )
                return evaluations, errors, False
        save_checkpoint(
            {
                "run_id": run_id,
                "out_dir": str(out_dir),
                "evaluations": evaluations,
                "errors": errors,
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
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    dump_json(
        out_dir / "evaluations.json",
        {"run_id": run_id, "mode": "live", "evaluations": evaluations, "errors": errors},
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
    parser = argparse.ArgumentParser(description="Poll quota and run live Phase 1")
    parser.add_argument("--seed", type=int, default=20260614)
    parser.add_argument("--poll-interval", type=int, default=300, help="Seconds between quota probes")
    parser.add_argument("--max-wait-hours", type=float, default=72.0)
    parser.add_argument("--once", action="store_true", help="Single probe, no polling loop")
    parser.add_argument("--commit", action="store_true", help="Git commit live_runs on success")
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--push", action="store_true", help="Git push after commit")
    args = parser.parse_args()

    quota = load_json(CONFIG_DIR / "quota_phase1.json")
    seed = args.seed or quota.get("seed_default", 20260614)
    run_id = run_id_now("hyakkei_live")
    out_dir = LIVE_RUNS / f"gatea_a001_{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    deadline = time.time() + args.max_wait_hours * 3600
    while True:
        ok, reason = probe_openai(args.model)
        if ok:
            log("OpenAI probe: OK — starting live run")
            break
        log(f"OpenAI probe: waiting ({reason[:160]})")
        if args.once:
            sys.exit(1)
        if time.time() >= deadline:
            log("Max wait exceeded; exiting")
            sys.exit(1)
        time.sleep(args.poll_interval)

    personas = build_panel(seed)
    persona_path = write_personas(personas, seed)

    evaluations, errors, complete = run_resumable_live(
        personas, run_id, out_dir, args.model, args.concurrency
    )

    if not complete:
        log(f"Incomplete: {len(evaluations)}/{len(personas)} evaluations; checkpoint saved")
        sys.exit(2)

    finalize_run(out_dir, run_id, seed, personas, evaluations, errors, persona_path)

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
