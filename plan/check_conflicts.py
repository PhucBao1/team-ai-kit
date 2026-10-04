"""Tìm file bị ≥ 2 người sửa trong cùng tuần (dựa trên mục '## File' của card)."""
import re, sys, pathlib, collections

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
T = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / "tasks"
IGN = {"WORKLOG.md"}  # ai cũng thêm dòng của mình — append-only
def paths(text):
    sec = re.search(r"^## File\n(.*?)(?=^## )", text, re.M | re.S)
    out = set()
    if not sec: return out
    for tok in re.findall(r"`([^`]+)`", sec.group(1)):
        tok = tok.split("::")[0].split(" ")[0].strip().rstrip(",")
        if ("/" not in tok and "." not in tok) or tok.startswith("."): continue  # ".meta.yaml" = hậu tố, không phải file
        if tok.startswith("../"): tok = tok  # file của kit
        for part in re.split(r",\s*", tok):
            if part and part not in IGN: out.add(part.rstrip("/"))
    return out
def overlap(a, b):
    def base(p): return re.split(r"[*{]", p)[0].rstrip("/")
    x, y = base(a), base(b)
    return x == y or x.startswith(y + "/") or y.startswith(x + "/")
by_week = collections.defaultdict(list)
for f in sorted(T.glob("[A-D]*.md")):
    wk = f.stem[1]
    for p in paths(f.read_text(encoding="utf-8")):
        by_week[wk].append((f.stem[0], f.stem, p))
bad = 0
for wk, items in sorted(by_week.items()):
    seen = set()
    for i, (w1, id1, p1) in enumerate(items):
        for w2, id2, p2 in items[i + 1:]:
            if w1 != w2 and overlap(p1, p2):
                key = (id1, id2, p1, p2)
                if key in seen: continue
                seen.add(key); bad += 1
                print(f"Tuần {wk}: {id1} `{p1}`  ⟷  {id2} `{p2}`")
print(f"{bad} xung đột")
sys.exit(1 if bad else 0)
