from typing import Any

from app.agents.state import AgentState


def _normalize_messages(message_value: Any) -> list[str]:
    if not message_value:
        return []

    if isinstance(message_value, str):
        return [message_value]

    if isinstance(message_value, list):
        normalized: list[str] = []
        for item in message_value:
            if isinstance(item, dict):
                content = item.get("content") or item.get("message") or item.get("text")
                normalized.append(str(content)) if content is not None else None
            else:
                normalized.append(str(item))
        return [value for value in normalized if value]

    return [str(message_value)]


def handle_hitl(state: AgentState):
    """Create or update a human-in-the-loop interaction for the current research task."""
    history = _normalize_messages(state.get("message", []))
    query = state.get("input_query", "")

    if history:
        last_message = history[-1]
        return {
            "message": history + [
                "Thanks for the feedback. I will use it to refine the research request."
            ],
            "needs_human_input": False,
            "hitl_status": "feedback_received",
            "last_human_message": last_message,
        }

    clarification_prompt = (
        f"The current research request is: {query}\n"
        "Please provide any clarification, constraints, or preferred focus areas so I can refine the search."
    )

    return {
        "message": history + [clarification_prompt],
        "needs_human_input": True,
        "hitl_status": "awaiting_input",
        "clarification_prompt": clarification_prompt,
    }


def process_hitl(state: AgentState):
    return handle_hitl(state)
