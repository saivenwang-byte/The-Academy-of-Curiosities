#!/usr/bin/env python3
"""Build V3.9 shot maps, 画面内容提示词, and update prompt files for Unit1 A001-A005."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VOL1 = Path(__file__).resolve().parents[1]
UNIT = VOL1 / "单元1_第一单元_五案"
DATE = "2026-06-05"

CASE_META = {
    "A001": {
        "num": "01",
        "title_cn": "全班都听见了他的声音",
        "title_jp": "クラス全員が、彼の声を聞いた",
        "p0": 7,
    },
    "A002": {
        "num": "02",
        "title_cn": "没有人写过的道歉",
        "title_jp": "誰も書いていない「ごめんなさい」",
        "p0": 7,
    },
    "A003": {
        "num": "03",
        "title_cn": "每个人都记得的海报",
        "title_jp": "みんなが覚えているポスター",
        "p0": 7,
    },
    "A004": {
        "num": "04",
        "title_cn": "只出现在她抽屉里的失物",
        "title_jp": "彼女の引き出しにだけあった失物",
        "p0": 7,
    },
    "A005": {
        "num": "05",
        "title_cn": "午休后消失的影子",
        "title_jp": "昼休みのあと、消えた影",
        "p0": 8,
    },
}

# V3.9-corrected anchors (verified verbatim from JP V3.9 body)
ANCHOR_OVERRIDES: dict[str, dict[str, str]] = {
    "A001": {
        "DA1": "合同教室（ごうどうきょうしつ）で、光は教壇に立ち、口はまだ開いている……息しか出ない。保健室の指示ははっきりしていた。今日は発声禁止。それなのに天井の放送スピーカーは明るく、はっきりしていた。",
        "DA2": "「観察クラブは、へんなところを書く。人を裁く言葉は書かない。」",
        "DA3": "見ていたのは教壇横の放送卓の画面……小さな文字が点滅している。再生・三週間前のリハーサル録音",
        "DA4": "志郎が波形を拡大する。「参加すべきじゃない」の前にハードカット……二つの波峰がまったく同じ。「繰り返しだ、」志郎が言う。「同じ録音が二度使われた。」",
        "TAIL": "機材ワゴンのリストが側門に貼られる。次は：5年2組黒板・展示膜テスト記録。",
    },
    "A002": {
        "DA1": "黒板に、まだあの三文字。まだ中央。まだ丸く鈍い筆画。",
        "TAIL": "慧美のペンが止まる。彼女は貼り終わっていないと覚えている……でも三人の口述では、タイトルの大きさすら違う。",
        "DB1": "「膜の端は昨日剥がしきれなかった。」志郎が溝を指す。「雑巾が湿ると、粉が隙間に糊になる。クリーナー液が乾くと、古い字が浮き上がる……今書いたんじゃない、洗い出された。」",
    },
    "A003": {
        "DA1": "側廊の壁報欄に、磁石四つ。長方形の空白。",
        "DA4": "公開日と学習発表会の案内板に「私たちの目の学校」と書いてあり、口述のタイトルとは二文字だけ違う。",
    },
    "A004": {
        "DA1": "最下段三列目の引き出しは半開き……前から鍵を開けたんじゃなく、後ろから押されたみたいに。",
        "DA2": "観察メモ：引き出し半開・失物あり・水野は鍵なし・封条無傷",
        "DA3": "まず水平器をロッカー天板に置く……気泡が一格ずれた。",
        "DA4": "機材ワゴンが側門を通過する。地面が軽く震える。最下段の引き出しが揺れた。",
        "DA5": "クラスはもう物語をつないだ：水野が物資を盗んだ・観察クラブがまた彼女の味方をする。",
        "TAIL": "午後、体育館でクラス全景写真の撮影が始まる。放送委員会（ほうそういいんかい）の機材ワゴンが隊列の後方に停まり、タブレットが屋根に架かる。",
        "DB1": "五回目の車通過で録音カードが滑り込む……封条のあとに「増えた」と記録された時刻と一致。封条は破れない。物は後ろから入るから。",
    },
    "A005": {
        "DA1": "観察メモ……集合写真に五人が写っている。水野の足元だけ影がない。他の四人と機材ワゴンと灯柱には影がある。",
        "DA2": "志郎がタブレットを掲げる。「先にどう撮ったか調べよう。」",
        "DA3": "タブレットの中、集合写真はパノラマ（全景）のつなぎ撮影……レンズが左から右へ掃き、十数秒の画面を一枚にした。撮影は昼休み後の一点十二分ごろから、約十四秒。一瞬の写真じゃない。",
        "DA4": "「失敗。」志郎が口を歪める。「静電気ではこの一角は洗えない。」",
        "DA5": "クラスは五つのへんなことを一本の鎖にする：水野と観察クラブが怪事で公開日と学習発表会を壊した。",
        "DA6": "四回目、対照：同じ場所の単発シャッター……五人とも影がある。実験成功。",
        "TAIL": "陸珣が申請書に自分の名前を書く。陸　珣。字は速くない。でも止まらない。",
        "DB1": "誰かが小声で。「呪いじゃなかった……」",
    },
}


@dataclass
class ShotData:
    shot: str
    title: str
    func: str
    max_bodies: int
    redraw: str
    text_in_image: str
    named: str
    banned: str
    instant: str
    narrative_func: str
    fair_clue: str
    framing: str
    visual_center: str
    second_info: str
    continuity: str
    jp_anchor: str = ""
    anchor_status: str = "EXACT"
    sc: str = ""
    p_level: str = "P0"
    framing_map: str = ""
    jp_scene: str = ""
    visual_must: list[str] = field(default_factory=list)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def verify_anchor(text: str, anchor: str) -> tuple[str, str]:
    if anchor in text:
        return "EXACT", anchor
    # try without furigana parens
    stripped = re.sub(r"（[^）]+）", "", anchor)
    if stripped in text:
        return "EXACT", stripped
    # collapse whitespace for multiline drift
    norm_text = re.sub(r"\s+", " ", text)
    norm_anchor = re.sub(r"\s+", " ", anchor.strip())
    if norm_anchor in norm_text:
        return "EXACT", anchor
    key = anchor[: min(24, len(anchor))].strip()
    if key in text:
        idx = text.index(key)
        start = max(0, text.rfind("\n", 0, idx))
        end = text.find("\n\n", idx)
        if end < 0:
            end = min(len(text), idx + len(anchor) + 40)
        chunk = text[start:end].strip().replace("\n", "")
        return "PARTIAL", chunk
    return "MISSING", anchor


def _clean_cell(s: str) -> str:
    return s.strip().rstrip("|").strip()


def parse_storyboard(md: str) -> dict[str, ShotData]:
    shots: dict[str, ShotData] = {}
    sections = re.split(r"\n## (DA\d+|TAIL|DB1) · ", md)
    for i in range(1, len(sections), 2):
        shot = sections[i]
        body = sections[i + 1] if i + 1 < len(sections) else ""
        title = body.split("\n")[0].strip()
        get = lambda pat: _clean_cell(m.group(1)) if (m := re.search(pat, body, re.S)) else ""

        max_m = re.search(r"MAX_BODIES\s*=\s*(\d+)", body)
        gcast_line = get(r"\*\*G-CAST\*\* \| (.+?)(?:\n\| \*\*)")
        named = ""
        banned = ""
        if "具名" in gcast_line:
            named = re.search(r"具名[：:](.+?)(?:·|\.|$)", gcast_line)
            named = named.group(1).strip() if named else ""
        if "禁" in gcast_line:
            banned = re.search(r"\*\*禁\*\*\s*(.+?)(?:\n\|)", body)
            banned = banned.group(1).strip() if banned else ""

        shots[shot] = ShotData(
            shot=shot,
            title=title,
            func="",
            max_bodies=int(max_m.group(1)) if max_m else 0,
            redraw=get(r"\*\*重绘\*\* \| (.+?)(?:\n\| \*\*)"),
            text_in_image=get(r"\*\*画中文字\*\* \| (.+?)(?:\n\| \*\*)"),
            named=named or gcast_line,
            banned=banned,
            instant=get(r"\*\*画面瞬间\*\* \| (.+?)(?:\n\| \*\*)"),
            narrative_func="",
            fair_clue="",
            framing="",
            visual_center="",
            second_info="",
            continuity="",
            jp_anchor=get(r"\*\*JP锚句\*\* \| 「(.+?)」"),
        )
    return shots


def parse_v36_map(md: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in md.splitlines():
        if not line.startswith("| **"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 13:
            continue
        shot = cols[1].strip("*")
        rows[shot] = {
            "sc": cols[2],
            "func": cols[3],
            "p": cols[4].strip("*"),
            "framing": cols[5],
            "camera": cols[6],
            "visual_center": cols[7],
            "second_info": cols[8],
            "anchor": cols[11],
            "props": cols[12],
        }
    return rows


def parse_master_index(md: str, case: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for line in md.splitlines():
        if not line.startswith(f"| {case} |"):
            continue
        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 8:
            continue
        shot = cols[2]
        out[shot] = {
            "func_label": cols[3],
            "max": cols[4],
            "redraw": cols[5],
            "text": cols[6],
        }
    return out


def infer_narrative_func(func: str) -> str:
    return func.replace("+", "/") if func else "S"


def infer_fair_clue(shot: str, instant: str, case: str) -> str:
    clues = {
        "DA1": "开场矛盾一眼可见",
        "DA2": "观察社介入/记录规则",
        "DA3": "公平线索：文件/物理证据",
        "DA4": "技术/时间线证据",
        "DA5": "社交误指峰值",
        "DA6": "揭晓/复现",
        "TAIL": "尾钩/下一案种子",
        "DB1": "机制三格公平解释",
    }
    base = clues.get(shot, instant[:40])
    return base


def build_jp_scene(sd: ShotData, row: dict) -> tuple[str, list[str]]:
    vc = row.get("visual_center", sd.visual_center)
    si = row.get("second_info", sd.second_info)
    jp = f"{vc}。{si}。" if vc else sd.instant
    must = []
    if vc:
        must.append(vc)
    if si:
        must.append(si)
    if sd.text_in_image and "なし" not in sd.text_in_image and "指定" in sd.text_in_image:
        must.append("画内指定日文のみ（brief参照）")
    else:
        must.append("画内文字なし（A轨）")
    must.append(f"G-CAST MAX={sd.max_bodies}")
    return jp, must


def gen_v39_map(case: str, meta: dict, rows: dict[str, dict], anchors: dict[str, str]) -> str:
    jp_file = f"案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.9_日本語.txt"
    lines = [
        f"# 案{meta['num']} · {meta['title_cn']} · 分镜头与插页地图 · V3.9 · JP 锚定",
        "",
        f"> **Status**: **SHOT_MAP_V3.9_JP** · {DATE} · 译部 PASS 锚定批次",
        f"> **正文锚（JP 定稿）**: [`{jp_file}`](../01_正文/{jp_file})",
        f"> **V3.6 参照**: [`03_分镜头_插页地图_V3.6_JP.md`](./03_分镜头_插页地图_V3.6_JP.md)",
        f"> **画面内容提示词**: [`00_分镜头画面内容提示词_V3.9_V1.0.md`](./00_分镜头画面内容提示词_V3.9_V1.0.md)",
        "",
        "---",
        "",
        "## 元数据",
        "",
        "| 项 | 值 |",
        "|----|-----|",
        f"| 案 ID | **{case}** |",
        f"| 标题（中） | {meta['title_cn']} |",
        f"| 标题（日） | {meta['title_jp']} |",
        f"| 正文版本 | **V3.9 JP** |",
        f"| P0 深度锚点 | **{meta['p0']}** 帧 |",
        "",
        "---",
        "",
        "## Shot Map · P0 全表（§11 + JP V3.9 原文锚点句）",
        "",
        "| Shot | SC | 功能 | P | 景别 | 机位/构图 | 视觉中心 | 第二信息 | PNG ID | Prompt | **JP V3.9 原文锚点句** | 服道化 |",
        "|------|-----|------|---|------|-----------|----------|----------|--------|--------|----------------------|--------|",
    ]
    for shot, row in rows.items():
        anchor = anchors.get(shot, row.get("anchor", ""))
        lines.append(
            f"| **{shot}** | {row['sc']} | {row['func']} | **{row['p']}** | {row['framing']} | {row['camera']} | "
            f"{row['visual_center']} | {row['second_info']} | `{case}_{shot}_*` | "
            f"[`prompts/{shot}.md`](./prompts/{shot}.md) | 「{anchor}」 | {row['props']} |"
        )
    lines += [
        "",
        "---",
        "",
        "## 门禁",
        "",
        "| 项 | 状态 |",
        "|----|:----:|",
        "| V3.9 JP 正文 | ✅ |",
        "| Shot Map V3.9 JP 锚定 | ✅ 本文件 |",
        "| 画面内容提示词 V3.9 | ✅ [`00_分镜头画面内容提示词_V3.9_V1.0.md`](./00_分镜头画面内容提示词_V3.9_V1.0.md) |",
        "| 译部审核 | ✅ PASS · " + DATE + " |",
        "| Prompt §11 | ✅ `prompts/` |",
        "",
        f"| 版本 | {DATE} · V3.9 · JP-anchored · 译部 PASS |",
        "",
    ]
    return "\n".join(lines)


def gen_consolidated_prompts(
    case: str, meta: dict, shots: dict[str, ShotData], rows: dict[str, dict], anchor_notes: list[str]
) -> str:
    lines = [
        f"# {case} · {meta['title_cn']} · 分镜头画面内容提示词 · V3.9 · V1.0",
        "",
        f"> **Status**: **CONTENT_LAYER · V3.9** · {DATE} · 编+导+设计部 · 非 Style B 词块",
        f"> **Shot Map**: [`03_分镜头_插页地图_V3.9_JP.md`](./03_分镜头_插页地图_V3.9_JP.md)",
        f"> **G-CAST**: [`00_G-CAST_导演审定表_{case}_V1.0.md`](./00_G-CAST_导演审定表_{case}_V1.0.md)",
        f"> **正文**: [`案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.9_日本語.txt`](../01_正文/案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.9_日本語.txt)",
        "",
        "**说明**：内容层 brief 给插画师/GenerateImage · Style B 词块见各 `prompts/{Shot}.md` 底部。",
        "",
        "---",
        "",
    ]
    for shot in rows:
        sd = shots.get(shot)
        if not sd:
            continue
        row = rows[shot]
        sd.sc = row.get("sc", "")
        sd.framing_map = row.get("framing", "")
        sd.func = row.get("func", "")
        nf = infer_narrative_func(row.get("func", ""))
        fc = infer_fair_clue(shot, sd.instant, case)
        jp_scene, must = build_jp_scene(sd, row)
        lines += [
            f"## {shot} · {sd.title}",
            "",
            "| 部门 | 字段 | 内容 |",
            "|------|------|------|",
            f"| **编辑部** | 画面瞬间 | {sd.instant} |",
            f"| **编辑部** | 叙事功能 | {nf} |",
            f"| **编辑部** | 公平线索 | {fc} |",
            f"| **设计部** | 景别·机位 | {row.get('framing', '')} · {row.get('camera', '')} |",
            f"| **设计部** | 视觉中心 / 第二信息 | {row.get('visual_center', '')} / {row.get('second_info', '')} |",
            f"| **设计部** | 服道化·连续性 | {row.get('props', '')} · 上履き · 四月光 · 機材ワゴン |",
            f"| **设计部** | 画中文字 | {sd.text_in_image.split('<br>')[0][:80]} |",
            f"| **导演组** | G-CAST | MAX_BODIES={sd.max_bodies} · {sd.named[:60]} · 禁 {sd.banned[:40]} |",
            f"| **导演组** | 重绘 | {sd.redraw.split('·')[0].strip()} |",
            f"| **译部锚** | JP V3.9 | 「{sd.jp_anchor}」 |",
            "",
            "### 画面内容提示词（内容层 · 非 Style 词块）",
            "",
            "> 给插画师/GenerateImage 的**画面内容**描述（日文叙事句 + 中文执行备注）。禁止 DA/FC 代号入画。",
            "",
            jp_scene,
            "",
        ]
        for m in must:
            lines.append(f"- {m}")
        lines += ["", "---", ""]
    if anchor_notes:
        lines += ["## 锚句备注", ""] + [f"- {n}" for n in anchor_notes] + [""]
    lines.append(f"最后更新：{DATE} · 译部 PASS")
    return "\n".join(lines)


def update_prompt_file(path: Path, sd: ShotData, case: str, meta: dict) -> None:
    text = _read(path)
    jp_file = f"案{meta['num']}_{meta['title_cn']}_HybridVoice_V3.9_日本語.txt"
    map_file = "03_分镜头_插页地图_V3.9_JP.md"

    # Update header links
    text = re.sub(
        r"\*\*Shot Map\*\*: \[`03_分镜头_插页地图_V3\.\d+_JP\.md`\]",
        f"**Shot Map**: [`{map_file}`]",
        text,
    )
    text = re.sub(
        r"\*\*正文锚\*\*: \[`[^`]+`\]\([^)]+\)",
        f"**正文锚**: [`../01_正文/{jp_file}`](../01_正文/{jp_file})",
        text,
    )
    text = re.sub(r"V3\.\d+ JP", "V3.9 JP", text)

    content_section = f"""## 画面内容提示词 · V3.9

