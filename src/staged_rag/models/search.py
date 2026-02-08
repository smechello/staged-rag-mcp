from __future__ import annotations

from pydantic import BaseModel, Field

class SummaryResult(BaseModel):
    doc_id: str
    title: str
    summary: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    token_count: int
    tags: list[str] = Field(default_factory=list)
    collection: str

class SearchResponse(BaseModel):
    query: str
    results: list[SummaryResult]
    total_candidates: int = Field(default=0)
    search_time_ms: float = Field(default=0.0)
