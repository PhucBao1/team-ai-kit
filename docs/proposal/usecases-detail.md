# Use case chi tiết (PL-A) — dữ liệu từ explorer trong proposal

> Trích tự động từ mảng USECASES của proposal.


## UC1 — Friction dịch vụ đang hình thành

**customer:** Cảnh báo cứ hiện rồi tắt. Tôi không biết có sao không, tới lúc sắp đi xa mới phải tìm lịch sửa.
**outcome:** Được báo trước, hiểu đúng mức độ, có sẵn phương án — không phải tự mở case.
**type:** Flagship · FULL · Proactive
**name:** Preemptive Service Friction Rescue — can thiệp trước khi có case
**context:** Mã lỗi WARNING lặp lại trên xe, chưa có lịch / ticket / khiếu nại. L0 đếm tín hiệu lặp, arbitration kiểm tra được phép liên hệ, Agent chỉ được gọi khi ca nhiều nguồn và mơ hồ. Synthetic / illustrative scenario for MVP.
**actors:**
- Chủ xe
- CSKH
- Cố vấn dịch vụ (CVDV)
- Điều phối xưởng
**systems:**
- Telematics
- DMS xưởng
- ERP kho
- App
- CRM
**happy:**
- Xe ghi nhận cảnh báo (lần 1, 2, 3…)
- Khách có thể không để ý
- Khách tự đặt lịch hoặc gọi hỏi
- Xưởng kiểm tra, sửa
- Đóng lệnh
**brk:** 1
**breakpoint:** Không ai nhìn thấy chuỗi tín hiệu lặp cho tới khi khách tự khởi xướng — thường quá muộn để chọn slot và giữ linh kiện thuận tiện.
**rules:**
- Chỉ WARNING lặp ≥ 3 lần / 14 ngày mới là candidate; CRITICAL đi SafetyPath, không qua UC1
- Không liên hệ khi đã có case mở, đang chat với nhân viên, giờ yên tĩnh hoặc quá ngân sách chú ý
- Agent không chẩn đoán, không kết luận bảo hành, không ghi dữ liệu
- Đặt lịch / giữ linh kiện luôn cần khách xác nhận (mức 2)
**signal:** ON vehicle.dtc.raised
  IF severity = WARNING
  AND count(same system, 14d) >= 3
  AND NOT known_safe_transient
  AND no open appointment / RO / ticket / complaint
  THEN candidate(UC1)  # không LLM
