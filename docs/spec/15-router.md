# 15 · Model router & context engineering — Dùng trí tuệ rẻ nhất đủ tin cậy cho từng việc

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Việc | Tầng model | Mức suy luận | Output | Ngân sách token (ước tính) |
| --- | --- | --- | --- | --- |
| Triage ý định, mức khẩn, cảm xúc | Nhỏ / nhanh | Thấp | JSON schema | ~800 |
| Hội thoại thường, tra cứu, giải thích | Nhanh | Thấp–trung bình | Text + tool call | ~3.000 / lượt |
| Can thiệp nhiều nguồn (UC1), lập phương án đa ràng buộc (UC3), hội thoại mơ hồ nhiều mục đích | Suy luận | Cao | Options (JSON) | ~6.000 |
| Soạn tin chủ động từ mẫu | Nhỏ | Thấp | Điền slot mẫu | ~600 |
| Tóm tắt 1 câu + sentiment cho handoff | Nhỏ | Thấp | JSON | ~1.200 |
| Chấm rubric (eval, QA mẫu) | Suy luận | Trung bình | Điểm + lý do | ~2.500 |
| Phân tích trace (loop 4) | Suy luận, chạy batch | Cao | Đề xuất PR | Theo lô, ngoài giờ |

### Context packet — chỉ bằng chứng cần thiết

```text
{
 "task": "reschedule_after_parts_loss",
 "customer": {"id":"C-10293","segment":"personal",
              "pref":{"hours":"sau 12:00","channel":"app"}},
 "vehicle": {"model":"VF 8","soc":42,"odometer":38420,
             "sw":"x.y.z","dtc":["BATT-COOL-01:WARNING"]},
 "appointment": {"id":"SA-20931","ws":"Long Biên",
                 "start":"2026-10-03T09:00"},
 "evidence": ["ERP R-7702 cancelled 14:02 (recall)"],
 "candidates": [ …kết quả find_options… ],
 "policy_refs": ["sop:reschedule_parts v1.2"]
}
```

### Kỹ thuật context

- **Thứ tự cho prompt caching:** system prompt → mô tả tool → SOP/chính sách (tĩnh) → rồi mới đến dữ liệu phiên (động).
- **Nén hội thoại:** sau ~10 lượt, thay lịch sử bằng goal stack + 3 lượt gần nhất.
- **Cắt kết quả tool:** tool trả về trường cần thiết, không dump bản ghi.
- **Truy xuất đúng lúc:** KB chỉ lấy khi agent cần, giới hạn 3–5 đoạn.
- **Không đưa định danh thật vào model bên ngoài:** tên / SĐT / vị trí thay bằng token giả (§30).

Chi phí mỗi việc = Σ(token × giá model) + tool + hạ tầng, gắn theo journey_id → ra ACRC thật trên dashboard.
