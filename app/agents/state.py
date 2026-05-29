from typing import TypedDict, Annotated, Any
import operator


# AgentState is just a name, you can name anything you want it just a standard convention, its like giving a name
class AgentState(TypedDict):
    input_query: str
    subquery: list[str]
    search_result: dict[str, Any]
    validate_result: bool
    retry_count: int
    final_answer: str
    message: Annotated[list, operator.add]  # for llm history
