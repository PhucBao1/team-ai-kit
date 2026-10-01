---
name: langgraph-human-in-the-loop
description: Mẫu human-in-the-loop của LangGraph (interrupt, Command(resume), nhiều interrupt, subgraph). Dùng khi viết/sửa bước Xác nhận trước khi ghi (node confirm_and_execute) hoặc bất kỳ chỗ nào dùng interrupt(); không dùng cho xử lý lỗi chung (debug-failure).
---

## Luật nhóm P-073 (ưu tiên hơn nội dung bên dưới)

Bản chép từ langchain-ai/langchain-skills (MIT, xem `NOTICE.md`). Luật nhóm (`AGENTS.md`, `src/agents/AGENTS.md`, skill `add-langgraph-node`) luôn thắng phần tiếng Anh bên dưới.
Đã kiểm với bản cài: langgraph 1.2.12, langgraph-checkpoint 4.2, langgraph-checkpoint-postgres 3.1.2.

a. **Node chứa `interrupt()` CHẠY LẠI TỪ ĐẦU khi resume** (trong subgraph: node cha gọi subgraph cũng chạy lại).
   Mọi thứ trước `interrupt()` phải tất định / idempotent: không gọi LLM, không ghi DB, không sinh id ngẫu nhiên, không `datetime.now()`.
   **Confirmation token (HMAC + nonce)** phải hoặc sinh tất định từ `(thread_id, hash(proposal))`, hoặc tạo ở node TRƯỚC (vd `prepare_confirmation`)
   và lưu vào state — nếu sinh ngẫu nhiên trong node có `interrupt()`, token lúc resume sẽ KHÁC token khách đã bấm → executor từ chối.
b. **Executor chỉ được gọi SAU resume, ở node riêng**, qua `src.executor.run` (không bao giờ gọi `src.tools` từ `src/agents/`).
   Node hỏi xác nhận chỉ `interrupt()` + trả quyết định; node thực thi đọc quyết định từ state rồi gọi executor.
c. **Payload `interrupt()` JSON-serializable** (dict thuần, không Pydantic object / datetime): gồm `summary_vi` (câu tiếng Việt cho khách)
   + `params` (đủ tham số hành động: xưởng, giờ, mã dịch vụ…) + `confirmation_token` để UI hiện đủ và gửi lại đúng token.
d. **Resume chỉ bằng `Command(resume={...})` có token** (vd `{"decision": "confirm"|"cancel", "confirmation_token": "..."}`).
   Không resume bằng dict state thường; không truyền `Command(update=...)` làm input.
e. **Cần checkpointer + `thread_id`** ở mọi lần gọi. Prod: `AsyncPostgresSaver` (xem `add-langgraph-node/references/langgraph-persistence.md`).
   Test: `InMemorySaver()` (`MemorySaver` là cùng một lớp) + fixture `mock_llm`, kiểm `result["__interrupt__"]` rồi resume.

```python
# Mẫu tối thiểu theo luật nhóm (tên hàm minh hoạ — giữ đúng contracts/ và src/executor/ thật)
async def prepare_confirmation(state: AgentState, config: RunnableConfig) -> dict:
    """Node TRƯỚC: tạo token một lần, lưu vào state (hoặc tính tất định từ thread_id + hash proposal)."""
    thread_id = config["configurable"]["thread_id"]
    return {"confirmation": make_confirmation(state["proposal"], thread_id=thread_id)}

async def ask_confirmation(state: AgentState) -> dict:
    """Không có gì ngoài interrupt(): chạy lại khi resume cũng vô hại."""
    conf = state["confirmation"]
    decision = interrupt({"summary_vi": conf["summary_vi"], "params": conf["params"],
                          "confirmation_token": conf["token"]})
    return {"user_decision": decision}

async def execute_confirmed(state: AgentState) -> dict:
    """Node riêng SAU resume: chỉ ở đây mới gọi executor (validator + idempotency key)."""
    if state["user_decision"].get("decision") != "confirm":
        return {"execution_result": None}
    return {"execution_result": await executor.run(state["proposal"], state["user_decision"])}
```

Ghi chú phiên bản (đã chạy thử trên 1.2.12):
- `graph.invoke(...)` khi dừng trả dict có khoá `"__interrupt__"` = list `Interrupt(value=..., id=..., response_schema=None)`;
  `Interrupt.id` dùng để resume nhiều interrupt. Cũng đọc được qua `graph.get_state(config).interrupts`.
- `interrupt(value, response_schema=...)` là tham số MỚI ở 1.2 (không có trong bản gốc của tài liệu này) — nhóm chưa dùng, chưa kiểm hành vi.
- Code async: dùng `await graph.ainvoke(...)`; ví dụ dưới viết sync cho gọn.

---

<overview>
LangGraph's human-in-the-loop patterns let you pause graph execution, surface data to users, and resume with their input:

