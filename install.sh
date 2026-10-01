#!/usr/bin/env bash
# Gắn team-ai-kit vào repo BTC (P-073) trên MÁY NÀY — không commit, không push gì lên BTC.
# Dùng:  bash install.sh [đường-dẫn-repo]   (mặc định ../P-073)   ·   --copy: chép thay vì symlink (Windows không bật symlink)
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE=link
REPO=""
for a in "$@"; do
  case "$a" in
    --copy) MODE=copy ;;
    *) REPO="$a" ;;
  esac
done
REPO="$(cd "${REPO:-$KIT/../P-073}" && pwd)"
[ -d "$REPO/.git" ] || { echo "Không thấy repo git ở $REPO"; exit 1; }
[ -d "$REPO/src" ] || { echo "$REPO không giống repo template BTC (thiếu src/)"; exit 1; }
cd "$REPO"

INSTALLED=()
tracked() { git ls-files --error-unmatch "$1" >/dev/null 2>&1; }
place() {  # place <nguồn trong kit> <đích trong repo>
  local src="$1" dst="$2"
  if tracked "$dst"; then echo "  ! bỏ qua $dst — file này đã có trong repo BTC"; return; fi
  mkdir -p "$(dirname "$dst")"
  rm -rf "$dst"
  if [ "$MODE" = link ]; then ln -s "$src" "$dst"; else cp -R "$src" "$dst"; fi
  INSTALLED+=("$dst")
  echo "  + $dst"
}

echo "[1/5] Luật cho AI agent (AGENTS.md, CLAUDE.md)"
while IFS= read -r f; do
  rel="${f#"$KIT/rules/"}"
  dir="$(dirname "$rel")"
  if [ "$dir" != "." ] && [ ! -d "$dir" ]; then echo "  · chưa có $dir/ — chạy lại install.sh khi thư mục được tạo"; continue; fi
  place "$f" "$rel"
done < <(find "$KIT/rules" -type f \( -name AGENTS.md -o -name CLAUDE.md \) | sort)

echo "[2/5] Skills cho Claude Code / Codex / Copilot"
for d in .claude/skills .agents/skills .github/skills; do place "$KIT/skills" "$d"; done

echo "[3/5] Hook guardrails cho Claude Code (.claude/settings.local.json — chạy CÙNG hook log của BTC)"
if [ -e .claude/settings.local.json ] && ! grep -q "team-ai-kit" .claude/settings.local.json 2>/dev/null \
   && ! grep -q "$KIT" .claude/settings.local.json 2>/dev/null; then
  cp .claude/settings.local.json .claude/settings.local.json.bak
  echo "  ! đã có settings.local.json riêng → sao lưu .bak rồi ghi đè (gộp tay nếu cần)"
fi
sed "s#__KIT__#$KIT#g" "$KIT/guardrails/settings.local.template.json" > .claude/settings.local.json
INSTALLED+=(".claude/settings.local.json")

echo "[4/5] Giấu khỏi git (.git/info/exclude — chỉ nằm trên máy này)"
EXC=.git/info/exclude
mkdir -p .git/info; touch "$EXC"
sed -i.bak '/# >>> team-ai-kit/,/# <<< team-ai-kit/d' "$EXC" && rm -f "$EXC.bak"
{
  echo "# >>> team-ai-kit (không sửa tay — install.sh quản lý)"
  printf '/%s\n' "${INSTALLED[@]}"
  echo "/.claude/settings.local.json.bak"
  echo "# <<< team-ai-kit"
} >> "$EXC"

echo "[5/5] pre-commit (hook pre-commit; KHÔNG đụng pre-push của BTC)"
mkdir -p "$KIT/.generated"
sed "s#__KIT__#$KIT#g" "$KIT/guardrails/pre-commit.template.yaml" > "$KIT/.generated/pre-commit.yaml"
if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install -c "$KIT/.generated/pre-commit.yaml" >/dev/null && echo "  + .git/hooks/pre-commit"
else
  echo "  ! chưa có pre-commit: pip install pre-commit rồi chạy lại install.sh"
fi
[ -f .git/hooks/pre-push ] || echo "  ! chưa có hook log AI của BTC — chạy: bash scripts/setup_hooks.sh"

echo
if [ -n "$(git status --porcelain -- "${INSTALLED[@]}" 2>/dev/null)" ]; then
  echo "CẢNH BÁO: git vẫn thấy file của kit:"; git status --porcelain -- "${INSTALLED[@]}"; exit 1
fi
echo "Xong. git status sạch với file của kit. Luật: AGENTS.md · Skills: .claude/skills · Kế hoạch: $KIT/plan/"
