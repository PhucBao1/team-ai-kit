---
name: ui-ux-pro-max
description: Kiến trúc UX cho frontend P-073 — kiến trúc thông tin, mẫu UX sản phẩm, cấu trúc responsive, sinh và tổ chức design system / component. Bản vendored của nextlevelbuilder/ui-ux-pro-max-skill v2.13.0 (ghim commit, dữ liệu + script Python offline), bọc luật nhóm. Dùng khi thiết kế cấu trúc màn / luồng cho Landing, trải nghiệm khách hoặc Console CSKH, hoặc khi đề xuất thay đổi cho design system team-ai-kit/design-system/proactive-care/ (chỉ đề xuất, vào bằng PR). Không dùng để chốt cá tính thị giác (taste-skill), motion (emil-design-eng) hay audit cuối (web-design-guidelines).
---
<!-- Modified by P-073 team, 2026-10-03: lớp bọc luật nhóm; bản gốc y nguyên ở references/upstream-SKILL.md -->

# ui-ux-pro-max — kiến trúc UX (bọc luật nhóm)

Bản gốc: `references/upstream-SKILL.md` (nextlevelbuilder/ui-ux-pro-max-skill @ `09170eec67`, v2.13.0, không sửa).
`data/`, `scripts/*.py`, `references/{quick-reference,pro-rules}.md` y nguyên bản gốc. Nguồn, hash: `NOTICE.md`.
Bản đồ cả bộ skill + thứ tự ưu tiên: `../team-ai-kit/docs/frontend/skill-stack.md`.

## Luật nhóm P-073 (thắng nội dung bản gốc)

**Thứ tự ưu tiên:** yêu cầu sản phẩm (spec `20-ui.md` / `21-fe.md`, card, contracts) > design system nội bộ
(`add-frontend-screen/references/taste-rules.md`, `frontend/AGENTS.md`, token CSS, `team-ai-kit/design-system/`)
> taste-skill > **ui-ux-pro-max** > emil-design-eng > web-design-guidelines.

**Đường dẫn script** — bản gốc ghi `${CLAUDE_PLUGIN_ROOT}/.claude/skills/...` (chỉ đúng khi cài dạng plugin). Ở đây chạy từ gốc P-073:
```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <domain>
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system -p "<Bề mặt>"
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --stack react
```
Chỉ dùng thư viện chuẩn Python, đọc CSV cục bộ, không gọi mạng. Không chạy `uipro`, `npm install -g ui-ux-pro-max-cli`, `/plugin install`.

**Không `--persist`, không `--force`.** Design system đã có, do người duyệt: `team-ai-kit/design-system/proactive-care/`
(MASTER + `pages/`). Chạy script **không** persist để lấy đề xuất; đề xuất nào được nhận thì đưa vào design system bằng PR
theo `docs/frontend/design-governance.md` §4. Không bao giờ ghi vào P-073.

**Ghi đè cụ thể:**
- Stack `react` (React + TS + Vite + Tailwind). Bỏ gợi ý Next.js / RSC / thư viện chưa có trong `package.json`.
- Bảng màu, phông bản gốc gợi ý chỉ là tham khảo: màu là token nội bộ, AA 2 theme; phông theo `taste-rules.md` (tự host, không Google Fonts `@import`).
- Vùng chạm ≥44px, `lang="vi"`, chữ thân ≥16px (màn khách 18px) — luật nhóm thắng mọi số liệu trong `data/`.
- Mục motion / GSAP preset trong bản gốc: chỉ để biết có gì; chốt motion ở `emil-design-eng`. Không thêm GSAP.
- Dial `--variance/--motion/--density`: lấy đúng giá trị ở `design-system/proactive-care/MASTER.md` §2.1 cho bề mặt đang làm.

## Vai trò theo bề mặt
| Bề mặt | Việc chính |
|---|---|
| Landing / Story page | Cấu trúc section, mạch kể, CTA, responsive |
| Trải nghiệm khách | Luồng (chat → xác nhận → theo dõi việc), trạng thái loading / empty / lỗi, form, mobile trước |
| Console CSKH | Kiến trúc thông tin, mật độ dữ liệu, điều hướng bàn phím, bảng / hàng đợi |

## ui-ux-pro-max KHÔNG quyết định
Cá tính thị giác / hướng chữ (taste-skill) · thời lượng, easing (emil-design-eng) · kết luận audit cuối ·
yêu cầu sản phẩm, API, contracts, stack · ghi file vào P-073.
