"""Validate evaluation JSON against evaluation.schema.json (stdlib-first)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from common import ROOT

SCHEMA_PATH = ROOT / "schema" / "evaluation.schema.json"

REQUIRED_TOP = [
    "persona_id",
    "corpus_id",
    "run_id",
    "mode",
    "reading_experience",
    "comprehension_quiz",
    "structured_scores",
    "behavioral_intent",
    "evidence_citations",
    "uncertainty",
]

REQUIRED_READING = [
    "hook",
    "dropout_point",
    "skip_risk_pages",
    "continue_next",
    "memorable_character",
]

QUIZ_MIN = 3


def _load_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return True


def validate_evaluation(obj: dict[str, Any], *, schema: dict[str, Any] | None = None) -> tuple[bool, list[str]]:
    """Return (valid, error_messages). Uses jsonschema if installed, else stdlib checks."""
    try:
        import jsonschema  # type: ignore

        jsonschema.validate(instance=obj, schema=schema or _load_schema())
        return True, []
    except ImportError:
        pass
    except Exception as e:
        return False, [f"jsonschema: {e}"]

    errors: list[str] = []
    if not isinstance(obj, dict):
        return False, ["root must be object"]

    for key in REQUIRED_TOP:
        if key not in obj:
            errors.append(f"missing required field: {key}")

    mode = obj.get("mode")
    if mode not in ("dry_run", "live"):
        errors.append(f"mode must be dry_run or live, got {mode!r}")

    rexp = obj.get("reading_experience")
    if not isinstance(rexp, dict):
        errors.append("reading_experience must be object")
    else:
        for key in REQUIRED_READING:
            if key not in rexp:
                errors.append(f"reading_experience missing: {key}")

    quiz = obj.get("comprehension_quiz")
    if not isinstance(quiz, list):
        errors.append("comprehension_quiz must be array")
    elif len(quiz) < QUIZ_MIN:
        errors.append(f"comprehension_quiz minItems {QUIZ_MIN}, got {len(quiz)}")
    else:
        for i, item in enumerate(quiz):
            if not isinstance(item, dict):
                errors.append(f"comprehension_quiz[{i}] must be object")
                continue
            for qk in ("question", "answer", "correct"):
                if qk not in item:
                    errors.append(f"comprehension_quiz[{i}] missing {qk}")
                elif qk == "correct" and not isinstance(item[qk], bool):
                    errors.append(f"comprehension_quiz[{i}].correct must be boolean")

    scores = obj.get("structured_scores")
    if not isinstance(scores, dict):
        errors.append("structured_scores must be object")
    else:
        for k, v in scores.items():
            if v is None:
                continue
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                errors.append(f"structured_scores.{k} must be number or null")
            elif not (1 <= float(v) <= 10):
                errors.append(f"structured_scores.{k} out of range 1-10: {v}")

    citations = obj.get("evidence_citations")
    if not isinstance(citations, list):
        errors.append("evidence_citations must be array")
    else:
        for i, c in enumerate(citations):
            if not isinstance(c, dict):
                errors.append(f"evidence_citations[{i}] must be object")
                continue
            for ck in ("location", "observation"):
                if ck not in c:
                    errors.append(f"evidence_citations[{i}] missing {ck}")

    intent = obj.get("behavioral_intent")
    if intent is not None and not isinstance(intent, dict):
        errors.append("behavioral_intent must be object")

    unc = obj.get("uncertainty")
    if unc is not None and not isinstance(unc, dict):
        errors.append("uncertainty must be object")

    return len(errors) == 0, errors
