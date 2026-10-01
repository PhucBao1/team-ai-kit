> **P-073:** Tài liệu tham khảo, KHÔNG phải skill — chỉ đọc file rule cần khi skill `db-migration` trỏ tới (index FK, timestamptz, upsert, SKIP LOCKED, pagination, transaction ngắn, pooling…). Luật trong `db-migration/SKILL.md` và `../team-ai-kit/docs/conventions.md` ưu tiên hơn nội dung ở đây. Ví dụ SQL thuần; ở dự án viết bằng SQLModel/Alembic. Nguồn & thay đổi: `NOTICE.md`.

# Postgres Best Practices (vendored from Supabase, Supabase-specific parts removed)

Performance and schema guide for Postgres, maintained by Supabase. Contains rules across 8 categories, prioritized by impact to guide query optimization and schema design.

## When to Apply

Reference these guidelines when:
- Writing SQL queries or designing schemas
- Implementing indexes or query optimization
- Reviewing database performance issues
- Configuring connection pooling
- Optimizing for Postgres-specific features

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security (privileges only) | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

## Most relevant to P-073

| Need | File |
|---|---|
| Index every FK column | `schema-foreign-key-indexes.md` |
| Column types (timestamptz, text, bigint) | `schema-data-types.md` |
| Idempotent insert / upsert | `data-upsert.md` |
| Worker/detector job claiming | `lock-skip-locked.md` |
| Keep transactions short | `lock-short-transactions.md` |
| Keyset pagination | `data-pagination.md` |
| PgBouncer / prepared statements | `conn-pooling.md`, `conn-prepared-statements.md` |
| Slow query | `monitor-explain-analyze.md`, `query-missing-indexes.md` |

## How to Use

Read individual rule files for detailed explanations and SQL examples. Each rule file contains:
- Brief explanation of why it matters
- Incorrect SQL example with explanation
- Correct SQL example with explanation
- Optional EXPLAIN output or metrics
- Additional context and references

Category definitions: `_sections.md`.

## References

- https://www.postgresql.org/docs/current/
- https://wiki.postgresql.org/wiki/Performance_Optimization
