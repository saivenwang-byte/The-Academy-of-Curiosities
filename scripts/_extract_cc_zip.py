#!/usr/bin/env python3
"""Extract CC zip for analysis."""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "【CC】" / "files" / "files20260605-1.zip"
OUT = ROOT / "【CC】" / "files" / "files20260605-1_extracted"

print("ZIP exists:", ZIP.exists(), ZIP)
if not ZIP.exists():
    raise SystemExit(1)

OUT.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(ZIP) as z:
    print("Entries:", len(z.namelist()))
    for n in z.namelist():
        print(n)
    z.extractall(OUT)
print("Extracted to:", OUT)
