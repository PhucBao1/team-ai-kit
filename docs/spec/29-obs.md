# 29 · Observability & SLO — Một trace cho một việc, kể cả khi việc kéo dài nhiều ngày

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
# Span theo OpenTelemetry GenAI semantic conventions (+ thuộc tính riêng)
span "chat.turn"                 attrs: journey.id, customer.token, channel
 ├─ span "gen_ai.chat"           attrs: gen_ai.request.model, gen_ai.usage.input_tokens,
 │                                      gen_ai.usage.output_tokens, gen_ai.operation.name
 ├─ span "execute_tool find_options"   attrs: tool.name, tool.level=0, db.ms
 ├─ span "verify.claim_check"    attrs: violations=0
 └─ span "execute_tool book_appointment" attrs: tool.level=2, validator.failed=[], idempotency_key
# Việc nhiều ngày: mỗi bước workflow là trace riêng, liên kết bằng span link + journey.id
```

| SLO | Mục tiêu (đề xuất) | Cảnh báo khi |
| --- | --- | --- |
| Hội thoại: thời gian đến token đầu tiên | p95 < 2 giây | p95 > 3 giây trong 10 phút |
| Hội thoại: hoàn tất lượt | p95 < 8 giây | p95 > 12 giây |
| Luồng an toàn (không LLM) | Sẵn sàng ≥ 99,95%; < 60 giây từ sự kiện đến tin | Bất kỳ lỗi nào |
| Sự kiện → tin chủ động (UC1) | p95 < 5 phút | Hàng đợi tồn > 15 phút |
| Grounding violation | 0 | Bất kỳ vi phạm nào lọt qua |
| Ghi không có xác nhận | 0 | Bất kỳ trường hợp nào (sự cố mức cao) |
| Chi phí / việc (ACRC) | Theo ngân sách | Tăng > 30% tuần so với tuần |

**Drift của agent** (thay cho drift model truyền thống): eval online trên mẫu trace hằng ngày; phân phối sự kiện (ví dụ một mã lỗi tăng vọt sau cập nhật phần mềm); precision detector theo tuần. Dashboard: Cloud Monitoring cho hạ tầng, Langfuse cho agent, Looker cho metric CX.
