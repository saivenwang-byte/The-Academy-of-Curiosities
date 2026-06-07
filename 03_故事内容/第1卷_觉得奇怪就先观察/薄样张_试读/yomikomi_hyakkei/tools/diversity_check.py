"""Duplicate opinion detection via bag-of-words cosine similarity."""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable


def _tokenize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^\w\s\u3040-\u30ff\u4e00-\u9fff]", " ", text)
    return [t for t in text.split() if len(t) >= 2]


def _bow(tokens: Iterable[str]) -> Counter[str]:
    return Counter(tokens)


def cosine_similarity(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b[k] for k in a if k in b)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def eval_text_blob(ev: dict) -> str:
    parts: list[str] = []
    rexp = ev.get("reading_experience", {})
    for k in ("hook", "dropout_point", "memorable_character", "favorite_moment", "boring_moment"):
        v = rexp.get(k)
        if v:
            parts.append(str(v))
    for c in ev.get("evidence_citations", []):
        parts.append(c.get("observation", ""))
    return " ".join(parts)


def duplicate_pairs(evaluations: list[dict], threshold: float = 0.92) -> list[tuple[str, str, float]]:
    bows = [(e["persona_id"], _bow(_tokenize(eval_text_blob(e)))) for e in evaluations]
    pairs: list[tuple[str, str, float]] = []
    for i in range(len(bows)):
        for j in range(i + 1, len(bows)):
            sim = cosine_similarity(bows[i][1], bows[j][1])
            if sim >= threshold:
                pairs.append((bows[i][0], bows[j][0], round(sim, 4)))
    return pairs


def duplicate_ratio(evaluations: list[dict], threshold: float = 0.92) -> float:
    n = len(evaluations)
    if n < 2:
        return 0.0
    pairs = duplicate_pairs(evaluations, threshold)
    involved = set()
    for a, b, _ in pairs:
        involved.add(a)
        involved.add(b)
    return len(involved) / n
