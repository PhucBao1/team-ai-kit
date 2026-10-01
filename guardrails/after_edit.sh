#!/usr/bin/env bash
# Hook PostToolUse (Claude Code): sau mỗi lần AI sửa file Python → format + lint file đó;
# chạm src/core hoặc src/executor → chạy test nhanh. Không chặn (exit 0), chỉ báo để agent tự sửa.
input=$(cat)
f=$(printf '%s' "$input" | bash scripts/_pyrun.sh -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
case "$f" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then ruff format -q "$f"; ruff check -q --fix "$f" || true; fi
    case "$f" in
      *src/core/*|*src/executor/*)
        bash scripts/_pyrun.sh -m pytest -q -x tests/test_core tests/test_executor >&2 \
          || echo "Test core/executor FAIL — sửa trước khi làm tiếp." >&2 ;;
    esac ;;
esac
exit 0
