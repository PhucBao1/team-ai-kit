---
name: taste-skill
description: Định hướng thị giác (art direction) cho frontend P-073 — cá tính thị giác, hướng chữ, bố cục, mật độ, độ biến thiên thiết kế. Bản vendored của Leonxlnx/taste-skill (design-taste-frontend v2), đã ghim commit, bọc luật nhóm. Dùng khi chốt hướng thị giác cho Landing / Story page, hoặc cá tính thị giác của trải nghiệm khách. Không dùng cho Console CSKH, bảng dữ liệu, luồng nhiều bước, motion chi tiết (emil-design-eng), kiến trúc UX (ui-ux-pro-max) hay audit cuối (web-design-guidelines).
---
<!-- Modified by P-073 team, 2026-10-03: lớp bọc luật nhóm; bản gốc y nguyên ở references/upstream-SKILL.md -->

# taste-skill — định hướng thị giác (bọc luật nhóm)

Bản gốc: `references/upstream-SKILL.md` (Leonxlnx/taste-skill @ `ce26fc25c0`, không sửa). Nguồn, hash: `NOTICE.md`.
Bản đồ cả bộ skill + thứ tự ưu tiên: `../team-ai-kit/docs/frontend/skill-stack.md`.

## Luật nhóm P-073 (thắng nội dung bản gốc)

**Thứ tự ưu tiên:** yêu cầu sản phẩm (spec `20-ui.md` / `21-fe.md`, card, contracts) > design system nội bộ
(`add-frontend-screen/references/taste-rules.md`, `frontend/AGENTS.md`, token CSS, `team-ai-kit/design-system/` khi có)
> **taste-skill** > ui-ux-pro-max > emil-design-eng > web-design-guidelines. Mâu thuẫn → làm theo bậc trên và ghi rõ đã bỏ gợi ý nào.

**Phạm vi theo bề mặt:**
| Bề mặt | Dùng taste-skill? |
|---|---|
| Landing / Story page | Có — vai trò chính: design read, 3 dial, chữ, bố cục, mật độ |
| Trải nghiệm khách (Chat khách, Việc của tôi) | Hạn chế — chỉ cá tính thị giác trong khung `taste-rules.md`; dial theo `design-system/proactive-care/MASTER.md` §2.1 |
| Console CSKH | Không (bản gốc tự nói: không dashboard, bảng dữ liệu, UI nhiều bước) |

**Ghi đè cụ thể lên bản gốc:**
- Stack cố định theo `21-fe.md`: React + TypeScript + Vite + Tailwind, TanStack Query. Bỏ mục 3.A (Next.js / RSC / `next/font`).
  Không tự cài thư viện / design system mới (mục 2.A, 3.F) — đề xuất trong card, người duyệt.
- Phông: Be Vietnam Pro / Inter subset `vietnamese` tự host (luật 1 của `taste-rules.md`) — thắng mục 0.D "tránh Inter" và 4.1.
  Không `uppercase`, không `letter-spacing` dương với chữ Việt.
- Không tài nguyên ngoài lúc chạy: bỏ `picsum.photos`, `cdn.simpleicons.org`, CDN, Google Fonts `<link>` (mục 4.8, 9.E). Icon: `lucide-react`.
- Màu luôn là token CSS, AA cả 2 theme, sáng / tối theo máy + nút chuyển (thắng mục 4.11 "Page Theme Lock" và 8.C).
- Nội dung là tiếng Việt, ngữ cảnh CSKH hậu mãi xe điện; người dùng có người lớn tuổi → tin cậy và dễ đọc trước, đẹp sau.
  Không testimonial / số liệu bịa (mục 4.10, 9.D vẫn áp dụng).
- "Hỏi 1 câu khi mơ hồ" (mục 0.C): hỏi người làm task, không tự chọn hướng trái spec.

## Cách dùng
1. Đọc `taste-rules.md` + spec bề mặt đang làm.
2. Đọc các mục cần trong `references/upstream-SKILL.md` (0, 1, 4, 9 là cốt lõi; 5 chỉ tham khảo — motion chốt ở `emil-design-eng`).
3. Xuất **Design Read** 1 dòng + 3 dial + danh sách gợi ý bản gốc đã bỏ vì luật nhóm. Ghi vào card hoặc
   `team-ai-kit/design-system/` (nơi lưu quyết định thiết kế), không viết thẳng vào code P-073 khi chưa duyệt.

## taste-skill KHÔNG quyết định
Kiến trúc thông tin, luồng, cấu trúc responsive (ui-ux-pro-max) · thời lượng / easing / chuyển cảnh (emil-design-eng) ·
kết luận a11y / audit (web-design-guidelines, web-accessibility) · stack, thư viện, API, contracts · nội dung sản phẩm.
