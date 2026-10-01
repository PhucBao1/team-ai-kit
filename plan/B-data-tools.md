# B — Data & Tools · tên: ______ · tải: VỪA (~27 giờ/tuần · tổng ~82h)

Sở hữu: `src/sim/ detect/ kb/` (trừ reranker tuần 2), `src/agents/tools/` (tool đọc), `README.md` (tuần 1), `JOURNAL.md`, kịch bản eval UC1/upsell. **Phần agent/platform:** subgraph `charging` (B2.14), `post_repair` (B2.15), Pub/Sub worker (B2.16), PhoBERT + MLflow (B3.08, B3.09). Review chéo với C.
Skill hay dùng: `start-task` · `add-mcp-tool` · `add-kb-document` · `inject-fault` · `add-eval-scenario` · `update-deliverables`.
Mọi task có card chi tiết (bấm mã task); card tuần 2–3 là **bản nháp**. **Chỉ tick `[x]` khi `python3 ../team-ai-kit/plan/verify.py <mã>` báo ĐẠT** + PR đã merge + 1 dòng `WORKLOG.md`. Tối Chủ nhật mỗi người soát card tuần sau bằng skill `write-task-card` (sửa đường dẫn / lệnh kiểm cho khớp code thật), người cặp review. Việc của B ít chặn người khác nhất — **ngoại trừ B1.02, B1.03, B1.05 (đường găng MVP)**: làm trước.

## Tuần 1 · 28/9 → 4/10 · ~29,5h

### MVP (28–30/9)
- [x] **[B1.01](tasks/B1.01.md)** · 0,5h · 28/9 — Hook log AI + `install.sh`. **Xong khi:** `.ai-log/` có dòng mới; `git status` sạch.
- [ ] **[B1.02](tasks/B1.02.md)** · 1,5h · 28/9 trước 11:00 — Cùng A, D **duyệt** interface `src/sim/world.py` + `contracts/fixtures/demo_world.yaml` (đã có khung trong PR bootstrap: `get_world()`, `reset_world()`, `SimClock`) — sửa nếu thiếu trường, rồi đóng băng. **Xong khi:** `tests/test_fixtures.py` + `tests/test_interfaces.py` xanh. *(đường găng)*
- [ ] **[B1.03](tasks/B1.03.md)** · 4h · 28/9 — `src/sim/seed.py`: anh Minh (VF 8, 38.420 km, pin 42%), 20 khách / 24 xe, 3 xưởng (4 km · 6 km có kỹ thuật viên pin · 35 km), 8 mã lỗi, 3 chính sách, ~60 slot; `python -m src.sim.seed --reset` < 1 giây. *(đường găng)*
- [ ] **[B1.04](tasks/B1.04.md)** · 3h · 28/9 — Tool đọc `get_vehicle_status`, `explain_dtc`, `check_warranty` (gọi `src/core/warranty` của D), `list_jobs` (`@tool`, `src/agents/tools/`) + test. **mock:** kết quả bảo hành giả cho tới D1.05.
- [ ] **[B1.05](tasks/B1.05.md)** · 4h · 29/9 — `find_options`: tồn kho + quãng đường (`src/core/range`) + kỹ năng kỹ thuật viên + khoá slot 15'. **Xong khi:** trả 2–3 phương án, xưởng 35 km bị loại khi pin thấp. *(đường găng)*
- [ ] **[B1.06](tasks/B1.06.md)** · 3h · 29/9 — `src/detect/rules.py` (L0: huỷ giữ linh kiện < 72h trước hẹn → candidate T1; mã CRITICAL → safety) + đồng hồ giả lập + hàm bơm sự kiện (D nối vào `/events/inject`, `/clock/advance`).
- [ ] **[B1.07](tasks/B1.07.md)** · 2h · 30/9 — Kịch bản demo cố định trong `src/sim/scenarios/` + 2 xe phụ; nội dung Problem / Solution cho README (gửi D).
- [ ] **[B1.08](tasks/B1.08.md)** · 0,5h · mỗi ngày — Gom `WORKLOG.md` lúc 17:30 (mọi người tự ghi dòng của mình).

### 1–4/10
- [ ] **[B1.09](tasks/B1.09.md)** · 4h — KB: 3 chính sách công khai (bảo hành, bảo dưỡng, sạc) dạng markdown có phiên bản trong `src/kb/docs/` + `src/kb/ingest.py` + retriever hybrid (pgvector + từ khoá) trả đoạn kèm trích dẫn (skill `add-kb-document`).
- [ ] **[B1.10](tasks/B1.10.md)** · 2h — Lỗi tiêm có nhãn T1 + T2 (ca thật + ca gây nhiễu) + 10 kịch bản eval proactive (skill `inject-fault`).
- [ ] **[B1.11](tasks/B1.11.md)** · 1h — Chủ nhật: `JOURNAL.md` tuần 1 (mục tiêu · xong · khó khăn · bài học · tuần sau).
- [ ] **[B1.12](tasks/B1.12.md)** · 3h — 20 kịch bản eval hội thoại (skill `add-eval-scenario`): hỏi bảo hành, đổi ý giữa chừng, không dấu, đòi gặp người, prompt injection. *(chuyển từ A1.15)*
- [ ] **[B1.13](tasks/B1.13.md)** · 1h · 30/9 — README bản đầu theo `README_boilerplate.md` (Problem/Solution, Setup, Live URL). *(report bản 0 chuyển D1.21)*

