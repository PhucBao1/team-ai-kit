<!-- Modified by P-073 team, 2026-10-01: chép phần Python từ langchain-ai/langchain-skills@a76fef33ed (MIT) config/skills/langgraph-persistence/SKILL.md; bỏ TS, Store, create_agent; thêm AsyncPostgresSaver + pool cho FastAPI, ghi chú 1.2.12 — xem NOTICE.md -->
# LangGraph persistence (Python) — tham khảo cho P-073

## Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)
- Luật trong `AGENTS.md`, `src/agents/AGENTS.md`, `../SKILL.md` thắng tài liệu này.
- Prod: `AsyncPostgresSaver` dùng chung pool psycopg (mục cuối). Test: `InMemorySaver()` — không cần Postgres trong `pytest`.
- `thread_id` = id hội thoại do API cấp; không dùng `customer_id` làm `thread_id` (một khách nhiều hội thoại).
- `checkpointer.setup()` tạo bảng — chạy MỘT lần ở bước deploy/migration, không chạy mỗi request, không chạy ở mỗi lần khởi động instance Cloud Run.
- Không dùng Store (bộ nhớ dài hạn xuyên thread) khi chưa có ADR. Dữ liệu khách lấy qua tool / DB, không lưu vào checkpoint ngoài phạm vi hội thoại.
- Đã kiểm với langgraph 1.2.12, langgraph-checkpoint 4.2.0, langgraph-checkpoint-postgres 3.1.2, psycopg 3.3, psycopg-pool 3.3.

<overview>
LangGraph's persistence layer enables durable execution by checkpointing graph state:

- **Checkpointer**: Saves/loads graph state at every super-step
- **Thread ID**: Identifies separate checkpoint sequences (conversations)
</overview>

| Checkpointer | Use Case | Production Ready |
|--------------|----------|------------------|
| `InMemorySaver` (= `MemorySaver`) | Testing, development | No |
| `SqliteSaver` | Local development | Partial |
| `PostgresSaver` / `AsyncPostgresSaver` | Production | Yes |

---

## Checkpointer Setup

Set up a basic graph with in-memory checkpointing and thread-based state persistence.

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]

def add_message(state: State) -> dict:
    return {"messages": ["Bot response"]}

checkpointer = InMemorySaver()

graph = (
    StateGraph(State)
    .add_node("respond", add_message)
    .add_edge(START, "respond")
    .add_edge("respond", END)
    .compile(checkpointer=checkpointer)  # Pass at compile time
)

# ALWAYS provide thread_id
config = {"configurable": {"thread_id": "conversation-1"}}

result1 = graph.invoke({"messages": ["Hello"]}, config)
print(len(result1["messages"]))  # 2

result2 = graph.invoke({"messages": ["How are you?"]}, config)
print(len(result2["messages"]))  # 4 (previous + new)
```

Configure PostgreSQL-backed checkpointing (sync; for FastAPI use the async section at the end).

```python
import os
from langgraph.checkpoint.postgres import PostgresSaver

# Run once during deployment (not at application startup):
#   PostgresSaver.from_conn_string(os.environ["DATABASE_URL"]).setup()

with PostgresSaver.from_conn_string(os.environ["DATABASE_URL"]) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```

---

## Thread Management

```python
# Different threads maintain separate state
alice_config = {"configurable": {"thread_id": "user-alice"}}
bob_config = {"configurable": {"thread_id": "user-bob"}}

graph.invoke({"messages": ["Hi from Alice"]}, alice_config)
graph.invoke({"messages": ["Hi from Bob"]}, bob_config)

# Alice's state is isolated from Bob's
```

---

## State History & Time Travel

Browse checkpoint history and replay or fork from a past state.

```python
config = {"configurable": {"thread_id": "session-1"}}

result = graph.invoke({"messages": ["start"]}, config)

# Browse checkpoint history
states = list(graph.get_state_history(config))

