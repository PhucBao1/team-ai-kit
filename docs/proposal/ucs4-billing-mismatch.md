# PL-A4 · SPEC ONLY · LLM-light — UC4 — Billing / Charging Mismatch Prevention

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Cố ý LLM-light: không phải event proactive nào cũng cần Agent. Tiền luôn do người duyệt.

**UC4 — spec / scenario only tuần này; cố ý LLM-light.** UC này tồn tại để chứng minh: **không phải event proactive nào cũng cần LLM Agent.** Liên quan tiền → Agent không bao giờ quyết định hoàn tiền; người duyệt. Mọi kịch bản là *Synthetic / illustrative scenario for MVP*.

### Goal

Phát hiện và ngăn friction billing sạc (tính phí sai quyền ưu đãi, trừ trùng) **trước khi khách phải khiếu nại**, bằng so khớp tất định; chỉ dùng LLM khi bằng chứng mâu thuẫn.

### Customer Pain

Xe thuộc diện miễn phí sạc mà vẫn bị trừ tiền, hoặc bị trừ hai lần cho một phiên sạc. Khách chỉ phát hiện khi xem hoá đơn, rồi phải khiếu nại và giải thích lại. Với tiền, mất niềm tin nhanh nhất.

### Why Proactive?

- Mismatch nằm sẵn ở dữ liệu `session ↔ billing ↔ entitlement`; hệ thống thấy ngay khi phiên sạc kết thúc.
- Báo trước ("đang xử lý, có hạn phản hồi") và sửa trước giảm khiếu nại và đối soát thủ công.
- Khoảng cách phát hiện càng ngắn thì phạm vi sửa càng nhỏ (ít phiên bị tính sai).

### Trigger Signals

| Tín hiệu | Nguồn | Vai trò |
| --- | --- | --- |
| `charging.session.completed` + `billing.charge.created` (session_id, amount, tariff, account_id) | CSMS / Billing | Tín hiệu chính |
| Quyền ưu đãi theo hồ sơ xe + `usage_type` + chính sách có phiên bản **[FACT: miễn phí sạc cá nhân đến 30/6/2027 theo công bố; xe kinh doanh có chính sách riêng]** | Hồ sơ xe / KB | So khớp |
| Lịch sử sang tên / liên kết tài khoản sạc | Hồ sơ xe & chủ xe | Ngữ cảnh |

### What Happens Before the Customer Contacts Support

Ngay sau phiên sạc, hệ thống so khớp phí với quyền ưu đãi và kiểm trùng. Phần lớn ca được xử lý hoặc chuẩn bị xong (sửa trùng, hồ sơ điều chỉnh chờ duyệt) trước khi khách mở hoá đơn.

### L0 Detector — NO LLM

L0 xử lý **phần lớn** ca bằng so khớp và state machine:

| Rule | Điều kiện | Kết quả |
| --- | --- | --- |
| R1 Trừ trùng | ≥ 2 giao dịch cùng `session_id` | `CandidateFriction(UC4, kind=duplicate)` |
| R2 Phí khi được miễn | Phí > 0 **và** xe `usage_type = personal` **và** chính sách miễn phí hiệu lực tại ngày sạc **và** tài khoản liên kết đúng chủ xe hiện tại | `kind=entitlement_mismatch_clean` |
| R3 Dữ liệu mâu thuẫn | Phí > 0 với xe được miễn nhưng liên kết tài khoản ≠ chủ hiện tại / sang tên gần đây / `usage_type` mơ hồ | `kind=entitlement_mismatch_conflict` |

Cooldown theo `(vin, session_id)`. Arbitration giữ nguyên (không spam). **Không LLM.**

### Context / Evidence Required

Giao dịch billing của phiên · hồ sơ xe (`usage_type`, chủ xe, ngày sang tên) · liên kết tài khoản sạc · chính sách miễn phí đúng phiên bản và ngày hiệu lực (KB) · lịch sử các phiên bị tính gần đây.

### Why an Agent Is Necessary

Phần lớn ca **không** cần: R1 và R2 là so khớp tất định và chính sách đã rõ. Agent (tuỳ chọn) chỉ cần khi **R3**: nhiều nguồn mâu thuẫn (sang tên, liên kết cũ, loại hình sử dụng) và cần quyết định *can thiệp nào* (sửa liên kết, hỏi khách xác minh loại hình, chuyển đối soát) cùng cách diễn đạt phù hợp. Ngay cả khi đó, Agent chỉ **chuẩn bị hồ sơ**, không quyết định.

