"""Multi-provider embedding package.

Provides a pluggable embedding system inspired by mem0ai/mem0:

* **Base class** – ``EmbeddingBase`` (abstract, all providers inherit from it)
* **Config** – ``BaseEmbedderConfig`` (provider-agnostic config dataclass)
* **Factory** – ``EmbedderFactory`` (lazy-import factory mapping provider
  names to implementation classes)
* **Providers** – Gemini, OpenAI, Ollama, HuggingFace, Azure OpenAI,
  Together, LM Studio

Usage::

    from staged_rag.embeddings import EmbedderFactory, BaseEmbedderConfig

    embedder = EmbedderFactory.create("gemini", {
        "api_key": "...",
        "model": "gemini-embedding-001",
        "embedding_dims": 3072,
    })
    vector = embedder.embed("Hello, world!")
"""
from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig, EmbedderConfig
from staged_rag.embeddings.factory import EmbedderFactory

__all__ = [
    "EmbeddingBase",
    "BaseEmbedderConfig",
    "EmbedderConfig",
    "EmbedderFactory",
]
