"""Together AI embedding provider."""
from __future__ import annotations

import os
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from together import Together
except ImportError:
    raise ImportError(
        "The 'together' library is required for the Together AI embedder. "
        "Install it with: pip install together"
    )


class TogetherEmbedding(EmbeddingBase):
    """Together AI embedding provider."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "togethercomputer/m2-bert-80M-8k-retrieval"
        self.config.embedding_dims = self.config.embedding_dims or 768

        api_key = self.config.api_key or os.getenv("TOGETHER_API_KEY")
        self.client = Together(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using Together AI."""
        text = text.replace("\n", " ")
        return self.client.embeddings.create(
            model=self.config.model,
            input=text,
        ).data[0].embedding
