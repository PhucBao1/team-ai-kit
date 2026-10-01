# team-ai-kit — bộ luật, skill, kế hoạch của đội (PRIVATE)

Repo **riêng của đội** (GitHub private, 4 thành viên). KHÔNG push vào repo BTC (P-073).
AI coding agent của mỗi người đọc luật + skill từ đây thông qua `install.sh` — file được gắn vào repo P-073 trên máy bạn
và **giấu khỏi git** (`.git/info/exclude`), nên `git status` của P-073 luôn sạch.

```
vin-smart-future/
├─ P-073/          ← repo BTC — chỉ push sản phẩm (code, contracts, deliverables)
└─ team-ai-kit/    ← repo này
```

## Bắt đầu (mỗi người, 10 phút)

```bash
git clone <P-073 của đội> P-073 && git clone <team-ai-kit private> team-ai-kit
cd P-073
bash scripts/setup_hooks.sh            # hook log AI của BTC — BẮT BUỘC, làm trước tiên
cp .env.example .env                    # điền AI_LOG_API_KEY (dashboard Phoenix), LLM key
python3.11 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt pre-commit
bash ../team-ai-kit/install.sh          # Windows (Git Bash, không bật symlink): bash ../team-ai-kit/install.sh --copy
```
Kiểm tra: gõ 1 prompt trong Claude Code → `.ai-log/session.jsonl` có dòng mới · `git status` sạch · mở `AGENTS.md` thấy luật.
Bắt đầu việc: mở Claude Code trong `P-073/` và gõ *"Làm task A1.04 theo ../team-ai-kit/plan/tasks/A1.04.md và skill start-task"*. Xong: `python3 ../team-ai-kit/plan/verify.py A1.04` → chỉ tick khi ĐẠT.

## Repo riêng của đội (GitHub private)

**Người giữ kit (1 lần):** tạo repo **Private** trên GitHub (tên gợi ý `team-ai-kit`, KHÔNG đặt trong org của BTC), mời 3 người còn lại.
```bash
git clone team-ai-kit.bundle team-ai-kit      # từ file bundle nhận được (đã có sẵn lịch sử commit)
cd team-ai-kit
git remote set-url origin git@github.com:<tài-khoản>/team-ai-kit.git
git push -u origin main
```
GitHub → Settings → Collaborators: mời 3 người (quyền Write). Bật "Require pull request" cho `main` nếu muốn review sửa luật / skill.
**Mỗi người:** clone cạnh `P-073/` (xem "Bắt đầu" ở trên) rồi `bash ../team-ai-kit/install.sh`.

**Cập nhật kit:** `cd ../team-ai-kit && git pull`. Gắn bằng symlink nên luật / skill / card mới có hiệu lực ngay; chạy lại `install.sh` khi
có thư mục mới (vd. vừa tạo `frontend/`) hoặc khi dùng `--copy` (Windows). Mở lại phiên Claude Code để nạp skill mới.

**Sửa kit:** nhánh + PR như repo chính; trước khi push: `python3 guardrails/validate_kit.py` và `python3 plan/check_conflicts.py`.
Tick task (`plan/<người>.md`) commit thẳng `main` được, mỗi người chỉ sửa file của mình → không xung đột.

## install.sh làm gì

| Bước | Tác dụng | Vào git BTC? |
|---|---|---|
| Luật | symlink `AGENTS.md`, `CLAUDE.md` (gốc) + `src/agents/`, `src/core/`, `src/executor/`, `src/tools/`, `eval/`, `frontend/` `AGENTS.md` | Không (exclude) |
| Skills | symlink `skills/` → `.claude/skills`, `.agents/skills`, `.github/skills` | Không |
| Hook guardrails | `.claude/settings.local.json` — chạy **cùng** hook log AI của BTC trong `.claude/settings.json` (không sửa file BTC) | Không |
| Giấu | ghi danh sách vào `.git/info/exclude` (chỉ máy này) | — |
| pre-commit | `.git/hooks/pre-commit` dùng cấu hình `.generated/pre-commit.yaml`: chặn commit nhầm file kit, luật kiến trúc, ruff như CI BTC, test core, contracts, sơ đồ, gitleaks. **Không đụng `pre-push` của BTC.** | Không |

Chạy lại `install.sh` khi: vừa tạo thư mục mới có luật (vd. `frontend/`), hoặc sau `git pull` kit ở chế độ `--copy`.
Gỡ: `bash ../team-ai-kit/uninstall.sh`.

## Công cụ nào đọc gì

| Tool | Luật | Skill | Chặn |
|---|---|---|---|
| Claude Code | `CLAUDE.md` → `AGENTS.md` | `.claude/skills` | hook PreToolUse / PostToolUse + pre-commit |
| Codex CLI · Cursor · Copilot | `AGENTS.md` (gốc + thư mục) | `.agents/skills` · `.github/skills` | pre-commit |
| Gemini CLI | thêm vào `~/.gemini/settings.json` của bạn: `"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}` (kiểm tên khoá theo bản đang dùng) — KHÔNG sửa `.gemini/settings.json` của repo | — | pre-commit |

## Trong repo này
- `rules/` luật (AGENTS.md) · `skills/` 22 skill (4 skill gốc ngoài đã vá + tài liệu tham khảo ngoài — xem `THIRD_PARTY.md`) · `plan/` kế hoạch, 140 task card (tuần 1 chi tiết, tuần 2–3 nháp), `verify.py` · `guardrails/` hook, pre-commit, kiểm contracts / sơ đồ · `kit.mk` (`make -f ../team-ai-kit/kit.mk check`)
- `plan/` **kế hoạch & task từng người** (tick `[x]`, `python3 plan/progress.py`) · `docs/` spec 49 mục, proposal, quy ước, gap analysis · `diagrams/` script sinh sơ đồ

## Cái gì push lên P-073, cái gì không
| Push lên P-073 (BTC chấm) | Chỉ ở team-ai-kit |
|---|---|
| `src/ tests/ frontend/ eval/ contracts/ migrations/` · config gộp (`ruff.toml`, `requirements.txt`, `Makefile`, `docker-compose.yml`, `.env.example`) · deliverables (README, `docs/architecture*`, `docs/adr/`, WORKLOG, JOURNAL, `eval/results/report.md`, `presentation/`) | luật, skill, guardrails, pre-commit, spec, proposal, kế hoạch, script sinh sơ đồ |

Lưu ý: CI trên GitHub là CI của BTC (ruff + pytest) — luật riêng của đội chỉ chạy trên máy (hook + pre-commit).
