from __future__ import annotations

import logging

from staged_rag.utils import extract_key_sentences, split_sentences

try:
    from google import genai
except ImportError:  # pragma: no cover
    genai = None

logger = logging.getLogger(__name__)


def _is_rate_limit_error(exc: Exception) -> bool:
    """Return True if *exc* looks like a Gemini rate-limit (429) error."""
    msg = str(exc).lower()
    type_name = type(exc).__name__.lower()
    return (
        "429" in msg
        or "resource exhausted" in msg
        or "rate limit" in msg
        or "quota" in msg
        or "too many requests" in msg
        or "resourceexhausted" in type_name
        or "toomanyrequests" in type_name
    )


class SummaryGenerator:
    """Generate short summaries using Gemini with a local fallback.

    Uses the new ``google.genai`` SDK (replaces deprecated ``google.generativeai``).
    The SDK has built-in tenacity retry.  This class tries once and falls back
    to a high-quality extractive summary if the API call fails, so the server
    never blocks for minutes due to exhausted free-tier quotas.
    """

    def __init__(self, api_key: str | None, model_name: str, max_sentences: int) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.max_sentences = max_sentences

    def _local_fallback(self, text: str) -> str:
        """Extract the most informative sentences as an extractive summary.

        Cleans PDF noise, skips formatting artefacts, and picks substantive
        sentences from the beginning of the document.
        """
        return extract_key_sentences(text, max_sentences=self.max_sentences)

    def summarize(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        if not genai or not self.api_key:
            return self._local_fallback(text)

        prompt = (
            "Summarize the following document in 2-4 sentences, focusing on the key facts and intent.\n\n"
            f"DOCUMENT:\n{text}\n"
        )
        from staged_rag.core.embeddings import _get_genai_client
        client = _get_genai_client(self.api_key)
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return str(response.text).strip()
        except Exception as exc:
            logger.warning(
                "Summary generation failed, using local fallback: %s", exc,
            )
            return self._local_fallback(text)
