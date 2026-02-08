from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path


class AuditLogger:
    """Record retrieval events to a JSONL file."""

    def __init__(self, location: str | Path, max_entries: int = 10000) -> None:
        self.location = Path(location)
        self.location.parent.mkdir(parents=True, exist_ok=True)
        self.max_entries = max_entries
        self._lock = threading.Lock()

    def record(self, entry: dict) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **entry,
        }
        with self._lock:
            with self.location.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload) + "\n")
            self._truncate_if_needed()

    def _truncate_if_needed(self) -> None:
        if not self.location.exists():
            return
        lines = self.location.read_text(encoding="utf-8").splitlines()
        if len(lines) <= self.max_entries:
            return
        trimmed = lines[-self.max_entries :]
        self.location.write_text("\n".join(trimmed) + "\n", encoding="utf-8")

    def read(self, last_n: int, tool_filter: str | None = None, session_id: str | None = None) -> list[dict]:
        if not self.location.exists():
            return []
        lines = self.location.read_text(encoding="utf-8").splitlines()
        entries = [json.loads(line) for line in lines if line.strip()]
        if tool_filter:
            entries = [entry for entry in entries if entry.get("tool") == tool_filter]
        if session_id:
            entries = [entry for entry in entries if entry.get("session") == session_id]
        return list(reversed(entries))[:last_n]
