"""Kiểm sơ đồ kiến trúc trong docs/architecture/.

Dùng:
  python3 scripts/ci/check_diagrams.py             # kiểm nội dung
  python3 scripts/ci/check_diagrams.py origin/main # thêm kiểm "đổi kiến trúc mà không đổi sơ đồ" (CI trên PR)

Kiểm:
  1. Mọi file liệt kê trong README tồn tại; mọi file sơ đồ đều có trong README.
  2. File .md có ít nhất một khối ```mermaid với loại sơ đồ hợp lệ.
  3. File .drawio.svg còn dữ liệu sửa được (thuộc tính content chứa mxfile) — không phải ảnh xuất thường.
  4. Tên tool dạng `ten_tool(` trong sơ đồ phải có trong contracts/tools.yaml; loại sự kiện a.b.c phải có trong contracts/events.yaml.
  6. Quy tắc vẽ: flowchart Mermaid có subgraph (nhóm) và mọi cạnh có nhãn; mọi cạnh draw.io có nhãn (hướng dữ liệu);
     sơ đồ luồng (NUMBERED) có đánh số "(1)" hoặc `autonumber`.
  5. (có BASE) PR đổi agent/graph.py, agent/subagents/, contracts/, db/migrations/ mà không đổi docs/architecture/
     → lỗi, trừ khi mô tả PR có `DIAGRAM-NOCHANGE: <lý do>` (biến môi trường PR_BODY).
Cú pháp Mermaid được kiểm riêng bằng mermaid-cli trong CI (xem .github/workflows/guardrails.yml).
"""

import os
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET  # chỉ đọc file trong repo

import yaml

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(
    subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
)
ARCH = ROOT / "docs/architecture"
TYPES = ("flowchart", "graph", "sequenceDiagram", "stateDiagram", "erDiagram", "classDiagram", "C4")
# hàm nội bộ hợp lệ trong sơ đồ, không phải tool trong hợp đồng
INTERNAL = {
    "interrupt",
    "draw_mermaid",
    "claim_check",
    "validate",
    "run",
    "build_graph",
    "reachable",
    "warranty_precheck",
}
TRIGGERS = ("src/agents/graph.py", "src/agents/subgraphs/", "contracts/", "migrations/")
NUMBERED = ("02-", "03-", "04-", "05-", "06-", "09-")  # sơ đồ có luồng tuần tự phải đánh số
EDGE = re.compile(r"^[ \t]*\S+[ \t]*(-->|-\.->|==>)(?!\|)[ \t]*\S", re.M)  # cạnh flowchart không có |nhãn|


def main() -> int:
    errs: list[str] = []
    if not ARCH.exists():
        print("docs/architecture chưa có — bỏ qua.")
        return 0
    readme = (ARCH / "README.md").read_text(encoding="utf-8")
    listed = {f for f in re.findall(r"\]\(([^)#]+\.(?:md|svg|mmd))\)", readme) if "/" not in f}
    files = {p.name for p in ARCH.iterdir() if p.suffix in (".md", ".svg") and p.name != "README.md"}
    for f in sorted(listed - {p.name for p in ARCH.iterdir()}):
        errs.append(f"README trỏ tới {f} nhưng file không tồn tại")
    for f in sorted(files - listed):
        errs.append(f"{f} chưa có trong bảng docs/architecture/README.md")

    tools = {
        t["name"]
        for t in yaml.safe_load((ROOT / "contracts/tools.yaml").read_text(encoding="utf-8"))["tools"]
    }
    events = {
        e["type"]
        for e in yaml.safe_load((ROOT / "contracts/events.yaml").read_text(encoding="utf-8"))["events"]
    }

    for p in sorted(ARCH.glob("*.md")):
        if p.name == "README.md":
            continue
        text = p.read_text(encoding="utf-8")
        blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
        if not blocks:
            errs.append(f"{p.name}: không có khối ```mermaid")
        for b in blocks:
            first = next(
                (ln.strip() for ln in b.splitlines() if ln.strip() and not ln.strip().startswith("%%")), ""
            )
            if not first.startswith(TYPES):
                errs.append(f"{p.name}: loại sơ đồ không hợp lệ: '{first[:40]}'")
            if first.startswith(("flowchart", "graph")):
                if "subgraph" not in b:
                    errs.append(f"{p.name}: flowchart chưa phân nhóm bằng subgraph (quy tắc 2)")
                for m in EDGE.finditer(b):
                    line = b[m.start() : b.find("\n", m.start())].strip()
                    errs.append(f"{p.name}: cạnh chưa có nhãn dữ liệu (quy tắc 3): {line[:60]}")
            for name in set(re.findall(r"\b([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\(", b)):
                if name not in tools and name not in INTERNAL:
                    errs.append(f"{p.name}: '{name}(' không có trong contracts/tools.yaml")
            for ev in set(re.findall(r"\b([a-z_]+\.[a-z_]+\.[a-z_]+)\b", b)):
                if (
                    ev.split(".")[0] in {"vehicle", "parts", "appointment", "repair_order", "chat"}
                    and ev not in events
                ):
                    errs.append(f"{p.name}: sự kiện '{ev}' không có trong contracts/events.yaml")

    for p in sorted(ARCH.glob("*.drawio.svg")):
        raw = p.read_text(encoding="utf-8", errors="ignore")
        if 'content="' not in raw[:5000] or "mxfile" not in raw[:5000]:
            errs.append(
                f"{p.name}: mất dữ liệu sửa được — lưu lại bằng draw.io dạng 'Editable SVG' (.drawio.svg)"
            )
            continue
        model = ET.fromstring(ET.fromstring(raw).get("content", ""))
        if model.find(".//mxGraphModel") is None:
            errs.append(
                f"{p.name}: dữ liệu draw.io bị nén — trong draw.io tắt Extras → Compressed rồi lưu lại"
            )
            continue
        for c in model.iter("mxCell"):
            if c.get("edge") == "1" and not (c.get("value") or "").strip():
                errs.append(
                    f"{p.name}: cạnh {c.get('source')} → {c.get('target')} chưa có nhãn dữ liệu (quy tắc 3)"
                )
        if p.name.startswith(NUMBERED) and "(1)" not in raw:
            errs.append(f"{p.name}: luồng tuần tự chưa đánh số (1), (2)… (quy tắc 4)")

    for p in sorted(ARCH.glob("*.md")):
        if p.name.startswith(NUMBERED):
            t = p.read_text(encoding="utf-8")
            if "(1)" not in t and "autonumber" not in t:
                errs.append(f"{p.name}: luồng tuần tự chưa đánh số (1), (2)… hoặc autonumber (quy tắc 4)")

    if len(sys.argv) > 1:
        base = sys.argv[1]
        out = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True, check=True
        )
        changed = [f for f in out.stdout.split() if f]
        touched = [f for f in changed if f.startswith(TRIGGERS)]
        no_diagram = not any(f.startswith("docs/architecture/") for f in changed)
        if touched and no_diagram and "DIAGRAM-NOCHANGE:" not in os.environ.get("PR_BODY", ""):
            errs.append(
                "PR đổi " + ", ".join(touched[:5]) + " nhưng không cập nhật docs/architecture/ "
                "(skill update-architecture-diagram) — hoặc ghi 'DIAGRAM-NOCHANGE: <lý do>' trong mô tả PR"
            )

    if errs:
        print("Sơ đồ kiến trúc có vấn đề:\n- " + "\n- ".join(errs))
        return 1
    print(f"diagrams OK ({len(files)} file)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
