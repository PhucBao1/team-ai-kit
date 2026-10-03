# 08 · MVP & kịch bản demo — Preemptive Service Friction Rescue — một kịch bản bao trọn đề bài

> Trích từ Proposal EV CX Agent. Nguồn gốc: file HTML cùng tên. Sửa nội dung ở file HTML rồi chạy lại script chuyển đổi, hoặc sửa file .md này và ghi chú trong PR.

Demo bắt đầu từ **tín hiệu hệ thống**, không phải từ khách: mã lỗi lặp lại → L0 phát hiện (UC1) → agent điều tra và chủ động nhắn → hội thoại nhiều mục đích → UC3 lập phương án đa ràng buộc, đặt lịch có xác nhận → linh kiện bị điều đi → lập lại phương án → khách bực → chuyển người kèm tóm tắt → xác minh bằng dữ liệu xe. Mọi yêu cầu của đề xuất hiện trong một câu chuyện. *Synthetic / illustrative scenario for MVP.*

Thứ Ba 08:15 · telematics · VF 8 …4821 · mã lỗi hệ thống làm mát pin · severity = WARNING · lần thứ 3 trong 14 ngày · chưa có lịch / ticket → L0 tạo candidate UC1 (0 token) → arbitration qua → Agent được gọiChào anh Minh, xe VF 8 của anh đã ghi nhận cảnh báo ở hệ thống làm mát pin 3 lần trong 14 ngày, mức **cảnh báo** (chưa nguy hiểm). Theo hướng dẫn của hãng cho mã lỗi này, anh vẫn di chuyển được nhưng nên kiểm tra sớm. Em đã kiểm tra: lỗi này **không khắc phục được bằng cập nhật phần mềm từ xa**, cần kiểm tra tại xưởng. Anh có muốn em đặt lịch không?  
*Vì sao anh nhận tin này: xe gửi cảnh báo lặp lại 3 lần trong 14 ngày và anh đã bật thông báo dịch vụ.*nguồn: KB mã lỗi v3.2 (giả định) · telematics 08:15Ừ đặt giúp anh cuối tuần. Mà cái này có được bảo hành không em?Về bảo hành: xe anh mua 14/03/2024, hiện 38.420 km, đăng ký sử dụng cá nhân — trong thời hạn 10 năm hoặc 200.000 km của VF 8. Anh bảo dưỡng đúng lịch tại xưởng ủy quyền (gần nhất 02/2026), nên đủ điều kiện **sơ bộ**; xưởng sẽ kết luận sau khi kiểm tra.  
  
Về lịch: thứ Bảy 3/10, xưởng Long Biên (4 km từ nhà anh) đã có sẵn linh kiện dự kiến cho mã lỗi này, còn 9:00 hoặc 14:00. Pin xe hiện 42%, đủ đi tới xưởng.nguồn: chính sách bảo hành công bố · hồ sơ xe · odometer · DMS · ERP kho9h nhéEm xác nhận: **kiểm tra hệ thống làm mát pin · VF 8 30A-xxx.xx · 9:00 thứ Bảy 3/10 · xưởng Long Biên · dự kiến 2 giờ**. Anh bấm Xác nhận để em đặt nhé.Xác nhậnĐổi giờĐã đặt lịch SA-20931. Linh kiện đã được giữ cho xe anh. Em sẽ nhắc anh tối thứ Sáu.— hai ngày sau, khách không làm gì —Thứ Năm 14:02 · ERP kho (UC3 · nhánh lập lại) · reservation linh kiện cho SA-20931 bị huỷ (điều chuyển cho xe triệu hồi)Chào anh Minh, linh kiện cho lịch 9:00 thứ Bảy của anh tại Long Biên vừa bị điều chuyển nên chưa kịp về. Em rất tiếc. Bên em có 2 phương án:  
(1) Giữ nguyên 9:00 thứ Bảy, chuyển sang **xưởng Gia Lâm** (cách nhà anh 6 km) đã có sẵn linh kiện.  
(2) Dời sang **9:00 thứ Ba 6/10** tại Long Biên khi linh kiện về.Phương án 1Phương án 2Gặp nhân viênnguồn: ERP kho 14:02 · DMS slot · khoảng cách từ địa chỉ đã đăng kýSao lại thế, anh sắp xếp hết rồi. Cho anh nói chuyện với người.Em hiểu, và xin lỗi anh vì sự bất tiện này. Em chuyển anh cho CVDV Hải ngay — anh Hải đã có đầy đủ thông tin, anh không cần kể lại. Anh Hải sẽ gọi anh trong 15 phút.chuyển người → CVDV Hải nhận handoff card lúc 14:07 · xem "Phía nhân viên" bên dướiAnh Hải đã nhận thông tin và sẽ gọi anh ngay. Đây là cuộc trò chuyện với nhân viên, em sẽ cập nhật lại lịch ở đây sau khi anh chốt.14:11 · CVDV Hải gọi · khách chọn phương án 1 · agent gửi xác nhận lịch mới vào chatLịch mới đã được xác nhận: **9:00 thứ Bảy 3/10 · xưởng Gia Lâm** · linh kiện đã giữ cho xe anh · người phụ trách: CVDV Hải. Em sẽ nhắc anh tối thứ Sáu.nguồn: DMS SA-20931 (cập nhật 14:18) · ERP reservation #R-7702— thứ Bảy + 14 ngày —Verify · xe sửa xong 11:30 thứ Bảy · telematics 14 ngày không ghi nhận lại mã lỗi → RECOVERED

