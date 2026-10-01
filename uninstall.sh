#!/usr/bin/env bash
# Gỡ team-ai-kit khỏi repo BTC trên máy này. Dùng: bash uninstall.sh [đường-dẫn-repo]
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${1:-$KIT/../P-073}" && pwd)"; cd "$REPO"
EXC=.git/info/exclude
if [ -f "$EXC" ]; then
  sed -n '/# >>> team-ai-kit/,/# <<< team-ai-kit/p' "$EXC" | grep '^/' | sed 's#^/##' | while read -r p; do
    git ls-files --error-unmatch "$p" >/dev/null 2>&1 || rm -rf "$p"
  done
  sed -i.bak '/# >>> team-ai-kit/,/# <<< team-ai-kit/d' "$EXC" && rm -f "$EXC.bak"
fi
command -v pre-commit >/dev/null 2>&1 && pre-commit uninstall >/dev/null || true
echo "Đã gỡ. Hook log AI của BTC (pre-push) giữ nguyên."
