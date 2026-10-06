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

### Luồng B — Tín hiệu hệ thống → candidate → can thiệp → xác minh

Luồng chung cho UC1–UC6; chỉ phần detector, tool đọc và hành động khác nhau theo use case (proposal PL-A). Khách **không** cần làm gì để luồng này bắt đầu. Ví dụ UC1: telematics gửi mã lỗi WARNING lần thứ 3 trong 14 ngày, chưa có lịch / ticket.

```text
Telematics ──vehicle.dtc.raised──► Pub/Sub topic "ops-events"       # UC2/4/5: CSMS · billing · claim — cùng khung
  1  schema validation (Pub/Sub schema) ── sai ─► dead-letter topic + cảnh báo
  2  dedupe theo event.id (idempotent consumer)
  3  detector L0 (rule · ngưỡng · cửa sổ · dedupe · không có case) → CandidateFriction | None   # 0 token, KHÔNG LLM
  4  Contact Arbitration (code): khách đang chat với NV? đang khiếu nại? quá ngân sách chú ý? giờ yên tĩnh?
        ── chặn ─► ghi "suppressed" + lý do, thử lại theo lịch
  5  context builder (code): tool ĐỌC gom bằng chứng tối thiểu → ContextBundle (mỗi fact có nguồn)
  6  decision gate:
        hành động tất định đủ ────────────► mẫu tin + action theo rule                  # KHÔNG LLM
        phân loại là đủ ──────────────────► L1 triage (model nhỏ)
        mơ hồ · nhiều nguồn · nhiều bước ─► L2 agent (§13)
  7  agent điều tra → suy luận → InterventionProposal (chỉ tool đọc; gọi Scheduler (§14) như một tool khi UC3 cần lập phương án)
  8  validator: claim_check · cụm từ cấm (chẩn đoán, kết luận bảo hành) · quy tắc · arbitration kiểm lại ngay trước khi gửi
  9  Writer ⇄ Critic (§14): tin 5 phần (điều đã xảy ra · phương án · thời hạn · phụ trách · vì sao nhận tin)
 10  gửi vào session chat của khách + push notification theo kênh ưa thích
 11  cập nhật journey: bước hiện tại = "chờ khách chọn", promise mới, hẹn giờ nhắc (workflow)
 12  theo kết quả (loop 5): repair_order.closed (lưu km lúc sửa) ─► việc "đã sửa xong, đang theo dõi"
     tới hạn đánh giá: assess_post_repair (heartbeat đúng xe sau sửa · km tăng ≥ 50 · không khoảng trống > 72h · không mã cũ) — ngưỡng GIẢ LẬP
        đủ dữ liệu ─► "trong dữ liệu nhận được sau sửa, chưa ghi nhận lại mã X" + hỏi khách còn triệu chứng (KHÔNG gọi là đã xác minh / đã đóng)
        thiếu dữ liệu ─► KHÔNG đóng: tiếp tục theo dõi +7 ngày, khách thấy "chưa đủ dữ liệu để đánh giá sau sửa"            # A2.27
 13  mã đã sửa báo lại khi việc còn đang theo dõi (kể cả quá 14 ngày vì thiếu dữ liệu) ─► "mở lại" đúng journey (UC6), tối đa 2 chu kỳ ─► handoff
```

Nhánh lập lại của UC3: parts.reservation.cancelled · parts.eta.changed làm một lịch *đã xác nhận* mất điều kiện (còn < 72 giờ) cũng đi vào bước 3 như một candidate, rồi UC3 lập lại 2–3 phương án và xin khách xác nhận.

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

### Luồng D — Chuyển người, người nhận và quá hạn (viết lại 06/10)

```text
  1  trigger: khách yêu cầu · sentiment ≥ annoyed · 2 lần thất bại · mức 3 · an toàn · khiếu nại · LLM lỗi giữa lượt
  2  lắp HandoffCard từ goal stack + audit + promises + facts (có nguồn); LLM chỉ viết 1 câu + sentiment
  3  định tuyến theo xưởng có lịch của xe / tổng đài; hạn gọi lại từ bảng SLA (15' · an toàn 5' · ngoài giờ 09:30 hôm sau)
  4  ghi handoff qua executor ── lỗi ─► KHÔNG nói "đã chuyển"; đưa tổng đài 1900 23 23 89; không hứa hạn          # A2.22
  5  khách thấy "đã chuyển tới {hàng chờ}, chưa có người nhận · hẹn liên hệ trước HH:MM"                          # A2.25
  6  NV bấm Nhận ca (status accepted, assignee = tên NV) ─► khách thấy "{tên} đang xử lý, cập nhật trước HH:MM"
  7  mỗi lần tua đồng hồ: ca open quá deadline_at ─► chuyển assignee sang hàng chờ "Trưởng ca CSKH" (vẫn open) ─► đọc lại kiểm
        thành công ─► tin hệ thống (nơi chuyển trước/sau + giờ) + báo khách "đã chuyển tới hàng chờ trưởng ca, hiện chưa có người nhận"
        thất bại   ─► báo "vẫn chưa có người nhận", không đánh dấu, lần sau thử lại · KHÔNG hứa giờ mới                  # A2.26
     MVP chỉ giám sát "quá hạn chưa nhận"; "đã nhận nhưng không tiến triển" là roadmap
  8  NV chốt trong console → tool ghi (NV là người xác nhận); auto-wrap ghi chú → NV xác nhận
  9  NV Đóng ca ─► khách thấy "đã kết thúc trao đổi với nhân viên" (không có nghĩa đã giải quyết); agent nhận lại việc, tiếp tục loop 5
```

**Vòng đời việc của khách** (`CustomerCase.status`, ADR 011 — A2.23, A2.25, A2.27; gắn theo `journey_id`, không theo "việc mới nhất của VIN"):
`waiting` (chờ khách chọn) → `done` (đã xác nhận — thao tác thành công) → `service_done` (đã sửa xong) → `monitored_clear` (chưa ghi nhận lại mã trong dữ liệu đủ) /
`insufficient_data` (chưa đủ dữ liệu, vẫn theo dõi) / `reopened` (mã báo lại) / `symptom_reported` (khách báo còn dấu hiệu bất thường — mở lại cả journey, dừng đánh giá tự động). Nhánh người: `handoff_sent` (đã chuyển, chưa ai nhận) → `handed_off` (đã có người nhận)
→ `handoff_closed` (đã kết thúc trao đổi). Không có `verified`: dữ liệu xe không chứng minh khách hết triệu chứng.