# Replay from a past checkpoint
past = states[-2]
result = graph.invoke(None, past.config)  # None = resume from checkpoint

# Or fork: update state at a past checkpoint, then resume
fork_config = graph.update_state(past.config, {"messages": ["edited"]})
result = graph.invoke(None, fork_config)
```

Manually update graph state before resuming execution.

```python
config = {"configurable": {"thread_id": "session-1"}}

# Modify state before resuming
graph.update_state(config, {"data": "manually_updated"})

# Resume with updated state
result = graph.invoke(None, config)
```

Nhóm P-073: `update_state` / time travel chỉ dùng trong test, debug và console nhân viên có kiểm quyền — KHÔNG dùng để "bỏ qua" bước xác nhận.

---

## Bẫy: `update_state` + reducer

`update_state` đi QUA reducer như một node bình thường (đã chạy thử trên 1.2.12):

```python
from langgraph.types import Overwrite

# State with reducer: items: Annotated[list, operator.add]
# Current state: {"items": ["A", "B"]}

graph.update_state(config, {"items": ["C"]})             # → ["A", "B", "C"]  (nối thêm!)
graph.update_state(config, {"items": Overwrite(["C"])})  # → ["C"]            (thay thế)
```

- Muốn thay hẳn trường có reducer → `Overwrite(...)`. Muốn xoá message → `RemoveMessage` (với `add_messages`).
- Nếu bước cuối có nhiều node chạy song song, `update_state` báo `InvalidUpdateError: Ambiguous update, specify as_node`
  → truyền `as_node="<tên node>"`; `as_node` cũng quyết định cạnh nào chạy tiếp khi `invoke(None, config)`.
- Ghi đè trường đếm vòng lặp (`critic_rounds`…) bằng `update_state` là cách vô tình phá giới hạn vòng lặp — kiểm lại trong test.

---

## Subgraph Checkpointer Scoping

When compiling a subgraph, the `checkpointer` parameter controls persistence behavior. Critical for subgraphs that use interrupts, need multi-turn memory, or run in parallel.

| Feature | `checkpointer=False` | `None` (default) | `True` |
|---|---|---|---|
| Interrupts (HITL) | No | Yes | Yes |
| Multi-turn memory | No | No | Yes |
| Multiple calls (different subgraphs) | Yes | Yes | Warning (namespace conflicts possible) |
| Multiple calls (same subgraph) | Yes | Yes | No |
| State inspection | No | Warning (current invocation only) | Yes |

- **`checkpointer=False`** — Subgraph doesn't need interrupts or persistence. Simplest option, no checkpoint overhead.
- **`None` (default / omit `checkpointer`)** — Subgraph needs `interrupt()` but not multi-turn memory. Each invocation starts fresh but can pause/resume. Parallel execution works because each invocation gets a unique namespace.
- **`checkpointer=True`** — Subgraph needs to remember state across invocations (multi-turn). Each call picks up where the last left off.

**Warning**: Stateful subgraphs (`checkpointer=True`) do NOT support calling the same subgraph instance multiple times within a single node — the calls write to the same checkpoint namespace and conflict.

```python
subgraph = subgraph_builder.compile(checkpointer=False)  # No interrupts needed
subgraph = subgraph_builder.compile()                    # Interrupts, no cross-invocation memory (default)
subgraph = subgraph_builder.compile(checkpointer=True)   # Cross-invocation memory (stateful)
```

Chỉ graph CHA nhận checkpointer thật (`AsyncPostgresSaver`); subgraph không truyền saver riêng, chỉ `None`/`False`/`True`.
Mặc định nhóm cho PolicyQA / Scheduler / Writer⇄Critic / Handoff: `compile()` (None) — trí nhớ hội thoại nằm ở state graph cha.
Subgraph thêm bằng `add_node(name, compiled_subgraph)` tự có namespace theo tên node.

---

## Fixes

```python
# WRONG: No thread_id - state NOT persisted!
graph.invoke({"messages": ["Hello"]})
graph.invoke({"messages": ["What did I say?"]})  # Doesn't remember!

