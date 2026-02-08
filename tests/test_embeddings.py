from staged_rag.core.embeddings import EmbeddingEngine


def test_embedding_engine_returns_vectors() -> None:
    """EmbeddingEngine falls back to deterministic vectors when no API key is set."""
    engine = EmbeddingEngine(
        provider="gemini",
        api_key=None,
        model_name="gemini-embedding-001",
        dimension=16,
    )
    vectors = engine.encode(["hello", "world"])
    assert len(vectors) == 2
    assert all(len(vec) == engine.dimension for vec in vectors)


def test_embedding_factory_list_providers() -> None:
    """The factory should list all supported providers."""
    from staged_rag.embeddings import EmbedderFactory

    providers = EmbedderFactory.list_providers()
    assert "gemini" in providers
    assert "openai" in providers
    assert "ollama" in providers
    assert len(providers) >= 5
