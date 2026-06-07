"""Tests for primary-first provider routing (no network)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from provider_router import (
    FALLBACK_PROVIDER,
    PRIMARY_PROVIDER,
    ProviderUnavailableError,
    is_quota_exhausted,
    select_provider,
)


class TestProviderRouter(unittest.TestCase):
    def test_is_quota_exhausted(self):
        self.assertTrue(is_quota_exhausted('{"error":{"code":"insufficient_quota"}}'))
        self.assertFalse(is_quota_exhausted("invalid_api_key"))

    @patch("provider_router.probe_llm")
    def test_primary_ok_no_fallback(self, mock_probe):
        mock_probe.return_value = (True, "ok")
        sel = select_provider(force=None)
        self.assertEqual(sel.provider, PRIMARY_PROVIDER)
        self.assertFalse(sel.fallback_used)
        mock_probe.assert_called_once()

    @patch("provider_router.probe_llm")
    def test_primary_quota_triggers_fallback(self, mock_probe):
        mock_probe.side_effect = [
            (False, "insufficient_quota"),
            (True, "ok"),
        ]
        sel = select_provider(force=None)
        self.assertEqual(sel.provider, FALLBACK_PROVIDER)
        self.assertTrue(sel.fallback_used)
        self.assertEqual(mock_probe.call_count, 2)

    @patch("provider_router.probe_llm")
    def test_primary_non_quota_does_not_fallback(self, mock_probe):
        mock_probe.return_value = (False, "invalid_api_key")
        with self.assertRaises(ProviderUnavailableError):
            select_provider(force=None)

    @patch("provider_router.probe_llm")
    def test_always_reprobe_primary_even_after_fallback(self, mock_probe):
        mock_probe.return_value = (True, "ok")
        sel = select_provider(force=None)
        self.assertEqual(sel.provider, PRIMARY_PROVIDER)
        mock_probe.assert_called_with(PRIMARY_PROVIDER, None)


if __name__ == "__main__":
    unittest.main()
