from langchain_exa import ExaSearchResults 
from typing import Any
import config 
from app.agents.state import AgentState


search_tool = ExaSearchResults(exa_api_key=config.exasearch_api_key, max_results=5)

def perform_search(state: AgentState):
    results : dict[str, Any] = {}
    for sub_query in state["subquery"]:
        try:
            output = search_tool.invoke({"query": sub_query})
            results[sub_query] = output
        except Exception as e:
            print(f"Error occurred while performing search for '{sub_query}': {e}")
    return {
        "search_result": results
    }
        
