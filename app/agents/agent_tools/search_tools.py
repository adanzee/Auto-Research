from typing import Any, Iterable

from langchain_exa import ExaSearchResults

import config


search_tool = ExaSearchResults(exa_api_key=config.exasearch_api_key, max_results=5)


def run_search(query: str) -> dict[str, Any]:
    """Run a single search query and return the raw result."""
    try:
        result = search_tool.invoke({"query": query})
        return {"query": query, "result": result}
    except Exception as exc:
        return {"query": query, "error": str(exc)}


def run_batch_search(queries: Iterable[str]) -> dict[str, dict[str, Any]]:
    """Run multiple search queries and return a mapping from query to result."""
    return {query: run_search(query) for query in queries}


def normalize_search_result(raw_result: Any) -> list[dict[str, Any]]:
    """Normalize raw search output into a list of structured items."""
    normalized: list[dict[str, Any]] = []

    if raw_result is None:
        return normalized

    if isinstance(raw_result, dict):
        if "results" in raw_result and isinstance(raw_result["results"], list):
            for item in raw_result["results"]:
                normalized.append(_item_to_dict(item))
            return normalized
        if "data" in raw_result and isinstance(raw_result["data"], list):
            for item in raw_result["data"]:
                normalized.append(_item_to_dict(item))
            return normalized

    if isinstance(raw_result, list):
        for item in raw_result:
            normalized.append(_item_to_dict(item))
        return normalized

    normalized.append(_item_to_dict(raw_result))
    return normalized


def _item_to_dict(item: Any) -> dict[str, Any]:
    if item is None:
        return {"text": ""}

    if isinstance(item, dict):
        return item

    return {"text": str(item)}
