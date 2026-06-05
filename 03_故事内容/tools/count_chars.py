#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"


def count_cn_narrative(raw: str) -> int:
    starts = []
    for pat in [r"^序\s*[·・]", r"^[一二三四五六]、"]:
        m = re.search(pat, raw, re.M)
        if m:
            starts.append(m.start())
    if starts:
        raw = raw[min(starts) :]
    for marker in ["【语感编辑", "---\n【", "（案"]:
        idx = raw.find(marker)
        if idx > 0:
            raw = raw[:idx]
    raw = re.sub(r"\*\*", "", raw)
    return len(re.findall(r"[\u4e00-\u9fff]", raw))


def count_jp_narrative(raw: str) -> int:
    starts = []
    for pat in [r"^序\s*[·・]", r"^(序・|一、|二、|三、|四、|五、)"]:
        m = re.search(pat, raw, re.M)
        if m:
            starts.append(m.start())
    if starts:
        raw = raw[min(starts) :]
    for marker in ["【E04", "【日本語", "---\n【", "（事件", "（案"]:
        idx = raw.find(marker)
        if idx > 0:
            raw = raw[:idx]
    raw = re.sub(r"\s+", "", raw)
    return len(
        re.findall(
            r"[\u3040-\u30ff\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]",
            raw,
        )
    )


def main() -> None:
    for f in sorted(BASE.glob("*.txt")):
        raw = f.read_text(encoding="utf-8")
        if "日本語" in f.name:
            n = count_jp_narrative(raw)
            print(f"JP {f.name}: {n}")
        elif "HybridVoice" in f.name:
            n = count_cn_narrative(raw)
            print(f"CN {f.name}: {n}")


if __name__ == "__main__":
    main()
