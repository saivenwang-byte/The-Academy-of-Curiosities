"""Quota-based persona factory: 12 anchors + 38 generated = 50."""
from __future__ import annotations

import random
from pathlib import Path
from typing import Any

from common import CONFIG_DIR, DATA_DIR, PERSONAS_DIR, SYNTHETIC_LABEL, dump_json, load_json

MOTIVES_CHILD = [
    "尽快发现怪事",
    "看朋友关系是否真实",
    "自己也能做观察实验",
    "插图好看就继续",
    "推理谁最可疑",
    "知道风的方向秘密",
]
AVERSIONS_CHILD = [
    "连续解释超过两页",
    "汉字太多",
    "人物名字分不清",
    "线索不公平",
    "像教辅",
    "没有插图的长页",
]
MOTIVES_ADULT = [
    "安全适龄第一",
    "购买价值清晰",
    "学校可推荐",
    "亲子共读有话题",
]
MOTIVES_PRO = [
    "首章钩子与系列设计",
    "图文叙事质量",
    "名古屋校园真实性",
    "市场差异化",
    "认知负荷匹配",
]


def _pick_gender(rng: random.Random, target_f: float) -> str:
    return "F" if rng.random() < target_f else "M"


def _child_params(rng: random.Random, age: int) -> dict[str, Any]:
    low_mot = rng.random() < 0.28
    return {
        "age": age,
        "gender": _pick_gender(rng, 0.5),
        "reading_level": rng.choices(["low", "average", "high"], weights=[0.25, 0.50, 0.25])[0],
        "weekly_reading_minutes": rng.randint(10, 45) if low_mot else rng.randint(40, 200),
        "attention_span": rng.choices(["short", "medium", "long"], weights=[0.35, 0.45, 0.20])[0],
        "mystery_affinity": round(rng.uniform(0.2, 0.95), 2),
        "visual_dependency": round(rng.uniform(0.2, 0.95), 2),
        "competitor_familiarity": round(rng.uniform(0.0, 0.95), 2),
        "competitor_titles_read": [],
        "strictness": round(rng.uniform(0.25, 0.85), 2),
        "low_reading_motivation": low_mot,
        "cultural_familiarity": rng.choice(
            ["jp_native", "jp_returnee", "overseas_ja_learner", "zh_in_jp_family"]
        ),
        "language_background": "ja",
        "primary_motive": rng.choice(MOTIVES_CHILD),
        "main_aversion": rng.choice(AVERSIONS_CHILD),
    }


def _adult_params(rng: random.Random, role: str) -> dict[str, Any]:
    return {
        "age": rng.randint(32, 55),
        "gender": _pick_gender(rng, 0.55),
        "role": role,
        "reading_level": "n/a",
        "strictness": round(rng.uniform(0.35, 0.85), 2),
        "risk_sensitivity": round(rng.uniform(0.4, 0.95), 2),
        "purchase_sensitivity": round(rng.uniform(0.3, 0.9), 2),
        "cultural_familiarity": "jp_native",
        "language_background": "ja",
        "primary_motive": rng.choice(MOTIVES_ADULT),
        "main_aversion": rng.choice(["说教感", "恐怖要素", "参考書感", "语汇过难"]),
    }


def _pro_params(rng: random.Random, role: str) -> dict[str, Any]:
    return {
        "age": rng.randint(33, 58),
        "gender": _pick_gender(rng, 0.5),
        "role": role,
        "reading_level": "n/a",
        "strictness": round(rng.uniform(0.55, 0.90), 2),
        "cultural_familiarity": "jp_native",
        "language_background": "ja",
        "primary_motive": rng.choice(MOTIVES_PRO),
        "main_aversion": rng.choice(["套路化", "制度错误", "系列感弱", "图文脱节"]),
    }


def _human_summary_zh(panel: str, p: dict[str, Any]) -> str:
    if panel == "child_experience":
        age = p.get("age", "?")
        mot = p.get("primary_motive", "")
        low = "低阅读意愿" if p.get("low_reading_motivation") else "普通阅读意愿"
        return f"{age}岁儿童读者（{low}），关注：{mot}。"
    if panel == "adult_gate":
        return f"{p.get('age')}岁{p.get('role', '成人')}，关注：{p.get('primary_motive')}。"
    return f"专业视角·{p.get('role', 'pro')}，关注：{p.get('primary_motive')}。"


