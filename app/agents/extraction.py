from typing import Any

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

import config
from app.agents.state import AgentState


def _format_search_results(search_result: dict[str, Any]) -> str:
    if not search_result:
        return "No search results were provided."

    formatted_sections: list[str] = []
    for subquery, tool_output in search_result.items():
        formatted_sections.append(f"SUBQUERY: {subquery}")

        if isinstance(tool_output, dict):
            items = tool_output.get("results") or tool_output.get("data") or []
        elif isinstance(tool_output, list):
            items = tool_output
        else:
            items = [tool_output]

        if not isinstance(items, list):
            items = [items]

        if not items:
            formatted_sections.append("No supporting evidence found.")
            continue

        for index, item in enumerate(items, start=1):
            if isinstance(item, dict):
                title = item.get("title") or item.get("page_title") or item.get("name") or "Untitled"
                url = item.get("url") or item.get("link") or ""
                snippet = item.get("snippet") or item.get("text") or item.get("content") or ""
                formatted_sections.append(f"{index}. {title}")
                if url:
                    formatted_sections.append(f"URL: {url}")
                if snippet:
                    formatted_sections.append(f"Snippet: {snippet}")
            else:
                formatted_sections.append(f"{index}. {item}")

        formatted_sections.append("")

    return "\n".join(formatted_sections).strip()


def extract_relevant_information(state: AgentState):
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        model="openai/gpt-oss-120b:free",
        api_key=config.gpt_oss_key,
        temperature=0.3,
    )

    prompt = ChatPromptTemplate.from_template("""
        You are an expert evidence extraction agent.

        Your task is to extract the most relevant facts from the provided search results that directly answer the user's query.

        User Query:
        {input_query}

        Search Results:
        {search_results}

        Instructions:
        - Keep only facts that directly support the user's query.
        - Preserve names, dates, numbers, and any important caveats.
        - Do not invent information that is not present in the results.
        - If something is missing, mention it in missing_information.

        Return JSON with this structure:
        {
          "summary": "A concise summary of the most relevant findings",
          "key_facts": ["fact 1", "fact 2"],
          "citations": ["short reference to the most relevant result"],
          "missing_information": ["anything that is still unclear"]
        }
    """)

    parser = JsonOutputParser()
    chain = prompt | llm | parser

    try:
        formatted_results = _format_search_results(state.get("search_result", {}))
        result = chain.invoke(
            {
                "input_query": state["input_query"],
                "search_results": formatted_results,
            }
        )
    except Exception as exc:
        result = {
            "summary": "Extraction could not be completed.",
            "key_facts": [],
            "citations": [],
            "missing_information": [f"Extraction failed: {exc}"],
        }

    return {
        "extracted_info": result,
        "extraction_result": result,
    }


def extract_information(state: AgentState):
    return extract_relevant_information(state)


def perform_extraction(state: AgentState):
    return extract_relevant_information(state)
