"""Quick test of search ranking with real Gemini embeddings."""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from staged_rag.config import load_settings
from staged_rag.service import RAGService

cfg = load_settings()
svc = RAGService(cfg)

queries = [
    "humanitarian data sharing donors",
    "flood risk Somalia",
    "somatosensory nervous system",
]

for q in queries:
    print(f"\n{'='*60}")
    print(f"QUERY: {q}")
    print(f"{'='*60}")
    resp = svc.search_summaries(q, top_k=5, collection="default", min_score=0.0, tags_filter=None)
    for i, r in enumerate(resp["results"], 1):
        print(f"  {i}. [{r['similarity_score']:.4f}] {r['title']}")
        summary = r["summary"][:120].replace("\n", " ")
        print(f"     {summary}...")
