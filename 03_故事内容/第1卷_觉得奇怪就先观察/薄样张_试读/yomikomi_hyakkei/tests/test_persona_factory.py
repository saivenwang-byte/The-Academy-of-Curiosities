"""Tests for persona factory."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from persona_factory import build_panel, validate_low_motivation_ratio


class TestPersonaFactory(unittest.TestCase):
    def test_panel_size_and_anchors(self):
        panel = build_panel(20260614)
        self.assertEqual(len(panel), 50)
        self.assertEqual(sum(1 for p in panel if p["is_anchor"]), 12)
        self.assertEqual(sum(1 for p in panel if not p["is_anchor"]), 38)

    def test_low_reading_motivation_ratio(self):
        panel = build_panel(20260614)
        self.assertTrue(validate_low_motivation_ratio(panel, 0.25))


if __name__ == "__main__":
    unittest.main()
