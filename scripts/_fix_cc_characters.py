# -*- coding: utf-8 -*-
import glob
from pathlib import Path
paths = glob.glob(str(Path(__file__).resolve().parents[1] / "【CC】files/characters.html"))
p = Path(paths[0])
t = p.read_text(encoding="utf-8")
t = t.replace("泉蔹", "泉藏").replace("泉蔹", "泉藏")
t = t.replace("せんzō · Kasai", "せんzō ※ · Kasai")
if "泉藏" not in t:
    # fallback: replace between 葛西 and community role
    import re
    t = re.sub(r"(葛西 )泉.", r"\1泉藏", t)
p.write_text(t, encoding="utf-8")
print("fixed", p)
