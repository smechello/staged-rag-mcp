from __future__ import annotations

from staged_rag.service import get_service


def get_document_metadata(doc_id: str, collection: str = "default") -> dict:
    """Return stored metadata without reading full text."""
    service = get_service()
    return service.get_document_metadata(doc_id, collection)
