# WCAG 2.2 AA — áp vào app CSKH P-073

Đọc khi làm form, nút Xác nhận, header / ô chat dính, đếm hạn token, điều hướng giữa các màn. Audit cả màn → skill `web-accessibility`.
Luật nhóm: vùng chạm ≥44px (không chỉ 24px của WCAG 2.5.8) vì khách lớn tuổi.

| Tiêu chí | Áp vào app | Cách làm |
|---|---|---|
| 2.2.1 Timing adjustable | Token xác nhận có hạn | Trước khi hết hạn ≥60 giây: thông báo `role="alert"` "Phiên xác nhận sắp hết hạn" + nút **"Gia hạn"** (xin token mới, giữ nguyên tham số). Hết hạn → nói rõ và cho làm lại 1 chạm, không mất dữ liệu đã chọn. |
| 3.3.4 Error prevention | Mọi hành động GHI (đặt lịch, đổi lịch, huỷ) | Màn / khối xem lại hiện đủ tham số trước khi gửi; có "Sửa" quay lại bước trước mà không mất lựa chọn; huỷ là hành động riêng, nói rõ hậu quả. |
| 2.4.11 Focus not obscured | Header dính, ô nhập chat dính đáy, demo panel | Phần tử đang focus không bị che: `scroll-margin-top` = chiều cao header, `scroll-margin-bottom` = chiều cao ô chat (`scroll-padding` trên vùng cuộn). Kiểm bằng Tab ở 390×844. |
| 3.3.7 Redundant entry | VIN, biển số, SĐT, xưởng đã chọn | Không bắt nhập lại trong cùng phiên: điền sẵn / cho chọn lại giá trị đã có (giữ trong state của luồng, không localStorage). |
| 3.2.6 Consistent help | "Gặp nhân viên" / gọi tổng đài | Cùng vị trí tương đối trên MỌI màn khách (vd. góc trên phải header), cùng nhãn. |
| 3.3.1 / 3.3.3 Error identification | Form, ô chat | Submit lỗi → focus ô lỗi đầu tiên; ô lỗi có `aria-invalid="true"` + `aria-describedby` trỏ tới dòng lỗi dưới ô; lỗi nói cách sửa ("Biển số gồm 2 số, 1 chữ, 5 số"). |
| 1.4.10 Reflow | Mọi màn | Không cuộn ngang ở 320px và ở 200% zoom (1280px); bảng của console → chuyển dạng thẻ hoặc cuộn trong khung có nhãn. |
| 1.4.12 Text spacing | Chữ Việt có dấu | Đặt line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em, paragraph 2em → không cắt chữ / chồng chữ: không `height` cố định cho khối chữ, dùng `min-height`. |
| 1.4.3 / 1.4.11 Contrast | Cả 2 theme | Chữ ≥4.5:1, chữ lớn + viền điều khiển + focus ring ≥3:1; tính cả placeholder và disabled. |
| 1.4.1 Use of color | Trạng thái job, SLA handoff | Luôn kèm chữ / icon, không chỉ màu. |
| 2.5.8 Target size | Mọi nút, link trong thẻ | Nhóm: ≥44×44px, cách nhau ≥8px. |
| 4.1.3 Status messages | Tin SSE, "đang đặt…", "đã lưu" | Vùng `aria-live="polite"` cố định trong DOM từ đầu (không tạo lúc có tin); lỗi dùng `role="alert"`. Không đọc lại cả lịch sử chat. |
| 3.1.1 Language | Toàn app | `<html lang="vi">`; đoạn tiếng Anh (mã lỗi, tên model) bọc `lang="en"`. |
| 2.4.1 Bypass blocks | Mọi màn | Skip-link "Bỏ qua tới nội dung chính" là phần tử focus đầu tiên. |
| 2.3.3 / 2.2.2 Motion | Skeleton, chỉ báo đang gõ | Tôn trọng `prefers-reduced-motion`; không nhấp nháy; không tự cuộn khi người dùng đang đọc tin cũ. |

## Kiểm nhanh
- Tab từ đầu tới cuối mỗi màn: thứ tự hợp lý, focus luôn thấy, không bị header / ô chat che.
- Zoom 200% + 320px: không cuộn ngang. Bookmarklet / CSS text-spacing: không cắt chữ.
- axe (Vitest + Playwright) = 0 vi phạm `wcag2a`, `wcag2aa` ở màn khách; axe không thay được kiểm bằng tay.
