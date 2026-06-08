# -*- coding: utf-8 -*-
import os
import shutil
import glob

SRC = r"C:\Users\Lenovo\.cursor\projects\d-AI-Project-The-Academy-of-Curiosities\assets"
DST = r"D:\【AI Project】\【The Academy of Curiosities】\03_故事内容\第1卷_觉得奇怪就先观察\样章包\插图\depth_anchor"

NAMES = [
    "V-S01-V2-DEMO_广播唇不同步.png",
    "V-S02-V2-DEMO_黑板对不起.png",
    "V-S03-V2-DEMO_空海报位.png",
    "V-S04-V2-DEMO_抽屉失物.png",
    "V-S05-V2-DEMO_仅水野无影.png",
]

# Copy by index from sorted DEMO pngs in assets
src_files = sorted(glob.glob(os.path.join(SRC, "V-S*-V2-DEMO*.png")))
if len(src_files) < 5:
    src_files = sorted(glob.glob(os.path.join(SRC, "*.png")))
    src_files = [f for f in src_files if "DEMO" in os.path.basename(f)]

for i, name in enumerate(NAMES):
    if i < len(src_files):
        dest = os.path.join(DST, name)
        shutil.copy2(src_files[i], dest)
        print(f"OK {name} <- {os.path.basename(src_files[i])}")

# Remove non-canonical DEMO pngs in dst
for f in glob.glob(os.path.join(DST, "V-S*-V2-DEMO*.png")):
    if os.path.basename(f) not in NAMES:
        os.remove(f)
        print(f"removed {os.path.basename(f)}")

for name in NAMES:
    p = os.path.join(DST, name)
    print(f"exists={os.path.exists(p)} size={os.path.getsize(p) if os.path.exists(p) else 0} {name}")
