from pathlib import Path

from dio import D

d = D("03-deployment")
TAG = {
    "MVP": ("#dcfce7", "#166534"),
    "T1–2": ("#dbeafe", "#1e40af"),
    "T3": ("#fef3c7", "#92400e"),
    "Prod": ("#e5e7eb", "#374151"),
}


def zone(x, y, w, h, title, color="#6b7280", fill="#f9fafb", dashed=False):
    st = (
        f"rounded=1;arcSize=2;html=1;fillColor={fill};strokeColor={color};verticalAlign=top;align=left;spacingLeft=8;"
        f"spacingTop=2;fontSize=12;fontStyle=1;fontColor=#374151;{'dashed=1;dashPattern=8 4;' if dashed else ''}"
    )
    return d._cell(None, title, st, x, y, w, h, "1")


def ic(x, y, shape, title, sub="", tag=None, id=None, top=False):
    i = d.icon(x, y, shape, title, sub, id=id, top=top)
    if tag:
        f, c = TAG[tag]
        d._cell(
            None,
            tag,
            f"rounded=1;arcSize=40;html=1;fillColor={f};strokeColor={c};fontColor={c};fontSize=9;fontStyle=1;",
            x + 34 if not top else x - 30,
            y - 8 if not top else y + 36,
            34,
            16,
            "1",
        )
    return i


d.text(
    20,
    10,
    1700,
    40,
    "<b style='font-size:20px'>Deployment Diagram — GCP</b> &nbsp; <font color='#6b7280'>(1)→(8) một lượt chat có đặt lịch · (P1)→(P3) proactive · nhãn = mốc có thành phần</font>",
    size=14,
)

zone(20, 70, 200, 330, "Người dùng")
ic(98, 120, "users", "Khách hàng", "App · Zalo · Web", "MVP", id="cus")
ic(98, 280, "users", "Nhân viên CSKH", "Console", "MVP", id="nv")
zone(20, 430, 200, 330, "Việt Nam · ngoài GCP")
ic(
    98,
    480,
    "lock",
    "Identity vault",
    "định danh thật lưu trong nước\nGCP chỉ thấy mã giả danh",
    "Prod",
    id="vault",
)
ic(
    98,
    640,
    "external_data_center",
    "Hệ thống nguồn",
    "DMS · ERP · Telematics · CSMS\n(MVP: giả lập)",
    "MVP",
    id="src",
)

d._cell(
    None,
    "Google Cloud · asia-southeast1 · VPC Service Controls",
    "rounded=1;arcSize=1;html=1;fillColor=none;strokeColor=#dc2626;dashed=1;dashPattern=10 5;strokeWidth=2;verticalAlign=top;align=left;spacingLeft=10;spacingTop=4;fontSize=13;fontStyle=1;fontColor=#991b1b;",
    260,
    55,
    1490,
    730,
    "1",
)

zone(290, 95, 150, 305, "Biên")
ic(343, 145, "https_load_balancer", "HTTPS LB", "+ Cloud Armor", "T1–2", id="lb")
ic(343, 290, "identity_aware_proxy", "IAP", "xác thực NV", "T1–2", id="iap")

zone(480, 95, 700, 305, "Serving · Cloud Run", color="#2563eb", fill="#f8fbff")
ic(520, 150, "cloud_run", "web", "React", "MVP", id="web")
ic(700, 150, "cloud_run", "api", "FastAPI · SSE", "MVP", id="api")
ic(880, 150, "cloud_run", "agent · LangGraph", "", "MVP", id="agent", top=True)
ic(1060, 150, "cloud_run", "executor", "nơi duy nhất ghi", "MVP", id="exe")
ic(790, 300, "cloud_run", "mcp tool servers", "", "T1–2", id="mcp")

zone(1220, 95, 220, 150, "AI", color="#7c3aed", fill="#faf5ff")
ic(1308, 140, "cloud_machine_learning", "Gemini (Vertex AI)", "", "MVP", id="gem")

zone(1470, 95, 260, 330, "Bảo mật · vận hành (mọi service)", color="#dc2626", fill="#fffafa")
ic(1515, 135, "key_management_service", "Secret Manager", "+ KMS", "MVP")
ic(1640, 135, "cloud_iam", "IAM", "quyền tối thiểu", "MVP")
ic(1515, 235, "data_loss_prevention_api", "Sensitive Data", "Protection", "T1–2")
ic(1640, 235, "logging", "Logging · Trace", "OTel GenAI", "MVP")
ic(1515, 335, "container_builder", "Cloud Build", "eval gate", "T1–2")
ic(1640, 335, "cloud_run", "Langfuse", "trace · eval", "MVP")

zone(480, 440, 300, 160, "Sự kiện", color="#059669", fill="#f7fdfb")
ic(520, 490, "cloud_pubsub", "Pub/Sub", "schema · DLQ", "T1–2", id="ps")
ic(680, 490, "cloud_run", "detector-worker", "rule L0", "T1–2", id="det")

zone(820, 440, 360, 160, "Dữ liệu vận hành", color="#2563eb", fill="#f8fbff")
ic(960, 490, "cloud_sql", "Cloud SQL → AlloyDB", "+ pgvector", "MVP", id="db")
ic(1100, 490, "cloud_memorystore", "Memorystore", "Redis", "T1–2", id="redis")

