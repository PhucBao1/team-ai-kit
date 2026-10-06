# PL-A · Proactive AI Customer Care & sáu use case — Một engine chăm sóc chủ động, sáu use case

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

AI không chờ khách đặt lịch, mở ticket hay khiếu nại. Hệ thống quan sát tín hiệu đủ điều kiện, phát hiện friction đang hình thành bằng cơ chế rẻ trước, chỉ gọi LLM khi cần suy luận, rồi hành động có kiểm soát và **xác minh** kết quả. Appointment chỉ là một hành động xuôi dòng.

### North star — Proactive AI Customer Care

**Định nghĩa chuẩn (EN):** The system proactively detects emerging customer friction from eligible system signals, investigates the issue using relevant context and tools, selects the least-cost safe intervention that is appropriate for the case, executes controlled actions when authorized, and verifies whether the customer problem was actually resolved — before the customer needs to initiate support.

**Bản tiếng Việt dùng trong tài liệu:** AI chủ động phát hiện, điều tra và xử lý những customer friction đang hình thành trước khi khách hàng phải chủ động yêu cầu hỗ trợ.

**Câu ngắn cho pitch:** AI không chờ khách yêu cầu. Hệ thống phát hiện, điều tra và xử lý friction đủ điều kiện trước khi khách phải mở case.

**Không nói / không claim** (mọi tài liệu của đội phải tuân thủ):

- Không nói AI giải quyết mọi vấn đề, luôn biết khách cần gì, tự chẩn đoán xe, thay thế CSKH, tự đặt lịch cho mọi vấn đề, hay chạy LLM liên tục trên mọi event của xe / khách.
- Không claim đã triển khai production, có dữ liệu khách thật, tích hợp hệ thống nội bộ VinFast / V-Green, hay đã đo được tác động kinh doanh. Dữ liệu là **giả lập**; số đo là **mục tiêu thiết kế** cho đến khi eval chạy.
- Mọi kịch bản trong các mục UC1–UC6 là *Synthetic / illustrative scenario for MVP*.

**Nhãn bằng chứng** dùng trong các mục UC: **[FACT]** có nguồn công khai hoặc có trong repo · **[ASSUMPTION]** giả định chờ kiểm chứng · **[SYNTHETIC]** dữ liệu / kịch bản giả lập của MVP · **[POLICY]** luật do đội quyết định (không phải chính sách thật của hãng).

### Appointment không phải điểm bắt đầu

Câu chuyện cũ — *khách đặt lịch → có gì đó hỏng → AI cứu lịch* — **không còn là câu chuyện chính**. Câu chuyện mới:

```text
Tín hiệu hệ thống → friction đang hình thành → đối chiếu ngữ cảnh
   → (chỉ khi cần) suy luận chọn lọc → can thiệp → xác minh → xong / chuyển người
```

Đặt lịch chỉ là **một hành động xuôi dòng** (UC3), do khách xác nhận, khi Agent kết luận cần can thiệp tại xưởng. Khi một lịch đã đặt bị hỏng (ví dụ kho điều linh kiện đi), đó là **nhánh lập lại phương án của UC3**, không phải điểm khởi đầu của sản phẩm.

### Kiến trúc chung của mọi use case

```text
EVENT / SIGNAL                       (xe, trạm sạc, billing, claim, DMS, ERP)
      ↓
L0 DETERMINISTIC DETECTOR            rule · ngưỡng · cửa sổ thời gian · dedupe        — KHÔNG LLM
      ↓
CANDIDATE FRICTION                   CandidateFriction
      ↓
CONTACT / POLICY ARBITRATION         đang chat với NV? khiếu nại? ngân sách chú ý? giờ yên tĩnh? — KHÔNG LLM
      ↓
CONTEXT CORRELATION                  gom bằng chứng tối thiểu qua tool đọc            — KHÔNG LLM
      ↓
DECISION GATE
  ├─ hành động tất định đủ  ──────►  mẫu tin + action theo rule                       — KHÔNG LLM
  └─ mơ hồ / nhiều nguồn / nhiều bước
        ├─ L1 triage (model nhỏ) nếu chỉ cần phân loại
        └─ L2 Agent (model suy luận) nếu cần chọn can thiệp
      ↓
AGENT INVESTIGATES / REASONS         gọi tool ĐỌC → InterventionProposal
      ↓
VALIDATOR / POLICY GATE              claim_check · quy tắc · quyền · ngưỡng           — KHÔNG LLM
      ↓
EXECUTOR (chỉ khi là hành động ghi)  confirmation token · idempotency · saga          — KHÔNG LLM
      ↓
VERIFY RESULT                        bằng bằng chứng hệ thống, không bằng "đã gửi"
      ↓
RESOLVED?
  ├─ CÓ    → đóng / cập nhật journey
  └─ CHƯA  → retry có giới hạn → chuyển người (HandoffCard)
```

