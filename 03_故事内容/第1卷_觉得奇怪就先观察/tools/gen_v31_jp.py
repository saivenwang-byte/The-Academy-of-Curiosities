# -*- coding: utf-8 -*-
"""Generate JP V3.1 from V3.0 + glossary + A005 timestamp fix."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "正式版" / "01_正文"

JP_GLOSSARY = [
    (r"合班教室", "合同教室"),
    (r"禁声届", "発声禁止届"),
    (r"禁声", "発声禁止"),
    (r"社徽", "部章"),
    (r"もっと牢だ", "もっとしっかり"),
    (r"こうした方が牢だ", "こうした方がしっかり"),
    (r"「牢」", "「しっかり」"),
    (r"観察社", "観察クラブ"),
    (r"移動メディア機材車", "放送委員会の機材ワゴン"),
    (r"機材車", "機材ワゴン"),
    (r"分段曝光", "パノラマのつなぎ撮影"),
    (r"露出値", "明るさ"),
    (r"公開日", "学校公開日と学習発表会"),
    (r"掘り取られた", "えぐり取られた"),
    (r"男生", "男子"),
    (r"女生", "女子"),
    (r"；", "。"),
]

A005_TIMESTAMP_BLOCK_OLD = """タブレットの中、集合写真は分段曝光：10:52:03 · 10:52:05 · 10:52:07——三段つなぎ。撮影開始：13:12:08。撮影終了：13:12:22。十四秒。一瞬じゃない。


各フレームの角に露出値——10:52:05は前後より0.3段明るい——その一秒に側光が動いたみたいに。"""

A005_TIMESTAMP_BLOCK_NEW = """タブレットの中、集合写真はパノラマのつなぎ撮影——レンズが左から右へ掃き、十数秒の画面を一枚にした。撮影は昼休み後の一点十二分ごろから、約十四秒。一瞬の写真じゃない。


水野の足元のタイルのひびが、画面の真ん中で途切れて、またつながっている——二枚の写真を貼り合わせた跡。"""

A005_MECHANISM_OLD = """10:52:05のフレームで、水野真帆は志郎に機材を渡すため半歩横に譲る；側光が変わり、彼女足元の影は前のフレームの地面領域に落ちる。隣接フレームを重ねると、彼女の影だけが食われた。


志郎が機材車ログをつなぐ：10:52 側門通過 · 地面軽震 · 彼女がちょうど動いた。"""

A005_MECHANISM_NEW = """志郎がクラスに指し示す。「水野さんに機材を渡すフレームで、彼女が横に譲った。側光が変わり、影が前のフレームの地面に落ちた。次のスキャンが重なると、彼女の影だけ消えた——彼女だけ。」


志郎が機材ワゴンのログをつなぐ：側門通過 · 地面が軽く震えた · 彼女がちょうど動いた。"""

A001_CN_FAIRPLAY = """其实完整句里并没有「水野」两个字——是「迟到者」。名字是耳朵自己填进去的。"""

def apply_glossary(text):
    for old, new in JP_GLOSSARY:
        text = re.sub(old, new, text)
    return text

def process_a005(text):
    text = text.replace(A005_TIMESTAMP_BLOCK_OLD, A005_TIMESTAMP_BLOCK_NEW)
    text = text.replace(A005_MECHANISM_OLD, A005_MECHANISM_NEW)
    text = text.replace("分段曝光三帧并排", "パノラマ三コマ並べ")
    text = text.replace("13:12:14", "一点十二分十四秒")
    text = text.replace("タイムスタンプ、", "撮影情報、")
    return text

def main():
    for i in range(1, 6):
        jp_files = list(BASE.glob(f"案0{i}_*_HybridVoice_V3.0_日本語.txt"))
        if not jp_files:
            print(f"skip A00{i}")
            continue
        src = jp_files[0]
        dst = BASE / src.name.replace("_V3.0_日本語", "_V3.1_日本語")
        text = src.read_text(encoding="utf-8")
        text = apply_glossary(text)
        if i == 5:
            text = process_a005(text)
        # header version bump
        text = text.replace("V3.0", "V3.1") if "V3.0" in text else text
        dst.write_text(text, encoding="utf-8")
        print(f"Wrote {dst.name}")

if __name__ == "__main__":
    main()
