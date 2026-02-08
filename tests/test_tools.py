from staged_rag.tools import ingest_document, list_collections, search_summaries


def test_tools_can_be_imported() -> None:
    response = search_summaries("query")
    assert isinstance(response, dict)
    assert callable(ingest_document)
    collections = list_collections()
    assert "collections" in collections