**Ba luật bất biến**

1. **Proactive không có nghĩa là LLM chạy trên mọi event.** Mọi event đi qua lọc tất định rẻ trước; chỉ candidate có ý nghĩa mới có thể tới suy luận.
2. **LLM là tầng leo thang (escalation layer), không phải tầng xử lý event.**
3. **Hệ thống chỉ tiêu "trí thông minh" ở nơi nó tạo thêm giá trị.** Thứ tự ưu tiên: rule tất định → tương quan / state machine → model nhỏ (phân loại) → model suy luận (chọn can thiệp) → người (khi rủi ro hoặc bất định vượt chính sách).

**Ranh giới không được phá** (khớp `rules/AGENTS.md`): Detector ≠ Agent · Agent ≠ Executor (Agent chỉ đề xuất, mọi ghi đi qua Executor) · Core ≠ LLM (`src/core/` tất định) · Appointment ≠ Trigger.

**Mức hành động** (giữ nguyên §11): mức 0 chỉ đọc · mức 1 ghi nội bộ không ảnh hưởng khách (gửi tin chủ động theo chính sách liên hệ, tạo handoff, đính kèm bằng chứng) · mức 2 ảnh hưởng khách → **bắt buộc** confirmation token khách tạo · mức 3 liên quan tiền / quyết định cuối → **chỉ người duyệt**.

### Các đối tượng dùng chung

Đây là mô tả cấp tài liệu để A/B/C/D thống nhất tên gọi. **Chưa phải contract** — chưa nằm trong `contracts/*.yaml` hay schema API; khi implement, B + D chốt qua PR riêng + ADR (task này không đổi contract).

| Đối tượng | Trường chính | Ai tạo → ai dùng |
| --- | --- | --- |
| `CandidateFriction` | candidate_id · uc_type (UC1…UC6) · vin · customer_id · signals[] (event_id, type, time) · window · count · dedupe_key · priority (normal / high / urgent) · detector_rule_id + version · created_at · synthetic | Detector (B) → Arbitration (D) → Context builder |
| `ContextBundle` | candidate · vehicle · recent_events · service_history · journey · warranty_prelim (nếu cần) · capability / parts / slots (nếu cần) · kb_refs[] — **mỗi fact có nguồn** | Context builder (B) → Agent (A) |
| `InterventionProposal` | candidate_id · assessment {meaningful, urgency, confidence} · evidence_refs[] · intervention_type · options[] (`Option` §13) · needs_confirmation · needs_human · reason · message_draft | Agent (A) → Validator (D) |
| `VerificationResult` | candidate_id · check · evidence_ref · outcome (resolved / pending / failed / recurred) · next_action | Verifier (D, nguồn sự kiện từ B) → Journey |

> **Ghi chú 06/10 ([business discovery lại](../research/2026-10-06-business-discovery.md)):** UC4 (hoá đơn) và UC6 (tái phát) **không tìm thấy bằng chứng là pain
> của khách VinFast** → chỉ giữ ở mức spec, không đưa vào phần "vấn đề" khi pitch. Phát hiện lỗi rồi báo khách (UC1) VinFast đã công bố từ 2021 → UC1 là cửa vào,
> khác biệt nằm ở phần sau khi báo (`plan/PLAN.md` mục "Bổ sung 06/10").

`intervention_type` thuộc tập: `explain` (giải thích chủ động) · `self_help` (hướng dẫn từ KB) · `prepare_service_option` · `ask_confirmation` · `service_action` (đi qua UC3) · `handoff` · `no_action` (đóng / hoãn, ghi lý do).

### Sáu use case một nhìn

