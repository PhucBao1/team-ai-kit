# Use case chi tiết (PL-A) — dữ liệu từ explorer trong proposal

> Trích tự động từ mảng USECASES của proposal.


## UC1 — Đến xưởng rồi phải về

**customer:** Tôi xin nghỉ nửa ngày, lái xe đến xưởng đúng hẹn — rồi được bảo linh kiện chưa về, hẹn hôm khác.
**outcome:** Khách biết trước 2 ngày, chọn phương án phù hợp, sửa đúng hẹn — không mất công đi lại.
**type:** T1 · Lệch trạng thái · Sự cố & bảo hành · MVP
**name:** Service Appointment Rescue — lịch sửa lệch kho linh kiện
**context:** Khách đặt lịch sửa / bảo hành qua app, tổng đài hoặc qua agent. Lịch được xác nhận theo công suất xưởng, nhưng linh kiện nằm ở ERP kho. Khi linh kiện bị điều cho xe khác (ví dụ xe triệu hồi), hàng về trễ hoặc giữ sai mã, lịch vẫn "đã xác nhận" — khách đến xưởng mới biết.
**actors:**
- Chủ xe
- Cố vấn dịch vụ (CVDV)
- Điều phối xưởng
- Kho phụ tùng
- CSKH
**systems:**
- App / tổng đài
- DMS xưởng
- ERP kho
- Telematics
- CRM
**happy:**
- Xe báo mã lỗi / khách yêu cầu
- Chẩn đoán sơ bộ, xác định linh kiện theo số khung
- Đặt lịch theo công suất xưởng
- Giữ linh kiện cho lệnh sửa chữa
- Linh kiện có mặt trước ngày hẹn
- Sửa, bàn giao, theo dõi mã lỗi
**brk:** 3
**breakpoint:** Reservation linh kiện không ràng buộc với lịch hẹn: kho huỷ / điều chuyển, ETA trễ, hoặc khách đổi lịch mà reservation vẫn ở ngày cũ.
**rules:**
- Lịch cần linh kiện chỉ "xác nhận" khi linh kiện đã được giữ
- Linh kiện không về trước hẹn 48h → báo khách và đề xuất phương án
- Xe có cảnh báo an toàn được ưu tiên linh kiện
- Đổi lịch / đổi xưởng phải được khách xác nhận (mức 2)
**signal:** ON part_reservation.cancelled OR eta_changed
  IF appointment.status = "confirmed"
  AND appointment.start − now < 72h
  THEN candidate(T1)
