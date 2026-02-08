"""Seed mock data + test search ranking with real Gemini embeddings."""
import os, sys, json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from staged_rag.config import load_settings
from staged_rag.service import RAGService

cfg = load_settings()
svc = RAGService(cfg)

# --- Seed mock data ---
mock_path = os.path.join("data", "mock", "documents.json")
with open(mock_path) as f:
    docs = json.load(f)

print("=== Seeding mock data ===")
for doc in docs:
    result = svc.ingest_document(
        title=doc["title"],
        text=doc["full_text"],
        source=doc.get("source", "mock"),
        tags=doc.get("tags", []),
        metadata=doc.get("metadata", {}),
        summary=doc.get("summary"),
        collection="default",
    )
    print(f"  Ingested: {doc['title']} -> {result.get('doc_id', '?')[:12]}...")

# --- List all docs with summaries ---
print(f"\n=== All documents ===")
for d in svc.store.list("default"):
    did = d["doc_id"][:12]
    title = d.get("title", "?")[:55]
    summary = d.get("summary", "")[:100].replace("\n", " ")
    print(f"  {did}... | {title}")
    print(f"    Summary: {summary}")
    print()

# --- Search tests ---
queries = [
    "humanitarian data sharing donors",
    "flood risk Somalia exposure",
    "somatosensory nervous system anatomy",
    "staged retrieval pipeline architecture",
    "MCP tool contracts governance",
]

for q in queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {q}")
    print(f"{'='*60}")
    resp = svc.search_summaries(q, top_k=5, collection="default", min_score=0.0, tags_filter=None)
    for i, r in enumerate(resp["results"], 1):
        score = r["similarity_score"]
        title = r["title"][:50]
        print(f"  {i}. [{score:.4f}] {title}")
