"""Azure OpenAI embedding provider."""
from __future__ import annotations

import os
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

try:
    from openai import AzureOpenAI
except ImportError:
    raise ImportError(
        "The 'openai' library is required for the Azure OpenAI embedder. "
        "Install it with: pip install openai"
    )


class AzureOpenAIEmbedding(EmbeddingBase):
    """Azure OpenAI embedding provider."""

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        super().__init__(config)

        self.config.model = self.config.model or "text-embedding-3-small"
        self.config.embedding_dims = self.config.embedding_dims or 1536

        azure_kwargs = self.config.azure_kwargs or {}
        api_key = azure_kwargs.get("api_key") or os.getenv("EMBEDDING_AZURE_OPENAI_API_KEY")
        azure_deployment = azure_kwargs.get("azure_deployment") or os.getenv("EMBEDDING_AZURE_DEPLOYMENT")
        azure_endpoint = azure_kwargs.get("azure_endpoint") or os.getenv("EMBEDDING_AZURE_ENDPOINT")
        api_version = azure_kwargs.get("api_version") or os.getenv("EMBEDDING_AZURE_API_VERSION")

        self.client = AzureOpenAI(
            azure_deployment=azure_deployment,
            azure_endpoint=azure_endpoint,
            api_version=api_version,
            api_key=api_key,
        )

    def embed(self, text: str) -> list[float]:
        """Get embedding for *text* using Azure OpenAI."""
        text = text.replace("\n", " ")
        return self.client.embeddings.create(
            input=[text],
            model=self.config.model,
        ).data[0].embedding
