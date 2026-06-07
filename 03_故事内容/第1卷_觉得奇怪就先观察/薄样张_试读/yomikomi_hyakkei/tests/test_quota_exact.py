"""Exact quota bucket/role tests after anchor subtraction."""
from __future__ import annotations

import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from common import load_json, CONFIG_DIR
from persona_factory import build_panel, validate_panel_quotas


class TestQuotaExact(unittest.TestCase):
    def test_validate_panel_quotas_passes(self):
        panel = build_panel(20260614)
        v = validate_panel_quotas(panel)
        self.assertTrue(v["valid"], v["errors"])

    def test_child_age_buckets_exact(self):
        panel = build_panel(20260614)
        quota = load_json(CONFIG_DIR / "quota_phase1.json")
        buckets = quota["panels"]["child_experience"]["age_buckets"]
        children = [p for p in panel if p["panel"] == "child_experience"]
        for b in buckets:
            lo, hi = b["ages"][0], b["ages"][-1]
            cnt = sum(1 for p in children if lo <= int(p["age"]) <= hi)
            self.assertEqual(cnt, b["count"], f"bucket {b['ages']}: {cnt} != {b['count']}")

    def test_adult_roles_exact(self):
        panel = build_panel(20260614)
        quota = load_json(CONFIG_DIR / "quota_phase1.json")
        roles_cfg = quota["panels"]["adult_gate"]["roles"]
        adults = [p for p in panel if p["panel"] == "adult_gate"]
        for role, target in roles_cfg.items():
            cnt = sum(1 for p in adults if p.get("role") == role)
            self.assertEqual(cnt, target, f"role {role}: {cnt} != {target}")

    def test_pro_roles_exact(self):
        panel = build_panel(20260614)
        quota = load_json(CONFIG_DIR / "quota_phase1.json")
        roles_cfg = quota["panels"]["pro_diagnosis"]["roles"]
        pros = [p for p in panel if p["panel"] == "pro_diagnosis"]
        for role, target in roles_cfg.items():
            cnt = sum(1 for p in pros if p.get("role") == role)
            self.assertEqual(cnt, target, f"role {role}: {cnt} != {target}")

    def test_generated_counts(self):
        panel = build_panel(20260614)
        quota = load_json(CONFIG_DIR / "quota_phase1.json")
        for panel_name, pcfg in quota["panels"].items():
            members = [p for p in panel if p["panel"] == panel_name]
            gen = sum(1 for p in members if not p.get("is_anchor"))
            self.assertEqual(gen, pcfg["generated"])
            anc = sum(1 for p in members if p.get("is_anchor"))
            self.assertEqual(anc, pcfg["anchors"])


if __name__ == "__main__":
    unittest.main()
