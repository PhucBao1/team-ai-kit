# Mục lục — Technical spec & kế hoạch build


## Phần 0 — Định hướng — bám đề, phạm vi, mốc thời gian

- [Rà nghiệp vụ VinFast + so sánh hãng nước ngoài (03/10, có nguồn)](../research/2026-10-03-nghiep-vu-vinfast.md)
- [01 · Bám đề — Có lạc đề không? — truy vết từ yêu cầu của đề đến code và phép đo](01-bamde.md)
- [02 · Phạm vi & mốc — Hai tuần làm đủ, tuần 3 chỉ cải thiện](02-scope.md)

## Phần A — Kiến trúc — một bức tranh, năm vòng lặp, bốn luồng

- [03 · Kiến trúc tổng thể — Sáu tầng, một bộ não, một điểm ghi duy nhất](03-overview.md)
- [04 · Năm vòng lặp — Mỗi vòng: nằm ở đâu trong code, dừng khi nào, tốn bao nhiêu](04-loops.md)
- [05 · Luồng xử lý chi tiết — Bốn luồng, từng bước, ai gọi ai](05-flows.md)
- [06 · Triển khai: MVP → production — MVP gọn, production mở rộng theo cùng ranh giới](06-arch.md)
- [07 · Production trên GCP — Từng dịch vụ, dùng để làm gì](07-gcp.md)

## Phần B — Thành phần — đi từ dữ liệu lên tới giao diện

- [08 · Mô hình dữ liệu — Schema tối thiểu cho UC1, đủ để mở rộng](08-data.md)
- [09 · Sự kiện & detector — Một định dạng sự kiện chung, rule tất định](09-events.md)
- [10 · Hợp đồng dữ liệu & chất lượng — Sự kiện sai định dạng có thể làm detector báo sai hàng loạt](10-datacontract.md)
- [11 · Tools — Chữ ký tool — chốt sáng 28/9](11-tools.md)
- [12 · MCP servers & A2A — Mỗi hệ thống gốc một MCP server, quyền theo người dùng thật](12-mcp.md)
- [13 · Agent & coordinator — Một agent gốc cho MVP, tách subagent ở tuần 1](13-agent.md)
- [14 · Multi-agent — Tách agent khi có lý do — agent đề xuất, code tất định thực thi](14-multiagent.md)
- [15 · Model router & context engineering — Dùng trí tuệ rẻ nhất đủ tin cậy cho từng việc](15-router.md)
- [16 · Knowledge, RAG & memory — Trả lời đúng phiên bản, đúng điều khoản, nhớ đúng thứ được phép nhớ](16-knowledge.md)
- [17 · Lõi tất định & Executor — Bốn module quyết định mọi thứ quan trọng — không có LLM bên trong](17-core.md)
- [18 · Model triage & MLOps (tuần 3) — Bộ phân loại triage tiếng Việt: huấn luyện, phục vụ, giám sát, huấn luyện lại](18-mleng.md)
- [19 · API contract — Frontend làm với mock ngay từ sáng 28/9](19-api.md)
- [20 · Giao diện — Bốn màn hình trên một trang demo](20-ui.md)
- [21 · Frontend engineering — Ba màn hình realtime, người lớn tuổi dùng được, mạng yếu không vỡ](21-fe.md)

## Phần C — Chất lượng, dữ liệu & vận hành — làm sao biết nó đúng và giữ nó đúng

- [22 · Chiến lược đánh giá 5 tầng — Đo ở năm tầng: module → agent → end-to-end → hệ thống → kinh doanh](22-evalmod.md)
- [23 · Harness kịch bản — Từ 10 kịch bản chạy tay đến 150 kịch bản tự động](23-eval.md)
- [24 · Đánh giá RAG — Tách lỗi tìm kiếm khỏi lỗi sinh câu trả lời](24-rageval.md)
- [25 · Đánh giá AI agent — Đo kết quả, đo đường đi, đo độ tin cậy — và đo cả multi-agent](25-agenteval.md)
- [26 · Chiến lược kiểm thử — Bảy tầng kiểm thử, từ hàm thuần đến sự cố LLM](26-testing.md)
- [27 · AI data engineering — Dữ liệu cho AI cũng cần pipeline, phiên bản và kiểm soát chất lượng](27-aidata.md)
- [28 · Data science — Thiết kế thí nghiệm, chọn ngưỡng bằng chi phí, dự báo, phân tích thời gian](28-ds.md)
- [29 · Observability & SLO — Một trace cho một việc, kể cả khi việc kéo dài nhiều ngày](29-obs.md)
- [30 · CI/CD & phát hành — Prompt, SOP, KB được phát hành như code](30-cicd.md)
- [31 · Bảo mật — Mỗi service một danh tính, quyền tối thiểu, chặn ở tầng thực thi](31-security.md)
- [32 · Vận hành & runbook — Khi có sự cố, ai làm gì trong 15 phút đầu](32-ops.md)

## Phần D — Kỹ thuật, scale & tối ưu

- [33 · Tech stack tổng hợp — Toàn bộ tech stack ở một chỗ: mỗi thứ giải quyết vấn đề gì](33-stack.md)
- [34 · Kỹ thuật AI & framework — Mỗi kỹ thuật có chỗ dùng cụ thể — và có kỹ thuật cố ý không dùng](34-aitech.md)
- [35 · Kỹ thuật lập trình — Async đầu-cuối, ghi nhiều hệ thống an toàn, chịu được lỗi](35-prog.md)
- [36 · Tải & chi phí (ước tính) — Một phép tính để biết kiến trúc có đủ và có lãi không](36-capacity.md)
- [37 · Các bước scale — Năm giai đoạn — mỗi giai đoạn một nút thắt khác nhau](37-scale.md)
- [38 · Tối ưu — Độ trễ, chi phí, chất lượng — đo trước, tối ưu sau](38-optimize.md)

## Phần E — Đội, kế hoạch 3 tuần & roadmap

- [39 · Ma trận kỹ năng theo vai trò — Mỗi vai trò gắn với một sản phẩm thật, một người phụ trách](39-skills.md)
- [40 · Đối chiếu kỹ năng hạ tầng ML — Dùng gì, dùng kiểu khác, và không cần gì](40-curriculum.md)
- [41 · Cấu trúc repo — Một monorepo, ranh giới rõ để 4 người không giẫm chân](41-repo.md)
- [42 · Kế hoạch 3 tuần — Tuần 1 dựng xương sống, tuần 2 làm đủ, tuần 3 cải thiện](42-plan3w.md)
- [43 · Chi tiết 3 ngày MVP (28–30/9) — Ngày nào cũng kết thúc bằng một thứ chạy được](43-plan3.md)
- [44 · Backlog task — Nhận việc ngay — MVP chia theo ngày, tuần 1–2 theo epic](44-backlog.md)
- [45 · Kịch bản demo — Một câu chuyện, ba phía, mọi yêu cầu của đề](45-demo.md)
- [46 · Rủi ro & dự phòng — Chuẩn bị cho những gì chắc chắn sẽ trục trặc](46-risk.md)
- [47 · Quyết định kiến trúc (ADR) — Ghi lại vì sao — để trả lời giám khảo và để không cãi lại](47-adr.md)
- [48 · Definition of Done & quy ước — Thế nào là "xong" cho một task](48-dod.md)
- [49 · Roadmap kỹ thuật 24 tháng — Từ demo tới nền tảng agent của hệ sinh thái](49-future.md)