| UC | Sự kiện bắt đầu (KHÔNG phải khách) | L0 phát hiện (không LLM) | LLM khi nào | Hành động chính | Xác minh bằng | MVP | Cost |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **UC1** Preemptive Service Friction Rescue *(flagship)* | Mã lỗi WARNING lặp lại, chưa có case / lịch | Ngưỡng + cửa sổ + dedupe + không có case + arbitration | Ca nhiều nguồn, mơ hồ (L1 tuỳ chọn, L2 chỉ khi cần) | Giải thích, self-help, chuẩn bị phương án, hỏi xác nhận, handoff | Telematics N ngày không lặp lại | **Full** | CAO — chỉ ca ứng viên thật |
| **UC2** Charging Friction Prevention | Phiên sạc thất bại lặp lại | Số lần thất bại + tương quan trạm + cooldown | Khi trạm khoẻ nhưng nguyên nhân chưa rõ | Gợi ý thử lại, trạm khác, đề xuất dịch vụ, handoff khẩn | Phiên sạc kế tiếp thành công | **Demo-ready** | TB / CAO khi mơ hồ |
| **UC3** Service Readiness / Intervention Orchestration | Can thiệp xưởng đã được khách chấp nhận (từ UC1/UC2/UC6) hoặc lịch đã đặt bị hỏng điều kiện | Điều kiện đầu vào + kiểm tra ràng buộc cơ bản | Luôn (suy luận đa ràng buộc) nhưng chỉ sau khi can thiệp đã được chứng minh cần | 2–3 phương án khả thi → xác nhận → đặt | Đọc lại lịch + linh kiện; telematics sau sửa | **Demo-ready** | CAO nhưng hiếm |
| **UC4** Billing / Charging Mismatch Prevention | Phiên sạc có phí sai hoặc trừ trùng | So khớp session ↔ billing ↔ quyền ưu đãi | Chỉ khi bằng chứng mâu thuẫn *(cố ý LLM-light)* | Tự sửa (nếu policy cho), chuẩn bị điều chỉnh, người duyệt | Số tiền + liên kết + phiên sau đúng | Spec only | THẤP |
| **UC5** Proactive Warranty / Claim Follow-up | Claim kẹt (chờ bổ sung, SLA gần) | State + thời gian + phụ thuộc | Khi lý do trả về là văn bản tự do / mơ hồ | Nhắc, xin bổ sung, đính kèm bằng chứng, escalate nội bộ | Bằng chứng nhận được, claim tiến triển | Spec only | TB |
| **UC6** Recurrence / Return-of-Friction Prevention | Tín hiệu quay lại sau khi case đã đóng | Case cũ đã resolved + tín hiệu tương tự + ngưỡng + cooldown | Để đánh giá "lần can thiệp trước có thật sự giải quyết không" | Check-in, đề nghị kiểm tra lại, mở lại, escalate | Telematics sau lần xử lý mới | Spec only | TB / CAO |

### Cost tier — mỗi use case tiêu LLM ở đâu

*Nguyên tắc: hệ thống chỉ tiêu trí thông minh ở nơi trí thông minh tạo thêm giá trị.*

| UC | Detector tất định | Triage L1 (model nhỏ) | Agent L2 (suy luận) | Cost tier | Lý do |
| --- | --- | --- | --- | --- | --- |
| UC1 | Bắt buộc | Tuỳ chọn | Chỉ cho candidate có ý nghĩa và mơ hồ | **CAO — chỉ khi có candidate thật** | Can thiệp nhiều nguồn, nhiều lựa chọn |
| UC2 | Bắt buộc | Không cần | Có chọn lọc | **TB / CAO — chỉ khi mơ hồ** | Trạm hỏng rõ → đường tất định, không LLM |
| UC3 | Bắt buộc (điều kiện đầu vào) | Không | **Bắt buộc** — suy luận đa ràng buộc | **CAO — chỉ gọi sau khi can thiệp đã chính đáng** | Linh kiện × kỹ năng × slot × quãng đường × lịch khách |
| UC4 | Bắt buộc, xử lý phần lớn ca | Không | Tuỳ chọn, hiếm | **THẤP** | Chứng minh "không phải event proactive nào cũng cần Agent" |
| UC5 | Detector + state machine trước | Có thể (trích lý do trả về) | Chỉ khi ngữ cảnh / hành động mơ hồ | **TB** | Phần lớn là trạng thái có cấu trúc |
| UC6 | Bắt buộc | Không | Cho suy luận tái phát | **TB / CAO** | So case cũ với tín hiệu mới |