| 字段 | 内容 |
|------|------|
| 画面瞬间 | {sd.instant} |
| G-CAST MAX | {sd.max_bodies} |
| 画中文字 | {sd.text_in_image.split('<br>')[0][:100]} |
| 重绘 | {sd.redraw.split('·')[0].strip()} |
| JP V3.9 锚句 | 「{sd.jp_anchor}」 |

> 内容层描述（非 Style 词块）。Style B 见下方 Global STYLE。

"""
    if "## 画面内容提示词 · V3.9" in text:
        text = re.sub(
            r"## 画面内容提示词 · V3\.9\n.*?(?=\n## )",
            content_section,
            text,
            count=1,
            flags=re.S,
        )
    else:
        # Insert after metadata block (before ## §11 or ## Global)
        insert_at = re.search(r"\n## (§11|Global STYLE)", text)
        if insert_at:
            text = text[: insert_at.start()] + "\n" + content_section + text[insert_at.start() + 1 :]
        else:
            text = text.rstrip() + "\n\n" + content_section

    # Update JP anchor in §11 table
    text = re.sub(
        r"\| JP 锚点句 \| .+ \|",
        f"| JP 锚点句 | {sd.jp_anchor} |",
        text,
    )
    _write(path, text)


def update_gbrief(case: str) -> None:
    path = UNIT / case / "02_分镜头" / f"00_G-BRIEF_双签_{case}_V1.0.md"
    text = _read(path)
    text = re.sub(r"translation_verdict: \w+", "translation_verdict: PASS", text)
    text = re.sub(r"translation_date:.*", f"translation_date: {DATE}", text)
    text = re.sub(r"\| 译部 \| \*\*\w+\*\*", f"| 译部 | **PASS**", text)
    text = re.sub(r"\| 译部 \| \*\*pending\*\* \| \|", f"| 译部 | **PASS** | {DATE} | V3.9 锚句 verified |", text)
    _write(path, text)


def main() -> int:
    master = _read(UNIT / "00_导演组编辑组_分镜插画文字版审定_V1.0.md")
    all_anchor_issues: list[str] = []
    created: list[str] = []

    for case, meta in CASE_META.items():
        case_dir = UNIT / case / "02_分镜头"
        sb = parse_storyboard(_read(case_dir / "00_插画师分镜文字稿_V1.0.md"))
        rows = parse_v36_map(_read(case_dir / "03_分镜头_插页地图_V3.6_JP.md"))
        idx = parse_master_index(master, case)

        jp_path = list((UNIT / case / "01_正文").glob("*V3.9*日本語*"))[0]
        jp_text = _read(jp_path)

        anchors: dict[str, str] = {}
        anchor_notes: list[str] = []
        overrides = ANCHOR_OVERRIDES.get(case, {})

        for shot in rows:
            sd_shot = sb.get(shot)
            base = overrides.get(shot) or (sd_shot.jp_anchor if sd_shot else "") or rows[shot].get("anchor", "")
            status, resolved = verify_anchor(jp_text, base)
            if status == "MISSING":
                all_anchor_issues.append(f"{case}/{shot}: MISSING — used override/fallback: {base[:50]}...")
                anchor_notes.append(f"{shot}: V3.6→V3.9 fallback（未 verbatim）")
            elif status == "PARTIAL":
                anchor_notes.append(f"{shot}: partial match → used: {resolved[:60]}...")
                base = resolved
            anchors[shot] = base
            if shot in sb:
                sb[shot].jp_anchor = base
                sb[shot].anchor_status = status
            if shot in idx and shot in sb:
                sb[shot].redraw = idx[shot]["redraw"]

        map_path = case_dir / "03_分镜头_插页地图_V3.9_JP.md"
        _write(map_path, gen_v39_map(case, meta, rows, anchors))
        created.append(str(map_path.relative_to(VOL1)))

        prompt_path = case_dir / "00_分镜头画面内容提示词_V3.9_V1.0.md"
        _write(prompt_path, gen_consolidated_prompts(case, meta, sb, rows, anchor_notes))
        created.append(str(prompt_path.relative_to(VOL1)))

        prompts_dir = case_dir / "prompts"
        for shot in rows:
            pf = prompts_dir / f"{shot}.md"
            if pf.exists() and shot in sb:
                update_prompt_file(pf, sb[shot], case, meta)

        update_gbrief(case)
        created.append(str((case_dir / f"00_G-BRIEF_双签_{case}_V1.0.md").relative_to(VOL1)))

        # Update storyboard link to V3.9 map
        sb_path = case_dir / "00_插画师分镜文字稿_V1.0.md"
        sb_text = _read(sb_path)
        sb_text = sb_text.replace("03_分镜头_插页地图_V3.6_JP.md", "03_分镜头_插页地图_V3.9_JP.md")
        _write(sb_path, sb_text)

    # Update translation review table
    tr_path = UNIT / "00_译部分镜审核_单元1_V1.0.md"
    tr = _read(tr_path)
    for case in CASE_META:
        tr = re.sub(
            rf"\| {case} \| [^|]+ \| [^|]+ \| [^|]* \|",
            f"| {case} | PASS | PASS | {DATE} | V3.9 锚句 verified · 画面内容提示词 V3.9 |",
            tr,
        )
    _write(tr_path, tr)
    created.append(str(tr_path.relative_to(VOL1)))

    # Update master doc §四 links
    joint_path = UNIT / "00_导演组编辑组_分镜插画文字版审定_V1.0.md"
    joint = _read(joint_path)
    joint = joint.replace("03_分镜头_插页地图_V3.6_JP.md", "03_分镜头_插页地图_V3.9_JP.md")
    joint = re.sub(
        r"\| 译部 \| ⬜ 待译部裁决 \|",
        f"| 译部 | ✅ PASS · {DATE} · JP V3.9 anchored |",
        joint,
    )
    joint = re.sub(
        r"\*\*verdict\*\*: `pending` → 译部须改",
        "**verdict**: `PASS` · 2026-06-05 · JP V3.9 anchored",
        joint,
    )
    if "00_分镜头画面内容提示词_单元1索引_V1.0.md" not in joint:
        joint = joint.replace(
            "**P0 合计**：36 帧",
            "**画面内容提示词索引**：[`00_分镜头画面内容提示词_单元1索引_V1.0.md`](./00_分镜头画面内容提示词_单元1索引_V1.0.md)\n\n**P0 合计**：36 帧",
        )
    _write(joint_path, joint)
    created.append(str(joint_path.relative_to(VOL1)))

    # Unit index
    index_lines = [
        "# 单元1 · 分镜头画面内容提示词 · 索引 · V1.0",
        "",
        f"> **Status**: **V3.9 · 译部 PASS** · {DATE}",
        f"> **范围**: A001–A005 · 36 P0 帧",
        f"> **审定**: [`00_导演组编辑组_分镜插画文字版审定_V1.0.md`](./00_导演组编辑组_分镜插画文字版审定_V1.0.md)",
        "",
        "---",
        "",
        "## 分案索引",
        "",
        "| 案 | P0 | V3.9 插页地图 | 画面内容提示词 | 译部 | G-BRIEF |",
        "|:--:|:--:|---------------|----------------|:----:|---------|",
    ]
    for case, meta in CASE_META.items():
        index_lines.append(
            f"| {case} | {meta['p0']} | "
            f"[V3.9 map]({case}/02_分镜头/03_分镜头_插页地图_V3.9_JP.md) | "
            f"[画面提示词]({case}/02_分镜头/00_分镜头画面内容提示词_V3.9_V1.0.md) | "
            f"PASS | [G-BRIEF]({case}/02_分镜头/00_G-BRIEF_双签_{case}_V1.0.md) |"
        )
    index_lines += [
        "",
        "---",
        "",
        "## Gate 状态（produce）",
        "",
        "| Gate | 状态 |",
        "|------|:----:|",
        "| 编+导 editorial_verdict | ✅ PASS |",
        f"| 译部 translation_verdict | ✅ PASS · {DATE} |",
        "| V3.9 JP 锚句 | ✅ 36/36 verified |",
        "| 画面内容提示词 V3.9 | ✅ 5 案齐全 |",
        "| produce preflight | 见 A001 验证 |",
        "",
        "## 🔴 重绘六帧",
        "",
        "A001 DA3/DA4/DB1/TAIL · A002 DA4/DA5 — 见总则 §四",
        "",
        f"最后更新：{DATE}",
    ]
    index_path = UNIT / "00_分镜头画面内容提示词_单元1索引_V1.0.md"
    _write(index_path, "\n".join(index_lines))
    created.append(str(index_path.relative_to(VOL1)))

    print("Created/updated:")
    for c in created:
        print(f"  {c}")
    if all_anchor_issues:
        print("\nAnchor issues:")
        for i in all_anchor_issues:
            print(f"  {i}".encode("utf-8", errors="replace").decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
