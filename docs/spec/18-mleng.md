# 18 · Model triage & MLOps (tuần 3) — Bộ phân loại triage tiếng Việt: huấn luyện, phục vụ, giám sát, huấn luyện lại

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

**Cải tiến tuần 3.** Tuần 1–2 triage dùng LLM nhỏ (đủ cho đề bài). Tuần 3 thay bằng model tự huấn luyện theo cascade — hệ thống vẫn chạy đúng nếu phần này chưa xong.

Triage chạy trên **mọi** tin nhắn, nên là chỗ hợp lý nhất để thay LLM bằng một model nhỏ tự huấn luyện: nhanh hơn, rẻ hơn, và chạy được trong hạ tầng của mình. Khi có một model thật, toàn bộ chuỗi MLOps trở thành việc thật chứ không còn là "tương đương".

| Hạng mục | Thiết kế |
| --- | --- |
| Bài toán | 3 đầu ra: **ý định** (~15 lớp: hỏi cảnh báo, bảo hành, đặt lịch, đổi lịch, tiến độ, sạc, phí, khiếu nại, gặp người…) · **mức khẩn** (nhị phân, ưu tiên recall) · **bực / khiếu nại** (nhị phân) |
| Model | **PhoBERT** (VinAI) fine-tune, một encoder + 3 head. Đầu vào cần tách từ tiếng Việt (VnCoreNLP / RDRSegmenter) theo yêu cầu của PhoBERT |
| Dữ liệu | UIT-ViOCD (khiếu nại, chỉ dùng cho nghiên cứu — đủ cho cuộc thi, production phải thay bằng dữ liệu của mình) · câu hỏi rút từ diễn đàn chủ xe và phỏng vấn (nhóm tự viết lại, không sao chép) · dữ liệu sinh tổng hợp đã review (§27) · sau này: nhãn từ trace thật |
| Baseline bắt buộc | (1) TF-IDF + Logistic Regression · (2) LLM zero-shot. Model chỉ được dùng nếu thắng cả hai trên bộ test tiếng Việt |
| Thước đo | Macro-F1 ý định · **recall mức khẩn ≥ 99%** · F1 khiếu nại · độ trễ p95 · chi phí / 1.000 tin · kiểm tra riêng nhóm câu không dấu |
| Tối ưu phục vụ | Xuất ONNX + lượng tử hoá INT8 → chạy CPU trên Cloud Run (không cần GPU) |
| Cascade với LLM | Độ tin cậy ≥ ngưỡng → dùng kết quả model; thấp hơn → LLM quyết định; **mức khẩn không bao giờ bị hạ** bởi model nhỏ |

```python
# triage/cascade.py — model nhỏ trước, LLM khi không chắc
async def triage(text: str) -> Triage:
    seg = segment_vi(restore_diacritics(text))
    p = clf.predict(seg)                                   # ONNX, ~vài chục ms trên CPU
    if p.urgent_prob >= URGENT_LOW_BAR:                     # ngưỡng thấp → ưu tiên recall
        return Triage(intent=p.intent, urgent=True, source="clf")
    if p.intent_conf >= CONF_THRESHOLD and p.angry_conf >= CONF_THRESHOLD:
        return Triage(intent=p.intent, urgent=False, angry=p.angry, source="clf")
    return await llm_triage(text)                          # fallback, ghi lại để làm nhãn
```

### Chuỗi MLOps

```text
dataset vN (§27) ─► train (Vertex AI custom job / GPU) ─► MLflow: params · metrics · artifact
      ─► đánh giá trên bộ test cố định + nhóm không dấu + so baseline
      ─► model registry: candidate ─(duyệt)─► shadow (chạy song song, không quyết định)
      ─► canary 10% ─► production rollback = đổi alias về phiên bản trước
      ─► giám sát: phân phối lớp dự đoán · độ dài / từ vựng đầu vào (PSI) · drift embedding
                  · độ chính xác trễ từ nhãn người sửa · tỷ lệ rơi xuống LLM
      ─► trigger huấn luyện lại: drift vượt ngưỡng · F1 trễ giảm · mỗi tháng có ≥ N nhãn mới
```

| Thành phần | Công cụ |
| --- | --- |
| Theo dõi thí nghiệm, registry | MLflow (tracking server trên Cloud Run, artifact trên GCS, metadata trên Cloud SQL) — hoặc Vertex AI Experiments / Model Registry |
| Huấn luyện | Hugging Face Transformers; Vertex AI custom training (hoặc GPU cá nhân cho cuộc thi) |
| Phục vụ | ONNX Runtime trong FastAPI trên Cloud Run |
| Giám sát drift | Evidently (hoặc tự tính PSI) chạy job hằng ngày, đẩy metric lên Cloud Monitoring |
| Pipeline | Vertex AI Pipelines / Cloud Composer cho huấn luyện lại định kỳ |

**Model thống kê thứ hai (nhẹ):** xác suất "mã lỗi → linh kiện cần thay" từ lịch sử sửa chữa (đếm có làm mượt, theo dòng xe / đời xe) — phục vụ quyết định ④. Đơn giản, giải thích được, cập nhật hằng tuần.
