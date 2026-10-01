# 39 · Ma trận kỹ năng theo vai trò — Mỗi vai trò gắn với một sản phẩm thật, một người phụ trách

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Vai trò | Thể hiện ở | Sản phẩm cụ thể | Người | Khi nào |
| --- | --- | --- | --- | --- |
| **AI / LLM engineer** | §13 §15 §16 §34 §14 | Agent LangGraph, multi-agent, router, context packet, RAG pipeline | A | MVP → tuần 1 |
| **ML engineer** | §18 | PhoBERT triage 3 head, so baseline, ONNX INT8, cascade | A | Tuần 3 |
| **MLOps** | §18 §29 | MLflow + registry, shadow → canary, drift, trigger huấn luyện lại | D | Tuần 3 |
| **LLMOps** | §29 §30 §22 §24 §25 | Release registry prompt/SOP/KB, eval gate, trace OTel GenAI, eval online, ACRC | D | Tuần 1–2 |
| **Backend** | §19 §05 §35 | FastAPI async, token xác nhận, saga, outbox, locking | D | MVP → tuần 1 |
| **Infra / DevOps** | §07 §31 §30 §32 | Terraform GCP, CI/CD canary, SLO, bảo mật, runbook | D | Tuần 1 |
| **Data engineer** | §09 §07 §10 | Pub/Sub + schema + dead-letter, detector worker, BigQuery, hợp đồng dữ liệu | B | Tuần 1 |
| **AI data engineer** | §27 | Pipeline gán nhãn, sinh dữ liệu tổng hợp, DVC, embedding blue/green, lineage | B | Tuần 1–2 |
| **Data scientist** | §28 | Tính cỡ mẫu, ngưỡng theo chi phí, dự báo contact, survival, uplift | B (+A) | Tuần 2–3 |
| **Frontend** | §20 §21 | 3 màn hình realtime, design system, accessibility, e2e | C | MVP → tuần 2 |
| **QA / eval** | §23 §26 §22 | Harness kịch bản, khách ảo, red-team, tải, chaos | D + C | Tuần 1–2 |
| **Product / CX** | Proposal | Nghiệp vụ, blueprint, phỏng vấn, mystery shopping, kiểm thử người dùng | Cả nhóm | Tuần 1–2 |

**Phân bổ theo tuần:** tuần 1–2 thể hiện AI/LLM engineer, LLMOps, backend, infra/DevOps, data engineer, AI data engineer, frontend, QA và một phần data science (cỡ mẫu, ngưỡng). Tuần 3 bổ sung ML engineer + MLOps (PhoBERT) và data science nâng cao. Nếu tuần 3 bị rút ngắn, vẫn đủ 10/12 vai trò có sản phẩm thật.
