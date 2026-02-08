"""Manifest tracker for the knowledge-base folder.

Keeps a ``kb_manifest.json`` file that maps every watched file to its
doc_id, content hash, size, and timestamps.  This lets the system
know exactly which files have been indexed and detect changes across
server restarts without re-scanning the vector store.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ManifestEntry:
    """Single file entry inside the manifest."""

    __slots__ = ("relative_path", "doc_id", "content_hash", "file_size",
                 "indexed_at", "updated_at", "status", "error")

    def __init__(
        self,
        relative_path: str,
        doc_id: str,
        content_hash: str,
        file_size: int = 0,
        indexed_at: str | None = None,
        updated_at: str | None = None,
        status: str = "indexed",
        error: str | None = None,
    ) -> None:
        self.relative_path = relative_path
        self.doc_id = doc_id
        self.content_hash = content_hash
        self.file_size = file_size
        now = datetime.now(timezone.utc).isoformat()
        self.indexed_at = indexed_at or now
        self.updated_at = updated_at or now
        self.status = status  # "indexed" | "skipped" | "error" | "deleted"
        self.error = error

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "relative_path": self.relative_path,
            "doc_id": self.doc_id,
            "content_hash": self.content_hash,
            "file_size": self.file_size,
            "indexed_at": self.indexed_at,
            "updated_at": self.updated_at,
            "status": self.status,
        }
        if self.error:
            d["error"] = self.error
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ManifestEntry":
        return cls(
            relative_path=data["relative_path"],
            doc_id=data["doc_id"],
            content_hash=data.get("content_hash", ""),
            file_size=data.get("file_size", 0),
            indexed_at=data.get("indexed_at"),
            updated_at=data.get("updated_at"),
            status=data.get("status", "indexed"),
            error=data.get("error"),
        )


class KBManifest:
    """JSON-backed manifest that tracks knowledge-base file → doc_id mappings.

    The manifest file is stored alongside the data directory so that it
    persists across server restarts.

    Schema::

        {
            "version": 1,
            "kb_dir": "<absolute path>",
            "files": {
                "relative/path.md": { ... ManifestEntry ... },
                ...
            },
            "stats": {
                "total_files": 10,
                "total_indexed": 9,
                "total_errors": 1,
                "last_scan": "2026-02-08T..."
            }
        }
    """

    VERSION = 1

    def __init__(self, manifest_path: Path, kb_dir: Path) -> None:
        self.manifest_path = manifest_path
        self.kb_dir = kb_dir
        self._entries: dict[str, ManifestEntry] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not self.manifest_path.exists():
            return
        try:
            raw = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            for rel_path, entry_data in raw.get("files", {}).items():
                self._entries[rel_path] = ManifestEntry.from_dict(entry_data)
            logger.info("Loaded KB manifest with %d entries", len(self._entries))
        except Exception:
            logger.exception("Failed to load KB manifest – starting fresh")
            self._entries = {}

    def save(self) -> None:
        """Persist the manifest to disk."""
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        indexed = sum(1 for e in self._entries.values() if e.status == "indexed")
        errors = sum(1 for e in self._entries.values() if e.status == "error")
        payload = {
            "version": self.VERSION,
            "kb_dir": str(self.kb_dir),
            "files": {rel: entry.to_dict() for rel, entry in sorted(self._entries.items())},
            "stats": {
                "total_files": len(self._entries),
                "total_indexed": indexed,
                "total_errors": errors,
                "last_scan": datetime.now(timezone.utc).isoformat(),
            },
        }
        self.manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def get(self, relative_path: str) -> ManifestEntry | None:
        return self._entries.get(relative_path)

    def upsert(self, entry: ManifestEntry) -> None:
        self._entries[entry.relative_path] = entry
        self.save()

    def remove(self, relative_path: str) -> ManifestEntry | None:
        entry = self._entries.pop(relative_path, None)
        if entry is not None:
            self.save()
        return entry

    def all_entries(self) -> list[ManifestEntry]:
        return list(self._entries.values())

    def indexed_entries(self) -> list[ManifestEntry]:
        return [e for e in self._entries.values() if e.status == "indexed"]

    def doc_id_for(self, relative_path: str) -> str | None:
        entry = self._entries.get(relative_path)
        return entry.doc_id if entry else None

    def relative_path_for(self, doc_id: str) -> str | None:
        for entry in self._entries.values():
            if entry.doc_id == doc_id:
                return entry.relative_path
        return None

    def known_hashes(self) -> dict[str, str]:
        """Return {relative_path: content_hash} for watcher bootstrap."""
        # IMPORTANT: include non-indexed files too (e.g., skipped/error) so the watcher
        # doesn't repeatedly re-process the same unreadable/unsupported files forever.
        return {rel: e.content_hash for rel, e in self._entries.items() if e.status != "deleted"}

    def summary(self) -> dict[str, Any]:
        indexed = sum(1 for e in self._entries.values() if e.status == "indexed")
        errors = sum(1 for e in self._entries.values() if e.status == "error")
        return {
            "total_files": len(self._entries),
            "total_indexed": indexed,
            "total_errors": errors,
            "files": [e.to_dict() for e in self._entries.values()],
        }
