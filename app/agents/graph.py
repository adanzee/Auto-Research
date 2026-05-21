
from langgraph.graph import StateGraph, END, START
from state  import AgentState
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
    if state.validate_node == True:
        return synthesize_node
    elif state.validate_node == False and state.retry_count <= 3:
        return search_node
    elif state.validate_node == False and state.retry_count > 3:
        return planner_node
    else:   
        return END
    
workflow.add_node(START, planner_node)
workflow.add_node(planner_node, search_node)
workflow.add_node(search_node, validate_node)
workflow.add_node(validate_node, synthesize_node)
workflow.add_node(synthesize_node, END)
workflow.add_edge(START, planner_node)
workflow.add_edge(planner_node, search_node)
workflow.add_edge(search_node, validate_node)
workflow.add_edge(validate_node, synthesize_node)
workflow.add_conditional_edge(
    validate_node, 
    router_function,{
        True: synthesize_node,
        False: search_node
    }   
)

app = workflow.compile()