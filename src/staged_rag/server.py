from __future__ import annotations

import logging
from functools import wraps
from typing import Any, Callable

try:
    from fastmcp import FastMCP as MCPServer
except ImportError:  # pragma: no cover
    class MCPServer:
        def __init__(self, *, name: str, instructions: str, resources: dict | None = None) -> None:
            self.name = name
            self.instructions = instructions
            self._tools: list[str] = []

        def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
                self._tools.append(func.__name__)
                return func

            return decorator

        def run(self, transport: str | None = None, **_kwargs: Any) -> None:  # pragma: no cover
            raise NotImplementedError("FastMCP is not installed")

_logger = logging.getLogger(__name__)


def _safe_tool(func: Callable[..., Any]) -> Callable[..., Any]:
    """Wrap a tool handler so that unhandled exceptions return an error dict
    instead of crashing the MCP server."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            _logger.exception("Tool %s failed", func.__name__)
            return {"error": f"{type(exc).__name__}: {exc}"}
    return wrapper

INSTRUCTIONS = """
Staged RAG Server — Two-level retrieval system.
1. Always call search_summaries before any expansion.
2. Inspect summaries + scores before fetching full documents.
3. Prefer targeted chunks instead of entire documents when possible.
4. Log every retrieval and collection change for auditability.
"""

server = MCPServer(name="staged-rag", instructions=INSTRUCTIONS)

from staged_rag.config import load_settings
from staged_rag import tools as rag_tools

@server.tool()
@_safe_tool
def search_summaries(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    min_score: float = 0.0,
    tags_filter: list[str] | None = None,
) -> dict:
    """Entry point that returns compact summaries for candidate documents."""
    return rag_tools.search_summaries(query, top_k, collection, min_score, tags_filter)

@server.tool()
@_safe_tool
def get_documents(doc_ids: list[str], include_chunks: bool = False, collection: str = "default") -> dict:
    """Fetch full text for selected document identifiers."""
    return rag_tools.get_documents(doc_ids, include_chunks, collection)

@server.tool()
@_safe_tool
def get_document_chunk(
    doc_id: str,
    chunk_index: int | None = None,
    chunk_query: str | None = None,
    collection: str = "default",
) -> dict:
    """Return a single chunk of a document for surgical retrieval."""
    return rag_tools.get_document_chunk(doc_id, chunk_index, chunk_query, collection)

@server.tool()
@_safe_tool
def find_similar(doc_id: str, top_k: int = 5, exclude_same_source: bool = False, collection: str = "default") -> dict:
    """Return doc IDs that are semantically similar to the source document."""
    return rag_tools.find_similar(doc_id, top_k, exclude_same_source, collection)

@server.tool()
@_safe_tool
def multi_query_search(
    queries: list[str],
    top_k: int = 5,
    collection: str = "default",
    fusion_method: str = "rrf",
) -> dict:
    """Run several queries and collapse the best summaries for each."""
    return rag_tools.multi_query_search(queries, top_k, collection, fusion_method)

@server.tool()
@_safe_tool
def hybrid_search(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3,
) -> dict:
    """Combine keyword and embedding searches for tighter recall."""
    return rag_tools.hybrid_search(query, top_k, collection, semantic_weight, keyword_weight)

@server.tool()
@_safe_tool
def ingest_document(
    title: str,
    text: str,
    source: str = "manual",
    collection: str = "default",
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None,
) -> dict:
    """Store a single document into the JSON store + vector index."""
    return rag_tools.ingest_document(title, text, source, collection, tags, metadata, summary)

@server.tool()
@_safe_tool
def ingest_batch(documents: list[dict[str, Any]], collection: str = "default") -> dict:
    """Bulk ingest helper that batches document writes."""
    return rag_tools.ingest_batch(documents, collection)

@server.tool()
@_safe_tool
def delete_document(doc_id: str, collection: str = "default") -> dict:
    """Delete a document and prune related embeddings."""
    return rag_tools.delete_document(doc_id, collection)

@server.tool()
@_safe_tool
def update_document(
    doc_id: str,
    text: str | None = None,
    title: str | None = None,
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None,
    collection: str = "default",
) -> dict:
    """Update metadata or rerun chunking for a stored document."""
    return rag_tools.update_document(doc_id, text, title, tags, metadata, summary, collection)

@server.tool()
@_safe_tool
def get_document_metadata(doc_id: str, collection: str = "default") -> dict:
    """Return stored metadata for a document without full text."""
    return rag_tools.get_document_metadata(doc_id, collection)

@server.tool()
@_safe_tool
def retrieval_log(last_n: int = 10, tool_filter: str | None = None, session_id: str | None = None) -> dict:
    """Emit audit events that describe every retrieval call."""
    return rag_tools.retrieval_log(last_n, tool_filter, session_id)

@server.tool()
@_safe_tool
def collection_stats(collection: str = "default") -> dict:
    """Return collection sizes and token counts."""
    return rag_tools.collection_stats(collection)

@server.tool()
@_safe_tool
def list_collections() -> dict:
    """Utility to enumerate configured collections."""
    return rag_tools.list_collections()

@server.tool()
@_safe_tool
def explain_retrieval(query: str, doc_ids: list[str], collection: str = "default") -> dict:
    """Explain retrieval ranking for a query."""
    return rag_tools.explain_retrieval(query, doc_ids, collection)


# ---------------------------------------------------------------------------
# Knowledge-base tools
# ---------------------------------------------------------------------------

@server.tool()
@_safe_tool
def kb_status() -> dict:
    """Return current knowledge-base watcher status and manifest summary."""
    from staged_rag.service import get_kb_manager
    mgr = get_kb_manager()
    if mgr is None:
        return {"enabled": False, "message": "Knowledge-base watcher is not enabled. Set knowledge_base.enabled=true in config.yaml."}
    return mgr.status()


@server.tool()
@_safe_tool
def kb_resync() -> dict:
    """Force a full re-sync of the knowledge-base folder.

    Deletes all KB-sourced documents and re-ingests everything from the folder.
    """
    from staged_rag.service import get_kb_manager
    mgr = get_kb_manager()
    if mgr is None:
        return {"enabled": False, "message": "Knowledge-base watcher is not enabled."}
    return mgr.force_resync()


def start_server() -> None:
    import logging
    settings = load_settings()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.logging.log_level, logging.INFO),
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    # Start knowledge-base watcher if enabled
    from staged_rag.service import start_kb_manager, stop_kb_manager
    kb_mgr = start_kb_manager(settings)
    if kb_mgr:
        logging.getLogger(__name__).info(
            "Knowledge-base watcher active – monitoring %s", settings.knowledge_base.kb_dir
        )

    if hasattr(server, "run"):
        try:
            server.run(transport=settings.server.transport, host=settings.server.host, port=settings.server.port)
        finally:
            stop_kb_manager()
        return
    raise RuntimeError("MCP server cannot start with current fastmcp version")

if __name__ == "__main__":
    start_server()
