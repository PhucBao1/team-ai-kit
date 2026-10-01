# Cloud Run — chi tiết vận hành (P-073)

Đọc khi: deploy lần đầu, thêm service (worker, MCP, frontend), đặt cảnh báo, tạo Cloud Build trigger, hoặc revision mới không lên.
Nguồn ý tưởng (diễn đạt lại, Apache-2.0): Google `skills` @ `d5d905232e` — `skills/cloud/cloud-run-basics` (SKILL.md, references/iam-security.md),
`cloud-build-basics`, `cloud-run-alert-configuration` (references/services.md), `google-cloud-recipe-auth`. Luật nhóm ưu tiên hơn.
Mọi lệnh `gcloud` thay đổi hạ tầng: **người chạy**, đọc lại trước khi Enter. Không thêm `--quiet` cho thao tác xoá/đổi traffic/IAM.

## 1. Container
- App phải nghe **`0.0.0.0:$PORT`** (Cloud Run bơm `PORT`, mặc định 8080). Nghe `127.0.0.1` hoặc cổng cứng 8000 → revision crash khi khởi động.
  CMD mẫu: `uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}` (không `--reload`).
- Image gọn (multi-stage), chạy user không phải root, pin bản base image + dependency.

## 2. Revision không lên / crash
```bash
gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=ev-cx-api' \
  --limit 50 --freshness 1h --format='value(timestamp,severity,textPayload,jsonPayload.event)'
gcloud run revisions list --service ev-cx-api --region asia-southeast1
```
Thường gặp: sai cổng/host · thiếu biến/secret (Settings fail) · lỗi import do thiếu package · hết RAM (exit 137 → tăng `--memory`).

## 3. Danh tính & quyền
- Mỗi service một **service account riêng**, quyền tối thiểu (bảng trong `docs/spec/31-security.md`: `sa-api`, `sa-agent`, `sa-detector`…). Không dùng Compute Engine default SA (thường có quyền Editor).
  `--service-account sa-api@<PROJECT>.iam.gserviceaccount.com`
- **Không file key JSON** (không tạo, không commit, không đưa vào image). Local: `gcloud auth application-default login` (ADC); cần quyền của SA → impersonation (`--impersonate-service-account`), không tải key.
- Secret qua Secret Manager: `--set-secrets OPENAI_API_KEY=openai-api-key:latest,CONFIRM_TOKEN_SECRET=confirm-token-secret:latest,LANGCHAIN_API_KEY=langchain-api-key:latest`; cấp `roles/secretmanager.secretAccessor` cho đúng SA trên đúng secret.

## 4. Công khai hay không
- **Chỉ** API cho khách/giám khảo (và frontend) dùng `--allow-unauthenticated`.
- Worker Pub/Sub, detector, MCP server: `--no-allow-unauthenticated` (+ `--ingress internal` nếu được). Pub/Sub push dùng OIDC:
  `gcloud pubsub subscriptions create <sub> --topic <topic> --push-endpoint <URL>/push --push-auth-service-account sa-pubsub-push@<PROJECT>.iam.gserviceaccount.com`
  rồi cấp `roles/run.invoker` cho SA đó trên service worker.
- Kiểm: `gcloud run services get-iam-policy <svc> --region asia-southeast1` — worker không có `allUsers`.

## 5. Scale & chi phí
- `--max-instances 5` (chặn DoS chi phí) · `--min-instances 1` **chỉ trong tuần demo** (11/10 → Demo Day + 7 ngày; không "ngủ"); ngoài khung đó có thể về 0. Ghi chi phí ước tính vào WORKLOG.
- `--concurrency` mặc định 80 ổn cho FastAPI async; `--timeout` ≥ thời gian LLM tối đa + biên.

## 6. Cảnh báo (Cloud Monitoring, gửi email/Slack nhóm)
| Cảnh báo | Metric | Ngưỡng gợi ý |
|---|---|---|
| Lỗi 5xx | `run.googleapis.com/request_count` lọc `response_code_class="5xx"` | > 2% trong 5 phút |
| Độ trễ | `run.googleapis.com/request_latencies` P95 | > 3 s (BTC yêu cầu < 3 s) trong 5 phút |
| Chi phí | `run.googleapis.com/container/billable_instance_time` | tăng > 3× trung bình 1 giờ, và > 5 giây-instance/giây |
| Ngân sách | Billing budget | 50% / 90% / 100% số tiền nhóm đặt |
Kèm uptime check `/health` (task của C). Cửa sổ đánh giá 5 phút để tránh báo nhầm khi scale.

## 7. Cloud Build trigger
- Chọn **region** khi tạo (vd. `asia-southeast1`) — **không đổi được sau khi tạo**; build và trigger cùng region.
- Trigger dùng **SA riêng** quyền tối thiểu (`roles/run.builder`/`run.developer`, `iam.serviceAccountUser` trên SA runtime, `artifactregistry.writer`), không dùng SA mặc định.
- Chạy tay: `gcloud builds triggers run <TRIGGER> --region asia-southeast1 --branch main` → xem `gcloud builds log <BUILD_ID> --region asia-southeast1`.
- Chỉ ghi đè được substitution đã khai báo trong trigger.

## 8. Frontend
- Ngân sách bundle: tổng JS khởi đầu **< 300 KB nén gzip**. Kiểm: `cd frontend && npm run build && for f in dist/assets/*.js; do printf '%s %s\n' "$(gzip -c "$f" | wc -c)" "$f"; done`.
- Asset có hash trong tên (`dist/assets/*-[hash].js|css`): `Cache-Control: public, max-age=31536000, immutable`. `index.html`: `Cache-Control: no-cache` (để bản mới lên ngay).
- `VITE_*` là công khai — không đặt key/secret; `CORS_ORIGINS` của API phải có đúng domain frontend.
