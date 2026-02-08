from __future__ import annotations

import threading
from pathlib import Path

import numpy as np

from staged_rag.utils import normalize_vectors


class VectorIndex:
    """Persisted vector index with cosine similarity search."""

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._doc_ids: list[str] = []
        self._vectors: np.ndarray | None = None
        self._lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        data = np.load(self.storage_path, allow_pickle=True)
        self._doc_ids = list(data["doc_ids"])
        self._vectors = data["vectors"]

    def _persist(self) -> None:
        if self._vectors is None:
            return
        np.savez_compressed(self.storage_path, doc_ids=np.array(self._doc_ids), vectors=self._vectors)

    def upsert(self, doc_id: str, vector: list[float]) -> None:
        with self._lock:
            vector_array = np.array(vector, dtype=float)
            if self._vectors is None:
                self._doc_ids = [doc_id]
                self._vectors = vector_array.reshape(1, -1)
            elif doc_id in self._doc_ids:
                index = self._doc_ids.index(doc_id)
                self._vectors[index] = vector_array
            else:
                self._doc_ids.append(doc_id)
                self._vectors = np.vstack([self._vectors, vector_array])
            self._persist()

    def delete(self, doc_id: str) -> None:
        with self._lock:
            if self._vectors is None or doc_id not in self._doc_ids:
                return
            index = self._doc_ids.index(doc_id)
            self._doc_ids.pop(index)
            self._vectors = np.delete(self._vectors, index, axis=0) if self._vectors.size else None
            if self._vectors is None or not self._doc_ids:
                if self.storage_path.exists():
                    self.storage_path.unlink()
            else:
                self._persist()

    def search(self, query_vector: list[float], top_k: int) -> list[tuple[str, float]]:
        with self._lock:
            if self._vectors is None or not self._doc_ids:
                return []
            matrix = normalize_vectors(self._vectors)
            query = normalize_vectors(np.array(query_vector, dtype=float).reshape(1, -1))
            scores = matrix @ query.T
            scores = scores.flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            return [(self._doc_ids[int(i)], float(scores[int(i)])) for i in top_indices]
