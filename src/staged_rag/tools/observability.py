from __future__ import annotations

from staged_rag.service import get_service


def retrieval_log(last_n: int = 10, tool_filter: str | None = None, session_id: str | None = None) -> dict:
    """Return recent audit log entries."""
    service = get_service()
    return service.retrieval_log(last_n, tool_filter, session_id)


def collection_stats(collection: str = "default") -> dict:
    """Return stats for a collection."""
    service = get_service()
    return service.collection_stats(collection)


def list_collections() -> dict:
    """Enumerate available collections."""
    service = get_service()
    return service.list_collections()


def explain_retrieval(query: str, doc_ids: list[str], collection: str = "default") -> dict:
    """Explain why documents ranked for a query."""
    service = get_service()
    return service.explain_retrieval(query, doc_ids, collection)