- **`interrupt(value)`** — pauses execution, surfaces a value to the caller
- **`Command(resume=value)`** — resumes execution, providing the value back to `interrupt()`
- **Checkpointer** — required to save state while paused
- **Thread ID** — required to identify which paused execution to resume
</overview>

---

## Requirements

Three things are required for interrupts to work:

1. **Checkpointer** — compile with `checkpointer=InMemorySaver()` (dev) or `PostgresSaver` / `AsyncPostgresSaver` (prod)
2. **Thread ID** — pass `{"configurable": {"thread_id": "..."}}` to every `invoke`/`stream` call
3. **JSON-serializable payload** — the value passed to `interrupt()` must be JSON-serializable

---

## Basic Interrupt + Resume

`interrupt(value)` pauses the graph. The value surfaces in the result under `__interrupt__`. `Command(resume=value)` resumes — the resume value becomes the return value of `interrupt()`.

**Critical**: when the graph resumes, the node restarts from the **beginning** — all code before `interrupt()` re-runs.

```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class State(TypedDict):
    approved: bool

def approval_node(state: State):
    # Pause and ask for approval
    approved = interrupt("Do you approve this action?")
    # When resumed, Command(resume=...) returns that value here
    return {"approved": approved}

checkpointer = InMemorySaver()
graph = (
    StateGraph(State)
    .add_node("approval", approval_node)
    .add_edge(START, "approval")
    .add_edge("approval", END)
    .compile(checkpointer=checkpointer)
)

config = {"configurable": {"thread_id": "thread-1"}}

# Initial run — hits interrupt and pauses
result = graph.invoke({"approved": False}, config)
print(result["__interrupt__"])
# [Interrupt(value='Do you approve this action?', id='...', response_schema=None)]

# Resume with the human's response
result = graph.invoke(Command(resume=True), config)
print(result["approved"])  # True
```

---

## Approval Workflow

A common pattern: interrupt to show a draft, then route based on the human's decision.

```python
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from typing import Literal
from typing_extensions import TypedDict

class EmailAgentState(TypedDict):
    email_content: str
    draft_response: str
    classification: dict

def human_review(state: EmailAgentState) -> Command[Literal["send_reply", "__end__"]]:
    """Pause for human review using interrupt and route based on decision."""
    classification = state.get("classification", {})

    # interrupt() must come first — any code before it will re-run on resume
    human_decision = interrupt({
        "email_id": state.get("email_content", ""),
        "draft_response": state.get("draft_response", ""),
        "urgency": classification.get("urgency"),
        "action": "Please review and approve/edit this response"
    })

    # Process the human's decision
    if human_decision.get("approved"):
        return Command(
            update={"draft_response": human_decision.get("edited_response", state.get("draft_response", ""))},
            goto="send_reply"
        )
    else:
        # Rejection — human will handle directly
        return Command(update={}, goto=END)
```

Nhóm P-073: node đi tiếp sau xác nhận là node thực thi riêng (luật b). Nếu dùng `Command(goto=...)` thì KHÔNG thêm `add_edge` tĩnh
từ cùng node — cả hai nhánh sẽ chạy.

---

## Validation Loop

Use `interrupt()` in a loop to validate human input and re-prompt if invalid.

```python
from langgraph.types import interrupt

def get_age_node(state):
    prompt = "What is your age?"

    while True:
        answer = interrupt(prompt)

        # Validate the input
        if isinstance(answer, int) and answer > 0:
            break
        else:
            # Invalid input — ask again with a more specific prompt
            prompt = f"'{answer}' is not a valid age. Please enter a positive number."

    return {"age": answer}
```

Each `Command(resume=...)` call provides the next answer. If invalid, the loop re-interrupts with a clearer message.

```python
config = {"configurable": {"thread_id": "form-1"}}
first = graph.invoke({"age": None}, config)
# __interrupt__: "What is your age?"

retry = graph.invoke(Command(resume="thirty"), config)
# __interrupt__: "'thirty' is not a valid age..."

final = graph.invoke(Command(resume=30), config)
print(final["age"])  # 30
```

Nhóm P-073: vòng hỏi lại phải có giới hạn (luật "mọi vòng lặp có max") — quá N lần → handoff.

---

## Multiple Interrupts

When parallel branches each call `interrupt()`, resume all of them in a single invocation by mapping each interrupt ID to its resume value.

