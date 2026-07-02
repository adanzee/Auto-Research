from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import config
from app.agents.state import AgentState


def _serialize_search_results(search_result: dict[str, Any]) -> str:
    if not search_result:
        return "No search results were captured."

    lines: list[str] = []
    for subquery, tool_output in search_result.items():
        lines.append(f"SUBQUERY: {subquery}")

        if isinstance(tool_output, dict):
            if "results" in tool_output and isinstance(tool_output["results"], list):
                for item in tool_output["results"]:
                    lines.append(f"- {item}")
            else:
                lines.append(f"- {tool_output}")
        elif isinstance(tool_output, list):
            for item in tool_output:
                lines.append(f"- {item}")
        else:
            lines.append(f"- {tool_output}")

        lines.append("")

    return "\n".join(lines).strip()


def generate_report(state: AgentState):
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        model="openai/gpt-oss-120b:free",
        api_key=config.gpt_oss_key,
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_template("""
        You are an expert research report writer.

        Create a concise and polished research report that summarizes the entire investigation.

        Include the following sections:
        - Research question
        - Validation status
        - Search summary
        - Final consolidated answer
        - Key insights
        - Outstanding gaps or open questions

        Use the inputs faithfully and do not introduce information that is not present.

        Research question:
        {input_query}

        Validation status:
        {validate_result}

        Final answer:
        {final_answer}

        Search results:
        {search_results}
    """)

    parser = StrOutputParser()
    chain = prompt | llm | parser
    formatted_search_results = _serialize_search_results(state.get("search_result", {}))

    result = chain.invoke(
        {
            "input_query": state.get("input_query", ""),
            "validate_result": state.get("validate_result", False),
            "final_answer": state.get("final_answer", ""),
            "search_results": formatted_search_results,
        }
    )

    return {
        "report_text": result,
        "report_status": "generated",
    }


def create_report(state: AgentState):
    return generate_report(state)