ARBITRATION: không đang chat · ngoài giờ yên tĩnh · <= 3 tin / khách / tuần
**action:** Gom ngữ cảnh bằng tool đọc → L1 phân loại (nếu cần) → Agent L2 trả lời 8 câu và chọn can thiệp (giải thích / self-help / chuẩn bị phương án / hỏi xác nhận / handoff) → validator → tin chủ động. Không tự đặt lịch khi chưa có xác nhận.
**message:** Chào anh Minh, xe VF 8 của anh đã ghi nhận cảnh báo hệ thống làm mát pin 3 lần trong 14 ngày (mức cảnh báo, chưa nguy hiểm). Theo KB mã lỗi, lỗi này không khắc phục được bằng cập nhật phần mềm từ xa nên nên kiểm tra tại xưởng. Em đã chuẩn bị 2 phương án; anh chọn giúp em nhé. Vì sao anh nhận tin này: xe gửi cảnh báo lặp lại và anh đã bật thông báo dịch vụ.
**verify:** Telematics 14 ngày không ghi nhận lại mã · khách được báo trước khi tự tạo appointment / ticket
**kpi:** Pre-chase recovery, detector P/R, llm_call_rate
**cost:**
- Khách tự phát hiện, nhiều khi sát chuyến đi
- Chen lịch, chờ linh kiện, bị từ chối
- Mất niềm tin vào cảnh báo của xe
**trace:**
- t: T0 · Thứ Ba 08:15 · l: L0 · ttl: Hệ thống nhận tín hiệu · d: vehicle.dtc.raised (làm mát pin, WARNING, 38.420 km, SoC 42%) → Pub/Sub ops-events · tok: 0
- t: T+0,2 s · l: L0 · ttl: Detector đánh giá · d: WARNING ✓ · lần thứ 3 trong 14 ngày (23/9, 26/9, 29/9) ✓ · dedupe mới ✓ · không có appointment / RO / ticket ✓ → CandidateFriction(UC1) · tok: 0
- t: T+0,3 s · l: L0 · ttl: Arbitration qua · d: Không đang chat · ngoài giờ yên tĩnh · 0/3 tin tuần này · có consent thông báo → allowed · tok: 0
- t: T+1 s · l: Tool · ttl: Gom ngữ cảnh · d: get_vehicle_status · get_recent_events · explain_dtc (không sửa từ xa) · bảo dưỡng · check_warranty (sơ bộ) · chuyến đi thứ Bảy → ContextBundle · tok: 0
- t: T+1 s · l: L1 · ttl: Decision gate + triage · d: Rule tất định không đủ (nhiều nguồn + lựa chọn). L1: không có dấu hiệu an toàn, cần xem xét dịch vụ → escalate_to_L2 · tok: 300
- t: T+3 s · l: L2 · ttl: AGENT được gọi · d: Trả lời 8 câu: friction có ý nghĩa · mức khẩn bình thường · KB không đủ self-help → cần xưởng · gọi find_options kiểm khả thi · cần xác nhận · chưa cần người → InterventionProposal · tok: 2500
- t: T+5 s · l: Validator · ttl: Kiểm tra · d: claim_check ✓ · không có cụm từ cấm (chẩn đoán / bảo hành) ✓ · severity còn WARNING ✓ · arbitration kiểm lại ✓ · tok: 0
- t: T+6 s · l: Inform · ttl: Tin chủ động · d: Tin 5 phần + 'vì sao anh nhận tin' + 2 phương án + nút Gặp nhân viên; journey = chờ khách chọn · tok: 300
- t: T+8 phút · l: Customer · ttl: Khách xác nhận · d: Chọn phương án, bấm Xác nhận → POST /confirm {token} · tok: 0
- t: T+8 phút · l: Act · ttl: Validator + Executor · d: 6 check ✓ → book_appointment (idempotent) → giữ linh kiện, ghi promise → đọc lại để xác nhận (UC3) · tok: 0
- t: T+18 ngày · l: Verify · ttl: Xác minh bằng dữ liệu xe · d: Sửa xong thứ Bảy 3/10; telematics 14 ngày không ghi nhận lại → resolved. Tái phát → UC6 · tok: 0
**note:** Chưa hề có khách nào nhờ giúp: hệ thống phát hiện, điều tra, chủ động can thiệp và xác minh.


## UC2 — Ngăn friction sạc

**customer:** Cắm sạc không được, thử lại vẫn không được. Không biết do trạm, do xe hay do tài khoản.
**outcome:** Nhận ngay việc nên làm: thử đúng cách, trạm khác đi tới được, hoặc có người gọi nếu pin thấp.
**type:** DEMO-READY · Proactive · hai đường
**name:** Charging Friction Prevention — phiên sạc thất bại lặp lại
**context:** CSMS ghi nhận thất bại lặp lại của cùng xe; L0 tương quan với tình trạng trạm. Trạm hỏng → đường tất định, 0 token. Trạm khoẻ mà xe vẫn lỗi → Agent so sánh 5 giả thuyết. Synthetic / illustrative scenario for MVP.
**actors:**
- Chủ xe
- Tổng đài 24/7
- Vận hành trạm sạc
**systems:**
- CSMS trạm sạc
- Telematics
- App
- Live chat queue
**happy:**
- Khách cắm sạc
- Phiên sạc thất bại
- Khách thử lại nhiều lần
- Khách gọi hotline / bấm gặp người
- Chờ nhân viên
**brk:** 3
**breakpoint:** Khách phải tự thử nhiều lần mới liên hệ; handoff ngoài giờ có thể rơi (không owner, không ticket) đúng lúc khách đang kẹt.
**rules:**
- ≥ 2 thất bại / 30 phút cùng xe → candidate; station_health gắn nhãn faulted / healthy / unknown
- SoC ≤ 10% và không ở trạm hoạt động → urgent → 24/7 trong 2 phút
- Không tự gọi cứu hộ khi khách chưa đồng ý
- Không khẳng định nguyên nhân khi bằng chứng không đủ
**signal:** ON charging.session.failed
  IF count(same vin, 30 phút) >= 2
  AND no open complaint / ticket
  THEN candidate(UC2) + station_health + vehicle_failures_30d
  IF SoC <= 10% THEN priority = urgent
