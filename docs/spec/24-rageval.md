# 24 · Đánh giá RAG — Tách lỗi tìm kiếm khỏi lỗi sinh câu trả lời

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

### Phân loại lỗi — mỗi câu trả lời sai phải gán được một nhãn

| Tầng | Loại lỗi | Ví dụ trong domain |
| --- | --- | --- |
| Retrieval | Không tìm thấy đoạn đúng | Hỏi bảo hành pin, chỉ lấy đoạn bảo hành xe |
| Sai phiên bản / hết hiệu lực | Lấy chính sách sạc cũ |
| Sai đối tượng | Lấy thời hạn xe cá nhân cho xe kinh doanh vận tải |
| Cắt mất điều kiện | Có "10 năm" nhưng mất "hoặc 200.000 km, tuỳ điều kiện nào đến trước" |
| Generation | Không trung thành với nguồn (bịa) | Thêm điều kiện không có trong tài liệu |
| Thiếu ý bắt buộc | Không nhắc loại trừ khi được hỏi "có mất bảo hành không" |
| Từ chối sai / không từ chối khi nên | Nói "không có thông tin" dù có; hoặc trả lời khi tài liệu không nói |
| Trích dẫn sai | Dẫn §2.1 nhưng nội dung ở §3 |

### Chỉ số

| Thành phần | Chỉ số | Định nghĩa | Ngưỡng |
| --- | --- | --- | --- |
| **Retrieval** | Recall@k / Hit@k | Đoạn đúng có nằm trong top-k | Recall@5 ≥ 0,90 |
| MRR, nDCG@k | Đoạn đúng xếp cao đến đâu | MRR ≥ 0,75 |
| Context precision | Tỷ lệ đoạn lấy về thật sự liên quan (Ragas) | ≥ 0,80 |
| Context recall | Thông tin cần cho đáp án chuẩn có đủ trong context (Ragas) | ≥ 0,90 |
| **Version accuracy** (riêng của bài) | Đoạn lấy về đúng dòng xe, loại hình, phiên bản, còn hiệu lực | 100% |
| **Generation** | Faithfulness | Số khẳng định được context hỗ trợ / tổng số khẳng định (Ragas) | ≥ 0,95 |
| Answer relevancy | Trả lời đúng câu hỏi (Ragas) | ≥ 0,85 |
| Answer correctness | So với đáp án chuẩn | ≥ 0,90 |
| Citation precision | Trích dẫn trỏ đúng đoạn chứa ý | ≥ 0,95 |
| Correct abstention | Câu không có trong tài liệu → nói chưa có và chuyển người | ≥ 0,95 |
| Noise robustness | Chèn đoạn nhiễu gần giống (dòng xe khác) mà vẫn đúng | ≥ 0,90 |

### Bộ dữ liệu ~150 câu

| Nhóm | Tỷ lệ | Ví dụ |
| --- | --- | --- |
| Đơn giản | 20% | "Bao lâu phải bảo dưỡng một lần?" |
| Có điều kiện | 20% | "Xe chạy dịch vụ thì bảo hành bao lâu?" |
| Nhạy phiên bản / thời gian | 15% | "Sau 30/6/2027 sạc có mất phí không?" |
| Nhiều bước | 10% | Mã lỗi → hệ thống → có thuộc bảo hành không |
| Không có trong tài liệu | 10% | Hỏi chính sách chưa công bố |
| Tiền đề sai | 10% | "Nghe nói bảo hành 15 năm đúng không?" |
| Không dấu, viết tắt, teencode | 15% | "bh vf8 bao lau vay" |

Sinh bằng LLM từ KB rồi người review; mỗi câu có đáp án chuẩn + ID đoạn đúng; thêm **hard negatives** (điều khoản gần giống của dòng xe khác).

```python
# eval/rag_eval.py — faithfulness mức khẳng định (phác thảo)
async def faithfulness(answer: str, contexts: list[str]) -> float:
    claims = await llm_json(SPLIT_CLAIMS_PROMPT, answer)          # tách thành các khẳng định nguyên tử
    verdicts = await asyncio.gather(*[
        llm_json(NLI_PROMPT, {"claim": c, "context": contexts}) for c in claims])
    supported = sum(v["label"] == "supported" for v in verdicts)
    return supported / max(len(claims), 1)
# Con số, ngày, km vẫn đi qua claim_check tất định — LLM chỉ chấm phần ngữ nghĩa
# So sánh cấu hình (có/không rerank, contextual retrieval, kích thước chunk, model embedding)
# bằng ablation trên cùng bộ, báo cáo khoảng tin cậy bootstrap
```