### Exact Agent Reasoning Task

Chỉ cho R3. Cho `ContextBundle`: (1) bằng chứng nào mâu thuẫn và nguồn nào đáng tin hơn theo chính sách? (2) khả năng cao là liên kết sai, loại hình sử dụng, hay dữ liệu thiếu? (3) cần hỏi khách xác minh điều gì (loại hình sử dụng)? (4) hồ sơ cho đối soát cần có gì? Đầu ra: `InterventionProposal` + tóm tắt có nguồn cho đối soát. **Không** kết luận hoàn tiền; **không** hứa kết quả.

### Tools the Agent May Call

Mức 0 **[mới, đề xuất]**: `get_billing_records(session_id)` · `get_entitlement(vin, date)` · `get_ownership_history(vin)` · `get_charging_history`. Mức 1: `prepare_adjustment` (tạo hồ sơ điều chỉnh ở trạng thái *chờ duyệt*) · `create_handoff`. Agent **không** có tool hoàn tiền hay sửa liên kết.

### Decision / Intervention Options

| Ca | Hành động | Ai quyết |
| --- | --- | --- |
| R1 dưới ngưỡng | **Tự sửa tất định** (hoàn giao dịch trùng) khi policy cho phép | Policy (không LLM) |
| R2 sạch | **Chuẩn bị điều chỉnh** → đối soát duyệt (mức 3); mẫu tin báo đang xử lý | Người |
| R3 | Agent chuẩn bị hồ sơ + tin; hỏi khách xác minh loại hình nếu cần; đối soát duyệt | Người |
| Số tiền ≥ ngưỡng hoặc xe kinh doanh | Chuyển người ngay | Người |

### Validation Rules

Quyền ưu đãi phải theo **chính sách có phiên bản và ngày hiệu lực** (KB) · tự sửa chỉ khi **cùng `session_id`** và số tiền **dưới ngưỡng [POLICY — giá trị do đối soát chốt]** · `claim_check` cho mọi số tiền / ngày trong tin · không hứa hoàn trước khi xác minh loại hình sử dụng · Executor idempotent theo `(session_id, adjustment_type)`.

### Customer Confirmation Requirement

Báo "đang xử lý, có hạn phản hồi": không cần xác nhận. Thay đổi liên kết tài khoản của khách: **cần khách xác nhận** (mức 2). Hoàn tiền: **chỉ người duyệt (mức 3)** — khách không "xác nhận" thay người duyệt, nhưng được thông báo.

### Executor / Write Actions

Tự sửa R1 (ledger đảo giao dịch, idempotent, audit). Tạo `adjustment_request` (chờ duyệt). Sau khi đối soát duyệt: hoàn tiền + sửa liên kết qua Executor. Mọi ghi append-only vào `audit_log`.

### Verification Loop

| Kiểm tra | Bằng chứng | Kết quả |
| --- | --- | --- |
| Số tiền hoàn đúng hoá đơn | Ledger sau điều chỉnh khớp | `resolved_amount` |
| Liên kết xe ↔ tài khoản đúng | Hồ sơ sau sửa | `resolved_link` |
| Phiên sạc **sau đó** tính đúng | Phiên kế tiếp có phí = 0 (hoặc đúng biểu giá) | `resolved` |
| Không hoàn tiền sau hạn | Hạn phản hồi đã hứa với khách | SLA đạt / vi phạm → escalate |

### Failure / Retry / Handoff

Đối soát chưa duyệt đến hạn → nhắc nội bộ + báo khách tình trạng thật · phiên sau vẫn tính sai → `failed` → escalate người (không retry tự động nhiều lần) · mâu thuẫn không giải quyết được → handoff.

### Customer UX

Tin: *phiên sạc nào, bị tính gì, dự kiến sẽ có phản hồi trước thời điểm cụ thể, anh không cần thao tác thêm* — không hứa kết quả. Vì sao nhận tin. Màn hình "Việc của tôi" có bước Xác minh phiên sạc tiếp theo.

### CSKH / Staff UX