# không LLM
**action:** Trạm faulted → mẫu tin + trạm thay thế (0 token). Trạm healthy → Agent xếp hạng 5 giả thuyết, chọn: thử lại / trạm khác / chuẩn bị đề xuất dịch vụ / handoff 24/7. Cứu hộ cần khách đồng ý.
**message:** Chào anh Tuấn, xe của anh vừa thất bại 2 lần khi sạc tại trạm Thanh Xuân dù trạm đang hoạt động bình thường. Em chưa xác định được nguyên nhân. Anh thử cổng #2; nếu chưa được, trạm cách 2,1 km còn 3 cổng trống và đi tới được với pin 18%. Vì sao anh nhận tin này: xe ghi nhận 2 lần sạc thất bại liên tiếp.
**verify:** Phiên sạc kế tiếp thành công trong 60 phút · tổng đài gọi trong 5 phút (luồng khẩn)
**kpi:** Handoff có owner trong 2 phút, tỉ lệ phiên sạc kế tiếp thành công
**cost:**
- Khách kẹt ngoài đường, nhất là ban đêm
- Mất niềm tin vào xe điện nói chung
- Contact lặp qua hotline, mạng xã hội
**trace:**
- t: T0 · 20:42 · l: L0 · ttl: Thất bại lần 1 · d: charging.session.failed · trạm Thanh Xuân #4 · PLUG_HANDSHAKE_FAIL (giả lập) · SoC 18% · tok: 0
- t: T+10 phút · l: L0 · ttl: Thất bại lần 2 · d: Cùng xe, 10 phút sau → ≥ 2 thất bại / 30 phút ✓ · tok: 0
- t: T+10 phút · l: L0 · ttl: Detector + tương quan trạm · d: station_health = healthy (7/8 phiên khác thành công) · 2 thất bại ở trạm khác trong 30 ngày · không khiếu nại · SoC 18% (không urgent) → CandidateFriction(UC2) · tok: 0
- t: T+10 phút · l: L0 · ttl: Arbitration qua · d: Ngoài giờ yên tĩnh · 0/3 tin tuần này → allowed · tok: 0
- t: T+10 phút · l: Tool · ttl: Gom ngữ cảnh · d: get_charging_history · get_station_status · find_chargers (đi tới được với 18%) · KB thử lại · chuyến đi thứ Bảy → ContextBundle · tok: 0
- t: T+10 phút · l: L0 · ttl: Decision gate · d: Trạm khoẻ nhưng xe thất bại lặp lại → rule tất định không đủ → escalate_to_L2 (nếu trạm faulted: đường tất định, KHÔNG Agent) · tok: 0
- t: T+11 phút · l: L2 · ttl: AGENT được gọi · d: Xếp hạng: B (xe / tài khoản) cao nhất · C thấp · D chưa đủ bằng chứng. Chọn: thử cổng khác + trạm 2,1 km + chuẩn bị đề xuất dịch vụ; nói rõ 'chưa xác định được nguyên nhân' · tok: 2200
- t: T+11 phút · l: Validator · ttl: Kiểm tra · d: claim_check ✓ (2,1 km, 3 cổng trống khớp CSMS) · core.range ✓ · không khẳng định nguyên nhân ✓ · tok: 0
- t: T+11 phút · l: Inform · ttl: Tin chủ động · d: Hướng dẫn thử cổng #2 + trạm thay thế + vì sao nhận tin + nút Gặp nhân viên · tok: 0
- t: T+16 phút · l: Customer · ttl: Khách thử cổng #2 · d: Phiên sạc mới thành công · tok: 0
- t: T+17 phút · l: Verify · ttl: Xác minh · d: CSMS: charging.session.completed (kWh > 0) trong 60 phút → resolved. Lần 4 trong 30 ngày → chuẩn bị đề xuất dịch vụ (UC3) · tok: 0
**note:** Hai đường: trạm hỏng rõ → 0 token; trạm khoẻ mà xe vẫn lỗi → mới cần Agent. SoC 6% → handoff 24/7 ngay, không chờ Agent.


## UC3 — Điều phối can thiệp xưởng

