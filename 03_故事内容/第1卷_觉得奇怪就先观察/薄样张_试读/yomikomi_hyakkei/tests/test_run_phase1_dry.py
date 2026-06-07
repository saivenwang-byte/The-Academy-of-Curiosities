"""Dry-run integration test."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from corpus_loader import load_corpus_from_quota
from eval_worker import dry_run_evaluate
from panel_health import assess_panel_health
from persona_factory import build_panel


class TestPhase1DryRun(unittest.TestCase):
    def test_dry_run_produces_50_evaluations(self):
        panel = build_panel(20260614)
        corpus = load_corpus_from_quota()
        run_id = "test_run"
        evals = [dry_run_evaluate(p, corpus, run_id) for p in panel]
        self.assertEqual(len(evals), 50)
        self.assertTrue(all(e["mode"] == "dry_run" for e in evals))
        self.assertTrue(all(len(e["comprehension_quiz"]) >= 3 for e in evals))
        health = assess_panel_health(evals, panel)
        self.assertIn(health["status"], ("PASS", "FAIL"))


if __name__ == "__main__":
    unittest.main()
