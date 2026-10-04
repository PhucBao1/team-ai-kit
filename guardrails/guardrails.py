"""Luật tất định của đội — dùng chung cho hook Claude Code và pre-commit (không chạy trên CI BTC).
Chạy với thư mục hiện tại = gốc repo P-073.

Dùng:
  python3 scripts/guardrails.py hook-edit   < JSON từ hook PreToolUse (Edit/Write/MultiEdit)
  python3 scripts/guardrails.py hook-bash   < JSON từ hook PreToolUse (Bash)
  python3 scripts/guardrails.py ci [BASE|--staged]   # CI: so với BASE (mặc định origin/main); pre-commit: --staged

Exit 2 = chặn (thông điệp ở stderr để AI agent đọc và tự sửa). Exit 0 = cho qua.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from fnmatch import fnmatch

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# --- Luật đường dẫn ---------------------------------------------------------
BTC = "File của BTC — AI không sửa; cần đổi thì hỏi người (và hỏi BTC nếu là .github/, docs/guide/)."
PROTECTED = {
    ".ai-log/*": "Log AI do hook BTC quản lý — không sửa / xoá.",
    "docs/guide/*": BTC,
    ".github/*": BTC,
    "scripts/log_*.py": BTC,
    "scripts/setup_hooks*": BTC,
    "scripts/_pyrun*": BTC,
    "scripts/submit_log.py": BTC,
    ".claude/settings.json": BTC,
    ".gemini/settings.json": BTC,
    ".cursor/hooks.json": BTC,
    ".codex/hooks.json": BTC,
    ".agents/hooks.json": BTC,
    ".agents/rules/*": BTC,
    "eval/golden/*": "Bộ golden là hợp đồng đánh giá — AI không được sửa để test pass. Người sửa qua PR (ghi GOLDEN-CHANGE: <lý do> trong mô tả PR).",
    "contracts/*": "Hợp đồng tool/agent — đổi cần PR riêng + ADR (skill write-adr). Đặt ALLOW_CONTRACT_EDIT=1 nếu người đã đồng ý.",
    ".env": "Không đọc/ghi secret. Dùng .env.example hoặc Secret Manager.",
    ".env.*": "Không đọc/ghi secret. Dùng .env.example hoặc Secret Manager.",
}
ALLOW_ENV = {"contracts/*": "ALLOW_CONTRACT_EDIT", ".github/*": "ALLOW_BTC_EDIT", "docs/guide/*": "ALLOW_BTC_EDIT"}

# --- Luật nội dung -----------------------------------------------------------
CORE_FORBIDDEN = re.compile(
    r"^\s*(from|import)\s+(langchain\w*|langgraph\w*|google\w*|httpx|requests|sqlalchemy|sqlmodel|openai|anthropic)\b",
    re.M,
)
CORE_ENV = re.compile(r"os\.environ|os\.getenv")
AGENT_WRITE_IMPORT = re.compile(r"^\s*(from\s+src\.tools(\.|\s)|import\s+src\.tools\b)", re.M)
HARDCODED_MODEL = re.compile(r"""["'](gemini-|gpt-|claude-)[\w.\-]+["']""")

BASH_BLOCK = [
    (
        re.compile(r"\bgcloud\b.*\b(run\s+deploy|deploy)\b.*\b(prod|production)\b"),
        "Không deploy lên prod từ máy/AI agent — deploy qua CI có eval gate.",
    ),
    (re.compile(r"\brm\s+-rf?\s+(/|~|\.\s*$|\*)"), "Lệnh xoá quá rộng."),
    (
        re.compile(r"(cat|less|more|head|tail|source)\s+[^|;]*\.env\b(?!\.example)"),
        "Không đọc file secret .env.",
    ),
    (re.compile(r"\bgit\s+push\b.*(--force|-f)\b.*\bmain\b"), "Không force-push lên main."),
    (re.compile(r"--no-verify\b"), "Không bỏ qua pre-commit / hook."),
]


def _norm(path: str) -> str:
    path = path.replace("\\", "/")
    root = os.getcwd().replace("\\", "/").rstrip("/") + "/"
    if path.startswith(root):
        return path[len(root) :]
    return path[2:] if path.startswith("./") else path


def check_path(path: str) -> list[str]:
    p, errs = _norm(path), []
    for pat, msg in PROTECTED.items():
        if fnmatch(p, pat) or fnmatch(os.path.basename(p), pat):
            env = ALLOW_ENV.get(pat)
            if env and os.environ.get(env) == "1":
                continue
            errs.append(f"{p}: {msg}")
    return errs


def check_content(path: str, text: str) -> list[str]:
    p, errs = _norm(path), []
    if not p.endswith(".py") or p.startswith("tests/"):
        return errs
    if p.startswith("src/core/"):
        if CORE_FORBIDDEN.search(text):
            errs.append(f"{p}: src/core/ phải là Python thuần — không import LLM/HTTP/DB (src/core/AGENTS.md).")
        if CORE_ENV.search(text):
            errs.append(f"{p}: src/core/ không đọc biến môi trường — nhận cấu hình qua tham số.")
    if p.startswith("src/agents/") and AGENT_WRITE_IMPORT.search(text):
        errs.append(f"{p}: src/agents/ không được import src.tools (tool GHI) — trả proposal, để src/executor ghi.")
    if p.startswith("src/") and p != "src/config.py" and HARDCODED_MODEL.search(text):
        errs.append(f"{p}: không hard-code tên model — cấu hình ở src/config.py / env (MODEL_CHAT, MODEL_REASON, MODEL_LITE).")
    return errs


def _block(errs: list[str]) -> int:
    if errs:
        print("Bị chặn bởi guardrails:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 2
    return 0


def hook_edit() -> int:
    data = json.load(sys.stdin)
    ti = data.get("tool_input", {})
    path = ti.get("file_path") or ti.get("path") or ""
    text = ti.get("content") or ti.get("new_string") or ""
    for e in ti.get("edits", []) or []:
        text += "\n" + e.get("new_string", "")
    return _block(check_path(path) + check_content(path, text))


def hook_bash() -> int:
    cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    return _block([msg for rx, msg in BASH_BLOCK if rx.search(cmd)])


def ci(base: str) -> int:
    staged = base == "--staged"
    args = (
        ["git", "diff", "--cached", "--name-status"]
        if staged
        else ["git", "diff", "--name-status", f"{base}...HEAD"]
    )
    out = subprocess.run(args, capture_output=True, text=True, check=True)
    changes = [ln.split("\t") for ln in out.stdout.splitlines() if ln.strip()]
    files = [c[-1] for c in changes]
    added = {c[-1] for c in changes if c[0].startswith("A")}
    pr_body = os.environ.get("PR_BODY", "")
    errs: list[str] = []
    for f in files:
        # File được bảo vệ: tạo mới thì cho qua (vd. chốt hợp đồng lần đầu); sửa thì cần lý do.
        # Ở pre-commit (--staged) chỉ nhắc, CI trên PR mới chặn.
        if (
            f in added
            or staged
            or (fnmatch(f, "eval/golden/*") and "GOLDEN-CHANGE:" in pr_body)
            or (fnmatch(f, "contracts/*") and any(x.startswith("docs/adr/") for x in files))
        ):
            pass
        else:
            errs += [e for e in check_path(f) if not e.startswith(".env")]
        if staged and f not in added and check_path(f):
            print(f"Nhắc: {f} là file được bảo vệ — PR cần ADR / GOLDEN-CHANGE, CI sẽ kiểm.", file=sys.stderr)
        if os.path.exists(f):
            errs += check_content(f, pathlib.Path(f).read_text(encoding="utf-8", errors="ignore"))
    return _block(errs)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "hook-edit":
        sys.exit(hook_edit())
    if mode == "hook-bash":
        sys.exit(hook_bash())
    if mode == "ci":
        sys.exit(ci(sys.argv[2] if len(sys.argv) > 2 else "origin/main"))
    print(__doc__)
    sys.exit(1)