**customer:** Lịch nhìn có vẻ ổn nhưng thiếu linh kiện, hoặc xưởng không có kỹ thuật viên pin cao áp — tôi nghỉ làm rồi mới biết.
**outcome:** Nhận 2–3 phương án khả thi thật kèm lý do; chọn, xác nhận; được báo trước nếu điều kiện đổi.
**type:** DEMO-READY · Downstream · nơi appointment xuất hiện
**name:** Service Readiness / Intervention Orchestration — suy luận đa ràng buộc
**context:** Chạy SAU khi UC1 / UC2 / UC6 hoặc khách đã chứng minh cần can thiệp xưởng; appointment chỉ là hành động xuôi dòng. Nhánh lập lại phương án khi reservation của lịch đã xác nhận bị huỷ. Synthetic / illustrative scenario for MVP.
**actors:**
- Chủ xe
- Cố vấn dịch vụ (CVDV)
- Điều phối xưởng
- Kho phụ tùng
**systems:**
- DMS xưởng
- ERP kho
- Telematics
- App
**happy:**
- Có yêu cầu can thiệp xưởng
- Chọn slot trống đầu tiên
- Đặt lịch
- Giữ linh kiện
- Khách tới xưởng
**brk:** 1
**breakpoint:** 'Slot trống đầu tiên' bỏ sót ràng buộc: linh kiện, kỹ năng, quãng đường / pin, giờ rảnh của khách; reservation có thể bị kho điều đi sau khi đã xác nhận.
**rules:**
- Chỉ phương án qua đủ 7 check validator mới được hiển thị / ghi
- Phương án bị loại phải có lý do trong trace
- Không tự đổi lịch khi chưa có xác nhận (mức 2)
- Xe có cảnh báo an toàn được ưu tiên linh kiện
**signal:** INPUT InterventionRequest(vin, issue, source = UC1 | UC2 | UC6 | chat)
L0: part_matches_vin · core.range · xưởng mở · slot free
REPLAN: ON parts.reservation.cancelled | eta_changed
  IF appointment.status = confirmed AND start - now < 72h
  THEN candidate(UC3_REPLAN)
**action:** find_options gom kho + kỹ năng + slot + range (khoá slot tạm 15 phút) → Agent loại có lý do, xếp hạng 2–3 phương án → validator → khách chọn & xác nhận → Executor + saga → đọc lại xác minh.
**message:** Chào anh Minh, em có 2 phương án: (1) 9:00 thứ Bảy 3/10 tại xưởng Gia Lâm (6 km) — đã có sẵn linh kiện và kỹ thuật viên pin cao áp; (2) 9:00 thứ Ba 6/10 tại Long Biên khi linh kiện về. Long Biên thứ Bảy không phù hợp vì linh kiện chưa có. Anh chọn phương án nào ạ?
**verify:** Đọc lại lịch confirmed + reservation đúng mã đúng xưởng · sửa đúng hẹn · telematics 14 ngày sạch
**kpi:** % phương án vượt validator, Pre-chase recovery (nhánh lập lại), Time-to-Recovery
**cost:**
- Khách mất nửa ngày đến xưởng rồi về
- Slot xưởng lãng phí
- Khiếu nại tại chỗ
**trace:**
- t: T0 · Thứ Ba 08:16 · l: L0 · ttl: InterventionRequest · d: vin, issue = cooling_pump, source = UC1 → UC3 · tok: 0
- t: T+0 s · l: L0 · ttl: Lọc cứng · d: Điều kiện hợp lệ · part_matches_vin ✓ · pin / quãng đường qua core.range → 3 xưởng ứng viên · tok: 0
- t: T+1 s · l: Tool · ttl: find_options · d: Tồn kho, kỹ thuật viên, slot, khoảng cách; khoá slot tạm 15 phút → ContextBundle · tok: 0
- t: T+3 s · l: L2 · ttl: AGENT đa ràng buộc (giai đoạn 1) · d: Long Biên: linh kiện ✓ · kỹ thuật viên pin cao áp ✓ · slot 9:00 / 14:00 thứ Bảy · 4 km → HỢP LỆ. Gia Lâm: đủ cả, xa hơn → xếp sau. Xưởng 35 km: LOẠI (không có kỹ thuật viên pin cao áp ca thứ Bảy, pin cần sạc dọc đường) · tok: 2500
- t: T+4 s · l: Validator · ttl: Kiểm tra · d: part_matches_vin ✓ · technician_certified ✓ · part_reserved (tạm) ✓ · slot_locked ✓ · tok: 0
- t: T+5 s · l: Inform · ttl: 2 phương án + lý do · d: Tin có 'vì sao hợp lệ' và 'vì sao loại', nút Xác nhận / Gặp nhân viên · tok: 0
- t: T+7 phút · l: Customer · ttl: Khách xác nhận · d: Chọn Long Biên 9:00 thứ Bảy → POST /confirm {token} · tok: 0
- t: T+7 phút · l: Act · ttl: Validator + Executor · d: 7 check ✓ → book_appointment (idempotent) → SA-20931, giữ linh kiện + ghi promise → đọc lại: confirmed, reservation held · tok: 0
- t: Thứ Năm 14:02 · l: L0 · ttl: NHÁNH LẬP LẠI · d: Kho điều linh kiện đi: parts.reservation.cancelled, lịch còn 67 giờ → candidate(UC3_REPLAN) · tok: 0
- t: 14:03 · l: L2 · ttl: AGENT lập lại (giai đoạn 2) · d: Long Biên: slot ✓ nhưng hết linh kiện → LOẠI. Xưởng 35 km: linh kiện ✓ nhưng không có kỹ thuật viên pin cao áp thứ Bảy → LOẠI. Gia Lâm: đủ cả → HỢP LỆ. Long Biên thứ Ba → hợp lệ nhưng muộn · tok: 2500
- t: 14:06 · l: Customer · ttl: Khách bực · d: 'Cho anh nói chuyện với người' → handoff · tok: 0
- t: 14:07 · l: Human · ttl: Handoff · d: CVDV Hải nhận card: đã đề xuất gì, đã hứa gì, KHÔNG làm gì; chốt phương án 1 → Executor reschedule, giải phóng slot cũ → verify đọc lại · tok: 400
**note:** Chính chỗ này chứng minh Agent cần suy luận + điều phối tool: một rule 'slot sớm nhất' sẽ sai ở cả hai phương án đầu.


