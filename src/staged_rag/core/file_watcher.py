"""File-system watcher that monitors a knowledge-base folder for changes.

Uses polling (no native OS events needed) so it works everywhere and
integrates cleanly with the async / threaded MCP server lifecycle.
"""

from __future__ import annotations

import hashlib
import logging
import threading
import time
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)

# File extensions that should be treated as knowledge-base documents
SUPPORTED_EXTENSIONS: set[str] = {
    ".txt", ".md", ".markdown", ".rst",
    ".json", ".yaml", ".yml",
    ".csv", ".tsv",
    ".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".go", ".rs",
    ".html", ".htm", ".xml",
    ".log", ".cfg", ".ini", ".toml",
    ".pdf",  # placeholder – reader can be extended later
}


def _file_hash(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's contents."""
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
    except (OSError, PermissionError):
        return ""
    return h.hexdigest()


class FileWatcher:
    """Poll a directory tree for added / modified / deleted files.

    Parameters
    ----------
    watch_dir : Path
        Root directory to watch (the knowledge_base folder).
    poll_interval : float
        Seconds between successive scans.  Default 5.
    on_created : callback(path)
        Called when a new file appears.
    on_modified : callback(path)
        Called when a file's content hash changes.
    on_deleted : callback(path)
        Called when a previously-tracked file disappears.
    extensions : set[str] | None
        Only watch files with these extensions.  ``None`` = SUPPORTED_EXTENSIONS.
    """

    def __init__(
        self,
        watch_dir: Path,
        poll_interval: float = 5.0,
        on_created: Callable[[Path], None] | None = None,
        on_modified: Callable[[Path], None] | None = None,
        on_deleted: Callable[[Path], None] | None = None,
        extensions: set[str] | None = None,
    ) -> None:
        self.watch_dir = watch_dir
        self.poll_interval = poll_interval
        self._on_created = on_created or (lambda _: None)
        self._on_modified = on_modified or (lambda _: None)
        self._on_deleted = on_deleted or (lambda _: None)
        self._extensions = extensions or SUPPORTED_EXTENSIONS

        # {relative_path_str: sha256_hex}
        self._known: dict[str, str] = {}
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    # ------------------------------------------------------------------
    # Scanning
    # ------------------------------------------------------------------

    def _scan(self) -> dict[str, str]:
        """Walk the directory and return {relative_path: hash}."""
        result: dict[str, str] = {}
        if not self.watch_dir.exists():
            return result
        for path in self.watch_dir.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in self._extensions:
                continue
            rel = str(path.relative_to(self.watch_dir))
            result[rel] = _file_hash(path)
        return result

    def _diff(self, current: dict[str, str]) -> tuple[list[str], list[str], list[str]]:
        """Compare *current* snapshot against known state.

        Returns (created, modified, deleted) lists of relative paths.
        """
        old_keys = set(self._known)
        new_keys = set(current)

        created = sorted(new_keys - old_keys)
        deleted = sorted(old_keys - new_keys)
        modified = sorted(
            k for k in old_keys & new_keys if self._known[k] != current[k]
        )
        return created, modified, deleted

    # ------------------------------------------------------------------
    # Initial snapshot (used for manifest bootstrap)
    # ------------------------------------------------------------------

    def snapshot(self) -> dict[str, str]:
        """Take a snapshot without triggering callbacks.  Returns {rel: hash}."""
        snap = self._scan()
        self._known = dict(snap)
        return snap

    # ------------------------------------------------------------------
    # Background polling loop
    # ------------------------------------------------------------------

    def _poll_loop(self) -> None:
        logger.info("FileWatcher started – monitoring %s (interval=%ss)", self.watch_dir, self.poll_interval)
        while not self._stop_event.is_set():
            try:
                current = self._scan()
                created, modified, deleted = self._diff(current)

                for rel in created:
                    full = self.watch_dir / rel
                    logger.info("KB file created: %s", rel)
                    try:
                        self._on_created(full)
                    except Exception:
                        logger.exception("Error handling created file %s", rel)

                for rel in modified:
                    full = self.watch_dir / rel
                    logger.info("KB file modified: %s", rel)
                    try:
                        self._on_modified(full)
                    except Exception:
                        logger.exception("Error handling modified file %s", rel)

                for rel in deleted:
                    full = self.watch_dir / rel
                    logger.info("KB file deleted: %s", rel)
                    try:
                        self._on_deleted(full)
                    except Exception:
                        logger.exception("Error handling deleted file %s", rel)

                self._known = current
            except Exception:
                logger.exception("FileWatcher poll error")

            self._stop_event.wait(self.poll_interval)
        logger.info("FileWatcher stopped")

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the watcher in a daemon thread."""
        if self._thread and self._thread.is_alive():
            return
        self.watch_dir.mkdir(parents=True, exist_ok=True)
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_loop, daemon=True, name="kb-file-watcher")
        self._thread.start()

    def stop(self) -> None:
        """Signal the watcher to stop and wait for the thread to exit."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=self.poll_interval + 2)
            self._thread = None

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def set_known(self, known: dict[str, str]) -> None:
        """Restore known-state from a persisted manifest."""
        self._known = dict(known)