Sweep hằng ngày: mọi lịch trong 72h phải có reservation hợp lệ
**action:** Tra tồn kho các xưởng, slot trống, khoảng cách → 2–3 phương án xếp hạng theo thời gian, quãng đường, mức nghiêm trọng → validator → khách chọn & xác nhận → giữ slot + linh kiện, chuyển lệnh sửa chữa. Không tự đổi lịch khi chưa có xác nhận.
**message:** Chào anh Minh, linh kiện cho lịch 9:00 thứ Bảy của anh tại Long Biên chưa về kịp. Bên em có 2 phương án: (1) giữ giờ, chuyển sang xưởng Gia Lâm (6 km) đã có sẵn linh kiện; (2) dời sang 9:00 thứ Ba 6/10 tại Long Biên. Anh chọn phương án nào ạ?
**verify:** Lịch mới được khách xác nhận · linh kiện giữ đúng mã · sửa đúng hẹn · telematics 14 ngày không ghi nhận lại mã lỗi
**kpi:** Wasted Visit Rate, Pre-Chase Recovery, Time-to-Recovery
**cost:**
- Khách mất nửa ngày đến xưởng rồi về
- Slot xưởng lãng phí
- Khiếu nại tại chỗ, niềm tin giảm mạnh
**trace:**
- t: T5 14:02 · l: L0 · ttl: Phát hiện lệch · d: ERP: reservation bơm làm mát pin cho RO-5581 bị huỷ (điều chuyển xe triệu hồi); SA-20931 vẫn "confirmed", còn 67 giờ · tok: 0
- t: 14:02 · l: L1 · ttl: Triage · d: Mã lỗi mức WARNING (không nguy hiểm) → RESCHEDULE_NEEDED · tok: 0
- t: 14:03 · l: Tool · ttl: Tra dữ liệu · d: Tồn kho 5 xưởng · slot thứ Bảy / thứ Ba · khoảng cách từ địa chỉ đăng ký · tok: 0
- t: 14:03 · l: L2 · ttl: Lập phương án · d: Gia Lâm có linh kiện + slot 9:00 thứ Bảy; Long Biên ETA thứ Hai → slot thứ Ba. Xếp hạng 2 phương án · tok: 2500
- t: 14:03 · l: Validator · ttl: Kiểm tra · d: part_matches_vin ✓ · technician_certified ✓ · part_reserved (tạm) ✓ · slot_locked ✓ · tok: 0
- t: 14:04 · l: Inform · ttl: Hỏi khách · d: Tin 2 phương án + nút "Gặp nhân viên" qua app · tok: 300
- t: 14:06 · l: Customer · ttl: Khách phản hồi · d: "Cho anh nói chuyện với người" → handoff card cho CVDV Hải · tok: 400
- t: 14:21 · l: Act · ttl: Thực hiện sau xác nhận · d: Khách chọn phương án 1 qua CVDV → chuyển lệnh sửa chữa sang Gia Lâm, giải phóng slot Long Biên · tok: 0
- t: +14 ngày · l: Verify · ttl: Xác minh bằng dữ liệu xe · d: Sửa xong 11:30 thứ Bảy; telematics 14 ngày không ghi nhận lại mã lỗi → RECOVERED · tok: 0
- t: Tuần · l: Learn · ttl: Root cause · d: Phần lớn reservation bị huỷ do điều chuyển không kiểm tra lịch hẹn → đề xuất ràng buộc trong ERP · tok: 0


## UC3 — Kẹt ở trạm sạc, không ai trả lời

**customer:** 9 giờ tối, pin còn 6%, trụ sạc không nhận. Tôi bấm gặp nhân viên rồi ngồi chờ mãi không ai trả lời.
**outcome:** Trong vài phút có người gọi, biết ngay trạm gần nhất còn trống, và được hỏi có cần cứu hộ.
**type:** T3 · Rơi quyền sở hữu · Sử dụng & sạc · Quick win
**name:** Handoff rơi khi khách đang kẹt ở trạm sạc
**context:** Chatbot trong app xử lý câu hỏi đơn giản. Khi khách cần người, bot chuyển sang live chat. Ngoài giờ live chat, handoff có thể rơi — nguy hiểm nhất khi khách đang kẹt: pin thấp, trụ sạc không nhận.
**actors:**
- Chủ xe
- Chatbot
- Tổng đài 24/7
- Vận hành trạm sạc
**systems:**
- Chatbot
- Live chat queue
- CSMS trạm sạc
- Telematics
- Cứu hộ
**happy:**
- Khách yêu cầu gặp người
- Bot tạo handoff kèm tóm tắt
- Queue nhận yêu cầu
- Nhân viên nhận trong 5 phút
- Ngoài giờ: khẩn → tổng đài 24/7; thường → ticket + hẹn giờ
**brk:** 2
**breakpoint:** Queue live chat đóng ngoài giờ, không có fallback → không ticket, không owner, khách chờ trong cửa sổ chat.
**rules:**
- Mọi handoff có owner trong 2 phút
- Khách đang kẹt (SoC thấp, tại trạm lỗi, xe không khởi động) → luồng khẩn 24/7
- Không tự gọi cứu hộ khi khách chưa đồng ý
**signal:** IF handoff_requested
  AND NOT (live_session OR ticket) SAU 2 phút
  THEN candidate(T3)
