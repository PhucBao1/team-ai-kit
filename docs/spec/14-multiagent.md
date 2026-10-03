# 14 · Multi-agent — Tách agent khi có lý do — agent đề xuất, code tất định thực thi

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Nguyên tắc: bắt đầu bằng một agent (MVP). Chỉ tách khi thoả ít nhất một điều kiện: **quyền tool khác nhau**, **model / chi phí khác nhau**, **cần test độc lập**, hoặc **context quá lớn**. Tách vì "trông hiện đại" chỉ làm tăng chi phí, độ trễ và chỗ hỏng.

### Topology của hệ thống (tuần 1 trở đi)

```text
KÊNH KHÁCH ─► Coordinator (node supervisor, model nhanh) — giữ goal stack, nói chuyện với khách
                   ├─ route ────► PolicyQA subgraph     (RAG chính sách, chỉ tool đọc KB)
                   ├─ as tool ──► Scheduler subgraph    (model suy luận, lập phương án UC3 — một năng lực, không phải mục đích duy nhất)
                   ├─ as tool ──► Handoff builder      (lắp card từ state, model nhỏ)
                   └─ tool ─────► Executor tất định  (tool ghi: token + validator + saga) ◄─ duy nhất được ghi

SỰ KIỆN ─► Proactive pipeline = StateGraph nối tiếp [
              Detector L0 (code, không LLM) → Arbitration (code) →
              ContextBuilder (code) →
              fan-out song song [ vehicle · parts · slots · history ]  (Send / nhiều cạnh) →
              Decision gate (code: tất định đủ? → mẫu tin, KHÔNG LLM) →
              Coordinator điều tra → suy luận → InterventionProposal   (gọi Scheduler subgraph như tool khi UC3 cần) →
              Validator (claim_check, cụm từ cấm) →
              vòng Writer → Critic (claim_check + rubric), cạnh điều kiện, tối đa 2 lần →
              Arbitration kiểm lại (code) → gửi vào session của khách → Verifier (loop 5) ]

NHÂN VIÊN ─► Copilot agent (gợi ý có nguồn, không có tool ghi)
BATCH     ─► Insights agent (loop 4, VoC — chạy ngoài giờ, batch)
LIÊN ĐƠN VỊ ─► A2A: agent trạm sạc · agent cư dân · trợ lý AI của khách (agent card + phạm vi quyền)
```

| Pattern | Ở đâu | Cách làm trong LangGraph | Vì sao |
| --- | --- | --- | --- |
| Coordinator / dispatcher | Coordinator → PolicyQA | Node supervisor + conditional edge tới subgraph | Hội thoại chính sách dài cần context riêng |
| Hierarchical (agent như tool) | Scheduler, Handoff builder | Subgraph bọc thành tool | Coordinator giữ quyền điều khiển hội thoại, gọi chuyên gia như một hàm |
| Sequential pipeline | Proactive pipeline | Các node nối cạnh cố định | Các bước cố định, dễ test từng bước |
| Parallel fan-out / gather | Lấy dữ liệu xe, kho, slot | Fan-out bằng nhiều cạnh / Send API (hoặc TaskGroup trong code) | Giảm độ trễ |
| Generator – critic | Writer ↔ claim_check + rubric | Cạnh điều kiện Critic → Writer, đếm vòng trong state (tối đa 2) | Chặn tin sai trước khi gửi |
| Human-in-the-loop | Xác nhận của khách, duyệt hoàn tiền, duyệt SOP | interrupt() + checkpointer, resume bằng Command | Hành động có hậu quả |
| Agent-to-agent liên tổ chức | V-Green, Vinhomes, trợ lý AI của khách | A2A (adapter, roadmap) | Mỗi đơn vị giữ agent và dữ liệu của mình |

### Hợp đồng cho mỗi agent

```yaml
# agent/contracts.yaml — mỗi agent khai báo như một service
coordinator_care:           # agent gốc khi chạy với một candidate (UC1, UC2, UC5, UC6)
  goal: "Điều tra candidate → suy luận → đề xuất can thiệp (InterventionProposal)"
  model_tier: reasoning
  input:  ContextBundle       # từ context builder, mỗi fact có nguồn
  output: InterventionProposal
  tools_allow: [get_vehicle_status, explain_dtc, check_warranty, list_jobs, find_chargers]   # chỉ đọc; + scheduler (as tool)
  budget: {tokens: 8000, seconds: 10, tool_calls: 6}
  on_fail: "handoff với HandoffCard; không gửi tin"
scheduler:                  # năng lực của UC3
  goal: "Đề xuất 2–3 phương án đặt / đổi lịch khả thi, kèm lý do loại các phương án khác"
  model_tier: reasoning
  input:  SchedulerInput      # từ session.state["context"]
  output: list[Option]        # ghi vào session.state["options"] (output_key)
  tools_allow: [find_options, check_stock, explain_dtc]     # chỉ đọc
  budget: {tokens: 8000, seconds: 10, tool_calls: 6}
  on_fail: "trả options rỗng + lý do → coordinator chuyển người"
writer:
  model_tier: small
  output: ProactiveMessage    # 5 phần bắt buộc
  tools_allow: []
  critic: [claim_check, rubric_tone]
```

### Lỗi đặc thù của multi-agent và cách chặn

| Lỗi | Chặn bằng |
| --- | --- |
| Chuyển qua lại vô hạn giữa agent | Giới hạn số lần transfer / độ sâu; coordinator là điểm quay về duy nhất |
| Mất ngữ cảnh khi chuyển agent | Chỉ truyền **state có cấu trúc** (session.state, journey DB), không truyền văn bản tự do |
| Chi phí bùng nổ | Ngân sách token / thời gian theo agent và theo journey; vượt → dừng và chuyển người |
| Hai agent cùng ghi, ghi mâu thuẫn | Không agent LLM nào giữ tool ghi — chỉ Executor tất định, qua token + validator + saga |
| Agent này "tiêm lệnh" sang agent khác | Output của agent khác và của A2A được coi là dữ liệu không tin cậy, như tin nhắn khách |
| Khó debug | Mỗi agent một span OTel con, có agent.name, tokens, quyết định; xem trọn cây trong trace |
