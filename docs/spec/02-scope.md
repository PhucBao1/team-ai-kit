# 02 · Phạm vi & mốc — Hai tuần làm đủ, tuần 3 chỉ cải thiện

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

## Ma trận nghiệm thu hiện hành (chốt 06/10 — thay các bảng phạm vi bên dưới)

Nguồn duy nhất để nghiệm thu demo 11/10. Bảng mốc và "Đủ phạm vi" bên dưới giữ làm **lịch sử** (viết trước 03/10, còn UC2 sạc, upsell, PhoBERT, Temporal…).

| Nhóm | Phải chạy được 11/10 | Card | Đo / kiểm |
| --- | --- | --- | --- |
| Yêu cầu bắt buộc của đề | Hội thoại nhiều bước giữ ngữ cảnh · KB có trích dẫn đúng phiên bản · 4 workflow tool (tra việc/đơn, đặt/đổi lịch, đổi/trả + ticket, đổi thông tin) · xác nhận trước khi ghi · chuyển người kèm thẻ | đã có + A2.20, A2.21 | claim_check sạch · ghi không xác nhận = 0 · eval pass / partial / fail (A2.32) |
| Đúng đối tượng | Tin chủ động xử lý đúng xe phát sự kiện · không phát lại câu cũ · khách khác không nhận kết quả / đơn của người khác | A2.28, A2.29 | test nhiều xe nhiều vai trò · test replay khác khách · test đơn người khác |
| Chuỗi chăm sóc chủ động | Phát hiện → báo (qua một cửa kiểm giờ yên tĩnh / ngân sách) → lịch kiểm tra → điều kiện lịch đổi → chuyển người trung thực → quá hạn chưa nhận → sau sửa có điều kiện dữ liệu → khách báo còn triệu chứng | A2.18, A2.22, A2.23, A2.25, A2.26, A2.27, A2.31 | hứa sai = 0 · đóng sai = 0 · quá hạn được phát hiện · handoff được nhận vs chỉ gửi |
| Giao diện live | Không lẫn dữ liệu khi đổi khách · một phương án / lượt · test frontend xanh | A2.30 | `npm test`, `npm run typecheck` |
| Chứng minh phần nào cần AI | Cùng bộ kịch bản: rule + mẫu cố định vs rule + agent AI | A2.32 | `eval/results/compare_rule_vs_ai.md` |
| Chạy thật | Live URL `/health` 200 sau deploy · không trả dữ liệu mẫu ngoài development | A2.33 | smoke container bằng `appuser` |
| **Không nghiệm thu 11/10** (roadmap) | UC2 sạc · upsell / bán kèm · giao nhận xe · xưởng chưa tái hiện lỗi · đã nhận nhưng không tiến triển · gửi lại tin bị hoãn · duyệt phạm vi sửa / chi phí · kiểm lại xưởng định kỳ · PhoBERT / Temporal | — | — |

## Giới hạn chế độ demo (ghi nguyên văn vào README / SECURITY của P-073 — A2.33)

Bản demo chạy **dữ liệu giả lập, một process, không dành cho người dùng thật**. Các giới hạn đã biết, chưa xử lý trước Demo Day:

