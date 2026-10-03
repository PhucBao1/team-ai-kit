# 33 · Tech stack tổng hợp — Toàn bộ tech stack ở một chỗ: mỗi thứ giải quyết vấn đề gì

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Nguyên tắc: **một framework điều phối agent (LangGraph)**; mọi thứ quyết định đúng/sai (bảo hành, quãng đường, validator, Executor) là Python thuần có unit test, không phụ thuộc framework. Cột "Khi nào": MVP có trong demo 30/9 · T1–2 xong trước demo đầy đủ 11/10 · T3 cải thiện tuần 3 · Prod chỉ ở production, ghi để thể hiện hướng đi.

| Công nghệ | Vai trò | Giải quyết vấn đề gì trong bài | Khi nào | Chi tiết |
| --- | --- | --- | --- | --- |
| 1 · Agent & AI | | | | |
| **LangGraph** | Framework điều phối agent duy nhất | Coordinator + sub-agent, luồng proactive, vòng Writer ⇄ Critic, dừng chờ khách xác nhận (interrupt), nhớ trạng thái hội thoại bền qua checkpoint | MVP | §13 §14 |
| **LangChain (create_agent, tool)** | Lớp gọi model + tool bên dưới LangGraph | Khai báo tool, structured output (JSON schema), không phải tự viết vòng gọi tool | MVP | §13 |
| **Gemini (Gemini Enterprise Agent Platform / Vertex AI)** | Model ngôn ngữ | Bản nhanh: hội thoại, soạn tin. Bản suy luận: can thiệp nhiều nguồn (UC1) và lập phương án đa ràng buộc (UC3). Nằm trong GCP, dùng IAM và VPC-SC | MVP | §07 §15 |
| **Lớp adapter model (hoặc LiteLLM)** | Router theo việc + đổi nhà cung cấp | Đổi model / nhà cung cấp không sửa code agent; chọn model rẻ cho việc dễ | T1–2 | §15 §38 |
| **Pydantic v2 (schema output)** | Ép model trả đúng cấu trúc | Quyết định, handoff card, đề xuất hành động luôn parse được và kiểm tra được | MVP | §13 |
| **Validator + claim_check + confirmation token (code nhóm)** | Guardrail tất định | Chặn bịa chính sách / giá / trạng thái; không ghi gì khi khách chưa xác nhận — ràng buộc cốt lõi của đề | MVP | §17 |
| **Executor tất định (code nhóm)** | Nơi duy nhất được ghi vào hệ thống | Idempotency, saga, outbox: không đặt lịch trùng, lỗi giữa chừng thì hoàn tác | T1–2 | §17 |
| **PhoBERT (VinAI) + transformers** | Model triage tiếng Việt tự huấn luyện | Phân loại ý định / mức khẩn rẻ và nhanh hơn gọi LLM; chỉ ca không chắc mới lên LLM (cascade) | T3 | §18 |
| **ONNX Runtime (INT8)** | Chạy model nhỏ nhanh trên CPU | Triage dưới ~20 ms, không cần GPU | T3 | §18 §38 |
| **vLLM trên GKE** | Tự host model open-weight | Dữ liệu nhạy cảm không ra ngoài; giảm chi phí khi khối lượng lớn | Prod | §37 |
| **A2A** | Agent nói chuyện với agent của đơn vị khác | Nối agent trạm sạc, cư dân, trợ lý AI của khách mà không chung code | Prod | §14 |
| 2 · Tool & tích hợp | | | | |
| **MCP + FastMCP** | Chuẩn bọc hệ thống thành tool | DMS, ERP kho, CSMS, bảo hành, CRM mỗi cái là một MCP server có quyền riêng; agent nào cũng gọi được theo một chuẩn | T1–2 | §11 §12 |
| **Hàm Python thường làm tool** | Tool nhanh cho MVP | Có tool chạy được trong 3 ngày; lên MCP ở tuần 1 không đổi chữ ký | MVP | §11 |
| 3 · Tri thức (RAG) | | | | |
| **pgvector (vector store trong Postgres), chỉ mục HNSW** | Vector store | Lọc theo dòng xe, phiên bản phần mềm, ngày hiệu lực rồi tìm theo nghĩa trong một câu SQL; cùng DB với trạng thái nên không lệch metadata. Lên production: AlloyDB + ScaNN, không đổi code | T1–2 | §16 |
| **BM25 + underthesea + khôi phục dấu** | Tìm theo từ khoá tiếng Việt | Bắt mã lỗi, tên linh kiện, câu gõ không dấu mà tìm vector hay trượt | T1–2 | §16 |
| **Hybrid + RRF + cross-encoder rerank** | Gộp và xếp lại kết quả | Đưa đúng điều khoản lên đầu → trích dẫn chính xác, ít bịa | T1–2 | §16 |
| **Gemini embedding** | Biến văn bản thành vector | Tìm theo nghĩa, đa ngôn ngữ | T1–2 | §16 |
| **GraphRAG / knowledge graph** | Tri thức dạng quan hệ | Mã lỗi → hệ thống → linh kiện → SOP; câu hỏi nhiều bước | T3 | §16 |
| **AlloyDB ScaNN / Vertex AI Vector Search** | Vector store quy mô lớn | Khi index hàng triệu đoạn (transcript, lịch sử dịch vụ) hoặc tìm kiếm thành tải chính; ngưỡng đổi ghi ở §16 | Prod | §16 |
| 4 · Backend & dữ liệu | | | | |
| **FastAPI + Uvicorn + SSE** | API và stream chat | Async, stream câu trả lời từng phần, nhóm quen | MVP | §19 |
| **SQLModel / SQLAlchemy async + asyncpg** | Truy cập DB bất đồng bộ | Không chặn luồng khi gọi nhiều nguồn song song | MVP | §35 |
| **Postgres (Cloud SQL) → AlloyDB** | Journey State Graph, audit, checkpoint | Nguồn sự thật cho lịch, kho, lệnh sửa chữa; audit mọi hành động | MVP | §08 |
| **Redis / Memorystore** | Cache, khoá, rate limit | Chống gửi trùng, giới hạn tần suất liên hệ khách, cache context | T1–2 | §35 |
| **Pub/Sub (schema + dead-letter)** | Luồng sự kiện hệ thống | Cửa thứ 2 của bộ não: tín hiệu xe, kho, sạc đi vào detector; sai schema không làm sập | T1–2 | §09 |
| **Detector worker (Python, Cloud Run)** | Rule L0 tất định | Lọc phần lớn sự kiện với ~0 token trước khi tới LLM | T1–2 | §09 |
| **Temporal (trên GKE)** | Workflow bền nhiều ngày | Giữ linh kiện đến ngày hẹn, cửa sổ xác minh 14–30 ngày, retry không mất trạng thái | T3 | §17 |
| **Datastream (CDC) + Dataflow** | Lấy thay đổi từ hệ thống cũ | Không phải sửa DMS/ERP cũ vẫn có sự kiện | Prod | §07 |
| **BigQuery + Looker** | Kho phân tích + dashboard | Tầng gold: metric CX, bảng so sánh baseline, chi phí trên mỗi việc, VoC cho quản lý | T1–2 | §08 §28 |
| **Lakehouse (BigLake cũ) · Iceberg trên Cloud Storage · Dataplex** | Lakehouse bronze / silver / gold | Tách phân tích khỏi DB vận hành; giữ dữ liệu thô (telematics, transcript, trace) rẻ, đọc bằng BigQuery và Spark; lineage cho dataset huấn luyện | T3 · Prod | §08 |
| **Great Expectations / Pandera** | Kiểm dữ liệu | Dữ liệu vào sai định dạng bị chặn trước khi làm hỏng metric | T1–2 | §10 |
| 5 · Frontend | | | | |
| **React + Vite + Tailwind (hoặc Next.js)** | 3 màn hình demo | Chat của khách, "Việc của tôi", console nhân viên + bảng điều khiển demo | MVP | §20 §21 |
| **TanStack Query + SSE** | Đồng bộ dữ liệu thời gian thực | Trạng thái việc cập nhật ngay khi agent xử lý xong | T1–2 | §21 |
| 6 · Đánh giá & kiểm thử | | | | |
| **Harness kiểu τ-bench (code nhóm) + khách ảo** | Eval end-to-end | Đo agent có đưa thế giới về trạng thái đúng không, chạy k lần (pass^k) | T1–2 | §23 §25 |
| **Baseline B0–B3 (cờ cấu hình)** | Mốc so sánh | Chứng minh hơn quy trình không AI, chatbot FAQ, single agent; ablation cho biết thành phần nào đáng tiền | T1–2 · T3 | §23 |
| **τ²/τ³-bench · BFCL · VN-MTEB** | Benchmark công khai | Neo lõi agent, model gọi tool, embedding tiếng Việt với chuẩn bên ngoài | MVP → T3 | §23 |
| **Ragas / DeepEval** | Đo chất lượng RAG | Faithfulness, context precision/recall, bỏ trả lời khi thiếu nguồn | T1–2 | §24 |
| **Trajectory eval (state LangGraph / agentevals)** | Đo đường đi của agent | Gọi đúng tool, đúng thứ tự, đúng tham số | T1–2 | §25 |
| **LLM-as-judge có hiệu chỉnh (kappa ≥ 0.7)** | Chấm tự động câu trả lời | Chấm nhanh ~300 kịch bản mà vẫn khớp người chấm | T1–2 | §23 |
| **pytest + hypothesis** | Unit / property test | Luật bảo hành, quãng đường, validator đúng với mọi đầu vào | MVP | §26 |
| **Playwright** | Test giao diện E2E | Kịch bản demo không vỡ trước giờ trình bày | T1–2 | §26 |
| **Locust** | Load test | Biết chịu được bao nhiêu hội thoại đồng thời | T3 | §36 |
| **promptfoo / red-team suite** | Tấn công thử | Prompt injection, đòi hoàn tiền trái phép, rò dữ liệu | T1–2 | §31 |
| 7 · Observability, MLOps & data science | | | | |
| **OpenTelemetry GenAI** | Chuẩn trace cho LLM | Một trace xuyên suốt một việc: model, tool, token, chi phí | T1–2 | §29 |
| **Langfuse** | Xem trace + eval online | Debug vì sao agent trả lời sai; gắn điểm eval vào trace | MVP | §29 |
| **Cloud Trace / Cloud Monitoring / Logging** | Giám sát hạ tầng | SLO độ trễ, lỗi, cảnh báo | T1–2 | §29 |
| **MLflow** | Registry model | Quản lý phiên bản PhoBERT, shadow → canary, rollback | T3 | §18 |
| **Evidently (hoặc tự tính PSI)** | Phát hiện drift | Biết khi nào ý định khách thay đổi và model cần huấn luyện lại | T3 | §18 |
| **Python DS (pandas, scipy, statsmodels, lifelines)** | Thống kê | Cỡ mẫu pilot, ngưỡng detector theo chi phí (T1–2); CUPED, survival, uplift (T3) | T1–2 | §28 |
| 8 · Hạ tầng, CI/CD & bảo mật | | | | |
| **Cloud Run** | Chạy các service | api, agent, mcp-*, detector, web; tự scale, trả theo dùng | MVP | §07 |
| **Docker + Artifact Registry** | Đóng gói | Một image chạy giống nhau ở máy dev và GCP | MVP | §30 |
| **Terraform** | Hạ tầng dạng code | Dựng lại môi trường bằng một lệnh, review được | T1–2 | §30 |
| **GitHub Actions / Cloud Build** | CI/CD + eval gate | Đổi prompt / KB / model mà eval tụt thì không cho deploy | T1–2 | §30 |
| **GKE Autopilot** | Chạy phần cần stateful / GPU | Temporal, vLLM | T3 | §37 |
| **Secret Manager · KMS (CMEK)** | Khoá và bí mật | Không để API key trong code; dữ liệu mã hoá bằng khoá của mình | T1–2 | §31 |
| **Sensitive Data Protection** | Che dữ liệu cá nhân | Tên, SĐT, biển số bị thay bằng token trước khi vào LLM và kho phân tích | T1–2 | §31 |
| **VPC-SC · Cloud Armor · IAM** | Rào mạng và quyền | Chặn rò dữ liệu ra ngoài, chống tấn công web, quyền tối thiểu cho từng service | Prod | §31 |
| **Model Armor (hoặc lớp sàng lọc tương đương)** | Lọc prompt / output | Chặn prompt injection và nội dung độc hại ở biên | Prod | §31 |

**Vì sao LangGraph mà không dùng thêm Google ADK:** hai framework làm cùng một việc (điều phối agent). Dùng cả hai thì trạng thái hội thoại nằm ở hai nơi, trace bị đứt, eval phải viết hai lần. LangGraph vẫn chạy trên Cloud Run và gọi Gemini qua Vertex AI, nên câu chuyện "production trên GCP" giữ nguyên. Nếu sau này đơn vị khác dùng framework khác, hai bên nói chuyện qua A2A (ADR 003, §47).

Tên sản phẩm GCP: Vertex AI được phát triển thành Gemini Enterprise Agent Platform (công bố 22/4/2026). Kiểm tra lại tên model và API theo tài liệu hiện hành trước khi code.
