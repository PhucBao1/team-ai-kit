---
name: add-kb-document
description: Nạp hoặc cập nhật tài liệu chính sách vào knowledge base (bảo hành, bảo dưỡng, sạc, triệu hồi, SOP, FAQ) ở src/kb với metadata phiên bản và chạy RAG eval. Dùng khi thêm/sửa file trong src/kb/, khi chính sách công khai thay đổi, hoặc khi sửa pipeline nạp / truy hồi hybrid (pgvector + BM25) của KB.
---

# Thêm / cập nhật tài liệu KB

Spec: `../team-ai-kit/docs/spec/16-knowledge.md` (RAG, pgvector), `24-rageval.md`. Sai phiên bản chính sách = lỗi nặng nhất.

## Bước
1. Chỉ nguồn công khai (URL chính thức) hoặc tài liệu giả định ghi `assumed: true`.
2. Tạo `src/kb/docs/<miền>/<doc_id>_v<YYYY.MM>.md` + `<doc_id>_v<YYYY.MM>.meta.yaml` theo `templates/meta.yaml`.
   **Không đặt KB dưới `data/`** — `.gitignore` của BTC bỏ qua `data/`. `.dockerignore` đã cho phép `src/kb/**/*.md`.
3. Văn bản giữ cấu trúc điều khoản (§1, §1.1…) — pipeline cắt theo điều khoản, không theo số ký tự.
4. Bản mới thay bản cũ: đặt `effective_to` cho bản cũ, KHÔNG xoá (xe mua theo chính sách cũ vẫn cần trả lời đúng).
5. `python -m src.kb.ingest` (dựng chỉ mục mới kiểu blue/green) → `python -m eval.rag_eval`. Không đạt ngưỡng (faithfulness, context recall, version accuracy) → không chuyển chỉ mục.
6. Thêm ≥ 3 câu hỏi vào `eval/rag_golden/` cho điều khoản mới, có đáp án + đoạn nguồn đúng (ghi `chunk_id` mong đợi).
7. Mâu thuẫn giữa nguồn → ghi trong PR, để người nghiệp vụ quyết.

## Metadata mỗi chunk (ingest phải ghi đủ)
`doc_id`, `version`, `effective_from`, `effective_to`, `section` (§…), `chunk_index`, `embed_model`.
`chunk_id` ổn định = `<doc_id>_v<version>§<section>#<chunk_index>`; citation theo `contracts/api.yaml` = `kb:<doc_id>_v<version>§<section>`.
- **1 model embedding cho 1 chỉ mục.** Đổi model (hoặc số chiều) → embed lại TOÀN BỘ vào chỉ mục mới (blue/green), không trộn vector của 2 model.
  Truy vấn kiểm `embed_model` của chỉ mục khớp model đang dùng, lệch → lỗi rõ, không trả kết quả.

## Truy hồi hybrid (khi sửa `src/kb/` phần search) — chi tiết + SQL mẫu: `references/hybrid-retrieval.md`
- **Lọc phiên bản hiệu lực ở CẢ HAI nhánh** (vector và text) TRƯỚC khi trộn: `effective_from <= ngày tham chiếu < effective_to` (null = còn hiệu lực),
  ngày tham chiếu = ngày mua / ngày sự kiện của xe nếu có, không mặc định "hôm nay".
- **Trộn bằng RRF, k = 60**: `score(chunk) = Σ_nhánh w_nhánh / (k + rank_nhánh)`, rank đếm từ 1. Mỗi nhánh lấy `3 × top_k` ứng viên.
  **KHÔNG cộng thẳng** cosine với BM25 / `ts_rank` (thang đo khác nhau). Log `chunk_id` + rank ở cả hai nhánh (thiếu = null) để debug.
- **Text search tiếng Việt**: cấu hình `'simple'` + `unaccent` (cả lúc index lẫn lúc truy vấn) để gõ không dấu vẫn khớp — hoặc tokenizer BM25 riêng
  có bỏ dấu. KHÔNG dùng `'english'` (stemmer tiếng Anh cắt hỏng từ tiếng Việt).
- **Filter an toàn**: khoá filter theo whitelist (`doc_id`, `domain`, `models`, `usage_type`…); giá trị truyền tham số (`$1`, `:name`),
  KHÔNG f-string / nối chuỗi SQL. Khoá lạ → lỗi, không bỏ qua im lặng.
- **KB < 10K vector → tìm chính xác** (quét tuần tự `ORDER BY embedding <=> $1`), KHÔNG dùng HNSW kèm `WHERE` (lọc sau ANN làm rơi kết quả đúng).

## Đo và trích dẫn
- Đo **retrieval theo `chunk_id`** trước (recall@k, MRR trên `eval/rag_golden/`), rồi mới đo Ragas (faithfulness, context recall).
  Retrieval kém → sửa chunk / truy hồi, không chỉnh prompt để che.
- Câu trả lời dùng KB **phải có citation trỏ chunk** (`kb:<doc_id>_v<version>§<section>`, khớp một chunk đã truy hồi trong lượt đó);
  không có chunk ủng hộ → nói không tìm thấy / handoff, không suy diễn.

## Kiểm tra
- [ ] Mọi con số (năm, km, %) có trong nguồn — không suy diễn · `accessed_at` là ngày thật mở nguồn
- [ ] Chunk có đủ metadata (gồm `embed_model`); bản cũ còn, có `effective_to`
- [ ] Sửa truy hồi: lọc phiên bản ở cả 2 nhánh, RRF theo rank, SQL tham số hoá, có test câu hỏi không dấu
- [ ] recall@k / MRR theo `chunk_id` không tụt so với chỉ mục đang chạy

Nguồn ý tưởng (diễn đạt lại): wshobson/agents `plugins/llm-application-dev/skills/hybrid-search-implementation`, `embedding-strategies`,
`rag-implementation` (MIT, commit 156b7a5e7a).