1. **Danh tính và phân quyền (#19, #21):** API nhận `customer_id` / session do client gửi; chưa có xác thực, chưa phân quyền khách / nhân viên; endpoint điều khiển giả lập (`/events/inject`, `/clock/advance`, `/reset`) mở. Bản public phải lấy danh tính từ xác thực, gắn session với chủ sở hữu và khoá endpoint giả lập.
2. **Quyền đọc qua MCP (#20):** chỉ tool tra việc kiểm chủ sở hữu; tool đọc theo VIN / khách khác chưa kiểm ở cửa gọi tool.
3. **Audit (#22):** audit còn lưu nội dung khách nguyên văn (vd. tóm tắt ticket); bản public phải lọc trường nhạy cảm, chỉ giữ ID / hash.
4. **Giao tin (#23):** outbox đánh dấu `sent` khi đưa vào SSE, chưa có ack / replay khi mất kết nối — **không** phải "giao đúng một lần".
5. **Lưu trữ (#24):** việc của khách, handoff, outbox, idempotency, checkpoint đang trong RAM; restart / `/reset` mất dữ liệu. Postgres checkpointer có helper nhưng chưa nối (D1.14).
6. **Rate limit (#27):** khoá theo header `X-Customer-Id` do client gửi; đổi header là né được. Bản public dùng danh tính đã xác thực + giới hạn theo nguồn.
7. **Số liệu và ngưỡng:** mã lỗi (`BATT-COOL-01`…), ngưỡng phát hiện, ngưỡng dữ liệu sau sửa (14 ngày / 50 km / 72 giờ) là **giả lập**; số liệu khảo sát lấy từ InsightAsia 2025 công khai (n=762).

## Lịch sử — phạm vi viết trước 03/10 (không dùng để nghiệm thu)

| Mốc | Ngày | Phải có |
| --- | --- | --- |
| MVP | Thứ Tư 30/9 | Chat nhiều bước (tín hiệu lặp → agent chủ động nhắn → bảo hành → đặt lịch có xác nhận, UC1 → UC3) · 1 sự kiện "linh kiện bị điều đi" → UC3 lập lại 2 phương án · chuyển người với handoff card · "Việc của tôi" cơ bản · demo panel (bơm sự kiện, tua thời gian) |
| Tuần 1 | 28/9 → 4/10 | MVP + engine chăm sóc chủ động (detector registry · arbitration · context builder · Agent chọn lọc · verifier) + đủ 6 quyết định (UC1 → UC3) · tách multi-agent + Executor · MCP · Pub/Sub + detector worker · RAG có phiên bản · memory · Terraform + CI · trace OTel · 40 kịch bản eval |
| Tuần 2 — đủ phạm vi | 5/10 → 11/10 | **Toàn bộ phạm vi build**: 6 use case: UC1 đầy đủ · UC2, UC3 demo-ready (tích hợp cùng engine) · UC4–UC6 spec + kịch bản khung (không build) · copilot + auto-wrap · 5 loại handoff · Contact Arbitration · bảo mật (policy, sàng lọc injection) · eval ~150 kịch bản + RAG eval + red-team · **baseline B0–B2** (§23) · eval gate · dashboard · pipeline dữ liệu (gán nhãn, tổng hợp, DVC) · cỡ mẫu + ngưỡng detector · tải + chaos · 5 người dùng thử + mystery shopping · **demo đầy đủ 11/10** |
| Tuần 3 — cải thiện | 12/10 → 18/10 | Chỉ cải thiện, không thêm phạm vi: **model triage PhoBERT + chuỗi MLOps** · data science nâng cao (dự báo contact, survival, uplift) · tối ưu chi phí / độ trễ · chuyển workflow nhiều ngày sang Temporal · GraphRAG · tinh chỉnh theo kết quả eval và người dùng thử |

**"Đủ phạm vi" nghĩa là:** mọi thành phần trong Phần B và C chạy được trên thế giới giả lập, có phép đo, có trong demo 11/10.**Chỉ ở mức thiết kế production** (không build trong cuộc thi): Dataflow, vLLM tự host, A2A với đơn vị thật, đa region, identity vault trong nước với dữ liệu thật, tích hợp DMS/ERP thật.**Luật cắt phạm vi:** 21:00 mỗi tối kiểm tra; việc không kịp đẩy sang mốc sau, không kéo dài ngày. Không bao giờ hy sinh: tín hiệu hệ thống → can thiệp chủ động → xác nhận → xác minh → chuyển người (cùng chat đa mục đích), và các hard gate (§22). Hai tuần cho 4 người là dày — §42 có thứ tự cắt khi trễ.