Mức khẩn: SoC, vị trí tại trạm, trạng thái trụ
**action:** Xác định mức khẩn từ dữ liệu xe + trạm → chuyển tổng đài 24/7 kèm tóm tắt → gửi khách trụ gần nhất đang trống (dữ liệu thời gian thực) → hỏi có cần cứu hộ.
**message:** Anh Tuấn ơi, em đã chuyển anh cho tổng đài viên trực 24/7, anh sẽ nhận cuộc gọi trong vài phút. Trong lúc chờ: trạm gần nhất đang hoạt động cách anh 1,2 km, còn 3 cổng trống. Anh có cần em gửi yêu cầu cứu hộ không?
**verify:** Tổng đài gọi trong 5 phút · CSMS ghi nhận phiên sạc mới thành công · không có contact lặp
**kpi:** Handoff có owner trong 2 phút, thời gian khách bị kẹt
**cost:**
- Khách kẹt ngoài đường ban đêm
- Mất niềm tin vào xe điện nói chung
- Contact lặp qua hotline, mạng xã hội
**trace:**
- t: 21:14 · l: L0 · ttl: Phát hiện · d: handoff_requested 21:12, không có session hay ticket sau 2 phút · tok: 0
- t: 21:14 · l: L1 · ttl: Mức khẩn · d: SoC 6% · GPS tại trạm · "sạc không nhận" → URGENT · tok: 200
- t: 21:14 · l: Tool · ttl: Tra trạm · d: CSMS: trụ #4 Faulted; trạm cách 1,2 km còn 3 cổng Available · tok: 0
- t: 21:14 · l: Act · ttl: Chuyển 24/7 · d: Tạo cuộc gọi ưu tiên cho tổng đài kèm tóm tắt (model nhỏ) · tok: 500
- t: 21:15 · l: Inform · ttl: Báo khách · d: Mẫu tin khẩn + trạm gần nhất + câu hỏi cứu hộ · tok: 0
- t: 21:19 · l: Verify · ttl: Xác minh · d: Tổng đài gọi 21:17; CSMS ghi nhận phiên sạc mới 21:31 → RECOVERED · tok: 0
- t: Tuần · l: Learn · ttl: Root cause · d: Trụ #4 lỗi 3 lần/tuần → ticket bảo trì; queue đêm cần fallback cố định · tok: 0
**note:** Gần như không cần LLM — minh hoạ nguyên tắc cost-aware. Dữ liệu xe và trạm biến một handoff bình thường thành phản hồi đúng mức khẩn.


## UC2 — Chờ mãi không thấy gọi báo giá

