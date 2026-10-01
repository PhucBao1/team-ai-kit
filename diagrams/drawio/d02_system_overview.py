from pathlib import Path

from dio import D

d = D("02-system-overview")
d.text(20, 10, 1800, 40, "<b style='font-size:20px'>System Overview</b> &nbsp; <font color='#6b7280'>Luồng chính (1)→(12) · proactive (P1)→(P2) rồi đi tiếp từ (3) · chuyển người (H1)→(H3)</font>", size=14)

# nhóm (subgraph)
d.group(700, 60, 480, 110, "Bên ngoài · AI", kind="ext")
d.group(20, 230, 230, 370, "Frontend (React)", kind="white")
d.group(350, 230, 230, 370, "Backend API (FastAPI)", kind="white")
d.group(680, 230, 520, 230, "Agent · LangGraph — chỉ ĐỀ XUẤT, không ghi", kind="llm")
d.group(680, 500, 520, 130, "An toàn & thực thi — code tất định", kind="write")
d.group(680, 670, 520, 120, "Dữ liệu vận hành", kind="data")
d.group(1310, 230, 230, 400, "Tích hợp", kind="code")
d.group(1650, 230, 240, 400, "Bên ngoài · doanh nghiệp", kind="ext")

# node
d.box(830, 90, 220, 60, "Gemini (Vertex AI)", "Flash · Flash-Lite · Pro", kind="llm", id="gem")
d.box(35, 270, 200, 120, "Chat khách hàng", "App · Zalo · Web\nnút Xác nhận hiện đủ tham số", kind="human", id="chat")
d.box(35, 480, 200, 90, "Console nhân viên CSKH", "handoff card · copilot", kind="human", id="console")
d.box(365, 270, 200, 120, "Chat & Confirm API", "/chat (SSE) · /confirm\nxác thực · che PII · ký token", kind="code", id="api")
d.box(365, 480, 200, 90, "Handoff API", "/handoffs · hàng đợi · SLA", kind="code", id="hapi")
d.box(700, 270, 200, 56, "Triage & context builder", "ý định · mức khẩn · journey · KB", kind="llm", id="tri", size=12)
d.box(980, 270, 200, 56, "Coordinator agent", "giữ goal stack · định tuyến", kind="llm", id="coord", size=12)
subs = [("PolicyQA", "RAG có phiên bản", "llm"), ("Scheduler", "6 quyết định UC1", "llm"),
        ("Writer ⇄ Critic", "soạn + claim check", "llm"), ("Handoff builder", "lắp HandoffCard", "code")]
for i, (t, s, k) in enumerate(subs):
    d.box(700 + i * 122, 350, 112, 60, t, s, kind=k, id=f"sub{i}", size=11)
d.box(700, 535, 200, 80, "Validator 7 kiểm tra", "token · quyền theo xe · linh kiện\nslot · kỹ thuật viên", kind="code", id="val", size=12)
d.box(980, 535, 200, 80, "Executor", "nơi DUY NHẤT được ghi\nidempotency · saga · outbox", kind="write", id="exe", size=12)
d.cyl(860, 700, 190, 80, "Postgres", "journey · audit · checkpoint · KB pgvector", id="pg")
d.box(1325, 275, 200, 80, "Pub/Sub + Detector L0", "rule tất định ~0 token\narbitration chống làm phiền", kind="code", id="det", size=12)
d.box(1325, 480, 200, 110, "MCP tool servers", "đọc: xe · mã lỗi · bảo hành · lịch\nghi (level 2): đặt / đổi lịch", kind="code", id="mcp", size=12)
d.box(1665, 275, 210, 90, "Hệ thống nguồn", "DMS · ERP kho · Telematics\nCSMS · Bảo hành", kind="ext", id="src")