# CORRECT: Always provide thread_id
config = {"configurable": {"thread_id": "session-1"}}
graph.invoke({"messages": ["Hello"]}, config)
graph.invoke({"messages": ["What did I say?"]}, config)  # Remembers!
```

```python
# WRONG: Data lost on process restart
checkpointer = InMemorySaver()  # In-memory only!

# CORRECT: Use persistent storage for production (setup() once, at deploy time — see below)
from langgraph.checkpoint.postgres import PostgresSaver
with PostgresSaver.from_conn_string("postgresql://...") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
```

---

## AsyncPostgresSaver + pool psycopg cho FastAPI (P-073)

Một pool cho cả tiến trình, mở/đóng trong `lifespan`; graph compile một lần với saver dùng pool đó.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from src.agents.graph import build_graph
from src.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Mở pool checkpoint một lần cho cả tiến trình; đóng khi tắt."""
    pool = AsyncConnectionPool(
        conninfo=settings.checkpoint_db_url,  # DSN psycopg thuần "postgresql://…", không phải URL "+asyncpg" của SQLAlchemy
        max_size=10,
        open=False,
        kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row},  # saver cần đủ 3 tham số này
    )
    await pool.open()
    checkpointer = AsyncPostgresSaver(pool)  # phải tạo bên trong event loop đang chạy
    app.state.agent = build_graph().compile(checkpointer=checkpointer)  # chỉnh theo build_graph() thật của repo
    try:
        yield
    finally:
        await pool.close()

app = FastAPI(lifespan=lifespan)
```

Gọi trong route: `await request.app.state.agent.ainvoke(inputs, {"configurable": {"thread_id": conv_id}, "recursion_limit": 25})`.

Tạo bảng — chạy MỘT lần ở bước deploy/migration (vd `python -m src.db.setup_checkpoint` trong Cloud Build trước khi deploy, hoặc cùng bước `alembic upgrade head`):

```python
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def main(dsn: str) -> None:
    """Tạo/nâng cấp bảng checkpoint (idempotent, nhưng không chạy mỗi request)."""
    async with AsyncPostgresSaver.from_conn_string(dsn) as checkpointer:
        await checkpointer.setup()

# asyncio.run(main(dsn))
```

Lưu ý:
- (Đã chạy thử trên 3.1.2) `AsyncPostgresSaver(pool)` gọi `asyncio.get_running_loop()` trong `__init__` → tạo ở module-level sẽ lỗi `RuntimeError: no running event loop`.
- (Theo docs LangGraph + mã nguồn `from_conn_string` dùng đúng 3 tham số đó; chưa chạy với Postgres thật) thiếu `autocommit=True` → `setup()` không lưu bảng;
  thiếu `row_factory=dict_row` → đọc checkpoint lỗi.
- `settings.checkpoint_db_url` và cách `build_graph()` trả builder hay graph đã compile là MINH HOẠ — theo code thật của repo (graph.py do A sở hữu).
- Không dùng `pipeline=True` / `pipe` với pool (chỉ cho một `AsyncConnection` đơn).
- Test không cần Postgres: compile với `InMemorySaver()`; test tích hợp Postgres (nếu có) đánh dấu riêng, không chạy trong CI BTC.

<boundaries>
### What You Should NOT Do

- Use `InMemorySaver` in production — data lost on restart; use `AsyncPostgresSaver`
- Forget `thread_id` — state won't persist without it
- Expect `update_state` to bypass reducers — it passes through them; use `Overwrite` to replace
- Run the same stateful subgraph (`checkpointer=True`) in parallel within one node — namespace conflict
- (P-073) Call `setup()` per request or at every instance start; create a new pool per request
</boundaries>
