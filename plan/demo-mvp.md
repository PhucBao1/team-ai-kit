# Kịch bản demo MVP — T4 30/9 (≈ 5 phút) = bài kiểm end-to-end của tuần đầu

Mọi task MVP phục vụ kịch bản này. Dữ liệu: `contracts/fixtures/demo_world.yaml` (đồng hồ giả lập bắt đầu 30/9 09:00).
Chạy trên **Live URL**; dự phòng: video quay trước 15:00 (C1.08). LLM: OpenAI `gpt-4o-mini`.

| # | Người trình bày làm | Hệ thống phải làm (kiểm được) | Task giao |
|---|---|---|---|
| 0 | Demo panel → **Reset** | Thế giới về seed; "Việc của tôi" của anh Minh có lịch A-20931 (2/10 14:00, Long Biên) | B1.03 · C1.05 · D1.11 |
| 1 | Chat: *"Xe tôi báo lỗi làm mát pin, có được bảo hành không?"* | Gọi `get_vehicle_status`, `explain_dtc`, `check_warranty` · trả **"đủ điều kiện bảo hành sơ bộ"** + lý do + trích dẫn `kb:…` · không bịa số | A1.04 · B1.04 · D1.05 · C1.03 |
| 2 | Demo panel → bơm sự kiện **`uc1_parts_cancelled`** (R-7702) | Detector tạo candidate T1 · tin chủ động 5 phần xuất hiện trong chat · 2 phương án: Gia Lâm 3/10 09:00, Hoài Đức 1/10 09:00 · **không có Long Biên** (hết linh kiện) | B1.06 · A1.07 · B1.05 · C1.03 |
| 3 | Bấm **Xác nhận** phương án Gia Lâm | Nút hiện đủ: việc · xe · giờ · xưởng · `/api/v1/confirm` → validator 7 kiểm tra → `reschedule` · "Việc của tôi" đổi sang 3/10 09:00 · slot cũ được giải phóng | D1.08 · D1.09 · A1.06 · C1.04 |
| 4 | Thử gian lận: sửa token / bấm lại lần 2 | Token sửa → từ chối, không ghi · bấm lại → trả kết quả cũ, không đặt 2 lịch (idempotent) | D1.09 |
| 5 | Chat: *"Thôi cho tôi nói chuyện với người"* | HandoffCard đủ trường (tóm tắt 1 dòng, mục tiêu, sự thật có nguồn, đã hứa gì, không được làm gì, hạn gọi lại) xuất hiện ở Console NV | A1.08 · D1.11 · C1.06 |
| 6 | Mở trace | Thấy từng bước: triage → tool → critic → xác nhận; trace có trên LangSmith | A1.03 · D1.11 |

**Cổng 30/9:** chạy liền 6 bước 2 lần không lỗi · `ruff check src/ tests/` + `pytest tests/` xanh · Live URL mở được · video dự phòng có.

## Lần chạy thử (A1.09 tick khi có ≥ 2 dòng `[x]`)
- [ ] Lần chạy 1 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
- [ ] Lần chạy 2 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
