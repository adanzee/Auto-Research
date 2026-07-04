from fastapi import FastAPI

from app.api.research import router as research_router

app = FastAPI(title="Auto Research API")
app.include_router(research_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
