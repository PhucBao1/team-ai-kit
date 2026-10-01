# Nội dung bên ngoài trong team-ai-kit

Repo này **private** (chỉ 4 thành viên). Mỗi thư mục có nội dung ngoài đều giữ `LICENSE` gốc + `NOTICE.md` (nguồn, commit, đã sửa gì).
Không đưa các thư mục dưới đây vào repo BTC. Muốn công khai kit → đọc lại điều khoản từng license (CC BY-SA yêu cầu bản chuyển thể giữ CC BY-SA).

| Thư mục | Nguồn (commit) | License | Loại |
|---|---|---|---|
| `skills/langgraph-human-in-the-loop/` | langchain-ai/langchain-skills (a76fef33ed) | MIT | skill, đã vá (bỏ TS, luật token) |
| `skills/add-langgraph-node/references/langgraph-*.md` | langchain-ai/langchain-skills (a76fef33ed) | MIT | tham khảo |
| `skills/web-accessibility/` | addyosmani/web-quality-skills (afa8da9421) | MIT | skill, đã vá |
| `skills/playwright-cli/` | microsoft/playwright-cli (b85c7a736b) | Apache-2.0 | skill, đã vá (file sửa có dòng Modified) |
| `skills/add-frontend-screen/references/visual-design.md` | anthropics/skills `frontend-design` (8a1541c4a3) | Apache-2.0 | tham khảo, đã vá |
| `skills/property-based-testing/` | trailofbits/skills (82fe822625) | CC BY-SA 4.0 | skill, chuyển thể (cũng CC BY-SA 4.0) |
| `skills/security-review/references/{fastapi,react}.md` | openai/skills `security-best-practices` (49f948faa9) | Apache-2.0 | tham khảo, đã cắt |
| `skills/security-review/references/{threat-model,insecure-defaults,sharp-edges-python}.md` | openai/skills, trailofbits/skills, wshobson/agents | Apache-2.0 / CC BY-SA 4.0 / MIT | chuyển thể — xem NOTICE trong thư mục |
| `skills/db-migration/references/postgres-best-practices/` | supabase/agent-skills (544bfc56c8) | MIT | tham khảo (không tự kích hoạt) |

Chỉ lấy Ý (diễn đạt lại, có ghi nguồn cuối file, không chép văn bản): obra/superpowers (MIT), Leonxlnx/taste-skill (MIT),
vercel-labs/agent-skills (MIT), wshobson/agents (MIT), google/skills (Apache-2.0), anthropics/skills `mcp-builder` (Apache-2.0).

**Không chép (license "All rights reserved"):** skill `docx/pdf/pptx/xlsx` của Anthropic, plugin trong anthropics/claude-code.
Ai cần làm pitch deck: tự cài trên máy mình `/plugin marketplace add anthropics/skills` → `/plugin install document-skills@anthropic-agent-skills` (phạm vi user, không phải project).

**Đã đọc và KHÔNG dùng** (lý do trong lịch sử thảo luận): modern-python & uv-package-manager (thay pip, hook chặn pip), Superpowers cài nguyên bộ
(hook ép gọi skill), fastapi-templates (Pydantic v1), langchain-architecture / rag-implementation / prompt-engineering (API cũ),
web-design-guidelines (tải luật từ mạng lúc chạy), LambdaTest playwright (khoá vào cloud trả phí), pr-review-toolkit / commit-commands / feature-dev,
các skill Google Cloud (mặc định `--allow-unauthenticated`, `--quiet`).

Cập nhật bản ngoài: chỉ khi cần; chép lại ở commit mới, vá lại theo `NOTICE.md`, chạy `python3 guardrails/validate_kit.py`.
