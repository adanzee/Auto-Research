
from langgraph.graph import StateGraph, END, START
from state  import AgentState
# this is the wrong logic to build the nodes 

workflow = StateGraph(AgentState)
workflow.add_node(START, "plan")
workflow.add_node("plan", "search")
workflow.add_node("search", "validate")
workflow.add_node("validate", "synthesize")
workflow.add_node("synthesize", END)
workflow.add_edge(START, "plan")
workflow.add_edge("plan", "search")
workflow.add_edge("search", "validate")
def route (AgentState):
    if AgentState.validate >= 0.7:
        return "synthesize"
    else:
        return "search" or "plan"