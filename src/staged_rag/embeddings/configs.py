"""Embedding configuration models.

* ``BaseEmbedderConfig`` – provider-agnostic config carrying model name, API key,
  dimensions and provider-specific knobs.
* ``EmbedderConfig`` – a Pydantic model used for YAML/dict-based provider
  selection and validation.

Inspired by mem0ai/mem0's ``BaseEmbedderConfig`` and ``EmbedderConfig``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Provider-agnostic embedding configuration
# ---------------------------------------------------------------------------

@dataclass
class BaseEmbedderConfig:
    """Carrier for all provider-agnostic *and* provider-specific knobs.

    Not every field is used by every provider – unused fields are simply
    ignored by the concrete implementation.
    """

    # Common
    model: Optional[str] = None
    api_key: Optional[str] = None
    embedding_dims: Optional[int] = None

    # Ollama specific
    ollama_base_url: Optional[str] = None

    # OpenAI / LM-Studio / Together specific
    openai_base_url: Optional[str] = None

    # HuggingFace specific
    model_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)
    huggingface_base_url: Optional[str] = None

    # Azure OpenAI specific
    azure_kwargs: Optional[Dict[str, Any]] = field(default_factory=dict)
    http_client_proxies: Optional[str] = None

    # Gemini specific
    output_dimensionality: Optional[int] = None


# ---------------------------------------------------------------------------
# Provider selection + validation (used when loading from YAML / dict)
# ---------------------------------------------------------------------------

SUPPORTED_PROVIDERS = (
    "gemini",
    "openai",
    "ollama",
    "huggingface",
    "azure_openai",
    "together",
    "lmstudio",
)


class EmbedderConfig(BaseModel):
    """Pydantic model for selecting and validating embedding providers."""

    provider: str = Field(
        description="Provider of the embedding model (e.g., 'gemini', 'openai', 'ollama')",
        default="gemini",
    )
    config: Optional[dict] = Field(
        description="Configuration dict for the specific embedding model",
        default_factory=dict,
    )

    @field_validator("config")
    @classmethod
    def validate_config(cls, v: dict | None, info) -> dict | None:  # noqa: N805
        provider = info.data.get("provider")
        if provider not in SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported embedding provider: {provider!r}. "
                f"Choose from: {', '.join(SUPPORTED_PROVIDERS)}"
            )
        return v
