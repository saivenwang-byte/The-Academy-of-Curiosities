# -*- coding: utf-8 -*-
from pathlib import Path
import glob
root = Path(__file__).resolve().parents[1]
for pattern in ["docs/story_database/*.xlsx", "【CC】files/**/*.xlsx"]:
    print(pattern, list(root.glob(pattern)))