def _assign_child_ages(rng: random.Random, n: int, buckets: list[dict]) -> list[int]:
    ages: list[int] = []
    for b in buckets:
        lo, hi = b["ages"][0], b["ages"][-1]
        for _ in range(b["count"]):
            ages.append(rng.randint(lo, hi))
    while len(ages) < n:
        ages.append(rng.choice([10, 11, 12]))
    rng.shuffle(ages)
    return ages[:n]


def _assign_adult_roles(rng: random.Random, n: int, roles_cfg: dict[str, int]) -> list[str]:
    roles: list[str] = []
    for role, cnt in roles_cfg.items():
        roles.extend([role] * cnt)
    rng.shuffle(roles)
    return roles[:n]


def _assign_pro_roles(rng: random.Random, n: int, roles_cfg: dict[str, int]) -> list[str]:
    roles: list[str] = []
    for role, cnt in roles_cfg.items():
        roles.extend([role] * cnt)
    rng.shuffle(roles)
    return roles[:n]


def build_panel(seed: int = 20260614) -> list[dict[str, Any]]:
    quota = load_json(CONFIG_DIR / "quota_phase1.json")
    rng = random.Random(seed)
    anchors: list[dict] = load_json(DATA_DIR / "anchors_12.json")
    for a in anchors:
        a["synthetic_label"] = SYNTHETIC_LABEL

    generated: list[dict] = []
    seq = {"child_experience": 0, "adult_gate": 0, "pro_diagnosis": 0}
    prefixes = {"child_experience": "CH", "adult_gate": "AD", "pro_diagnosis": "PR"}

    def next_id(panel: str) -> str:
        seq[panel] += 1
        return f"{prefixes[panel]}-G{seq[panel]:03d}"

    # Child generated
    cp = quota["panels"]["child_experience"]
    child_ages = _assign_child_ages(rng, cp["generated"], cp["age_buckets"])
    for age in child_ages:
        p = _child_params(rng, age)
        generated.append(
            {
                "persona_id": next_id("child_experience"),
                "panel": "child_experience",
                "is_anchor": False,
                **p,
                "human_summary_zh": _human_summary_zh("child_experience", p),
                "synthetic_label": SYNTHETIC_LABEL,
            }
        )

    # Adult generated
    ap = quota["panels"]["adult_gate"]
    adult_roles = _assign_adult_roles(rng, ap["generated"], ap["roles"])
    for role in adult_roles:
        p = _adult_params(rng, role)
        generated.append(
            {
                "persona_id": next_id("adult_gate"),
                "panel": "adult_gate",
                "is_anchor": False,
                **p,
                "human_summary_zh": _human_summary_zh("adult_gate", p),
                "synthetic_label": SYNTHETIC_LABEL,
            }
        )

    # Pro generated
    pp = quota["panels"]["pro_diagnosis"]
    pro_roles = _assign_pro_roles(rng, pp["generated"], pp["roles"])
    for role in pro_roles:
        p = _pro_params(rng, role)
        generated.append(
            {
                "persona_id": next_id("pro_diagnosis"),
                "panel": "pro_diagnosis",
                "is_anchor": False,
                **p,
                "human_summary_zh": _human_summary_zh("pro_diagnosis", p),
                "synthetic_label": SYNTHETIC_LABEL,
            }
        )

    panel = anchors + generated
    assert len(panel) == quota["total"], f"Expected {quota['total']} personas, got {len(panel)}"
    assert sum(1 for p in panel if p["is_anchor"]) == quota["anchors"]
    return panel


def validate_low_motivation_ratio(panel: list[dict], min_ratio: float = 0.25) -> bool:
    children = [p for p in panel if p["panel"] == "child_experience"]
    low = sum(1 for p in children if p.get("low_reading_motivation"))
    return (low / len(children)) >= min_ratio if children else False


def write_personas(panel: list[dict], seed: int) -> Path:
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    out = PERSONAS_DIR / f"personas_50_seed{seed}.json"
    meta = {
        "status": "SIMULATION",
        "seed": seed,
        "count": len(panel),
        "anchors": sum(1 for p in panel if p["is_anchor"]),
        "generated": sum(1 for p in panel if not p["is_anchor"]),
        "personas": panel,
    }
    dump_json(out, meta)
    return out


def main() -> None:
    seed = 20260614
    panel = build_panel(seed)
    path = write_personas(panel, seed)
    low_ok = validate_low_motivation_ratio(panel, 0.25)
    print(f"Wrote {path} ({len(panel)} personas, low_motivation_ok={low_ok})")


if __name__ == "__main__":
    main()
