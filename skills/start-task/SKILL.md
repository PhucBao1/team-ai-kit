---
name: start-task
description: Quy trình chuẩn để bắt đầu và hoàn thành MỌI task code trong repo P-073 — đọc task trong plan, đọc đúng mục spec, lập kế hoạch ngắn, làm lát mỏng, kiểm như CI BTC, mở PR nhỏ, tick task và ghi WORKLOG. Dùng khi nhận một task (A1.03, D2.05…), issue, hoặc yêu cầu "làm tính năng X".
---

# Bắt đầu một task

## 1. Hiểu (≤ 10 phút)
- Mở **card** `../team-ai-kit/plan/tasks/<mã>.md` (mục tiêu, file, Interfaces, đầu vào→đầu ra theo fixture, test phải viết, lệnh kiểm). Card còn dòng "Bản nháp" → soát bằng skill `write-task-card` trước.
- Chạy `python3 ../team-ai-kit/plan/verify.py <mã>` một lần để thấy nó CHƯA ĐẠT — đó là đích cần tới.
- Đọc mục spec được nhắc tới qua `../team-ai-kit/docs/spec/README.md` (chỉ mục đó) + `AGENTS.md` của thư mục sẽ sửa.
- Đụng `contracts/` hoặc thư mục của người khác? → báo nhóm trước. Chờ phần của người khác → dùng mock / hợp đồng, KHÔNG chờ.
- Nghiệp vụ chưa rõ (bảo hành, SOP, câu chữ gửi khách) → hỏi người, không đoán.

## 2. Kế hoạch (PR description, ≤ 10 dòng)
Mục tiêu 1 câu · file sẽ sửa · test / kịch bản eval sẽ thêm · cách kiểm tra xong · rủi ro. Task > ~300 dòng → tách PR.

## 3. Làm theo lát mỏng
- Nhánh từ `develop`: `<tên>/<mã-task>-<mô-tả>` (vd. `b/B1.04-seed-world`). Nhiều AI agent song song → `git worktree add ../wt-<mã> -b <nhánh>`.
- **Worktree mới → chạy `pytest tests/` ngay làm baseline.** Baseline đỏ → báo người (test nào, lỗi gì) TRƯỚC khi làm; không thì mọi lỗi sau đều không biết của ai.
- Test trước hoặc cùng lúc → code tối thiểu cho xanh → dọn. Việc có skill riêng → dùng skill đó.
- Code: type hints mọi hàm, docstring hàm public, hàm ≤ 30 dòng, không `print`, không `except:` trần.
- Lệch khỏi card (đổi file, chữ ký, cách làm) → ghi 1 dòng trong PR: `Quyết định: … vì … · rủi ro nếu sai: …`.

### Viết test (mỗi test phải bắt được một lỗi thật)
- **Trước khi viết thân test:** nêu được thay đổi code nào sẽ làm nó fail. Không nêu được → test vô ích, đổi sang hành vi quan sát được.
- **Kỳ vọng là literal hoặc fixture** (`contracts/fixtures/demo_world.yaml`), tự tính tay. Không tính kỳ vọng bằng chính hàm đang test hay helper của nó.
- **Không assert vào mock** (mock có mặt ≠ code đúng). Chỉ mock tầng chậm/ngoài (LLM, HTTP, MCP); assert kết quả hoặc tác dụng phụ thật.
- **Thấy test FAIL đúng lý do trước khi code:** chạy test mới → đỏ vì THIẾU tính năng (assert sai giá trị / chưa có hành vi), KHÔNG phải `ImportError`/`NameError`/lỗi fixture. Test pass ngay từ đầu = test sai → sửa test.
- Tên: `test_<đơn vị>_<tình huống>_<kỳ vọng>` — vd. `test_warranty_odometer_over_limit_returns_expired`. 1 hành vi / test.
- Luôn có ít nhất 1 test đường lỗi (input sai, tool trả `ToolError`, timeout).
- Retry / idempotency: `mock.side_effect = [err, err, ok]` rồi assert kết quả + `mock.call_count == 3`; gọi lại cùng idempotency key → assert chỉ ghi 1 lần.

## 4. Kiểm trước PR (đúng như CI BTC + của đội)
- `ruff check src/ tests/` · `ruff format src/ tests/` · `pytest tests/ -v` · `make test-cov` (≥ 60%, không tụt).
- `make -f ../team-ai-kit/kit.mk check` (contracts, sơ đồ, guardrails).
- Chạm agent / prompt / KB → chạy kịch bản eval liên quan (`python -m eval.run --id <id> --k 3` khi đã có runner).
- Tự review bằng skill `review-pr` trên diff của mình.

### Bằng chứng trước khi nói "xong"
- **Không tuyên bố XONG / ĐẠT / "test xanh" nếu chưa chạy lại lệnh kiểm TRONG LƯỢT NÀY và đọc output**: số test fail, số lỗi ruff, exit code. Ghi con số vào báo cáo (vd. `pytest: 42 passed, 0 failed`).
- "Chắc là pass", "lẽ ra chạy được", "lần trước xanh" = CHƯA KIỂM. Ruff xanh ≠ test xanh; test xanh ≠ đủ yêu cầu card (đối chiếu lại từng dòng card).
- Sub-agent / AI khác báo "xong" → tự xem `git diff` (đúng file trong card? có sửa thừa?) và tự chạy `python3 ../team-ai-kit/plan/verify.py <mã>`. Không tin báo cáo.

## 5. PR & ghi nhận
- PR vào `develop`, title Conventional Commit (`feat(core): …`). Không nhắc tới team-ai-kit trong code / commit.
- `python3 ../team-ai-kit/plan/verify.py <mã>` ĐẠT + mục "Kiểm bằng tay" được người review xác nhận.
- Merge xong: tick `[x]` task trong `plan/<tên>.md` (commit ở repo team-ai-kit) và thêm 1 dòng `WORKLOG.md` (repo P-073): ai · task · kết quả · giờ.
- AI mắc lỗi lặp lại → ghi `../team-ai-kit/docs/agent-lessons.md`.

---
Ý tưởng tham khảo (diễn đạt lại): obra/superpowers (MIT) — test-driven-development, verification-before-completion, using-git-worktrees.
