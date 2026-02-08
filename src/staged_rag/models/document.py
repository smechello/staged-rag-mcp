from __future__ import annotations

from datetime import datetime, timezone

from typing import Any

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class DocumentChunk(BaseModel):
    chunk_index: int
    text: str
    token_count: int = Field(ge=0)
    start_char: int
    end_char: int

class Document(BaseModel):
    doc_id: str = Field(description="Stable unique identifier such as UUID4")
    title: str
    source: str = Field(description="Origin path, URL, or label")
    full_text: str
    summary: str = Field(description="2-4 sentence summary for Level 1 retrieval")
    chunks: list[DocumentChunk] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    collection: str = Field(default="default")
    token_count: int = Field(description="Token count of full_text")
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)
