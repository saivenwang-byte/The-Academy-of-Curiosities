#!/usr/bin/env python3
"""V3.1 editorial pass helper: char counts + JP glossary replacements."""
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "正式版" / "01_正文"

JP_GLOSSARY = [
    (r"合班教室", "合同教室"),
    (r"禁声", "発声禁止"),
    (r"禁声届", "発声禁止届"),
    (r"社徽", "部章"),
    (r"牢だ", "しっかり"),
    (r"もっと牢", "もっとしっかり"),
    (r"「牢」", "「しっかり」"),
    (r"観察社", "観察クラブ"),
    (r"移動メディア機材車", "放送委員会の機材ワゴン"),
    (r"機材車", "機材ワゴン"),
    (r"分段曝光", "パノラマのつなぎ撮影"),
    (r"露出値", "明るさの差"),
    (r"公開日", "学校公開日と学習発表会"),
    (r"确认済み", "確認済み"),
    (r"确认済", "確認済"),
    (r"掘り取られた", "えぐり取られた"),
    (r"男生", "男子"),
    (r"女生", "女子"),
    (r"骂", "ののし"),
    (r"骂り", "ののし"),
    (r"；", "。"),
    (r" · ", "・"),
]

def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]", text))


def apply_jp_glossary(text: str) -> str:
    for old, new in JP_GLOSSARY:
        text = re.sub(old, new, text)
    return text


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "count"
    for i in range(1, 6):
        cn_v30 = list(BASE.glob(f"案0{i}_*_HybridVoice_V3.0.txt"))
        jp_v30 = list(BASE.glob(f"案0{i}_*_HybridVoice_V3.0_日本語.txt"))
        if not cn_v30:
            continue
        cn_path = cn_v30[0]
        cn = cn_path.read_text(encoding="utf-8")
        print(f"A00{i} CN V3.0: {count_cjk(cn)}")
        if jp_v30:
            jp = jp_v30[0].read_text(encoding="utf-8")
            print(f"A00{i} JP V3.0: {count_cjk(jp)}")
        if action == "jp-gloss" and jp_v30:
            stem = cn_path.stem.replace("_V3.0", "_V3.1_日本語")
            out = BASE / f"{stem}.txt"
            # only if v31 jp doesn't exist yet from manual edit
            pass

if __name__ == "__main__":
    main()
