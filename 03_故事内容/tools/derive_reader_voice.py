#!/usr/bin/env python3
"""Derive Reader Voice V2.0 from G-EDITOR Hybrid Voice V2.0."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EDITOR_DIR = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/01_正文"
READER_DIR = REPO / "03_故事内容/第1卷_觉得奇怪就先观察/正式版/02_读者正文"

CASES = [
    ("A001", "案01_全班都听见了他的声音", "全班都听见了他的声音", True),
    ("A002", "案02_没有人写过的道歉", "没有人写过的道歉", False),
    ("A003", "案03_每个人都记得的海报", "每个人都记得的海报", False),
    ("A004", "案04_只出现在她抽屉里的失物", "只出现在她抽屉里的失物", False),
    ("A005", "案05_午休后消失的影子", "午休后消失的影子", False),
]

SECTION_MARKERS = {
    "A001": "序 · 公开日周",
    "A002": "二、没有人写过的道歉",
    "A003": "三、每个人都记得的海报",
    "A004": "四、只出现在她抽屉里的失物",
    "A005": "五、午休后消失的影子",
}

READER_HEADER = """《学堂趣事录》
第1卷 · 觉得奇怪，就先观察

{title}
· {case_id} · Reader Voice V2.0
· 派生自 G-EDITOR Hybrid Voice V2.0 · 2026-06-08