**customer:** Sáng gửi xe, xưởng hứa chiều gọi báo giá. Đến tối vẫn không ai gọi, tôi phải tự gọi hỏi.
**outcome:** Khách nhận báo giá trong ngày, duyệt ngay trong app, lấy xe đúng dự kiến.
**type:** T2 · Lời hứa bị quên · Bảo dưỡng · Wave 2
**name:** Lời hứa báo giá của cố vấn dịch vụ bị quên
**context:** Xe vào xưởng có hạng mục ngoài bảo hành. CVDV hứa "chiều em gọi báo giá". Báo giá đã lập trong DMS nhưng không ai gọi; xe nằm chờ duyệt, khách chờ điện thoại.
**actors:**
- Chủ xe
- CVDV
- Trưởng xưởng
**systems:**
- DMS xưởng
- Tổng đài / STT
- Zalo OA / app
- CRM task
**happy:**
- Kiểm tra xe
- Lập báo giá trong DMS
- CVDV liên hệ khách
- Khách duyệt từng hạng mục
- Sửa và bàn giao
**brk:** 2
**breakpoint:** Bước liên hệ là thủ công; lời hứa chỉ nằm trong cuộc gọi. DMS không biết có lời hứa.
**rules:**
- Báo giá chờ duyệt > 4 giờ làm việc → nhắc CVDV
- Không sửa hạng mục ngoài bảo hành khi chưa có khách duyệt
- Giá chỉ lấy nguyên văn từ báo giá DMS
**signal:** RO ở "chờ khách duyệt" > 4h AND không có liên lạc ra
+ L2 trích cam kết từ transcript cuộc gọi
**action:** Nhắc CVDV và trưởng xưởng; CVDV vẫn không liên hệ được → gửi khách báo giá nguyên văn từ DMS trong app, duyệt từng hạng mục (duyệt = xác nhận), kèm nút gọi CVDV.
**message:** Chào chị Lan, báo giá cho xe VF 6 của chị đã sẵn sàng. Chị xem chi tiết và duyệt từng hạng mục trong app, hoặc bấm gọi CVDV Hải nếu cần giải thích thêm.
**verify:** Khách duyệt / từ chối trong ngày · xe không nằm chờ báo giá quá 1 ngày
**kpi:** Thời gian xe chờ báo giá, Promise Kept Rate
**cost:**
- Xe nằm xưởng thêm ngày
- Khách tự gọi hỏi — failure demand
- Chiếm chỗ đỗ, giảm công suất xưởng
**trace:**
- t: 15:10 · l: L0 · ttl: Phát hiện · d: RO-6120 "chờ khách duyệt" 4h10, không có cuộc gọi / tin nhắn ra · tok: 0
- t: 15:10 · l: L2 · ttl: Trích cam kết · d: Transcript 11:02: "chiều em gọi báo giá chị" → {owner: CVDV Hải, hạn: chiều nay} · tok: 1200
- t: 15:11 · l: Act · ttl: Nhắc nội bộ · d: Nhắc CVDV Hải + trưởng xưởng (mức 1) · tok: 0
- t: 16:30 · l: L0 · ttl: Theo dõi · d: Vẫn chưa liên hệ (CVDV đang tiếp khách khác) · tok: 0
- t: 16:31 · l: Inform · ttl: Gửi báo giá · d: Báo giá nguyên văn từ DMS trong app; claim check: mọi số khớp DMS ✓ · tok: 200
- t: 16:45 · l: Customer · ttl: Khách duyệt · d: Duyệt 1/2 hạng mục trong app · tok: 0
- t: 18:00 · l: Verify · ttl: Xác minh · d: Sửa xong, bàn giao trong ngày · tok: 0
- t: Tuần · l: Learn · ttl: Pattern · d: Báo giá lập sau 15:00 thường trễ liên hệ → đề xuất phân công CVDV ca chiều · tok: 0
**note:** Rule không hiểu được lời hứa trong ngôn ngữ tự nhiên — đây là nơi LLM tạo giá trị rõ nhất.


## UC5 — Vừa sửa xong, đèn lỗi lại sáng

**customer:** Vừa sửa xong 3 ngày, đèn cảnh báo lại sáng. Tôi lại phải gọi, kể lại từ đầu, và không biết có mất tiền không.
**outcome:** Doanh nghiệp nhận lỗi trước khi khách phải gọi, ưu tiên sửa lại, khách chỉ cần chọn giờ.
**type:** T4 · Đóng sớm · Sự cố & bảo hành · Wave 2
**name:** Sửa xong nhưng mã lỗi quay lại
**context:** Xe sửa xong, lệnh sửa chữa đóng. Ba ngày sau, telematics ghi nhận lại cùng mã lỗi. Khách có thể chưa để ý — hoặc đang bực vì đèn cảnh báo lại sáng.
**actors:**
- Chủ xe
- CVDV
- Trưởng kỹ thuật
- Bảo hành hãng
**systems:**
- Telematics
- DMS xưởng
- CRM
- App
**happy:**
- Xe vào xưởng
- Chẩn đoán, sửa
- Chạy thử
- Đóng lệnh sửa chữa
- Theo dõi sau sửa: mã lỗi không quay lại
**brk:** 4
**breakpoint:** Không ai theo dõi sau khi đóng lệnh; tín hiệu lặp lại nằm trong telematics, xưởng không thấy.
**rules:**
- Cùng hệ thống báo lỗi lại trong 30 ngày → mở lại lệnh cũ (comeback), ưu tiên cao
- Comeback có trưởng kỹ thuật xem xét
- Chi phí comeback theo chính sách xưởng (giả định: không tính phí)
**signal:** telematics.dtc thuộc hệ thống X
  AND RO đóng < 30 ngày cùng hệ thống X
  THEN candidate(T4)