## UC4 — Phòng ngừa lệch phí sạc

**customer:** Xe tôi thuộc diện miễn phí sạc mà vẫn bị trừ tiền, hoặc bị trừ hai lần cho một phiên.
**outcome:** Được báo trước khi phát hiện, biết khi nào có kết quả, được hoàn đúng — không phải khiếu nại.
**type:** SPEC ONLY · cố ý LLM-light · tiền → người duyệt
**name:** Billing / Charging Mismatch Prevention — chứng minh 'không phải event nào cũng cần Agent'
**context:** So khớp tất định session ↔ billing ↔ quyền ưu đãi (chính sách có phiên bản). Trừ trùng dưới ngưỡng tự sửa không LLM; mâu thuẫn dữ liệu mới cần Agent chuẩn bị hồ sơ. Hoàn tiền luôn do người duyệt. Synthetic / illustrative scenario for MVP.
**actors:**
- Chủ xe
- CSKH
- Đối soát
- Kế toán
**systems:**
- CSMS trạm sạc
- Billing sạc
- Hồ sơ xe & chủ xe
- App
**happy:**
- Xe cắm sạc
- Trạm nhận diện tài khoản
- Billing tra quyền ưu đãi
- Phiên sạc tính phí
- Hoá đơn
**brk:** 2
**breakpoint:** Sang tên không kích hoạt cập nhật tài khoản sạc → billing tra theo chủ cũ; hoặc giao dịch bị trừ trùng; không ai kiểm tra cho tới khi khách khiếu nại.
**rules:**
- Quyền ưu đãi theo chính sách có phiên bản & ngày hiệu lực
- Tự sửa chỉ khi cùng session_id và dưới ngưỡng (POLICY do đối soát chốt)
- Mọi hoàn tiền khác do đối soát duyệt (mức 3)
- Không hứa hoàn trước khi xác minh loại hình sử dụng
**signal:** R1: >= 2 giao dịch cùng session_id            → duplicate
R2: phí > 0 AND xe personal AND chính sách miễn phí hiệu lực AND liên kết đúng → mismatch_clean
R3: như R2 nhưng sang tên / liên kết cũ / usage_type mơ hồ → mismatch_conflict
# không LLM ở detector
**action:** R1 dưới ngưỡng: tự sửa tất định. R2: chuẩn bị điều chỉnh → đối soát duyệt. R3: Agent (tuỳ chọn) chuẩn bị hồ sơ + tin → đối soát duyệt. Agent không có tool hoàn tiền.
**message:** Chào anh Nam, bên em thấy 2 phiên sạc ngày 12–13/9 của xe VF 5 bị tính phí dù xe thuộc diện ưu đãi sạc của khách hàng cá nhân. Bộ phận đối soát đang xác nhận và sẽ phản hồi trước 17:00 ngày 15/9. Anh không cần thao tác gì thêm.
**verify:** Hoàn đúng số tiền · liên kết xe – tài khoản đúng · phiên sạc sau đó tính đúng
**kpi:** Số phiên tính sai được chặn, tỉ lệ ca xử lý không qua LLM, 0 tiền sai
**cost:**
- Khách bị trừ tiền dù được miễn phí → mất niềm tin
- Khiếu nại, mạng xã hội
- Đối soát thủ công
**trace:**
- t: A · T0 · l: L0 · ttl: Trừ trùng · d: billing.charge.created hai lần cùng session_id S-8841 · tok: 0
- t: A · T+1 s · l: L0 · ttl: Detector R1 · d: ≥ 2 giao dịch cùng session_id, số tiền dưới ngưỡng → candidate duplicate; arbitration qua · tok: 0
- t: A · T+3 s · l: Act · ttl: KHÔNG Agent — tự sửa · d: Policy cho phép → Executor đảo giao dịch trùng (idempotent, audit); mẫu tin 'đã hoàn' · tok: 0
- t: A · Verify · l: Verify · ttl: Xác minh · d: Ledger khớp 1 giao dịch; phiên sau tính đúng → resolved · tok: 0
- t: B · T0 · l: L0 · ttl: Phí khi được miễn · d: Phiên sạc 12/9 có phí; VF 5 cá nhân · tok: 0
- t: B · T+1 s · l: L0 · ttl: Detector R3 · d: Xe sang tên 05/9, tài khoản sạc vẫn gắn chủ cũ → mâu thuẫn → candidate mismatch_conflict · tok: 0
- t: B · T+3 s · l: L2 · ttl: Agent (bằng chứng mâu thuẫn) · d: Khả năng cao là liên kết sai; chuẩn bị đề xuất hoàn + sửa liên kết + tóm tắt cho đối soát · tok: 1800
- t: B · T+4 s · l: Validator · ttl: Mức 3 · d: Số tiền / phiên bản chính sách khớp; hoàn tiền = chỉ người duyệt → needs_human · tok: 0
- t: B · 08:32 · l: Inform · ttl: Báo khách · d: Đang xử lý, phản hồi trước 17:00 15/9; không hứa kết quả · tok: 300
- t: B · 10:15 · l: Human · ttl: Đối soát duyệt · d: Duyệt hoàn + sửa liên kết → Executor · tok: 0
- t: B · 16/9 · l: Verify · ttl: Xác minh · d: Phiên mới tính đúng ưu đãi; hoàn tiền đã về → resolved · tok: 0
**note:** Cố ý LLM-light: nhánh A không dùng token nào. Tiền không bao giờ do LLM quyết định.


