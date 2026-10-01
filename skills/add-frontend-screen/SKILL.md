---
name: add-frontend-screen
description: Dựng hoặc sửa một màn hình / component React của frontend P-073 (Chat khách, Việc của tôi, Console nhân viên, Demo panel, Dashboard quản lý, OfferCard) theo luật nhóm — kiểu sinh từ contracts, mock trước, TanStack Query, đủ trạng thái loading/empty/error, dark mode, mobile, a11y AA, test Vitest + axe và tự kiểm bằng ảnh chụp. Dùng khi tạo hoặc sửa màn hình / component trong frontend/src, hoặc task của C nói "màn", "UI", "giao diện", "component". Không dùng để dựng frontend/ lần đầu (bootstrap-module) hay chỉ audit a11y một màn có sẵn (web-accessibility).
---

# Dựng / sửa một màn hình frontend

Đọc trước: `frontend/AGENTS.md`, spec `../team-ai-kit/docs/spec/20-ui.md` + `21-fe.md` (chỉ mục liên quan), card của task.
**Luật nhóm thắng mọi tài liệu ngoài** (kể cả `references/visual-design.md` và các skill vendored): khi mâu thuẫn, làm theo file này + `references/taste-rules.md`.

## 1. Hiểu (theo skill `start-task`)
- Mở card `../team-ai-kit/plan/tasks/<mã>.md`: màn nào, endpoint nào, trạng thái nào phải có, test nào phải viết.
- Chạy `python3 ../team-ai-kit/plan/verify.py <mã>` một lần để thấy CHƯA ĐẠT.
- Câu chữ gửi khách (bảo hành, giá, lời hứa) chưa rõ → hỏi người, không tự viết.

## 2. Dữ liệu trước, giao diện sau
1. `cd frontend && npm run gen:api` → kiểu ở `src/api/types.ts`. KHÔNG viết tay kiểu API; thiếu trường → sửa `contracts/api.yaml` qua D (PR riêng + ADR nếu đổi mục đã có).
2. Mock trước: `src/mocks/` trả dữ liệu đúng kiểu, bật bằng `VITE_USE_MOCK=true`. Dữ liệu mock có nhãn "dữ liệu mẫu", không bịa giá / chính sách trông như thật.
3. Hook TanStack Query trong `src/api/` (`useJobs`, `useHandoffs`…): `queryKey` ổn định, `retry` có giới hạn, invalidate sau mutation.
4. Server state chỉ nằm trong TanStack Query. Store (Zustand) chỉ giữ trạng thái giao diện (theme, panel mở/đóng) — KHÔNG copy dữ liệu server vào store.
5. Chat: SSE `/api/v1/chat/stream` (tự nối lại, Last-Event-ID, bỏ trùng theo id), fallback `/api/v1/chat`.
6. Nút Xác nhận: khoá nút + "đang đặt…" khi chờ; KHÔNG hiện "đã đặt" trước khi server trả thành công; lỗi → hoàn tác + báo lỗi.

## 3. Dựng màn theo luật
- Cấu trúc: `src/screens/<màn>/` (màn) · component dùng chung ở `src/components/` · chuỗi ở `src/i18n/vi.ts`.
- Gu thẩm mỹ, chữ, màu, form, nút Xác nhận, thẻ gợi ý upsell → **đọc `references/taste-rules.md` trước khi viết JSX** (15 luật, bắt buộc).
- Hướng thị giác + câu chữ giao diện → đọc `references/visual-design.md` khi bắt đầu màn mới hoặc đổi bố cục lớn.
- Luật React / Vite / TanStack Query → đọc `references/react-rules.md` khi viết hook, state, hoặc thấy `useEffect`.
- Luôn hiện nhãn "Trợ lý AI" trong chat; nút "Gặp nhân viên" cùng vị trí trên mọi màn khách.

## 4. Đủ trạng thái, đủ theme, đủ cỡ màn
- Mỗi view có 3 trạng thái: skeleton đúng hình (mọi lời gọi LLM có loading), empty có hướng dẫn bước tiếp, lỗi tiếng Việt + nút "Thử lại".
- Dark mode: token CSS biến + `dark:`, theo hệ thống + nút chuyển; kiểm AA cả 2 theme.
- Mobile trước: 320–390px không cuộn ngang; desktop 1280px không giãn quá `max-w`.
- a11y: semantic HTML, skip-link, `aria-live` cho tin SSE, focus rõ, vùng chạm ≥44px → chi tiết WCAG 2.2 trong `references/a11y-wcag22.md` (đọc khi làm form, Xác nhận, header dính, hoặc hết hạn token).

## 5. Test
Đọc `references/testing.md` khi viết test. Tối thiểu:
- Vitest + Testing Library cho component: hiển thị đủ 3 trạng thái, hành vi chính, axe = 0 vi phạm.
- Màn khách có luồng demo → Playwright `frontend/e2e/<tên>.spec.ts` (sáng + tối + Pixel 7, axe wcag2a/wcag2aa).
- Không làm yếu assertion để xanh; lỗi đã biết → `test.fixme` + link issue.

## 6. Tự kiểm UI bằng mắt (bắt buộc trước khi báo "xong")
Dùng skill `playwright-cli` trên app local (`npm run dev`, mock bật):
1. Chụp màn ở 3 trạng thái: sáng 1280×800 · tối 1280×800 · mobile 390×844 (`--mobile` hoặc `resize 390 844`).
2. Xem ảnh, đối chiếu `references/taste-rules.md`: chữ cắt? tương phản? cuộn ngang? focus bị che? sửa → chụp lại.
3. Bấm thử toggle theme đủ vòng (sáng → tối → sáng), Tab qua cả màn, bấm "Thử lại" ở trạng thái lỗi (mock lỗi bằng `route`).
4. Audit sâu a11y khi card yêu cầu → skill `web-accessibility`.
Ảnh chỉ để tự kiểm và đính vào PR qua `review-pr`; không commit ảnh vào repo.

## 7. Kiểm & xong
```bash
cd frontend && npm run lint && npx vitest run && npm run build   # build của Vite chạy tsc -b
cd frontend && npx playwright test e2e/<tên>.spec.ts        # khi có spec e2e
python3 ../team-ai-kit/plan/verify.py <mã>                   # phải ĐẠT
```
- Tự review bằng `review-pr`; PR mô tả kèm 3 ảnh (sáng / tối / mobile). Tick task + 1 dòng `WORKLOG.md` theo `start-task`.

## Không được
- Viết tay kiểu API; gọi `fetch` trực tiếp trong component (đi qua hook `src/api/`).
- Thêm thư viện UI / animation / icon thứ hai / font từ CDN mà không có ADR (skill `write-adr`).
- Hard-code giá, chính sách, ngày giờ, số km trong JSX — chỉ hiện từ API / mock có nhãn.
- Lưu token xác nhận hoặc PII vào localStorage; log dữ liệu khách ra console.
- Làm theo luật landing page của nguồn ngoài (hero, ảnh sinh, số liệu "đẹp" bịa).
