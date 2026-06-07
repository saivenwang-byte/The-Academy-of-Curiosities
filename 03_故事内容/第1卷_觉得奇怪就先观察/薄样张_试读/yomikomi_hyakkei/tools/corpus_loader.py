"""Load Gate A corpus text from HTML with validation gate."""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from common import ROOT, dump_json, load_json


class CorpusValidationError(ValueError):
    """Raised when corpus fails min length, markers, or integrity checks."""


@dataclass
class Corpus:
    corpus_id: str
    title: str
    text: str
    source_path: str
    char_count: int
    sha256: str


@dataclass
class CorpusManifest:
    corpus_id: str
    source_path: str
    char_count: int
    sha256: str
    min_char_count: int
    required_markers: list[str]
    markers_found: list[str]
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</p>", "\n\n", html)
    html = re.sub(r"(?is)<[^>]+>", " ", html)
    html = re.sub(r"[ \t]+", " ", html)
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _corpus_config() -> dict[str, Any]:
    quota = load_json(ROOT / "config" / "quota_phase1.json")
    cfg = dict(quota.get("corpus", {}))
    cfg.setdefault("min_char_count", 5000)
    cfg.setdefault("required_markers", ["陸珣", "観察"])
    return cfg


def validate_corpus_text(
    text: str,
    *,
    min_char_count: int = 5000,
    required_markers: list[str] | None = None,
) -> tuple[list[str], list[str]]:
    """Return (markers_found, errors). Empty errors => pass."""
    required_markers = required_markers or ["陸珣", "観察"]
    errors: list[str] = []
    if not text or not text.strip():
        errors.append("corpus text is empty after HTML strip")
    elif len(text) < min_char_count:
        errors.append(f"corpus too short: {len(text)} chars < min {min_char_count}")
    markers_found = [m for m in required_markers if m in text]
    missing = [m for m in required_markers if m not in text]
    if missing:
        errors.append(f"missing required markers: {missing}")
    return markers_found, errors


def build_corpus_manifest(corpus: Corpus, markers_found: list[str], gate_status: str = "PASS") -> CorpusManifest:
    cfg = _corpus_config()
    return CorpusManifest(
        corpus_id=corpus.corpus_id,
        source_path=corpus.source_path,
        char_count=corpus.char_count,
        sha256=corpus.sha256,
        min_char_count=int(cfg.get("min_char_count", 5000)),
        required_markers=list(cfg.get("required_markers", [])),
        markers_found=markers_found,
        gate_status=gate_status,
    )


def write_corpus_manifest(manifest: CorpusManifest, out_path: Path) -> Path:
    dump_json(out_path, manifest.to_dict())
    return out_path


def load_corpus_from_quota(*, strict: bool = True) -> Corpus:
    cfg = _corpus_config()
    rel = cfg["html"]
    html_path = (ROOT / rel).resolve()
    if not html_path.exists():
        raise FileNotFoundError(f"Corpus HTML not found: {html_path}")
    raw = html_path.read_text(encoding="utf-8")
    text = _strip_html(raw)
    title_m = re.search(r"<title>([^<]+)</title>", raw, re.I)
    title = title_m.group(1).strip() if title_m else cfg["id"]
    sha = _sha256_text(text)
    corpus = Corpus(
        corpus_id=cfg["id"],
        title=title,
        text=text,
        source_path=str(html_path),
        char_count=len(text),
        sha256=sha,
    )
    markers_found, errors = validate_corpus_text(
        text,
        min_char_count=int(cfg.get("min_char_count", 5000)),
        required_markers=list(cfg.get("required_markers", [])),
    )
    if strict and errors:
        raise CorpusValidationError("; ".join(errors))
    if strict and not markers_found and cfg.get("required_markers"):
        raise CorpusValidationError("no required markers found")
    return corpus


def load_corpus_with_manifest(out_dir: Path | None = None) -> tuple[Corpus, CorpusManifest]:
    corpus = load_corpus_from_quota(strict=True)
    cfg = _corpus_config()
    markers_found, _ = validate_corpus_text(
        corpus.text,
        min_char_count=int(cfg.get("min_char_count", 5000)),
        required_markers=list(cfg.get("required_markers", [])),
    )
    manifest = build_corpus_manifest(corpus, markers_found, "PASS")
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        write_corpus_manifest(manifest, out_dir / "corpus_manifest.json")
    return corpus, manifest


def excerpt(text: str, max_chars: int = 12000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[…truncated for eval payload…]"
