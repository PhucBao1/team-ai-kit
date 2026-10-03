# Kế hoạch tổng — EV CX Agent (repo P-073)

File này là **overview**: mục tiêu, mốc, ai gánh gì, phụ thuộc. Task nhỏ để tick nằm ở file của từng người:
[A — Agent/AI](A-agent.md) · [B — Data & Tools](B-data-tools.md) · [C — Frontend & UX](C-frontend.md) · [D — Platform & Quality](D-platform.md).
Xem tiến độ: `python3 plan/progress.py` (đếm task đã tick theo người / tuần).

**Cách làm một task:** mở card `tasks/<mã>.md` (mục tiêu · file · test phải viết · lệnh kiểm · prompt cho AI agent) → làm → `python3 ../team-ai-kit/plan/verify.py <mã>` → **chỉ tick khi ĐẠT**.
Card: tuần 1 chi tiết (62), tuần 2–3 bản nháp (78) — soát tối Chủ nhật trước tuần. Buổi tập pitch: mỗi người ghi file riêng `presentation/rehearsals/<A|B|C|D>.md`.
Kịch bản demo cố định: [demo MVP 30/9](demo-mvp.md) · [demo đủ phạm vi 11/10](demo-full.md) — mọi task tuần 1 phải phục vụ một bước trong đó.

## Định hướng sản phẩm — Proactive AI Customer Care (cập nhật)

AI chủ động phát hiện, điều tra và xử lý customer friction đang hình thành **trước khi khách phải hỏi**: detector tất định (0 token) → arbitration → agent chọn lọc → validator → Executor → **xác minh**. *LLM là tầng leo thang, không phải tầng xử lý event.* Appointment **không** phải điểm bắt đầu — chỉ là hành động xuôi dòng (UC3). Chi tiết sáu use case: `docs/proposal/usecases.md` + `ucs1…ucs6-*.md`.

| Mức Final MVP | Use case |
|---|---|
| **FULL** | UC1 Preemptive Service Friction Rescue (flagship) |
| **Demo-ready** | UC2 Charging Friction Prevention · UC3 Service Readiness / Intervention Orchestration |
| **Spec + kịch bản khung** (chưa build) | UC4 Billing Mismatch · UC5 Claim Follow-up · UC6 Recurrence |

**Đổi số UC (card viết trước 3/10 dùng số cũ):** UC1 cũ *Service Appointment Rescue* → bộ máy nằm ở **UC3** (nhánh lập lại), flagship là **UC1 mới** · UC2 cũ (lời hứa báo giá) → bỏ khỏi sáu UC · UC3 cũ (kẹt ở trạm sạc) → **UC2** · UC4 giữ · UC5 cũ (comeback) → **UC6** · UC6 cũ (claim) → **UC5**. Các card dưới đây đã đổi nhãn; chưa có card cho engine chăm sóc chủ động (epic E15–E17 ở spec §44).

### Phạm vi build — lead chốt 03/10 ("UC1 làm gọn")

**Proactive là cửa vào, hội thoại đa bước là thân bài.** Lõi đề BTC (FAQ RAG có trích dẫn, phân loại ý định, 4 workflow
tool-calling, xác nhận trước khi ghi, handover kèm tóm tắt, đo lường) **không giảm**; UC1 là cú mở màn của demo.
Chi tiết, so sánh hãng nước ngoài, sai sót nghiệp vụ và nguồn: [`docs/research/2026-10-03-nghiep-vu-vinfast.md`](../docs/research/2026-10-03-nghiep-vu-vinfast.md).

| Hạng mục | Quyết định | Lý do |
|---|---|---|
| UC1: detector lặp ≥ 3 lần / 14 ngày + đường tất định | **Làm** (B2.17, A2.18, C2.14) | Dùng lại T0 / Scheduler / executor đã có |
| "InterventionProposal 8 câu hỏi" | **Bản nhẹ:** schema có `evidence_refs`, điền tất định, LLM chỉ viết câu | Luật đã trả lời phần lớn; LLM tự đánh giá mức khẩn dễ suy diễn; spec UC1: "rule đủ → không gọi Agent" |
| UC2 trạm sạc | **Hoãn tuần 3** (B2.14 giữ, làm nếu dư giờ) | Dữ liệu + tool + detector mới; không thuộc 4 workflow đề chấm |
| UC4 / UC5 / UC6 | **Chỉ pitch** (UC6 một phần qua B2.15) | Mỗi UC là miền dữ liệu mới |
| Sai sót nghiệp vụ (lịch bảo dưỡng ô tô, FOTA khi pin thấp, consent, SLA, mẫu an toàn) | **Lead sửa** (PR P-073 `a/w2-business-fixes`) | Xem research §1 |

