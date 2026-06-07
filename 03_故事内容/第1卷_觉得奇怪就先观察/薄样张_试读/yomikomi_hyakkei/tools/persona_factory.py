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
FRIENDSHIP_MOTIVES = {"看朋友关系是否真实", "插图好看就继续"}
SCIENCE_MOTIVES = {"自己也能做观察实验", "知道风的方向秘密"}
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


def _child_params(rng: random.Random, age: int, *, force_low_mot: bool | None = None) -> dict[str, Any]:
    low_mot = force_low_mot if force_low_mot is not None else rng.random() < 0.28
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


def _age_in_bucket(age: int, bucket: dict) -> bool:
    lo, hi = bucket["ages"][0], bucket["ages"][-1]
    return lo <= age <= hi


def _bucket_index(age: int, buckets: list[dict]) -> int | None:
    for i, b in enumerate(buckets):
        if _age_in_bucket(age, b):
            return i
    return None


def _remaining_age_slots(anchors: list[dict], buckets: list[dict]) -> list[int]:
    """Return exact ages for generated children after subtracting anchor occupancy."""
    remaining_counts = [b["count"] for b in buckets]
    for a in anchors:
        if a.get("panel") != "child_experience":
            continue
        idx = _bucket_index(int(a["age"]), buckets)
        if idx is None:
            raise ValueError(f"anchor age {a['age']} outside buckets: {a.get('persona_id')}")
        remaining_counts[idx] -= 1
        if remaining_counts[idx] < 0:
            raise ValueError(f"anchor overfills bucket {idx}: {a.get('persona_id')}")

    ages: list[int] = []
    for b, rem in zip(buckets, remaining_counts):
        if rem < 0:
            raise ValueError(f"negative bucket remainder: {b}")
        lo, hi = b["ages"][0], b["ages"][-1]
        for _ in range(rem):
            ages.append(lo if lo == hi else random.choice(list(range(lo, hi + 1))))
    return ages


def _remaining_roles(anchors: list[dict], roles_cfg: dict[str, int], panel: str) -> list[str]:
    remaining = dict(roles_cfg)
    for a in anchors:
        if a.get("panel") != panel:
            continue
        role = a.get("role")
        if role not in remaining:
            raise ValueError(f"anchor role {role!r} not in quota: {a.get('persona_id')}")
        remaining[role] -= 1
        if remaining[role] < 0:
            raise ValueError(f"anchor overfills role {role}: {a.get('persona_id')}")

    roles: list[str] = []
    for role, cnt in remaining.items():
        if cnt < 0:
            raise ValueError(f"negative role remainder: {role}")
        roles.extend([role] * cnt)
    return roles


def _count_child_metric(children: list[dict], key: str, predicate) -> int:
    return sum(1 for p in children if predicate(p))


def _enforce_child_attribute_targets(
    generated: list[dict], anchors: list[dict], targets: dict[str, int], rng: random.Random
) -> None:
    """Patch generated child personas so panel-wide attribute mins are met."""
    anchor_children = [a for a in anchors if a.get("panel") == "child_experience"]
    all_children = anchor_children + generated

    def need(attr: str, current: int, target: int) -> int:
        return max(0, target - current)

    comp_need = need(
        "competitor_familiarity_high",
        _count_child_metric(all_children, "competitor_familiarity", lambda p: float(p.get("competitor_familiarity", 0)) >= 0.6),
        targets.get("competitor_familiarity_high", 0),
    )
    low_read_need = need(
        "reading_level_low",
        sum(1 for p in all_children if p.get("reading_level") == "low"),
        targets.get("reading_level_low", 0),
    )
    visual_need = need(
        "visual_dependency_high",
        _count_child_metric(all_children, "visual_dependency", lambda p: float(p.get("visual_dependency", 0)) >= 0.7),
        targets.get("visual_dependency_high", 0),
    )
    mystery_need = need(
        "mystery_affinity_high",
        _count_child_metric(all_children, "mystery_affinity", lambda p: float(p.get("mystery_affinity", 0)) >= 0.7),
        targets.get("mystery_affinity_high", 0),
    )
    friend_need = need(
        "character_friendship_focus",
        sum(1 for p in all_children if p.get("primary_motive") in FRIENDSHIP_MOTIVES),
        targets.get("character_friendship_focus", 0),
    )
    science_need = need(
        "science_knowledge_focus",
        sum(1 for p in all_children if p.get("primary_motive") in SCIENCE_MOTIVES),
        targets.get("science_knowledge_focus", 0),
    )

    pool = list(generated)
    rng.shuffle(pool)

    def take(n: int) -> list[dict]:
        nonlocal pool
        n = min(n, len(pool))
        picked, pool = pool[:n], pool[n:]
        return picked

    for p in take(comp_need):
        p["competitor_familiarity"] = round(rng.uniform(0.6, 0.95), 2)
    for p in take(low_read_need):
        p["reading_level"] = "low"
        p["low_reading_motivation"] = True
    for p in take(visual_need):
        p["visual_dependency"] = round(rng.uniform(0.7, 0.95), 2)
    for p in take(mystery_need):
        p["mystery_affinity"] = round(rng.uniform(0.7, 0.95), 2)
    for p in take(friend_need):
        p["primary_motive"] = rng.choice(list(FRIENDSHIP_MOTIVES))
    for p in take(science_need):
        p["primary_motive"] = rng.choice(list(SCIENCE_MOTIVES))


