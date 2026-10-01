# 30 · CI/CD & phát hành — Prompt, SOP, KB được phát hành như code

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

```text
PR ─► lint + type check ─► pytest core/ (< 5s) ─► contract test tools/MCP
   ─► build image ─► quét lỗ hổng ─► EVAL GATE: bộ kịch bản (hard = 0 lỗi, soft ≥ ngưỡng, không tụt so với main)
   ─► deploy staging ─► smoke e2e (Playwright) ─► duyệt ─► prod canary 10% ─► theo dõi SLO 30 phút
   ─► 50% ─► 100%          # tự rollback nếu SLO / hard gate vi phạm
```

| Thứ được phiên bản hoá | Ở đâu | Ai duyệt |
| --- | --- | --- |
| System prompt, mô tả tool | agent/prompts/ | Người A + review |
| SOP (skills) | agent/skills/ | Chủ sở hữu nghiệp vụ |
| KB chính sách | kb/ (có effective_from) | Chủ sở hữu nội dung / pháp chế |
| Rule detector, ngưỡng | detect/rules/ | Digital Ops |
| Cấu hình router (model, mức suy luận) | config/router.yaml | Người A + D |

Mỗi câu trả lời lưu release_id gồm phiên bản của tất cả những thứ trên — truy ngược được "câu này sinh ra từ cấu hình nào". Đây là "model registry" của một hệ thống agent.