**Card mới 03/10** (không sửa card cũ; việc chồng lên card đang có ghi ở mục "Bổ sung 3/10" cuối card D2.01, A2.13):
[A2.18](tasks/A2.18.md) · [A2.19](tasks/A2.19.md) · [B2.17](tasks/B2.17.md) · [B2.18](tasks/B2.18.md) · [B2.19](tasks/B2.19.md) ·
[C2.14](tasks/C2.14.md) · [D2.15](tasks/D2.15.md) · [D2.16](tasks/D2.16.md). Kịch bản demo 11/10: [7 màn](demo-full.md).

> Điền tên thật: A = ______ · B = ______ · C = ______ · D = ______ · Demo Day BTC = ______ (lộ trình sách BTC ghi 6 tuần — hỏi BTC).

## 1. Mốc

| Mốc | Ngày | Cổng (phải đạt) |
|---|---|---|
| Khởi động | **T2 28/9** | Mỗi người: hook log AI chạy · `install.sh` xong · PR bootstrap merge · `develop` tạo · Live URL `/health` |
| **Demo MVP** | **T4 30/9** | Chat tra xe + bảo hành sơ bộ có trích dẫn · UC1 → UC3: tín hiệu lặp → agent chủ động → khách xác nhận → đặt / đổi lịch (UC3) · 1 tin proactive · handoff có card · deploy · video dự phòng |
| Cổng tuần 1 | CN 4/10 | Tách multi-agent · 6 quyết định (UC1 → UC3) · Postgres + checkpoint · 40 kịch bản eval tự động, 0 vi phạm "hard" · coverage ≥ 60% · RAG có phiên bản |
| **Demo đầy đủ** | **CN 11/10** | Đủ 4 workflow PRD (tra đơn/việc, đặt lịch, đổi/trả + ticket, cập nhật thông tin) + proactive + copilot · 150 kịch bản + baseline B0–B2 · 5 người dùng thử · dark mode · pitch nháp |
| Chốt | CN 18/10 | Chỉ cải thiện (PhoBERT triage, tối ưu, ablation) · **10/10 deliverables hoàn chỉnh** · tập pitch ≥ 3 lần |
| Demo Day | ___ | URL sống tới Demo Day + 7 ngày (min-instances 1) |

Nếu Demo Day xa hơn 18/10: tuần 4+ **không mở thêm phạm vi** — user test vòng 2, sửa theo feedback, luyện pitch, giữ URL (mục 7).

## 2. Chia vai và tải

Hai người **gánh chính**: A và D — giữ đường găng (graph chính, xác nhận, executor). Hai người **vừa**: B và C. **Cả 4 người đều có một phần agent / platform và một phần deliverable** — ai ốm / trễ vẫn có người hiểu để đỡ, và ai cũng trả lời được câu hỏi kỹ thuật khi pitch.

| Giờ | Tuần 1 | Tuần 2 | Tuần 3 | Tổng |
|---|---|---|---|---|
| **A** | 38,5 | 35 | 30 | **103,5** |
| **D** | 39 | 38,5 | 21 | **98,5** |
| C | 29,5 | 32 | 24 | 85,5 |
| B | 29,5 | 30,5 | 22 | 82 |

### Đổi việc hai chiều (29/9)

**A / D → B / C** (phần agent / platform không nằm trên đường găng, là module riêng có chữ ký rõ):

