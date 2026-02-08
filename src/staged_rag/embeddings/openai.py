"""OpenAI embedding provider.

Supports OpenAI-compatible APIs (OpenAI, Azure via base_url, LM Studio, etc.).
"""
from __future__ import annotations

import os
import warnings
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from openai import OpenAI
except ImportError:
    raise ImportError(
        "The 'openai' library is required for the OpenAI embedder. "
        "Install it with: pip install openai"
    )


class OpenAIEmbedding(EmbeddingBase):
    """OpenAI text embedding provider."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "text-embedding-3-small"
        self.config.embedding_dims = self.config.embedding_dims or 1536

        api_key = self.config.api_key or os.getenv("OPENAI_API_KEY")
        base_url = (
            self.config.openai_base_url
            or os.getenv("OPENAI_BASE_URL")
            or "https://api.openai.com/v1"
        )

        if os.environ.get("OPENAI_API_BASE"):
            warnings.warn(
                "The environment variable 'OPENAI_API_BASE' is deprecated. "
                "Please use 'OPENAI_BASE_URL' instead.",
                DeprecationWarning,
                stacklevel=2,
            )
            base_url = base_url or os.environ["OPENAI_API_BASE"]

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using OpenAI."""
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(
            input=[text],
            model=self.config.model,
            dimensions=self.config.embedding_dims,
        )
        return response.data[0].embedding
