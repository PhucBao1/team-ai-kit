"""pre-commit: chặn commit nhầm file của team-ai-kit vào repo BTC (kể cả khi `git add -f`)."""

import subprocess
import sys
from fnmatch import fnmatch

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

KIT_PATTERNS = [
    "AGENTS.md", "*/AGENTS.md", "CLAUDE.md", "*/CLAUDE.md", "CLAUDE.local.md",
    ".claude/skills/*", ".agents/skills/*", ".github/skills/*",
    ".claude/settings.local.json", ".team-ai-kit*",
]


def main() -> int:
    out = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True, check=True)
    bad = [f for f in out.stdout.split() if any(fnmatch(f, p) for p in KIT_PATTERNS)]
    if bad:
        print("Không commit file của team-ai-kit vào repo BTC:\n- " + "\n- ".join(bad))
        print("Gỡ khỏi commit: git restore --staged <file>")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
