#!/usr/bin/env python3
"""Regenerate Gate A corpus TXT SSoT from HTML display source.

Usage (from yomikomi_hyakkei root):
    python tools/extract_corpus_from_html.py
    python tools/extract_corpus_from_html.py --write --update-manifest

Eval SSoT is data/corpus/gatea_preface_a001_ja.txt; HTML is display-only (~45MB).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from common import ROOT, dump_json, load_json  # noqa: E402
from corpus_loader import (  # noqa: E402
    _sha256_text,
    _strip_html,
    build_corpus_manifest,
    validate_corpus_text,
)


def extract(*, write: bool = False, update_manifest: bool = False) -> dict:
    quota = load_json(ROOT / "config" / "quota_phase1.json")
    cfg = quota["corpus"]
    html_path = (ROOT / cfg["html"]).resolve()
    txt_path = (ROOT / cfg["txt"]).resolve()
    manifest_path = txt_path.with_suffix(".manifest.json")

    if not html_path.exists():
        raise FileNotFoundError(f"HTML not found: {html_path}")

    raw = html_path.read_text(encoding="utf-8")
    text = _strip_html(raw)
    sha = _sha256_text(text)
    markers_found, errors = validate_corpus_text(
        text,
        min_char_count=int(cfg.get("min_char_count", 5000)),
        required_markers=list(cfg.get("required_markers", [])),
    )

    result = {
        "corpus_id": cfg["id"],
        "txt_path": str(txt_path),
        "char_count": len(text),
        "sha256": sha,
        "expected_sha256": cfg.get("expected_sha256"),
        "sha_match": sha == cfg.get("expected_sha256"),
        "markers_found": markers_found,
        "errors": errors,
        "gate_status": "PASS" if not errors else "FAIL",
    }

    if write:
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(text, encoding="utf-8")
        print(f"Wrote {txt_path} ({len(text)} chars)")

    if update_manifest and not errors:
        from corpus_loader import Corpus

        corpus = Corpus(
            corpus_id=cfg["id"],
            title=cfg.get("title", cfg["id"]),
            text=text,
            source_path=str(txt_path),
            char_count=len(text),
            sha256=sha,
        )
        manifest = build_corpus_manifest(corpus, markers_found, "PASS")
        dump_json(
            manifest_path,
            {
                "corpus_id": cfg["id"],
                "source_path": cfg["txt"],
                "char_count": len(text),
                "sha256": sha,
                "min_char_count": int(cfg.get("min_char_count", 5000)),
                "required_markers": list(cfg.get("required_markers", [])),
                "gate_status": "PASS",
                "record_type": "actual",
                "evidence_source": "extracted from GateA HTML · extract_corpus_from_html.py",
                "html_display_only": cfg.get("html"),
            },
        )
        print(f"Updated {manifest_path}")

        if cfg.get("expected_sha256") and sha != cfg["expected_sha256"]:
            print(
                "WARNING: sha256 mismatch with quota_phase1.json expected_sha256.\n"
                f"  got:      {sha}\n"
                f"  expected: {cfg['expected_sha256']}\n"
                "Update config/quota_phase1.json expected_sha256 after review."
            )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write TXT to data/corpus/")
    parser.add_argument(
        "--update-manifest",
        action="store_true",
        help="Update manifest JSON (implies --write)",
    )
    args = parser.parse_args()
    write = args.write or args.update_manifest
    result = extract(write=write, update_manifest=args.update_manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
