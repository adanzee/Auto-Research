from langgraph.graph import StateGraph, END, START
from state import AgentState
# correct way of defining nodes and edges in a state graph

workflow = StateGraph(AgentState)


def planner_node(state: AgentState):
    pass


def search_node(state: AgentState):
    pass


def validate_node(state: AgentState):
    pass


def synthesize_node(state: AgentState):
    pass


def router_function(state: AgentState):
    if state["validate_result"]:
        return "synthesize"
    elif state["validate_result"] and state["retry_count"] <= 3:
        return "search"
    elif state["validate_result"] and state["retry_count"] > 3:
        return "planner"
    else:
        return END


workflow.add_node("planner", planner_node)
workflow.add_node("search", search_node)
workflow.add_node("validate", validate_node)
workflow.add_node("synthesize", synthesize_node)

workflow.add_edge(START, "planner")
workflow.add_edge("planner", "search")
workflow.add_edge("search", "validate")
workflow.add_conditional_edges(
    "validate",
    router_function,
    {"planner": "planner", "synthesize": "synthesize", "search": "search"},
)

app = workflow.compile()
