# PL-A5 · SPEC ONLY — UC5 — Proactive Warranty / Claim Follow-up

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Giữ claim không rơi giữa đại lý và hãng; Agent không quyết định kết quả bảo hành.

**UC5 — spec / scenario only tuần này.** Agent **không** quyết định kết quả bảo hành; việc của hệ thống là giữ claim không rơi giữa đại lý và hãng và nói thật tiến độ. Mọi kịch bản là *Synthetic / illustrative scenario for MVP*.

### Goal

Phát hiện claim bảo hành bị kẹt (chờ bổ sung, SLA gần) và đẩy nó đi **trước khi** khách phải hỏi tiến độ; cập nhật khách đúng sự thật.

### Customer Pain

Xe nằm xưởng chờ bảo hành; hỏi xưởng thì "chờ hãng", hỏi hãng thì "hỏi xưởng". Khách không biết đang chờ bước nào, vì sao, đến khi nào.

### Why Proactive?

Việc kẹt thường nằm ở khoảng giữa hai tổ chức: thông báo trả claim nằm trong portal của hãng mà xưởng không thấy. Mỗi ngày kẹt là một ngày xe nằm xưởng và một lần khách gọi hỏi (failure demand). Trạng thái claim + thời gian đủ để phát hiện **mà không cần khách nói gì**.

### Trigger Signals

| Tín hiệu | Nguồn | Vai trò |
| --- | --- | --- |
| `warranty.claim.state_changed` (ví dụ `returned_for_info`) | Warranty portal giả lập | Tín hiệu chính |
| Đồng hồ SLA / thời gian ở trạng thái | Timer | Tín hiệu thời gian |
| Hoạt động của đại lý trên claim | DMS | Điều kiện loại trừ |
| Bằng chứng đã có (log mã lỗi, odometer, lịch sử bảo dưỡng) | Telematics / DMS | Ngữ cảnh |

### What Happens Before the Customer Contacts Support

Claim bị trả về lúc nào, thiếu gì, ai chịu trách nhiệm bước tiếp — hệ thống đã biết. Bằng chứng tự động đính kèm; nhiệm vụ còn lại giao CVDV có hạn; khách nhận cập nhật tiến độ thật.

### L0 Detector — NO LLM

Detector + **state machine** (trạng thái · thời gian · phụ thuộc):

| Rule | Điều kiện | Kết quả |
| --- | --- | --- |
| C1 | `returned_for_info` > **4 giờ làm việc** và không có hoạt động đại lý | `CandidateFriction(UC5)` |
| C2 | `pending_dealer` ≥ 75% SLA nội bộ | candidate (nhắc) |
| C3 | `pending_manufacturer` ≥ 80% SLA | candidate (escalate nội bộ, không liên hệ hãng thật) |

Cooldown theo `(claim_id, state)`. Ngưỡng là **[POLICY]** khởi đầu. **Không LLM.**

### Context / Evidence Required

Trạng thái claim + lý do trả về (trường có cấu trúc hoặc văn bản tự do) · danh sách bằng chứng đã đính / còn thiếu · bên chịu trách nhiệm bước kế · SLA · điều kiện theo chính sách bảo hành công bố (thời hạn năm / km, loại hình sử dụng, loại trừ) · hạn đã hứa với khách.

### Why an Agent Is Necessary

Nếu lý do trả về là **trường có cấu trúc** ("thiếu log lỗi và ảnh linh kiện") thì rule + mẫu đủ — Agent không cần. Agent cần khi lý do là **văn bản tự do / mơ hồ** hoặc nhiều bên: phải trích *thiếu gì*, *ai có thể cung cấp*, *bước nào làm được tự động*, và viết tin tiến độ trung thực mà không hứa kết quả duyệt.

### Exact Agent Reasoning Task