## Tuần 2 · 5/10 → 11/10 · ~30,5h

- [ ] **[B2.01](tasks/B2.01.md)** · 3h — Thế giới mở rộng: 200 xe / 5 xưởng / 60 linh kiện; lỗi T3–T5 có nhãn.
- [ ] **[B2.03](tasks/B2.03.md)** · 2h — `find_chargers` (UC3: trạm còn cổng, đi tới được với SoC) + test.
- [ ] **[B2.04](tasks/B2.04.md)** · 2h — Contact arbitration (đang chat với NV? giờ yên tĩnh? ngân sách chú ý?) trong detector; hỗ trợ B2.16 (Pub/Sub).
- [ ] **[B2.05](tasks/B2.05.md)** · 1,5h — Ngưỡng detector theo chi phí (precision / recall trên lỗi tiêm) → 1 bảng cho report (bỏ phần cỡ mẫu pilot — dành giờ cho upsell).
- [ ] **[B2.07](tasks/B2.07.md)** · 4h — Chạy 5 buổi test (cùng C), tổng hợp feedback + điểm hài lòng → gửi D cho `eval/results/report.md`, gửi A lỗi hiểu sai.
- [ ] **[B2.08](tasks/B2.08.md)** · 3h — Nội dung Product cho pitch & README: thị trường (xe điện bàn giao, lượt dịch vụ/năm), đối thủ / cách làm hiện tại, mô hình kinh doanh.
- [ ] **[B2.09](tasks/B2.09.md)** · 1h — `JOURNAL.md` tuần 2; WORKLOG hằng ngày.
- [ ] **[B2.12](tasks/B2.12.md)** · 2h — **Upsell**: danh mục 4 gói giả lập (`src/kb/docs/offers/`) + mục `offers` trong fixture + 8 kịch bản eval (4 nên gợi ý · 4 cấm gợi ý).
- [ ] **[B2.13](tasks/B2.13.md)** · 3h — Eval RAG (Ragas: faithfulness, context precision/recall, version accuracy) trên `rag_golden` của B. *(từ D2.04 — B sở hữu KB nên tự đo KB của mình)*
- [ ] **[B2.14](tasks/B2.14.md)** · 3h — UC3 trạm sạc (`find_chargers`, mức khẩn khi SoC thấp) · **Chờ:** B2.03. *(đổi: A → B: B viết subgraph độc lập, A2.17 nối)*
- [ ] **[B2.15](tasks/B2.15.md)** · 3h — UC5 xác minh sau sửa (telematics sạch 14–30 ngày → đóng; tái phát → mở lại) dùng đồng hồ giả lập. *(đổi: A → B: B nắm detector + đồng hồ giả lập)*
- [ ] **[B2.16](tasks/B2.16.md)** · 3h — Pub/Sub topic + schema + dead-letter; detector worker Cloud Run (cùng B2.04). *(đổi: D → B: worker chạy detector của B)*

## Tuần 3 · 12/10 → 18/10 · ~22h — cải thiện + deliverables

- [ ] **[B3.01](tasks/B3.01.md)** · 5h — Dataset `triage_vi_v1` ≥ 1.000 câu (tổng hợp + lọc trùng + biến thể không dấu), 3 nhãn (ý định · mức khẩn · cảm xúc), chia train/test — cho B3.08.
- [ ] **[B3.03](tasks/B3.03.md)** · 4h — (Tuỳ chọn) notebook dự báo sóng liên hệ / survival trên dữ liệu giả lập — chỉ khi B3.01, A3.10 xong.
- [ ] **[B3.06](tasks/B3.06.md)** · 1h — `JOURNAL.md` tuần 3; WORKLOG hằng ngày.
- [ ] **[B3.07](tasks/B3.07.md)** · 2h — Tập pitch ≥ 3 lần (phần Product / Market).
- [ ] **[B3.08](tasks/B3.08.md)** · 6h — **PhoBERT triage** 3 đầu (ý định · mức khẩn · cảm xúc) trên `triage_vi_v1` của B; so baseline TF-IDF và LLM zero-shot. *(đổi: A → B: B làm dataset triage_vi_v1)*
- [ ] **[B3.09](tasks/B3.09.md)** · 4h — MLflow registry cho PhoBERT (B3.08): shadow → bật; theo dõi drift đơn giản (PSI). *(đổi: D → B: đi liền PhoBERT)*
