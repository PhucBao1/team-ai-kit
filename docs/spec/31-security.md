# 31 · Bảo mật — Mỗi service một danh tính, quyền tối thiểu, chặn ở tầng thực thi

> Trích từ Technical spec & kế hoạch build. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

| Service account | Được phép | Không được |
| --- | --- | --- |
| `sa-api` | Gọi agent, đọc session, ký token (secret HMAC) | Gọi thẳng MCP ghi |
| `sa-agent` | Gọi model; gọi MCP đọc; gọi MCP ghi *kèm token* | Đọc identity vault; đọc secret HMAC |
| `sa-mcp-*` | Truy cập đúng một hệ thống gốc | Hệ thống khác |
| `sa-detector` | Đọc Pub/Sub, đọc journey, gọi agent | Gửi tin trực tiếp cho khách |
| `sa-analytics` | BigQuery dữ liệu đã ẩn danh | AlloyDB bản gốc |

#### Prompt injection

Đánh dấu dữ liệu không tin cậy; sàng lọc đầu vào/đầu ra bằng lớp chuyên dụng (ví dụ Model Armor của Google Cloud hoặc tương đương); quyền tool không phụ thuộc hội thoại; red-team mỗi sprint.

#### Bí mật & khoá

Secret Manager, không key trong repo; CMEK cho AlloyDB / BigQuery; xoay khoá HMAC định kỳ.

#### Mạng

VPC Service Controls quanh dữ liệu; Cloud Armor trước API; MCP server không public.

#### Audit bất biến

audit_log append-only có chuỗi hash (mỗi bản ghi chứa hash bản trước) + Cloud Audit Logs; không ai sửa được lịch sử quyết định của agent.

#### Chuỗi cung ứng

Quét lỗ hổng image; pin phiên bản dependency; SBOM; chỉ deploy image đã ký.

#### Nhân viên

SSO (Identity Platform / IAP), RBAC theo xưởng; console chỉ thấy khách của xưởng mình.