| Khoảnh khắc trong demo | Thể hiện |
| --- | --- |
| UC1 · tín hiệu lặp lúc 08:15 (khách chưa làm gì) | L0 đếm 3 lần / 14 ngày, 0 token; arbitration; agent điều tra; ① phân loại từ xa: không sửa được qua phần mềm |
| "Có được bảo hành không" | Goal stack (2 mục đích); ② bộ tính bảo hành tất định; không kết luận thay xưởng |
| "Đã có sẵn linh kiện… pin 42% đủ đi" | UC3 · ④ dự đoán linh kiện; ⑤ xếp lịch theo quãng đường; phương án bị loại đều có lý do |
| Nút Xác nhận | Xác nhận mức 2, nhắc lại đủ tham số |
| Thứ Năm 14:02 | UC3 · nhánh lập lại: lịch đã xác nhận mất linh kiện; phát hiện lệch lịch – kho trước khi khách đến xưởng |
| 2 phương án | L2 lập phương án; validator kiểm tra; không tự đổi lịch |
| Khách bực → gặp người | Handoff card lắp từ dữ liệu có cấu trúc; copilot trong cuộc gọi; auto-wrap; agent nhận lại việc sau khi chốt |
| 14 ngày sau | ⑥ xác minh bằng dữ liệu xe, không chỉ "đã đóng lệnh"; tái phát → UC6 |

### Màn hình "Việc của tôi" — khách tự thấy lời hứa đang mở

Việc của tôiSửa hệ thống làm mát pin · VF 8Bảo hành: đủ điều kiện sơ bộ · xưởng xác nhận khi kiểm traĐặt lịchGiữ linh kiệnChờ hẹnChẩn đoánSửaXác minh**9:00 thứ Bảy 3/10** · Xưởng Gia LâmPhụ trách: CVDV HảiThay đổi gần nhất (Thứ Năm 14:18): đổi sang xưởng Gia Lâm vì linh kiện ở Long Biên chưa về kịp. Anh đã đồng ý qua điện thoại.Gọi CVDVĐổi lịchGặp nhân viênSau chẩn đoán: **video kỹ thuật viên giải thích lỗi** và báo giá sẽ hiện ở đây · thanh toán phần ngoài bảo hành ngay trong app khi nhận xeNhắc bảo dưỡng định kỳDự kiến khi đạt ~40.000 km (theo quãng đường thực tế của xe)Bên em sẽ nhắc trước 10 ngày.

Khách giục vì bất định. Cách giảm bất định tốt nhất là để khách **tự nhìn thấy**, như màn hình theo dõi đơn giao hàng. Ứng dụng VinFast công khai đã có "theo dõi tiến độ sửa chữa"; đề xuất nâng cấp nó thành màn hình hiển thị Journey State Graph cho khách:

