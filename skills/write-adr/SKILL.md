---
name: write-adr
description: Viết Architecture Decision Record ngắn cho một quyết định kỹ thuật (chọn framework, đổi hợp đồng tool, đổi kiến trúc, thêm dịch vụ GCP). Dùng khi đổi contracts/, thêm dependency lớn, đổi luồng dữ liệu, hoặc task nói ADR / quyết định kiến trúc.
---

# Viết ADR

Spec: `../team-ai-kit/docs/spec/47-adr.md`. Một ADR = một quyết định, ≤ 1 trang. ADR đặt trong repo: `docs/adr/` (giám khảo đọc được — mục System Design).

## Bước
1. Số tiếp theo: xem `docs/adr/`, lấy số lớn nhất + 1 (3 chữ số).
2. Copy `templates/adr.md` → `docs/adr/<số>-<slug>.md`. Trạng thái `Đề xuất`.
3. Bối cảnh: vấn đề + ràng buộc thật (thời gian 3 tuần, 4 người, GCP, ràng buộc đề). Không viết chung chung.
4. Liệt kê ≥ 2 phương án đã cân nhắc, kể cả "không làm gì".
5. Hệ quả: cái được, cái mất, cách đo lại quyết định (metric/ngưỡng), khi nào xem lại.
6. ADR đặt ở `docs/adr/` trong repo (giám khảo đọc — System Design); thêm 1 dòng vào bảng "Design Decisions" của `docs/architecture_diagram.md`. D duyệt → `Chấp nhận`.
