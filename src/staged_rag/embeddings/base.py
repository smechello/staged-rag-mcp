"""Abstract base class for all embedding providers.

Inspired by mem0ai/mem0's EmbeddingBase pattern.
Every provider must implement the ``embed`` method that converts a single
text string into a fixed-dimension float vector.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from staged_rag.embeddings.configs import BaseEmbedderConfig


class EmbeddingBase(ABC):
    """Base class for embedding providers.

    :param config: Embedding configuration, defaults to None
    :type config: Optional[BaseEmbedderConfig], optional
    """

    def __init__(self, config: Optional[BaseEmbedderConfig] = None) -> None:
        if config is None:
            self.config = BaseEmbedderConfig()
        else:
            self.config = config

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return the embedding vector for *text*.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        ...
