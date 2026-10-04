"""Kiểm file luật và skill trong team-ai-kit: AGENTS.md đủ ngắn, SKILL.md đúng chuẩn mở (name khớp thư mục, description ≤ 1024)."""

import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):  # Windows console cp1252 không in được tiếng Việt → UTF-8
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = pathlib.Path(__file__).resolve().parents[1]
errs: list[str] = []

for f in (ROOT / "rules").rglob("AGENTS.md"):
    if "node_modules" in f.parts:
        continue
    n = len(f.read_text(encoding="utf-8").splitlines())
    limit = 150 if f.parent == ROOT / "rules" else 60
    if n > limit:
        errs.append(
            f"{f.relative_to(ROOT)}: {n} dòng > {limit}. Luật dài bị bỏ sót — đẩy chi tiết sang skill."
        )

for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errs.append(f"{skill}: thiếu frontmatter YAML")
        continue
    fm = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    d = skill.parent.name
    if fm.get("name") != d:
        errs.append(f"{skill.relative_to(ROOT)}: name '{fm.get('name')}' phải trùng tên thư mục '{d}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", d):
        errs.append(f"{d}: tên skill chỉ gồm chữ thường, số, gạch nối")
    desc = fm.get("description", "")
    if not desc or len(desc) > 1024:
        errs.append(f"{skill.relative_to(ROOT)}: description rỗng hoặc > 1024 ký tự")
    if "Dùng khi" not in desc:
        errs.append(
            f"{skill.relative_to(ROOT)}: description nên có 'Dùng khi …' để agent biết lúc nào nạp skill"
        )
    vendored = (skill.parent / "NOTICE.md").exists()  # skill bên ngoài đã vá: giữ LICENSE + NOTICE
    if vendored and not any((skill.parent / n).exists() for n in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
        errs.append(f"{skill.relative_to(ROOT)}: skill bên ngoài phải giữ file LICENSE gốc")
    if len(text.splitlines()) > (400 if vendored else 120):
        errs.append(
            f"{skill.relative_to(ROOT)}: quá dài (skill nhóm ≤ 120 dòng, skill ngoài ≤ 400) — tách phần tham khảo sang references/"
        )

if errs:
    print("\n".join(errs))
    sys.exit(1)
print("agent files OK")
