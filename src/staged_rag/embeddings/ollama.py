"""Ollama embedding provider for local models.

Requires a running Ollama server (default ``http://localhost:11434``).
"""
from __future__ import annotations

from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from ollama import Client
except ImportError:
    raise ImportError(
        "The 'ollama' library is required for the Ollama embedder. "
        "Install it with: pip install ollama"
    )


class OllamaEmbedding(EmbeddingBase):
    """Ollama local-model embedding provider."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "nomic-embed-text"
        self.config.embedding_dims = self.config.embedding_dims or 768

        self.client = Client(host=self.config.ollama_base_url)
        self._ensure_model_exists()

    def _ensure_model_exists(self) -> None:
        """Pull the model from Ollama registry if not available locally."""
        local_models = self.client.list().get("models", [])
        if not any(
            m.get("name") == self.config.model or m.get("model") == self.config.model
            for m in local_models
        ):
            self.client.pull(self.config.model)

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using Ollama."""
        response = self.client.embeddings(
            model=self.config.model,
            prompt=text,
        )
        return response["embedding"]
