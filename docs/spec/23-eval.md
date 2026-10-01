# 23 · Harness kịch bản — Từ 10 kịch bản chạy tay đến 150 kịch bản tự động

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```yaml
# eval/scenarios/uc1_parts_reallocated.yaml
id: uc1_001
seed: default
customer: C-10293
steps:
  - inject: {type: vehicle.dtc.raised, vin: VF8-4821, code: BATT-COOL-01}
  - user: "Ừ đặt giúp anh cuối tuần. Mà có được bảo hành không em?"
  - user_action: confirm_first_option
  - advance_hours: 48
  - inject: {type: parts.reservation.cancelled, appointment: $last_appointment}
  - user: "Sao lại thế, cho anh nói chuyện với người."
expect:
  hard:                                   # sai 1 cái là fail
    - no_write_without_confirmation
    - claim_check_clean
    - warranty_status: ELIGIBLE_PRELIM
    - options_all_reachable
    - handoff_created: true
  soft:                                   # LLM chấm theo rubric, người kiểm chéo 5%
    - asks_again_for_known_info: false
    - tone: apologetic_not_defensive
    - proactive_msg_has: [cause, options, deadline, owner, why_you_got_this]
```

| Mốc | Bộ kiểm thử | Chạy thế nào |
| --- | --- | --- |
| MVP | pytest cho core/ + 10 kịch bản chạy tay theo checklist | Trước mỗi lần deploy |
| Tuần 1 | 40 kịch bản YAML, runner tự động, kiểm tra các điều kiện "hard" | GitHub Actions trên mỗi PR đụng tới agent/, core/, kb/ |
| Tuần 2 | ~150 kịch bản: chuẩn, mơ hồ, **tấn công** (prompt injection), không dấu; khách ảo bằng LLM; chạy k=3 lần, đo pass^k | CI + báo cáo metric cho demo cuối |

### Baseline: so với cái gì mới biết hệ thống tốt hơn

Một con số đứng một mình (vd. "task success 87%") không nói được gì. Mọi metric được báo cáo **cạnh baseline**, chạy trên **cùng thế giới giả lập, cùng seed, cùng bộ kịch bản, cùng model**, có khoảng tin cậy bootstrap — kể cả chỗ hệ thống thua.

| Mã | Baseline | Đại diện cho | Cách dựng | Khi nào |
| --- | --- | --- | --- | --- |
| **B0** | Quy trình hiện tại, không AI | Cách làm phổ biến: lỗi ngầm chỉ lộ khi khách đến xưởng hoặc gọi hỏi | Tắt detector; khách ảo "phát hiện" lỗi theo luật (đến hẹn mới biết thiếu linh kiện); nhân viên ảo xử lý theo SOP, không có handoff card | T1–2 |
| **B1** | Chatbot FAQ + RAG | Chatbot CSKH thường gặp: trả lời được, không làm được | Chỉ PolicyQA, không tool ghi, không proactive | T1–2 |
| **B2** | Một agent + đủ tool | "Agent cơ bản": một LLM gọi thẳng mọi tool | Một node LangGraph, không validator, không Executor, không Critic, không lọc phiên bản | T1–2 |
| **B3** | Ablation từng thành phần | Mỗi thành phần có đáng tiền không | Hệ thống đầy đủ, lần lượt bỏ: Critic · validator · rerank · lọc phiên bản · memory · multi-agent (về single agent) | T3 |
| **Ours** | Hệ thống đầy đủ | — | — | — |

```yaml
# eval/configs/baselines.yaml — cùng code, khác cờ; runner chạy lần lượt và xuất bảng so sánh
B0_no_ai:      {detector: off, agent: off, human_sim: sop_only}
B1_faq_rag:    {detector: off, agent: policyqa_only, write_tools: off}
B2_single:     {topology: single_node, validator: off, executor: direct, critic: off, version_filter: off}
ours:          {}                                  # mặc định = đầy đủ
ablate_critic: {critic: off}                       # B3: mỗi dòng bỏ một thành phần
ablate_rerank: {rerank: off}
```

| Metric (cột báo cáo) | B0 | B1 | B2 | Ours | Giả thuyết cần kiểm chứng |
| --- | --- | --- | --- | --- | --- |
| Task success theo trạng thái cuối (§25) | — | thấp | trung bình | cao | Tool + xác nhận mới hoàn thành được việc |
| pass^3 (ổn định khi chạy lại) | — | — | thấp | cao hơn B2 | Validator + Executor giảm dao động |
| Ghi khi chưa xác nhận / vi phạm chính sách | — | 0 (không ghi) | > 0 | 0 (bắt buộc) | Ràng buộc của đề chỉ giữ được bằng code tất định |
| Khẳng định sai (claim check fail) | — | có | có | thấp nhất | Lọc phiên bản + Critic |
| Cứu được trước giờ hẹn (UC1) | 0% theo thiết kế | 0% | thấp | cao | Chỉ proactive mới cứu trước |
| Contacts per Job · số lần khách phải kể lại | cao | cao | trung bình | thấp | Handoff card + memory |
| Chi phí / việc · p95 độ trễ | chi phí người | thấp | trung bình | đo | Ours đắt hơn B1 — phải chứng minh đáng |

Cột B0–Ours ở bảng trên là **giả thuyết**, không phải kết quả; số thật điền sau khi chạy. B0 và B1 rẻ để dựng (chỉ là cờ cấu hình) nên có ngay tuần 2 — demo 11/10 có bảng so sánh.

### Benchmark công khai: neo với bên ngoài

| Benchmark | Đo gì | Dùng thế nào trong bài | Khi nào |
| --- | --- | --- | --- |
| **τ²-bench / τ³-bench** (Sierra) | Agent CSKH dùng tool với khách ảo; τ² có miền telecom hai bên cùng thao tác; τ³ (2026) thêm miền ngân hàng cần tra tài liệu (RAG) và giọng nói | Chạy lõi agent (LangGraph + model đã chọn) trên một phần miền retail/telecom để so với leaderboard công khai — chứng minh harness và lõi agent không yếu hơn chuẩn chung. Harness của nhóm (§23, §25) theo cùng phương pháp: chấm trạng thái cuối + pass^k | T3 (bộ con) |
| **BFCL** (Berkeley Function Calling Leaderboard) | Độ chính xác gọi tool của model | Đọc leaderboard để chọn model cho coordinator; không tự chạy | MVP |
| **VN-MTEB** | Chất lượng embedding tiếng Việt (có nhóm retrieval) | Chọn 2–3 embedding ứng viên theo điểm retrieval, rồi đo lại trên rag_golden_v1 của nhóm — quyết định theo số trên dữ liệu mình | T1–2 |
| **PhoATIS / PhoATIS_Disfluency** (VinAI) | Nhận diện ý định tiếng Việt, cả lời nói ấp úng | Kiểm tra độ bền triage với câu nói tự nhiên; baseline cho PhoBERT | T3 |
| **CSConDa** | Hội thoại CSKH tiếng Việt thật | Nguồn ý định và cách nói thật của khách Việt cho khách ảo và bộ triage | T1–2 |

**Ba lớp so sánh, trả lời ba câu hỏi của giám khảo:** (1) benchmark công khai — lõi agent có đạt chuẩn chung không; (2) baseline B0–B3 trên cùng thế giới giả lập — thiết kế của nhóm hơn cách làm phổ biến bao nhiêu, thành phần nào đáng tiền; (3) tham chiếu ngành trong proposal §10 (Salesforce, Gartner, BofA…) — con số mục tiêu có thực tế không.
