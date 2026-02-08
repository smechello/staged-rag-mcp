"""Re-export staged rag MCP tools for convenience."""

from .advanced import find_similar, hybrid_search, multi_query_search
from .management import delete_document, ingest_batch, ingest_document, kb_resync, kb_status, update_document
from .metadata import get_document_metadata
from .observability import collection_stats, explain_retrieval, list_collections, retrieval_log
from .retrieval import get_document_chunk, get_documents, search_summaries

__all__ = [
    "search_summaries",
    "get_documents",
    "get_document_chunk",
    "find_similar",
    "multi_query_search",
    "hybrid_search",
    "ingest_document",
    "ingest_batch",
    "delete_document",
    "update_document",
    "kb_status",
    "kb_resync",
    "get_document_metadata",
    "retrieval_log",
    "collection_stats",
    "list_collections",
    "explain_retrieval",
]
