# src/agents/ — LangGraph (owner: A) · spec `../team-ai-kit/docs/spec/13-agent.md`, `14-multiagent.md`, `15-router.md`

- Graph: `graph.py` (giữ tên biến `agent` và hàm `build_graph()` của template — route + test đang dùng). Node trong `nodes/`, sub-agent trong `subgraphs/`.
- State: `state.py` (TypedDict của template, thêm trường có kiểu). Không nhét dữ liệu tuỳ tiện vào `messages`.
- `tools/` = tool ĐỌC (`@tool`, level 0 trong `contracts/tools.yaml`). **Không import `src.tools`**; ghi → trả `proposal`, node `confirm_and_execute` gọi `src.executor`.
- Output LLM parse bằng schema Pydantic (`src/models/schemas.py`); lỗi parse → retry ≤ 2 → handoff.
- Vòng lặp có bộ đếm trong state + giới hạn (Critic ≤ 2, tool call ≤ 8/lượt). LLM qua `get_llm("chat"|"reason"|"lite")`.
- Prompt ở `prompts/*.md`, dòng đầu `<!-- v<số> · <ngày> -->`. Đổi prompt → chạy kịch bản eval liên quan.
- Test trong `tests/test_agents/` dùng LLM giả (fixture `mock_llm`) — không gọi model thật.
