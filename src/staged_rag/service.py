from __future__ import annotations

import time
import uuid
from typing import Any, Iterable

from staged_rag.config import Settings, load_settings
from staged_rag.core.bm25 import BM25Scorer
from staged_rag.core.chunk_manager import ChunkManager
from staged_rag.core.document_store import DocumentStore
from staged_rag.core.embeddings import EmbeddingEngine
from staged_rag.core.summary_generator import SummaryGenerator
from staged_rag.core.vector_index import VectorIndex
from staged_rag.logging.audit import AuditLogger
from staged_rag.models.document import Document, DocumentChunk
from staged_rag.models.search import SearchResponse, SummaryResult
from staged_rag.utils import count_tokens


class RAGService:
    """Coordinates ingestion, retrieval, and audit logging."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.store = DocumentStore(settings.storage.store_dir)
        self.audit = AuditLogger(settings.logging.audit_file, settings.logging.max_log_entries)
        self.chunker = ChunkManager()
        self.embedding = EmbeddingEngine(
            provider=settings.embedding.provider,
            api_key=_read_api_key(),
            model_name=settings.embedding.model,
            dimension=settings.embedding.dimensions,
            provider_config=settings.embedding.provider_config,
        )
        self.summarizer = SummaryGenerator(
            api_key=_read_api_key(),
            model_name=settings.generation.model,
            max_sentences=settings.generation.summary_max_sentences,
        )
        self._bm25: dict[str, BM25Scorer] = {}
        self._indexes: dict[str, VectorIndex] = {}

    def _log(self, tool: str, params: dict[str, Any], result_count: int, doc_ids: Iterable[str], latency_ms: float) -> None:
        self.audit.record(
            {
                "tool": tool,
                "params": params,
                "result_count": result_count,
                "doc_ids": list(doc_ids),
                "latency_ms": latency_ms,
            }
        )

    def _index_for(self, collection: str) -> VectorIndex:
        if collection not in self._indexes:
            index_path = self.settings.storage.index_dir / f"{collection}.npz"
            self._indexes[collection] = VectorIndex(index_path)
        return self._indexes[collection]

    def _bm25_for(self, collection: str) -> BM25Scorer:
        if collection not in self._bm25:
            self._bm25[collection] = BM25Scorer()
            self._rebuild_bm25(collection)
        return self._bm25[collection]

    def _rebuild_bm25(self, collection: str) -> None:
        scorer = self._bm25.setdefault(collection, BM25Scorer())
        documents = []
        for doc in self.store.list(collection):
            # Include title, summary, AND full_text for better keyword coverage
            keyword_text = f"{doc.get('title', '')} {doc.get('summary', '')} {doc.get('full_text', '')}"
            documents.append({"doc_id": doc["doc_id"], "keyword_text": keyword_text})
        scorer.build(documents)

    def ingest_document(
        self,
        title: str,
        text: str,
        source: str,
        collection: str,
        tags: list[str] | None,
        metadata: dict[str, Any] | None,
        summary: str | None,
    ) -> dict[str, Any]:
        start_time = time.time()
        if not title or not title.strip():
            return {"status": "error", "error": "Title must not be empty"}
        if not text or not text.strip():
            return {"status": "error", "error": "Text must not be empty"}
        token_count = count_tokens(text)
        if token_count > self.settings.ingestion.max_document_tokens:
            return {"status": "error", "error": "Document exceeds max tokens"}

        doc_id = str(uuid.uuid4())
        summary_text = summary or (self.summarizer.summarize(text) if self.settings.ingestion.auto_summary else "")
        chunk_metadata = self.chunker.chunk(
            text,
            self.settings.chunking.chunk_size,
            self.settings.chunking.chunk_overlap,
            self.settings.chunking.min_chunk_size,
        )
        chunks = [DocumentChunk(**chunk) for chunk in chunk_metadata]

        document = Document(
            doc_id=doc_id,
            title=title,
            source=source,
            full_text=text,
            summary=summary_text,
            chunks=chunks,
            tags=tags or [],
            collection=collection,
            token_count=token_count,
            metadata=metadata or {},
        )

        self.store.save(collection, document.model_dump(mode="json"))
        embedding = self.embedding.encode([summary_text])[0] if summary_text else self.embedding.encode([title])[0]
        self._index_for(collection).upsert(doc_id, embedding)
        self._rebuild_bm25(collection)

        elapsed_ms = (time.time() - start_time) * 1000
        self._log(
            "ingest_document",
            {"title": title, "source": source, "collection": collection},
            1,
            [doc_id],
            elapsed_ms,
        )

        return {
            "doc_id": doc_id,
            "title": title,
            "collection": collection,
            "chunk_count": len(chunks),
            "token_count": token_count,
            "summary": summary_text,
            "status": "indexed",
        }

    def ingest_batch(self, documents: list[dict[str, Any]], collection: str) -> dict[str, Any]:
        if len(documents) > self.settings.ingestion.max_batch_size:
            return {
                "total": len(documents),
                "succeeded": 0,
                "failed": len(documents),
                "results": [],
                "total_tokens_indexed": 0,
            }
        start_time = time.time()
        results = []
        succeeded = 0
        failed = 0
        total_tokens = 0
        for payload in documents:
            try:
                if "title" not in payload or "text" not in payload:
                    failed += 1
                    results.append({"title": payload.get("title", "<missing>"), "status": "error", "error": "Missing required 'title' or 'text' field"})
                    continue
                result = self.ingest_document(
                    title=payload["title"],
                    text=payload["text"],
                    source=payload.get("source", "batch"),
                    collection=collection,
                    tags=payload.get("tags"),
                    metadata=payload.get("metadata"),
                    summary=payload.get("summary"),
                )
                if result.get("status") == "indexed":
                    succeeded += 1
                    total_tokens += int(result.get("token_count", 0))
                    results.append({"doc_id": result["doc_id"], "title": result["title"], "status": "indexed"})
                else:
                    failed += 1
                    results.append({"title": payload.get("title", ""), "status": "error", "error": result.get("error")})
            except Exception as exc:
                failed += 1
                results.append({"title": payload.get("title", ""), "status": "error", "error": str(exc)})

        payload = {
            "total": len(documents),
            "succeeded": succeeded,
            "failed": failed,
            "results": results,
            "total_tokens_indexed": total_tokens,
        }
        self._log(
            "ingest_batch",
            {"collection": collection, "count": len(documents)},
            succeeded,
            [item.get("doc_id") for item in results if item.get("doc_id")],
            (time.time() - start_time) * 1000,
        )
        return payload

    def search_summaries(
        self,
        query: str,
        top_k: int,
        collection: str,
        min_score: float,
        tags_filter: list[str] | None,
    ) -> dict[str, Any]:
        start_time = time.time()
        if not query or not query.strip():
            return SearchResponse(query=query or "", results=[], total_candidates=0, search_time_ms=0.0).model_dump()
        top_k = max(1, min(top_k, self.settings.retrieval.max_top_k))
        index = self._index_for(collection)
        query_vector = self.embedding.encode([query])[0]
        scored = index.search(query_vector, top_k)
        documents = {doc["doc_id"]: doc for doc in self.store.list(collection)}

        results: list[SummaryResult] = []
        for doc_id, score in scored:
            doc = documents.get(doc_id)
            if not doc:
                continue
            clamped_score = max(0.0, min(1.0, float(score)))
            if clamped_score < min_score:
                continue
            if tags_filter and not set(tags_filter).intersection(set(doc.get("tags", []))):
                continue
            results.append(
                SummaryResult(
                    doc_id=doc_id,
                    title=doc.get("title", ""),
                    summary=doc.get("summary", ""),
                    similarity_score=clamped_score,
                    token_count=doc.get("token_count", 0),
                    tags=doc.get("tags", []),
                    collection=doc.get("collection", collection),
                )
            )

        response = SearchResponse(
            query=query,
            results=results,
            total_candidates=len(documents),
            search_time_ms=(time.time() - start_time) * 1000,
        )

        self._log(
            "search_summaries",
            {"query": query, "top_k": top_k, "collection": collection},
            len(results),
            [result.doc_id for result in results],
            response.search_time_ms,
        )
        return response.model_dump()

    def get_documents(self, doc_ids: list[str], collection: str, include_chunks: bool) -> dict[str, Any]:
        start_time = time.time()
        documents = []
        total_tokens = 0
        for doc_id in doc_ids:
            doc = self.store.get(collection, doc_id)
            if not doc:
                continue
            payload = {
                "doc_id": doc_id,
                "title": doc.get("title", ""),
                "full_text": doc.get("full_text", ""),
                "source": doc.get("source", ""),
                "token_count": doc.get("token_count", 0),
                "tags": doc.get("tags", []),
                "metadata": doc.get("metadata", {}),
            }
            if include_chunks:
                payload["chunks"] = doc.get("chunks", [])
            documents.append(payload)
            total_tokens += int(payload.get("token_count", 0))

        elapsed_ms = (time.time() - start_time) * 1000
        self._log(
            "get_documents",
            {"doc_ids": doc_ids, "collection": collection},
            len(documents),
            [doc.get("doc_id") for doc in documents],
            elapsed_ms,
        )

        return {"documents": documents, "total_tokens": total_tokens}

    def get_document_chunk(
        self, doc_id: str, collection: str, chunk_index: int | None, chunk_query: str | None
    ) -> dict[str, Any]:
        doc = self.store.get(collection, doc_id)
        if not doc:
            return {"error": "Document not found"}
        chunks = doc.get("chunks", [])
        if chunk_index is None and chunk_query is None:
            return {"error": "Provide chunk_index or chunk_query"}
        if chunk_index is not None:
            if chunk_index < 0 or chunk_index >= len(chunks):
                return {"error": "chunk_index out of range"}
            chunk = chunks[chunk_index]
            self._log(
                "get_document_chunk",
                {"doc_id": doc_id, "chunk_index": chunk_index, "collection": collection},
                1,
                [doc_id],
                0.0,
            )
            return {
                "doc_id": doc_id,
                "chunk_index": chunk_index,
                "total_chunks": len(chunks),
                "text": chunk["text"],
                "token_count": chunk["token_count"],
                "has_previous": chunk_index > 0,
                "has_next": chunk_index < len(chunks) - 1,
            }

        query_vector = self.embedding.encode([chunk_query or ""])[0]
        chunk_texts = [chunk["text"] for chunk in chunks]
        chunk_vectors = self.embedding.encode(chunk_texts)
        index_scores = []
        for idx, vector in enumerate(chunk_vectors):
            query_norm = sum(a * a for a in query_vector) ** 0.5 or 1.0
            vec_norm = sum(a * a for a in vector) ** 0.5 or 1.0
            score = sum(a * b for a, b in zip(query_vector, vector)) / (query_norm * vec_norm)
            index_scores.append((idx, score))
        best_idx, best_score = max(index_scores, key=lambda item: item[1])
        chunk = chunks[best_idx]
        self._log(
            "get_document_chunk",
            {"doc_id": doc_id, "chunk_query": chunk_query, "collection": collection},
            1,
            [doc_id],
            0.0,
        )
        return {
            "doc_id": doc_id,
            "chunk_index": best_idx,
            "total_chunks": len(chunks),
            "text": chunk["text"],
            "token_count": chunk["token_count"],
            "has_previous": best_idx > 0,
            "has_next": best_idx < len(chunks) - 1,
            "relevance_score": float(best_score),
        }

    def get_document_metadata(self, doc_id: str, collection: str) -> dict[str, Any]:
        doc = self.store.get(collection, doc_id)
        if not doc:
            return {"error": "Document not found"}
        payload = {
            "doc_id": doc_id,
            "title": doc.get("title", ""),
            "source": doc.get("source", ""),
            "collection": doc.get("collection", collection),
            "tags": doc.get("tags", []),
            "token_count": doc.get("token_count", 0),
            "chunk_count": len(doc.get("chunks", [])),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
            "metadata": doc.get("metadata", {}),
        }
        self._log("get_document_metadata", {"doc_id": doc_id, "collection": collection}, 1, [doc_id], 0.0)
        return payload

    def find_similar(self, doc_id: str, collection: str, top_k: int, exclude_same_source: bool) -> dict[str, Any]:
        doc = self.store.get(collection, doc_id)
        if not doc:
            return {"query": doc_id, "results": [], "total_candidates": 0, "search_time_ms": 0.0}
        index = self._index_for(collection)
        summary_text = doc.get("summary", "") or doc.get("title", "")
        query_vector = self.embedding.encode([summary_text])[0]
        scored = index.search(query_vector, top_k + 1)
        documents = {doc["doc_id"]: doc for doc in self.store.list(collection)}

        results: list[SummaryResult] = []
        for candidate_id, score in scored:
            if candidate_id == doc_id:
                continue
            candidate = documents.get(candidate_id)
            if not candidate:
                continue
            if exclude_same_source and candidate.get("source") == doc.get("source"):
                continue
            clamped = max(0.0, min(1.0, float(score)))
            results.append(
                SummaryResult(
                    doc_id=candidate_id,
                    title=candidate.get("title", ""),
                    summary=candidate.get("summary", ""),
                    similarity_score=clamped,
                    token_count=candidate.get("token_count", 0),
                    tags=candidate.get("tags", []),
                    collection=candidate.get("collection", collection),
                )
            )
            if len(results) >= top_k:
                break

        response = SearchResponse(
            query=doc_id,
            results=results,
            total_candidates=len(documents),
            search_time_ms=0.0,
        )
        self._log(
            "find_similar",
            {"doc_id": doc_id, "top_k": top_k, "collection": collection},
            len(results),
            [result.doc_id for result in results],
            0.0,
        )
        return response.model_dump()

    def multi_query_search(
        self, queries: list[str], top_k: int, collection: str, fusion_method: str
    ) -> dict[str, Any]:
        rankings: list[list[str]] = []
        scores_lookup: dict[str, float] = {}
        for query in queries:
            response = self.search_summaries(
                query=query,
                top_k=top_k,
                collection=collection,
                min_score=self.settings.retrieval.min_similarity_score,
                tags_filter=None,
            )
            docs = [item["doc_id"] for item in response["results"]]
            rankings.append(docs)
            for item in response["results"]:
                scores_lookup[item["doc_id"]] = max(scores_lookup.get(item["doc_id"], 0.0), item["similarity_score"])

        if fusion_method == "max":
            fused = sorted(scores_lookup.items(), key=lambda pair: pair[1], reverse=True)[:top_k]
        else:
            fused_scores: dict[str, float] = {}
            for ranked_list in rankings:
                for rank, doc_id in enumerate(ranked_list):
                    fused_scores[doc_id] = fused_scores.get(doc_id, 0.0) + 1.0 / (60 + rank + 1)
            fused = sorted(fused_scores.items(), key=lambda pair: pair[1], reverse=True)[:top_k]

        documents = {doc["doc_id"]: doc for doc in self.store.list(collection)}
        results = []
        for doc_id, score in fused:
            doc = documents.get(doc_id)
            if not doc:
                continue
            results.append(
                SummaryResult(
                    doc_id=doc_id,
                    title=doc.get("title", ""),
                    summary=doc.get("summary", ""),
                    similarity_score=max(0.0, min(1.0, float(score))),
                    token_count=doc.get("token_count", 0),
                    tags=doc.get("tags", []),
                    collection=doc.get("collection", collection),
                )
            )

        response = SearchResponse(query="; ".join(queries), results=results, total_candidates=len(documents), search_time_ms=0.0)
        self._log(
            "multi_query_search",
            {"queries": queries, "top_k": top_k, "collection": collection},
            len(results),
            [result.doc_id for result in results],
            0.0,
        )
        return response.model_dump()

    def hybrid_search(
        self,
        query: str,
        top_k: int,
        collection: str,
        semantic_weight: float,
        keyword_weight: float,
    ) -> dict[str, Any]:
        semantic_results = self.search_summaries(
            query=query,
            top_k=top_k,
            collection=collection,
            min_score=self.settings.retrieval.min_similarity_score,
            tags_filter=None,
        )["results"]
        semantic_scores = {item["doc_id"]: item["similarity_score"] for item in semantic_results}
        bm25 = self._bm25_for(collection)
        bm25_scores = dict(bm25.score(query))

        # Normalise weights and scores to keep similarity_score within [0, 1].
        # Vector similarity is expected to already be in [0, 1], but we clamp defensively.
        semantic_w = max(0.0, float(semantic_weight))
        keyword_w = max(0.0, float(keyword_weight))
        weight_sum = semantic_w + keyword_w
        if weight_sum <= 0.0:
            semantic_w, keyword_w, weight_sum = 1.0, 0.0, 1.0
        semantic_w /= weight_sum
        keyword_w /= weight_sum

        max_bm25 = max(bm25_scores.values(), default=0.0)
        bm25_norm = {
            doc_id: (score / max_bm25 if max_bm25 > 0.0 else 0.0)
            for doc_id, score in bm25_scores.items()
        }

        combined_scores: dict[str, float] = {}
        for doc_id in set(semantic_scores) | set(bm25_norm):
            sem = float(semantic_scores.get(doc_id, 0.0))
            sem = 0.0 if sem < 0.0 else (1.0 if sem > 1.0 else sem)
            kw = float(bm25_norm.get(doc_id, 0.0))
            kw = 0.0 if kw < 0.0 else (1.0 if kw > 1.0 else kw)
            combined_scores[doc_id] = (semantic_w * sem) + (keyword_w * kw)

        ranked = sorted(combined_scores.items(), key=lambda pair: pair[1], reverse=True)[:top_k]
        documents = {doc["doc_id"]: doc for doc in self.store.list(collection)}
        results = []
        for doc_id, score in ranked:
            doc = documents.get(doc_id)
            if not doc:
                continue
            results.append(
                SummaryResult(
                    doc_id=doc_id,
                    title=doc.get("title", ""),
                    summary=doc.get("summary", ""),
                    similarity_score=float(score),
                    token_count=doc.get("token_count", 0),
                    tags=doc.get("tags", []),
                    collection=doc.get("collection", collection),
                )
            )

        response = SearchResponse(query=query, results=results, total_candidates=len(documents), search_time_ms=0.0)
        self._log(
            "hybrid_search",
            {"query": query, "top_k": top_k, "collection": collection},
            len(results),
            [result.doc_id for result in results],
            0.0,
        )
        return response.model_dump()

    def delete_document(self, doc_id: str, collection: str) -> dict[str, Any]:
        deleted = self.store.delete(collection, doc_id)
        self._index_for(collection).delete(doc_id)
        self._rebuild_bm25(collection)
        self._log(
            "delete_document",
            {"doc_id": doc_id, "collection": collection},
            1 if deleted else 0,
            [doc_id] if deleted else [],
            0.0,
        )
        return {"doc_id": doc_id, "deleted": bool(deleted)}

    def update_document(
        self,
        doc_id: str,
        collection: str,
        text: str | None,
        title: str | None,
        tags: list[str] | None,
        metadata: dict[str, Any] | None,
        summary: str | None,
    ) -> dict[str, Any]:
        doc = self.store.get(collection, doc_id)
        if not doc:
            return {"error": "Document not found"}

        from datetime import datetime, timezone
        doc["updated_at"] = datetime.now(timezone.utc).isoformat()

        if title is not None:
            doc["title"] = title
        if tags is not None:
            doc["tags"] = tags
        if metadata is not None:
            doc["metadata"] = {**doc.get("metadata", {}), **metadata}

        if text is not None:
            doc["full_text"] = text
            doc["token_count"] = count_tokens(text)
            chunk_metadata = self.chunker.chunk(
                text,
                self.settings.chunking.chunk_size,
                self.settings.chunking.chunk_overlap,
                self.settings.chunking.min_chunk_size,
            )
            doc["chunks"] = chunk_metadata
            doc["summary"] = summary or (self.summarizer.summarize(text) if self.settings.ingestion.auto_summary else "")
            embedding = self.embedding.encode([doc["summary"]])[0] if doc["summary"] else self.embedding.encode([doc["title"]])[0]
            self._index_for(collection).upsert(doc_id, embedding)
            self._rebuild_bm25(collection)
        elif summary is not None:
            doc["summary"] = summary
            embedding = self.embedding.encode([summary])[0]
            self._index_for(collection).upsert(doc_id, embedding)

        self.store.save(collection, doc)
        self._log(
            "update_document",
            {"doc_id": doc_id, "collection": collection},
            1,
            [doc_id],
            0.0,
        )
        return {"doc_id": doc_id, "status": "updated"}

    def collection_stats(self, collection: str) -> dict[str, Any]:
        documents = self.store.list(collection)
        if not documents:
            stats = {
                "collection": collection,
                "document_count": 0,
                "total_tokens": 0,
                "avg_tokens_per_doc": 0.0,
                "total_chunks": 0,
                "tag_distribution": {},
                "source_distribution": {},
                "oldest_document": None,
                "newest_document": None,
                "index_size_bytes": 0,
            }
            self._log("collection_stats", {"collection": collection}, 0, [], 0.0)
            return stats

        total_tokens = sum(doc.get("token_count", 0) for doc in documents)
        total_chunks = sum(len(doc.get("chunks", [])) for doc in documents)
        tag_distribution: dict[str, int] = {}
        source_distribution: dict[str, int] = {}
        for doc in documents:
            for tag in doc.get("tags", []):
                tag_distribution[tag] = tag_distribution.get(tag, 0) + 1
            source = doc.get("source", "unknown")
            source_distribution[source] = source_distribution.get(source, 0) + 1

        index_path = self.settings.storage.index_dir / f"{collection}.npz"
        index_size = index_path.stat().st_size if index_path.exists() else 0

        stats = {
            "collection": collection,
            "document_count": len(documents),
            "total_tokens": total_tokens,
            "avg_tokens_per_doc": total_tokens / len(documents),
            "total_chunks": total_chunks,
            "tag_distribution": tag_distribution,
            "source_distribution": source_distribution,
            "oldest_document": min(doc.get("created_at", "") for doc in documents),
            "newest_document": max(doc.get("created_at", "") for doc in documents),
            "index_size_bytes": index_size,
        }
        self._log("collection_stats", {"collection": collection}, len(documents), [doc["doc_id"] for doc in documents], 0.0)
        return stats

    def list_collections(self) -> dict[str, Any]:
        collections = []
        for path in self.settings.storage.store_dir.glob("*.json"):
            name = path.stem
            stats = self.collection_stats(name)
            collections.append(
                {
                    "name": name,
                    "document_count": stats["document_count"],
                    "total_tokens": stats["total_tokens"],
                    "description": "",
                }
            )
        if not collections:
            collections.append({"name": self.settings.retrieval.default_collection, "document_count": 0, "total_tokens": 0, "description": ""})
        payload = {"collections": collections}
        self._log("list_collections", {}, len(collections), [item["name"] for item in collections], 0.0)
        return payload

    def explain_retrieval(self, query: str, doc_ids: list[str], collection: str) -> dict[str, Any]:
        query_vector = self.embedding.encode([query])[0]
        explanations = []
        for doc_id in doc_ids:
            doc = self.store.get(collection, doc_id)
            if not doc:
                continue
            doc_vector = self.embedding.encode([doc.get("summary", "")])[0]
            cosine_similarity = sum(a * b for a, b in zip(query_vector, doc_vector))
            bm25_scores = dict(self._bm25_for(collection).score(query))
            bm25_score = bm25_scores.get(doc_id, 0.0)
            query_terms = set(query.lower().split())
            doc_terms = set(doc.get("summary", "").lower().split())
            overlap = len(query_terms & doc_terms)
            overlap_ratio = overlap / max(1, len(query_terms))
            explanations.append(
                {
                    "doc_id": doc_id,
                    "title": doc.get("title", ""),
                    "cosine_similarity": float(cosine_similarity),
                    "bm25_score": float(bm25_score),
                    "top_matching_terms": query.lower().split()[:5],
                    "query_doc_term_overlap": float(overlap_ratio),
                    "explanation_text": "Combined semantic and keyword scores to rank this document.",
                }
            )
        payload = {"query": query, "explanations": explanations}
        self._log("explain_retrieval", {"query": query, "doc_ids": doc_ids}, len(explanations), doc_ids, 0.0)
        return payload

    def retrieval_log(self, last_n: int, tool_filter: str | None, session_id: str | None) -> dict[str, Any]:
        entries = self.audit.read(last_n, tool_filter=tool_filter, session_id=session_id)
        payload = {"entries": entries, "total_entries": len(entries)}
        self._log("retrieval_log", {"last_n": last_n, "tool_filter": tool_filter}, len(entries), [], 0.0)
        return payload


def _read_api_key() -> str | None:
    import os

    return os.getenv("GEMINI_API_KEY")


_service: RAGService | None = None


def get_service() -> RAGService:
    global _service
    if _service is None:
        _service = RAGService(load_settings())
    return _service


# ---------------------------------------------------------------------------
# Knowledge-base manager singleton
# ---------------------------------------------------------------------------
from staged_rag.core.kb_manager import KnowledgeBaseManager as _KBManager

_kb_manager: _KBManager | None = None


def get_kb_manager() -> _KBManager | None:
    """Return the active KB manager (if knowledge_base is enabled)."""
    return _kb_manager


def start_kb_manager(settings=None) -> _KBManager | None:
    """Initialise and start the knowledge-base watcher.

    Returns the manager instance, or ``None`` if KB is disabled.
    """
    global _kb_manager
    if _kb_manager is not None and _kb_manager.is_running:
        return _kb_manager

    if settings is None:
        settings = get_service().settings

    kb_cfg = settings.knowledge_base
    if not kb_cfg.enabled:
        return None

    _kb_manager = _KBManager(
        kb_dir=kb_cfg.kb_dir,
        manifest_path=kb_cfg.manifest_file,
        collection=kb_cfg.collection,
        poll_interval=kb_cfg.poll_interval,
        max_file_size=kb_cfg.max_file_size,
        auto_summary=settings.ingestion.auto_summary,
    )
    _kb_manager.start()
    return _kb_manager


def stop_kb_manager() -> None:
    """Stop the knowledge-base watcher."""
    global _kb_manager
    if _kb_manager is not None:
        _kb_manager.stop()
        _kb_manager = None
