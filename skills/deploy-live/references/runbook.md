# Runbook sự cố Live URL (D2.07 · D3.07 · tuần demo)

Ngắn để đọc lúc gấp. Lệnh thay đổi hạ tầng do **người** chạy. Ghi mọi sự cố vào WORKLOG (giờ phát hiện, giờ xử lý, nguyên nhân, việc phòng ngừa).
Chi tiết lệnh: `cloud-run-ops.md`.

## Mức sự cố
| SEV | Dấu hiệu | Phản hồi | Ai |
|---|---|---|---|
| SEV1 | Live URL sập / 5xx hàng loạt / ghi sai dữ liệu khách / lộ secret | ngay, ≤ 15 phút: rollback hoặc tắt tính năng; xoay secret nếu lộ | D (+ người trực) |
| SEV2 | P95 > 3 s kéo dài, một luồng demo hỏng, LLM lỗi liên tục | ≤ 1 giờ: rollback hoặc chuyển model/mock theo cờ | người sở hữu module |
| SEV3 | lỗi lẻ, UI lệch, cảnh báo chi phí | trong ngày, mở card | người sở hữu module |

## Checklist nhanh (theo thứ tự)
1. `curl -s <URL>/health` — trả gì? (DB, Redis, LLM theo D2.07)
2. Log 50 dòng gần nhất (lệnh mục 2 trong `cloud-run-ops.md`) — lỗi đầu tiên là gì, từ revision nào?
3. Vừa deploy? → **rollback**: `gcloud run services update-traffic ev-cx-api --region asia-southeast1 --to-revisions <REVISION_TRƯỚC>=100`
4. Lỗi LLM/provider? → bật cờ mock/fallback (nếu có), báo nhóm; không sửa nóng prompt trên prod.
5. Chi phí tăng vọt? → kiểm request bất thường (IP), hạ `--max-instances`, siết rate limit.
6. Lộ secret? → tạo version mới trong Secret Manager, deploy lại, vô hiệu version cũ; ghi sự cố.
7. Ổn định lại → chạy 3 câu kịch bản demo; ghi WORKLOG; mở card sửa gốc + test tái hiện.

## Kiểm lần cuối ngày (tuần demo, mỗi tối)
- [ ] `/health` OK; 3 câu demo chạy trên URL thật; trace thấy trên LangSmith (đã che PII)
- [ ] Revision đang nhận 100% traffic = commit trên `main` (ghi vào README mục Demo)
- [ ] `min-instances=1`, `max-instances` đặt đúng; không có service worker/MCP public
- [ ] Không cảnh báo 5xx/latency/chi phí đang mở; ngân sách còn trong ngưỡng
- [ ] `/docs` tắt ở prod; CORS đúng domain frontend
- [ ] WORKLOG có dòng hôm nay (deploy, sự cố nếu có)
