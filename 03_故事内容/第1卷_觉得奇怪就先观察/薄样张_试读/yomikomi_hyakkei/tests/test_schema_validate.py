"""Schema validation for evaluation payloads."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from eval_worker import dry_run_evaluate
from corpus_loader import Corpus
from schema_validate import validate_evaluation


def _minimal_corpus() -> Corpus:
    return Corpus(
        corpus_id="test",
        title="test",
        text="陸珣観察" * 1000,
        source_path="/tmp/test.html",
        char_count=6000,
        sha256="abc",
    )


class TestSchemaValidate(unittest.TestCase):
    def test_dry_run_passes_schema(self):
        persona = {
            "persona_id": "CH-G001",
            "panel": "child_experience",
            "low_reading_motivation": False,
            "mystery_affinity": 0.7,
            "visual_dependency": 0.5,
            "strictness": 0.5,
            "primary_motive": "推理",
            "main_aversion": "汉字",
        }
        ev = dry_run_evaluate(persona, _minimal_corpus(), "run_test")
        ok, errors = validate_evaluation(ev)
        self.assertTrue(ok, errors)

    def test_missing_field_fails(self):
        ok, errors = validate_evaluation({"persona_id": "x"})
        self.assertFalse(ok)
        self.assertTrue(any("missing" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