P = "#7c3aed"; OR = "#ea580c"; Y = "#ca8a04"; G = "#059669"; B = "#2563eb"; K = "#374151"
e = d.edge
# luồng chính
e("chat", "api", "(1) tin nhắn", color=Y, exitX=1, exitY=0.2, entryX=0, entryY=0.2)
e("api", "tri", "(2) tin đã che PII", color=K, exitX=1, exitY=0.2, entryX=0, entryY=0.3)
e("tri", "coord", "(3) ý định", color=P)
e("coord", "mcp", "(4) gọi tool đọc", color=K, pts=[(1270, 290), (1270, 505)], exitX=1, exitY=0.35, entryX=0, entryY=0.23)
e("mcp", "coord", "(5) dữ liệu thật", color=G, pts=[(1245, 555), (1245, 312)], exitX=0, exitY=0.68, entryX=1, entryY=0.75)
e("sub2", "api", "(6) trả lời có nguồn + phương án", color=P, pts=[(944, 440), (640, 440), (640, 340)], exitX=0.5, exitY=1, entryX=1, entryY=0.58)
e("api", "chat", "(7) stream + nút Xác nhận", color=P, exitX=0, exitY=0.55, entryX=1, entryY=0.55)
e("chat", "api", "(8) bấm Xác nhận (token)", color=Y, exitX=1, exitY=0.85, entryX=0, entryY=0.85)
e("api", "val", "(9) token hợp lệ", color=Y, pts=[(465, 460), (610, 460), (610, 575)], exitX=0.5, exitY=1, entryX=0, entryY=0.5)
e("val", "exe", "(10) đạt", color=OR)
e("exe", "mcp", "(11) gọi tool ghi", color=OR, exitX=1, exitY=0.5, entryX=0, entryY=0.87)
e("mcp", "src", "(12) đọc / ghi theo quyền", color=OR, pts=[(1595, 505), (1595, 320)], exitX=1, exitY=0.23, entryX=0, entryY=0.78)
e("src", "mcp", "dữ liệu thật", color=G, pts=[(1770, 560)], exitX=0.5, exitY=1, entryX=1, entryY=0.73)
# proactive
e("src", "det", "(P1) sự kiện: kho · lịch · mã lỗi", color=G, exitX=0, exitY=0.3, entryX=1, entryY=0.34)
e("det", "coord", "(P2) candidate", color=G, pts=[(1425, 215), (1150, 215)], exitX=0.5, exitY=0, entryX=0.85, entryY=0)
# chuyển người
e("sub3", "hapi", "(H1) HandoffCard", color=P, pts=[(1066, 470), (660, 470), (660, 525)], exitX=0.5, exitY=1, entryX=1, entryY=0.5)
e("hapi", "console", "(H2) card + hạn gọi lại", color=P, exitX=0, exitY=0.3, entryX=1, entryY=0.3)
e("console", "hapi", "(H3) NV chốt · trả việc", color=Y, dashed=True, exitX=1, exitY=0.75, entryX=0, entryY=0.75)
# hỗ trợ
e("coord", "gem", "prompt (đã che PII)", color=P, pts=[(1010, 200)], exitX=0.15, exitY=0, entryX=0.82, entryY=1)
e("gem", "tri", "trả lời · tool call", color=P, pts=[(860, 200)], exitX=0.14, exitY=1, entryX=0.8, entryY=0)
e("exe", "pg", "ghi audit", color=OR, exitX=0.5, exitY=1, entryX=0.62, entryY=0)
e("pg", "tri", "đọc journey · KB", color=B, dashed=True, pts=[(665, 740), (665, 305)], exitX=0, exitY=0.5, entryX=0, entryY=0.63)

lx, ly = 20, 820
for k, (kind, name) in enumerate([("llm", "Có gọi LLM"), ("code", "Code tất định"), ("write", "Ghi hệ thống"),
                                   ("human", "Người dùng / người duyệt"), ("data", "Dữ liệu"), ("ext", "Bên ngoài")]):
    x = lx + k * 190
    d.box(x, ly, 24, 20, "", kind=kind)
    d.text(x + 30, ly - 3, 160, 26, name, size=12)
d.text(1180, 815, 720, 30, "<font color='#6b7280'>Hai chiều = 2 mũi tên, mỗi chiều một nhãn · chi tiết bên trong Agent: <b>Agent Flow Diagram</b></font>", size=11)
Path("02-system-overview.drawio").write_text(d.xml(), encoding="utf-8")
