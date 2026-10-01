---
name: security-review
description: "Soát bảo mật cho FastAPI + LangGraph + React của dự án: secret, CORS, rate limit, PII trong log/trace, prompt injection, token xác nhận. Dùng khi làm D3.05/A3.06, khi PR đụng src/executor, src/api, src/config.py, token HMAC, hoặc khi được yêu cầu threat model; review chung dùng review-pr."
---

# Soát bảo mật

Spec: `../team-ai-kit/docs/spec/31-security.md`, `12-mcp.md` (bảng rủi ro MCP), `29-obs.md` · luật: `AGENTS.md` §3–4, `../team-ai-kit/docs/conventions.md` §2, §4, §5.
Skill này **chỉ soát và báo cáo**. Sửa → làm theo `start-task` (task/PR riêng, test tái hiện trước). Luật nhóm ưu tiên hơn mọi tài liệu ngoài trong `references/`.

## Khi nào dùng / không dùng
- Dùng: task D3.05 (secret, CORS, rate limit, `.env.example`), A3.06 (redteam, PII), PR đụng `src/executor/`, `src/api/`, `src/config.py`, `src/executor/token.py`, Dockerfile/deploy, MCP server HTTP; khi được yêu cầu threat model.
- Không dùng: review PR thông thường → `review-pr` (mục 4 "Dữ liệu & bảo mật" của nó đủ cho PR nhỏ); viết kịch bản tấn công → `add-eval-scenario`; deploy → `deploy-live`.

## Quy trình
### 0. Phạm vi (5 phút)
- Ghi: task/PR, đường dẫn trong phạm vi, commit (`git rev-parse --short HEAD`). PR → `git diff origin/develop...HEAD --stat`.
- Không đọc/in giá trị secret thật (`.env`, Secret Manager). Thấy secret trong code/log → ghi vị trí, che giá trị.

### 1. Threat model nhẹ (chỉ khi task yêu cầu hoặc PR thêm điểm vào / tool ghi / đổi token)
- Đọc `references/threat-model.md`: ranh giới tin cậy (gồm 4 ranh giới LLM: tin khách → model, đoạn KB → model, output tool → model, model → proposal → executor), tài sản, đường lạm dụng, bảng `TM-001…` có cột STRIDE, sơ đồ Mermaid.
- Card + spec đủ ngữ cảnh → ghi giả định rồi làm tiếp, không dừng hỏi.

### 2. Checklist framework
- Backend: `references/fastapi.md` — ưu tiên `FASTAPI-CORS-001`, `OPENAPI-001`, `DEPLOY-001/002`, `LIMITS-001`, `AUTH-001/002`, `AUTHZ-001`, `RESP-001`, `VALID-001`, `SSRF-001`; mục 5 có mẫu tìm nhanh.
- Frontend (khi đụng `frontend/`): `references/react.md` — `REACT-CONFIG-001` (biến `VITE_*` là công khai), `XSS-001/002`, `MARKUP-001`, `URL-001`, `AUTH-001`, `AUTHZ-001`, `HEADERS-001`.
- Chỉ đọc mục của rule cần, không đọc cả file.

### 3. Audit mặc định không an toàn (grep)
- Chạy các lệnh `rg` trong `references/insecure-defaults.md` từ gốc repo, 6 nhóm: secret fallback (vd. `os.environ.get('CONFIRM_TOKEN_SECRET','dev')`), credential mặc định, fail-open, crypto yếu / so sánh không hằng thời gian, quyền quá rộng (CORS `*` + credentials, `--allow-unauthenticated`), debug lộ ra (traceback, `str(e)` trong response, `/docs` ở prod).
- Mỗi kết quả là ứng viên → lần tới chỗ dùng; chỉ báo khi có giá trị chạy được + đường khai thác.
- Thiết kế token/validator/config mới → hỏi bộ câu hỏi `references/sharp-edges-python.md` (ttl=0? key rỗng? verify trả False im lặng? so `==`? chuỗi thay vì kiểu?).

