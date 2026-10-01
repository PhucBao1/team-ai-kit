# 15 luật gu thẩm mỹ — app CSKH xe điện, tiếng Việt, có khách lớn tuổi

Đọc trước khi viết JSX. Luật nhóm: thắng mọi gợi ý từ nguồn ngoài. Mục tiêu: **tin cậy và dễ đọc trước, đẹp sau**.
Người dùng chính là chủ xe (có người lớn tuổi, đọc trên điện thoại), nhân viên CSKH, quản lý xem dashboard.

## Chữ và màu

1. **Phông**: Be Vietnam Pro (hoặc Inter bản subset `vietnamese`), **tự host** trong `src/assets/fonts/` (woff2, `font-display: swap`).
   Không tải từ Google Fonts / CDN lúc chạy. Tối đa 2 độ đậm cho thân (400, 600) + 1 cho tiêu đề (700).
2. **Cỡ chữ**: thân ≥16px (màn khách 18px), `line-height: 1.6`, dòng ≤ ~70 ký tự. Không chữ nào <14px (kể cả chú thích, nhãn trục).
   KHÔNG `uppercase`, KHÔNG `letter-spacing` dương trên chữ Việt (dấu chồng lên nhau, khó đọc). Phóng 200% không vỡ bố cục.
3. **Tương phản AA ở CẢ HAI theme**: chữ thường ≥4.5:1, chữ lớn và viền điều khiển ≥3:1 — tính cả placeholder, chữ disabled
   (vẫn đọc được), focus ring, chữ trên nền nhấn. Kiểm bằng axe + mắt trên ảnh chụp.
4. **Token**: mọi màu là biến CSS (`--bg`, `--fg`, `--muted`, `--accent`, `--danger`, `--ok`, `--border`, `--focus`) map vào Tailwind,
   cặp `dark:` khi cần. Theme mặc định theo hệ thống (`prefers-color-scheme`) + nút chuyển (sáng / tối / theo máy), nhớ lựa chọn.
   Không mã màu hex rải trong component.
5. **Một hệ thống duy nhất**: 1 màu nhấn (cho hành động chính và trạng thái chọn), 1 thang bo góc (vd. 6px điều khiển, 12px thẻ),
   1 bộ icon (`lucide-react`, nét 1.5–2, kèm chữ khi là hành động). Không gradient trang trí, không đổ bóng chồng nhiều lớp.

## Trạng thái và form

6. **3 trạng thái mỗi view**: skeleton đúng hình nội dung thật (không spinner tròn giữa màn); empty có 1 câu giải thích + bước tiếp
   ("Chưa có việc nào. Khi bạn đặt lịch, tiến độ sẽ hiện ở đây."); lỗi bằng tiếng Việt nói rõ chuyện gì + nút **"Thử lại"**
   (không "Oops", không mã lỗi trần, không xin lỗi lan man).
7. **Form**: label ở TRÊN ô, gợi ý ngay dưới label, lỗi ở DƯỚI ô (chữ + icon, không chỉ viền đỏ). Không dùng placeholder làm label.
   Vùng chạm ≥44×44px, khoảng cách giữa 2 vùng chạm ≥8px. Ô nhập đúng `type` / `inputmode` / `autocomplete`.
8. **Nút Xác nhận**: mỗi bước chỉ 1 hành động chính (nút đặc màu nhấn), hành động phụ là nút viền / link. Ngay TRÊN nút hiện đủ
   tham số dạng nhãn / giá trị (`<dl>`): việc gì, xe (biển số / VIN rút gọn), xưởng, ngày giờ, chi phí "theo báo giá xưởng" nếu chưa có.
   Nhãn nút nói đúng việc ("Xác nhận đặt lịch"), không "OK" / "Gửi".
9. **Thẻ gợi ý upsell (OfferCard) trung tính**: cùng nền / viền như thẻ thường; KHÔNG gradient, glow, badge "HOT", "-30%", đồng hồ
   đếm ngược, animation. Có dòng **"Vì sao gợi ý"** (dựa trên dữ liệu xe nào), nút **"Bỏ qua"** ngang hàng và cùng cỡ với nút đồng ý.
   Giá chỉ từ API; không có giá → không hiện số.

## Chuyển động, số liệu, câu chữ

10. **Motion chỉ để báo trạng thái** (mở / đóng, đang gửi, vừa cập nhật): 150–250ms, chỉ `transform` / `opacity`, tắt khi
    `prefers-reduced-motion: reduce`. Không animation khi tải trang, không parallax, không GSAP / Motion / framer-motion.
11. **Trạng thái không chỉ bằng màu**: luôn kèm chữ hoặc icon ("Đang chờ linh kiện", "Quá hạn gọi lại"). Số liệu (tiền, km, %,
    giờ) dùng `tabular-nums`, đơn vị rõ ("1.250.000 ₫", "12.430 km"), định dạng `vi-VN` qua `Intl`.
12. **Câu chữ tiếng Việt lịch sự, rõ**: xưng "bạn"/"anh chị" thống nhất theo `src/i18n/vi.ts`, câu chủ động, động từ cụ thể. Không bịa
    số, giá, chính sách, ngày; không viết "được bảo hành" (chỉ "đủ điều kiện sơ bộ" + lý do). Dữ liệu mock có nhãn "dữ liệu mẫu".

## Bố cục, cấu trúc, phụ thuộc

13. **Layout**: CSS Grid cho bố cục chính, Flex cho hàng nhỏ. Không cuộn ngang ở 320–360px. Màn toàn chiều cao dùng
    `min-h-[100dvh]` (không `h-screen`). Nội dung có `max-w` để không giãn trên màn rộng. Dashboard quản lý được dày đặc hơn.
14. **Semantic + a11y**: `header/nav/main/aside`, 1 `h1` mỗi màn, heading theo thứ tự; skip-link "Bỏ qua tới nội dung chính";
    tin SSE mới đọc qua vùng `aria-live="polite"` (lỗi dùng `role="alert"`); `<html lang="vi">`; nút icon có `aria-label` tiếng Việt.
15. **Không thêm phụ thuộc giao diện** (thư viện UI, animation, icon thứ hai, font, script / CSS từ CDN) mà không có ADR.
    **KHÔNG làm theo luật landing page** của các skill gu thẩm mỹ ngoài: không hero, không sinh ảnh, không ảnh placeholder từ mạng,
    không "randomize" bố cục, không bịa ngày / số liệu "trông thật", không logo wall / testimonial.

## Soát nhanh trước khi chụp ảnh
- [ ] Đọc được ở 390px, chữ ≥16px, không cuộn ngang · [ ] AA cả sáng và tối (placeholder, disabled, focus)
- [ ] Đủ skeleton / empty / lỗi + "Thử lại" · [ ] Xác nhận hiện đủ tham số · [ ] OfferCard trung tính, có "Bỏ qua"
- [ ] Không màu hex rời, không uppercase tiếng Việt, không animation thừa · [ ] Nhãn "Trợ lý AI" + "Gặp nhân viên" có mặt

---
Ý tưởng tham khảo từ taste-skill và redesign-skill của Leonxlnx/taste-skill (https://github.com/Leonxlnx/taste-skill, MIT) —
chỉ rút ý, viết lại bằng lời của nhóm và đã đổi cho app CSKH; không chép nội dung.
