"""Google Gemini embedding provider.

Uses the ``google-genai`` SDK (the modern replacement for ``google.generativeai``).
"""
from __future__ import annotations

import os
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError(
        "The 'google-genai' library is required for the Gemini embedder. "
        "Install it with: pip install google-genai"
    )


class GeminiEmbedding(EmbeddingBase):
    """Google Gemini embedding provider."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "gemini-embedding-001"
        self.config.embedding_dims = (
            self.config.embedding_dims
            or self.config.output_dimensionality
            or 3072
        )

        api_key = self.config.api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using Google Gemini."""
        text = text.replace("\n", " ")
        cfg = types.EmbedContentConfig(
            output_dimensionality=self.config.embedding_dims,
        )
        response = self.client.models.embed_content(
            model=self.config.model,
            contents=text,
            config=cfg,
        )
        return list(response.embeddings[0].values)
