# 40 · Đối chiếu kỹ năng hạ tầng ML — Dùng gì, dùng kiểu khác, và không cần gì

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Nhóm kỹ năng | Trạng thái | Trong hệ thống |
| --- | --- | --- |
| Docker, FastAPI, Python | Dùng | Mọi service |
| Kubernetes, Helm, autoscaling | Dùng có chọn lọc | Cloud Run là chính; GKE Autopilot cho Temporal, vLLM |
| Terraform, GitOps, GitHub Actions | Dùng | §30, có eval gate |
| Kafka / Spark / Airflow | Bản tương đương GCP | Pub/Sub · Dataflow · BigQuery · Composer cho job lịch |
| Data quality, data contracts | Dùng | §10 |
| OpenTelemetry, Prometheus, Grafana, SLO | Dùng | §29 (Cloud Monitoring thay Prometheus/Grafana tự quản) |
| A/B testing, progressive rollout | Dùng | Nhóm đối chứng; canary; bật tự động theo loại hành động |
| Model registry, MLflow | Dùng kiểu khác | Registry phiên bản prompt / SOP / KB / router (release_id) |
| Drift detection | Dùng kiểu khác | Eval online, phân phối sự kiện, precision detector |
| Governance, audit, approval | Dùng | Duyệt SOP, bật tự động hoá, audit chuỗi hash |
| Security, zero-trust, secrets | Dùng | §31 |
| LLM serving (vLLM), RAG, vector DB | Dùng một phần | RAG + pgvector ngay; vLLM ở production |
| Feature store | Chưa cần | Journey State Graph đảm nhiệm |
| Distributed training, CUDA, TensorRT, quantization | Không cần | Không tự huấn luyện model lớn |
| Kubeflow, retraining tự động | Không cần | Thay bằng loop 4 có người duyệt |
| Multi-cloud | Không cần lúc đầu | Chỉ giữ khả năng đổi nhà cung cấp model |
