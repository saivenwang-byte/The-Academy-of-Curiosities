"""Primary-first LLM routing: OpenAI preferred, DeepSeek fallback on quota exhaustion only."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Literal

from llm_config import get_provider, resolve_model

PRIMARY_PROVIDER = "openai"
FALLBACK_PROVIDER = "deepseek"
ProviderName = Literal["openai", "deepseek"]


class ProviderUnavailableError(RuntimeError):
    pass


class ProviderQuotaExhaustedError(RuntimeError):
    def __init__(self, provider: str, reason: str) -> None:
        super().__init__(reason)
        self.provider = provider
        self.reason = reason


@dataclass
class ProviderSelection:
    provider: str
    reason: str
    primary_probed: bool
    primary_ok: bool
    fallback_used: bool

    @property
    def model(self) -> str:
        return resolve_model(get_provider(self.provider), None)


def is_quota_exhausted(reason: str) -> bool:
    r = reason.lower()
    markers = (
        "insufficient_quota",
        "exceeded your current quota",
        "quota has been exceeded",
        "billing_hard_limit",
        "insufficient balance",
        "余额不足",
    )
    return any(m in r for m in markers)


def probe_llm(provider: str, model: str | None = None) -> tuple[bool, str]:
    prov = get_provider(provider)
    api_key = prov.api_key()
    if not api_key:
        return False, f"{prov.api_key_env} not set"
    model = resolve_model(prov, model)
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "reply ok"}],
        "max_tokens": 5,
    }
    req = urllib.request.Request(
        prov.chat_url,
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
        return False, e.read().decode()
    except Exception as e:
        return False, str(e)


def select_provider(
    *,
    model: str | None = None,
    force: str | None = None,
) -> ProviderSelection:
    """Pick provider for a live run start/resume.

    Policy:
    - Always probe PRIMARY first (even if previously on fallback).
    - Use PRIMARY when probe OK.
    - Use FALLBACK only when PRIMARY probe fails with quota exhaustion.
    - Manual ``force`` bypasses policy (openai | deepseek); ``auto``/None uses policy.
    """
    if force and force not in ("auto", ""):
        ok, reason = probe_llm(force, model)
        if not ok:
            raise ProviderUnavailableError(f"forced provider {force!r} unavailable: {reason[:300]}")
        return ProviderSelection(
            provider=force,
            reason=f"forced:{force}",
            primary_probed=(force == PRIMARY_PROVIDER),
            primary_ok=ok if force == PRIMARY_PROVIDER else False,
            fallback_used=(force == FALLBACK_PROVIDER),
        )

    primary_ok, primary_reason = probe_llm(PRIMARY_PROVIDER, model)
    if primary_ok:
        return ProviderSelection(
            provider=PRIMARY_PROVIDER,
            reason="primary_ok",
            primary_probed=True,
            primary_ok=True,
            fallback_used=False,
        )

    if not is_quota_exhausted(primary_reason):
        raise ProviderUnavailableError(
            f"primary ({PRIMARY_PROVIDER}) unavailable (non-quota): {primary_reason[:300]}"
        )

    fallback_ok, fallback_reason = probe_llm(FALLBACK_PROVIDER, model)
    if fallback_ok:
        return ProviderSelection(
            provider=FALLBACK_PROVIDER,
            reason=f"primary_quota_exhausted; fallback_active",
            primary_probed=True,
            primary_ok=False,
            fallback_used=True,
        )

    raise ProviderUnavailableError(
        f"primary quota exhausted ({primary_reason[:120]}); "
        f"fallback also unavailable ({fallback_reason[:120]})"
    )


def maybe_switch_from_fallback(model: str | None = None) -> ProviderSelection:
    """Re-probe primary before each eval batch/resume when on fallback."""
    return select_provider(model=model, force=None)


def classify_live_http_error(provider: str, err_body: str) -> Exception:
    if is_quota_exhausted(err_body):
        return ProviderQuotaExhaustedError(provider, err_body)
    return RuntimeError(f"{provider} API error: {err_body[:300]}")
