from __future__ import annotations

from typing import Iterable

from rank_bm25 import BM25Okapi


class BM25Scorer:
    """BM25 scorer for keyword-based retrieval."""

    def __init__(self) -> None:
        self._bm25: BM25Okapi | None = None
        self._doc_ids: list[str] = []

    def build(self, documents: Iterable[dict[str, str]]) -> None:
        corpus = []
        self._doc_ids = []
        for document in documents:
            text = document.get("keyword_text", "")
            corpus.append(text.lower().split())
            self._doc_ids.append(document["doc_id"])
        self._bm25 = BM25Okapi(corpus) if corpus else None

    def score(self, query: str) -> list[tuple[str, float]]:
        if not self._bm25:
            return []
        tokenized_query = query.lower().split()
        scores = self._bm25.get_scores(tokenized_query)
        return list(zip(self._doc_ids, scores))
