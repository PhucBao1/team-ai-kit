# src/core/ — logic tất định (owner: D) · spec `../team-ai-kit/docs/spec/17-core.md`

- CHỈ Python thuần: cấm import `langchain*`, `langgraph*`, `google*`, `openai`, `httpx`, `requests`, `sqlalchemy`, `sqlmodel`; cấm đọc env. Hook sẽ chặn.
- Mỗi hàm public có test trong `tests/test_core/`; luật nghiệp vụ có thêm property test (hypothesis). Test chạy < 5 giây.
- Input là model Pydantic đã chuẩn hoá; trả kết quả + `reasons: list[str]` giải thích được.
- Luật từ chính sách công khai: ghi nguồn trong docstring (`kb:warranty_v2026.03§2.1`). Thiếu luật → trả `UNKNOWN` kèm lý do, không đoán.
- `validator.py` có đúng 7 kiểm tra. Thêm kiểm tra → test + ADR.
