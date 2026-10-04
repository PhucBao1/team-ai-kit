"""Đếm task đã tick theo người và tuần. Dùng: python3 plan/progress.py"""

import sys
import pathlib
import re

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HERE = pathlib.Path(__file__).parent
for f in sorted(HERE.glob("[A-D]-*.md")):
    text = f.read_text(encoding="utf-8")
    weeks = re.split(r"^## ", text, flags=re.M)[1:]
    parts = []
    for w in weeks:
        title = w.splitlines()[0].split("·")[0].strip()
        done = len(re.findall(r"^- \[x\]", w, flags=re.M | re.I))
        total = done + len(re.findall(r"^- \[ \]", w, flags=re.M))
        if total:
            parts.append(f"{title}: {done}/{total}")
    print(f"{f.stem:16} " + " | ".join(parts))
