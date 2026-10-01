"""So contracts/tools.yaml với code trong tools/ (đọc bằng AST — không cần cài dependency của app).

Kiểm:
  1. Tool đã tới mốc (CONTRACT_MILESTONE, mặc định MVP; thứ tự MVP < W1 < W2) phải có hàm cùng tên trong `module`.
     Thiếu file/hàm chỉ là CẢNH BÁO, trừ khi CONTRACT_STRICT=1 (bật trong CI từ sau demo MVP 30/9).
  2. Tham số hàm khớp `input` — hoặc hàm nhận 1 tham số kiểu Pydantic model (class cùng file) có đúng các field đó.
  3. Tool level 2 phải có `confirmation_token` trong input.
  4. Không file nào trong src/agents/ (trừ tools/) nhắc tới tên tool level 2 (agent chỉ đề xuất; src/executor mới gọi).
Repo chưa có file .py nào trong tools/ → chỉ kiểm cú pháp hợp đồng.
"""

from __future__ import annotations

import ast
import os
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(
    subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
)
ORDER = {"MVP": 0, "W1": 1, "W2": 2}
current = ORDER[os.environ.get("CONTRACT_MILESTONE", "MVP")]
STRICT = os.environ.get("CONTRACT_STRICT") == "1"


def fields_of(fn: ast.AST, classes: dict[str, ast.ClassDef]) -> set[str]:
    """Tên tham số của tool; nếu (ngoài idempotency_key / ctx) chỉ còn 1 tham số kiểu model cùng file → field của model."""
    args = [a for a in fn.args.args + fn.args.kwonlyargs if a.arg not in ("self", "cls", "idempotency_key", "ctx")]
    if len(args) == 1 and isinstance(args[0].annotation, ast.Name) and args[0].annotation.id in classes:
        cls = classes[args[0].annotation.id]
        return {n.target.id for n in cls.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)}
    return {a.arg for a in args}


def main() -> int:
    spec = yaml.safe_load((ROOT / "contracts/tools.yaml").read_text(encoding="utf-8"))
    code_dirs = [ROOT / "src/agents/tools", ROOT / "src/tools"]
    has_code = any(p.name != "__init__.py" for d in code_dirs if d.exists() for p in d.rglob("*.py"))
    if not has_code:
        print("src/agents/tools, src/tools chưa có tool — chỉ kiểm cú pháp hợp đồng.")
    errs: list[str] = []
    warns: list[str] = []
    level2 = []
    for t in spec["tools"]:
        name, inp = t["name"], set((t.get("input") or {}).keys())
        if t["level"] == 2:
            level2.append(name)
            if "confirmation_token" not in inp:
                errs.append(f"{name}: level 2 phải có confirmation_token trong input")
        if not has_code or ORDER[t["milestone"]] > current:
            continue
        mod = ROOT / t["module"]
        if not mod.exists():
            (errs if STRICT else warns).append(f"{name}: chưa có file {t['module']} (mốc {t['milestone']})")
            continue
        tree = ast.parse(mod.read_text(encoding="utf-8"))
        classes = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        fns = {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        if name not in fns:
            (errs if STRICT else warns).append(f"{name}: không thấy hàm trong {t['module']}")
            continue
        got = fields_of(fns[name], classes)
        if got != inp:
            errs.append(f"{name}: input hợp đồng {sorted(inp)} ≠ code {sorted(got)}")
    agent = ROOT / "src/agents"
    if agent.exists():
        for f in agent.rglob("*.py"):
            if "tests" in f.parts or "tools" in f.relative_to(agent).parts:
                continue
            text = f.read_text(encoding="utf-8")
            for n in level2:
                if n in text:
                    errs.append(
                        f"{f.relative_to(ROOT)}: nhắc tới tool ghi '{n}' — agent chỉ trả proposal, src/executor gọi"
                    )
    if warns:
        print("Cảnh báo (chưa làm tới):\n- " + "\n- ".join(warns))
    if errs:
        print("Hợp đồng lệch:\n- " + "\n- ".join(errs))
        return 1
    print(f"contracts OK ({len(spec['tools'])} tool, mốc ≤ {os.environ.get('CONTRACT_MILESTONE', 'MVP')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