- **Trạng thái thật** lấy từ vòng đời lệnh sửa chữa (§03), không phải trạng thái cập nhật tay.
- **Lời hứa và người phụ trách** hiển thị rõ — ai chịu trách nhiệm, hạn khi nào.
- **Nói thật khi thay đổi:** mọi thay đổi có dòng giải thích lý do và thời điểm.
- **Bước "Xác minh"** là bước cuối: việc chỉ "xong" khi dữ liệu xe xác nhận lỗi đã hết.
- Luôn có nút **Gặp nhân viên** — nguyên tắc không ngõ cụt.
- **Video kỹ thuật viên** giải thích lỗi và **thanh toán trong app** — như BMW Proactive Care đang làm; giúp khách hiểu vì sao phải sửa và giảm thời gian chờ khi nhận xe.

Tin nhắn chủ động và màn hình này dùng chung một nguồn dữ liệu, nên không bao giờ nói hai điều khác nhau.

### Phía nhân viên: khi khách muốn gặp người

Đề bài yêu cầu khách không phải trình bày lại. Vì vậy thứ quan trọng không phải là "có chuyển người", mà là **nhân viên nhận được gì trong 10 giây đầu**. Dưới đây là màn hình CVDV Hải thấy lúc 14:07.

**Handoff** · Trần Minh · VF 8 30A-xxx.xx · từ chat appGọi lại trước 14:21 (agent đã hứa 15 phút) · còn 14 phút**Tóm tắt 1 câu:** Linh kiện cho lịch sửa làm mát pin 9:00 thứ Bảy tại Long Biên bị điều đi; khách đã được đề xuất 2 phương án, đang bực vì đã sắp xếp công việc, muốn nói chuyện với người.

###### Khách & xe

- Đã xác thực qua app · chủ xe
- VF 8 · mua 14/03/2024 · 38.420 km · cá nhân
- Kênh ưa thích: gọi điện sau 12:00 memory

###### Mục đích trong hội thoại

- ✓ Giải thích cảnh báo làm mát pin
- ✓ Bảo hành: đủ điều kiện sơ bộ kb:warranty_v2026.03
- … Đổi lịch: **đang chờ khách chọn**

###### Dữ kiện từ hệ thống

- SA-20931 · 03/10 09:00 · Long Biên · confirmed DMS
- Reservation huỷ 14:02 · điều cho xe triệu hồi ERP
- Gia Lâm: có linh kiện, slot 09:00 đang khoá tạm đến 14:34 ERP · DMS
- Pin 42%, đủ đi tới cả hai xưởng telematics

###### Agent đã nói & hứa

- "Xưởng Gia Lâm (6 km) đã có sẵn linh kiện"
- "Anh Hải sẽ gọi anh trong 15 phút"
- Đã xin lỗi 1 lần
- Chưa hứa bồi thường hay ưu đãi nào

###### Cảm xúc & ưu tiên

- **Bực** — "anh sắp xếp hết rồi"
- Chưa phải khiếu nại chính thức
- Lần đầu gặp sự cố với xưởng này

###### Gợi ý bước tiếp theo

- Mở đầu: xin lỗi, xác nhận đã nắm việc
- Ưu tiên phương án 1 (giữ giờ, Gia Lâm)
- Nếu khách ngại đi xa: đề xuất xem xét hỗ trợ đi lại theo chính sách SOP-DV-12

###### Không làm

- Không hỏi lại biển số, tình trạng xe, lịch cũ
- Không hứa "chắc chắn bảo hành" — xưởng kết luận sau kiểm tra
- Không hứa ưu đãi ngoài chính sách

###### Nguồn & lịch sử

- Toàn bộ hội thoại (8 lượt) · audit log quyết định
- Handoff card đi qua claim check: mọi mốc, mã, số đều có nguồn

### Cuộc gọi tiếp nối — nhân viên có copilot

14:11 · CVDV Hải gọi khách · copilot nghe và gợi ý trên màn hình (chỉ nhân viên thấy)[Hải] Chào anh Minh, em là Hải bên xưởng Long Biên. Em đã nắm việc linh kiện cho lịch thứ Bảy của anh bị điều đi, em xin lỗi anh vì chuyện này.Ừ, anh xin nghỉ rồi. Gia Lâm thì cũng được nhưng chắc chắn có đồ chưa em?copilot gợi ý: "Linh kiện đã được giữ tạm tại Gia Lâm cho xe anh, khoá đến 14:34" · nguồn ERP reservation #R-7702 · Hải xác nhận dùng[Hải] Dạ linh kiện đã được giữ riêng cho xe anh ở Gia Lâm rồi ạ. Nếu anh đồng ý em chốt 9:00 thứ Bảy luôn, em vẫn là người phụ trách xe anh.Ok chốt vậy.14:17 · Hải chốt trong DMS (khách đồng ý bằng lời, có ghi âm) · auto-wrap: AI soạn ghi chú cuộc gọi + gắn nhãn lý do liên hệ "đổi lịch do thiếu linh kiện" → Hải đọc và xác nhận trong 20 giây14:18 · agent nhận lại việc: gửi xác nhận lịch mới vào chat của khách, đặt nhắc tối thứ Sáu, tiếp tục theo dõi đến khi xác minh xong

