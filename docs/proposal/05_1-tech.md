# 05.1 · Kỹ thuật: loop engineering & tech stack — Từ prompt → context → harness → loop engineering

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Năm 2026, trọng tâm kỹ thuật agent đã dịch chuyển: không còn là viết prompt hay, mà là thiết kế **vòng lặp** quanh model — agent tự hành động, được kiểm tra, được kích hoạt bởi sự kiện, và được cải thiện từ dữ liệu vận hành. Đề xuất này vốn là một hệ thống nhiều vòng lặp; phần này gọi tên và thiết kế chúng theo ngôn ngữ kỹ thuật hiện đại.

### Năm vòng lặp của hệ thống

Bốn vòng đầu theo khung loop engineering (LangChain, 2026); vòng 5 là vòng đặc thù của đề xuất.

LOOP 4 · HILL-CLIMBING*tuần*

trace vận hành → agent phân tích → đề xuất sửa SOP / KB / ngưỡng → **người duyệt** → chạy lại eval → triển khai

LOOP 3 · EVENT-DRIVEN*giây → giờ*

telematics · CSMS · DMS · ERP · claim · tin nhắn → kích hoạt agent (phần proactive)

LOOP 2 · VERIFICATION*mỗi lượt*

output → claim check + validator + rubric → sai thì sửa có phản hồi

LOOP 1 · AGENT*mili-giây*

model ↔ tool (MCP) cho đến khi xong bước

LOOP 5 · OUTCOME*ngày → tuần*

theo dõi lời hứa và dữ liệu xe đến khi "xong" được xác minh — durable execution

| Vòng lặp | Trong hệ thống | Kỹ thuật | Con người ở đâu |
| --- | --- | --- | --- |
| **1 · Agent** | Hội thoại và Decision Engine gọi tool: tra lịch, kho, bảo hành, trạm sạc | LangGraph (coordinator + sub-agent); tool qua MCP; structured output (JSON schema); gọi tool song song khi độc lập | — |
| **2 · Verification** | Claim check, 6 validator, rubric giọng văn, kiểm tra quyền trước khi ghi | Hook trước và sau khi gọi tool; tự sửa có phản hồi, tối đa N lần rồi chuyển người | Xác nhận mức 2–3 |
| **3 · Event-driven** | Chính là phần **proactive**: sự kiện hệ thống kích hoạt agent | Event stream + detector L0 tất định; chỉ event vượt ngưỡng mới gọi LLM | — |
| **4 · Hill-climbing** | Bước Learn: trace → phát hiện mẫu lỗi, lỗ hổng KB, SOP chưa tốt → đề xuất sửa | Agent phân tích trace; đề xuất thành pull request cho SOP / KB / cấu hình; chạy lại bộ eval trước khi áp dụng | **Luôn có người duyệt** — agent không tự sửa chính sách của mình |
| **5 · Outcome** | Theo dõi việc qua nhiều ngày: giữ linh kiện đến ngày hẹn, xác minh 14–30 ngày bằng dữ liệu xe | **Durable execution**: workflow sống nhiều ngày, không mất trạng thái khi hệ thống khởi động lại | Nhận lại việc khi có ngoại lệ |

Vòng 5 là thứ ít framework nói tới nhưng là cốt lõi của đề xuất: một agent CSKH chỉ "xong" khi kết quả ngoài đời được xác minh, và việc đó kéo dài nhiều ngày — vượt xa một phiên hội thoại.

### Harness — hệ điều hành bao quanh model

Model như CPU, context như RAM, harness như hệ điều hành. Model hàng đầu chênh nhau ít trên benchmark tĩnh, nhưng chênh nhiều khi phải làm việc nhiều bước — khác biệt nằm ở harness.

| Thành phần harness | Trong đề xuất |
| --- | --- |
| Context engineering | Context packet chỉ chứa bằng chứng liên quan; nén hội thoại dài theo goal stack; truy xuất đúng lúc (just-in-time) thay vì nhồi cả KB; cắt gọn kết quả tool; phần tĩnh (chính sách, SOP) đặt đầu để dùng **prompt caching** |
| Skills | Mỗi SOP tiếng Việt (§06-G) là một skill: hướng dẫn + bước tất định + test đi kèm; nạp khi cần |
| Subagents | Triage · chẩn đoán · lập lịch · soạn tin — mỗi subagent có tool scope và ngân sách token riêng; routing tất định trước khi cần LLM |
| Hooks | Trước khi gọi tool ghi: policy check + validator + xác nhận. Sau khi gọi: audit log, cập nhật Journey State Graph |
| Spine / state | Journey State Graph + trạng thái workflow bền — agent không lặp lại lỗi đã biết, không hỏi lại điều đã có |
| Permissions | Tool gateway phân quyền theo vai trò, chủ xe / người lái, mức xác nhận |
| Memory | Sở thích dài hạn có đồng ý, xem / xoá được (§06-H) |

### Tech stack theo lớp — MVP cuộc thi và production

