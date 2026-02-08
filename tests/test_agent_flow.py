from staged_rag import server as staged_server


def test_server_has_expected_name() -> None:
    assert staged_server.server.name == "staged-rag"