**action:** Xác định comeback, mở lại lệnh cũ, giữ slot ưu tiên, báo khách chủ động kèm xin lỗi; khách chọn giờ. Mã lỗi CRITICAL → luồng an toàn.
**message:** Chào chị Mai, hệ thống ghi nhận cảnh báo hệ thống điều hoà trên xe VF 7 của chị xuất hiện lại sau lần sửa ngày 20/9. Bên em rất tiếc. Xưởng đã mở lại hồ sơ với mức ưu tiên cao; chị chọn giúp em khung giờ phù hợp trong app nhé.
**verify:** Sửa lần 2 · telematics 30 ngày không ghi nhận lại mã lỗi
**kpi:** Comeback Rate, thời gian phát hiện comeback
**cost:**
- Khách tự phát hiện, bực hơn nhiều
- Chỉ số "sửa đúng lần đầu" sai sự thật
- Rủi ro hỏng lan rộng nếu chậm
**trace:**
- t: T2 07:40 · l: L0 · ttl: Phát hiện · d: Mã lỗi điều hoà lặp lại; RO-5402 cùng hệ thống đóng 3 ngày trước · tok: 0
- t: 07:40 · l: L1 · ttl: Triage · d: WARNING, cùng hệ thống → COMEBACK · tok: 0
- t: 07:41 · l: L2 · ttl: Đối chiếu · d: Hạng mục đã sửa + lịch sử mã lỗi → khả năng sửa chưa triệt để · tok: 2000
- t: 07:41 · l: Validator · ttl: Quy tắc · d: < 30 ngày · cùng hệ thống → comeback ưu tiên · tok: 0
- t: 07:42 · l: Act · ttl: Mở lại lệnh · d: Mở lại RO-5402, giữ slot ưu tiên chờ khách chọn (mức 1 nội bộ) · tok: 0
- t: 08:00 · l: Inform · ttl: Báo khách · d: Tin xin lỗi + chọn giờ (đặt lịch = mức 2, cần khách chọn) · tok: 300
- t: 08:20 · l: Customer · ttl: Khách chọn · d: 9:00 thứ Hai tuần sau · tok: 0
- t: +30 ngày · l: Verify · ttl: Xác minh · d: Telematics 30 ngày không ghi nhận lại → RECOVERED · tok: 0
- t: Tháng · l: Learn · ttl: Chất lượng · d: Comeback theo hạng mục / xưởng → báo cáo chất lượng sửa chữa · tok: 0
**note:** Điểm mạnh riêng của xe điện: outcome được xác minh bằng dữ liệu của chính chiếc xe.


## UC6 — Xe nằm xưởng, không ai nói vì sao

