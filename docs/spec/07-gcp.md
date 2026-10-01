# 07 · Production trên GCP — Từng dịch vụ, dùng để làm gì

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
               ┌──────────── Kênh ─────────────────────────────────────────────┐
               │ App VinFast · Zalo OA · Tổng đài (STT/TTS) · Console NV · A2A  │
               └───────────────────────────┬──────────────────────────────────┘
                     Cloud Armor · API Gateway · Identity Platform / IAP (NV)
                                           │
  ┌─────────────────────────── VPC (Serverless VPC Access / PSC) ──────────────────────────┐
  │  Cloud Run: api · agent (LangGraph) · mcp-* · detector-worker · web                    │
  │  Agent Engine (tuỳ chọn) · GKE Autopilot: Temporal · vLLM (model tự host, GPU)         │
  │                                                                                        │
  │  Pub/Sub (ops-events, dead-letter) ◄── Datastream (CDC) ◄── DMS / ERP / Warranty cũ     │
  │        └─► Dataflow (detector ở quy mô lớn)                                            │
  │  AlloyDB (journey, audit, pgvector) · Memorystore (session, rate limit)                 │
  │  BigQuery (VoC, stall audit, holdout) · Looker (dashboard)                             │
  │  Secret Manager · KMS (CMEK) · Sensitive Data Protection · lớp sàng lọc prompt          │
  └────────────────────────── VPC Service Controls perimeter ──────────────────────────────┘
          Cloud Logging / Monitoring / Trace (OTel) · Langfuse (tự host trên Cloud Run)
          Artifact Registry + quét lỗ hổng · Cloud Build / GitHub Actions · Terraform
```

| Dịch vụ | Vai trò | Cấu hình gợi ý |
| --- | --- | --- |
| Cloud Run | api, agent, mcp-*, worker, web | min-instances 1 cho api/agent (tránh cold start); concurrency theo đo tải; traffic split cho canary |
| Gemini Enterprise Agent Platform | Model Gemini, Model Garden, embedding (agent chạy bằng LangGraph trên Cloud Run; Agent Engine tuỳ chọn) | Region có model cần dùng; quota theo môi trường |
| GKE Autopilot | Temporal; vLLM cho model open-weight (production) | Node pool GPU chỉ khi dùng model tự host |
| Pub/Sub | Hàng đợi sự kiện, dead-letter | Schema cho topic; ordering key = vin; retention 7 ngày để replay |
| Datastream | CDC từ DB hệ thống cũ | Chỉ bảng cần thiết |
| Dataflow | Detector ở quy mô hàng trăm nghìn xe | Streaming; rule versioned |
| AlloyDB | Journey State Graph, audit, KB vector | HA; PITR; tách schema identity |
| Memorystore (Redis) | Session, khoá slot tạm, rate limit | TTL rõ ràng |
| BigQuery + Looker | VoC, eval, nhóm đối chứng, dashboard | Chỉ dữ liệu đã ẩn danh |
| Sensitive Data Protection | Che / thay token dữ liệu cá nhân | De-identify trước khi gửi model bên ngoài và trước khi vào BigQuery |

### Môi trường & dữ liệu trong nước

| Môi trường | Dữ liệu | Deploy |
| --- | --- | --- |
| **dev** (project riêng) | Giả lập | Mỗi merge vào main |
| **staging** | Giả lập + replay ẩn danh | Sau eval gate |
| **prod** | Thật | Canary 10% → 50% → 100%, có duyệt |

**Mô hình lai cho dữ liệu định danh:** hiện chưa có region GCP tại Việt Nam (trung tâm dữ liệu hyperscale dự kiến khoảng 2027). Theo một báo cáo thị trường, Luật Bảo vệ dữ liệu cá nhân yêu cầu lưu dữ liệu người dùng Việt Nam trong nước — cần pháp chế xác nhận. Thiết kế:

- **Identity vault trong nước** (hạ tầng nội bộ / cloud nội địa): tên, SĐT, giấy tờ, vị trí chính xác.
- GCP chỉ thấy **token giả** (C-10293, vùng thay vì toạ độ).
- Tin gửi khách được "điền lại" định danh ở vault ngay trước khi gửi.
- Khi có region Việt Nam: chuyển vault vào GCP.
