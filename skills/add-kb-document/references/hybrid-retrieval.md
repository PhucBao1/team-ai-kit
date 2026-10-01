# Truy hồi hybrid cho KB (pgvector + text search) — tham khảo

Đọc khi sửa phần search trong `src/kb/` (vd `retriever.py`, task B1.09) hoặc pipeline ingest. Luật trong `../SKILL.md` thắng file này.
Tên bảng / cột dưới đây là MINH HOẠ — theo migration thật (skill `db-migration`).

## 1. Bảng chunk

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS unaccent;

-- unaccent() không IMMUTABLE → bọc lại để dùng trong cột sinh / index
CREATE OR REPLACE FUNCTION vi_unaccent(text) RETURNS text
  LANGUAGE sql IMMUTABLE PARALLEL SAFE STRICT
  AS $$ SELECT public.unaccent('public.unaccent'::regdictionary, $1) $$;

CREATE TABLE kb_chunk (
  chunk_id        text PRIMARY KEY,            -- <doc_id>_v<version>§<section>#<chunk_index>
  doc_id          text NOT NULL,
  version         text NOT NULL,
  effective_from  date NOT NULL,
  effective_to    date,                         -- null = còn hiệu lực
  section         text NOT NULL,                -- §2.1
  chunk_index     int  NOT NULL,
  domain          text NOT NULL,                -- warranty | maintenance | charging | recall | sop | faq
  models          text[] NOT NULL DEFAULT '{}',
  usage_type      text,
  embed_model     text NOT NULL,                -- vd text-embedding-3-small@1536
  content         text NOT NULL,
  embedding       vector(1536) NOT NULL,
  tsv             tsvector GENERATED ALWAYS AS (to_tsvector('simple', vi_unaccent(lower(content)))) STORED
);
CREATE INDEX kb_chunk_tsv ON kb_chunk USING gin (tsv);
-- KHÔNG tạo HNSW/IVFFlat khi < 10K vector: quét tuần tự là tìm chính xác, và lọc WHERE không làm rơi kết quả.
```

`unaccent` mặc định bỏ dấu tiếng Việt (gồm `đ → d`): "bảo hành pin" và "bao hanh pin" ra cùng token.
Không dùng cấu hình `'english'` (stemmer + stopword tiếng Anh). Tokenizer BM25 riêng (vd `rank_bm25` trong Python) cũng phải bỏ dấu + lower trước.

## 2. Truy vấn: lọc phiên bản ở cả hai nhánh → RRF theo rank

```sql
-- $1 query_embedding  $2 query_text  $3 ref_date  $4 n_cand (= 3*top_k)  $5 top_k
-- $6 w_vec  $7 w_txt  $8 domain (hoặc NULL)  $9 model (hoặc NULL)
WITH eligible AS (
  SELECT * FROM kb_chunk
  WHERE effective_from <= $3 AND (effective_to IS NULL OR $3 < effective_to)
    AND ($8::text IS NULL OR domain = $8)
    AND ($9::text IS NULL OR cardinality(models) = 0 OR $9 = ANY(models))
),
vec AS (
  SELECT chunk_id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1) AS rnk
  FROM eligible ORDER BY embedding <=> $1 LIMIT $4
),
txt AS (
  SELECT chunk_id,
         ROW_NUMBER() OVER (ORDER BY ts_rank_cd(tsv, q) DESC, chunk_id) AS rnk
  FROM eligible, plainto_tsquery('simple', vi_unaccent(lower($2))) AS q
  WHERE tsv @@ q
  ORDER BY ts_rank_cd(tsv, q) DESC, chunk_id LIMIT $4
)
SELECT COALESCE(vec.chunk_id, txt.chunk_id)          AS chunk_id,
       vec.rnk                                       AS vec_rank,   -- log cả hai rank
       txt.rnk                                       AS txt_rank,
       COALESCE($6 / (60 + vec.rnk), 0) + COALESCE($7 / (60 + txt.rnk), 0) AS rrf
FROM vec FULL OUTER JOIN txt USING (chunk_id)
ORDER BY rrf DESC, chunk_id
LIMIT $5;
```

- `ROW_NUMBER()` bắt đầu từ 1 → đúng công thức `w / (k + rank)`, k = 60. Trọng số mặc định `w_vec = w_txt = 1.0`; chỉ đổi khi số đo recall@k chứng minh.
- `plainto_tsquery` nối từ bằng AND; câu hỏi dài hay rơi về 0 kết quả ở nhánh text → chấp nhận (RRF vẫn còn nhánh vector)
  hoặc thử `websearch_to_tsquery` / OR các từ — quyết bằng số đo, không cảm tính.
- Không cộng `1 - cosine` với `ts_rank`: hai thang đo khác nhau, trộn điểm thô làm một nhánh lấn át tuỳ câu hỏi.
- Ngày tham chiếu `$3`: ngày mua / ngày sự kiện của xe (lấy từ tool) nếu câu hỏi gắn với xe; không có → ngày hiện tại của simulator.

## 3. Filter từ code Python

```python
ALLOWED_FILTERS: tuple[str, ...] = ("domain", "model")  # whitelist; mỗi khoá ứng với MỘT tham số cố định trong SQL ($8, $9)

def build_params(filters: dict[str, str | None]) -> tuple[str | None, ...]:
    """Chỉ nhận khoá trong whitelist; giá trị đi qua tham số, không ghép vào SQL."""
    unknown = set(filters) - set(ALLOWED_FILTERS)
    if unknown:
        raise ValueError(f"filter không hỗ trợ: {sorted(unknown)}")
    return tuple(filters.get(k) for k in ALLOWED_FILTERS)
```

(SQL ở mục 2 đã chạy thử trên Postgres 16 + unaccent, thay pgvector bằng cột số: lọc phiên bản theo ngày, lọc model, "doi dieu khoan" khớp "Đổi điều khoản".)

Cấm: `f"... WHERE {key} = '{value}'"`, `.format()` vào SQL, `text(...)` có nội suy chuỗi. Dùng tham số của driver (`%(name)s` / `$n` / `bindparam`).

## 4. Đo

| Mức | Chỉ số | Dữ liệu |
|---|---|---|
| Truy hồi | recall@k (k = top_k), MRR — so `chunk_id` trả về với `expected_chunk_ids` | `eval/rag_golden/` |
| Phiên bản | version accuracy: chunk top-1 đúng `version` hiệu lực tại ngày tham chiếu | câu hỏi có `ref_date` cũ / mới |
| Sinh | Ragas faithfulness, context recall | chỉ chạy khi truy hồi đạt |

Mỗi lần đổi truy hồi: chạy đủ 3 nhánh (chỉ vector, chỉ text, hybrid) trên cùng golden, log `vec_rank` / `txt_rank` của câu sai để biết nhánh nào hỏng.
Có câu hỏi không dấu / viết tắt trong golden (vd "bao hanh pin bn nam").

Nguồn ý tưởng (diễn đạt lại, không chép nguyên văn): wshobson/agents — `plugins/llm-application-dev/skills/hybrid-search-implementation`
(RRF k = 60, log cả hai điểm), `embedding-strategies` (không trộn model embedding, metadata để lọc), `rag-implementation` (MIT, commit 156b7a5e7a).
