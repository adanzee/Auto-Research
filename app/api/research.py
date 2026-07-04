from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["research"])


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The topic or question to research")


class ResearchResponse(BaseModel):
    status: str
    query: str
    report_text: str | None = None
    final_answer: str | None = None
    validation_status: bool | None = None
    retry_count: int = 0
    subqueries: list[str] = []
    message: list[str] = []


@router.post("", response_model=ResearchResponse)
@router.post("/", response_model=ResearchResponse)
async def create_research(request: ResearchRequest) -> ResearchResponse:
    result: dict[str, Any] = ResearchService.run_research(query=request.query)

    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", ["Research failed"]))

    return ResearchResponse(**result)
