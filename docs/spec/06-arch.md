# 06 · Triển khai: MVP → production — MVP gọn, production mở rộng theo cùng ranh giới

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### MVP (30/9)

```yaml
[Web UI: Chat · Việc của tôi · Console NV · Demo panel]
            │  HTTP + SSE
            ▼
[FastAPI app — 1 service]
  ├─ /chat ──────► Agent (LangGraph + Gemini)
  │                  └─ tools = hàm Python
  │                        │
  ├─ /events/inject ► Detector (rule) ─► Agent (proactive)
  ├─ /clock/advance ► Đồng hồ giả lập
  │
  ├─ core/  warranty · range · validator · claim_check
  │         (Python thuần, có unit test)
  └─ sim/   thế giới giả lập (seed cố định)
            │
            ▼
      [Postgres hoặc SQLite]
Deploy: 1 container trên Cloud Run
```

### Production (hướng đích trên GCP)

```yaml
Kênh: App · Zalo OA · Tổng đài · Console
Cổng: API Gateway · Cloud Armor · Identity
Agent: LangGraph trên Cloud Run (checkpoint Postgres)
Tool: MCP servers (Cloud Run) → DMS · ERP ·
      CSMS · Warranty · CRM
Sự kiện: Pub/Sub → Dataflow (detector)
         ← Datastream (CDC hệ thống cũ)
Trạng thái: AlloyDB (+pgvector) · Redis
Workflow nhiều ngày: Temporal trên GKE
Phân tích: BigQuery · Looker
Bảo vệ: Sensitive Data Protection · VPC-SC
        · CMEK · Secret Manager
Quan sát: OpenTelemetry → Cloud Trace + Langfuse
Vận hành: Terraform · CI có cổng eval
Dữ liệu định danh: lưu trong nước
```

**Vì sao đi được từ trái sang phải mà không viết lại:** ranh giới module giữ nguyên. tools/ hôm nay là hàm Python, tuần 1 bọc thành MCP server mà agent không đổi. /events/inject hôm nay gọi detector trực tiếp, tuần 1 chuyển sang hàng đợi. core/ không bao giờ phụ thuộc LLM.