```python
from typing import Annotated, TypedDict
import operator
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt

class State(TypedDict):
    vals: Annotated[list[str], operator.add]

def node_a(state):
    answer = interrupt("question_a")
    return {"vals": [f"a:{answer}"]}

def node_b(state):
    answer = interrupt("question_b")
    return {"vals": [f"b:{answer}"]}

graph = (
    StateGraph(State)
    .add_node("a", node_a)
    .add_node("b", node_b)
    .add_edge(START, "a")
    .add_edge(START, "b")
    .add_edge("a", END)
    .add_edge("b", END)
    .compile(checkpointer=InMemorySaver())
)

config = {"configurable": {"thread_id": "1"}}

# Both parallel nodes hit interrupt() and pause
result = graph.invoke({"vals": []}, config)
# result["__interrupt__"] contains both Interrupt objects with IDs

# Resume all pending interrupts at once using a map of id -> value
resume_map = {
    i.id: f"answer for {i.value}"
    for i in result["__interrupt__"]
}
result = graph.invoke(Command(resume=resume_map), config)
# result["vals"] = ["a:answer for question_a", "b:answer for question_b"]
```

User-fixable errors (missing info) use `interrupt()` to pause and collect missing data — that's the pattern covered by this skill.
For transient errors (`RetryPolicy`) and tool errors, see `add-langgraph-node/references/langgraph-fundamentals-python.md`.

---

## Side Effects Before Interrupt Must Be Idempotent

When the graph resumes, the node restarts from the **beginning** — ALL code before `interrupt()` re-runs. In subgraphs, BOTH the parent node and the subgraph node re-execute.

<idempotency-rules>

**Do:**
- Use **upsert** (not insert) operations before `interrupt()`
- Use **check-before-create** patterns
- Place side effects **after** `interrupt()` when possible
- Separate side effects into their own nodes

**Don't:**
- Create new records before `interrupt()` — duplicates on each resume
- Append to lists before `interrupt()` — duplicate entries on each resume

</idempotency-rules>

Nhóm P-073: node trong `src/agents/` KHÔNG ghi DB trực tiếp — các ví dụ `db.*` dưới đây chỉ minh hoạ nguyên lý; ghi luôn đi qua executor (luật b).

```python
# GOOD: Upsert is idempotent — safe before interrupt
def node_a(state: State):
    db.upsert_user(user_id=state["user_id"], status="pending_approval")
    approved = interrupt("Approve this change?")
    return {"approved": approved}

# GOOD: Side effect AFTER interrupt — only runs once
def node_a(state: State):
    approved = interrupt("Approve this change?")
    if approved:
        db.create_audit_log(user_id=state["user_id"], action="approved")
    return {"approved": approved}

# BAD: Insert creates duplicates on each resume!
def node_a(state: State):
    audit_id = db.create_audit_log({  # Runs again on resume!
        "user_id": state["user_id"],
        "action": "pending_approval",
    })
    approved = interrupt("Approve this change?")
    return {"approved": approved}
```

<subgraph-interrupt-re-execution>

### Subgraph re-execution on resume

When a subgraph contains an `interrupt()`, resuming re-executes BOTH the parent node (that invoked the subgraph) AND the subgraph node (that called `interrupt()`):

```python
def node_in_parent_graph(state: State):
    some_code()  # <-- Re-executes on resume
    subgraph_result = subgraph.invoke(some_input)
    # ...

def node_in_subgraph(state: State):
    some_other_code()  # <-- Also re-executes on resume
    result = interrupt("What's your name?")
    # ...
```

(Kiểm trên 1.2.12: subgraph gọi từ trong hàm node → cả node cha và node con chạy lại; subgraph thêm trực tiếp bằng
`add_node("x", compiled_subgraph)` → chỉ node con chạy lại. Subgraph có interrupt: compile với `checkpointer=None` (mặc định) hoặc `True`,
KHÔNG dùng `False` — xem bảng ở `add-langgraph-node/references/langgraph-persistence.md`.)

</subgraph-interrupt-re-execution>

---

## Command(resume) Warning

`Command(resume=...)` is the **only** Command pattern intended as input to `invoke()`/`stream()`. Do NOT pass `Command(update=...)` as input — it resumes from the latest checkpoint and the graph appears stuck (no node runs). See `add-langgraph-node/references/langgraph-fundamentals-python.md`.

---

## Fixes

Checkpointer required for interrupt functionality.

```python
# WRONG
graph = builder.compile()

# CORRECT
graph = builder.compile(checkpointer=InMemorySaver())
```

Use Command to resume from an interrupt (regular dict restarts graph).

```python
# WRONG
graph.invoke({"resume_data": "approve"}, config)

# CORRECT
graph.invoke(Command(resume="approve"), config)
```

<boundaries>
### What You Should NOT Do

- Use interrupts without a checkpointer — will fail
- Resume without the same thread_id — creates a new thread instead of resuming
- Pass `Command(update=...)` as invoke input — graph appears stuck (use plain dict)
- Perform non-idempotent side effects before `interrupt()` — creates duplicates on resume
- Assume code before `interrupt()` only runs once — it re-runs every resume
- (P-073) Generate a random confirmation token / nonce in the same node as `interrupt()` — it changes on resume
- (P-073) Call the executor in the node that calls `interrupt()` — use a separate node after resume
</boundaries>
