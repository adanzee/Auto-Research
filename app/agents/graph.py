from langgraph.graph import StateGraph, END, START
from state import AgentState
from validation import validate_search_result
from synthesis import synthesize_results
from planner import create_research_plan
from search import perform_search

# correct way of defining nodes and edges in a state graph

workflow = StateGraph(AgentState)


def planner_node(state: AgentState):
    return create_research_plan(state)
    


def search_node(state: AgentState):
    return perform_search(state)
    




def validate_node(state: AgentState):
    return validate_search_result(state)
    


def synthesize_node(state: AgentState):
    return synthesize_results(state)
    


def router_function(state: AgentState):
    if state["validate_result"]:
        return "synthesize"
    elif not state["validate_result"] and state["retry_count"] <= 3:
        return "search"
    elif not state["validate_result"] and state["retry_count"] > 3:
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

graph = workflow.compile()