| Loại handoff | Khi nào | Nhân viên nhận gì |
| --- | --- | --- |
| **Chat → nhân viên** (như trên) | Khách yêu cầu, bực, agent không chắc | Handoff card + copilot; agent nhận lại việc sau khi chốt |
| **Tổng đài giọng nói → tổng đài viên** | Khách gọi, AI không xử lý được | **Chuyển máy có giới thiệu:** tổng đài viên nghe bản tóm tắt 1 câu và thấy handoff card *trước khi* nối máy, nên câu đầu tiên đã đúng việc |
| **Ngoài giờ** (UC2) | Không có nhân viên trực chat | Việc khẩn → tổng đài 24/7 ngay; việc thường → ticket kèm card, khách được hẹn giờ cụ thể |
| **Khiếu nại chính thức** | Bộ phát hiện khiếu nại kích hoạt | Card + toàn bộ lịch sử chuyển bộ phận xử lý khiếu nại; agent không gửi tin bán hàng, không tự giải quyết cho xong |
| **An toàn** | Mã lỗi CRITICAL, mô tả nguy hiểm | Chuyển 24/7 ngay với vị trí (có đồng ý), tình trạng pin, mã lỗi — không chờ tóm tắt đầy đủ |

**Cách tóm tắt được tạo:** không phải LLM "viết tự do" từ hội thoại. Card được **lắp từ dữ liệu có cấu trúc** (goal stack, kết quả tool, audit log, lời hứa đã trích); LLM chỉ viết câu tóm tắt 1 dòng và phần cảm xúc, rồi đi qua claim check. Đo bằng **Re-ask Rate**: nhân viên có phải hỏi lại điều đã có trong card không. Nhân viên sửa card → dùng làm dữ liệu cải thiện.```text
Thứ Năm 14:02  Kho điều linh kiện đi — không ai kiểm tra lịch hẹn
Thứ Bảy 08:30  Khách xin nghỉ, lái xe tới xưởng
Thứ Bảy 09:05  CVDV: "Linh kiện chưa về anh ạ"
Thứ Bảy 09:10  Khách về; gọi tổng đài khiếu nại, kể lại từ đầu
Thứ Hai        CSKH tạo ticket, chuyển xưởng; xưởng hẹn lại
               → 1 slot lãng phí · 2+ contact · 1 khiếu nại · niềm tin giảm
``````text
Thứ Năm 14:02  L0 phát hiện reservation bị huỷ cho lịch còn 67 giờ
Thứ Năm 14:03  Agent lập 2 phương án, validator kiểm tra
Thứ Năm 14:04  Khách nhận tin, chọn (hoặc gặp CVDV kèm tóm tắt)
Thứ Năm 14:21  Lịch + linh kiện mới được giữ, slot cũ giải phóng
Thứ Bảy 11:30  Sửa xong đúng hẹn · 14 ngày telematics xác nhận
               → 0 slot lãng phí · 0 contact phải tự khởi xướng · verified
```

### Validator trước khi đổi lịch (mức 2)

| Check | Quy tắc | Không đạt thì |
| --- | --- | --- |
| `customer_verified` | Phiên app hoặc OTP; khách sở hữu xe | Dừng, yêu cầu xác thực |
| `part_matches_vin` | Mã linh kiện khớp đời xe theo số khung | Chuyển CVDV |
| `technician_certified` | Xưởng có kỹ thuật viên đủ chứng chỉ cho hạng mục (ví dụ pin cao áp) | Loại phương án |
| `part_reserved` | Linh kiện đã được giữ cho đúng lệnh, đúng xưởng | Loại phương án |
| `slot_locked` | Slot được khoá tạm trong thời gian chờ khách xác nhận | Tìm slot khác |
| `customer_confirmed` | Khách bấm xác nhận đúng phương án, tham số không đổi sau đó | Không ghi |
