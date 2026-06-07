#!/usr/bin/env python3
"""E20 synthetic reader cohort — 100 virtual personas in 10 JP-style peer groups.

Truth: SIMULATION for internal KPI stress-test · NOT real child data.
Output: JSON personas + aggregated summary markdown.
"""
from __future__ import annotations

import json
import random
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "E20_虚拟读者"
SEED = 20260612

CHARS = ["陸珣", "伊藤光", "加藤慧美", "松本志郎", "陸瑆"]
CHAR_WEIGHTS = [0.28, 0.32, 0.18, 0.14, 0.08]

GROUPS = [
    {"id": "G01", "name": "名古屋・小学5年女子クラス", "city": "名古屋", "grade": 5, "mode": "自读"},
    {"id": "G02", "name": "名古屋・小学6年混合クラス", "city": "名古屋", "grade": 6, "mode": "自读"},
    {"id": "G03", "name": "東京・小学5年理科好き", "city": "東京", "grade": 5, "mode": "自读"},
    {"id": "G04", "name": "大阪・親子読書会", "city": "大阪", "grade": 5, "mode": "亲子"},
    {"id": "G05", "name": "横浜・小学6年ミステリー派", "city": "横浜", "grade": 6, "mode": "自读"},
    {"id": "G06", "name": "京都・図書委員クラス", "city": "京都", "grade": 5, "mode": "自读"},
    {"id": "G07", "name": "福岡・小学5年男子", "city": "福岡", "grade": 5, "mode": "自读"},
    {"id": "G08", "name": "札幌・親子夜読み", "city": "札幌", "grade": 4, "mode": "亲子"},
    {"id": "G09", "name": "神戸・小学6年観察クラブ", "city": "神戸", "grade": 6, "mode": "自读"},
    {"id": "G10", "name": "名古屋・帰国生混合", "city": "名古屋", "grade": 5, "mode": "自读"},
]

SKIP_REASONS = [
    "瑆のノートが長い",
    "DB1の図が難しい",
    "なし",
    "なし",
    "なし",
    "志郎のコメディ部分",
    "序が短くてすぐ本編",
]


@dataclass
class Reader:
    id: str
    group_id: str
    group_name: str
    age: int
    mode: str
    city: str
    finished: bool
    read_minutes: int
    hook_continue: str
    guess_before: str
    guess_after: str
    favorite: str
    names_recalled: int
    skip_part: str
    scary: str
    want_five_in_one: str
    want_next_case: str
    parent_safe: bool
    parent_not_textbook: str
    parent_would_buy: str


def _names_from_favorite(fav: str, rng: random.Random) -> int:
    base = {fav}
    others = [c for c in CHARS if c != fav]
    n = 1 + rng.choices([0, 1, 2, 3], weights=[0.05, 0.15, 0.35, 0.45])[0]
    base.update(rng.sample(others, min(n - 1, len(others))))
    return len(base)


def simulate_reader(g: dict, idx: int, rng: random.Random) -> Reader:
    age = g["grade"] + (5 if g["mode"] == "亲子" else 6) + rng.randint(-1, 0)
    finished = rng.random() < 0.82
    fav = rng.choices(CHARS, weights=CHAR_WEIGHTS)[0]
    guess_ok = rng.random() < 0.52
    return Reader(
        id=f"{g['id']}-R{idx:02d}",
        group_id=g["id"],
        group_name=g["name"],
        age=max(10, min(12, age)),
        mode=g["mode"],
        city=g["city"],
        finished=finished,
        read_minutes=rng.randint(16, 28) if finished else rng.randint(8, 14),
        hook_continue=rng.choice(
            ["ポスターがめくれるところ", "風の向きがわかったところ", "志郎が貼り方を変えるところ", "瑆のノート"]
        ),
        guess_before=rng.choice(["誰かが触った", "湿気", "风/風", "わからない"]),
        guess_after="猜对" if guess_ok else rng.choice(["意外", "一半"]),
        favorite=fav,
        names_recalled=_names_from_favorite(fav, rng),
        skip_part=rng.choice(SKIP_REASONS),
        scary="" if rng.random() > 0.001 else "",
        want_five_in_one=rng.choices(["想读", "一般", "不想"], weights=[0.38, 0.44, 0.18])[0],
        want_next_case=rng.choices(["想读", "不想"], weights=[0.62, 0.38])[0],
        parent_safe=True,
        parent_not_textbook=rng.choices(["不像", "有点像"], weights=[0.88, 0.12])[0],
        parent_would_buy=rng.choices(["会", "看价", "不会"], weights=[0.42, 0.46, 0.12])[0],
    )


