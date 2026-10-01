from pathlib import Path

from dio import D

d = D("01-context")
d.text(
    20,
    10,
    1100,
    40,
    "<b style='font-size:20px'>EV CX Agent — nhìn tổng thể</b> &nbsp; <font color='#6b7280'>Context view · ai dùng, hệ thống nói chuyện với ai</font>",
    size=14,
)

L = (20, 250)
CX, CW = 560, 420
R = (1280, 270)
boxes = {
    "cus": (L[0], 110, L[1], 120),
    "nv": (L[0], 310, L[1], 120),
    "core": (CX, 100, CW, 340),
    "src": (R[0], 110, R[1], 120),
    "mgr": (R[0], 310, R[1], 120),
}
d.box(
    *boxes["cus"],
    "Chủ xe / người lái",
    "Chat trong app · Zalo · Web\nTổng đài",
    kind="human",
    id="cus",
    size=15,
)
d.box(
    *boxes["nv"], "Nhân viên CSKH / CVDV", "Console: handoff card · copilot", kind="human", id="nv", size=15
)
d.box(
    *boxes["core"],
    "EV CX Agent",
    "AI chăm sóc khách hàng hậu mãi xe điện\n\n• Hiểu ý định xuyên suốt cuộc hội thoại\n• Tra cứu KB có phiên bản\n• Dùng tool có phân quyền\n• Chủ động phát hiện việc bị kẹt\n• Chuyển người kèm tóm tắt",
    kind="llm",
    id="core",
    size=20,
)
d.box(
    *boxes["src"],
    "Hệ thống nguồn",
    "DMS xưởng · ERP kho · Telematics\nCSMS trạm sạc · Bảo hành",
    kind="ext",
    id="src",
    size=15,
)
d.box(
    *boxes["mgr"],
    "Quản lý CX / vận hành",
    "Dashboard: CSAT · Contacts per Job\ncứu trước hẹn · chi phí / việc",
    kind="data",
    id="mgr",
    size=15,
)
d.box(
    CX,
    470,
    CW,
    60,
    "Không bịa · Xác nhận trước khi ghi · Người luôn có mặt",
    "ràng buộc gốc của đề — thực thi bằng code tất định",
    kind="write",
    id="rule",
    size=14,
)


def line(a, b, y, label, color, dashed=False):
    ax, ay, _aw, ah = boxes[a]
    bx, by, _bw, bh = boxes[b]
    exitX = 1 if ax < bx else 0
    entryX = 0 if ax < bx else 1
    d.edge(
        a,
        b,
        label,
        color=color,
        dashed=dashed,
        exitX=exitX,
        exitY=round((y - ay) / ah, 3),
        entryX=entryX,
        entryY=round((y - by) / bh, 3),
        extra="edgeStyle=none;labelBackgroundColor=#ffffff;fontSize=12;",
    )


line("cus", "core", 150, "hỏi · xác nhận", "#ca8a04")
line("core", "cus", 195, "trả lời có nguồn · tin chủ động", "#7c3aed")
line("core", "nv", 350, "handoff card — khách không kể lại", "#7c3aed")
line("nv", "core", 395, "chốt phương án · trả lại việc", "#ca8a04", dashed=True)
line("src", "core", 150, "sự kiện: kho · lịch · mã lỗi · sạc", "#059669")
line("core", "src", 195, "đọc / ghi qua tool có quyền", "#ea580c")
line("core", "mgr", 370, "metric CX · VoC", "#2563eb")
d.text(
    CX,
    545,
    CW,
    30,
    "<font color='#6b7280'>Chi tiết bên trong: sơ đồ 02 (container) → 03 (GCP) → 04–09</font>",
    size=12,
    align="center",
)
Path("01-context.drawio").write_text(d.xml(), encoding="utf-8")