## UC5 — Theo dõi claim bảo hành chủ động

**customer:** Xe nằm xưởng cả tuần chờ bảo hành. Hỏi xưởng thì bảo chờ hãng, hỏi hãng thì bảo hỏi xưởng.
**outcome:** Biết đúng đang chờ bước nào, vì sao, đến khi nào — hồ sơ được đẩy đi trong ngày.
**type:** SPEC ONLY · state machine trước · Agent không quyết định bảo hành
**name:** Proactive Warranty / Claim Follow-up — giữ claim không rơi giữa hai tổ chức
**context:** Claim bị trả về yêu cầu bổ sung; thông báo nằm ở portal hãng, xưởng không thấy. Detector + state machine phát hiện; Agent chỉ cần khi lý do trả về là văn bản tự do. Synthetic / illustrative scenario for MVP.
**actors:**
- Chủ xe
- CVDV đại lý
- Bảo hành hãng
- Trưởng xưởng
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
**breakpoint:** Hãng trả claim yêu cầu bổ sung → không ai ở đại lý nhận; quyền sở hữu rơi giữa hai tổ chức.
**rules:**
- Claim trả về phải có owner đại lý trong 4 giờ làm việc
- Bằng chứng tự động (log mã lỗi, odometer, lịch sử bảo dưỡng) đính kèm mặc định
- Tin không hứa kết quả duyệt; chỉ 'đủ điều kiện sơ bộ' / trạng thái
- Agent không quyết định kết quả bảo hành
**signal:** ON warranty.claim.state_changed OR sweep
  IF state = returned_for_info AND elapsed > 4 giờ làm việc
  AND no dealer activity
  THEN candidate(UC5)