Cách đo (nằm trong eval, §22–§23): `llm_call_rate = số lần gọi L2 / số event`, token và độ trễ theo tầng, chi phí cho mỗi việc được giải quyết **và xác minh**. Chưa có số đo thật; mọi ngưỡng ở đây là **[ASSUMPTION]** để chỉnh theo dữ liệu giả lập.

### Final MVP — phạm vi tuần này

MVP phải chứng minh **một engine proactive-care thống nhất**, không phải sáu sản phẩm rời. Cả sáu UC dùng chung: event bus + detector registry → arbitration → context builder → Agent chọn lọc → validator → Executor → verifier → journey.

| Mức | Use case | Phải chạy được | Cắt gì nếu trễ |
| --- | --- | --- | --- |
| **FULL — implement đầy đủ** | **UC1** | Bơm tín hiệu giả lập → L0 → arbitration → context → (L1) → L2 → validator → tin chủ động → khách xác nhận → verify bằng đồng hồ giả lập → handoff. Có eval tự động + hard gate + trace panel | Không cắt — flagship |
| **DEMO-READY — tích hợp, chạy end-to-end ở happy path + 1 nhánh lỗi** | **UC2** | Thất bại sạc lặp lại → đường tất định (trạm hỏng) **và** đường Agent (trạm khoẻ) → verify bằng phiên sạc kế tiếp | Rút còn đường tất định + 1 kịch bản Agent **(lead 03/10: UC2 hoãn tuần 3, làm nếu dư giờ — xem `plan/PLAN.md`)** |
|  | **UC3** | Từ can thiệp đã được chấp nhận → 2–3 phương án có lý do loại → xác nhận → validator → Executor → verify; nhánh lập lại phương án khi reservation bị huỷ | Rút còn 2 phương án + 1 nhánh lập lại |
| **SPEC / SCENARIO ONLY — chưa implement** | **UC4, UC5, UC6** | Tài liệu đủ: trigger, detector, trách nhiệm Agent, action, verify, kịch bản khung, tiêu chí chấp nhận, backlog | Chỉ cần kịch bản khung YAML trong `sim/scenarios` nếu B còn giờ |

Chi tiết từng mốc ngày nằm ở §42 (kế hoạch), §44 (backlog), §45 (demo).

### Use Case × Owner

Mỗi UC có đủ A/B/C/D. Chi tiết nằm cuối từng mục UC.

| UC | **A — Agent / AI** | **B — Data / Tools / Thế giới giả lập** | **C — Frontend / UX** | **D — Core / API / Hạ tầng / Eval** |
| --- | --- | --- | --- | --- |
| **UC1** | Prompt suy luận 8 câu hỏi, chọn can thiệp, tin chủ động, handoff, tiêu chí thành công của Agent | Schema event, tín hiệu giả lập, rule detector + ngưỡng, **arbitration** (`detect/arbitration.py`), context builder, tool đọc, tiêm kịch bản, seed | Thông báo chủ động, "Vì sao tôi nhận tin này", bằng chứng / nguồn, lựa chọn can thiệp, xác nhận, journey, trace | Validator, policy, claim_check, Executor, token, verifier, API / event plumbing, eval + hard gate, đo cost / latency |
| **UC2** | Suy luận nguyên nhân (5 giả thuyết), chọn can thiệp, tin | Sự kiện phiên sạc, CSMS giả lập, `find_chargers`, detector + cooldown, lịch sử sạc | Màn hình trạm thay thế, tin khẩn, trạng thái "đang theo dõi phiên sạc" | Luồng khẩn 24/7, verifier phiên sạc, eval, handoff routing |
| **UC3** | Suy luận đa ràng buộc, 2–3 phương án + lý do loại | `find_options` đủ ràng buộc, tồn kho / kỹ năng / slot, nhánh reservation huỷ | Màn hình phương án (lý do hợp lệ / loại), xác nhận mức 2, "Việc của tôi" | Validator 7 check, Executor + saga, verify đọc lại, eval phương án hợp lệ |
| **UC4** | (Tuỳ chọn) tổng hợp bằng chứng mâu thuẫn | Billing giả lập, quyền ưu đãi có phiên bản, detector so khớp | Thông báo "đang xử lý", màn hình duyệt cho đối soát | Ngưỡng tự sửa, duyệt mức 3, ledger idempotent, eval tiền = 0 sai |
| **UC5** | Trích lý do trả về, chọn bước kế, soạn tin tiến độ | Claim state machine, portal giả lập, SLA timer | Tiến độ claim cho khách, console task cho CVDV | Escalation, đồng hồ SLA, verifier, eval |
| **UC6** | So case cũ với tín hiệu mới, đánh giá "đã giải quyết thật chưa" | Case đóng + `verify_until`, rule tái phát, cooldown | Tin check-in, "lịch sử lần trước", nút kiểm tra lại | Giới hạn chu kỳ, escalate lần 2, verifier, eval |

