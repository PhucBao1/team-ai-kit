# 14 · Câu hỏi mentor & giám khảo — FAQ

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Đáp ứng đủ: hội thoại nhiều bước, KB, tool, handoff kèm tóm tắt, không bịa, xác nhận trước (§01, §06). Phần chủ động là mở rộng theo góp ý của mentor, dùng chung một Decision Engine — không phải một hệ thống khác.

Không. Tín hiệu đến từ xe, trạm sạc, xưởng, kho, bảo hành. Khách nhắn chỉ là một cửa vào. Giá trị lớn nhất nằm ở cửa sổ in-flight: việc đã bắt đầu, đang âm thầm dừng, trước khi khách phải giục.

Không. Agent nhận cảnh báo đã được nền tảng telematics và trạm sạc chuẩn hoá. Chỉ 2/7 nguồn tín hiệu là IoT; phần lớn use case đến từ hệ thống doanh nghiệp (lịch, kho, bảo hành, billing).

Chính sách công khai của VinFast/V-Green cho KB; dữ liệu tiếng Việt (CSConDa, UIT-ViOCD, PhoATIS của VinAI) cho ngôn ngữ; phỏng vấn chủ xe Việt cho kịch bản thật; VED, ACN-Data, NHTSA làm nguyên liệu tín hiệu; thế giới giả lập có lỗi tiêm có nhãn cho phần nội bộ (§11). Mọi quy trình nội bộ ghi rõ là giả định.

Agent không kết luận bảo hành — chỉ nói đủ điều kiện sơ bộ theo chính sách, kèm nguồn, xưởng kết luận. Claim check tất định chặn mọi con số không có trong KB/tool. Grounding violation là hard gate = 0.

Không qua LLM. Mức CRITICAL dùng mẫu tin do hãng duyệt, chuyển tổng đài 24/7 ngay, đề nghị cứu hộ khi khách đồng ý. Agent không chẩn đoán, không trấn an.

Đo bằng ACRC — chi phí trên mỗi việc được giải quyết và xác minh. L0 tất định lọc phần lớn event; nhiều ca (UC4, đường tất định của UC2, claim có cấu trúc ở UC5) gần như không cần LLM. Ước tính theo giá Gemini niêm yết 9/2026: một hội thoại 6 lượt ≈ 1.300–2.700 đ, một ca proactive ≈ 1.200 đ; ở quy mô ~165.000 việc/tháng, tổng cả hạ tầng GCP ≈ 270–430 triệu đ/tháng, tức ≈ 1.600–2.600 đ mỗi việc. Ba tuần cuộc thi ≈ 13–26 triệu đ, phần lớn là chạy eval. Cách tính chi tiết: file technical §36.

Upsell cho khách đang có việc kẹt làm mất niềm tin; phần lớn upsell không cần LLM agent; tin marketing cần đồng ý riêng. Nền móng (hội thoại + Recovery) và Arbitration phải có trước.

Hệ thống được thiết kế theo loop engineering: vòng agent, vòng kiểm tra, vòng kích hoạt theo sự kiện (chính là phần proactive), vòng cải thiện từ trace (có người duyệt), và vòng outcome kéo dài nhiều ngày bằng durable execution. Stack dùng MCP, OpenTelemetry GenAI, eval bằng giả lập — nhưng MVP cố ý giữ gọn: chỉ dùng thứ cần cho từng vòng (§05.1).

Ba lớp. (1) Baseline trên cùng thế giới giả lập, cùng kịch bản: B0 quy trình hiện tại không AI, B1 chatbot FAQ + RAG, B2 một agent gọi thẳng mọi tool, B3 bỏ lần lượt từng thành phần (ablation). (2) Benchmark công khai: τ²/τ³-bench cho lõi agent CSKH, VN-MTEB để chọn embedding tiếng Việt, PhoATIS cho triage. (3) Tham chiếu ngành ở §10. Chi tiết: file technical §23.

Đúng, và đề xuất dùng lại có chủ đích (BMW Proactive Care, Tesla gửi trước linh kiện, Rivian ưu tiên lưu động). Điểm mới nằm ở: cứu việc đang chạy dở giữa các hệ thống (lịch lệch kho, claim kẹt, lời hứa bị quên); một bộ não cho cả hội thoại theo đề bài lẫn chủ động, có xác nhận và guardrail tất định; "xong" được xác minh bằng dữ liệu xe; và bối cảnh Việt Nam, nơi chưa doanh nghiệp nào triển khai AI agent CSKH ở quy mô lớn.

Không đặt mục tiêu đó. Bài học Klarna: giảm nhân sự theo tỷ lệ tự động hoá làm CSAT giảm và phải tuyển lại. Đề xuất bắt đầu bằng copilot cho nhân viên, giữ đội chuyên gia cho ca khó, và chỉ mở rộng tự động khi CSAT không giảm.

Xe có kết nối: ứng dụng VinFast công khai các tính năng xem pin, trạng thái sạc, vị trí từ xa, E-call và cập nhật phần mềm từ xa (FOTA). Phạm vi chi tiết — mã lỗi có gửi về theo thời gian thực không, tần suất — không công khai, nên bài ghi rõ là giả định và cần hãng xác nhận (§07).

Phần chính đào sâu một engine chăm sóc chủ động: UC1 (flagship, sáu quyết định đặc thù xe điện) đến mức prototype và bằng chứng; UC2, UC3 dùng chung engine ở mức demo-ready; UC4–UC6 là spec và kịch bản. Các trụ cột và nghiệp vụ khác nằm ở phụ lục như tầm nhìn, không phải phạm vi xây.

Có. Theo Luật Trí tuệ nhân tạo (hiệu lực 1/3/2026), agent tự giới thiệu là AI, tin tự động có nhãn, và luôn có lựa chọn gặp nhân viên. Khách có thể chọn không nhận tin chủ động do AI soạn.

Có trong thiết kế: tổng đài giọng nói và trợ lý trên xe dùng chung Decision Engine; khách chụp đèn cảnh báo gửi qua Zalo, agent đối chiếu với dữ liệu xe. MVP ưu tiên chat, giọng nói ở Level 4.5.

Nội dung khách luôn là dữ liệu, không phải lệnh; quyền tool không phụ thuộc hội thoại; hành động quan trọng qua validator và xác nhận. Bộ kiểm thử có nhóm kịch bản tấn công riêng.

Không. Đây là đề xuất cho cuộc thi, lấy cảm hứng từ hệ sinh thái VinFast/V-Green, dùng thông tin công khai; quy trình nội bộ là giả định.
