# Checklist review frontend (P-073)

Đọc khi diff đụng `frontend/`. Luật nhóm (`docs/conventions.md` §9) luôn thắng file này.
Màn mới / sửa lớn giao diện → làm theo skill `add-frontend-screen`; file này chỉ để soát diff.

## React
- [ ] Không dùng `useEffect` + `setState` để tính giá trị dẫn xuất từ props/state — tính thẳng khi render (hoặc `useMemo` nếu đắt).
- [ ] Không khai báo component bên trong component khác (mỗi lần render tạo kiểu mới → mất state, remount).
- [ ] Không `{count && <X/>}` khi `count` là số (hiện chữ "0") — dùng `count > 0 ? <X/> : null`.
- [ ] `useEffect` có đăng ký listener / fetch / timer → có cleanup: `AbortController` (`signal`) cho fetch & listener, `clearTimeout` cho timer.
- [ ] Logic chạy do thao tác người dùng nằm trong event handler, không dựng effect theo dõi state.
- [ ] Gọi API qua hook TanStack Query trong `src/api/`; component không gọi `fetch`. Kiểu từ `src/api/types.ts` (sinh từ `contracts/api.yaml`), không viết tay.

## Dữ liệu trình duyệt
- [ ] `localStorage`: key có phiên bản (`p073:v1:theme`), chỉ lưu field cần, bọc `try/catch` (chế độ riêng tư / bị chặn). Không lưu token, PII, nội dung hội thoại.
- [ ] Không chèn HTML từ API / LLM bằng `dangerouslySetInnerHTML`; nếu buộc phải dùng → sanitize.

## Build & bảo mật
- [ ] Vite production: `build.sourcemap` là `'hidden'` hoặc `false`, không `true`.
- [ ] Không tải script / font / CSS từ CDN ngoài lúc chạy — đóng gói vào bundle.
- [ ] Không key / secret trong biến `VITE_*` (lộ ra bundle).
- [ ] Không còn `console.log` / lỗi console khi chạy màn đó.

## Lỗi & trạng thái
- [ ] Có error boundary bao quanh vùng màn hình (lỗi một widget không làm trắng cả trang), hiện thông báo dễ hiểu + cách thử lại.
- [ ] Mỗi màn dữ liệu có đủ 3 trạng thái: **loading** (skeleton/spinner có nhãn), **rỗng** (câu hướng dẫn), **lỗi** (thông báo + nút thử lại). Không màn trắng.
- [ ] Nút Xác nhận hiện đủ tham số hành động (việc, xe, giờ, xưởng, thời lượng); nút bị khoá khi đang gửi (không gửi 2 lần).

## A11y & giao diện (chấm UI/UX)
- [ ] Màn của khách: axe 0 vi phạm (`@axe-core/playwright` hoặc tương đương); tương phản AA; chữ lớn, vùng bấm đủ to.
- [ ] Phần tử bấm được là `<button>` / `<a>`, có nhãn đọc được (`aria-label` khi chỉ có icon); form có `<label>`.
- [ ] Dark mode đúng ở màn mới (không chữ đen trên nền tối, không màu cứng ngoài token Tailwind).
- [ ] Responsive: xem ở bề rộng điện thoại, không cuộn ngang.
- [ ] Chuỗi hiển thị nằm ở `src/i18n/vi.ts`; thẻ gợi ý upsell trung tính, không giống quảng cáo.

---
Ý tưởng tham khảo (diễn đạt lại, không chép nguyên văn): vercel-labs/agent-skills (MIT) — react-best-practices (commit 063bee94c3);
addyosmani/web-quality-skills (MIT) — best-practices (commit afa8da9421). Phần còn lại là quy ước riêng của đội P-073.
