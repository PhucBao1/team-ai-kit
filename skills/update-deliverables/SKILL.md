---
name: update-deliverables
description: Cập nhật 10 deliverable Demo Day của BTC trong repo P-073 — WORKLOG.md hằng ngày, JOURNAL.md hằng tuần, README theo README_boilerplate, docs/architecture_diagram.md, eval/results/report.md, presentation/. Dùng khi hết ngày làm việc, cuối tuần, sau mỗi mốc demo, hoặc khi task nói worklog, journal, README, report, deliverable, pitch, video.
---

# Cập nhật deliverables Demo Day

Nguồn yêu cầu: `docs/guide/deliverables/checklist.md`, `docs/guide/chapter-09.md` (chỉ đọc). Chấm 5 tiêu chí × 20%: Product · System Design · UI/UX · DevOps · Code Quality.

| # | Deliverable | File | Khi nào | Người giữ |
|---|---|---|---|---|
| 1 | Source code | `src/` (+ `frontend/`, `eval/`) | liên tục | cả nhóm |
| 2 | README | `README.md` từ `README_boilerplate.md` | bản đầu 30/9, cập nhật mỗi mốc | D (B viết Problem/Solution) |
| 3 | Architecture | `docs/architecture_diagram.md` + `docs/architecture/` | khi đổi kiến trúc | D |
| 4 | AI logs | LangSmith (3 biến env) + hook log AI của BTC | từ 28/9 | A (LangSmith) · mỗi người (hook) |
| 5 | Live URL | Cloud Run (skill `deploy-live`) | `/health` 28/9 → bản đầy đủ 11/10 | D |
| 6 | Video demo ≤ 5 phút | link YouTube / Drive trong README + `presentation/README.md` | bản thô 30/9 · cuối 11/10 · chốt tuần 3 | C |
| 7 | Pitch deck 10 slide | `presentation/pitch_deck.pptx` (+ PDF) | nháp 11/10 · chốt tuần 3 | C (A viết nội dung) |
| 8 | Journal tuần | `JOURNAL.md` | Chủ nhật mỗi tuần | B |
| 9 | Worklog ngày | `WORKLOG.md` | mỗi ngày làm việc | mỗi người tự ghi dòng của mình, B gom cuối ngày |
| 10 | Eval evidence | `eval/results/report.md` | 30/9 · 4/10 · 11/10 · 18/10 | D (B lo user feedback) |

## WORKLOG (mỗi ngày, ≤ 2 phút)
Thêm bảng ngày theo đúng khung có sẵn: `| Member | Task | Status | Output | Time |` — Task ghi mã task (`A1.03 graph + 7 luật`), Output là link PR / kết quả.
Không ghi chung chung ("làm backend"). Cuối bảng 1 câu "Tổng kết ngày".

## JOURNAL (Chủ nhật)
Điền khung Week N: mục tiêu (lấy từ `../team-ai-kit/plan/PLAN.md`), đã hoàn thành (tick trong plan), khó khăn & giải pháp,
bài học (lấy từ ADR + `../team-ai-kit/docs/agent-lessons.md` — viết lại, không nhắc tên kit), kế hoạch tuần sau.

## README (khung `README_boilerplate.md`)
Problem → Solution → Demo (screenshot / GIF, Live URL, video) → Architecture (nhúng System Overview) → Tech stack (vì sao chọn) →
Setup (clone, `pip install -r requirements.txt`, `.env`, `make db`, `make run`) → API docs (`/docs`) → Evaluation (bảng số) → Team (ai làm gì).

## Eval report
Điền đúng bảng template: accuracy > 80%, latency < 3s, satisfaction > 4/5, coverage > 60% (`make test-cov`), user feedback 3–5 người,
+ mục thêm "So với baseline" (B0 không AI · B1 chatbot FAQ · B2 single agent) từ skill `run-eval-compare`. Số phải lấy từ lần chạy có ghi cấu hình.

## Không được
- Bịa số liệu, feedback, người dùng. Nhắc tới `team-ai-kit` trong deliverable.
