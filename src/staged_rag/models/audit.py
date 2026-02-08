from __future__ import annotations

from datetime import datetime

from typing import Any

from pydantic import BaseModel, Field

class AuditLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_name: str
    parameters: dict[str, Any]
    result_count: int
    doc_ids_returned: list[str] = Field(default_factory=list)
    latency_ms: float = Field(default=0.0)
    collection: str | None = None
    session_id: str | None = None
