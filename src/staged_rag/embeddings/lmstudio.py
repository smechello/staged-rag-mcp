"""LM Studio embedding provider.

LM Studio exposes an OpenAI-compatible API on localhost.
"""
from __future__ import annotations

from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "The 'openai' library is required for the LM Studio embedder. "
        "Install it with: pip install openai"
    )


class LMStudioEmbedding(EmbeddingBase):
    """LM Studio local embedding provider (OpenAI-compatible)."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "text-embedding-nomic-embed-text-v1.5"
        self.config.embedding_dims = self.config.embedding_dims or 768

        base_url = self.config.openai_base_url or "http://localhost:1234/v1"
        self.client = OpenAI(api_key="lm-studio", base_url=base_url)

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using LM Studio."""
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(
            input=[text],
            model=self.config.model,
        )
        return response.data[0].embedding
