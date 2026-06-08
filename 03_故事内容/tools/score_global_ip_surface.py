#!/usr/bin/env python3
"""Heuristic H/C/S self-score for CN HybridVoice body files.

Reads a case body .txt, outputs humor/cute/surface scores with evidence.
Appends results to V2迁移/scores_mvp_latest.json under global_ip_surface_self.

Usage:
  python score_global_ip_surface.py 案02_*.txt
  python score_global_ip_surface.py --all   # score A001-A005
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

# Repo-relative paths
TOOLS_DIR = Path(__file__).resolve().parent
STORY_ROOT = TOOLS_DIR.parent / "第1卷_觉得奇怪就先观察"
BODY_DIR = STORY_ROOT / "正式版" / "01_正文"
SCORES_JSON = STORY_ROOT / "V2迁移" / "scores_mvp_latest.json"

# Character names (core cast + recurring)
NAMED_CHARS = [
    "陸珣", "陸瑆", "伊藤光", "松本志郎", "加藤慧美", "水野真帆",
    "光", "志郎", "慧美", "珣", "瑆", "水野",
]

# Arc spoiler phrases in 序
XU_SPOILER_PATTERNS = [
    r"五件怪事",
    r"五案",
    r"他还不知道",
    r"会像拼图",
    r"拼图",
    r"下一件怪事",
    r"卷弧",
    r"五张证物",
]

# Running gag markers per case (heuristic)
CASE_GAGS = {
    "A001": [r"更牢", r"未确认是否更牢", r"撞.*门", r"气声"],
    "A002": [r"未登记", r"登记", r"对不起"],
    "A003": [r"又查", r"无实体", r"没有贴完", r"三种"],
    "A004": [r"偏了一格", r"倾斜", r"水平仪", r"封条"],
    "A005": [r"洗不掉", r"空的", r"无影", r"仅.*无影"],
}

# Humor dialogue patterns (generic)
HUMOR_PATTERNS = [
    r"更牢",
    r"未登记",
    r"偏了一格",
    r"洗不掉",
    r"又查了",
    r"撞.*门",
    r"字面",
    r"听说.*栏",
]

# Hook keywords (first 150 chars / opening)
HOOK_KEYWORDS = [
    r"广播",
    r"对不起",
    r"海报",
    r"抽屉",
    r"封条",
    r"影子",
    r"无影",
    r"空的",
    r"禁声",
    r"唇不同步",
    r"不可能",
    r"锁着",
    r"空栏",
]

# Cute: desire+gap markers
CUTE_MARKERS = [
    (r"想被信|想.*信", "渴望：被相信"),
    (r"说不出|禁声|气声", "缺口：说不出"),
    (r"银框|开衫|低马尾", "慧美可画外形"),
    (r"绿格|绿背心|胶带|扎带", "志郎可画外形"),
    (r"橙红|导播|背心", "光可画外形"),
    (r"撞.*门|看的是.*车", "珣可画习惯"),
    (r"社徽|翘角|观察眼", "mascot种子"),
    (r"笔记墙|证物盒|空.*壁报", "想加入空间"),
]


def detect_case_id(text: str, path: Path) -> str:
    m = re.search(r"案0(\d)", path.name)
    if m:
        return f"A00{m.group(1)}"
    if "一、" in text[:2000]:
        return "A001"
    if "二、" in text[:2000]:
        return "A002"
    if "三、" in text[:2000]:
        return "A003"
    if "四、" in text[:2000]:
        return "A004"
    if "五、" in text[:2000]:
        return "A005"
    return "UNKNOWN"


def extract_xu_and_opening(text: str) -> tuple[str, str, str]:
    """Return (xu_section, first_150_chars, opening_800_chars)."""
    # Find 序 section
    xu_match = re.search(
        r"(序[^\n]*\n[-=]+\n)(.*?)(?=\n[一二三四五]、|\Z)",
        text,
        re.DOTALL,
    )
    xu = xu_match.group(2) if xu_match else ""

    # Strip header boilerplate for opening measure
    body_start = re.search(r"[一二三四五]、", text)
    if body_start:
        main = text[body_start.start() :]
    else:
        main = text

    # Flatten whitespace for char count
    flat = re.sub(r"\s+", "", main)
    first_150 = flat[:150]
    opening_800 = flat[:800]
    return xu, first_150, opening_800


def count_named_in_opening(opening: str) -> tuple[int, list[str]]:
    found = []
    for name in NAMED_CHARS:
        if name in opening and name not in found:
            # Avoid double-counting 光 when 伊藤光 present
            if name == "光" and "伊藤光" in opening:
                continue
            if name == "志郎" and "松本志郎" in opening:
                continue
            if name == "慧美" and "加藤慧美" in opening:
                continue
            if name == "珣" and "陸珣" in opening:
                continue
            if name == "瑆" and "陸瑆" in opening:
                continue
            if name == "水野" and "水野真帆" in opening:
                continue
            found.append(name)
    # Dedupe by normalizing to family
    core = set()
    mapping = {
        "伊藤光": "光", "松本志郎": "志郎", "加藤慧美": "慧美",
        "陸珣": "珣", "陸瑆": "瑆", "水野真帆": "水野",
    }
    for n in found:
        core.add(mapping.get(n, n))
    return len(core), sorted(core)


def score_humor(text: str, case_id: str, xu: str, opening: str) -> dict:
    scan = xu + opening + text[:4000]
    gags = CASE_GAGS.get(case_id, HUMOR_PATTERNS)
    hits = []
    for pat in gags + HUMOR_PATTERNS:
        for m in re.finditer(pat, scan):
            snippet = scan[max(0, m.start() - 10) : m.end() + 20].replace("\n", " ")[:60]
            hits.append({"pattern": pat, "snippet": snippet.strip()})

    # Dedupe by snippet
    seen = set()
    unique = []
    for h in hits:
        key = h["snippet"][:30]
        if key not in seen:
            seen.add(key)
            unique.append(h)

    gag_count = len(unique)
    char_count = len(re.sub(r"\s+", "", xu + opening))
    laughs_per_800 = round(gag_count / max(char_count / 800, 0.1), 2)

    # Score heuristic
    score = 3.0
    running = sum(1 for h in unique if any(re.search(p, h["snippet"]) for p in (gags or [])))
    if running >= 2:
        score += 2.5
    elif running >= 1:
        score += 1.0
    if laughs_per_800 >= 1.0:
        score += 1.5
    elif laughs_per_800 >= 0.5:
        score += 0.5
    score = min(score, 8.0)  # cap — no fake 9+

    return {
        "score": round(score, 1),
        "running_gag_hits": running,
        "laughs_per_800w": laughs_per_800,
        "evidence": [h["snippet"] for h in unique[:5]],
        "note": "cap 8 · E20-H1 required for 9+",
    }


def score_cute(text: str, opening: str) -> dict:
    scan = opening + text[:3000]
    evidence = []
    for pat, label in CUTE_MARKERS:
        if re.search(pat, scan):
            evidence.append(label)
    evidence = list(dict.fromkeys(evidence))  # dedupe preserve order

    score = 3.0
    if len(evidence) >= 6:
        score = 7.5
    elif len(evidence) >= 4:
        score = 6.5
    elif len(evidence) >= 2:
        score = 5.0
    if any("mascot" in e or "想加入" in e for e in evidence):
        score = min(score + 0.5, 8.0)
    score = min(score, 8.0)

    return {
        "score": round(score, 1),
        "markers_hit": len(evidence),
        "evidence": evidence[:8],
        "note": "cap 8 · E20-C1/J1 for character memory",
    }


def score_surface(text: str, xu: str, first_150: str, opening: str) -> dict:
    hook_hits = [kw for kw in HOOK_KEYWORDS if re.search(kw, first_150)]
    spoiler = [p for p in XU_SPOILER_PATTERNS if re.search(p, xu)]
    named_count, named_list = count_named_in_opening(opening)

    score = 3.0
    if len(hook_hits) >= 2:
        score += 2.5
    elif len(hook_hits) >= 1:
        score += 1.5
    if not spoiler:
        score += 1.5
    else:
        score -= 2.0
    if named_count <= 4:
        score += 1.5
    elif named_count <= 5:
        score += 0.5
    else:
        score -= 1.0
    score = max(0, min(score, 8.0))

    return {
        "score": round(score, 1),
        "hook_keywords_in_first_150": hook_hits,
        "opening_named_chars": named_count,
        "named_list": named_list,
        "arc_spoiler_in_xu": bool(spoiler),
        "spoiler_phrases": spoiler,
        "evidence": [
            f"前150字含: {', '.join(hook_hits) or '（无）'}",
            f"开篇角色数: {named_count} ({', '.join(named_list)})",
            f"序剧透: {'是' if spoiler else '否'}",
        ],
        "note": "cap 8 · E20-04续读 for hook validation",
    }


def score_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    case_id = detect_case_id(text, path)
    xu, first_150, opening = extract_xu_and_opening(text)

    h = score_humor(text, case_id, xu, opening)
    c = score_cute(text, opening)
    s = score_surface(text, xu, first_150, opening)

    return {
        "case": case_id,
        "file": str(path.name),
        "date": date.today().isoformat(),
        "humor_H": h,
        "cute_C": c,
        "surface_S": s,
        "composite_avg": round((h["score"] + c["score"] + s["score"]) / 3, 2),
        "verified": "pending_E20",
        "disclaimer": "heuristic self-score · NOT G-BODY PASS",
    }


def find_case_files() -> list[Path]:
    return sorted(BODY_DIR.glob("案0*_HybridVoice_V2.0.txt"))


def append_to_scores_json(results: list[dict]) -> None:
    if SCORES_JSON.exists():
        data = json.loads(SCORES_JSON.read_text(encoding="utf-8"))
    else:
        data = {}

    block = data.setdefault("global_ip_surface_self", {})
    block["tool"] = "score_global_ip_surface.py"
    block["date"] = date.today().isoformat()
    block["method"] = "heuristic H/C/S · cap 8 · NOT E20"
    cases = block.setdefault("cases", {})
    for r in results:
        cases[r["case"]] = r

    SCORES_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="H/C/S global IP surface self-score")
    parser.add_argument("files", nargs="*", help="CN body txt files")
    parser.add_argument("--all", action="store_true", help="Score all A001-A005")
    parser.add_argument("--json-only", action="store_true", help="Print JSON only")
    parser.add_argument("--no-write", action="store_true", help="Skip scores_mvp_latest.json")
    args = parser.parse_args(argv)

    paths: list[Path] = []
    if args.all:
        paths = find_case_files()
    else:
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = BODY_DIR / p.name if (BODY_DIR / p.name).exists() else Path(f)
            paths.append(p)

    if not paths:
        parser.print_help()
        return 1

    results = []
    for p in paths:
        if not p.exists():
            print(f"ERROR: not found: {p}", file=sys.stderr)
            return 1
        r = score_file(p)
        results.append(r)

    if not args.no_write:
        append_to_scores_json(results)

    if args.json_only:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"\n=== {r['case']} · {r['file']} ===")
            print(f"  H={r['humor_H']['score']}  C={r['cute_C']['score']}  S={r['surface_S']['score']}  avg={r['composite_avg']}")
            print(f"  H evidence: {r['humor_H']['evidence'][:2]}")
            print(f"  S: chars={r['surface_S']['opening_named_chars']} spoiler={r['surface_S']['arc_spoiler_in_xu']}")
        if not args.no_write:
            print(f"\n→ appended to {SCORES_JSON}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
