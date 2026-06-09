#!/usr/bin/env python3
"""V3.2 JP expert polish: MoA-lite + doc81 human editor glossary → native children's prose."""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT = ROOT / "单元1_第一单元_五案"
V31 = UNIT / "正文" / "V3.1"
V32 = UNIT / "正文" / "V3.2"

# --- phrase-level (order matters: longer first) ---
PHRASE_FIXES: list[tuple[str, str]] = [
    ("修復の動作：", "誤解が解けたあと、クラスはこうした。"),
    ("修復の動作はこの三枚の横に書かれる——", "この三枚の横に、クラスが書き足す——"),
    ("修復は三歩で公然と行う：", "クラスは三つの手順で、みんなの前で直した。"),
    ("動機層を分ける：", "理由を分けて考える。"),
    ("動機層は分ける。", "理由の部分は、仕組みとは別に考える。"),
    ("一句の裁判詞に混ぜてはいけない。", "ひとつの決めつけに、全部を押し込んではいけない。"),
    ("裁判詞は手順に格下げ。", "決めつけの言葉は、手順のメモに下げた。"),
    ("観察クラブは面白いことを書く。裁判は書かない。", "観察クラブは、へんなところを書く。人を裁く言葉は書かない。"),
    ("五人同框", "五人が同じ写真に写っている"),
    ("口述の碎片", "口から聞いた断片"),
    ("口述碎片", "口から聞いた断片"),
    ("視覚の碎片", "目に残った断片"),
    ("たくさんの本当の碎片が、同時には存在しなかった全体を組み立てた。", "本当の断片ばかりが集まって、一度も存在しなかった一枚の絵をつくった。"),
    ("碎片 ≠ 一枚丸ごと · 覚えている ≠ 見た。", "断片と一枚丸ごとは違う。覚えていることと、見たことも違う。"),
    ("完全な文 ＝ 碎片 ＋ 転述 ＋ 空白。", "丸ごとの一枚は、断片とうわさと空白がくっついてできた。"),
    ("最終経手人", "最後に触った人"),
    ("先に仕組み、あとに動機。", "先に仕組み。理由はそのあと。"),
    ("仕組み確認済み · 動機は述べた（材料未登録）", "仕組みは確認した。理由も話した（材料はまだ登録していない）"),
    ("書面説明 · 先に仕組み、あとに動機。", "書面の説明——先に仕組み、あとに理由。"),
    ("カードを隠す ≠ 三件を盗む。", "カードを隠したことと、三件を盗んだことは別だ。"),
    ("確認済み：", "確認したこと："),
    ("聞いた話欄に慧美が書く：", "慧美は「聞いた話」欄に書く。"),
    ("ノート：", "ノートには、"),
    ("ノートに書く：", "ノートに書く。"),
    ("陸珣はノートにだけ書く：", "陸珣はノートにだけ書く。"),
    ("光は反論しようとする——喉はまだ気声。ノートにだけ書く：", "光は反論しようとしたが、喉はまだ気声。ノートにだけ書く。"),
    ("本当にもっと牢か", "本当にもっとしっかりか"),
    ("もっとしっかりと言った · 本当にもっとしっかりか · 未確認", "「もっとしっかり」って言った · 本当に？ · 未確認"),
    ("「牢だ。」", "「これなら、ぜったい外れない。」"),
    ("こうした方がしっかり", "こうした方が、ぜったい外れない"),
    ("PLAY · 三周前", "再生 · 三周前"),
    (" · ", "・"),
    ("——", "——"),  # keep em dash sparingly
    ("分段曝光", "パノラマのつなぎ撮影"),
    ("露出値", "明るさ"),
    ("合班教室", "合同教室"),
    ("禁声届", "発声禁止届"),
    ("禁声", "発声禁止"),
    ("社徽", "部章"),
    ("観察社", "観察クラブ"),
    ("移動メディア機材車", "放送委員会の機材ワゴン"),
    ("機材車", "機材ワゴン"),
    # Idempotent: only bare 公開日, not inside 公開日と学習発表会 / 学校公開日
    ("男生", "男子"),
    ("女生", "女子"),
    ("碎片", "断片"),
    ("裁判", "決めつけ"),
    ("動機", "理由"),
    ("掘り取られた", "えぐり取られた"),
    ("誤指", "間違った当てはめ"),
    ("；", "。"),
]

# subtitle/script lines → prose
SCRIPT_TO_PROSE: list[tuple[str, str]] = [
    (
        "ノートには、放送・光の声・唇が合わない。",
        "ノートには、放送と光の声、唇のずれだけを短く書いた。",
    ),
    (
        "確認したこと：集合写真に五人が同じ写真に写っている・水野の足元だけ無影・四人＋機材ワゴン＋灯柱に影",
        "確認したこと——集合写真に五人が写っている。水野の足元だけ影がない。他の四人と機材ワゴンと灯柱には影がある。",
    ),
]

# awkward calques from editor §4
CALQUE_FIXES: list[tuple[str, str]] = [
    (
        "しくみがわかるより先に、「光がやった」という話だけが廊下を走っていった。",
        "しくみがわかるより先に、「光がやった」という話だけが廊下を走った。",
    ),
    (
        "誤指は、仕組みより速い。",
        "間違った当てはめは、仕組みより速い。",
    ),
]

