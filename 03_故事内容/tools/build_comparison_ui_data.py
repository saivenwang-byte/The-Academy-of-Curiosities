#!/usr/bin/env python3
"""Build comparison_data.json for 三稿对比审读 UI.

Pulls three git versions per case (原稿 / 修改1稿 / 修改2稿), scores,
R16 changelogs, and paragraph-level diff highlights.

Usage:
  python build_comparison_ui_data.py
  python build_comparison_ui_data.py --repo /path/to/repo
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent.parent
STORY_ROOT = TOOLS_DIR.parent / "第1卷_觉得奇怪就先观察"
BODY_DIR = STORY_ROOT / "正式版" / "01_正文"
UI_DIR = STORY_ROOT / "正式版" / "06_审读对比UI"
SCORES_JSON = STORY_ROOT / "V2迁移" / "scores_mvp_latest.json"
A001_COMPARE_MD = STORY_ROOT / "V2迁移" / "37_A001_R16_原稿对比表_V0.1.md"

COMMIT_DRAFT0 = "050f810"  # R15 baseline (parent of A001 R16)
COMMIT_DRAFT1 = "a374cb7"  # A001-only R16
COMMIT_DRAFT2 = "b0adc91"  # Full five-case R16 + H/C/S

GIT_BODY_PREFIX = "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"

CASES = [
    ("A001", "案01_全班都听见了他的声音_HybridVoice_V2.0.txt", "全班都听见了他的声音"),
    ("A002", "案02_没有人写过的道歉_HybridVoice_V2.0.txt", "没有人写过的道歉"),
    ("A003", "案03_每个人都记得的海报_HybridVoice_V2.0.txt", "每个人都记得的海报"),
    ("A004", "案04_只出现在她抽屉里的失物_HybridVoice_V2.0.txt", "只出现在她抽屉里的失物"),
    ("A005", "案05_午休后消失的影子_HybridVoice_V2.0.txt", "午休后消失的影子"),
]

DIMENSION_TAGS = {
    "M1": "幽默",
    "M2": "钩子",
    "M3": "角色",
    "M4": "观察社",
    "M5": "减负",
    "M6": "视觉签名",
}

# Expert pre-R16 baseline (CC doc 2026-06-07) → maps to H/C/S display
HCS_EXPERT_BEFORE = {
    "humor_H": 3.0,
    "cute_C": 5.0,
    "surface_S": 5.0,
}


def git_show(repo: Path, commit: str, rel_path: str) -> str:
    full = f"{GIT_BODY_PREFIX}/{rel_path}"
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{full}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git show {commit}:{full} failed:\n{result.stderr.strip()}"
        )
    return result.stdout


def split_paragraphs(text: str) -> list[str]:
    blocks = re.split(r"\n\s*\n", text.strip())
    return [b.strip() for b in blocks if b.strip()]


def paragraph_diff_flags(base: list[str], other: list[str]) -> list[bool]:
    """Mark paragraphs in `other` that differ from aligned base."""
    if base == other:
        return [False] * len(other)
    sm = SequenceMatcher(None, base, other)
    changed_indices: set[int] = set()
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        for j in range(j1, j2):
            changed_indices.add(j)
    return [j in changed_indices for j in range(len(other))]


def parse_r16_changelog(md_path: Path) -> list[dict]:
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    items: list[dict] = []
    in_summary = False
    for line in text.splitlines():
        if line.strip() == "## 改动摘要":
            in_summary = True
            continue
        if in_summary and line.startswith("## "):
            break
        if not in_summary:
            continue
        if not line.startswith("|") or line.startswith("|------") or "维度" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 3:
            continue
        dim, before, after = cols[0], cols[1], cols[2]
        tags: list[str] = []
        tag_match = re.findall(r"M[1-6]", line)
        for t in tag_match:
            label = DIMENSION_TAGS.get(t, t)
            if label not in tags:
                tags.append(label)
        items.append(
            {
                "dimension": dim,
                "before": before,
                "after": after,
                "tags": tags,
                "summary": f"{dim}：{before} → {after}",
            }
        )
    return items


def parse_a001_compare_table(md_path: Path) -> list[dict]:
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    items: list[dict] = []
    in_section = False
    for line in text.splitlines():
        if line.strip().startswith("## 1. 维度总表"):
            in_section = True
            continue
        if in_section and line.strip().startswith("## 2."):
            break
        if not in_section:
            continue
        if not line.startswith("|") or line.startswith("|------") or "维度" in line:
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 4:
            continue
        dim, before, after, change_type = cols[0], cols[1], cols[2], cols[3]
        tags: list[str] = []
        for t in re.findall(r"M[1-6]", change_type):
            label = DIMENSION_TAGS.get(t, t)
            if label not in tags:
                tags.append(label)
        items.append(
            {
                "dimension": dim.strip("*"),
                "before": before,
                "after": after,
                "tags": tags,
                "change_type": change_type,
                "summary": f"{dim.strip('*')}（{change_type}）",
            }
        )
    return items


def build_scores(scores: dict, case_id: str) -> dict:
    case = scores.get("cases", {}).get(case_id, {})
    gip = scores.get("global_ip_expert", {})
    gip_dims = gip.get("dimensions", {})
    self_case = scores.get("global_ip_surface_self", {}).get("cases", {}).get(case_id, {})
    g_body = scores.get("g_body", {})

    h_after = self_case.get("humor_H", {}).get("score")
    c_after = self_case.get("cute_C", {}).get("score")
    s_after = self_case.get("surface_S", {}).get("score")

    def arrow(before, after):
        if before is None or after is None:
            return None
        return {"before": before, "after": after, "delta": round(after - before, 1)}

    return {
        "expert_panel": {
            "文学卷专家": arrow(None, case.get("expert")),
            "机制科学": {
                "note": scores.get("blockers", [""])[0] if scores.get("blockers") else "",
                "illustration_executability": case.get("illustration_executability"),
            },
            "global_ip_soul_avg": gip.get("soul_dimensions_avg"),
            "global_ip_body_avg_before": gip.get("body_dimensions_avg"),
            "幽默_H": arrow(HCS_EXPERT_BEFORE["humor_H"], h_after),
            "可爱_C": arrow(HCS_EXPERT_BEFORE["cute_C"], c_after),
            "表层_S": arrow(HCS_EXPERT_BEFORE["surface_S"], s_after),
            "expert_dimensions": {
                k: v.get("expert") if isinstance(v, dict) else v
                for k, v in gip_dims.items()
            },
        },
        "reader_panel": {
            "卷读者": arrow(None, case.get("reader")),
            "unit_reader": scores.get("卷读者"),
            "e20_probes": {
                "status": scores.get("e20_real", {}).get("status", "NOT_RUN"),
                "H1_笑过吗": None,
                "J1_想加入吗": None,
                "C1_角色记忆": None,
                "slots": f"{scores.get('e20_real', {}).get('slots_filled', 0)}/"
                f"{scores.get('e20_real', {}).get('slots_total', 12)}",
            },
        },
        "good": case.get("good", []),
        "bad": case.get("bad", []),
        "why": case.get("why", ""),
        "recommend": case.get("recommend", ""),
        "r16_changelog": case.get("r16_changelog", ""),
        "hcs_self": {
            "H": self_case.get("humor_H"),
            "C": self_case.get("cute_C"),
            "S": self_case.get("surface_S"),
            "composite_avg": self_case.get("composite_avg"),
            "verified": self_case.get("verified"),
        },
        "g_body": {
            "literary_expert": g_body.get("literary_expert"),
            "literary_reader": g_body.get("literary_reader"),
        },
    }


def build_case(repo: Path, case_id: str, filename: str, title: str, scores: dict) -> dict:
    rel = filename
    draft0 = git_show(repo, COMMIT_DRAFT0, rel)
    draft1 = git_show(repo, COMMIT_DRAFT1, rel)
    draft2 = git_show(repo, COMMIT_DRAFT2, rel)

    p0 = split_paragraphs(draft0)
    p1 = split_paragraphs(draft1)
    p2 = split_paragraphs(draft2)

    draft1_same_as_draft0 = draft0 == draft1
    highlight_d1 = paragraph_diff_flags(p0, p1) if not draft1_same_as_draft0 else [False] * len(p1)
    highlight_d2 = paragraph_diff_flags(p1, p2) if draft1 != draft2 else [False] * len(p2)

    r16_md = BODY_DIR / filename.replace(".txt", "_R16_globalIP.md")
    changes = parse_r16_changelog(r16_md)
    if case_id == "A001":
        a001_extra = parse_a001_compare_table(A001_COMPARE_MD)
        if a001_extra:
            changes = a001_extra + [c for c in changes if c not in a001_extra]

    return {
        "id": case_id,
        "title": title,
        "filename": filename,
        "version_mapping": {
            "原稿": {"commit": COMMIT_DRAFT0, "label": "R15 baseline"},
            "修改1稿": {
                "commit": COMMIT_DRAFT1,
                "label": "A001 R16 wave" if case_id == "A001" else "同原稿（A002-A005 待 R16）",
                "same_as_原稿": draft1_same_as_draft0,
            },
            "修改2稿": {"commit": COMMIT_DRAFT2, "label": "Full R16 + H/C/S"},
        },
        "stats": {
            "chars_原稿": len(draft0),
            "chars_修改1稿": len(draft1),
            "chars_修改2稿": len(draft2),
            "paragraphs_原稿": len(p0),
            "paragraphs_修改1稿": len(p1),
            "paragraphs_修改2稿": len(p2),
            "changed_p1_vs_p0": sum(highlight_d1),
            "changed_p2_vs_p1": sum(highlight_d2),
        },
        "drafts": {
            "原稿": {"text": draft0, "paragraphs": p0, "highlights": [False] * len(p0)},
            "修改1稿": {"text": draft1, "paragraphs": p1, "highlights": highlight_d1},
            "修改2稿": {"text": draft2, "paragraphs": p2, "highlights": highlight_d2},
        },
        "changes": changes,
        "scores": build_scores(scores, case_id),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build 三稿对比 UI data")
    parser.add_argument("--repo", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    repo = args.repo.resolve()

    if not SCORES_JSON.exists():
        print(f"Missing scores: {SCORES_JSON}", file=sys.stderr)
        return 1

    scores = json.loads(SCORES_JSON.read_text(encoding="utf-8"))
    UI_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": __import__("datetime").date.today().isoformat(),
        "version_mapping_global": {
            "原稿": {
                "commit": COMMIT_DRAFT0,
                "meaning": "Pre–global-IP R16 (R15 baseline)",
            },
            "修改1稿": {
                "commit": COMMIT_DRAFT1,
                "meaning": "A001-only R16 wave; A002-A005 同原稿",
            },
            "修改2稿": {
                "commit": COMMIT_DRAFT2,
                "meaning": "Full five-case R16 + H/C/S specs",
            },
        },
        "scores_meta": {
            "source": str(SCORES_JSON.relative_to(repo)),
            "ralph_iter": scores.get("ralph_iter"),
            "method": scores.get("method"),
            "global_ip_source": scores.get("global_ip_expert", {}).get("source"),
        },
        "cases": [build_case(repo, cid, fn, title, scores) for cid, fn, title in CASES],
    }

    json_path = UI_DIR / "comparison_data.json"
    js_path = UI_DIR / "comparison_data.js"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    js_path.write_text(
        "window.__COMPARISON_DATA__ = "
        + json.dumps(payload, ensure_ascii=False)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {json_path} ({json_path.stat().st_size:,} bytes)")
    print(f"Wrote {js_path} ({js_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
