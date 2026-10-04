# C — Frontend & UX · tên: ______ · tải: VỪA (~28 giờ/tuần · tổng ~85,5h)

Sở hữu: `frontend/`, Cloud Build trigger, `docs/images/`, pitch deck + video. **Phần agent/platform:** node `offer` (C2.13), giám sát uptime + cảnh báo (C3.08), Cloud Build (C1.14). Kiểm tay UI (C1.15), tuyển người dùng thử (C2.12). Review chéo với B.
Tiêu chí UI/UX của BTC (20%): **responsive (mobile) · dark mode · loading state · thông báo lỗi thân thiện · accessibility · ≥ 3 màn**.
Skill hay dùng: `start-task` · `bootstrap-module` (phần frontend) · `review-pr` · `update-deliverables`.
Mọi task có card chi tiết (bấm mã task); card tuần 2–3 là **bản nháp**. **Chỉ tick `[x]` khi `python3 ../team-ai-kit/plan/verify.py <mã>` báo ĐẠT** + PR đã merge + 1 dòng `WORKLOG.md`. Tối Chủ nhật mỗi người soát card tuần sau bằng skill `write-task-card` (sửa đường dẫn / lệnh kiểm cho khớp code thật), người cặp review. Làm hoàn toàn độc lập bằng mock sinh từ `contracts/api.yaml` — không chờ backend.

## Tuần 1 · 28/9 → 4/10 · ~29,5h

### MVP (28–30/9)
- [ ] **[C1.01](tasks/C1.01.md)** · 0,5h · 28/9 — Hook log AI + `install.sh` (chạy lại sau C1.02 để gắn `frontend/AGENTS.md`).
- [ ] **[C1.02](tasks/C1.02.md)** · 2h · 28/9 — Dựng `frontend/` (Vite + React + TS strict + Tailwind + TanStack Query) theo skill `bootstrap-module`; `npm run gen:api` sinh kiểu từ `contracts/api.yaml`; **dark mode ngay từ đầu**.
- [x] **[C1.03](tasks/C1.03.md)** · 5h · 28–29/9 — Màn **Chat khách**: SSE (mock) · nút phương án · nút **Xác nhận hiển thị đủ tham số** (việc, xe, giờ, xưởng) · trích dẫn nguồn · nhãn "Trợ lý AI" · loading.
- [x] **[C1.04](tasks/C1.04.md)** · 3h · 29/9 — Màn **"Việc của tôi"** từ `/api/v1/jobs/{id}` (bước hiện tại, lời hứa, người phụ trách, thay đổi gần nhất).
- [x] **[C1.05](tasks/C1.05.md)** · 2h · 29/9 — **Demo panel**: reset · bơm 2 sự kiện · tua +2 / +14 ngày.
- [x] **[C1.06](tasks/C1.06.md)** · 4h · 30/9 — Màn **Console nhân viên**: danh sách handoff + HandoffCard (tóm tắt 1 dòng, mục tiêu, sự thật có nguồn, đã hứa gì, không được làm gì, hạn gọi lại) + nút nhận.
- [x] **[C1.07](tasks/C1.07.md)** · 2h · 30/9 — Chuyển mock → API thật (D1.11), giữ cờ `VITE_USE_MOCK` để demo được khi backend lỗi.
- [ ] **[C1.08](tasks/C1.08.md)** · 1h · 30/9 — Quay **video dự phòng** demo MVP (trước 15:00, cùng A).

### 1–4/10
- [x] **[C1.09](tasks/C1.09.md)** · 3h — Responsive mobile cho cả 4 màn + skeleton / spinner cho mọi lời gọi LLM + thông báo lỗi thân thiện (không hiện exception).
- [x] **[C1.10](tasks/C1.10.md)** · 2h — Accessibility cơ bản: tương phản AA, focus bàn phím, `aria-live` cho tin mới, cỡ chữ lớn cho người lớn tuổi.
- [x] **[C1.11](tasks/C1.11.md)** · 2h — SSE tự nối lại + trạng thái "đang kết nối lại"; test Vitest cho hook chat.
- [ ] **[C1.12](tasks/C1.12.md)** · 0,5h — Chủ nhật: screenshot 4 màn (sáng + tối) gửi D cho README.
- [ ] **[C1.14](tasks/C1.14.md)** · 1,5h — Cloud Build trigger deploy từ `main` (CI/CD ngoài repo, không sửa `.github/`) + `min-instances 1`. *(chuyển từ D1.19)*
- [ ] **[C1.15](tasks/C1.15.md)** · 1h · 30/9 trước 14:00 — Chạy tay 10 kịch bản MVP trên giao diện (local rồi Live URL), ghi lỗi giao A/D. *(tách từ D1.12)*

