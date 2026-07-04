from typing import Any


class ResearchService:
    @staticmethod
    def run_research(query: str, max_retries: int = 1) -> dict[str, Any]:
        from app.agents.planner import create_research_plan
        from app.agents.report import create_report
        from app.agents.search import perform_search
        from app.agents.synthesis import synthesize_results
        from app.agents.validation import validate_search_result

        state: dict[str, Any] = {
            "input_query": query,
            "subquery": [],
            "search_result": {},
            "validate_result": False,
            "retry_count": 0,
            "final_answer": "",
            "message": [],
        }

        try:
            for _ in range(max(1, max_retries)):
                state.update(create_research_plan(state))
                state.update(perform_search(state))
                state.update(validate_search_result(state))

                if state.get("validate_result", False):
                    break

            state.update(synthesize_results(state))
            state.update(create_report(state))

            return {
                "status": "completed",
                "query": query,
                "report_text": state.get("report_text", ""),
                "final_answer": state.get("final_answer", ""),
                "validation_status": state.get("validate_result", False),
                "retry_count": state.get("retry_count", 0),
                "subqueries": state.get("subquery", []),
                "message": state.get("message", []),
            }
        except Exception as exc:  # pragma: no cover - defensive path for runtime failures
            return {
                "status": "error",
                "query": query,
                "report_text": None,
                "final_answer": "",
                "validation_status": False,
                "retry_count": state.get("retry_count", 0),
                "subqueries": state.get("subquery", []),
                "message": [str(exc)],
            }
