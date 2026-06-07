"""Evaluation worker: dry-run (deterministic) or live (OpenAI structured)."""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.error
import urllib.request
from typing import Any

from common import CONFIG_DIR, load_json
from corpus_loader import Corpus, excerpt
from llm_config import get_provider, resolve_model
from provider_router import ProviderQuotaExhaustedError, classify_live_http_error
from schema_validate import validate_evaluation


def _load_dims_config() -> dict:
    return load_json(CONFIG_DIR / "eval_dimensions.json")


def eligible_dimensions(persona: dict) -> set[str]:
    dims_cfg = _load_dims_config()
    panel = persona["panel"]
    eligible: set[str] = set()
    for layer in dims_cfg.get("layers", {}).values():
        if panel in layer.get("eligible_panels", []):
            eligible.update(d["id"] for d in layer["dimensions"])
    if panel == "adult_gate":
        extra = dims_cfg.get("layers", {}).get("adult_gate_extra", {})
        eligible.update(d["id"] for d in extra.get("dimensions", []))
    role = persona.get("role")
    scope = dims_cfg.get("pro_role_scope", {}).get(role or "", {})
    if panel == "pro_diagnosis" and scope:
        eligible = set(scope.get("must", [])) | set(scope.get("optional", []))
        for na in scope.get("na", []):
            eligible.discard(na)
    return eligible