## Tuần 2 · 5/10 → 11/10 · ~32h

- [ ] **[C2.01](tasks/C2.01.md)** · 4h — Console: panel **copilot** (gợi ý có nguồn của A2.06) + auto-wrap ghi chú + trace panel thu gọn.
- [ ] **[C2.02](tasks/C2.02.md)** · 3h — Luồng UI cho đủ 4 workflow PRD: đổi/trả + ticket, cập nhật thông tin (xác nhận trước), tra việc.
- [ ] **[C2.03](tasks/C2.03.md)** · 2h — Tin chủ động trong chat: thẻ 5 phần + "vì sao tôi nhận tin này" + tắt nhận tin.
- [ ] **[C2.04](tasks/C2.04.md)** · 3h — Màn **Dashboard** nhỏ cho quản lý: số liệu từ eval / API (cứu trước hẹn, handoff, độ trễ) — màn thứ 5, điểm Product.
- [ ] **[C2.05](tasks/C2.05.md)** · 3h — Playwright: kịch bản demo 11/10 chạy tự động (không vỡ trước giờ trình bày).
- [ ] **[C2.07](tasks/C2.07.md)** · 3h — Hỗ trợ B chạy 5 buổi người dùng thử (quan sát, ghi chỗ bối rối trên UI).
- [ ] **[C2.08](tasks/C2.08.md)** · 4h — **Pitch deck** nháp 10 slide theo `presentation/README.md` (nội dung từ A2.12, B2.08) → `presentation/pitch_deck.pptx`.
- [ ] **[C2.09](tasks/C2.09.md)** · 2h — **Video bản 1** ≤ 5' (problem < 30" · demo 2–3' · kết quả AI · impact) → link trong `presentation/README.md` (B chép sang README).
- [ ] **[C2.11](tasks/C2.11.md)** · 2h — **Upsell**: OfferCard trong chat (nhãn Gợi ý, lý do, nguồn, Xem báo giá / Không quan tâm) + chỉ số upsell trên Dashboard. **Chờ:** C2.13 · **mock:** JSON.
- [ ] **[C2.12](tasks/C2.12.md)** · 3h — Tuyển 5 người dùng thử (chủ xe / người lái), phiếu câu hỏi (CES, 1–5 sao, 3 câu mở), lịch test. *(từ B2.06 — nghiên cứu UX)*
- [ ] **[C2.13](tasks/C2.13.md)** · 3h — **Upsell**: node `offer` sau `respond` — tối đa 1 gợi ý/hội thoại, sau câu trả lời chính, có nguồn + "Không quan tâm"; báo giá qua Xác nhận. **Chờ:** D2.13 · **mock:** `eligible_offers` giả. *(đổi: A → C: C làm cả node lẫn thẻ gợi ý)*
- [ ] **[C2.14](tasks/C2.14.md)** · 2h — Demo panel nút UC1 (cảnh báo lặp), UI nhiều event `options`, phiếu tiền chẩn đoán trên console. *(mới 03/10)*

## Tuần 3 · 12/10 → 18/10 · ~24h — cải thiện + deliverables

- [ ] **[C3.01](tasks/C3.01.md)** · 5h — Sửa UI theo feedback người dùng thử (B2.07) — ưu tiên chỗ bối rối lặp lại.
- [ ] **[C3.02](tasks/C3.02.md)** · 2h — Hiệu năng: tải lần đầu, lazy load màn phụ; Lighthouse ≥ 90 (accessibility, best practices).
- [ ] **[C3.03](tasks/C3.03.md)** · 4h — **Pitch deck bản cuối** (pptx + PDF) có số eval thật + screenshot mới.
- [ ] **[C3.04](tasks/C3.04.md)** · 4h — **Video bản cuối** ≤ 5' (quay trên Live URL, có phụ đề) → YouTube/Drive, link trong `presentation/README.md`.
- [ ] **[C3.05](tasks/C3.05.md)** · 2h — GIF ngắn (luồng UC1 + handoff) + screenshot sáng / tối cuối vào `docs/images/` (B nhúng vào README).
- [ ] **[C3.06](tasks/C3.06.md)** · 2h — Kiểm dark mode / mobile toàn bộ lần cuối trên Live URL.
- [ ] **[C3.07](tasks/C3.07.md)** · 3h — Tập pitch ≥ 3 lần (điều khiển slide + demo trực tiếp, có phương án chạy video nếu mạng lỗi).
- [ ] **[C3.08](tasks/C3.08.md)** · 2h — URL ổn định tới Demo Day + 7 ngày (min-instances, cảnh báo uptime, ngân sách). *(đổi: D → C: DevOps nhẹ)*
