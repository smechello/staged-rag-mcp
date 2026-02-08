"""Inspect store and index contents."""
import json
import os
import numpy as np

os.chdir("d:/Python/MCP_RAG/staged-rag-mcp")

# Store
with open("data/store/default.json") as f:
    docs = json.load(f)
print(f"Total docs in store: {len(docs)}")
for doc_id, d in docs.items():
    title = d.get("title", "?")[:60]
    print(f"  {doc_id[:12]}... | {title}")

# Index
idx_path = "data/index/default.npz"
if os.path.exists(idx_path):
    data = np.load(idx_path, allow_pickle=True)
    print(f"\nTotal vectors in index: {len(data['doc_ids'])}")
    for did in data["doc_ids"]:
        print(f"  {str(did)[:12]}...")
else:
    print("\nNo index file")