def _persona_rng(persona_id: str, run_id: str) -> random.Random:
    h = hashlib.sha256(f"{persona_id}:{run_id}".encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def _score(rng: random.Random, base: float, spread: float = 2.0) -> float:
    v = base + rng.uniform(-spread, spread)
    return round(max(1.0, min(10.0, v)), 1)


def dry_run_evaluate(persona: dict, corpus: Corpus, run_id: str) -> dict[str, Any]:
    rng = _persona_rng(persona["persona_id"], run_id)
    panel = persona["panel"]
    low_mot = persona.get("low_reading_motivation", False)
    mystery = float(persona.get("mystery_affinity", 0.5))
    visual = float(persona.get("visual_dependency", 0.5))
    strict = float(persona.get("strictness", 0.5))

    pid = persona["persona_id"]
    archetype = persona.get("anchor_archetype") or persona.get("role") or persona.get("primary_motive", "")

    if panel == "child_experience":
        base_appeal = 7.5 - (2.0 if low_mot else 0) + mystery * 1.5
        hook = f"[{pid}] ポスターがめくれる場面" if mystery > 0.5 else f"[{pid}] イラストの教室"
        dropout = f"[{pid}] 瑆のノートが長い" if low_mot or visual < 0.4 else f"[{pid}] 特になし"
        skip_pages = [f"{pid}:瑆ノート"] if low_mot else ([f"{pid}:DB1図解"] if visual > 0.7 else [])
        mem_char = rng.choice(["伊藤光", "陸珣", "松本志郎", "加藤慧美"])
        will_continue = base_appeal >= 6.0
    elif panel == "adult_gate":
        base_appeal = 7.0 + (0.5 if float(persona.get("purchase_sensitivity", 0.5)) > 0.6 else 0)
        hook = f"[{pid}] 日常の異変・{archetype}"
        dropout = f"[{pid}] なし"
        skip_pages = []
        mem_char = f"{pid}·観察クラブ"
        will_continue = True
    else:
        base_appeal = 6.5 + (1.0 if persona.get("role") == "children_editor" else 0)
        hook = f"[{pid}] 序章導線・{archetype}"
        dropout = f"[{pid}] 説明密度"
        skip_pages = [f"{pid}:背景説明"]
        mem_char = f"{pid}·陸珣"
        will_continue = True

    eligible = eligible_dimensions(persona)
    scores: dict[str, float | None] = {}
    for dim in eligible:
        if dim in ("illustration_appeal", "text_image_narrative"):
            scores[dim] = _score(rng, base_appeal + visual)
        elif dim in ("mystery_fairness", "puzzle_engagement"):
            scores[dim] = _score(rng, 6.0 + mystery * 2.5 - strict)
        elif dim == "skip_risk":
            scores[dim] = _score(rng, 4.0 + (2.0 if low_mot else 0) + strict * 2)
        elif dim in ("safety", "purchase_intent"):
            scores[dim] = _score(rng, 7.5 - float(persona.get("risk_sensitivity", 0.5)))
        else:
            scores[dim] = _score(rng, base_appeal)

        if panel == "pro_diagnosis" and rng.random() < 0.05:
            scores[dim] = None

    quiz = [
        {
            "question": "ポスターはどうなっていた？",
            "answer": "めくれていた" if rng.random() > 0.3 else "わからない",
            "correct": rng.random() > 0.3,
        },
        {
            "question": "観察クラブは何を調べている？",
            "answer": "風の向き" if mystery > 0.4 else "不明",
            "correct": mystery > 0.4,
        },
        {
            "question": "一番覚えているキャラは？",
            "answer": mem_char,
            "correct": True,
        },
    ]

    result = {
        "persona_id": persona["persona_id"],
        "corpus_id": corpus.corpus_id,
        "run_id": run_id,
        "mode": "dry_run",
        "reading_experience": {
            "hook": hook,
            "dropout_point": dropout,
            "skip_risk_pages": skip_pages,
            "continue_next": will_continue,
            "memorable_character": mem_char,
            "favorite_moment": hook,
            "boring_moment": dropout if dropout != "なし" else "中盤の説明",
        },
        "comprehension_quiz": quiz,
        "structured_scores": scores,
        "behavioral_intent": {
            "continue_next_chapter": "想读" if will_continue else "一般",
            "recommend_to_friend": rng.choice(["会", "也许", "不会"]),
            "acquire_mode": rng.choice(["buy", "borrow", "skip", "unsure"]),
            "discuss_mystery": mystery > 0.55,
        },
        "evidence_citations": [
            {
                "location": f"序章〜A001·{pid}",
                "observation": f"{persona.get('primary_motive', '')} / {persona.get('main_aversion', '')} → {hook}",
                "severity": "P1" if will_continue else "P0",
            },
            {
                "location": f"panel={panel}·{archetype}",
                "observation": persona.get("human_summary_zh", pid),
                "severity": "note",
            },
        ],
        "uncertainty": {
            "confidence": round(0.55 + rng.uniform(0, 0.35), 2),
            "missing_materials": [] if visual > 0.4 else ["部分插页未单独输入"],
            "notes": "dry_run · SIMULATION · smoke test only",
        },
    }
    ok, schema_errors = validate_evaluation(result)
    if not ok:
        raise ValueError(f"dry_run schema validation failed: {schema_errors}")
    return result


def live_evaluate(
    persona: dict,
    corpus: Corpus,
    run_id: str,
    model: str | None = None,
    max_retries: int = 4,
    provider: str = "openai",
) -> dict[str, Any]:
    prov = get_provider(provider)
    api_key = prov.api_key()
    if not api_key:
        raise RuntimeError(f"{prov.api_key_env} not set; use --dry-run or set API key")
    model = resolve_model(prov, model)

    system = (
        "你是読者百景合成读者评估器。输出严格 JSON。"
        "必须包含字段: reading_experience, comprehension_quiz, structured_scores, "
        "behavioral_intent, evidence_citations, uncertainty。"
        "必须引用具体段落位置；材料不足则标注 uncertainty。"
        "合成Persona，不代表真人。禁止编造未提供的插画细节。"
    )
    user = {
        "persona": persona,
        "corpus_excerpt": excerpt(corpus.text, 10000),
        "eligible_dimensions": sorted(eligible_dimensions(persona)),
    }
    last_err: Exception | None = None
    last_schema_errors: list[str] = []
    for attempt in range(max_retries):
        system_msg = system
        if last_schema_errors:
            system_msg += f" 上次输出未通过 schema: {'; '.join(last_schema_errors[:5])}。请补全全部必填字段。"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
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
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read().decode())
            content = body["choices"][0]["message"]["content"]
            result = json.loads(content)
            result.setdefault("persona_id", persona["persona_id"])
            result.setdefault("corpus_id", corpus.corpus_id)
            result.setdefault("run_id", run_id)
            result["mode"] = "live"
            result["llm_provider"] = prov.name
            result["llm_model"] = model
            ok, schema_errors = validate_evaluation(result)
            if not ok:
                last_schema_errors = schema_errors
                last_err = ValueError(f"schema validation failed: {schema_errors}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                result["schema_valid"] = False
                result["schema_errors"] = schema_errors
                return result
            result["schema_valid"] = True
            return result
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            last_err = classify_live_http_error(prov.name, err_body)
            if isinstance(last_err, ProviderQuotaExhaustedError):
                raise last_err from e
            last_err = RuntimeError(f"{prov.name} API error ({e.code}): {err_body}")
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            raise last_err from e
        except Exception as e:
            last_err = e
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            raise
    raise last_err or RuntimeError("live_evaluate failed")