HEADER_V32 = """『学堂奇事録』

第1巻 · へんなところ、先に見てみよう

> Hybrid Voice JP · **V3.2** · MoA-lite 专家组润色 · {date} · 待田中 J10

"""


def collapse_list_colons(text: str) -> str:
    """Turn 'A · B · C' note lines into readable prose where triple."""
    def repl(m: re.Match) -> str:
        parts = [p.strip() for p in m.group(0).split("・") if p.strip()]
        if len(parts) >= 4 and len(m.group(0)) < 120:
            return "。".join(parts) + "。"
        return m.group(0)

    return re.sub(r"[^。\n]{10,80}(?:・[^。\n]{3,30}){2,}", repl, text)


# Bare 公開日 → canonical event name (idempotent; no append-on-rerun)
_EVENT_CANON = "公開日と学習発表会"
_EVENT_BARE_RE = re.compile(r"(?<![学校])公開日(?!と学習発表会)")


def _expand_bare_koukaihi(text: str) -> str:
    return _EVENT_BARE_RE.sub(_EVENT_CANON, text)


def polish(text: str) -> str:
    for old, new in PHRASE_FIXES:
        text = text.replace(old, new)
    text = _expand_bare_koukaihi(text)
    for old, new in SCRIPT_TO_PROSE:
        text = text.replace(old, new)
    for old, new in CALQUE_FIXES:
        text = text.replace(old, new)
    # Chinese-style enumeration colon after label
    text = re.sub(r"([ぁ-んァ-ヶ一-龥]{2,8})：([^。\n]{0,40})：", r"\1——\2。", text)
    # Remove duplicate spaces
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def setup_v32() -> None:
    for sub in ("01_中文", "02_日本語", "03_版本意见"):
        (V32 / sub).mkdir(parents=True, exist_ok=True)
    # CN unchanged from V3.1
    for f in (V31 / "01_中文").glob("*.txt"):
        dst = V32 / "01_中文" / f.name.replace("_V3.1", "_V3.2")
        if not dst.exists():
            shutil.copy2(f, dst)
    for f in (V31 / "03_版本意见").glob("*V3.1*"):
        dst = V32 / "03_版本意见" / f.name.replace("V3.1", "V3.2")
        if not dst.exists():
            shutil.copy2(f, dst)


def process_jp() -> dict[str, int]:
    stats = {}
    today = date.today().isoformat()
    for src in sorted((V31 / "02_日本語").glob("*_V3.1_日本語.txt")):
        text = src.read_text(encoding="utf-8")
        before = len(text)
        text = polish(text)
        # bump header if present
        if "V3.1" in text[:200]:
            text = re.sub(r"V3\.1", "V3.2", text, count=2)
        else:
            text = HEADER_V32.format(date=today) + text.split("---", 1)[-1] if "---" in text else text
        dst_name = src.name.replace("_V3.1_日本語", "_V3.2_日本語")
        dst = V32 / "02_日本語" / dst_name
        dst.write_text(text, encoding="utf-8")
        stats[src.name] = {"before": before, "after": len(text)}
    return stats


def write_meta(stats: dict) -> None:
    meta = V32 / "03_版本意见" / "00_JP_V3.2_专家组润色摘要.md"
    lines = [
        "# V3.2 · JP 专家组润色摘要（MoA-lite）",
        "",
        f"> 日期：{date.today().isoformat()}",
        "> 依据：doc81 真人编辑 P0 · academy-jp-voice-editor MoA-lite",
        "> CN：`V3.1/01_中文` 未改 · 本版 **JP-only**",
        "",
        "## 四视角处理",
        "",
        "| 视角 | 动作 |",
        "|------|------|",
        "| 論理 | 公平线索句保留 · metadata 读者化延续 |",
        "| 文体 | 字幕式 `ノート：` → 叙事句 · 减少 `·` 串列 |",
        "| 語彙 | 碎片/裁判/動機層/同框/経手人 → 日语儿童词 |",
        "| 読者 | 10–12 岁可读 · 観察クラブ · 合同教室 · 部章 |",
        "",
        "## 字数",
        "",
        "| 文件 | before | after |",
        "|------|--------|-------|",
    ]
    for name, s in stats.items():
        lines.append(f"| {name} | {s['before']} | {s['after']} |")
    lines += [
        "",
        "## 状态",
        "",
        "- **非 G-JP LOCK** · 待田中 J10 全文督查",
        "- 下一版小修 → V3.3 · 田中反馈后",
    ]
    meta.write_text("\n".join(lines), encoding="utf-8")

    readme = V32 / "00_版本说明.md"
    readme.write_text(
        f"# 第一单元正文 · V3.2 · **CURRENT（JP 轨）**\n\n"
        f"> 2026-06-09\n\n"
        f"## 版本摘要\n\n"
        f"- **CN**：同 V3.1（`01_中文/` 文件名 V3.2 为归档一致）\n"
        f"- **JP**：专家组 MoA-lite 母语润色 · 响应真人编辑 3.5/10\n"
        f"- **03_版本意见**：含 JP 润色摘要 + V3.1 meta 副本\n\n"
        f"## 版本号规则\n\n"
        f"- 小修 +0.1 · 大修 +1.0\n",
        encoding="utf-8",
    )


def main() -> None:
    setup_v32()
    stats = process_jp()
    write_meta(stats)
    print("V3.2 JP polish done:", len(stats), "files")


if __name__ == "__main__":
    main()