def validate_panel_quotas(panel: list[dict], quota: dict[str, Any] | None = None) -> dict[str, Any]:
    quota = quota or load_json(CONFIG_DIR / "quota_phase1.json")
    errors: list[str] = []
    checks: dict[str, Any] = {}

    if len(panel) != quota["total"]:
        errors.append(f"total {len(panel)} != {quota['total']}")
    anchor_n = sum(1 for p in panel if p.get("is_anchor"))
    if anchor_n != quota["anchors"]:
        errors.append(f"anchors {anchor_n} != {quota['anchors']}")

    for panel_name, pcfg in quota["panels"].items():
        members = [p for p in panel if p.get("panel") == panel_name]
        checks[f"{panel_name}_count"] = len(members)
        if len(members) != pcfg["count"]:
            errors.append(f"{panel_name} count {len(members)} != {pcfg['count']}")

        if panel_name == "child_experience":
            buckets = pcfg["age_buckets"]
            for i, b in enumerate(buckets):
                lo, hi = b["ages"][0], b["ages"][-1]
                cnt = sum(1 for p in members if lo <= int(p.get("age", 0)) <= hi)
                checks[f"age_bucket_{i}"] = {"target": b["count"], "actual": cnt, "ages": b["ages"]}
                if cnt != b["count"]:
                    errors.append(f"child age bucket {b['ages']} count {cnt} != {b['count']}")
        else:
            roles_cfg = pcfg["roles"]
            for role, target in roles_cfg.items():
                cnt = sum(1 for p in members if p.get("role") == role)
                checks[f"{panel_name}_role_{role}"] = {"target": target, "actual": cnt}
                if cnt != target:
                    errors.append(f"{panel_name} role {role} count {cnt} != {target}")

    children = [p for p in panel if p.get("panel") == "child_experience"]
    low = sum(1 for p in children if p.get("low_reading_motivation"))
    min_ratio = quota["panels"]["child_experience"].get("low_reading_motivation_min_ratio", 0.25)
    checks["low_reading_motivation_ratio"] = round(low / len(children), 3) if children else 0
    if children and (low / len(children)) < min_ratio:
        errors.append(f"low_reading_motivation ratio {low/len(children):.3f} < {min_ratio}")

    return {"valid": len(errors) == 0, "errors": errors, "checks": checks}


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

    cp = quota["panels"]["child_experience"]
    child_ages = _remaining_age_slots(anchors, cp["age_buckets"])
    if len(child_ages) != cp["generated"]:
        raise ValueError(f"child generated ages {len(child_ages)} != {cp['generated']}")
    rng.shuffle(child_ages)
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

    child_gen = [g for g in generated if g["panel"] == "child_experience"]
    _enforce_child_attribute_targets(child_gen, anchors, cp.get("attribute_targets", {}), rng)

    ap = quota["panels"]["adult_gate"]
    adult_roles = _remaining_roles(anchors, ap["roles"], "adult_gate")
    if len(adult_roles) != ap["generated"]:
        raise ValueError(f"adult generated roles {len(adult_roles)} != {ap['generated']}")
    rng.shuffle(adult_roles)
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

    pp = quota["panels"]["pro_diagnosis"]
    pro_roles = _remaining_roles(anchors, pp["roles"], "pro_diagnosis")
    if len(pro_roles) != pp["generated"]:
        raise ValueError(f"pro generated roles {len(pro_roles)} != {pp['generated']}")
    rng.shuffle(pro_roles)
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
    v = validate_panel_quotas(panel, quota)
    if not v["valid"]:
        raise ValueError("panel quota validation failed: " + "; ".join(v["errors"]))
    return panel


def validate_low_motivation_ratio(panel: list[dict], min_ratio: float = 0.25) -> bool:
    children = [p for p in panel if p["panel"] == "child_experience"]
    low = sum(1 for p in children if p.get("low_reading_motivation"))
    return (low / len(children)) >= min_ratio if children else False


def write_personas(panel: list[dict], seed: int) -> Path:
    PERSONAS_DIR.mkdir(parents=True, exist_ok=True)
    out = PERSONAS_DIR / f"personas_50_seed{seed}.json"
    quota_ok = validate_panel_quotas(panel)
    meta = {
        "status": "SIMULATION",
        "seed": seed,
        "count": len(panel),
        "anchors": sum(1 for p in panel if p["is_anchor"]),
        "generated": sum(1 for p in panel if not p["is_anchor"]),
        "quota_validation": quota_ok,
        "personas": panel,
    }
    dump_json(out, meta)
    return out


def main() -> None:
    seed = 20260614
    panel = build_panel(seed)
    path = write_personas(panel, seed)
    low_ok = validate_low_motivation_ratio(panel, 0.25)
    q = validate_panel_quotas(panel)
    print(f"Wrote {path} ({len(panel)} personas, low_motivation_ok={low_ok}, quota_valid={q['valid']})")


if __name__ == "__main__":
    main()