| Lớp | MVP (3 tuần: 30/9 → 18/10) | Production (big enterprise) | Vì sao |
| --- | --- | --- | --- |
| **Model** | Gemini trên Gemini Enterprise Agent Platform (Vertex AI): một model reasoning + một model nhỏ; router theo việc | Nhiều nhà cung cấp; model open-weight tự host (có khả năng tiếng Việt) cho dữ liệu nhạy cảm và việc khối lượng lớn; distillation cho triage | Chi phí, không phụ thuộc nhà cung cấp, dữ liệu trong nước |
| **Giao thức & tool** | MCP server (FastMCP) bọc các hệ thống giả lập: DMS, ERP kho, CSMS, bảo hành, CRM, gửi tin | MCP gateway có xác thực, kiểm theo OWASP MCP Top 10; **A2A** cho agent của đơn vị khác và trợ lý AI của khách | MCP là chuẩn chung; A2A mở đường "khách hàng là máy" |
| **Sự kiện** | Pub/Sub (schema + dead-letter) + worker Python trên Cloud Run cho detector L0 | Kafka + stream processing (Flink); CDC (Debezium) từ hệ thống cũ; mô phỏng OCPP | Hàng trăm nghìn xe × sự kiện liên tục |
| **Trạng thái & dữ liệu** | Postgres (AlloyDB khi lên production) + Redis: Journey State Graph, audit, snapshot, session | Postgres / AlloyDB cho Journey State Graph; **lakehouse** (Iceberg trên Cloud Storage + BigQuery, bronze/silver/gold) cho telematics, transcript, VoC, dữ liệu huấn luyện; lưu trữ theo yêu cầu dữ liệu trong nước | Nền dữ liệu là điều kiện tiên quyết (bài học Verizon) |
| **Knowledge** | pgvector + tìm kiếm từ khoá (hybrid) + reranker; KB có phiên bản và ngày hiệu lực | GraphRAG cho knowledge graph mã lỗi → hệ thống → linh kiện → SOP; phát hiện mâu thuẫn tự động | Câu hỏi xe điện cần quan hệ, không chỉ tìm đoạn văn giống |
| **Orchestration** | LangGraph: coordinator + sub-agent, chạy song song, vòng Writer ⇄ Critic, dừng chờ người (interrupt) và checkpoint bền trên Postgres; Executor tất định tách riêng | + **Temporal** (durable execution) cho vòng 5: workflow nhiều ngày, retry, hẹn giờ | Việc proactive kéo dài nhiều ngày — không được mất trạng thái |
| **Guardrail & policy** | Validator Python + claim check; đánh dấu nội dung khách là dữ liệu không tin cậy | Policy engine (Cedar / OPA) tại tool gateway; che dữ liệu cá nhân trước khi gửi LLM bên ngoài; red-team định kỳ | Chặn ở tầng thực thi tool, không chỉ lọc output |
| **Observability** | Langfuse + Cloud Trace, trace theo chuẩn **OpenTelemetry GenAI** | OTel collector → nền tảng observability chung; một trace xuyên suốt một việc qua nhiều ngày; chi phí gắn theo từng việc (ACRC) | Debug được agent, đo được chi phí trên outcome |
| **Eval** | Harness kiểu τ-bench: khách ảo + thế giới giả lập + lỗi tiêm có nhãn; LLM chấm theo rubric, người hiệu chỉnh; pass^k | Eval chạy trong CI mỗi lần đổi SOP / KB / model; eval online trên mẫu trace thật; shadow mode | Khảo sát 2026: 89% đội có observability nhưng chỉ 52% có eval — đây là chỗ nhiều dự án gãy |
| **Giọng nói** | STT → agent → TTS (dạng chuỗi, dễ kiểm soát) | Speech-to-speech thời gian thực cho câu đơn giản; chuỗi STT/TTS khi cần kiểm soát; kiểm thử giọng Bắc / Trung / Nam | Tổng đài vẫn là kênh chính của nhiều khách |
| **Giao diện** | Web (React / Next.js): chat, "Việc của tôi", màn hình nhân viên; cập nhật thời gian thực | Tích hợp app VinFast, Zalo OA, console của tổng đài / DMS | Demo được cả ba phía: khách, nhân viên, quản lý |

Bảng trên là tóm tắt theo lớp. Danh sách đầy đủ ~50 công nghệ, mỗi cái giải quyết vấn đề gì và làm ở tuần nào: file technical §33.

### Kỹ thuật cụ thể và nơi dùng

| Kỹ thuật | Dùng ở đâu |
| --- | --- |
| Structured output (JSON schema) | Mọi quyết định của Decision Engine, handoff card, lời hứa trích từ transcript |
| Điều chỉnh mức suy luận theo việc | Suy luận sâu chỉ ở lập phương án UC1 và hội thoại mơ hồ; triage và soạn tin dùng mức thấp |
| Prompt caching | Chính sách, SOP, mô tả tool — phần tĩnh lớn, dùng lại liên tục |
| Self-verification có phản hồi (vòng 2) | Claim check thất bại → trả lỗi cụ thể cho model sửa, tối đa 2 lần → chuyển người |
| Human-in-the-loop interrupt | Xác nhận của khách, duyệt hoàn tiền, duyệt đề xuất sửa SOP (vòng 4) |
| Simulation-based eval + LLM-as-judge có hiệu chỉnh | ~300 kịch bản; 5% chấm chéo bởi người để hiệu chỉnh giám khảo LLM |
| Trace-driven improvement (vòng 4) | Gom lỗi theo mẫu từ trace → đề xuất sửa → eval → người duyệt |
| Durable workflow | Giữ linh kiện đến ngày hẹn, nhắc lịch, cửa sổ xác minh 14–30 ngày |

**Cố ý không làm trong MVP:** không fine-tune model trong 2 tuần đầu (PhoBERT triage là việc cải thiện tuần 3, huấn luyện trên dữ liệu giả lập có nhãn); không để vòng 4 tự áp dụng thay đổi; không dựng "bầy" nhiều agent tự do phối hợp — subagent có routing tất định; không dùng Kafka; Temporal và fine-tune PhoBERT để tuần 3 (cải thiện), khi Pub/Sub và LangGraph đã đủ cho phạm vi 2 tuần đầu. Hiện đại không có nghĩa là dùng mọi thứ mới — mà là dùng đúng thứ cho đúng vòng lặp.
