import subprocess
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) )

patterns = ["*翘边*", "*めくれた*", "*Reader*20260607*", "*Reader*20260606*", "*COVER_A*"]
files = []
for p in patterns:
    out = subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "ls-files", p],
        text=True,
        encoding="utf-8",
    )
    for line in out.splitlines():
        f = line.strip()
        if f and f not in files:
            files.append(f)

for f in files:
    print("rm", f)
    subprocess.run(["git", "rm", "-f", f], check=True, encoding="utf-8")
print("done", len(files))