**customer:** Xe tôi nằm xưởng cả tuần chờ bảo hành. Hỏi xưởng thì bảo chờ hãng, hỏi hãng thì bảo hỏi xưởng.
**outcome:** Khách biết đúng đang chờ bước nào, vì sao và đến khi nào — và hồ sơ được đẩy đi trong ngày.
**type:** T3 · Rơi quyền sở hữu · Bảo hành · Wave 3
**name:** Claim bảo hành kẹt giữa đại lý và hãng
**context:** Linh kiện hỏng trong thời hạn bảo hành: xưởng lập claim gửi hãng duyệt. Claim thiếu bằng chứng bị trả về, nhưng thông báo nằm trong portal của hãng; xưởng không thấy, xe nằm chờ.
**actors:**
- Chủ xe
- CVDV đại lý
- Bảo hành hãng
- Kho
**systems:**
- DMS đại lý
- Warranty portal
- Telematics
- CRM
**happy:**
- Chẩn đoán lỗi trong bảo hành
- Lập claim kèm bằng chứng
- Hãng duyệt
- Cấp linh kiện
- Sửa, bàn giao
**brk:** 2
**breakpoint:** Hãng trả claim yêu cầu bổ sung → không ai ở đại lý nhận. Quyền sở hữu rơi giữa hai tổ chức.
**rules:**
- Claim trả về phải có owner đại lý trong 4 giờ làm việc
- Bằng chứng tự động (log mã lỗi, odometer, lịch sử bảo dưỡng) đính kèm mặc định
- Điều kiện theo chính sách công bố: thời hạn năm/km, loại hình sử dụng, loại trừ
**signal:** claim.status = "returned_for_info" > 4h
  AND không có hoạt động từ đại lý
  THEN candidate(T3)
**action:** Tự đính kèm bằng chứng có sẵn (mức 1), giao CVDV phần còn lại (ảnh linh kiện) có hạn, cập nhật khách tiến độ thật.
**message:** Chào anh Khoa, yêu cầu bảo hành cho xe VF 8 của anh đang chờ xưởng bổ sung hồ sơ cho hãng. Xưởng sẽ hoàn tất trong hôm nay; bên em sẽ cập nhật ngay khi có kết quả duyệt.
**verify:** Claim nộp lại ≤ 1 ngày · được duyệt · xe sửa xong
**kpi:** Thời gian claim nằm ở trạng thái trả về, số ngày xe chờ
**cost:**
- Xe khách nằm xưởng nhiều ngày
- Khách hỏi tiến độ liên tục
- Tranh cãi đại lý – hãng
**trace:**
- t: 09:00 · l: L0 · ttl: Phát hiện · d: Claim WC-2231 trả về 2 ngày, không có hoạt động từ đại lý · tok: 0
- t: 09:00 · l: L1 · ttl: Lý do trả · d: "Thiếu log lỗi và ảnh linh kiện" (trường có cấu trúc) · tok: 0
- t: 09:01 · l: Act · ttl: Đính kèm tự động · d: Log mã lỗi + odometer từ telematics + lịch sử bảo dưỡng · tok: 0
- t: 09:01 · l: Act · ttl: Giao việc · d: Task CVDV: chụp ảnh linh kiện, hạn 16:00 · tok: 0
- t: 09:05 · l: Inform · ttl: Báo khách · d: Tiến độ thật, không hứa kết quả duyệt · tok: 300
- t: 15:20 · l: Verify · ttl: Theo dõi · d: Claim nộp lại; hãng duyệt hôm sau; xe sửa xong · tok: 0
- t: Tháng · l: Learn · ttl: Pattern · d: Nhiều claim trả về do thiếu log → đính kèm log mặc định khi lập claim · tok: 0
**note:** Gần như không cần LLM: giá trị nằm ở việc có người "giữ" claim qua ranh giới hai tổ chức.


## UC4 — Được miễn phí sạc mà vẫn bị trừ tiền