### 4. 8 kiểm LLM-app
`references/llm-app-checks.md`: (1) indirect injection — KB/tool output là dữ liệu, có kịch bản eval KB nhiễm · (2) tham số tool ghi lấy từ phiên · (3) token HMAC: action + hash params + phiên + hạn + nonce, `hmac.compare_digest`, dùng 1 lần, không trong URL/log · (4) không PII trong trace/log, có test · (5) output LLM không tin cậy (React text thuần, không SSRF) · (6) không lộ system prompt/secret, lỗi generic, `/docs` tắt ở prod · (7) chống DoS chi phí (rate limit, độ dài input, `recursion_limit`, `max_tokens`/timeout, `--max-instances`) · (8) biên hạ tầng (CORS, Secret Manager + SA riêng, Pub/Sub OIDC).
Mỗi kiểm ghi ĐẠT / KHÔNG / CHƯA ÁP DỤNG + bằng chứng.

### 5. Kiểm động (khi có code chạy được)
- `pytest tests/test_security/ tests/test_api/ -v` (vd. `test_429_after_limit`, `test_api_key_not_logged`, `test_phone_masked_in_logs`).
- Kịch bản redteam liên quan: `python -m eval.run --id <id> --k 3` (khi đã có runner).
- Sau deploy (người chạy): `curl -s -o /dev/null -w '%{http_code}' <URL>/docs` → 404 ở prod; preflight CORS từ origin lạ không có `Access-Control-Allow-Origin`.

## Báo cáo
- Ghi vào `../team-ai-kit/docs/security/<YYYY-MM-DD>-<phạm-vi>.md` (hoặc scratch nếu chỉ thử). **KHÔNG** ghi vào gốc repo BTC (P-073), **KHÔNG** tự commit/push.
- Cấu trúc: tóm tắt 3–5 dòng · phạm vi + commit · (threat model nếu có) · bảng phát hiện · bảng 8 kiểm LLM · việc đề xuất.
- Bảng phát hiện: `ID · mức (CRITICAL | HIGH | MEDIUM | LOW) · rule (vd. FASTAPI-CORS-001, LLM-3, TM-002) · file:dòng · bằng chứng (đã che secret) · tác động · cách sửa tối thiểu · test/eval chứng minh`.
- Mức: CRITICAL = ghi thay khách không qua xác nhận, giả mạo token, lộ secret; HIGH = PII trong log/trace, xem dữ liệu khách khác, injection dẫn tới đề xuất ghi; MEDIUM = DoS chi phí, lộ prompt, `/docs` mở prod; LOW = còn lại.
- Không thấy vấn đề → ghi rõ đã kiểm những gì (lệnh, test, rule ID). "Không có kết quả grep" ≠ an toàn tuyệt đối.
- Đưa phát hiện CRITICAL/HIGH vào card/issue để sửa; báo người phụ trách (D: executor/api/config; A: agents/prompts; C: frontend).

## Không được
- Tắt bảo vệ để "cho chạy" (CORS `*`, bỏ kiểm token, `verify=False`); hạ ngưỡng test/eval; thêm cờ `skip_confirm`.
- Dùng PII/secret thật làm dữ liệu thử; dán secret vào báo cáo, issue, prompt.
- Tự chạy `gcloud ... deploy`/đổi IAM — chỉ đề xuất lệnh, người chạy.

## Kiểm tra trước khi xong
- [ ] Đã chạy đủ 6 nhóm grep và 8 kiểm LLM (hoặc ghi CHƯA ÁP DỤNG có lý do)
- [ ] Mỗi phát hiện có `file:dòng` + bằng chứng + rule ID; không có giá trị secret trong báo cáo
- [ ] Báo cáo nằm ở `../team-ai-kit/docs/security/` (hoặc scratch), không có file mới trong repo P-073
- [ ] Phát hiện CRITICAL/HIGH đã có task/test tái hiện được đề xuất