### UC cũ → UC mới (để đọc task card và tài liệu cũ)

| UC cũ | Số mới | Chuyện gì xảy ra |
| --- | --- | --- |
| UC1 Service Appointment Rescue | **UC3** (một phần) + vai trò flagship chuyển sang **UC1 mới** | Bộ máy `find_options` / validator / Executor / lập lại phương án giữ nguyên, nhưng không còn là điểm bắt đầu. `parts.reservation.cancelled` trở thành tín hiệu lập lại phương án trong UC3 |
| UC2 Lời hứa báo giá bị quên | *(bỏ khỏi sáu UC)* | Chuyển sang backlog tương lai (§49). Ý tưởng "trích lời hứa từ transcript" còn giá trị, nhưng không nằm trong sáu UC của định hướng mới |
| UC3 Kẹt ở trạm sạc | **UC2** | Mở rộng thành phòng ngừa friction sạc; đường khẩn 24/7 + handoff giữ nguyên làm nhánh khẩn cấp |
| UC4 Phí sạc sai ưu đãi | **UC4** | Giữ số; làm rõ cố ý LLM-light |
| UC5 Đèn lỗi sáng lại sau sửa | **UC6** | Đổi số; khung closed-loop care |
| UC6 Claim bảo hành kẹt | **UC5** | Đổi số; Agent không quyết định kết quả bảo hành |

**Cẩn thận khi đọc task card:** các card trong `plan/tasks/` được viết trước khi đổi số. Bảng này là nguồn đúng; các card đã được cập nhật nhãn UC tương ứng (xem §44).

### Năm dạng lỗi ngầm — ống kính phân tích phụ

Phân loại T1–T5 từ bản trước vẫn dùng để *đặt tên* friction, nhưng không còn quyết định thứ tự hay phạm vi. T0 là dạng mới: friction **chưa thành case** — chính là thứ UC1 nhắm tới.

| Dạng | Ý nghĩa | UC liên quan |
| --- | --- | --- |
| T0 | Friction đang hình thành, chưa có case nào | UC1 (flagship), UC2 |
| T1 Lệch trạng thái | Hai hệ thống giữ hai sự thật khác nhau | UC4; nhánh lập lại của UC3 |
| T2 Lời hứa bị quên | Cam kết trong hội thoại không có trong hệ thống | *Ngoài sáu UC — backlog §49* |
| T3 Rơi quyền sở hữu | Chuyển giao giữa bot, người, tổ chức bị mất | UC5; đường khẩn của UC2 |
| T4 Đóng sớm | Hệ thống ghi "xong" nhưng vấn đề còn | UC6 |
| T5 Trùng lặp | Một vấn đề thành nhiều case qua nhiều kênh | *Tương lai* |

### Chi tiết từng use case

Mỗi mục dưới đây dùng cùng một khung 24 đề mục để A/B/C/D đọc là biết phải làm gì:
[UC1 — Preemptive Service Friction Rescue](#ucs1-preemptive-friction) ·
[UC2 — Charging Friction Prevention](#ucs2-charging-friction) ·
[UC3 — Service Readiness / Intervention Orchestration](#ucs3-service-readiness) ·
[UC4 — Billing / Charging Mismatch Prevention](#ucs4-billing-mismatch) ·
[UC5 — Proactive Warranty / Claim Follow-up](#ucs5-claim-followup) ·
[UC6 — Recurrence / Return-of-Friction Prevention](#ucs6-recurrence).

Công cụ khám phá bên dưới (tab UC) dùng cùng dữ liệu kịch bản; bản đầy đủ nằm ở các mục trên.

Thời gian, token, tỷ lệ trong agent trace là minh hoạ (Illustrative); toàn bộ kịch bản là Synthetic / illustrative scenario for MVP. Quy trình nội bộ là giả định.