Màn hình duyệt cho đối soát: hồ sơ điều chỉnh với bằng chứng (giao dịch, hồ sơ, chính sách + phiên bản), nút Duyệt / Từ chối / Yêu cầu thêm, lý do bắt buộc. Báo cáo root cause (ví dụ sang tên không phát event sang billing).

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.* Xe **VF 5 "anh Nam"**: cá nhân, sang tên 05/9, tài khoản sạc vẫn gắn chủ cũ · 2 phiên sạc 12–13/9 bị tính phí (số tiền giả lập) · một cặp giao dịch trùng `session_id` (R1) · một xe kinh doanh vận tải (chính sách riêng) · bảng chính sách miễn phí có phiên bản + ngày hiệu lực.

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Hai nhánh để thấy LLM-light.

**Nhánh A — trừ trùng (KHÔNG Agent):**

| Bước | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- |
| T0 | `billing.charge.created` hai lần cùng `session_id=S-8841` | 2 event | Không |
| T+1 s | R1 khớp; số tiền dưới ngưỡng | → candidate `duplicate` | **Không** |
| T+2 s | Arbitration qua | `allowed` | Không |
| T+3 s | **Không Agent.** Policy cho tự sửa → Executor đảo giao dịch trùng (idempotent) | ledger đã sửa | Không |
| T+4 s | Mẫu tin: "phiên S-8841 bị trừ trùng, đã hoàn" | → app | Mẫu tin |
| Verify | Ledger khớp 1 giao dịch; phiên sau tính đúng | `resolved` | Không |

**Nhánh B — mâu thuẫn dữ liệu (Agent tuỳ chọn):**

| Bước | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- |
| T0 | Phiên sạc 12/9 có phí; xe VF 5 cá nhân | `billing.charge.created` | Không |
| T+1 s | R3: xe sang tên 05/9, tài khoản sạc vẫn gắn chủ cũ → mâu thuẫn | candidate `entitlement_mismatch_conflict` | **Không** |
| T+2 s | Arbitration qua; ngữ cảnh gom (hồ sơ, sang tên, chính sách phiên bản hiện hành) | `ContextBundle` | Không |
| T+3 s | **Agent được gọi** (bằng chứng mâu thuẫn): khả năng cao là *liên kết sai*; chuẩn bị đề xuất hoàn + sửa liên kết; tóm tắt cho đối soát | `InterventionProposal` + hồ sơ | L2 (~1.800 token) |
| T+4 s | Validator: số tiền / phiên bản chính sách khớp; mức 3 → chỉ người duyệt | `needs_human` | Không |
| 08:32 | Tin: đang xử lý, phản hồi trước 17:00 ngày 15/9; không hứa kết quả | → app | Mẫu tin |
| 10:15 | Đối soát duyệt hoàn + sửa liên kết | Executor | Không |
| 16/9 | Verify: phiên mới tính đúng ưu đãi; hoàn tiền đã về | `resolved` | Không |

### Cost Tier

**THẤP.** Đa số ca 0 token (R1, R2). LLM chỉ ở R3, hiếm. Chính cấu trúc này là ví dụ của nguyên tắc *"LLM là tầng leo thang"*.

### Success Criteria

Mục tiêu thiết kế — chưa đo: **0** hoàn tiền sai (tiền không bao giờ do LLM quyết) · **0** ghi mức 3 không có người duyệt · ≥ 80% candidate xử lý không qua LLM trên kịch bản giả lập **[ASSUMPTION — ngưỡng để chỉnh]** · phiên sau đó tính đúng ở 100% ca đã sửa · mọi tin có số tiền khớp ledger (`claim_check`).

### Out of Scope / Safety Boundaries

Agent không hoàn tiền, không sửa liên kết, không quyết định ưu đãi · không hứa hoàn trước khi xác minh · xe kinh doanh vận tải theo chính sách riêng → người · không dữ liệu thanh toán / khách thật · không tích hợp billing V-Green thật · mọi ngưỡng tiền là **[POLICY]** do đối soát chốt.

### A/B/C/D Ownership

Tuần này **chỉ tài liệu**. Backlog implement sau khi spec được chốt:

|  | Việc tương lai cho UC4 |
| --- | --- |
| **A** | (Tuỳ chọn) prompt tổng hợp bằng chứng mâu thuẫn + tóm tắt cho đối soát |
| **B** | Billing + entitlement giả lập có phiên bản · rule R1 / R2 / R3 · event `ownership.transferred` · seed anh Nam · kịch bản YAML khung |
| **C** | Thông báo "đang xử lý" · màn hình duyệt cho đối soát |
| **D** | Ngưỡng tự sửa · duyệt mức 3 · ledger idempotent · eval "0 tiền sai" |