(1) Lý do trả về nghĩa là cần bổ sung những mục nào? (2) Mục nào có thể đính tự động từ dữ liệu có sẵn, mục nào cần người? (3) Bên nào chịu trách nhiệm từng mục, hạn bao lâu? (4) Cần escalate nội bộ không? (5) Khách cần biết gì, nói thế nào mà không hứa kết quả? Đầu ra: `InterventionProposal` với checklist bằng chứng. **Agent không đánh giá "claim có được duyệt không".**

### Tools the Agent May Call

Mức 0 **[mới, đề xuất]**: `get_claim_status(claim_id)` · `list_claim_evidence(claim_id)` · `get_vehicle_status` · `get_maintenance_history` · `check_warranty` (sơ bộ). Mức 1: `attach_evidence(claim_id, items)` (chỉ bằng chứng **tự động có sẵn**) · `create_task(owner, due)` · `create_handoff`. Không tool ghi quyết định bảo hành.

### Decision / Intervention Options

| Hành động | Mức | Ai |
| --- | --- | --- |
| Nhắc chủ động (khách / CVDV) | 1 | Hệ thống |
| Yêu cầu bổ sung (tạo task CVDV có hạn) | 1 | Hệ thống |
| Đính kèm bằng chứng tự động | 1 | Hệ thống |
| Chuẩn bị escalate nội bộ | 1 | Hệ thống → người |
| Cập nhật tiến độ cho khách | 1 | Hệ thống (theo chính sách liên hệ) |
| **Quyết định bảo hành** | — | **Chỉ hãng / người** |

### Validation Rules

`claim_check` (mọi mốc, mã, số khớp dữ liệu) · tin **không** chứa "được / không được bảo hành" mà chỉ "đủ điều kiện sơ bộ" hoặc trạng thái · chỉ đính bằng chứng tự động đã có (không tạo / sửa bằng chứng) · hạn task là **[POLICY]** · tin không hứa kết quả duyệt.

### Customer Confirmation Requirement

Cập nhật tiến độ: không cần xác nhận (theo arbitration). Nếu cần khách cung cấp thêm (ví dụ ảnh): yêu cầu rõ, khách chủ động làm; **không** có hành động ghi ảnh hưởng khách cần token trong UC này. Đặt lịch bổ sung chứng từ nếu cần → UC3 (xác nhận mức 2).

### Executor / Write Actions

Mức 1 qua Executor tất định: `attach_evidence`, `create_task`, `create_handoff`, cập nhật journey / promise. Audit append-only. **Không** ghi vào quyết định bảo hành.

### Verification Loop

| Kiểm tra | Bằng chứng | Kết quả |
| --- | --- | --- |
| Bằng chứng đã nhận | Task hoàn tất; mục `received` | `evidence_ok` |
| Claim tiến triển | Trạng thái `returned_for_info → resubmitted` trong ≤ 1 ngày | `progressed` |
| Khách được báo | Tin đã gửi + mở | `informed` |
| Không tiến triển đến SLA | Còn kẹt | `failed` → escalate nội bộ / handoff |

### Failure / Retry / Handoff

Task quá hạn → nhắc 1 lần rồi escalate trưởng xưởng · claim không tiến triển sau escalate → handoff quản lý dịch vụ + báo khách tình trạng thật · lý do không trích được → handoff · không bao giờ tự đổi kết quả claim.

### Customer UX

Tin: *claim đang ở bước nào · đang chờ ai · điều gì sẽ xảy ra · khi nào sẽ cập nhật tiếp · vì sao nhận tin* (không hứa kết quả). "Việc của tôi" có bước claim.

### CSKH / Staff UX

Console task cho CVDV: việc còn lại (ví dụ chụp ảnh linh kiện) + hạn + bằng chứng đã đính tự động. Handoff card khi escalate. Báo cáo pattern: nhiều claim bị trả vì thiếu log → đính log mặc định khi lập claim.

### Synthetic Data Required

