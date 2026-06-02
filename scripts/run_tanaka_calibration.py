#!/usr/bin/env python3
"""Run CALIBRATION_DB (from japan_campus_consultant_agent.html) on text files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CALIBRATION_DB = {
    "space": [
        {"trigger": ["室内鞋", "上鞋", "换鞋"], "type": "ok", "title": "室内鞋细节到位"},
        {"trigger": ["推拉门", "推门", "哐"], "type": "warn", "title": "教室门类型需确认"},
        {"trigger": ["走进教室", "进入教室", "进教室", "推开教室"], "type": "warn", "title": "缺上履き换鞋流程"},
        {"trigger": ["食堂", "打饭", "端着餐", "饭堂", "餐厅"], "type": "warn", "title": "日本小学午餐不是食堂制"},
        {"trigger": ["教室後方の流し", "教室后方", "后方水池", "教室水槽"], "type": "warn", "title": "昼歯磨き一般不在教室后方"},
        {"trigger": ["班长", "课代表", "学习委员", "班干部"], "type": "warn", "title": "日本小学不是班干部制"},
        {"trigger": ["黑板", "板书", "黒板"], "type": "note", "title": "黑板擦放置习惯"},
        {"trigger": ["厕所", "卫生间", "トイレ"], "type": "warn", "title": "厕所需要专用拖鞋"},
    ],
    "routine": [
        {"trigger": ["午饭", "吃饭", "食堂", "给食", "値日", "給食", "配膳"], "type": "ok", "title": "给食制度是核心场景"},
        {"trigger": ["社团", "部活", "俱乐部"], "type": "note", "title": "部活结束时间感"},
        {"trigger": ["班级职责", "值日", "係", "掃除当番", "黒板係"], "type": "ok", "title": "係活動细节"},
        {"trigger": ["开学", "入学", "入学式", "毕业"], "type": "note", "title": "开学式氛围"},
    ],
    "social": [
        {"trigger": ["学长", "学姐", "前辈", "先輩", "後輩", "六年生"], "type": "warn", "title": "先輩/後輩关系要写准"},
        {"trigger": ["欺负", "孤立", "欺凌", "无视", "いじめ"], "type": "warn", "title": "欺凌的日本形态"},
        {"trigger": ["气氛", "沉默", "空气", "氛围", "空気"], "type": "note", "title": "空気を読む"},
    ],
    "culture": [
        {"trigger": ["书包", "ランドセル", "背包"], "type": "note", "title": "ランドセル细节"},
        {"trigger": ["暑假", "自由研究", "作业"], "type": "ok", "title": "自由研究契合IP"},
        {"trigger": ["怪谈", "鬼", "幽灵", "音乐室", "人体模型", "怪事", "ふしぎ"], "type": "note", "title": "校园怪谈/ふしぎ层"},
    ],
    "emotion": [
        {"trigger": ["再见", "告别", "走", "じゃあね", "明天见", "また明日"], "type": "note", "title": "じゃあね文化"},
        {"trigger": ["你真棒", "加油", "鼓励", "夸奖", "太厉害"], "type": "warn", "title": "鼓励方式不同"},
        {"trigger": ["安慰", "难过", "哭", "伤心", "ごめん"], "type": "note", "title": "安慰/道歉分寸"},
    ],
}

MODE_LABELS = {
    "space": "空间与物",
    "routine": "制度与流程",
    "social": "人际隐规则",
    "culture": "儿童亚文化",
    "emotion": "情感分寸",
}


def scan(text: str, modes: list[str] | None = None) -> list[dict]:
    modes = modes or list(CALIBRATION_DB.keys())
    lower = text.lower()
    hits: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for mode in modes:
        for card in CALIBRATION_DB.get(mode, []):
            for t in card["trigger"]:
                if t in text or t.lower() in lower:
                    key = (mode, card["title"])
                    if key not in seen:
                        seen.add(key)
                        hits.append({**card, "mode": mode, "trigger_hit": t})
                    break
    return hits


def split_jp_vol1(text: str) -> list[tuple[str, str]]:
    """Split Vol1 JP by chapter headers."""
    parts = re.split(r"(?=^序 ·|^一、|^二、|^三、|^四、|^五、|^六、|^\【あなたもできる】|^════+\s*\n陸瑆ノート)", text, flags=re.M)
    chunks: list[tuple[str, str]] = []
    for p in parts:
        p = p.strip()
        if not p or p.startswith("『学堂"):
            continue
        first = p.split("\n", 1)[0].strip()[:40]
        chunks.append((first, p))
    return chunks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", type=Path, required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = args.file.read_text(encoding="utf-8")
    # strip metadata footer
    if "【定稿自检】" in text:
        text = text.split("【定稿自检】")[0]

    all_hits: list[dict] = []
    batches = split_jp_vol1(text)
    batch_results = []
    for name, chunk in batches:
        hits = scan(chunk)
        batch_results.append({"batch": name, "hits": hits, "warn": sum(1 for h in hits if h["type"] == "warn")})
        all_hits.extend(hits)

    warn = [h for h in all_hits if h["type"] == "warn"]
    note = [h for h in all_hits if h["type"] == "note"]
    ok = [h for h in all_hits if h["type"] == "ok"]

    if args.json:
        print(json.dumps({"batches": batch_results, "warn": len(warn), "note": len(note), "ok": len(ok)}, ensure_ascii=False, indent=2))
        return 0

    print(f"File: {args.file.name}")
    print(f"Batches: {len(batches)} | warn={len(warn)} note={len(note)} ok={len(ok)}")
    for br in batch_results:
        print(f"\n--- {br['batch']} (warn={br['warn']}) ---")
        for h in br["hits"]:
            tag = h["type"].upper()
            print(f"  [{tag}] [{MODE_LABELS[h['mode']]}] {h['title']} (trigger:{h['trigger_hit']})")

    if warn:
        print("\n=== WARN summary (review manually for false positives) ===")
        for h in warn:
            print(f"  · {h['title']} ← 「{h['trigger_hit']}」")
    return 1 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
