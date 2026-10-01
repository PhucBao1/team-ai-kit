# 05 · Luồng xử lý chi tiết — Bốn luồng, từng bước, ai gọi ai

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### Luồng A — Một lượt hội thoại

```text
Khách ──POST /chat──► API
  1  xác thực phiên app (hoặc OTP) → customer_id, quyền theo xe (owner / driver)
  2  nạp session: goal stack, lịch sử rút gọn, memory sở thích (nếu đồng ý)
  3  input guard: đánh dấu nội dung khách là dữ liệu không tin cậy; sàng lọc prompt injection
  4  triage cascade (§15, §18): ý định, mức khẩn, bực? — tuần 1–2: LLM nhỏ; tuần 3: PhoBERT, không chắc → LLM
     dấu hiệu nguy hiểm? ── có ─► SafetyPath (không LLM)
  5  context builder: journey liên quan + bằng chứng tối thiểu + đoạn KB (hybrid retrieval)
  6  agent loop (loop 1): model ↔ tools (chỉ tool đọc tự do; tool ghi cần token)
  7  verification (loop 2): claim_check(reply, evidence) ── lỗi ─► trả lỗi cụ thể cho model sửa (≤2 lần) ─► handoff
  8  nếu có phương án: API ký confirmation_token cho từng option (LLM không thấy token)
  9  stream SSE về client · ghi audit_log · span OTel (tokens, ms, tool)
 10  cập nhật goal stack, promises (nếu agent vừa hứa gì)
```

### Luồng B — Sự kiện hệ thống → tin chủ động

```text
ERP ──parts.reservation.cancelled──► Pub/Sub topic "ops-events"
  1  schema validation (Pub/Sub schema) ── sai ─► dead-letter topic + cảnh báo
  2  dedupe theo event.id (idempotent consumer)
  3  detector L0 (rule) → Candidate | None                 # ~0 token
  4  Contact Arbitration: khách đang chat với NV? đang khiếu nại? quá ngân sách chú ý? giờ yên tĩnh?
        ── chặn ─► ghi "suppressed" + lý do, thử lại theo lịch
  5  Scheduler agent (§14): find_options → 2–3 phương án (range, kho, kỹ năng) → khoá slot 15 phút
  6  Writer ⇄ Critic (§14): tin 5 phần (điều đã xảy ra · phương án · thời hạn · phụ trách · vì sao nhận tin)
  7  claim_check → gửi vào session chat của khách + push notification theo kênh ưa thích
  8  cập nhật journey: bước hiện tại = "chờ khách chọn", promise mới, hẹn giờ nhắc (workflow)
```

### Luồng C — Xác nhận & ghi

```text
Khách bấm [Xác nhận] ──POST /confirm {token}──► API
  1  verify HMAC, exp, customer_id khớp phiên, params_hash khớp option đang khoá
  2  validator: customer_verified · owner_or_can_book · part_matches_vin · technician_certified
               · part_reserved · slot_locked · confirmation_valid       ── lỗi ─► báo khách + NV
  3  Executor (§17) gọi MCP tool ghi (saga nếu nhiều hệ thống) với idempotency_key = hash(option_id, token)
  4  thành công ─► giải phóng slot cũ, cập nhật reservation, promise, journey · ghi audit (append-only)
     thất bại / timeout ─► KHÔNG báo "đã đặt"; đọc lại trạng thái; retry có giới hạn; báo đúng tình trạng
```

### Luồng D — Chuyển người và nhận lại việc

```text
  1  trigger: khách yêu cầu · sentiment ≥ annoyed · 2 lần thất bại · mức 3 · an toàn · khiếu nại
  2  lắp HandoffCard từ goal stack + audit + promises + facts(có nguồn); LLM chỉ viết 1 câu + sentiment
  3  định tuyến theo kỹ năng / xưởng của xe / ca trực; ngoài giờ → 24/7 (khẩn) hoặc ticket có hẹn giờ
  4  NV nhận (accepted_at) → đồng hồ SLA gọi lại; copilot mở cho NV
  5  NV chốt trong console → tool ghi (NV là người xác nhận, có ghi âm / ghi chú)
  6  auto-wrap: AI soạn ghi chú + nhãn lý do liên hệ → NV xác nhận
  7  agent nhận lại journey: gửi xác nhận cho khách, đặt nhắc, tiếp tục loop 5
```
