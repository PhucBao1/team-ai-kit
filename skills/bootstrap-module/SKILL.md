---
name: bootstrap-module
description: Tạo package / module mới đúng khuôn repo P-073 (trong src/ với test ở tests/test_<module>/) hoặc dựng frontend/ lần đầu. Dùng khi cần thư mục mới như src/core/warranty, src/sim, src/detect, eval/ runner, frontend/, hoặc khi task nói "tạo module", "dựng khung".
---

# Tạo module mới

Đọc trước: `../team-ai-kit/docs/conventions.md` mục 1–7, `AGENTS.md` mục 3 và 6. Giữ cấu trúc template BTC.

## Python module trong `src/`
1. Tạo `src/<module>/` từ `templates/py-module/`: `__init__.py` (chỉ export API public, docstring 1 dòng), `models.py`, `<miền>.py`.
2. Test ở `tests/test_<module>/` (không đặt test trong `src/`): copy `templates/py-module/tests/test_service.py`, sửa import `from src.<module>...`.
3. Fixture dùng chung thêm vào `tests/conftest.py` (file của template — thêm, không xoá fixture cũ `client`, `mock_llm`). Mẫu `seeded_world`, `clock`: `templates/conftest_additions.py`.
4. Module có luật riêng → nhờ người thêm `AGENTS.md` vào `team-ai-kit/rules/src/<module>/` rồi chạy lại `install.sh` (không tạo AGENTS.md trong repo).
5. Kiểm: `ruff check src/ tests/` · `pytest tests/test_<module> -v` · `make typecheck`.

## Frontend lần đầu (người C)
Làm theo `templates/web/SETUP.md` trong thư mục `frontend/`. Xong → chạy lại `bash ../team-ai-kit/install.sh` để gắn `frontend/AGENTS.md`.

## Không được
- Viết tính năng trong PR dựng khung. Thêm thư viện lớn ngoài `requirements.txt` mà không hỏi D (người giữ dependency).
- Đổi `src/main.py`, `src/config.py`, `tests/conftest.py` theo cách phá test mẫu của BTC (`/health`, `/api/v1/chat`, `/api/v1/status`).
