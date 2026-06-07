"""Tests for corpus validation gate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from corpus_loader import CorpusValidationError, validate_corpus_text, _strip_html


class TestCorpusGate(unittest.TestCase):
    def test_empty_text_fails(self):
        _, errors = validate_corpus_text("", min_char_count=100)
        self.assertTrue(errors)

    def test_short_text_fails(self):
        _, errors = validate_corpus_text("短い" * 10, min_char_count=5000)
        self.assertTrue(any("too short" in e for e in errors))

    def test_markers_required(self):
        text = "x" * 6000
        _, errors = validate_corpus_text(text, min_char_count=5000, required_markers=["陸珣"])
        self.assertTrue(any("missing required markers" in e for e in errors))

    def test_valid_text_passes(self):
        text = "陸珣と観察クラブ。" * 600
        self.assertGreaterEqual(len(text), 5000)
        found, errors = validate_corpus_text(
            text, min_char_count=5000, required_markers=["陸珣", "観察"]
        )
        self.assertEqual(errors, [])
        self.assertIn("陸珣", found)

    def test_strip_html_nonempty(self):
        html = "<html><body><p>陸珣</p><p>" + ("観察。" * 3000) + "</p></body></html>"
        text = _strip_html(html)
        self.assertGreater(len(text), 5000)


if __name__ == "__main__":
    unittest.main()
