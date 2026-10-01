# 16 · Knowledge, RAG & memory — Trả lời đúng phiên bản, đúng điều khoản, nhớ đúng thứ được phép nhớ

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### Pipeline nạp KB

```text
nguồn công khai (URL) / tài liệu nội bộ
  → làm sạch HTML/PDF
  → cắt theo điều khoản (không cắt theo số ký tự)
  → metadata: doc_id, version, effective_from,
    effective_to, source_url, accessed_at,
    applies_to {model, usage_type, sw_version}
  → embedding + chỉ mục từ khoá (hybrid)
  → job phát hiện mâu thuẫn: cùng điều khoản,
    khác nội dung giữa các nguồn → gắn cờ,
    tạm dừng trả lời tự động điều khoản đó
```

Truy xuất: lọc metadata trước (dòng xe, loại hình, phiên bản phần mềm, còn hiệu lực) → hybrid search → rerank → 3–5 đoạn. Trích dẫn dạng kb:warranty_v2026.03§2.1.

### Knowledge graph mã lỗi

```text
(DTC)-[:THUOC_HE_THONG]->(System)
(DTC)-[:MUC_DO]->(Severity)
(DTC)-[:SUA_TU_XA {sw>=…}]->(RemoteAction)
(DTC)-[:KHA_NANG_THAY {p}]->(Part)
(DTC)-[:HUONG_DAN]->(SOP)
(Part)-[:LAP_CHO]->(Model)
(SOP)-[:YEU_CAU_KY_NANG]->(Certification)
```

MVP: bảng quan hệ trong Postgres. Production: GraphRAG khi số mã lỗi và SOP lớn.

### Vector store: pgvector ngay trong Postgres — vì sao không dùng vector DB riêng

Hệ thống **có** vector store: pgvector là extension biến Postgres thành vector store. Chọn nó vì bài này cần **lọc theo nghiệp vụ trước rồi mới tìm theo nghĩa** (dòng xe, loại hình sử dụng, phiên bản phần mềm, ngày hiệu lực). Lọc và tìm vector nằm chung một câu SQL, cùng DB với trạng thái hành trình và checkpoint LangGraph — không có hai nơi giữ metadata để lệch nhau, mà trả lời sai phiên bản chính sách là lỗi bài này đang chống.

| Phương án | Mạnh | Yếu với bài này | Dùng khi |
| --- | --- | --- | --- |
| **pgvector (Cloud SQL Postgres)** — chọn | Lọc metadata + vector + full-text trong một câu SQL; transaction; không thêm hệ thống | Đến vài triệu vector mới cần tinh chỉnh kỹ | MVP → tuần 2 (KB ~10.000 đoạn) |
| **AlloyDB + chỉ mục ScaNN** | Vẫn là Postgres (không đổi code); chỉ mục ScaNN của Google nhanh hơn ở quy mô lớn; HA sẵn | Đắt hơn Cloud SQL | Production, khi index thêm transcript tổng đài, ghi chú lệnh sửa chữa (hàng triệu đoạn) |
| **Vertex AI Vector Search** | Hàng tỷ vector, QPS rất cao, managed | Metadata phải đồng bộ sang; lọc phức tạp khó hơn SQL; thêm một hệ thống | Khi tìm kiếm là tải chính (vd. tìm ca tương tự trên toàn bộ lịch sử dịch vụ) |
| Qdrant / Weaviate / Pinecone | Chuyên vector, nhiều tính năng tìm kiếm | Ngoài hệ sinh thái GCP; thêm vận hành, bảo mật, dữ liệu nằm ngoài | Không dùng |

```text
-- db/migrations/002_kb.sql — kiểm tra theo docs pgvector hiện hành (≥ 0.8)
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE kb_chunk (
  id bigserial PRIMARY KEY,
  doc_id text, clause text, parent_id bigint,          -- parent-child: tìm đoạn nhỏ, trả điều khoản cha
  version text, effective_from date, effective_to date,
  models text[], usage_type text, sw_min text, sw_max text,
  content text,
  tsv tsvector,                                        -- từ khoá: underthesea tách từ + bản không dấu, config 'simple'
  embedding vector(768)                                -- Gemini embedding, giảm chiều còn 768
);
CREATE INDEX kb_hnsw ON kb_chunk USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
CREATE INDEX kb_tsv  ON kb_chunk USING gin (tsv);
CREATE INDEX kb_meta ON kb_chunk (usage_type, effective_from, effective_to);

-- truy vấn: lọc nghiệp vụ trước, rồi mới xếp theo nghĩa (nhánh vector của hybrid)
SET hnsw.ef_search = 100;
SET hnsw.iterative_scan = relaxed_order;   -- tránh thiếu kết quả khi bộ lọc chặt
SELECT id, clause, content
FROM kb_chunk
WHERE :model = ANY(models) AND usage_type = :usage
  AND current_date BETWEEN effective_from AND coalesce(effective_to, 'infinity')
  AND :sw BETWEEN sw_min AND sw_max
ORDER BY embedding <=> :query_vec
LIMIT 20;                                  -- + 20 từ nhánh BM25 → RRF → cross-encoder → giữ 3–5
```**Khi nào đổi sang chỗ khác — theo số đo, không theo cảm giác:** KB ~10.000 đoạn × 768 chiều ≈ 30 MB, nằm gọn trong RAM. Chỉ nâng cấp lên AlloyDB + ScaNN (không đổi code) khi p95 truy xuất > 50 ms, hoặc recall@20 của chỉ mục so với tìm chính xác < 0,95 (đo trong §24), hoặc số đoạn vượt vài triệu. Vertex AI Vector Search chỉ khi tìm kiếm trở thành tải chính.

### Ba tầng memory

| Tầng | Chứa gì | Lưu ở đâu | Thời hạn | Khách kiểm soát |
| --- | --- | --- | --- | --- |
| Phiên | Goal stack, slot đã biết, 3 lượt gần nhất | LangGraph checkpointer (Postgres, theo thread_id) + Redis cache | 24 giờ sau lượt cuối | — |
| Hành trình | Journey, promises, trạng thái, audit | Postgres / AlloyDB | Theo quy định lưu trữ nghiệp vụ | Xem trong "Việc của tôi" |
| Sở thích dài hạn | Xưởng quen, khung giờ, kênh, xưng hô, xe chính | Bảng riêng, tách khỏi dữ liệu định danh | Đến khi khách xoá / rút đồng ý | Xem, sửa, xoá; tắt cá nhân hoá |
