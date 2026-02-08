"""HuggingFace embedding provider.

Supports both local ``sentence-transformers`` models and the HuggingFace
Inference API (when ``huggingface_base_url`` is set).
"""
from __future__ import annotations

import os
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from openai import OpenAI  # HF Inference API is OpenAI-compatible
except ImportError:
    OpenAI = None  # type: ignore[assignment,misc]

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None  # type: ignore[assignment,misc]


class HuggingFaceEmbedding(EmbeddingBase):
    """HuggingFace embedding provider (local or API)."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "all-MiniLM-L6-v2"
        self.config.embedding_dims = self.config.embedding_dims or 384

        if self.config.huggingface_base_url:
            # Use the HuggingFace Inference API via OpenAI-compatible client
            if OpenAI is None:
                raise ImportError(
                    "'openai' package is required for HuggingFace Inference API. "
                    "Install with: pip install openai"
                )
            api_key = self.config.api_key or os.getenv("HUGGINGFACE_API_KEY") or "hf_dummy"
            self.client = OpenAI(
                api_key=api_key,
                base_url=self.config.huggingface_base_url,
            )
            self._local_model = None
        else:
            # Use local sentence-transformers
            if SentenceTransformer is None:
                raise ImportError(
                    "'sentence-transformers' package is required for local HuggingFace embeddings. "
                    "Install with: pip install sentence-transformers"
                )
            self._local_model = SentenceTransformer(
                self.config.model,
                **(self.config.model_kwargs or {}),
            )
            self.client = None  # type: ignore[assignment]

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using HuggingFace."""
        if self.client is not None and self.config.huggingface_base_url:
            # Remote inference API
            response = self.client.embeddings.create(
                input=text,
                model=self.config.model,
                **(self.config.model_kwargs or {}),
            )
            return response.data[0].embedding
        else:
            # Local sentence-transformers
            return self._local_model.encode(text, convert_to_numpy=True).tolist()
