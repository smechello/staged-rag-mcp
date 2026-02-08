from __future__ import annotations

import hashlib
import math
import re
from typing import Iterable

import numpy as np

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")

# Patterns for cleaning noisy PDF-extracted text
_PAGE_HEADER = re.compile(r"^\s*\d+\s*$", re.MULTILINE)  # standalone page numbers
_MULTI_NEWLINE = re.compile(r"\n{3,}")
_MULTI_SPACE = re.compile(r"[ \t]{3,}")
_FOOTNOTE_REF = re.compile(r"(?<!\d)\d{1,2}\s{2,}")  # footnote superscript references
# Split camelCase / PascalCase runs that PDF extraction jams together
_CAMELCASE = re.compile(r"([a-z])([A-Z])")
_UPPERCASE_RUN = re.compile(r"([A-Z]+)([A-Z][a-z])")
# Split letters→digits and digits→letters: "for2024" → "for 2024"
_LETTER_DIGIT = re.compile(r"([a-zA-Z])(\d)")
_DIGIT_LETTER = re.compile(r"(\d)([a-zA-Z])")


def count_tokens(text: str) -> int:
    return max(1, len(text.split()))


def _split_joined_words(text: str) -> str:
    """Insert spaces into CamelCase / PascalCase runs and letter-digit junctions.

    PDF extractors often jam words together:
      'SomaliaFloodExposure' → 'Somalia Flood Exposure'
      'for2024HNRP'          → 'for 2024 HNRP'
    """
    text = _CAMELCASE.sub(r"\1 \2", text)
    text = _UPPERCASE_RUN.sub(r"\1 \2", text)
    text = _LETTER_DIGIT.sub(r"\1 \2", text)
    text = _DIGIT_LETTER.sub(r"\1 \2", text)
    return text


def clean_text(text: str) -> str:
    """Clean noisy text (especially PDF-extracted) for better summarisation.

    - Splits CamelCase/joined words
    - Removes standalone page numbers
    - Normalises excessive whitespace / newlines
    - Strips leading/trailing junk per line
    - Collapses runs of whitespace
    """
    # Split joined CamelCase words from PDF extraction
    text = _split_joined_words(text)
    # Remove standalone page-number lines
    text = _PAGE_HEADER.sub("", text)
    # Collapse excessive newlines
    text = _MULTI_NEWLINE.sub("\n\n", text)
    # Collapse runs of spaces/tabs
    text = _MULTI_SPACE.sub(" ", text)
    # Clean up each line
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        # Skip very short lines that are likely headers/footers/artefacts
        # but keep them if they look like headings (start with uppercase and > 3 chars)
        if len(stripped) < 4 and not stripped.isupper():
            continue
        lines.append(stripped)
    return "\n".join(lines).strip()


def split_sentences(text: str) -> list[str]:
    """Split text into sentences at sentence-ending punctuation.

    Handles multi-line text by first joining lines into paragraphs.
    """
    # Join lines within paragraphs (single newlines) but respect paragraph breaks
    joined = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    sentences = [part.strip() for part in SENTENCE_SPLIT.split(joined) if part.strip()]
    return sentences or [text.strip()]


def extract_key_sentences(text: str, max_sentences: int = 4, min_word_count: int = 8) -> str:
    """Extract the most informative sentences for a summary.

    Strategy:
    1. Clean the text
    2. Split into sentences
    3. Skip noise (too short, just numbers, formatting artefacts, org headers)
    4. Prefer sentences from the beginning (they usually state the topic)
    5. Return up to *max_sentences* substantive sentences
    """
    cleaned = clean_text(text)
    sentences = split_sentences(cleaned)

    substantive: list[str] = []
    for sent in sentences:
        # Skip very short sentences (likely noise)
        words = sent.split()
        if len(words) < min_word_count:
            continue
        # Skip sentences that are mostly numbers or special characters
        alpha_ratio = sum(1 for c in sent if c.isalpha()) / max(1, len(sent))
        if alpha_ratio < 0.5:
            continue
        # Skip header-like lines: all-caps org names, dates, etc.
        upper_ratio = sum(1 for c in sent if c.isupper()) / max(1, sum(1 for c in sent if c.isalpha()))
        # If more than 70% of letters are uppercase and it's short, skip — it's a header
        if upper_ratio > 0.70 and len(words) < 15:
            continue
        # Skip sentences that START with an all-caps header (e.g. "THE CENTRE FOR X ... actual content")
        # If the first 5+ words are ALL CAPS, this sentence likely starts with an org header
        first_words = words[:6]
        if len(first_words) >= 5 and all(w.isupper() or not w.isalpha() for w in first_words):
            # Try to salvage by stripping the header part
            # Find where normal-case text begins
            for i, w in enumerate(words):
                if w[0:1].isupper() and not w.isupper() and w.isalpha() and len(w) > 2:
                    salvaged = " ".join(words[i:])
                    if len(salvaged.split()) >= min_word_count:
                        sent = salvaged
                        break
                    else:
                        break
            else:
                continue
        # Skip boilerplate phrasing
        lower = sent.lower()
        if any(skip in lower for skip in [
            "this is a sample document",
            "page-based formatting",
            "showcase page",
            "none of the content has been changed",
        ]):
            continue
        # Skip lines that look like date-only: e.g. "DECEMBER 2020"
        if re.match(r"^[A-Z]+\s+\d{4}$", sent.strip()):
            continue
        substantive.append(sent)
        if len(substantive) >= max_sentences:
            break

    if not substantive:
        # Fallback: just take whatever we have
        fallback = [s.strip() for s in sentences if len(s.split()) >= 3][:max_sentences]
        return " ".join(fallback).strip()

    return " ".join(substantive).strip()


def chunk_text(text: str, chunk_size: int, overlap: int, min_chunk_size: int) -> list[str]:
    sentences = split_sentences(text)
    chunks: list[str] = []
    current: list[str] = []
    current_count = 0

    for sentence in sentences:
        token_count = count_tokens(sentence)
        if current_count + token_count > chunk_size and current:
            chunk_text_value = " ".join(current).strip()
            if count_tokens(chunk_text_value) >= min_chunk_size:
                chunks.append(chunk_text_value)
            overlap_tokens = " ".join(current).split()[-overlap:] if overlap > 0 else []
            current = [" ".join(overlap_tokens)] if overlap_tokens else []
            current_count = count_tokens(" ".join(current)) if current else 0
        current.append(sentence)
        current_count += token_count

    if current:
        chunk_text_value = " ".join(current).strip()
        if chunk_text_value:
            chunks.append(chunk_text_value)
    return chunks


def normalize_vectors(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


def deterministic_vector(text: str, dimension: int) -> list[float]:
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**32)
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dimension)
    norm = math.sqrt(float(np.dot(vector, vector))) or 1.0
    return (vector / norm).astype(float).tolist()
