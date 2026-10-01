# Gộp PR bootstrap vào P-073 (người D, sáng 28/9)

File: `p073-bootstrap.bundle` (2 commit trên nền `main` ddabbe9: bootstrap 64 file + khoá version / bỏ mặc định không an toàn). Xem trước nội dung: `p073-bootstrap.patch`.

Gồm: config gộp (ruff, requirements py3.11, compose, Makefile, `.env.example`), **khung interface** (chữ ký + stub `NotImplementedError("<mã task>")`), **API mock** cho C, `contracts/` + `contracts/fixtures/demo_world.yaml`, sơ đồ kiến trúc, test (36 test, coverage 87%).

Máy Windows: chạy `git config core.autocrlf false` trước khi gộp, nếu không `git status` báo sửa hàng loạt file do CRLF.

```bash
cd P-073
git checkout main && git pull
git fetch ../p073-bootstrap.bundle chore/bootstrap:kit-bootstrap
git merge --squash kit-bootstrap
git commit -m "chore: bootstrap cấu trúc dự án EV CX Agent"   # tác giả là bạn
git branch -D kit-bootstrap
ruff check src/ tests/ && pytest tests/ -v                   # đúng như CI BTC — phải xanh
git push origin main
git checkout -b develop && git push -u origin develop
python3 ../team-ai-kit/plan/verify.py D1.02 A1.02 B1.02 D1.03 D1.07   # phải ĐẠT ngay (còn mục kiểm tay)
```
Không có file nào của team-ai-kit trong commit này (chỉ code, config gộp, contracts, sơ đồ, deliverable architecture).

## Đã gộp bootstrap trước 1/10?
Chỉ áp thêm commit sửa (khoá version theo major, `langgraph>=1.0`, `fastmcp` 4.x; production bắt buộc `CONFIRM_TOKEN_SECRET`; CORS không credentials; `/chat` không lộ lỗi):
```bash
git checkout develop && git pull
git am ../p073-fix-versions.patch        # tác giả là bạn: git am --reset-author nếu muốn
pip install -r requirements.txt && ruff check src/ tests/ && pytest tests/ -q
```