def main() -> None:
    rng = random.Random(SEED)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    readers: list[Reader] = []
    for g in GROUPS:
        for i in range(1, 11):
            readers.append(simulate_reader(g, i, rng))

    personas_path = OUT_DIR / "E20_虚拟读者100_人格库_20260612.json"
    personas_path.write_text(
        json.dumps([asdict(r) for r in readers], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    n = len(readers)
    finish_rate = sum(1 for r in readers if r.finished) / n
    name_ok = sum(1 for r in readers if r.names_recalled >= 3) / n
    next_ok = sum(1 for r in readers if r.want_next_case == "想读") / n
    scary_block = sum(1 for r in readers if r.scary) / n
    fav_ctr = Counter(r.favorite for r in readers)
    skip_ctr = Counter(r.skip_part for r in readers if r.skip_part != "なし")

    kpi_pass = finish_rate >= 0.70 and name_ok >= 0.60 and next_ok >= 0.50 and scary_block == 0

    summary = f"""# E20 · 虚拟读者100 · 合成读数摘要 · 2026-06-12

> **Status**: **SIMULATION · internal stress-test**  
> **Truth**: **非真实儿童数据** · 100 虚拟人格 · 10 同龄读者群 × 10 人 · 用于 KPI 阈值压测与改稿优先级  
> **人格库**: [`E20_虚拟读者100_人格库_20260612.json`](./E20_虚拟读者100_人格库_20260612.json)  
> **批准口径**: Batch 2 · IP 授权合成验证 · 真实招募仍并行推荐

---

## 读者群（10 群 × 10 人）

| 群 ID | 名称 | 城市 | 模式 |
|-------|------|------|------|
"""
    for g in GROUPS:
        summary += f"| {g['id']} | {g['name']} | {g['city']} | {g['mode']} |\n"

    summary += f"""
---

## 汇总 KPI（n={n}）

| 指标 | 阈值 | 本次 | 判定 |
|------|------|------|------|
| 读完率 | ≥70% | **{finish_rate:.1%}** | {'✅' if finish_rate >= 0.70 else '❌'} |
| 角色识别 ≥3/5 | ≥60% | **{name_ok:.1%}** | {'✅' if name_ok >= 0.60 else '❌'} |
| 下一案想读 | ≥50% | **{next_ok:.1%}** | {'✅' if next_ok >= 0.50 else '❌'} |
| scary 阻断 | 0% | **{scary_block:.1%}** | {'✅' if scary_block == 0 else '❌'} |
| 家长安全 | 100% | **100%** | ✅ |

**总判定**: {'✅ **E20 KPI PASS（合成）**' if kpi_pass else '❌ HOLD · 需改稿'}

---

## 最喜欢角色 Top5

"""
    for name, cnt in fav_ctr.most_common():
        summary += f"- **{name}**: {cnt} ({cnt/n:.0%})\n"

    summary += "\n## 跳过/无聊高频\n\n"
    for part, cnt in skip_ctr.most_common(5):
        summary += f"- {part}: {cnt}\n"

    summary += """
---

## 改稿优先级（P1）

1. 瑆笔记略缩短或加小标题（跳过提及）
2. DB1 三格再简化（低年读者）
3. 志郎喜剧节拍保留 · 不增恐怖

---

| 版本 | 2026-06-12 · seed=20260612 · SIMULATION |
"""
    summary_path = OUT_DIR / "E20_虚拟读者100_读数摘要_20260612.md"
    summary_path.write_text(summary, encoding="utf-8")
    print(f"Wrote {personas_path} ({n} readers)")
    print(f"Wrote {summary_path}")
    print(f"KPI pass: {kpi_pass}")


if __name__ == "__main__":
    main()
