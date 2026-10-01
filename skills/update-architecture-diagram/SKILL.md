---
name: update-architecture-diagram
description: Cập nhật sơ đồ kiến trúc trong docs/architecture (Mermaid low-level, draw.io high-level) cho khớp code và contracts. Dùng khi đổi agent/graph.py, subagent, contracts/, schema DB, luồng nghiệp vụ, dịch vụ GCP, hoặc khi CI check_diagrams báo lệch, hoặc task nói vẽ/sửa sơ đồ, architecture diagram.
---

# Cập nhật sơ đồ kiến trúc

Đọc trước: `docs/architecture/README.md` (bảng 9 sơ đồ, quy tắc). Bản nộp BTC: `docs/architecture_diagram.md` (deliverable #3) — nhúng 02, 03 và Mermaid của 04.

## 1. Đổi gì → sửa sơ đồ nào
| Thay đổi | Sơ đồ |
|---|---|
| Node / cạnh / subgraph LangGraph | 04 Agent Flow (`make -f ../team-ai-kit/kit.mk diagrams-export` sinh bản tự động, rồi chỉnh bản vẽ tay) + chép khối Mermaid mới vào `docs/architecture_diagram.md` · 02 nếu thêm/bớt khối lớn |
| Tool, API, sự kiện (`contracts/`) | 05, 06 (tên gọi phải đúng hợp đồng) · 02 nếu thêm hệ thống mới |
| Trạng thái journey / slot / token | 07 |
| Bảng / cột DB (migration) | 08 |
| Pipeline dữ liệu, eval, baseline | 09 |
| Dịch vụ GCP, mốc triển khai | 03 Deployment (đổi nhãn MVP / T1–2 / T3 / Prod) |

## 2. Năm quy tắc vẽ (CI kiểm 2–4)
1. Tên node nói đúng chức năng — không "Service A"; low-level dùng đúng tên trong `contracts/` và code.
2. Nhóm bằng subgraph / vùng: Frontend · Backend · Agent · An toàn & thực thi · Dữ liệu · Tích hợp · Bên ngoài.
3. Mọi mũi tên có nhãn dữ liệu; hai chiều = 2 mũi tên, mỗi chiều một nhãn.
4. Luồng tuần tự đánh số `(1) (2)…`, nhánh `(5a)(5b)`, ngoại lệ `(n')`, luồng phụ `(P1)` `(H1)`; sequence dùng `autonumber`.
5. Mỗi sơ đồ một ý; high-level ≤ ~20 khối — thừa thì ghi chú bên dưới hoặc tách sơ đồ mới.

## 3. Sửa Mermaid (04–09)
- Sửa text trong khối ```mermaid. Tên tool, sự kiện, bảng dùng ĐÚNG tên trong `contracts/` và code.
- Giữ lớp màu: `llm` tím · `code` xanh lá · `write` cam · `human` vàng · dữ liệu xanh dương.
- Tránh ký tự `;` và `#` trong nhãn sequence diagram (Mermaid hiểu sai). Nhãn có ngoặc → đặt trong `"..."`.
- Mỗi cạnh flowchart dạng `a -->|"(n) nhãn"| b`. Xem trước: preview VS Code hoặc mermaid.live.

## 4. Sửa draw.io (01–03)
- Mở `.drawio.svg` bằng app.diagrams.net hoặc extension Draw.io Integration (VS Code); kéo thả, sửa nhãn.
- Lưu lại đúng dạng `.drawio.svg` (ảnh + dữ liệu sửa được). KHÔNG xuất sang PNG/SVG thường đè lên — CI sẽ báo.
- Icon GCP: thư viện "Google Cloud Platform" (`mxgraph.gcp2`). Nhãn mốc: MVP · T1–2 · T3 · Prod.
- High-level giữ ≤ ~15 khối chính; chi tiết đưa xuống sơ đồ Mermaid.
- AI coding agent không kéo thả được: có thể sửa nhãn chữ trong XML (thuộc tính `content`) nếu thay đổi nhỏ, còn đổi bố cục → nhờ người.

## 5. Kiểm
- `make -f ../team-ai-kit/kit.mk diagrams`: README đủ file · tool/sự kiện khớp contracts · drawio còn sửa được và không nén · quy tắc 2–4.
- Mô tả PR: ghi sơ đồ đã sửa. Script sinh bản đầu draw.io: `../team-ai-kit/diagrams/drawio/`.
