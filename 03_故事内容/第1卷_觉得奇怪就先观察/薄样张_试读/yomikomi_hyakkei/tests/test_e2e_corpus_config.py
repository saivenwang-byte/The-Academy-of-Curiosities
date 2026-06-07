"""End-to-end: load corpus exactly as quota_phase1.json specifies (clone reproducibility)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from corpus_loader import load_corpus_from_quota  # noqa: E402


class TestE2ECorpusConfig(unittest.TestCase):
    def test_quota_config_loads_committed_txt(self):
        corpus = load_corpus_from_quota(strict=True)
        self.assertGreaterEqual(corpus.char_count, 5000)
        self.assertIn("陸珣", corpus.text)
        self.assertIn("観察", corpus.text)
        manifest_path = (
            Path(__file__).resolve().parents[1]
            / "data"
            / "corpus"
            / "gatea_preface_a001_ja.manifest.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(corpus.sha256, manifest["sha256"])
        self.assertTrue(corpus.source_path.endswith(".txt"))


if __name__ == "__main__":
    unittest.main()
