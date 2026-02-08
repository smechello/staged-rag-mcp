from __future__ import annotations


def document_resource(doc_id: str) -> dict:
    """Return a lightweight document locator for MCP resources."""
    return {"uri": f"doc://{doc_id}", "doc_id": doc_id}


def collection_resource(collection: str = "default") -> dict:
    """Return metadata for a document collection."""
    return {"uri": f"collection://{collection}", "collection": collection}
