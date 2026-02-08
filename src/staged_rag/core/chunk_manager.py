from __future__ import annotations

from staged_rag.utils import chunk_text, count_tokens


class ChunkManager:
    """Split long text into chunk metadata using sentence boundaries."""

    def chunk(self, text: str, chunk_size: int, overlap: int, min_chunk_size: int) -> list[dict]:
        chunks = chunk_text(text, chunk_size, overlap, min_chunk_size)
        chunk_metadata: list[dict] = []
        cursor = 0
        for idx, chunk in enumerate(chunks):
            start = text.find(chunk, cursor)
            end = start + len(chunk) if start >= 0 else cursor + len(chunk)
            cursor = max(end, cursor)
            chunk_metadata.append(
                {
                    "chunk_index": idx,
                    "text": chunk,
                    "token_count": count_tokens(chunk),
                    "start_char": max(start, 0),
                    "end_char": max(end, 0),
                }
            )
        return chunk_metadata
