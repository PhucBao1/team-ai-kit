"""src/agents/nodes/critic.py — mẫu node Critic (vòng Writer ⇄ Critic). Kiểm tra theo docs LangGraph hiện hành."""

from pathlib import Path

from src.core.claim_check import claim_check
from src.models.schemas import CriticVerdict
from src.services.llm import get_llm  # get_llm("lite" | "chat" | "reason")

MAX_CRITIC_ROUNDS = 2
CRITIC_PROMPT = Path("src/agents/prompts/critic_vi.md").read_text(encoding="utf-8")  # đọc 1 lần lúc import


async def critic_node(state: dict) -> dict:
    draft = state["draft_message"]
    issues = claim_check(draft, evidence=state["evidence"])  # tất định trước
    if not issues:
        verdict = (
            await get_llm("lite")
            .with_structured_output(CriticVerdict)
            .ainvoke([("system", CRITIC_PROMPT), ("user", draft)])
        )
        issues = verdict.issues
    return {"critic_issues": issues, "critic_rounds": state.get("critic_rounds", 0) + 1}


def after_critic(state: dict) -> str:
    if not state["critic_issues"]:
        return "arbitration"
    if state["critic_rounds"] >= MAX_CRITIC_ROUNDS:
        return "handoff"  # không tự sửa mãi — chuyển người
    return "writer"


# graph.add_node("critic", critic_node)
# graph.add_conditional_edges(
#     "critic", after_critic, {"writer": "writer", "arbitration": "arbitration", "handoff": "handoff"}
# )
