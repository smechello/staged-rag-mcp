from staged_rag.core.vector_index import VectorIndex


def test_vector_index_upsert_and_search(tmp_path) -> None:
    index_path = tmp_path / "index.npz"
    index = VectorIndex(index_path)
    index.upsert("doc-1", [0.1, 0.2])
    index.upsert("doc-2", [0.3, 0.4])
    results = index.search([0.0, 0.0], top_k=1)
    assert results
