#!/usr/bin/env python3
"""Second pass: move remaining 01_正文 files + remove duplicates already in version folders."""
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT / "正式版" / "01_正文"
NEW = ROOT / "单元1_第一单元_五案"

VERSION_PATTERNS = [
    (re.compile(r"_HybridVoice_V1\.1定稿"), "V1.1", "cn"),
    (re.compile(r"_V1\.1定稿_日本語"), "V1.1", "jp"),
    (re.compile(r"_HybridVoice_V1\.2文学重写"), "V1.2", "cn"),
    (re.compile(r"_HybridVoice_V2\.0\.txt$"), "V2.0", "cn"),
    (re.compile(r"_HybridVoice_V2\.0_日本語"), "V2.0", "jp"),
    (re.compile(r"_HybridVoice_V2\.0_R"), "V2.0", "opinion"),
    (re.compile(r"_HybridVoice_V2\.1\.txt$"), "V2.1", "cn"),
    (re.compile(r"_HybridVoice_V2\.1_日本語"), "V2.1", "jp"),
    (re.compile(r"_HybridVoice_V2\.1_R"), "V2.1", "opinion"),
    (re.compile(r"_A001_"), "V2.1", "opinion"),
]

SUB = {"cn": "01_中文", "jp": "02_日本語", "opinion": "03_版本意见"}

UNIT_DOCS = {
    "00_第一单元_V2_中文正文_阅读索引.md": "00_单元说明/00_阅读索引.md",
    "README_两轨说明_V0.1.md": "00_单元说明/README_两轨说明_V0.1.md",
    "00_第一单元_V2_Voice归一化摘要_V0.1.md": "00_单元说明/00_Voice归一化摘要_V0.1.md",
    "00_GPT_LOCK补丁_专家组复评_V0.1.md": "00_单元说明/00_GPT_LOCK补丁_专家组复评_V0.1.md",
}


def classify(name: str) -> tuple[str, str] | None:
    for pat, ver, kind in VERSION_PATTERNS:
        if pat.search(name):
            return ver, kind
    return None


def main() -> None:
    if not OLD.exists():
        print("OLD missing")
        return
    moved = removed = 0
    for f in list(OLD.iterdir()):
        if not f.is_file() or f.name.startswith("README_"):
            continue
        if f.name in UNIT_DOCS:
            dst = NEW / UNIT_DOCS[f.name]
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                f.unlink()
                removed += 1
            else:
                shutil.move(str(f), str(dst))
                moved += 1
            continue
        cls = classify(f.name)
        if not cls:
            print(f"UNCLASSIFIED: {f.name}")
            continue
        ver, kind = cls
        dst_dir = NEW / "正文" / ver / SUB[kind]
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / f.name
        if dst.exists():
            f.unlink()
            removed += 1
        else:
            shutil.move(str(f), str(dst))
            moved += 1
    print(f"moved={moved} removed_dup={removed}")


if __name__ == "__main__":
    main()
