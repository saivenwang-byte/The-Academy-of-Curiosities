#!/usr/bin/env python3
"""Run yomikomi_hyakkei unit tests (stdlib only)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
loader = unittest.TestLoader()
suite = loader.discover(str(ROOT / "tests"), pattern="test_*.py")
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