C2: pending_dealer >= 75% SLA · C3: pending_manufacturer >= 80% SLA (escalate nội bộ)
# không LLM
**action:** Lý do có cấu trúc → rule + mẫu (0 token). Lý do tự do → L1 / Agent trích mục thiếu → đính bằng chứng tự động (mức 1) → task CVDV có hạn → cập nhật khách tiến độ thật. Không tự quyết kết quả.
**message:** Chào anh Khoa, yêu cầu bảo hành cho xe VF 8 của anh đang chờ xưởng bổ sung hồ sơ cho hãng. Xưởng sẽ hoàn tất trong hôm nay; bên em sẽ cập nhật ngay khi có kết quả duyệt.
**verify:** Bằng chứng nhận được · claim resubmitted ≤ 1 ngày · khách được báo tiến độ thật
**kpi:** Thời gian claim ở trạng thái trả về, số ngày xe chờ, 0 tin hứa kết quả
**cost:**
- Xe khách nằm xưởng nhiều ngày
- Khách hỏi tiến độ liên tục
- Tranh cãi đại lý – hãng
**trace:**
- t: T0 · 09:00 · l: L0 · ttl: Sweep · d: Claim WC-2231 ở returned_for_info 2 ngày; không có hoạt động đại lý · tok: 0
- t: T+1 s · l: L0 · ttl: Detector C1 · d: > 4 giờ làm việc ✓ · không hoạt động ✓ → candidate(UC5); arbitration qua · tok: 0
- t: T+1 s · l: Tool · ttl: Gom ngữ cảnh · d: get_claim_status · list_claim_evidence · telematics · bảo dưỡng → ContextBundle · tok: 0
- t: T+1 s · l: L1 · ttl: Decision gate · d: Lý do là văn bản tự do ('thiếu bằng chứng tình trạng sử dụng') → rule không phân loại được; L1 trích mục thiếu · tok: 400
- t: T+1 s · l: L2 · ttl: Agent · d: Thiếu: log lỗi (tự động có) · odometer (tự động có) · ảnh hư hỏng (cần CVDV). Chọn: đính tự động + task CVDV hạn 16:00 + tin tiến độ · tok: 1500
- t: T+2 s · l: Validator · ttl: Kiểm tra · d: Bằng chứng đính đều có nguồn ✓ · tin không hứa kết quả ✓ · tok: 0
- t: T+2 s · l: Act · ttl: Executor (mức 1) · d: attach_evidence (log + odometer + lịch sử) · create_task(CVDV Hải, 16:00) · tok: 0
- t: T+5 s · l: Inform · ttl: Báo khách · d: Tiến độ thật; không hứa kết quả duyệt · tok: 0
- t: 15:20 · l: Verify · ttl: Xác minh · d: Ảnh đã đính; claim resubmitted → progressed · tok: 0
- t: Hôm sau · l: Learn · ttl: Pattern · d: Nhiều claim trả về do thiếu log → đính log mặc định khi lập claim · tok: 0
**note:** Rule lo phần có cấu trúc; Agent chỉ trích ý khi văn bản tự do. Quyết định bảo hành luôn thuộc hãng / người.


## UC6 — Khép vòng — phòng tái phát

