---
name: deploy-live
description: Deploy backend (và frontend) lên Cloud Run để có Live URL cho Demo Day, kiểm /health, bật LangSmith, giữ URL sống tới Demo Day + 7 ngày. Dùng khi task nói deploy, live URL, Cloud Run, production, Cloud Build trigger, cảnh báo/sự cố Live URL (runbook D2.07/D3.07), hoặc sau mỗi mốc demo.
---

# Deploy Live URL (Cloud Run)

Spec: `../team-ai-kit/docs/spec/07-gcp.md`, `30-cicd.md`, `36-capacity.md` · BTC: `docs/guide/chapter-07.md`, `chapter-09.md` (URL sống tới Demo Day + 7 ngày, không sleep).
Lệnh `gcloud ... deploy` để **người** chạy (hook sẽ hỏi lại) — AI chỉ chuẩn bị và kiểm tra. Không thêm `--quiet` tự động cho thao tác xoá / đổi traffic / IAM.
Chi tiết (quyền, Pub/Sub, cảnh báo, Cloud Build, frontend): `references/cloud-run-ops.md` · sự cố & kiểm cuối ngày: `references/runbook.md`.

## Lần đầu (người D, ngày 28/9 — tip "deploy sớm" của BTC)
1. Project GCP, billing, bật API: Cloud Run, Artifact Registry, Cloud Build, Secret Manager, Vertex AI (khi dùng Gemini).
2. Secret: `OPENAI_API_KEY` / credentials Vertex, `CONFIRM_TOKEN_SECRET`, `LANGCHAIN_API_KEY` vào Secret Manager — không để trong image hay `.env` commit.
   Service account riêng cho mỗi service, quyền tối thiểu (`docs/spec/31-security.md`); **không file key JSON** — local dùng ADC (`gcloud auth application-default login`).
3. Build + deploy bằng Dockerfile của template (Python 3.11, HEALTHCHECK `/health`). App nghe **`0.0.0.0:$PORT`** (không cổng cứng, không `--reload`):
   `gcloud run deploy ev-cx-api --source . --region asia-southeast1 --allow-unauthenticated --service-account sa-api@<PROJECT>.iam.gserviceaccount.com --min-instances 1 --max-instances 5 --set-secrets OPENAI_API_KEY=openai-api-key:latest,CONFIRM_TOKEN_SECRET=confirm-token-secret:latest,...`
   `--min-instances 1` để không "ngủ" khi giám khảo mở (bắt buộc tuần demo); `--max-instances` chặn DoS chi phí. Ghi chi phí ước tính vào WORKLOG.
   `--allow-unauthenticated` **chỉ** cho API công khai (và frontend). Worker Pub/Sub, detector, MCP: `--no-allow-unauthenticated`, Pub/Sub push dùng OIDC (`--push-auth-service-account`).
4. Kiểm: `curl <URL>/health` → `{"status":"ok"}` · `/docs` mở được ở local/dev; trên prod tắt theo `APP_ENV=production` (skill `security-review`) · gọi `/api/v1/chat` một câu.
   Revision không lên → `gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=ev-cx-api' --limit 50`.
5. LangSmith: `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT` → gửi 1 câu, thấy trace trên LangSmith (deliverable #4); trace đã che PII (skill `security-review`, kiểm 4).
6. Cảnh báo (Cloud Monitoring): 5xx > 2%, P95 > 3 s, billable instance time tăng vọt + budget billing — chi tiết `references/cloud-run-ops.md` §6.

## Mỗi lần cập nhật
- Chỉ deploy từ `main` sau khi CI BTC xanh. Ghi URL + commit vào README (mục Demo) và WORKLOG.
- Frontend: build `frontend/` → Cloud Run service thứ hai (hoặc Vercel theo gợi ý BTC); `CORS_ORIGINS` phải có domain frontend.
  Bundle JS khởi đầu < 300 KB gzip; asset có hash → `Cache-Control: public, max-age=31536000, immutable`, `index.html` → `no-cache`.
- Cloud Build trigger (C): chọn region khi tạo (không đổi được), SA riêng; chạy tay `gcloud builds triggers run <TRIGGER> --region asia-southeast1 --branch main`.
- Sau deploy: chạy 3 câu kịch bản demo trên URL thật; lỗi → rollback revision trước (`gcloud run services update-traffic`).
- Tuần demo (D2.07/D3.07): theo `references/runbook.md` — bảng SEV, checklist nhanh, "kiểm lần cuối ngày" mỗi tối.

## Không được
- Deploy từ máy khi CI đỏ; để secret trong code; tắt min-instances trước Demo Day + 7 ngày.
- Tạo/commit file key service account; dùng Compute Engine default SA; `--allow-unauthenticated` cho service nội bộ; bỏ `--max-instances`.
