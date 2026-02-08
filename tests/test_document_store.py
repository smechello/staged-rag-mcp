from staged_rag.core.document_store import DocumentStore


def test_document_store_save_and_get(tmp_path) -> None:
    store = DocumentStore(tmp_path)
    document = {"doc_id": "test", "title": "Demo"}
    store.save("default", document)
    assert store.get("default", "test") == document