**customer:** Vừa sửa xong 3 ngày, đèn cảnh báo lại sáng. Tôi lại phải gọi, kể lại từ đầu, không biết có mất tiền không.
**outcome:** Doanh nghiệp nhận lỗi trước khi khách phải gọi, ưu tiên sửa lại, khách chỉ cần chọn giờ.
**type:** SPEC ONLY · closed-loop care
**name:** Recurrence / Return-of-Friction Prevention — sửa xong nhưng tín hiệu quay lại
**context:** Case đã resolved, tín hiệu liên quan quay lại trong cửa sổ xác minh. Detector tất định liên kết với case cũ; Agent đánh giá 'lần can thiệp trước có thật sự giải quyết không'. Tối đa 2 chu kỳ tự động. Synthetic / illustrative scenario for MVP.
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
- Theo dõi sau sửa
**brk:** 4
**breakpoint:** Không ai theo dõi sau khi đóng lệnh; tín hiệu lặp lại nằm trong telematics, xưởng không thấy.
**rules:**
- Cùng hệ thống báo lại ≤ 30 ngày → candidate (comeback)
- Tái phát lần 2 → người (trưởng kỹ thuật); không tự mở lại lần 3
- Tin xin lỗi không quy lỗi, không khẳng định nguyên nhân
- Chi phí comeback: giả định không tính phí (chờ chính sách)
**signal:** ON vehicle.dtc.raised
  IF RO closed < 30d, cùng hệ thống
  AND (WARNING >= 1 OR INFO >= 2)
  AND no open case / appointment
  THEN candidate(UC6)  # không LLM
CRITICAL → SafetyPath
**action:** Agent so hạng mục đã sửa với tín hiệu mới → chọn: check-in / đề nghị kiểm tra lại / mở lại ưu tiên / escalate. Mở lại hồ sơ nội bộ (mức 1); đặt lịch cần khách xác nhận (UC3).
**message:** Chào chị Mai, hệ thống ghi nhận cảnh báo hệ thống điều hoà trên xe VF 7 của chị xuất hiện lại sau lần sửa ngày 20/9. Bên em rất tiếc. Xưởng đã mở lại hồ sơ với mức ưu tiên cao; chị chọn giúp em khung giờ phù hợp trong app nhé.
**verify:** Sửa lần 2 · telematics 30 ngày không ghi nhận lại · tái phát lần 2 → chuyển người
**kpi:** Comeback Rate, thời gian phát hiện comeback
**cost:**
- Khách tự phát hiện, bực hơn nhiều
- Chỉ số 'sửa đúng lần đầu' sai sự thật
- Rủi ro hỏng lan rộng nếu chậm
**trace:**
- t: T0 · 23/9 07:40 · l: L0 · ttl: Tín hiệu quay lại · d: vehicle.dtc.raised mã điều hoà (WARNING) · tok: 0
- t: T+1 s · l: L0 · ttl: Detector · d: RO-5402 cùng hệ thống đóng 3 ngày trước ✓ · WARNING ≥ 1 ✓ · không case mở ✓ → candidate(UC6, count = 1) · tok: 0
- t: T+1 s · l: L0 · ttl: Arbitration qua · d: Sau giờ yên tĩnh · 0/3 tin tuần này → allowed · tok: 0
- t: T+1 s · l: Tool · ttl: Gom ngữ cảnh · d: RO-5402 (hạng mục, linh kiện) · lịch sử mã · KB → ContextBundle · tok: 0
- t: T+2 s · l: L2 · ttl: AGENT so case cũ · d: Cùng hệ thống, sau 3 ngày → lần trước có thể chưa giải quyết triệt để; chọn reopen_case ưu tiên + kiểm tra lại; cần khách chọn giờ; chưa cần người (lần 1) · tok: 2000
- t: T+3 s · l: Validator · ttl: Kiểm tra · d: Tin xin lỗi không quy lỗi ✓ · claim_check ✓ · chu kỳ 1/2 ✓ · tok: 0
- t: T+3 s · l: Act · ttl: Executor (mức 1) · d: Mở lại RO-5402, giữ slot ưu tiên chờ khách · tok: 0
- t: 08:00 · l: Inform · ttl: Báo khách · d: Tin xin lỗi + chọn giờ (đặt lịch = mức 2, qua UC3) · tok: 300
- t: 08:20 · l: Customer · ttl: Khách chọn · d: 9:00 thứ Hai tuần sau → POST /confirm · tok: 0
- t: +30 ngày · l: Verify · ttl: Xác minh bằng dữ liệu xe · d: Sửa lần 2 xong; telematics 30 ngày không ghi nhận lại → resolved. Tái phát lần 2 → handoff trưởng kỹ thuật · tok: 0
**note:** Closed-loop care: Detect → Act → Verify → Observe outcome → Detect recurrence. Outcome được xác minh bằng dữ liệu của chính chiếc xe.

