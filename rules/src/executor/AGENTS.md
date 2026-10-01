# src/executor/ — nơi DUY NHẤT được ghi (owner: D) · spec `../team-ai-kit/docs/spec/17-core.md`

- Mỗi thao tác ghi: kiểm confirmation token (HMAC, hạn, đúng tham số) → validator → idempotency key → gọi `src.tools`.
- Nhiều bước → saga (bước bù) + transactional outbox; không gửi tin ngoài transaction. Mỗi lần ghi → 1 dòng `audit_log`.
- Không gọi LLM. Không nhận tham số trực tiếp từ text của khách — chỉ từ `proposal` đã xác nhận.
- Test trong `tests/test_executor/`: nhánh lỗi, retry, gọi trùng cùng token.