| Task | Từ → sang | Vì sao hợp |
|---|---|---|
| B2.14 subgraph UC2 trạm sạc | A → B | B đã viết `find_chargers` + dữ liệu SoC |
| B2.15 subgraph UC6 xác minh sau sửa | A → B | B nắm detector + đồng hồ giả lập |
| B3.08 PhoBERT triage | A → B | B làm dataset `triage_vi_v1` |
| C2.13 node gợi ý upsell | A → C | C làm cả node lẫn thẻ gợi ý → hiểu trọn luồng |
| B2.16 Pub/Sub + worker detector | D → B | Worker chạy detector của B |
| B3.09 MLflow + drift | D → B | Đi liền PhoBERT |
| C3.08 giám sát uptime + cảnh báo | D → C | DevOps nhẹ |
| C1.14 Cloud Build · C1.15 kiểm tay UI · B1.12 20 kịch bản eval · B1.13 README bản đầu | A/D → B/C | Giữ từ lần chia trước |

**B / C → A / D** (việc hợp tay người nhận):

| Task | Từ → sang | Vì sao hợp |
|---|---|---|
| A2.15 reranker + `rag_golden` 50 câu | B → A | Chất lượng tìm kiếm quyết định PolicyQA của A |
| A1.16 sơ đồ Agent Flow | C → A | A hiểu graph nhất |
| A2.09 40 kịch bản hội thoại | B → A | A biết agent hay sai chỗ nào |
| A3.10 user test vòng 2 · A3.11 lỗi tiêm demo cuối | B → A | Kiểm chính các sửa của A3.05; demo do A dẫn |
| D1.21 report bản 0 + báo cáo eval tuần 1 | B → D | D viết runner eval |
| D2.09 README đầy đủ · D3.09 soát README / pitch / report | B → D | D giữ Setup, API, kiến trúc |
| D2.07 load test (gộp lại với chaos) | C → D | Cùng file `src/main.py`, `eval/load/` |
| D2.14 CORS + deploy frontend | C → D | Đụng `src/main.py`, `src/api/` |

**Giữ không xung đột khi B, C làm phần agent:** B, C viết **module riêng** (`src/agents/subgraphs/charging.py`, `post_repair.py`, `src/agents/nodes/offer.py`) với chữ ký `build_*_subgraph()` / `offer_node(state)`. Chỉ A sửa `graph.py` và `state.py` — task **A2.17** (1h) nối cả 3 vào graph sau khi review PR. Upsell tuần 2 vẫn chia đều: B2.12 · D2.13 · C2.13 · C2.11. Bỏ: gửi câu hỏi BTC.

**Không xung đột file:** mỗi file chỉ một người sửa trong một tuần (trừ `WORKLOG.md` — mỗi người thêm dòng của mình). Kiểm: `python3 ../team-ai-kit/plan/check_conflicts.py` → phải "0 xung đột". Card mới / sửa card → chạy lại.

Bảng dưới là vùng chính; từng file cụ thể nằm ở mục **File** của card — `check_conflicts.py` đọc đúng mục đó. File kết quả trong `eval/results/` thuộc người tạo ra nó (vd. `latency.md` của A, `rag.md` của B, `load.md` của D).

| Ai | Được sửa |
|---|---|
| A | `src/agents/` (graph, state, nodes trừ `offer.py`, prompts trừ `offer_vi.md`), `src/services/`, `src/config.py` (tuần 3), `src/kb/retriever.py` + `src/kb/docs/{faq,sop}/` + `eval/golden/` (tuần 2), `src/sim/scenarios/` + `faults/` (tuần 3), `docs/architecture/` (tuần 1, 3), `eval/scenarios/{switch,uc2,chat,redteam}/` |
| B | `src/sim/ detect/ kb/` (trừ phần của A), `src/agents/tools/`, `src/agents/subgraphs/{charging,post_repair}.py`, `src/ml/` (train, registry, drift), `infra/pubsub.sh`, `contracts/fixtures/`, `README.md` (tuần 1), `JOURNAL.md`, `eval/scenarios/{uc1,upsell}/`, `eval/rag_eval.py` |
| C | `frontend/`, `src/agents/nodes/offer.py` + `prompts/offer_vi.md` (tuần 2), Cloud Build, `docs/images/`, `presentation/` pitch deck + video (nội dung: A `content.md` · B `product.md` · D `qa.md`), `eval/usertest/{protocol,participants,ui-notes}.md` |
| D | `src/core/ executor/ tools/ api/ db/`, `src/main.py`, `contracts/*.yaml`, `migrations/`, `docs/adr/`, `eval/run.py`, `eval/suites.yaml`, `eval/load/`, `eval/results/report.md`, `README.md` (từ tuần 2) |

