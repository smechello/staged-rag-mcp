from __future__ import annotations

import json
import threading
from pathlib import Path


class DocumentStore:
    """JSON-backed document store per collection."""

    def __init__(self, store_dir: Path) -> None:
        self.store_dir = store_dir
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, dict[str, dict]] = {}
        self._lock = threading.Lock()

    def _path_for(self, collection: str) -> Path:
        return self.store_dir / f"{collection}.json"

    def _load(self, collection: str) -> dict[str, dict]:
        if collection in self._cache:
            return self._cache[collection]
        path = self._path_for(collection)
        if not path.exists():
            self._cache[collection] = {}
            return self._cache[collection]
        data = json.loads(path.read_text())
        self._cache[collection] = {doc_id: doc for doc_id, doc in data.items()}
        return self._cache[collection]

    def _persist(self, collection: str) -> None:
        data = self._cache.get(collection, {})
        path = self._path_for(collection)
        path.write_text(json.dumps(data, indent=2))

    def save(self, collection: str, document: dict) -> None:
        with self._lock:
            store = self._load(collection)
            store[document["doc_id"]] = document
            self._persist(collection)

    def save_many(self, collection: str, documents: list[dict]) -> None:
        with self._lock:
            store = self._load(collection)
            for doc in documents:
                store[doc["doc_id"]] = doc
            self._persist(collection)

    def get(self, collection: str, doc_id: str) -> dict | None:
        with self._lock:
            return self._load(collection).get(doc_id)

    def list(self, collection: str) -> list[dict]:
        with self._lock:
            return list(self._load(collection).values())

    def delete(self, collection: str, doc_id: str) -> dict | None:
        with self._lock:
            store = self._load(collection)
            doc = store.pop(doc_id, None)
            if doc is not None:
                self._persist(collection)
            return doc
