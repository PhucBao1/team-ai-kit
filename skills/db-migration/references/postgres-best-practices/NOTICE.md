# NOTICE

- Dự án gốc: Supabase Agent Skills — `supabase-postgres-best-practices` (v1.1.1)
- Repo: https://github.com/supabase/agent-skills
- Commit: `544bfc56c8`
- Đường dẫn gốc: `skills/supabase-postgres-best-practices/` (`SKILL.md`, `references/*.md`)
- License: MIT (Copyright (c) 2026 Supabase) — bản gốc trong `LICENSE`.

## Đã sửa (P-073 team, 2026-10-01)
- `SKILL.md` → `README.md`: bỏ frontmatter (để KHÔNG thành skill tự kích hoạt), thêm dòng đầu "tài liệu tham khảo, đọc khi cần", bỏ nhắc RLS và link docs Supabase, thêm bảng "Most relevant to P-073".
- Không chép: `references/security-rls-basics.md`, `security-rls-performance.md`, `conn-limits.md`, `conn-idle-timeout.md` (dành cho Supabase / không áp dụng), `_template.md`, `_contributing.md`, `CHANGELOG.md`.
- `_sections.md`: bỏ câu hướng dẫn mẫu; sửa mô tả mục Connection và Security (không còn RLS).
- `conn-prepared-statements.md`: bỏ số cổng pooler riêng của Supabase; thêm ghi chú asyncpg `statement_cache_size=0`.
- Các file `references` còn lại: giữ nguyên (kể cả link tham khảo tới docs Supabase).
