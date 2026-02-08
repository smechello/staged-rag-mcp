"""Knowledge-base folder manager.

Bridges the FileWatcher, KBManifest, and RAGService so that
file-system events (create / modify / delete) automatically
translate into vector-store operations.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from staged_rag.core.file_watcher import FileWatcher, _file_hash
from staged_rag.core.kb_manifest import KBManifest, ManifestEntry
from staged_rag.utils import clean_text

logger = logging.getLogger(__name__)

# Maximum file size to auto-ingest (10 MB).  Override via config.
DEFAULT_MAX_FILE_SIZE: int = 10 * 1024 * 1024


def _extract_pdf_title(path: Path) -> str | None:
    """Try to extract a meaningful title from PDF metadata or first heading."""
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None

    try:
        with path.open("rb") as fh:
            reader = PdfReader(fh)
            meta = reader.metadata
            if meta:
                # Try /Title metadata field
                title = getattr(meta, "title", None) or meta.get("/Title")
                if title and isinstance(title, str):
                    title = title.strip()
                    # Clean up underscore/hyphen-based titles
                    if "_" in title or "-" in title:
                        title = title.replace("_", " ").replace("-", " ")
                        # Title-case if it looks like a slug
                        if title == title.lower() or title == title.upper():
                            title = title.title()
                    # Skip if title is just the filename or generic
                    if (
                        title
                        and len(title) > 3
                        and title.lower() not in {"untitled", "microsoft word", ""}
                        and not title.startswith("%PDF")
                    ):
                        return title
    except Exception:
        pass
    return None


def _title_from_first_line(text: str) -> str | None:
    """Extract a reasonable title from the first non-trivial line of text."""
    for line in text.splitlines():
        line = line.strip()
        if not line or len(line) < 5:
            continue
        # Skip lines that are just numbers (page numbers)
        if line.isdigit():
            continue
        # Use the first substantial line (truncate if too long)
        if len(line) > 120:
            line = line[:117] + "..."
        return line
    return None


def _read_pdf_text(path: Path) -> tuple[str, str | None]:
    """Extract text from a PDF using pypdf.

    Returns (text, error_reason). If extraction fails or produces no text, text is "".
    """
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return (
            "",
            "PDF text extraction requires 'pypdf' (install with: pip install pypdf)",
        )

    try:
        with path.open("rb") as fh:
            reader = PdfReader(fh)
            if getattr(reader, "is_encrypted", False):
                try:
                    reader.decrypt("")
                except Exception:
                    return ("", "PDF is encrypted and cannot be decrypted")

            page_texts: list[str] = []
            for i, page in enumerate(reader.pages):
                try:
                    extracted = page.extract_text() or ""
                except Exception:
                    logger.debug("Failed to extract text from %s page %d", path, i)
                    extracted = ""
                extracted = extracted.strip()
                if extracted:
                    page_texts.append(extracted)

        text = "\n\n".join(page_texts).strip()
        if not text:
            return ("", "No extractable text found in PDF")
        return (text, None)
    except Exception as exc:
        logger.exception("Cannot read PDF %s", path)
        return ("", f"Failed to read PDF: {type(exc).__name__}")


def _read_file_text(path: Path) -> tuple[str, str | None]:
    """Best-effort text read.

    Returns (text, error_reason). If read fails or produces no text, text is "".
    """
    if path.suffix.lower() == ".pdf":
        return _read_pdf_text(path)

    try:
        return (path.read_text(encoding="utf-8", errors="replace"), None)
    except (OSError, PermissionError) as exc:
        logger.warning("Cannot read file %s", path)
        return ("", f"Cannot read file: {type(exc).__name__}")


def _derive_tags(path: Path, kb_dir: Path) -> list[str]:
    """Derive tags from file extension and parent subdirectories."""
    tags: list[str] = []
    ext = path.suffix.lower().lstrip(".")
    if ext:
        tags.append(f"filetype:{ext}")
    tags.append("source:knowledge_base")
    # Add subfolder names as tags (useful for topic organisation)
    try:
        rel = path.relative_to(kb_dir)
        for part in rel.parent.parts:
            if part and part != ".":
                tags.append(f"folder:{part}")
    except ValueError:
        pass
    return tags


class KnowledgeBaseManager:
    """Orchestrates automatic ingestion of files from a knowledge-base folder.

    Usage (from server startup)::

        from staged_rag.service import get_service
        kb_mgr = KnowledgeBaseManager(
            kb_dir=Path("./knowledge_base"),
            manifest_path=Path("./data/kb_manifest.json"),
            collection="default",
            poll_interval=5.0,
        )
        kb_mgr.start()   # starts background watcher
        ...
        kb_mgr.stop()     # on server shutdown
    """

    def __init__(
        self,
        kb_dir: Path,
        manifest_path: Path,
        collection: str = "default",
        poll_interval: float = 5.0,
        max_file_size: int = DEFAULT_MAX_FILE_SIZE,
        auto_summary: bool = True,
    ) -> None:
        self.kb_dir = kb_dir.resolve()
        self.collection = collection
        self.max_file_size = max_file_size
        self.auto_summary = auto_summary

        self.manifest = KBManifest(manifest_path, self.kb_dir)

        self.watcher = FileWatcher(
            watch_dir=self.kb_dir,
            poll_interval=poll_interval,
            on_created=self._handle_created,
            on_modified=self._handle_modified,
            on_deleted=self._handle_deleted,
        )

    # ------------------------------------------------------------------
    # Lazy import to avoid circular dependency with service singleton
    # ------------------------------------------------------------------

    @staticmethod
    def _get_service():
        from staged_rag.service import get_service
        return get_service()

    # ------------------------------------------------------------------
    # Initial sync – run once before starting the watcher
    # ------------------------------------------------------------------

    def initial_sync(self) -> dict[str, Any]:
        """Compare the manifest against the actual folder and sync differences.

        * New files   → ingest
        * Changed hash → re-ingest (delete + ingest)
        * Deleted files → remove from store & index

        Returns summary statistics.
        """
        logger.info("Running initial KB sync for %s …", self.kb_dir)
        self.kb_dir.mkdir(parents=True, exist_ok=True)

        current_snapshot = self.watcher.snapshot()  # {rel: hash}
        manifest_hashes = self.manifest.known_hashes()  # {rel: hash}

        created = sorted(set(current_snapshot) - set(manifest_hashes))
        deleted = sorted(set(manifest_hashes) - set(current_snapshot))
        modified = sorted(
            r for r in set(current_snapshot) & set(manifest_hashes)
            if current_snapshot[r] != manifest_hashes[r]
        )

        stats = {"created": 0, "modified": 0, "deleted": 0, "errors": 0}

        for rel in created:
            full = self.kb_dir / rel
            try:
                self._ingest_file(full)
                stats["created"] += 1
            except Exception:
                logger.exception("Initial sync – failed to ingest %s", rel)
                stats["errors"] += 1

        for rel in modified:
            full = self.kb_dir / rel
            try:
                self._reingest_file(full)
                stats["modified"] += 1
            except Exception:
                logger.exception("Initial sync – failed to re-ingest %s", rel)
                stats["errors"] += 1

        for rel in deleted:
            try:
                self._remove_file(self.kb_dir / rel)
                stats["deleted"] += 1
            except Exception:
                logger.exception("Initial sync – failed to delete %s", rel)
                stats["errors"] += 1

        # Restore known state in watcher from the (now up-to-date) manifest
        self.watcher.set_known(self.manifest.known_hashes())
        logger.info("Initial KB sync complete: %s", stats)
        return stats

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> dict[str, Any]:
        """Run initial sync then start the background file watcher."""
        stats = self.initial_sync()
        self.watcher.start()
        logger.info("KnowledgeBaseManager started – watching %s", self.kb_dir)
        return stats

    def stop(self) -> None:
        """Stop the background watcher."""
        self.watcher.stop()
        logger.info("KnowledgeBaseManager stopped")

    @property
    def is_running(self) -> bool:
        return self.watcher.is_running

    # ------------------------------------------------------------------
    # File-event handlers (called from watcher thread)
    # ------------------------------------------------------------------

    def _handle_created(self, path: Path) -> None:
        self._ingest_file(path)

    def _handle_modified(self, path: Path) -> None:
        self._reingest_file(path)

    def _handle_deleted(self, path: Path) -> None:
        self._remove_file(path)

    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------

    def _relative(self, path: Path) -> str:
        return str(path.resolve().relative_to(self.kb_dir))

    def _ingest_file(self, path: Path) -> None:
        """Read file, ingest into RAG, and record in manifest."""
        rel = self._relative(path)
        logger.info("Ingesting KB file: %s", rel)

        if not path.exists():
            logger.warning("File no longer exists: %s", rel)
            return

        file_size = path.stat().st_size
        if file_size > self.max_file_size:
            entry = ManifestEntry(
                relative_path=rel,
                doc_id="",
                content_hash=_file_hash(path),
                file_size=file_size,
                status="error",
                error=f"File too large ({file_size} bytes, max {self.max_file_size})",
            )
            self.manifest.upsert(entry)
            logger.warning("Skipping large file %s (%d bytes)", rel, file_size)
            return

        content_hash = _file_hash(path)
        text, read_error = _read_file_text(path)
        if not text.strip():
            # Record skipped/error so the watcher doesn't keep re-processing it.
            status = "error" if read_error else "skipped"
            entry = ManifestEntry(
                relative_path=rel,
                doc_id="",
                content_hash=content_hash,
                file_size=file_size,
                status=status,
                error=read_error or "Empty or unsupported file",
            )
            self.manifest.upsert(entry)
            logger.info("Skipping KB file %s (%s)", rel, entry.error)
            return

        # Clean up the text (especially important for PDFs)
        text = clean_text(text)

        # Derive a meaningful title
        title: str | None = None
        if path.suffix.lower() == ".pdf":
            title = _extract_pdf_title(path)
        if not title:
            title = _title_from_first_line(text)
        if not title:
            # Last resort: use the filename stem cleaned up
            title = path.stem.replace("_", " ").replace("-", " ").title()

        tags = _derive_tags(path, self.kb_dir)
        metadata = {
            "kb_relative_path": rel,
            "file_extension": path.suffix.lower(),
            "file_size": file_size,
            "ingested_from": "knowledge_base",
        }

        service = self._get_service()
        result = service.ingest_document(
            title=title,
            text=text,
            source=f"knowledge_base:{rel}",
            collection=self.collection,
            tags=tags,
            metadata=metadata,
            summary=None,  # let auto-summary handle it
        )

        if result.get("status") == "indexed":
            entry = ManifestEntry(
                relative_path=rel,
                doc_id=result["doc_id"],
                content_hash=content_hash,
                file_size=file_size,
                status="indexed",
            )
            self.manifest.upsert(entry)
            logger.info("Indexed KB file %s → doc_id=%s", rel, result["doc_id"])
        else:
            entry = ManifestEntry(
                relative_path=rel,
                doc_id="",
                content_hash=content_hash,
                file_size=file_size,
                status="error",
                error=result.get("error", "Unknown error"),
            )
            self.manifest.upsert(entry)
            logger.error("Failed to index KB file %s: %s", rel, result.get("error"))

    def _reingest_file(self, path: Path) -> None:
        """Delete old version and re-ingest the updated file."""
        rel = self._relative(path)
        existing = self.manifest.get(rel)
        if existing and existing.doc_id:
            service = self._get_service()
            service.delete_document(existing.doc_id, self.collection)
            logger.info("Deleted old doc %s for re-indexing %s", existing.doc_id, rel)
        self._ingest_file(path)

    def _remove_file(self, path: Path) -> None:
        """Remove the document from the RAG store and manifest."""
        rel = self._relative(path)
        existing = self.manifest.get(rel)
        if existing and existing.doc_id:
            service = self._get_service()
            service.delete_document(existing.doc_id, self.collection)
            logger.info("Removed doc %s for deleted file %s", existing.doc_id, rel)
        self.manifest.remove(rel)

    # ------------------------------------------------------------------
    # Manual triggers / introspection
    # ------------------------------------------------------------------

    def force_resync(self) -> dict[str, Any]:
        """Clear the manifest and re-ingest everything from scratch."""
        logger.info("Force re-sync requested – clearing manifest")
        # Delete all existing KB-sourced docs
        service = self._get_service()
        for entry in self.manifest.indexed_entries():
            if entry.doc_id:
                service.delete_document(entry.doc_id, self.collection)
        # Clear manifest entirely
        for entry in list(self.manifest.all_entries()):
            self.manifest.remove(entry.relative_path)
        # Re-initialise known state and re-sync
        self.watcher.set_known({})
        return self.initial_sync()

    def status(self) -> dict[str, Any]:
        """Return current KB status for MCP tool consumption."""
        return {
            "kb_dir": str(self.kb_dir),
            "collection": self.collection,
            "watcher_running": self.is_running,
            "manifest": self.manifest.summary(),
        }
