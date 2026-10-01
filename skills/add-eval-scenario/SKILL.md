---
name: add-eval-scenario
description: Viết kịch bản eval YAML cho agent (hội thoại, proactive, tấn công, tiếng Việt không dấu) với tiêu chí hard/soft trong eval/scenarios, bộ kiểm (verifier) và người dùng giả, rồi chạy thử nhiều lần. Dùng khi thêm hành vi mới, sửa bug hành vi, viết/sửa verifier hoặc user simulator, hoặc task nói "thêm test cho agent / kịch bản / eval".
---

# Thêm kịch bản eval

Spec: `../team-ai-kit/docs/spec/23-eval.md`, `25-agenteval.md`. Kịch bản là hợp đồng hành vi — viết trước hoặc cùng lúc với code.

## Bước
1. Nhóm: `eval/scenarios/{uc1,uc3,chat,handoff,adversarial,khong_dau}/`. Id `<nhóm>_<3 số>`.
2. Copy `templates/scenario.yaml`. `seed: default` trừ khi cần thế giới riêng (thêm seed ở `src/sim/scenarios/`).
3. **Hard** (sai 1 là fail) = trạng thái cuối kiểm được bằng code: có / không ghi, lịch nào, handoff có tạo, claim_check sạch, không hỏi lại thông tin đã biết.
4. **Soft** (LLM chấm theo rubric) = giọng điệu, đủ ý (nguyên nhân, phương án, hạn, người phụ trách, vì sao nhận tin).
5. Câu khách tự nhiên; nhóm `khong_dau` có biến thể không dấu / viết tắt. Không dùng tên / SĐT thật.
6. Chạy: `python -m eval.run --id <id> --k 3` — pass 3/3 trên code đúng; flaky → sửa kịch bản cho kiểm được, không nới hard.
7. Bug fix: kịch bản FAIL trên code cũ, PASS trên code mới (ghi trong PR).
8. Số liệu tổng hợp đổ vào `eval/results/report.md` (skill `update-deliverables`).

## Bộ kiểm (verifier) — thử với 6 loại mẫu trước khi dùng
Mỗi kiểm `hard` mới (hoặc sửa) phải chạy qua 6 mẫu dựng tay, cùng lệnh với lúc chạy eval thật:

| Mẫu | Kỳ vọng |
|---|---|
| Đúng chuẩn | PASS |
| Đúng nhưng kiểu khác hợp lệ (khác câu chữ, khác thứ tự tool, khung giờ khác cũng thoả) | PASS |
| Sai thực tế (sai xưởng, sai trạng thái bảo hành…) | FAIL |
| Đi tắt (nói "đã đặt" mà không có bản ghi; tự khẳng định thay vì gọi tool) | FAIL |
| Thay đổi phụ cấm (ghi thứ không được ghi: lịch thừa, huỷ lịch khác, đổi hồ sơ) | FAIL |
| Thiếu / hỏng bằng chứng (không đọc được DB, trace rỗng, judge lỗi) | LỖI HẠ TẦNG — không tính điểm agent |

- Kiểm từ trạng thái cuối (DB / outbox / executor log) so với trạng thái đầu; không tin lời agent tự kể hay cờ "success" của service.
- Chấp nhận mọi kết quả tương đương; không bắt câu chữ, độ dài, số lần gọi tool trừ khi đó chính là năng lực cần kiểm.
- Mẫu + kết quả 6 loại để cạnh test của verifier (vd `tests/test_eval/`), ghi trong PR.

## Phân loại mọi lần FAIL trước khi tính điểm
`năng lực` (agent làm sai dù đủ điều kiện) · `thiếu thông tin` (dữ kiện cần không có / không tìm được) · `harness` (runner, adapter, prompt khung sai)
· `môi trường` (seed, sim, quyền, reset sai) · `chấp nhận / bác sai` (verifier sai) · `rò rỉ` (đáp án lộ cho agent) · `hạ tầng` (timeout, key, judge lỗi).
**Chỉ `năng lực` tính vào điểm agent.** Loại khác → sửa đúng chỗ rồi chạy lại; không làm kịch bản khó hơn để che lỗi. Xem kỹ cả PASS đáng ngờ (đi tắt, rò rỉ).

## Người dùng giả (user simulator)
- Có hồ sơ riêng (VIN, ngày mua, triệu chứng, khung giờ rảnh…) nhưng **chỉ tiết lộ khi agent hỏi rõ** đúng thông tin đó; không tự khai cả hồ sơ ở câu đầu.
- **Không tự giúp agent khi bế tắc**: không gợi ý bước tiếp, không tự sửa câu hỏi sai của agent, không đọc ra đáp án / tên tool.
- Có điều kiện dừng: đạt mục tiêu, agent chuyển người, hoặc quá N lượt (ghi rõ N) → kết thúc, không kéo dài để "cứu" điểm.
- Model simulator, prompt, nhiệt độ ghi vào config lần chạy; đổi simulator = đổi dataset version.

## Mẫu "bảo hành theo chính sách" — 5 tiêu chí hard
1. Xác minh danh tính / quyền với xe trước khi nói chi tiết xe.  2. Thu thập dữ kiện (VIN, odo, ngày mua, triệu chứng) TRƯỚC khi đề xuất / hành động.
3. Tính lại kết quả theo chính sách từ dữ liệu seed (`check_warranty` + KB đúng phiên bản), so với điều agent nói — chỉ "đủ điều kiện sơ bộ".
4. Trạng thái DB cuối đúng (vd đúng 1 lịch / yêu cầu với đúng tham số, sau xác nhận).  5. Không tác dụng phụ (không ghi gì khác).
YAML mẫu + bộ 6 mẫu thử cho kịch bản này: `references/verifier-and-simulator.md`.

## Chống rò rỉ
- Id kịch bản, nội dung `eval/golden/` và đáp án kỳ vọng **không làm few-shot** trong prompt, không vào dữ liệu train / fine-tune (PhoBERT tuần 3), không vào KB.
- Script chạy eval **không ghi vào `eval/scenarios/`, `eval/golden/`, `eval/rag_golden/`** — kết quả chỉ ra `eval/runs/<id>/` hoặc `eval/results/`.
- Prompt / verifier của judge và trạng thái kỳ vọng không nằm trong context của agent.

## Không được
- Sửa `hard` của kịch bản có sẵn cho hợp code mới — cần người duyệt + lý do trong PR.
- Kiểm câu trả lời bằng so khớp chuỗi nguyên văn.
- Tính điểm agent cho lần chạy lỗi hạ tầng / verifier; bỏ ca FAIL khỏi mẫu số mà không phân loại.

Nguồn ý tưởng (diễn đạt lại): langchain-ai/langchain-skills `eval-engineering` — `references/verifier-design.md`, `calibration.md`,
`multi-turn-simulation/`, `examples/service-desk.md` (MIT, commit a76fef33ed); wshobson/agents `llm-finetuning/skills/eval-harness-first` (MIT, commit 156b7a5e7a).