*Synthetic / illustrative scenario for MVP.* Claim **WC-2231** (xe VF 8 "anh Khoa") trả về 2 ngày trước với lý do **văn bản tự do** "Thiếu bằng chứng liên quan tình trạng sử dụng và hư hỏng" · portal giả lập có trạng thái + lý do · log mã lỗi / odometer / lịch sử bảo dưỡng trong seed · một claim lý do có cấu trúc (đường không Agent) · SLA timer giả lập.

### Concrete Demo Scenario

*Synthetic / illustrative scenario for MVP.* Anh Khoa chưa hỏi tiến độ.

| Bước | Thời điểm | Chuyện gì xảy ra | Đầu vào → Đầu ra | LLM? |
| --- | --- | --- | --- | --- |
| **T0** | Thứ Ba 09:00 | Sweep thấy claim WC-2231 ở `returned_for_info` 2 ngày; không có hoạt động đại lý | state + timer | Không |
| **T+1 s** Detector | 09:00 | C1: > 4 giờ làm việc ✓ · không hoạt động ✓ · cooldown mới ✓ | → `CandidateFriction(UC5)` | **Không** |
| Arbitration | 09:00 | Không đang chat; 0/3 tin tuần này | `allowed` | Không |
| Ngữ cảnh | 09:01 | `get_claim_status`, `list_claim_evidence`, telematics, bảo dưỡng | `ContextBundle` | Không |
| Decision gate | 09:01 | Lý do là **văn bản tự do** → rule không phân loại được | → `escalate_to_L1/L2` | L1 (~400 token) trích mục thiếu |
| **Agent được gọi** | 09:01 | Mục thiếu: log lỗi (**tự động có**), odometer (**tự động có**), ảnh hư hỏng (**cần CVDV**). Chọn: đính tự động + task CVDV hạn 16:00 + tin tiến độ | `InterventionProposal` | L2 (~1.500 token) |
| Validator | 09:02 | Bằng chứng đính đều có nguồn ✓ · tin không hứa kết quả ✓ | `approved` | Không |
| Executor | 09:02 | `attach_evidence` (log + odometer + lịch sử) · `create_task(CVDV Hải, 16:00)` | mức 1 | Không |
| Tin khách | 09:05 | Tiến độ thật; không hứa kết quả duyệt | → app | Mẫu tin |
| **Verify** | 15:20 | Ảnh đã đính; claim `resubmitted` | `progressed` | Không |
| Resolved / handoff | hôm sau | Hãng duyệt (do hãng, ngoài hệ thống); xe sửa xong → `resolved`. Nếu không tiến triển → escalate / handoff | — | — |

### Cost Tier

**TB.** State machine + mẫu tin xử lý ca có cấu trúc (0 token). Agent / L1 chỉ khi lý do mơ hồ.

### Success Criteria

Mục tiêu thiết kế — chưa đo: thời gian claim nằm ở `returned_for_info` giảm so với đối chứng giả lập · mọi claim kẹt có **owner đại lý trong 4 giờ làm việc** · **0** tin hứa kết quả duyệt · **0** thay đổi quyết định bảo hành bởi hệ thống · số ngày xe chờ giảm trên kịch bản.

### Out of Scope / Safety Boundaries

Agent không quyết định / dự đoán kết quả bảo hành · không sửa hay tạo bằng chứng · không liên hệ hãng thật · không tích hợp warranty portal thật · điều kiện bảo hành theo chính sách công bố, kết luận do xưởng / hãng.

### A/B/C/D Ownership

Tuần này **chỉ tài liệu**. Backlog:

|  | Việc tương lai cho UC5 |
| --- | --- |
| **A** | Prompt trích lý do trả về → checklist bằng chứng + tin tiến độ trung thực |
| **B** | Claim state machine + portal giả lập + SLA timer · rule C1–C3 · seed WC-2231 · kịch bản YAML khung |
| **C** | Tiến độ claim trong "Việc của tôi" · console task CVDV |
| **D** | Escalation + SLA clock · verifier · eval "0 hứa kết quả" |
