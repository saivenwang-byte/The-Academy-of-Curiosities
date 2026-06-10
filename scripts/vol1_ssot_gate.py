#!/usr/bin/env python3
"""Vol1 SSOT gate — verify per-case canon paths before write/build/report.

Usage:
  python scripts/vol1_ssot_gate.py
  python scripts/vol1_ssot_gate.py --case A001
  python scripts/vol1_ssot_gate.py --strict   # fail on legacy-only duplicates
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VOL1 = ROOT / "03_故事内容/第1卷_觉得奇怪就先观察"
UNIT = VOL1 / "单元1_第一单元_五案"

CASES = ["A001", "A002", "A003", "A004", "A005"]
CASE_NUM = {"A001": "01", "A002": "02", "A003": "03", "A004": "04", "A005": "05"}


@dataclass
class Result:
    ok: bool
    label: str
    detail: str


JP_POINTER_RE = re.compile(
    r"\./01_正文/((?:案\d+_[^`]+\*_日本語\.txt)|(?:[^`]+\*_日本語\.txt))"
)


def parse_pointer_jp_filename(case: str) -> str | None:
    """Read canonical JP filename from 00_正典指针.md (SSOT over glob order)."""
    ptr = UNIT / case / "00_正典指针.md"
    if not ptr.is_file():
        return None
    text = ptr.read_text(encoding="utf-8")
    for m in JP_POINTER_RE.finditer(text):
        name = m.group(1)
        if "日本語" in name:
            return name
    fallback = re.search(r"案\d+_[^\s`]+\*_V[\d.]+\_日本語\.txt", text)
    return fallback.group(0) if fallback else None


def check_pointer(case: str) -> list[Result]:
    out: list[Result] = []
    ptr = UNIT / case / "00_正典指针.md"
    if not ptr.is_file():
        out.append(Result(False, f"{case} 正典指针", "missing 00_正典指针.md"))
        return out
    out.append(Result(True, f"{case} 正典指针", "ok"))
    body = UNIT / case / "01_正文"
    n = CASE_NUM[case]
    cn = list(body.glob(f"案{n}_*.txt"))
    cn = [p for p in cn if "日本語" not in p.name and "_archive" not in str(p)]
    jp_live = [
        p
        for p in body.glob(f"案{n}_*_日本語.txt")
        if "_archive" not in str(p)
    ]
    canon_name = parse_pointer_jp_filename(case)
    if not cn:
        out.append(Result(False, f"{case} CN 正文", "01_正文/ 无案 CN 文件"))
    else:
        out.append(Result(True, f"{case} CN 正文", cn[0].name))
    if not jp_live:
        out.append(Result(False, f"{case} JP 正文", "01_正文/ 无案 JP 文件"))
        return out
    if canon_name:
        canon_path = body / canon_name
        if not canon_path.is_file():
            out.append(
                Result(
                    False,
                    f"{case} JP 正文",
                    f"指针指定 {canon_name} 不存在于 01_正文/",
                )
            )
        elif len(jp_live) > 1:
            others = [p.name for p in jp_live if p.name != canon_name]
            out.append(
                Result(
                    False,
                    f"{case} JP 正文",
                    f"多份 JP 并存 · 指针={canon_name} · 待归档 {others}",
                )
            )
        else:
            out.append(Result(True, f"{case} JP 正文", canon_name))
    else:
        if len(jp_live) > 1:
            out.append(
                Result(
                    False,
                    f"{case} JP 正文",
                    f"多份 JP 且无指针 · {[p.name for p in jp_live]}",
                )
            )
        else:
            out.append(Result(True, f"{case} JP 正文", jp_live[0].name))
    return out


def check_shims() -> list[Result]:
    out: list[Result] = []
    jp_shim = UNIT / "正文" / "V3.8" / "02_日本語"
    ill_shim = UNIT / "插图" / "绑定正文_V3.6"
    if jp_shim.is_dir() and any(jp_shim.glob("案*_日本語.txt")):
        out.append(Result(True, "正文 shim V3.8", "ok"))
    else:
        out.append(Result(False, "正文 shim V3.8", "missing or empty"))
    if ill_shim.is_dir():
        subs = [d.name for d in ill_shim.iterdir() if d.is_dir() and d.name.startswith("A")]
        out.append(Result(len(subs) >= 1, "插图 shim V3.6", f"{len(subs)} case dirs"))
    else:
        out.append(Result(False, "插图 shim V3.6", "missing"))
    return out


SHIM_VERSION_DIRS = frozenset({"V3.1", "V3.6", "V3.7", "V3.8", "V3.8.1", "V3.9"})


def check_no_version_folders() -> list[Result]:
    """Block new 正文/V3.9-style folders; known tool shims are allowed."""
    out: list[Result] = []
    live = UNIT / "正文"
    if not live.is_dir():
        return out
    bad = [
        p.name
        for p in live.iterdir()
        if p.is_dir() and p.name.startswith("V") and p.name not in SHIM_VERSION_DIRS
    ]
    if bad:
        out.append(
            Result(
                False,
                "禁止新横切版本夹",
                f"正文/ 下出现 {bad} — 升版请写 A00X/01_正文/文件名",
            )
        )
    else:
        out.append(Result(True, "禁止新横切版本夹", "ok"))
    return out


def check_nested_mirror() -> list[Result]:
    out: list[Result] = []
    nested = VOL1 / "V2迁移/打包/第二次检查上传包_V0.1/03_故事内容"
    if nested.exists():
        out.append(
            Result(
                False,
                "V2 嵌套镜像",
                "应已删除 — 运行 tools/flatten_v2_upload_mirror.py",
            )
        )
    else:
        out.append(Result(True, "V2 嵌套镜像", "clean"))
    return out


def run(cases: list[str], strict: bool) -> int:
    results: list[Result] = []
    for c in cases:
        results.extend(check_pointer(c))
    results.extend(check_shims())
    results.extend(check_no_version_folders())
    results.extend(check_nested_mirror())

    fails = [r for r in results if not r.ok]
    for r in results:
        tag = "PASS" if r.ok else "FAIL"
        print(f"[{tag}] {r.label}: {r.detail}")

    print()
    print(f"=== SSOT GATE · {len(results) - len(fails)}/{len(results)} PASS ===")
    if fails:
        return 1
    if strict:
        print("(strict mode: legacy trees not audited — see 00_目录架构_三段式_V1.0.md)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Vol1 SSOT path gate")
    ap.add_argument("--case", choices=CASES)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    cases = [args.case] if args.case else CASES
    return run(cases, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
