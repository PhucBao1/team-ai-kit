---
name: debug-failure
description: Xử lý test fail, eval fail, lỗi runtime hoặc agent trả lời sai — tái hiện, thu hẹp, tìm nguyên nhân gốc, sửa đúng chỗ mà không nới kỳ vọng. Dùng khi CI đỏ, make test/eval báo fail, agent hành xử sai trong demo, hoặc trace Langfuse cho thấy bước sai.
---

# Debug một lỗi

Luật gốc: **chưa biết nguyên nhân gốc thì chưa sửa.** Sửa triệu chứng = sẽ gặp lại.

## 1. Tái hiện
- Chạy đúng lệnh fail (`pytest tests/<file>::<test> -x -v`, `python -m eval.run --id <id> --k 3`, hoặc đúng lệnh CI BTC `ruff check src/ tests/`). Ghi seed, model, prompt version.
- Đọc hết thông báo lỗi + stack trace (dòng, file, mã lỗi) trước khi đoán. Xem thay đổi gần đây: `git diff`, `git log -5`, requirements, env.
- Không tái hiện được → chạy k=5; fail không đều = flaky → ghi nhận, vẫn phải tìm nguyên nhân (thường do thiếu ràng buộc hoặc thiếu timeout).
- **CI đỏ:** chỉ đọc phần lỗi — `gh run view <run-id> --log-failed` (hoặc log của đúng job lỗi), không đọc cả log. Rồi chạy lại đúng lệnh đó ở máy.

## 2. Thu hẹp
- Lỗi agent: mở trace (LangSmith, hoặc `GET /api/v1/trace/{trace_id}`) → tìm BƯỚC ĐẦU TIÊN sai: context thiếu? chọn nhầm tool? tham số sai? tool trả sai? claim_check bỏ lọt?
- Lỗi logic: viết unit test nhỏ nhất tái hiện ở tầng thấp nhất (`src/core` → `src/tools` → `src/agents`).
- **Lỗi xuyên tầng** (API → graph → tool → executor): tạm log dữ liệu VÀO / RA ở mỗi ranh giới (chỉ id, không PII), chạy 1 lần → biết tầng nào nhận đúng mà trả sai. Chỉ đào tầng đó. Gỡ log tạm trước khi PR.
- **So với code tương tự đang chạy đúng** (node / tool / test cùng loại): liệt kê MỌI khác biệt, kể cả nhỏ; đừng gạt "cái đó không ảnh hưởng".

## 3. Giả thuyết — một cái một lúc
1. Viết ra: "Tôi nghĩ **X** là gốc vì **Y**." Cụ thể, không mơ hồ.
2. Thay đổi NHỎ NHẤT để kiểm đúng giả thuyết đó, một biến một lần.
3. Sai → **hoàn tác** thay đổi đó rồi lập giả thuyết mới. Không chồng fix lên fix.
4. **Đã thử 3 cách sửa mà không được → DỪNG.** Mỗi lần sửa lại lộ lỗi mới ở chỗ khác = có thể sai thiết kế. Nghi vấn thiết kế, hỏi người sở hữu module (AGENTS.md §7) trước khi thử cách thứ 4.

### Lý do biện hộ phải bác bỏ (chưa có bằng chứng thì không được dùng)
| Câu hay nói | Phải có gì mới được nói |
|---|---|
| "Chắc do môi trường / máy" | Cùng commit, chạy chỗ khác thì xanh; chỉ ra biến env / phiên bản khác nhau |
| "Flaky thôi" | k=5 cho kết quả lẫn lộn + chỉ ra nguồn bất định (thời gian, thứ tự, mạng, LLM) |
| "Test sai, code đúng" | Trích spec/card/contract chứng minh kỳ vọng của test trái với yêu cầu → hỏi người trước khi sửa test |
| "Do LLM, không sửa được" | Trace cho thấy context + tool đúng mà model vẫn sai, ở nhiều lần chạy |
| "Lỗi có sẵn, không phải tôi" | Chạy trên `develop` (trước diff) cũng đỏ y hệt |
| "Thấy rõ rồi, sửa luôn" | Đã tái hiện + giả thuyết được kiểm ở bước 3 |

## 4. Sửa gốc, đúng tầng
| Nguyên nhân | Sửa ở |
|---|---|
| Luật nghiệp vụ sai | `src/core/` + test |
| Tool trả thiếu/sai dữ liệu | `src/agents/tools/` hoặc `src/tools/` + test + contract nếu cần |
| Agent chọn sai / hiểu sai | mô tả tool, prompt, hoặc schema output — kèm eval trước/sau |
| Guardrail bỏ lọt | `src/core/validator.py` / `claim_check.py` (repo) · `../team-ai-kit/guardrails/guardrails.py` (luật của đội) |

- Test tái hiện viết TRƯỚC bản sửa. Một bản sửa cho một nguyên nhân; không "tiện thể" refactor.
- **Chứng minh test bắt được lỗi:** tạm bỏ bản sửa (`git stash` phần code) → test ĐỎ → khôi phục → XANH. Không đỏ khi bỏ sửa = test không tái hiện lỗi.

## Playwright / e2e
- KHÔNG thêm `waitForTimeout`, `sleep`, `waitForLoadState('networkidle')` để "sửa" — chờ điều kiện cụ thể (`expect(locator).toBeVisible()`, chờ response API).
- KHÔNG làm yếu assertion (bỏ kiểm text, đổi `toHaveText` → `toBeVisible`, nới selector) cho xanh.
- Chưa rõ app hỏng hay test đã cũ so với UI → hỏi người sở hữu (C cho `frontend/`), không tự đoán.
- Lỗi đã biết, chưa sửa trong PR này → `test.fixme(...)` kèm link issue/task, không `skip` im lặng.

## Không được
- Sửa kỳ vọng `hard`, file golden, hạ ngưỡng, thêm `skip`/`xfail` để CI xanh.
- Thêm câu "nếu gặp trường hợp X thì…" vào prompt cho riêng một kịch bản (overfit) — tìm quy luật chung.

## 5. Chốt
- Test tái hiện giờ xanh (và đã thấy đỏ khi bỏ sửa); `pytest tests/` xanh; chạy lại kịch bản eval liên quan. Ghi nguyên nhân 1–2 dòng trong PR.
- Lỗi do AI coding agent gây ra và lặp lại → ghi `../team-ai-kit/docs/agent-lessons.md`.

---
Ý tưởng tham khảo (diễn đạt lại): obra/superpowers (MIT) — systematic-debugging, verification-before-completion; trailofbits/skills (CC BY-SA 4.0) — fp-check (chỉ rút ý); openai/skills — gh-fix-ci.
