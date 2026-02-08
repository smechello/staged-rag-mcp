from __future__ import annotations

from staged_rag.service import get_service


def search_summaries(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    min_score: float = 0.0,
    tags_filter: list[str] | None = None,
) -> dict:
    """Return ranked summaries and doc IDs for Level 1 retrieval."""
    service = get_service()
    return service.search_summaries(query, top_k, collection, min_score, tags_filter)


def get_documents(doc_ids: list[str], include_chunks: bool = False, collection: str = "default") -> dict:
    """Return staged document payloads for Level 2 retrieval."""
    service = get_service()
    return service.get_documents(doc_ids, collection, include_chunks)


def get_document_chunk(
    doc_id: str,
    chunk_index: int | None = None,
    chunk_query: str | None = None,
    collection: str = "default",
) -> dict:
    """Return a specific chunk when Level 2.5 retrieval is requested."""
    service = get_service()
    return service.get_document_chunk(doc_id, collection, chunk_index, chunk_query)
