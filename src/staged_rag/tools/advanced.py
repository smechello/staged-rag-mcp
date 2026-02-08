from __future__ import annotations

from staged_rag.service import get_service


def find_similar(doc_id: str, top_k: int = 5, exclude_same_source: bool = False, collection: str = "default") -> dict:
    """Return doc IDs similar to the provided document."""
    service = get_service()
    return service.find_similar(doc_id, collection, top_k, exclude_same_source)


def multi_query_search(
    queries: list[str],
    top_k: int = 5,
    collection: str = "default",
    fusion_method: str = "rrf",
) -> dict:
    """Run multiple queries and fuse ranked results."""
    service = get_service()
    return service.multi_query_search(queries, top_k, collection, fusion_method)


def hybrid_search(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> dict:
    """Blend keyword and semantic search traces for precise recall."""
    service = get_service()
    return service.hybrid_search(query, top_k, collection, semantic_weight, keyword_weight)
