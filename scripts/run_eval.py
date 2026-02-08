from __future__ import annotations

from staged_rag.tools import search_summaries


def main() -> None:
    """Run a lightweight retrieval check on a small query set."""
    queries = [
        "staged retrieval",
        "MCP tool contracts",
    ]
    for query in queries:
        response = search_summaries(query, top_k=3)
        print(f"Query: {query}")
        for result in response.get("results", []):
            print(f"  - {result['doc_id']}: {result['title']} ({result['similarity_score']:.2f})")


if __name__ == "__main__":
    main()
