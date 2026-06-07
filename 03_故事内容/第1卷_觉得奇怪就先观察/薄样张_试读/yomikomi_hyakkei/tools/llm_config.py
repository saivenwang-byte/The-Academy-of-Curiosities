"""LLM provider config (OpenAI-compatible endpoints)."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LlmProvider:
    name: str
    base_url: str
    api_key_env: str
    default_model: str

    @property
    def chat_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"

    def api_key(self) -> str | None:
        return os.environ.get(self.api_key_env)


PROVIDERS: dict[str, LlmProvider] = {
    "openai": LlmProvider(
        name="openai",
        base_url="https://api.openai.com/v1",
        api_key_env="OPENAI_API_KEY",
        default_model="gpt-4o-mini",
    ),
    "deepseek": LlmProvider(
        name="deepseek",
        base_url="https://api.deepseek.com",
        api_key_env="DEEPSEEK_API_KEY",
        default_model="deepseek-chat",
    ),
}


def get_provider(name: str) -> LlmProvider:
    key = name.lower().strip()
    if key not in PROVIDERS:
        raise ValueError(f"Unknown provider {name!r}; use: {', '.join(PROVIDERS)}")
    return PROVIDERS[key]


def resolve_model(provider: LlmProvider, model: str | None) -> str:
    return model or provider.default_model
