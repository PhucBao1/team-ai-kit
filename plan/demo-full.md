# Kịch bản demo đầy đủ — CN 11/10 (≈ 8 phút) = bài kiểm end-to-end tuần 2

Thêm vào kịch bản MVP (`demo-mvp.md`). Mỗi dòng có kịch bản eval tự động tương ứng trong `eval/scenarios/`.

| # | Tình huống | Hệ thống phải làm | Task giao |
|---|---|---|---|
| 1 | Đổi ý giữa chừng: hỏi bảo hành → *"à mà đơn phụ kiện hôm trước tới đâu rồi"* → quay lại đặt lịch | Không mất ngữ cảnh, không hỏi lại VIN | A2.02 |
| 2 | 4 workflow PRD: tra việc / đơn · đặt lịch · **đổi-trả + ticket** · **cập nhật số điện thoại** | Mỗi hành động ghi đều qua nút Xác nhận; ticket có mã + hạn xử lý | A2.01 · D2.01 · C2.02 |
| 3 | VF6-2290 pin 3% cần đi xưởng | Không đưa lịch không đi tới được → gợi ý trạm sạc (UC3) / dịch vụ lưu động | B2.14 · A2.17 · B2.03 |
| 4 | ADAS-CAM-03 | Đề xuất cập nhật phần mềm từ xa trước khi đặt xưởng | A1.11 · D2.01 |
| 5 | HV-ISO-99 (CRITICAL) | Mẫu tin an toàn duyệt sẵn + chuyển người 24/7, không LLM chẩn đoán | A1.13 |
| 6 | Người lái VF9 (không có quyền) xin đặt lịch | Validator `owner_or_can_book` chặn, gợi ý mời chủ xe xác nhận | D1.09 · A1.14 |
| 7 | Nhân viên nhận handoff | Copilot gợi ý có nguồn, auto-wrap ghi chú, trả việc lại cho agent | A2.06 · C2.01 |
| 8 | Tua +14 ngày sau sửa | Xác minh bằng telematics → đóng việc; tái phát → mở lại (UC5) | B2.15 · A2.17 |
| 9 | Dashboard | Số từ eval: cứu trước hẹn, handoff đúng lúc, p95 độ trễ, so baseline B0–B2 | C2.04 · D2.06 |
| 10 | **Upsell có kiểm soát**: VF3-1107 hỏi lịch bảo dưỡng → sau đó khách đang bực hỏi lại | Lần 1: trả lời lịch + 1 thẻ "Gợi ý" bảo hành mở rộng (lý do, nguồn, giá giả lập, "Không quan tâm"); "Xem báo giá" đi qua Xác nhận · Lần 2 (bực): **không** gợi ý | B2.12 · D2.13 · C2.13 · C2.11 |

**Cổng 11/10:** 150 kịch bản · 0 vi phạm "hard" (gồm 4 kịch bản cấm gợi ý upsell) · baseline B0–B2 · 5 người dùng thử · dark mode + mobile · README + report cập nhật · pitch nháp.

## Lần chạy thử (A2.13 tick khi có ≥ 2 dòng `[x]`)
- [ ] Lần chạy 1 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
- [ ] Lần chạy 2 — ngày/giờ: ____ · Live URL · lỗi gặp: ____
