from __future__ import annotations

import json
from pathlib import Path

from staged_rag.tools import ingest_batch

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "mock" / "documents.json"


def main() -> None:
    """Seed the document store with mock documents."""
    documents = json.loads(DATA_PATH.read_text())
    payloads = []
    for doc in documents:
        payloads.append(
            {
                "title": doc["title"],
                "text": doc["full_text"],
                "source": doc.get("source", "mock"),
                "tags": doc.get("tags", []),
                "metadata": doc.get("metadata", {}),
                "summary": doc.get("summary"),
            }
        )
    result = ingest_batch(payloads, collection="default")
    print(f"Seeded {result['succeeded']} documents.")


if __name__ == "__main__":
    main()