| | Vai | Sở hữu (thư mục) | Deliverable BTC giữ | Tải |
|---|---|---|---|---|
| **A** | Agent / AI lead | graph + state + node chính, `src/services/`, prompt, reranker (tuần 2) | #4 AI logs (LangSmith) · nội dung pitch · #3 sơ đồ Agent Flow | **Nặng** |
| **D** | Tech lead · Platform & Quality | `src/core/ executor/ tools/ api/ db/`, `src/main.py`, `migrations/`, `contracts/`, deploy, `eval/` runner + load | #1 · #2 README (từ tuần 2) · #3 Architecture · #5 Live URL · #10 Eval report · merge `develop → main` | **Nặng** |
| **B** | Data & Tools + agent/ML phụ | `src/sim/ detect/ kb/`, `src/agents/tools/`, subgraph `charging` / `post_repair`, Pub/Sub worker, `src/ml/` | #2 README bản đầu · #8 JOURNAL · #9 WORKLOG (gom) · user feedback vòng 1 trong #10 · nội dung Product | Vừa |
| **C** | Frontend & UX + agent/DevOps phụ | `frontend/`, node `offer`, Cloud Build, giám sát uptime | #6 Video · #7 Pitch deck (thiết kế) · screenshot / GIF | Vừa |

Đường găng MVP: A1.02 contracts → B1.03 seed → B1.05 find_options → D1.08 tool ghi → D1.09 token + executor → A1.06 luồng xác nhận → A1.08 handoff.
Người giữ đường găng báo tiến độ trong standup; trễ > 2 giờ → cả nhóm gỡ.

## 3. Làm song song, không chờ nhau

Nguyên tắc: **hợp đồng trước, mock thay người khác**. Hợp đồng đã có trong PR bootstrap: `contracts/tools.yaml`, `api.yaml`, `events.yaml`. Sáng 28/9 cả nhóm duyệt 1 lần rồi đóng băng (đổi sau = ADR).

| Ai cần | Của ai | Trong lúc chờ dùng |
|---|---|---|
| C (UI) | API của D | Mock JSON / SSE giả sinh từ `contracts/api.yaml` trong `frontend/src/mocks/` |
| A (agent) | Tool đọc của B | Stub trong `tests/` + hàm giả trả dữ liệu mẫu đúng `contracts/tools.yaml` |
| A (xác nhận) | Executor của D | `executor.run` giả trả `ConfirmResult` thành công / lỗi |
| D (tool ghi, validator) | Thế giới giả lập của B | Interface `src/sim/world.py` B chốt **trước 11:00 28/9** (B1.02); trước đó D dùng dict trong test |
| B (check_warranty) | `src/core/warranty.py` của D | Gọi hàm theo chữ ký đã chốt; test B dùng kết quả giả |
| D (eval runner) | Kịch bản của A, B | Tự viết 5 kịch bản mẫu, A/B thêm dần |
| C (console) | HandoffCard của A | Schema `HandoffCard` trong `contracts/api.yaml` |
| A (A2.17 nối graph) | Subgraph của B (B2.14, B2.15), node của C (C2.13) | B, C viết module độc lập + test riêng; A nối khi PR merge — chưa có thì graph chạy như cũ |
| B, C (phần agent) | `state.py` của A | Chỉ đọc state theo `src/agents/state.py`; cần trường mới → nhờ A thêm (A2.17) |

Mỗi người chỉ sửa thư mục mình sở hữu. File dùng chung (`contracts/`, `requirements.txt`, `src/config.py`, `tests/conftest.py`, `src/models/schemas.py`, `src/agents/state.py`) → báo trong nhóm trước, PR nhỏ riêng.

## 4. Nhịp làm việc

