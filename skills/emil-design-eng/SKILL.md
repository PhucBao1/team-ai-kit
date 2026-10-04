---
name: emil-design-eng
description: Motion cho frontend P-073 — quyết định có animate hay không, thời lượng, easing, spring, chuyển cảnh, kể chuyện theo cuộn, review motion. Bản vendored của emilkowalski/skill (emil-design-eng), ghim commit, bọc luật nhóm. Dùng khi thêm / sửa / review animation, transition, micro-interaction hoặc scroll storytelling trên Landing, trải nghiệm khách hay Console CSKH. Không dùng để chốt bố cục, màu, chữ (taste-skill), luồng UX (ui-ux-pro-max) hay audit a11y tổng (web-design-guidelines).
---
<!-- Modified by P-073 team, 2026-10-03: lớp bọc luật nhóm; bản gốc y nguyên ở references/upstream-SKILL.md -->

# emil-design-eng — motion (bọc luật nhóm)

Bản gốc: `references/upstream-SKILL.md` (emilkowalski/skill @ `e8a175de22`, không sửa). Nguồn, hash: `NOTICE.md`.
Bản đồ cả bộ skill + thứ tự ưu tiên: `../team-ai-kit/docs/frontend/skill-stack.md`.

## Luật nhóm P-073 (thắng nội dung bản gốc)

**Thứ tự ưu tiên:** yêu cầu sản phẩm > design system nội bộ (`taste-rules.md`, token) > taste-skill (mức `MOTION_INTENSITY` đã chốt)
> ui-ux-pro-max > **emil-design-eng** > web-design-guidelines.

- **Bỏ mục "Initial Response"** của bản gốc: không trả câu chào cố định, làm ngay việc được giao.
- Mục "Review Format (Required)": dùng được khi review motion, nhưng báo cáo theo định dạng của card / `review-pr`.
- `prefers-reduced-motion` là bắt buộc (không phải tuỳ chọn): bản giảm motion giữ nguyên thông tin và trạng thái cuối.
- Chỉ animate `transform` / `opacity`; không `transition: all`. Không thêm thư viện motion mới khi chưa duyệt trong card
  (ưu tiên CSS transition / `@starting-style` / WAAPI có sẵn).
- Mức motion theo bề mặt:
  | Bề mặt | Mức |
  |---|---|
  | Landing / Story page | Theo `design-system/proactive-care/motion.md` §4 và `pages/landing.md` L-02 (chờ sửa luật A-02); chỉ scroll-scrubbed, tắt được |
  | Trải nghiệm khách | Tiết chế: phản hồi nút, xuất hiện tin nhắn, chuyển bước; ≤ ~250ms; không chặn đọc |
  | Console CSKH | Tối thiểu: chỉ phản hồi trạng thái; không animation trang trí, không làm chậm thao tác lặp |
- Không animation ở nút Xác nhận / tham số xác nhận gây hiểu nhầm trạng thái; không đếm ngược / nhấp nháy ở OfferCard (`taste-rules.md`).
- Link `easing.dev` / `easings.co` trong bản gốc chỉ để người tra cứu; agent không cần mở.

## emil-design-eng KHÔNG quyết định
Có hay không một tính năng / màn · bố cục, màu, chữ · kiến trúc thông tin · ngưỡng a11y (vùng chạm, tương phản) ·
stack / thư viện · kết luận audit cuối.
