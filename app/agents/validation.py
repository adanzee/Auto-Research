# this node is used to validate whether the result of the search node
# is according to the input query or not  
from app.agents.state import AgentState
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import config
from langchain_core.output_parsers import JsonOutputParser

def validate_search_result(state:AgentState):
    llm = ChatOpenAI(
        openai_api_base = "https://openrouter.ai/api/v1",
        model = "openai/gpt-oss-120b:free",
        api_key = config.gpt_oss_key,
        temperature = 0.4,

    )

    prompt = ChatPromptTemplate.from_template("""
                You are an expert relevance evaluator.

                Your task is to determine whether the provided search_result adequately answers the input_query.

                Instructions:
                Read the input_query carefully and identify the user's actual information need.
                Examine the search_result and determine whether it directly, accurately, and sufficiently addresses that need.
                Consider:
                    Relevance: Does the result discuss the same topic as the query?
                    Completeness: Does it provide enough information to answer the query?
                    Correctness: Is the information consistent with the query and free of obvious contradictions?
                    Specificity: Does it answer the question asked, rather than providing only loosely related information?
                A result should be marked as adequate only if a reasonable user would consider their query answered after reading it.
                If the result is partially relevant but misses key information required to answer the query, mark it as inadequate.

                Return your evaluation in the following JSON format:

                {
                "adequate": false,
                "score": 45,
                "reason": "The result discusses test coverage in general but does not explain ExCoveralls.",
                "missing_information": [
                    "Purpose of ExCoveralls",
                    "How it integrates with Elixir projects",
                    "Coverage reporting workflow"
                ]
                }
                

                Scoring Guidelines:
                     90-100: Fully answers the query with relevant and sufficient information.
                     70-89: Mostly answers the query, minor details missing.
                     40-69: Partially relevant but important information is missing.
                     10-39: Weak relevance, does not answer the query.
                     0-9: Completely irrelevant or contradictory.

                Input Query:
                {input_query}

                Search Result:
                {search_result}

  """, template_format="jinja2")
    
    output_parser = JsonOutputParser()
    chain_prompt = prompt | llm | output_parser
    result = chain_prompt.invoke({"input_query": state["input_query"],
                                   "search_result": state["search_result"]})
    has_passed = result.get("adequate", False)
    current_retries = state["retry_count"]
    new_retry_count = current_retries + 1

    return {"validate_result": has_passed,
              "retry_count" : new_retry_count }