zone(1220, 460, 510, 160, "Phân tích", color="#2563eb", fill="#f8fbff")
ic(1270, 500, "cloud_storage", "Cloud Storage", "bronze / silver", "T3", id="gcs")
ic(1440, 500, "bigquery", "BigQuery", "gold · eval_runs", "T1–2", id="bq")
ic(1610, 500, "data_studio", "Looker", "dashboard CX", "T1–2", id="looker")

# nhãn mốc + ghi chú
for k, (t, desc) in enumerate(
    [("MVP", "demo 30/9"), ("T1–2", "trước 11/10"), ("T3", "tuần 3"), ("Prod", "production")]
):
    f, c = TAG[t]
    x = 820 + k * 150
    d._cell(
        None,
        t,
        f"rounded=1;arcSize=40;html=1;fillColor={f};strokeColor={c};fontColor={c};fontSize=10;fontStyle=1;",
        x,
        660,
        40,
        18,
        "1",
    )
    d.text(x + 46, 656, 100, 26, desc, size=11)
d.text(
    520,
    690,
    1200,
    80,
    "• MVP 30/9 chỉ cần: 1 service Cloud Run (web + api + agent + executor chung) · Cloud SQL · Gemini · Secret Manager · Logging.<br>"
    "• Chỉ service <b>executor</b> có quyền IAM gọi tool ghi; agent chỉ đọc. Dữ liệu định danh thật nằm ở identity vault trong nước.<br>"
    "• Tuần 3 / production bổ sung: GKE Autopilot (Temporal, vLLM) · Datastream · Dataflow · Dataplex · Model Armor — không vẽ để sơ đồ gọn.",
    size=11,
)

B = "#2563eb"
OR = "#ea580c"
G = "#059669"
P = "#7c3aed"
Y = "#ca8a04"
K = "#374151"
e = d.edge
e("cus", "lb", "(1) HTTPS", color=Y, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e("lb", "web", "(2a) tải giao diện", color=B, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e(
    "lb",
    "api",
    "(2b) /chat · /confirm",
    color=B,
    pts=[(365, 132), (722, 132)],
    exitX=0.5,
    exitY=0,
    entryX=0.5,
    entryY=0,
)
e("nv", "iap", "console", color=Y, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e(
    "iap",
    "web",
    "đã xác thực",
    color=B,
    pts=[(468, 312), (468, 185)],
    exitX=1,
    exitY=0.5,
    entryX=0,
    entryY=0.8,
)
e("api", "agent", "(3) tin đã che PII", color=K, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e("agent", "mcp", "(4) tool đọc", color=K, pts=[(812, 187)], exitX=0, exitY=0.85, entryX=0.5, entryY=0)
e(
    "mcp",
    "src",
    "(5) đọc / ghi · kết nối riêng",
    color=OR,
    pts=[(460, 322), (460, 655)],
    exitX=0,
    exitY=0.5,
    entryX=1,
    entryY=0.35,
    lpos=-0.4,
)
e(
    "src",
    "mcp",
    "dữ liệu thật",
    color=G,
    pts=[(448, 675), (448, 337)],
    exitX=1,
    exitY=0.8,
    entryX=0,
    entryY=0.85,
    lpos=0.8,
)
e(
    "api",
    "exe",
    "(6) xác nhận hợp lệ",
    color=Y,
    pts=[(760, 187), (760, 255), (1030, 255), (1030, 180)],
    exitX=1,
    exitY=0.85,
    entryX=0,
    entryY=0.7,
)
e(
    "exe",
    "mcp",
    "(7) tool ghi",
    color=OR,
    pts=[(1140, 172), (1140, 322)],
    exitX=1,
    exitY=0.5,
    entryX=1,
    entryY=0.5,
)
e(
    "exe",
    "db",
    "(8) journey · audit",
    color=OR,
    pts=[(1160, 185), (1160, 420), (982, 420)],
    exitX=1,
    exitY=0.8,
    entryX=0.5,
    entryY=0,
)
e(
    "agent",
    "gem",
    "prompt (đã che PII)",
    color=P,
    pts=[(985, 162), (985, 112), (1318, 112)],
    exitX=1,
    exitY=0.3,
    entryX=0.22,
    entryY=0,
)
e(
    "gem",
    "agent",
    "trả lời · tool call",
    color=P,
    pts=[(1345, 128), (1000, 128), (1000, 180)],
    exitX=0.84,
    exitY=0,
    entryX=1,
    entryY=0.68,
)
e(
    "src",
    "ps",
    "(P1) sự kiện",
    color=G,
    pts=[(472, 692), (472, 462), (542, 462)],
    exitX=0.5,
    exitY=1,
    entryX=0.5,
    entryY=0,
)
e("ps", "det", "(P2) đẩy sự kiện", color=G, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e(
    "det",
    "agent",
    "(P3) candidate",
    color=G,
    pts=[(702, 430), (902, 430)],
    exitX=0.5,
    exitY=0,
    entryX=0.5,
    entryY=1,
)
e(
    "ps",
    "gcs",
    "lưu thô (bronze)",
    color=B,
    pts=[(500, 512), (500, 625), (1245, 625), (1245, 522)],
    exitX=0,
    exitY=0.5,
    entryX=0,
    entryY=0.5,
)
e("gcs", "bq", "silver → gold", color=B, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
e("bq", "looker", "metric CX", color=B, exitX=1, exitY=0.5, entryX=0, entryY=0.5)
Path("03-deployment.drawio").write_text(d.xml(), encoding="utf-8")
