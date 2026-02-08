"""Embedding provider factory with lazy imports.

Follows the mem0 ``EmbedderFactory`` pattern: a class-level mapping from
provider name → fully-qualified class path.  ``load_class()`` uses
``importlib`` for lazy loading so optional dependencies (openai, ollama,
together, etc.) are only imported when actually selected.
"""
from __future__ import annotations

import importlib
import logging
from typing import Optional

from staged_rag.embeddings.base import EmbeddingBase
from staged_rag.embeddings.configs import BaseEmbedderConfig

logger = logging.getLogger(__name__)


def load_class(class_path: str) -> type:
    """Dynamically import a class from its fully-qualified dotted path.

    Example::

        cls = load_class("staged_rag.embeddings.openai.OpenAIEmbedding")
        instance = cls(config)
    """
    module_path, class_name = class_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, class_name)


class EmbedderFactory:
    """Create embedding providers by name with lazy imports.

    Usage::

        provider = EmbedderFactory.create("gemini", {"api_key": "...", "model": "gemini-embedding-001"})
        vector = provider.embed("Hello world")
    """

    provider_to_class: dict[str, str] = {
        "gemini": "staged_rag.embeddings.gemini.GeminiEmbedding",
        "openai": "staged_rag.embeddings.openai.OpenAIEmbedding",
        "ollama": "staged_rag.embeddings.ollama.OllamaEmbedding",
        "huggingface": "staged_rag.embeddings.huggingface.HuggingFaceEmbedding",
        "azure_openai": "staged_rag.embeddings.azure_openai.AzureOpenAIEmbedding",
        "together": "staged_rag.embeddings.together.TogetherEmbedding",
        "lmstudio": "staged_rag.embeddings.lmstudio.LMStudioEmbedding",
    }

    @classmethod
    def create(
        cls,
        provider_name: str,
        config: Optional[dict] = None,
    ) -> EmbeddingBase:
        """Instantiate an embedding provider.

        Args:
            provider_name: One of the registered provider keys
                           (gemini, openai, ollama, huggingface, azure_openai, together, lmstudio).
            config: Optional dict of config values passed to ``BaseEmbedderConfig``.

        Returns:
            An ``EmbeddingBase`` subclass instance ready to call ``.embed(text)``.

        Raises:
            ValueError: If provider_name is not registered.
        """
        class_path = cls.provider_to_class.get(provider_name)
        if class_path is None:
            supported = ", ".join(sorted(cls.provider_to_class.keys()))
            raise ValueError(
                f"Unsupported embedding provider: {provider_name!r}. "
                f"Supported providers: {supported}"
            )

        logger.info("Loading embedding provider %r from %s", provider_name, class_path)
        embedder_cls = load_class(class_path)

        # Build config object from dict
        base_config = BaseEmbedderConfig(**(config or {}))
        return embedder_cls(base_config)

    @classmethod
    def list_providers(cls) -> list[str]:
        """Return sorted list of supported provider names."""
        return sorted(cls.provider_to_class.keys())
