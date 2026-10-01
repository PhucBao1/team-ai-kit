---
name: inject-fault
description: Thêm một loại lỗi ngầm có nhãn (T1–T5) vào thế giới giả lập để detector và agent phát hiện, kèm kịch bản eval. Dùng khi task nói thêm lỗi giả lập, fault injection, loại silent failure mới, hoặc sửa src/sim/faults/.
---

# Tiêm lỗi có nhãn vào thế giới giả lập

Spec: `../team-ai-kit/docs/proposal/usecases.md` (5 dạng lỗi), `../team-ai-kit/docs/proposal/11-data.md`, `../team-ai-kit/docs/spec/09-events.md`, `28-ds.md` phần B · hợp đồng `contracts/events.yaml`.
Loại lỗi: T1 lệch trạng thái giữa hệ thống · T2 lời hứa bị quên · T3 rơi quyền sở hữu (không ai phụ trách) · T4 đóng sớm (đóng việc khi chưa xong) · T5 trùng lặp.

## Bước
1. Copy `templates/fault.yaml` vào `src/sim/faults/<loại>_<tên>.yaml`: điều kiện kích hoạt, sự kiện phát ra, **nhãn đáp án**
   (có phải lỗi thật không, hạn cứu, hành động đúng).
2. Mỗi loại lỗi cần cả ca **dương tính** và ca **âm tính gây nhiễu** (trông giống lỗi nhưng không phải) — để đo precision.
3. Neo tham số vào dữ liệu công khai khi có (VED cho hành trình, ACN cho phiên sạc); ghi nguồn trong file.
4. Thêm rule L0 trong `src/detect/rules.py` nếu là loại mới (test ở `tests/test_detect/`); sự kiện mới → thêm vào `contracts/events.yaml` (ADR). Rule tất định, không gọi LLM.
5. Thêm ≥ 2 kịch bản eval (skill `add-eval-scenario`): một ca cứu được, một ca âm tính (agent KHÔNG được làm phiền khách).
6. `python -m src.sim.seed --reset && python -m eval.detector_eval` → xem precision/recall theo loại; cập nhật `eval/golden/faults_labeled` qua PR có người duyệt.