"""

# Tail padding markers — cut from here to 案收束 / P06
TAIL_CUT_MARKERS = {
    "A002": ["### SC-08 续 · 流程课"],
    "A003": ["### SC-07 续 · 佐佐木之后", "打印无、正式照无、残胶无——第三次写在公开说明"],
    "A004": ["### SC-08 续 · 双说明之后", "双说明贴出后：报修柜体"],
    "A005": ["### SC-02 续 · 八秒链"],
}


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"\*\*", "", text)))


def count_narrative_cjk(text: str) -> int:
    raw = text
    for marker in ["瑆笔记", "【读者可以试"]:
        idx = raw.find(marker)
        if idx > 0:
            raw = raw[:idx]
    return count_cjk(raw)


def strip_bold(s: str) -> str:
    return s.replace("**", "")


def readerize_terms(s: str) -> str:
    s = s.replace("`", "")
    s = s.replace("rehearsal_0328", "三月二十八日彩排")
    s = s.replace("三月二十八日彩排.wav", "三月二十八日彩排录音")
    s = s.replace("rehearsal_0328.wav", "三月二十八日彩排录音")
    s = s.replace("`rehearsal_0328.wav`", "三月二十八日彩排录音")
    s = s.replace("`三月二十八日彩排录音`", "三月二十八日彩排录音")
    s = re.sub(r"\bmetadata\b", "拍摄记录", s)
    s = re.sub(r"【FC-\d+[^】]*】\s*", "", s)
    s = re.sub(r"【EXPERT_LOCK】\s*", "", s)
    s = re.sub(r"wrong_responsibility[^.\n]*", "", s)
    s = re.sub(r"true_responsibility[^.\n]*", "", s)
    s = re.sub(r"repair_action[^：:\n]*[：:]", "", s)
    s = re.sub(r"\brelation\b[^.\n]*", "", s)
    s = re.sub(r"误指峰值", "误会传得最快的时候", s)
    s = re.sub(r"像FC-(\d+)", r"像那条线索", s)
    s = re.sub(r"hide\b", "藏", s)
    s = re.sub(r"remember\b", "记住", s)
    s = re.sub(r"family\b", "一种", s)
    s = re.sub(r"repair\b", "补救", s)
    s = re.sub(r"EXPERT_LOCK", "", s)
    s = re.sub(r"仍≤5", "", s)
    s = re.sub(r"PLAY · ", "正在播放 · ", s)
    return strip_bold(s)


def is_skip_line(line: str) -> bool:
    stripped = line.strip()
    if stripped.startswith("### SC-"):
        return True
    if stripped.startswith("【V2.0") or stripped.startswith("【EDITOR NOTE"):
        return True
    skip_prefixes = ("wrong_responsibility", "true_responsibility", "relation：",
                     "relation:", "科学样本：", "SSOT：")
    return any(stripped.startswith(p) for p in skip_prefixes)


def is_continuation_header(line: str) -> bool:
    return bool(re.match(r"^### SC-\d+.*续", line.strip()))


def extract_tail_sections(raw: str) -> tuple[str, str]:
    """Extract P06 + 瑆笔记 blocks from original."""
    p06 = ""
    xing = ""
    m = re.search(
        r"(---\s*\n【读者可以试 · P06家庭实验】.*?)(?=\n瑆笔记|\Z)",
        raw,
        re.DOTALL,
    )
    if m:
        p06 = m.group(1).strip()
    m2 = re.search(
        r"(瑆笔记 · 第二真相.*?)(?=\n---\n\n【V2\.0|\Z)",
        raw,
        re.DOTALL,
    )
    if m2:
        xing = m2.group(1).strip()
    return p06, xing


def trim_a004_xing(xing: str) -> str:
    """READER_TRIM: remove 瑆尾重复收束 (合照/尺子 padding per C5)."""
    idx = xing.find("合照那天下午")
    if idx > 0:
        xing = xing[:idx].rstrip() + "\n\n\n——第四案完——\n"
    return xing


def trim_a005_xing(xing: str) -> str:
    """Trim repetitive卷终瑆笔记 padding."""
    lines = xing.split("\n")
    out = []
    for line in lines:
        if "四月最后一个公开日周的夜里" in line:
            break
        out.append(line)
    return "\n".join(out)


def process_body(raw: str, case_id: str, section_marker: str) -> str:
    start = raw.find(section_marker)
    if start < 0:
        raise ValueError(f"Marker {section_marker} not found")

    body = raw[start:]
    for end in ["\n---\n【V2.0", "\n---\n\n【V2.0"]:
        idx = body.find(end)
        if idx > 0:
            body = body[:idx]

    # Cut tail padding before continuation flood
    for marker in TAIL_CUT_MARKERS.get(case_id, []):
        idx = body.find(marker)
        if idx > 0:
            body = body[:idx]

    # Cut at first ### SC-* 续 if no explicit marker (A002 fallback)
    if case_id == "A002":
        m = re.search(r"\n### SC-\d+ 续", body)
        if m:
            body = body[: m.start()]

    lines = body.split("\n")
    processed = []
    for line in lines:
        if is_skip_line(line) or is_continuation_header(line):
            continue
        if line.strip().startswith("---"):
            continue
        processed.append(line)

    # Trim to 案收束 line inclusive; if cut removed it, append standard ending
    final = []
    has_close = False
    for line in processed:
        final.append(line)
        if re.search(r"（案[①②③④⑤]", line) and "收束" in line:
            has_close = True
            break

    if not has_close:
        close_map = {
            "A001": "——第一案完——",
            "A002": "——第二案完——",
            "A003": "——第三案完——",
            "A004": "——第四案完——",
            "A005": "——第五案完——\n——第一单元完——",
        }
        final.append("")
        final.append(close_map.get(case_id, ""))

    return "\n".join(final)


def main():
    READER_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    xing_trim = {"A004": trim_a004_xing, "A005": trim_a005_xing}

    for case_id, fname, title, _ in CASES:
        editor_path = EDITOR_DIR / f"{fname}_HybridVoice_V2.0.txt"
        raw = editor_path.read_text(encoding="utf-8")
        body = process_body(raw, case_id, SECTION_MARKERS[case_id])
        body = readerize_terms(body)
        p06, xing = extract_tail_sections(raw)
        p06 = readerize_terms(p06) if p06 else ""
        xing = readerize_terms(xing) if xing else ""
        if case_id in xing_trim and xing:
            xing = xing_trim[case_id](xing)

        parts = [READER_HEADER.format(title=title, case_id=case_id).strip(), body.strip()]
        if p06:
            parts.append("\n\n" + p06)
        if xing:
            parts.append("\n\n" + xing)
        text = "\n".join(parts) + "\n"

        # Collapse 3+ blank lines to 2
        text = re.sub(r"\n{4,}", "\n\n\n", text)

        out_path = READER_DIR / f"{fname}_ReaderVoice_V2.0.txt"
        out_path.write_text(text, encoding="utf-8")
        nar = count_narrative_cjk(text)
        full = count_cjk(text)
        results.append((case_id, out_path.name, nar, full))
        print(f"{case_id} narrative={nar} full={full}")

    return results


if __name__ == "__main__":
    main()
