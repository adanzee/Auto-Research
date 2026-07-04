from typing import Any, Optional

from fastapi import APIRouter, Body, HTTPException, Query
from pydantic import BaseModel, Field

from app.services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The topic or question to research")


class ResearchResponse(BaseModel):
    status: str
    query: str
    report_text: Optional[str] = None
    final_answer: Optional[str] = None
    validation_status: Optional[bool] = None
    retry_count: int = 0
    subqueries: list[str] = Field(default_factory=list)
    message: list[str] = Field(default_factory=list)


@router.api_route("", methods=["GET", "POST"], response_model=ResearchResponse)
@router.api_route("/", methods=["GET", "POST"], response_model=ResearchResponse)
async def create_research(
    request: Optional[ResearchRequest] = Body(default=None),
    query: Optional[str] = Query(default=None),
) -> ResearchResponse:
    query_text = query or (request.query if request else None)
    if not query_text or not str(query_text).strip():
        raise HTTPException(status_code=422, detail="A non-empty 'query' is required")

    result: dict[str, Any] = ResearchService.run_research(query=str(query_text).strip())

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", ["Research failed"]))

    return ResearchResponse(**result)
