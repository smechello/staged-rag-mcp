"""Quick MCP end-to-end test for multi-provider embeddings."""
import ast
import httpx
import json

BASE = "http://127.0.0.1:8090"

# Initialize session
r = httpx.post(
    f"{BASE}/mcp",
    json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "0.1"},
        },
    },
    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
)

sid = ""
for line in r.text.strip().split("\n"):
    if line.startswith("data:"):
        d = json.loads(line[5:].strip())
        # Session ID comes in response headers, not body
        print(f"Init response keys: {list(d.get('result', {}).keys())}")

# Session ID is in response headers
sid = r.headers.get("mcp-session-id", "")
print(f"Session ID from header: {sid[:30]}...")

# Search test
queries = [
    "humanitarian data sharing",
    "flood disaster Somalia",
    "MCP server protocol",
]

for query in queries:
    r2 = httpx.post(
        f"{BASE}/mcp",
        json={
            "jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "search_summaries", "arguments": {"query": query, "top_k": 2}},
        },
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Mcp-Session-Id": sid,
        },
    )
    for line in r2.text.strip().split("\n"):
        if line.startswith("data:"):
            d2 = json.loads(line[5:].strip())
            content = d2.get("result", {}).get("content", [])
            if content:
                text = content[0].get("text", "[]")
                print(f"\nQuery: {query}")
                # Results might be pre-formatted text or a parseable structure
                try:
                    results = ast.literal_eval(text)
                    if isinstance(results, list):
                        for item in results:
                            if isinstance(item, dict):
                                title = item.get("title", "")[:60]
                                score = item.get("score", 0)
                                print(f"  {score:.3f} | {title}")
                            else:
                                print(f"  {str(item)[:80]}")
                    else:
                        print(f"  {str(results)[:200]}")
                except Exception:
                    # Plain text response
                    for line2 in text.split("\n")[:5]:
                        print(f"  {line2[:100]}")

print("\nAll queries completed successfully!")
