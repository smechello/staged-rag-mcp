from __future__ import annotations

from typing import Any

from staged_rag.service import get_kb_manager, get_service, start_kb_manager, stop_kb_manager


def ingest_document(
    title: str,
    text: str,
    source: str = "manual",
    collection: str = "default",
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None,
) -> dict:
    """Write a single document record into storage and index."""
    service = get_service()
    return service.ingest_document(title, text, source, collection, tags, metadata, summary)


def ingest_batch(documents: list[dict[str, Any]], collection: str = "default") -> dict:
    """Multi-document helper used during onboarding or evaluation."""
    service = get_service()
    return service.ingest_batch(documents, collection)


def delete_document(doc_id: str, collection: str = "default") -> dict:
    """Remove a document and all associated chunks."""
    service = get_service()
    return service.delete_document(doc_id, collection)


def update_document(
    doc_id: str,
    text: str | None = None,
    title: str | None = None,
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None,
    collection: str = "default",
) -> dict:
    """Patch metadata or rerun chunking for an existing document."""
    service = get_service()
    return service.update_document(doc_id, collection, text, title, tags, metadata, summary)


def kb_status() -> dict:
    """Return Knowledge Base (knowledge_base folder) status.

    If the KB manager isn't running in this process, this will start it
    long enough to read status, then stop it.
    """
    manager = get_kb_manager()
    started_here = False
    if manager is None:
        manager = start_kb_manager()
        started_here = manager is not None

    if manager is None:
        return {"enabled": False, "watcher_running": False}

    payload = manager.status()
    if started_here:
        stop_kb_manager()
    return payload


def kb_resync() -> dict:
    """Force a full re-sync of the knowledge_base folder.

    Deletes all KB-sourced docs tracked in the manifest, clears the manifest,
    then re-ingests everything found in the folder.
    """
    manager = get_kb_manager()
    started_here = False
    if manager is None:
        manager = start_kb_manager()
        started_here = manager is not None

    if manager is None:
        return {"enabled": False, "status": "knowledge_base disabled"}

    stats = manager.force_resync()
    if started_here:
        stop_kb_manager()
    return stats
