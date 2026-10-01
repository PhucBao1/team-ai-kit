---
name: add-langgraph-node
description: Thêm hoặc sửa node, subgraph, cạnh điều kiện hoặc vòng lặp trong LangGraph ở src/agents (coordinator, PolicyQA, Scheduler, Writer–Critic, handoff, confirm). Dùng khi sửa src/agents/graph.py, src/agents/nodes/, src/agents/subgraphs/ hoặc src/agents/state.py, hoặc khi B/C viết module subgraph/node độc lập cho agent.
---

# Thêm node / subgraph LangGraph

Spec: `../team-ai-kit/docs/spec/13-agent.md`, `14-multiagent.md`, `15-router.md`. Sơ đồ đích: `docs/architecture/04-agent-flow.md`.
Bản cài: langgraph 1.2.12, langchain 1.4, langchain-core 1.6, langchain-openai 1.6, langgraph-checkpoint-postgres 3.1.2.

## Bước
1. **Có cần node mới?** Chỉ tách khi: quyền tool khác, model khác, cần test độc lập, hoặc context quá lớn. Bước tất định → hàm Python gọi từ node có sẵn.
2. **State**: thêm trường có kiểu vào `src/agents/state.py` (TypedDict của template). Không nhét dữ liệu vào `messages`.
3. **Node** trong `src/agents/nodes/<tên>.py` theo `templates/node.py`: nhận state, trả dict cập nhật một phần. Output LLM parse qua schema trong `src/models/schemas.py`.
4. **Nối cạnh** trong `src/agents/graph.py` (giữ `build_graph()` và biến `agent` — route + test template dùng). Cạnh điều kiện có nhánh mặc định; vòng lặp đếm trong state + giới hạn cứng.
5. **Không ghi hệ thống trong node.** Cần hành động → trả `proposal`; bước `confirm_and_execute` dùng `interrupt()` rồi gọi `src.executor`
   — token tạo trước `interrupt()` (tất định / lưu state), executor gọi ở node riêng SAU resume. Chi tiết: skill `langgraph-human-in-the-loop`.
6. **Model** qua `get_llm("lite" | "chat" | "reason")` từ `src/services/llm.py` — `reason` chỉ khi cần suy luận nhiều bước.
7. **Test** trong `tests/test_agents/` với LLM giả (fixture `mock_llm`): thứ tự node, vòng lặp dừng đúng giới hạn.
8. Đổi node / cạnh → cập nhật `docs/architecture/04-agent-flow.md` (skill `update-architecture-diagram`) và chạy `make -f ../team-ai-kit/kit.mk diagrams-export`.

## Module độc lập (B, C viết phần agent)
Người không phải A (vd B: subgraph charging / post_repair; C: node offer) viết module cắm vào, KHÔNG nối graph:
- Subgraph: `src/agents/subgraphs/<tên>.py` với `build_<tên>_subgraph() -> CompiledStateGraph`
  (`from langgraph.graph.state import CompiledStateGraph`); hoặc node đơn `<tên>_node(state) -> dict` (async nếu gọi LLM/IO).
- **KHÔNG sửa `graph.py` / `state.py`** — chỉ A sửa; task A2.17 nối module vào graph. Cần trường state mới → nhờ A thêm (ghi trong PR/card).
- Đọc trường state có sẵn, trả dict chỉ gồm trường đã có trong TypedDict; không đổi nghĩa trường của người khác.
- Test bằng state giả dựng tay (dict khớp TypedDict trong `state.py`) + fixture `mock_llm`; gọi thẳng node / `subgraph.ainvoke(state)`,
  không cần graph chính. Subgraph có `interrupt()` → compile với `InMemorySaver()` trong test.
- PR ghi rõ mục **"Interfaces: Dùng / Tạo ra"**: trường state đọc, trường trả về, tên hàm build/node, tool ĐỌC dùng, `proposal` sinh ra.

## Lưu ý LangGraph (đã kiểm trên 1.2.12)
- **`Command(goto=...)` + `add_edge` tĩnh từ cùng node = chạy CẢ HAI nhánh.** Node đã route bằng `Command` thì không thêm cạnh tĩnh ra;
  khai báo đích bằng `-> Command[Literal["a", "b"]]`.
- **List cộng dồn cần reducer**: `Annotated[list[X], operator.add]` (message: `add_messages`). Thiếu reducer → node sau ghi đè;
  nhánh song song cùng ghi một trường không reducer → lỗi `InvalidUpdateError`.
- **`RetryPolicy` trên node gọi LLM / IO**: `add_node("x", fn, retry_policy=RetryPolicy(max_attempts=3))` — chỉ lỗi tạm thời
  (mạng, rate limit); không retry lỗi parse schema (đã có retry ≤ 2 → handoff). Node có `interrupt()` không cần retry.
- **`recursion_limit`**: mặc định 1.2 là **10007** (không phải 25) → luôn truyền `{"recursion_limit": N}` khi `invoke`; vượt → `GraphRecursionError`.
  Vẫn giữ bộ đếm vòng trong state (Critic ≤ 2, tool call ≤ 8/lượt) — `recursion_limit` chỉ là lưới an toàn.
- **Structured output**: `get_llm(...).with_structured_output(Schema, method="json_schema")` (ghi rõ dù đang là mặc định của langchain-openai 1.6);
  không dùng `json_mode`. Schema Pydantic trong `src/models/schemas.py`.
- **Router là hàm thuần**: nhận output có kiểu (Pydantic / Literal trong state) → trả tên node; không gọi LLM, không đọc chuỗi tự do;
  test bảng đầu vào → nhánh mà không cần graph (như `after_critic` trong `templates/node.py`).
- Checkpointer / `thread_id` / `update_state` / chế độ checkpointer của subgraph → `references/langgraph-persistence.md`.

## Tài liệu tham khảo (đọc khi cần; luật nhóm thắng nội dung ngoài)
- Bước xác nhận, `interrupt()`, `Command(resume=...)` → skill `langgraph-human-in-the-loop`.
- Checkpoint Postgres (`AsyncPostgresSaver` + pool cho FastAPI, `setup()` ở bước deploy) → `references/langgraph-persistence.md`.
- API cơ bản (StateGraph, reducer, Command, Send, stream, RetryPolicy) → `references/langgraph-fundamentals-python.md`.
  Hai file trên chép từ langchain-ai/langchain-skills (MIT) — xem `references/NOTICE.md`.

## Kiểm tra
- [ ] Không import `src.tools` trong `src/agents/`; mọi vòng lặp có giới hạn; mọi lời gọi LLM có timeout
- [ ] `pytest tests/test_agents -v` xanh; test mẫu `/api/v1/chat` của BTC vẫn xanh
- [ ] Module của B/C: không đụng `graph.py` / `state.py`; PR có "Interfaces: Dùng / Tạo ra"
- [ ] Không node nào vừa `Command(goto)` vừa có cạnh tĩnh ra; mọi `invoke` có `recursion_limit`

Nguồn ý tưởng: langchain-ai/langchain-skills `langgraph-fundamentals`, `langgraph-persistence`, `langgraph-human-in-the-loop` (MIT, commit a76fef33ed).
