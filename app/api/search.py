from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.rag.retriever import search_chunks


router = APIRouter(
    prefix="/search",
    tags=["search"]
)


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=2,
        max_length=500
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=10
    )


@router.post("")
async def search(request: SearchRequest):
    results = search_chunks(
        query=request.query,
        limit=request.limit
    )

    return {
        "query": request.query,
        "count": len(results),
        "results": results
    }