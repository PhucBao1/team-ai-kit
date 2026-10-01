"""Sinh sơ đồ Mermaid từ chính LangGraph để sơ đồ 04 không lệch code.

Dùng (từ gốc repo P-073): make -f ../team-ai-kit/kit.mk diagrams-export
Tìm trong src/agents/graph.py: biến `agent` (template) / `graph` / `app`, hoặc hàm `build_graph()`.
"""

import importlib
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(
    subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
)
OUT = ROOT / "docs/architecture/04-agent-graph.generated.mmd"


def main() -> int:
    if not (ROOT / "src/agents/graph.py").exists():
        print("src/agents/graph.py chưa có — bỏ qua.")
        return 0
    sys.path.insert(0, str(ROOT))
    mod = importlib.import_module("src.agents.graph")
    g = getattr(mod, "agent", None) or getattr(mod, "graph", None) or getattr(mod, "app", None)
    if g is None and hasattr(mod, "build_graph"):
        g = mod.build_graph()
    if g is None:
        print("Không tìm thấy agent/graph/app/build_graph() trong src/agents/graph.py")
        return 1
    if hasattr(g, "compile") and not hasattr(g, "get_graph"):
        g = g.compile()
    mermaid = g.get_graph(xray=True).draw_mermaid()
    note = "%% Sinh tự động từ src/agents/graph.py — KHÔNG sửa tay. Chạy: make -f ../team-ai-kit/kit.mk diagrams-export\n"
    if mermaid.startswith("---"):  # frontmatter phải ở đầu file → chèn ghi chú sau frontmatter
        end = mermaid.index("---", 3) + 3
        mermaid = mermaid[:end] + "\n" + note + mermaid[end:].lstrip("\n")
    else:
        mermaid = note + mermaid
    OUT.write_text(mermaid, encoding="utf-8")
    print(f"Đã ghi {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
