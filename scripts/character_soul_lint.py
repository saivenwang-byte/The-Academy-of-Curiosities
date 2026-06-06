#!/usr/bin/env python3
"""Lint character soul YAML — schema, LOCK rules, optional characters.yaml cross-check."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
SOUL_DIR = ROOT / "characters" / "soul"
CHAR_YAML = ROOT / "skills" / "academy-character-scale" / "characters.yaml"

VOL1_CORE = [
    "ito_akira_soul.yaml",
    "kato_keimi_soul.yaml",
    "matsumoto_shiro_soul.yaml",
    "riku_shun_soul.yaml",
    "riku_hikaru_soul.yaml",
]

REQUIRED_TOP = [
    "meta",
    "soul_line",
    "core_desire",
    "core_fear",
    "core_contradiction",
    "curiosity_lens",
    "curiosity_first_move",
    "thinking_bias",
    "bias_story_function",
    "emotional_triggers",
    "language_fingerprint",
    "behavior_fingerprint",
    "aesthetics_and_objects",
    "relationship_vectors",
    "growth_and_guardrails",
    "regression_scenes",
]

REQUIRED_META = [
    "character_id",
    "display_name",
    "canonical_number",
    "narrative_tier",
    "status",
    "soul_version",
    "canon_refs",
]

EMOTIONAL_KEYS = ["anger", "silence", "shy", "joy"]
LANG_KEYS = ["sentence_length", "tempo", "register", "forbidden_patterns"]
BEHAVIOR_KEYS = ["stance", "gaze", "hands", "scene_entry", "scene_exit"]
GROWTH_KEYS = ["vol1_state", "never_write", "vol1_screen_time"]


def _empty(val: object) -> bool:
    if val is None:
        return True
    if isinstance(val, str):
        return not val.strip() or val.strip() in ("—", "-")
    if isinstance(val, (list, dict)):
        return len(val) == 0
    return False


def load_characters_yaml() -> dict:
    if not CHAR_YAML.exists():
        return {}
    text = CHAR_YAML.read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
        if isinstance(data, dict) and isinstance(data.get("characters"), dict):
            return data["characters"]
    except yaml.YAMLError:
        pass
    # Fallback: characters.yaml may contain non-strict YAML in never_says notes
    chars: dict = {}
    for m in re.finditer(
        r"^  ([a-z_]+):\s*\n    display_name: \"([^\"]+)\"",
        text,
        re.MULTILINE,
    ):
        chars[m.group(1)] = {"display_name": m.group(2)}
    return chars


def lint_file(path: Path, *, strict: bool, cross_yaml: bool, chars: dict) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{path.name}: parse error: {exc}"]

    if not isinstance(data, dict):
        return [f"{path.name}: root must be mapping"]

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"{path.name}: missing top-level '{key}'")

    meta = data.get("meta") or {}
    if not isinstance(meta, dict):
        errors.append(f"{path.name}: meta must be mapping")
        meta = {}

    for key in REQUIRED_META:
        if key not in meta:
            errors.append(f"{path.name}: meta missing '{key}'")

    cid = meta.get("character_id", "")
    expected_name = f"{cid}_soul.yaml" if cid else ""
    if cid and path.name != expected_name:
        errors.append(f"{path.name}: filename must be {expected_name}")

    status = meta.get("status", "")
    if status not in ("LOCK", "V0.1", "DRAFT"):
        errors.append(f"{path.name}: unexpected status '{status}'")

    if status == "LOCK":
        if not meta.get("locked_at"):
            errors.append(f"{path.name}: LOCK requires meta.locked_at")
        if not meta.get("locked_by"):
            errors.append(f"{path.name}: LOCK requires meta.locked_by")

    if cross_yaml and cid:
        if cid not in chars:
            errors.append(f"{path.name}: character_id '{cid}' not in characters.yaml")
        elif chars[cid].get("display_name") and meta.get("display_name"):
            if chars[cid]["display_name"].replace(" ", "") != meta["display_name"].replace(" ", ""):
                errors.append(
                    f"{path.name}: display_name mismatch vs characters.yaml"
                )

    emo = data.get("emotional_triggers") or {}
    if isinstance(emo, dict):
        for k in EMOTIONAL_KEYS:
            if _empty(emo.get(k)):
                errors.append(f"{path.name}: emotional_triggers.{k} empty")
        if _empty(data.get("recovery_style")):
            errors.append(f"{path.name}: recovery_style empty")
        if _empty(data.get("apologizes_when")):
            errors.append(f"{path.name}: apologizes_when empty")

    lang = data.get("language_fingerprint") or {}
    if isinstance(lang, dict):
        for k in LANG_KEYS:
            if k == "forbidden_patterns":
                if not lang.get("forbidden_patterns"):
                    errors.append(f"{path.name}: language_fingerprint.forbidden_patterns empty")
            elif _empty(lang.get(k)):
                errors.append(f"{path.name}: language_fingerprint.{k} empty")

    beh = data.get("behavior_fingerprint") or {}
    if isinstance(beh, dict):
        for k in BEHAVIOR_KEYS:
            if _empty(beh.get(k)):
                errors.append(f"{path.name}: behavior_fingerprint.{k} empty")

    guard = data.get("growth_and_guardrails") or {}
    if isinstance(guard, dict):
        for k in GROWTH_KEYS:
            if k == "never_write":
                if not guard.get("never_write"):
                    errors.append(f"{path.name}: growth_and_guardrails.never_write empty")
            elif _empty(guard.get(k)):
                errors.append(f"{path.name}: growth_and_guardrails.{k} empty")

    rel = data.get("relationship_vectors") or {}
    if isinstance(rel, dict) and len(rel) < 2:
        errors.append(f"{path.name}: relationship_vectors need ≥2 entries")

    scenes = data.get("regression_scenes") or []
    if not scenes:
        errors.append(f"{path.name}: regression_scenes empty")
    else:
        for i, scene in enumerate(scenes):
            if not isinstance(scene, dict):
                errors.append(f"{path.name}: regression_scenes[{i}] not mapping")
                continue
            for sk in ("scene_id", "expected_first_move", "must_not"):
                if sk == "must_not":
                    if not scene.get("must_not"):
                        errors.append(f"{path.name}: regression_scenes[{i}].must_not empty")
                elif _empty(scene.get(sk)):
                    errors.append(f"{path.name}: regression_scenes[{i}].{sk} empty")

    if strict:
        for field in ("soul_line", "core_desire", "core_fear", "core_contradiction"):
            if _empty(data.get(field)):
                errors.append(f"{path.name}: {field} empty")
        aes = data.get("aesthetics_and_objects") or {}
        if isinstance(aes, dict) and not aes.get("key_props"):
            errors.append(f"{path.name}: aesthetics_and_objects.key_props empty")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint character soul YAML files")
    parser.add_argument("--vol1-core", action="store_true", help="Vol1 five core only")
    parser.add_argument("--strict", action="store_true", help="Full 12-module strict (LOCK tier)")
    parser.add_argument(
        "--cross-yaml",
        action="store_true",
        default=True,
        help="Cross-check characters.yaml (default on)",
    )
    parser.add_argument("--no-cross-yaml", action="store_true", help="Skip characters.yaml")
    parser.add_argument("files", nargs="*", help="Optional soul yaml paths")
    args = parser.parse_args()

    cross = args.cross_yaml and not args.no_cross_yaml
    chars = load_characters_yaml() if cross else {}
    strict = args.strict or args.vol1_core

    if args.files:
        paths = [Path(f) for f in args.files]
    elif args.vol1_core:
        paths = [SOUL_DIR / name for name in VOL1_CORE]
    else:
        paths = sorted(SOUL_DIR.glob("*_soul.yaml"))

    all_errors: list[str] = []
    checked = 0
    for path in paths:
        if not path.exists():
            all_errors.append(f"missing: {path}")
            continue
        checked += 1
        all_errors.extend(
            lint_file(path, strict=strict, cross_yaml=cross, chars=chars)
        )

    if all_errors:
        print(f"FAIL ({len(all_errors)} issues, {checked} files checked):")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    mode = "strict" if strict else "basic"
    print(f"PASS: {checked} soul file(s) OK ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