- **09:00 standup 15'**: hôm qua xong gì (tick), hôm nay làm gì, đang chờ ai. Chạy `python3 plan/progress.py`.
- **17:30 demo nội bộ 15'**: mỗi người mở PR / màn hình chạy được. Ghi `WORKLOG.md` (mỗi người 1 dòng/task, B gom).
- **Chủ nhật**: B viết `JOURNAL.md` tuần; D chạy eval đầy đủ, cập nhật `eval/results/report.md`; cả nhóm xem cổng tuần.
- PR vào `develop`, người khác review trong 4 giờ (cặp review: A ↔ D, B ↔ C). `develop → main` ở mỗi mốc bởi D.
- Tick task: mỗi người chỉ sửa file của mình trong `plan/` (không xung đột), commit vào repo team-ai-kit.

## 5. Deliverables BTC — ai, khi nào

| # | Deliverable | Người giữ | 30/9 | 4/10 | 11/10 | 18/10 |
|---|---|---|---|---|---|---|
| 1 | Source code `src/` | D | ✔ MVP | ✔ | ✔ | ✔ |
| 2 | README (boilerplate) | B bản đầu (tuần 1) · D từ tuần 2 | bản đầu | Setup đủ | + screenshot, số eval | chốt |
| 3 | `docs/architecture_diagram.md` | D | ✔ (có sẵn) | cập nhật | cập nhật | chốt |
| 4 | AI logs: LangSmith + hook log | A · mọi người | ✔ | ✔ | ✔ | ✔ |
| 5 | Live URL | D | `/health` 28/9, MVP 30/9 | ✔ | bản đầy đủ | ổn định |
| 6 | Video ≤ 5' | C | video dự phòng | — | bản 1 | chốt |
| 7 | Pitch deck 10 slide | C (+A nội dung, B Product) | — | outline | nháp | chốt + tập |
| 8 | `JOURNAL.md` | B | — | tuần 1 | tuần 2 | tuần 3 |
| 9 | `WORKLOG.md` | mọi người, B gom | hằng ngày | | | |
| 10 | `eval/results/report.md` | D (B gửi feedback vòng 1, A gửi vòng 2) | bản 0 | 40 kịch bản | 150 + baseline + 5 user | chốt |

Chấm 5 tiêu chí × 20%: Product · System Design · **UI/UX** · **DevOps** · Code Quality. UI/UX và DevOps = 40% → C và D có task riêng cho từng tiêu chí.

## 6. Nếu trễ — cắt theo thứ tự (không cắt deliverable)

1. Upsell chỉ giữ gợi ý + "Không quan tâm" (bỏ báo giá `create_quote`) · 2. MCP servers (giữ hàm Python) · 3. copilot NV · 4. VED/ACN (dùng dữ liệu tổng hợp) ·
5. Tuần 3: GraphRAG, Temporal, MLflow (giữ PhoBERT nếu kịp, không thì giữ cascade LLM).
**Không bao giờ cắt**: luật chặn upsell (bực / khiếu nại / an toàn), xác nhận trước khi ghi, trích dẫn nguồn, handoff có card, test + CI xanh, 10 deliverables.

## 7. Còn thiếu / cần chốt

- [ ] Tên thật A/B/C/D và ngày Demo Day (hỏi BTC; lộ trình sách ghi 6 tuần).
- [ ] Trả lời BTC: sửa `.github/`/`docs/` được không · vị trí journal / pitch / architecture · Langfuse thay LangSmith được không.
- [x] LLM cho MVP: **OpenAI `gpt-4o-mini`** (`LLM_PROVIDER=openai`, đúng template BTC). Gemini Vertex để dành tuần 2 nếu có GCP billing — đổi bằng biến env, không sửa code.
- [ ] Ai giữ key OpenAI + trần ngân sách/tháng (đặt usage limit trên dashboard OpenAI).
- [ ] GCP project + billing (D, 28/9) · tài khoản LangSmith (A) · `AI_LOG_API_KEY` từng người (dashboard Phoenix).
- [ ] 5 người dùng thử (chủ xe / người lái thật) + lịch test tuần 2 (B).
- [ ] Buffer: mỗi tuần kế hoạch đã chừa ~15% cho sửa lỗi; nếu ai vắng > 1 ngày, người cùng cặp review nhận task đường găng.