**customer:** Xe tôi thuộc diện miễn phí sạc, vậy mà hai lần sạc gần đây đều bị trừ tiền.
**outcome:** Khách được báo trước khi phát hiện, biết khi nào có kết quả, được hoàn đúng — không phải khiếu nại.
**type:** T1 · Lệch trạng thái · Sạc · Wave 3 · HITL
**name:** Phí sạc bị tính sai quyền ưu đãi
**context:** Theo công bố, khách hàng cá nhân được miễn phí sạc tại V-Green đến 30/6/2027; xe kinh doanh vận tải có chính sách riêng. Quyền ưu đãi phụ thuộc hồ sơ xe – chủ xe – loại hình sử dụng ở các hệ thống khác nhau. Khi xe sang tên hoặc tài khoản sạc liên kết sai, phiên sạc có thể bị tính phí sai.
**actors:**
- Chủ xe
- CSKH
- Đối soát V-Green
- Kế toán
**systems:**
- CSMS trạm sạc
- Billing sạc
- Hồ sơ xe & chủ xe
- App
**happy:**
- Xe cắm sạc
- Trạm nhận diện xe / tài khoản
- Billing tra quyền ưu đãi theo chính sách hiện hành
- Phiên sạc tính đúng
- Hoá đơn / thông báo
**brk:** 2
**breakpoint:** Sang tên không kích hoạt cập nhật tài khoản sạc → billing tra theo chủ cũ hoặc tài khoản không có quyền ưu đãi.
**rules:**
- Quyền ưu đãi theo chính sách có phiên bản & ngày hiệu lực
- Mọi hoàn tiền do đối soát duyệt (mức 3)
- Hoàn tự động chỉ khi trừ trùng cùng mã phiên và dưới ngưỡng
- Không hứa hoàn trước khi xác minh loại hình sử dụng
**signal:** phiên sạc có phí AND xe thuộc diện cá nhân trong hồ sơ
  OR 2 giao dịch cùng session_id
  THEN candidate(T1)
**action:** Đối chiếu hồ sơ xe, lịch sử sang tên, chính sách phiên bản → đề xuất hoàn + sửa liên kết cho đối soát duyệt → báo khách đang xử lý kèm thời hạn.
**message:** Chào anh Nam, bên em thấy 2 phiên sạc ngày 12–13/9 của xe VF 5 bị tính phí dù xe thuộc diện ưu đãi sạc của khách hàng cá nhân. Bộ phận đối soát đang xác nhận và sẽ phản hồi trước 17:00 ngày 15/9. Anh không cần thao tác gì thêm.
**verify:** Hoàn đúng số tiền hoá đơn · liên kết xe – tài khoản đúng · phiên sạc sau đó tính đúng
**kpi:** Số phiên tính sai được chặn, thời gian đối soát
**cost:**
- Khách bị trừ tiền dù được miễn phí → mất niềm tin
- Khiếu nại, mạng xã hội
- Đối soát thủ công
**trace:**
- t: 08:30 · l: L0 · ttl: Phát hiện · d: 2 phiên có phí; hồ sơ xe VF 5: cá nhân · tok: 0
- t: 08:30 · l: L1 · ttl: Đối chiếu · d: Xe sang tên 05/9; tài khoản sạc vẫn gắn chủ cũ → LIKELY_MISLINK · tok: 0
- t: 08:31 · l: L2 · ttl: Kiểm tra chính sách · d: Chính sách sạc phiên bản hiện hành + loại hình sử dụng trên đăng ký → đủ điều kiện · tok: 1800
- t: 08:31 · l: Act · ttl: Tạo đề xuất · d: Đề xuất hoàn + sửa liên kết (chờ duyệt, mức 3) · tok: 0
- t: 08:32 · l: Inform · ttl: Báo khách · d: Đang xử lý, có hạn phản hồi; không hứa kết quả · tok: 300
- t: 10:15 · l: Human · ttl: Đối soát duyệt · d: Duyệt hoàn tiền + sửa liên kết · tok: 0
- t: 16/9 · l: Verify · ttl: Xác minh · d: Phiên sạc mới tính đúng ưu đãi; hoàn tiền đã về · tok: 0
- t: Tháng · l: Learn · ttl: Root cause · d: Sang tên không phát event sang billing → đề xuất event ownership.transferred · tok: 0
**note:** Liên quan tiền → agent chỉ chuẩn bị hồ sơ; quyết định luôn thuộc về người.
