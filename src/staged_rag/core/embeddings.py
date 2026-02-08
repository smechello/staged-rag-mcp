from __future__ import annotations

import collections
import logging
import time
from typing import Iterable

from staged_rag.embeddings import EmbedderFactory, EmbeddingBase
from staged_rag.utils import deterministic_vector

try:
    from google import genai as _genai_module
except ImportError:  # pragma: no cover
    _genai_module = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# Singleton genai client for summary generator (cross-cutting concern)
_genai_client_instance = None


def _get_genai_client(api_key: str):
    """Return a singleton google.genai.Client for non-embedding uses (e.g. summaries)."""
    global _genai_client_instance
    if _genai_client_instance is None:
        if _genai_module is None:
            raise ImportError("google-genai is not installed")
        _genai_client_instance = _genai_module.Client(api_key=api_key)
    return _genai_client_instance

# Light retry
_MAX_RETRIES = 2
_RETRY_DELAY = 5  # seconds

# Rate-limiter: pace API requests at ~80 RPM to leave headroom for free tiers.
_RPM_LIMIT = 80
_RPM_WINDOW = 60  # seconds

_call_timestamps: collections.deque[float] = collections.deque()


def _pace_request() -> None:
    """Block if we've hit the per-minute request budget."""
    now = time.monotonic()
    while _call_timestamps and _call_timestamps[0] < now - _RPM_WINDOW:
        _call_timestamps.popleft()
    if len(_call_timestamps) >= _RPM_LIMIT:
        sleep_for = _call_timestamps[0] + _RPM_WINDOW - now + 0.1
        if sleep_for > 0:
            logger.info("Embedding rate-limiter: sleeping %.1fs", sleep_for)
            time.sleep(sleep_for)
    _call_timestamps.append(time.monotonic())


class EmbeddingEngine:
    """Multi-provider embedding engine with rate limiting and deterministic fallback.

    Wraps an ``EmbeddingBase`` provider (created via ``EmbedderFactory``) and
    adds:
    * Per-minute rate pacing (80 RPM default)
    * Light retry on transient failures
    * Deterministic vector fallback when the API is unavailable

    The engine is provider-agnostic — it delegates the actual embedding call
    to whichever provider is configured (Gemini, OpenAI, Ollama, etc.).
    """

    def __init__(
        self,
        provider: str = "gemini",
        api_key: str | None = None,
        model_name: str | None = None,
        dimension: int = 3072,
        provider_config: dict | None = None,
    ) -> None:
        self.provider_name = provider
        self.dimension = dimension

        # Build provider config dict from explicit args + extra config
        cfg: dict = dict(provider_config or {})
        if api_key:
            cfg.setdefault("api_key", api_key)
        if model_name:
            cfg.setdefault("model", model_name)
        if dimension:
            cfg.setdefault("embedding_dims", dimension)

        # Create the provider via factory (lazy import)
        try:
            self._provider: EmbeddingBase | None = EmbedderFactory.create(provider, cfg)
            logger.info(
                "Embedding engine initialised: provider=%s, model=%s, dims=%d",
                provider, self._provider.config.model, dimension,
            )
        except Exception as exc:
            logger.warning(
                "Failed to initialise %s embedding provider (%s) – "
                "will use deterministic fallback only",
                provider, exc,
            )
            self._provider = None

    @property
    def provider(self) -> EmbeddingBase | None:
        """The underlying embedding provider instance."""
        return self._provider

    def _embed_with_retry(self, text: str) -> list[float]:
        """Call the provider's embed() with a light retry on transient errors."""
        if self._provider is None:
            return deterministic_vector(text, self.dimension)

        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES):
            try:
                _pace_request()
                return self._provider.embed(text)
            except Exception as exc:
                last_exc = exc
                if attempt < _MAX_RETRIES - 1:
                    logger.warning(
                        "Embedding attempt %d/%d failed – retrying in %ds: %s",
                        attempt + 1, _MAX_RETRIES, _RETRY_DELAY, exc,
                    )
                    time.sleep(_RETRY_DELAY)

        logger.error(
            "Embedding failed after %d attempt(s), using deterministic fallback: %s",
            _MAX_RETRIES, last_exc,
        )
        return deterministic_vector(text, self.dimension)

    def encode(self, texts: Iterable[str]) -> list[list[float]]:
        """Return embedding vectors for a batch of texts.

        Uses the configured provider, falling back to deterministic vectors
        if the provider is unavailable or all API calls fail.
        """
        texts_list = list(texts)
        if not texts_list:
            return []

        if self._provider is None:
            return [deterministic_vector(t, self.dimension) for t in texts_list]

        return [self._embed_with_retry(t) for t in texts_list]
