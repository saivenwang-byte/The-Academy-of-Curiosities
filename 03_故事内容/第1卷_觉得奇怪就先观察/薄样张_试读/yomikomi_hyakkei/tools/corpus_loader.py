"""Load Gate A corpus text from HTML."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from common import ROOT, load_json


@dataclass
class Corpus:
    corpus_id: str
    title: str
    text: str
    source_path: str
    char_count: int


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</p>", "\n\n", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def load_corpus_from_quota() -> Corpus:
    quota = load_json(ROOT / "config" / "quota_phase1.json")
    rel = quota["corpus"]["html"]
    html_path = (ROOT / rel).resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"Corpus HTML not found: {html_path}")
    raw = html_path.read_text(encoding="utf-8")
    text = _strip_html(raw)
    title_m = re.search(r"<title>([^<]+)</title>", raw, re.I)
    title = title_m.group(1).strip() if title_m else quota["corpus"]["id"]
    return Corpus(
        corpus_id=quota["corpus"]["id"],
        title=title,
        text=text,
        source_path=str(html_path),
        char_count=len(text),
    )


def excerpt(text: str, max_chars: int = 12000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[…truncated for eval payload…]"
