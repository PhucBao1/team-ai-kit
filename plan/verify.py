#!/usr/bin/env python3
"""Chạy mục "Kiểm xong" của task card — chỉ tick [x] khi lệnh này báo ĐẠT.

Dùng (từ gốc repo P-073):
    python3 ../team-ai-kit/plan/verify.py D1.05
    python3 ../team-ai-kit/plan/verify.py A1.02 B1.02 --keep-going
    python3 ../team-ai-kit/plan/verify.py --list          # liệt kê card

Quy ước card: trong khối ```bash của mục "## Kiểm xong", mỗi dòng bắt đầu bằng
"$ " là một lệnh phải thoát 0. Các dòng "- [ ]" sau khối là kiểm tay (in ra để
người làm tự xác nhận, không chặn).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TASKS = Path(__file__).resolve().parent / "tasks"
DEFAULT_ENV = {"APP_ENV": "test", "OPENAI_API_KEY": "test-key"}
TIMEOUT_S = 900


def parse_card(path: Path) -> tuple[str, list[str], list[str]]:
    """Trả về (tiêu đề, danh sách lệnh, danh sách kiểm tay)."""
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    m = re.search(r"^## Kiểm xong\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        raise SystemExit(f"{path.name}: thiếu mục '## Kiểm xong'")
    section = m.group(1)
    cmds: list[str] = []
    for block in re.findall(r"```(?:bash|sh)?\n(.*?)```", section, re.S):
        cmds += [ln[2:].strip() for ln in block.splitlines() if ln.startswith("$ ")]
    manual = [ln.strip()[5:].strip() for ln in section.splitlines() if ln.strip().startswith("- [ ]")]
    return title, cmds, manual


def run_card(task_id: str, verbose: bool) -> bool:
    """Chạy mọi lệnh của một card, in kết quả, trả True nếu đạt."""
    path = TASKS / f"{task_id}.md"
    if not path.exists():
        print(f"✗ {task_id}: không có card {path}")
        return False
    title, cmds, manual = parse_card(path)
    print(f"\n━━ {title}")
    if not cmds:
        print("  ✗ card không có lệnh '$ ' nào trong 'Kiểm xong' — sửa card trước")
        return False
    env = {**DEFAULT_ENV, **os.environ}
    venv_bin = Path(".venv/bin").resolve()
    if venv_bin.is_dir() and "VIRTUAL_ENV" not in os.environ:
        env["PATH"] = f"{venv_bin}{os.pathsep}{env.get('PATH', '')}"  # dùng .venv của repo nếu chưa activate
    ok = True
    for cmd in cmds:
        t0 = time.time()
        try:
            r = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True,
                               timeout=TIMEOUT_S, executable="/bin/bash")
            code, out = r.returncode, (r.stdout + r.stderr)
        except subprocess.TimeoutExpired:
            code, out = 124, f"quá {TIMEOUT_S}s"
        mark = "✓" if code == 0 else "✗"
        print(f"  {mark} {cmd}  ({time.time() - t0:.1f}s)")
        if code != 0 or verbose:
            tail = "\n".join(out.strip().splitlines()[-15:])
            if tail:
                print("    " + tail.replace("\n", "\n    "))
        ok = ok and code == 0
    for item in manual:
        print(f"  ☐ (kiểm tay) {item}")
    print(f"  → {'ĐẠT — được tick [x]' if ok else 'CHƯA ĐẠT — chưa tick'}")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="mã task, vd D1.05")
    ap.add_argument("--list", action="store_true", help="liệt kê card")
    ap.add_argument("-v", "--verbose", action="store_true", help="in output cả khi đạt")
    ap.add_argument("--keep-going", action="store_true", help="chạy tiếp khi một card trượt")
    a = ap.parse_args()
    if a.list:
        for p in sorted(TASKS.glob("[A-D]*.md")):
            print(parse_card(p)[0])
        return 0
    if not a.ids:
        ap.error("cần ít nhất một mã task")
    if not Path("src").is_dir() or not Path("tests").is_dir():
        print("! Chạy từ gốc repo P-073 (thư mục có src/ và tests/)")
        return 2
    results = {}
    for tid in a.ids:
        results[tid] = run_card(tid.upper(), a.verbose)
        if not results[tid] and not a.keep_going:
            break
    passed = [t for t, v in results.items() if v]
    print(f"\nTổng: {len(passed)}/{len(a.ids)} đạt")
    return 0 if len(passed) == len(a.ids) else 1


if __name__ == "__main__":
    sys.exit(main())
