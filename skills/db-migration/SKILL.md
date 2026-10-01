---
name: db-migration
description: Tạo migration Postgres (bảng, cột, index, pgvector) bằng Alembic có rollback và cập nhật seed giả lập; kèm luật truy cập DB của dự án (transaction ngắn, timeout, index FK, timestamptz, idempotency ON CONFLICT, SKIP LOCKED, keyset pagination). Dùng khi đổi schema DB, thêm bảng, thêm index, viết truy vấn ghi/worker nhận việc trong src/db hoặc src/executor, hoặc task nhắc tới migration/Alembic/schema.
---

# Migration DB

Spec: `../team-ai-kit/docs/spec/08-data.md`, `16-knowledge.md` · sơ đồ `docs/architecture/08-erd.md`. Alembic ở gốc repo: `alembic.ini` + `migrations/`.
Tham khảo khi cần (không đọc hết): `references/postgres-best-practices/README.md` → mở đúng file rule. Luật dưới đây ưu tiên hơn tài liệu đó.

## Bước
1. Lần đầu (người D): `alembic init migrations`, trỏ `sqlalchemy.url` tới `DATABASE_URL` trong `migrations/env.py`, model ở `src/db/models.py`.
2. `alembic revision -m "<mô tả ngắn>"` → sửa file trong `migrations/versions/`. Viết cả `upgrade()` và `downgrade()`.
3. An toàn khi đang chạy: thêm cột nullable → backfill → NOT NULL (migration sau). Index lớn: `CREATE INDEX CONCURRENTLY` (migration riêng, xem luật 7).
4. pgvector: `CREATE EXTENSION IF NOT EXISTS vector`; HNSW `vector_cosine_ops`, `m=16, ef_construction=64`.
5. Cập nhật `src/db/models.py` (SQLModel) và `src/sim/seed.py`. Không đưa dữ liệu thật vào seed.
6. Kiểm: `make db` → `alembic upgrade head && alembic downgrade -1 && alembic upgrade head` → `python -m src.sim.seed --reset` → `pytest tests/`.
7. Cột chứa PII → ghi rõ trong docstring model. Đổi bảng → cập nhật `docs/architecture/08-erd.md`.

## Luật schema & truy cập DB
1. **Không gọi LLM / HTTP / MCP trong transaction.** Gọi ngoài trước, mở transaction sau, giữ ngắn (vài chục ms). Transaction mở chờ LLM = giữ lock + giữ connection pool. (`lock-short-transactions.md`)
2. **Timeout ở engine**, đặt trong `connect_args` (giá trị lấy từ Settings):
   ```python
   create_async_engine(url, pool_pre_ping=True, connect_args={"server_settings": {
       "statement_timeout": "5000", "idle_in_transaction_session_timeout": "10000"}})  # asyncpg, ms
   # psycopg: connect_args={"options": "-c statement_timeout=5000 -c idle_in_transaction_session_timeout=10000"}
   ```
3. **Index MỌI cột FK:** `vehicle_id: int = Field(foreign_key="vehicle.id", index=True)`. Postgres không tự tạo index cho FK. (`schema-foreign-key-indexes.md`)
4. **Thời gian = `timestamptz`:** `Field(sa_type=sa.DateTime(timezone=True))`; giá trị `datetime.now(tz=UTC)` / `VN_TZ`. **Cấm** `datetime.utcnow()` (naive, deprecated) và cột `timestamp` không tz.
5. **Idempotency bằng ràng buộc DB:** `UNIQUE(idempotency_key)` + `INSERT … ON CONFLICT (idempotency_key) DO NOTHING RETURNING id`; không có dòng trả về → đã ghi trước đó → đọc lại kết quả cũ. **Không** select-rồi-insert (race). (`data-upsert.md`)
   ```python
   stmt = pg_insert(Booking).values(**row).on_conflict_do_nothing(index_elements=["idempotency_key"]).returning(Booking.id)
   ```
6. **Worker/detector nhận việc** bằng một `UPDATE` nguyên tử với `FOR UPDATE SKIP LOCKED` (`UPDATE jobs SET status='processing', worker_id=:w, started_at=now() WHERE id = (SELECT id … WHERE status='pending' ORDER BY created_at LIMIT 1 FOR UPDATE SKIP LOCKED) RETURNING *`). (`lock-skip-locked.md`)
7. **`CREATE INDEX CONCURRENTLY` trong Alembic** phải nằm trong autocommit block (không chạy được trong transaction):
   ```python
   def upgrade() -> None:
       with op.get_context().autocommit_block():
           op.create_index("ix_job_status", "job", ["status"], postgresql_concurrently=True, if_not_exists=True)
   ```
   `downgrade()` tương tự với `op.drop_index(..., postgresql_concurrently=True)`.
8. **Phân trang keyset**, không `OFFSET` lớn: `WHERE (created_at, id) < (:last_ts, :last_id) ORDER BY created_at DESC, id DESC LIMIT :n` + index khớp thứ tự. (`data-pagination.md`)
9. **PgBouncer transaction mode + asyncpg** → `connect_args={"statement_cache_size": 0}` (prepared statement không sống qua connection). Cloud SQL/kết nối trực tiếp thì không cần. (`conn-prepared-statements.md`)
10. **Test dùng Postgres thật** (image `pgvector/pgvector:pg16` qua `make db` / service CI), DB tạm riêng mỗi lần chạy (tạo + xoá, hoặc transaction rollback mỗi test). **Không SQLite** — khác kiểu, khác ON CONFLICT, không có pgvector/SKIP LOCKED.

## Kiểm tra
- [ ] up → down → up sạch · không xoá / đổi tên cột code cũ còn dùng trong cùng PR · test dùng Postgres thật (pgvector) trên DB tạm, không SQLite, không đụng DB dev của người khác
- [ ] Mọi FK có `index=True`; mọi cột thời gian `timestamptz`; không `utcnow()` (`rg -n "utcnow\(" src/ migrations/`)
- [ ] Ghi có idempotency key → có `UNIQUE` + `ON CONFLICT`; không gọi LLM/HTTP/MCP giữa `begin` và `commit`
- [ ] `CONCURRENTLY` nằm trong `autocommit_block()`; engine có `statement_timeout` + `idle_in_transaction_session_timeout`
