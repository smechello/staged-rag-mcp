<p align="center">
  <strong>Staged RAG MCP Server — Complete Usage Guide</strong><br>
  <em>Step-by-step instructions, real-world examples, and troubleshooting for every feature.</em>
</p>

---

# How to Use — Staged RAG MCP Server

> **Author:** Shashidhar Reddy Nalamari  
> **Version:** 0.1.0  
> **Last Updated:** February 2026

This guide walks you through every feature of the Staged RAG MCP Server with practical examples, real-world use cases, and detailed troubleshooting. Whether you are a first-time user setting up the system, a developer integrating it into your workflow, or an administrator managing a production knowledge base, this document covers everything you need.

---

## Table of Contents

- [1. Getting Started](#1-getting-started)
  - [1.1 System Requirements](#11-system-requirements)
  - [1.2 Installation (Step by Step)](#12-installation-step-by-step)
  - [1.3 Setting Up Your API Key](#13-setting-up-your-api-key)
  - [1.4 Starting the Server](#14-starting-the-server)
  - [1.5 Verifying the Server is Running](#15-verifying-the-server-is-running)
- [2. Configuration Guide](#2-configuration-guide)
  - [2.1 Configuration File Hierarchy](#21-configuration-file-hierarchy)
  - [2.2 Choosing a Transport Mode](#22-choosing-a-transport-mode)
  - [2.3 Embedding Provider Setup](#23-embedding-provider-setup)
  - [2.4 Chunking Configuration](#24-chunking-configuration)
  - [2.5 Search & Retrieval Tuning](#25-search--retrieval-tuning)
  - [2.6 Knowledge Base Configuration](#26-knowledge-base-configuration)
  - [2.7 Full Configuration Example](#27-full-configuration-example)
- [3. Connecting MCP Clients](#3-connecting-mcp-clients)
  - [3.1 VS Code / GitHub Copilot (HTTP Mode)](#31-vs-code--github-copilot-http-mode)
  - [3.2 VS Code / GitHub Copilot (STDIO Mode)](#32-vs-code--github-copilot-stdio-mode)
  - [3.3 Claude Desktop](#33-claude-desktop)
  - [3.4 Custom MCP Clients](#34-custom-mcp-clients)
- [4. Document Ingestion](#4-document-ingestion)
  - [4.1 Ingest a Single Document](#41-ingest-a-single-document)
  - [4.2 Ingest with Tags and Metadata](#42-ingest-with-tags-and-metadata)
  - [4.3 Ingest with a Pre-Computed Summary](#43-ingest-with-a-pre-computed-summary)
  - [4.4 Batch Ingestion](#44-batch-ingestion)
  - [4.5 Ingesting into Named Collections](#45-ingesting-into-named-collections)
- [5. The Two-Level Retrieval Workflow](#5-the-two-level-retrieval-workflow)
  - [5.1 Level 1 — Search Summaries](#51-level-1--search-summaries)
  - [5.2 Evaluating Summaries](#52-evaluating-summaries)
  - [5.3 Level 2 — Get Full Documents](#53-level-2--get-full-documents)
  - [5.4 Level 2.5 — Get a Specific Chunk](#54-level-25--get-a-specific-chunk)
  - [5.5 Complete Retrieval Walkthrough](#55-complete-retrieval-walkthrough)
- [6. Advanced Search](#6-advanced-search)
  - [6.1 Hybrid Search (Semantic + Keyword)](#61-hybrid-search-semantic--keyword)
  - [6.2 Multi-Query Search with Rank Fusion](#62-multi-query-search-with-rank-fusion)
  - [6.3 Find Similar Documents](#63-find-similar-documents)
  - [6.4 Filtering by Tags](#64-filtering-by-tags)
  - [6.5 Choosing the Right Search Strategy](#65-choosing-the-right-search-strategy)
- [7. Document Management](#7-document-management)
  - [7.1 Update a Document](#71-update-a-document)
  - [7.2 Delete a Document](#72-delete-a-document)
  - [7.3 Inspect Document Metadata](#73-inspect-document-metadata)
- [8. Knowledge Base (Auto-Sync Folder)](#8-knowledge-base-auto-sync-folder)
  - [8.1 Enabling the Knowledge Base](#81-enabling-the-knowledge-base)
  - [8.2 Adding Files](#82-adding-files)
  - [8.3 Organising with Subfolders](#83-organising-with-subfolders)
  - [8.4 Working with PDFs](#84-working-with-pdfs)
  - [8.5 Checking Knowledge Base Status](#85-checking-knowledge-base-status)
  - [8.6 Force Re-Synchronisation](#86-force-re-synchronisation)
  - [8.7 Understanding Auto-Generated Tags](#87-understanding-auto-generated-tags)
- [9. Collections](#9-collections)
  - [9.1 Creating and Using Collections](#91-creating-and-using-collections)
  - [9.2 Multi-Collection Strategies](#92-multi-collection-strategies)
  - [9.3 Listing All Collections](#93-listing-all-collections)
  - [9.4 Collection Statistics](#94-collection-statistics)
- [10. Observability & Debugging](#10-observability--debugging)
  - [10.1 Explain Why a Document Ranked](#101-explain-why-a-document-ranked)
  - [10.2 Viewing the Audit Log](#102-viewing-the-audit-log)
  - [10.3 Monitoring System Health](#103-monitoring-system-health)
- [11. Embedding Providers — Setup & Examples](#11-embedding-providers--setup--examples)
  - [11.1 Google Gemini (Default)](#111-google-gemini-default)
  - [11.2 OpenAI](#112-openai)
  - [11.3 Ollama (Local, No API Key)](#113-ollama-local-no-api-key)
  - [11.4 HuggingFace (Local or API)](#114-huggingface-local-or-api)
  - [11.5 Azure OpenAI](#115-azure-openai)
  - [11.6 Together AI](#116-together-ai)
  - [11.7 LM Studio (Local)](#117-lm-studio-local)
  - [11.8 Switching Providers Safely](#118-switching-providers-safely)
  - [11.9 Deterministic Fallback](#119-deterministic-fallback)
- [12. Prompt Engineering for Staged RAG](#12-prompt-engineering-for-staged-rag)
  - [12.1 System Prompt](#121-system-prompt)
  - [12.2 Evaluate Summaries Prompt](#122-evaluate-summaries-prompt)
  - [12.3 Deep Analysis Prompt](#123-deep-analysis-prompt)
- [13. Real-World Use Cases](#13-real-world-use-cases)
  - [13.1 Internal Knowledge Base for a Team](#131-internal-knowledge-base-for-a-team)
  - [13.2 Research Paper Collection](#132-research-paper-collection)
  - [13.3 Codebase Documentation Search](#133-codebase-documentation-search)
  - [13.4 Customer Support Knowledge Base](#134-customer-support-knowledge-base)
  - [13.5 Personal Note-Taking System](#135-personal-note-taking-system)
  - [13.6 Multi-Tenant SaaS Application](#136-multi-tenant-saas-application)
- [14. Testing](#14-testing)
  - [14.1 Running Tests](#141-running-tests)
  - [14.2 Seeding Sample Data](#142-seeding-sample-data)
  - [14.3 Inspecting Data Store State](#143-inspecting-data-store-state)
- [15. Performance Tuning](#15-performance-tuning)
  - [15.1 Optimising Search Quality](#151-optimising-search-quality)
  - [15.2 Reducing API Costs](#152-reducing-api-costs)
  - [15.3 Handling Large Collections](#153-handling-large-collections)
- [16. Security Best Practices](#16-security-best-practices)
- [17. Troubleshooting](#17-troubleshooting)
  - [17.1 Installation Problems](#171-installation-problems)
  - [17.2 Server Startup Issues](#172-server-startup-issues)
  - [17.3 Embedding & API Errors](#173-embedding--api-errors)
  - [17.4 Search Quality Issues](#174-search-quality-issues)
  - [17.5 Knowledge Base Issues](#175-knowledge-base-issues)
  - [17.6 Data & Storage Issues](#176-data--storage-issues)
  - [17.7 MCP Client Connection Issues](#177-mcp-client-connection-issues)
  - [17.8 Common Error Messages Explained](#178-common-error-messages-explained)
- [18. FAQ](#18-faq)

---

## 1. Getting Started

### 1.1 System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| **Python** | 3.11 | 3.12+ |
| **pip** | 21.0+ | Latest |
| **RAM** | 512 MB | 2 GB+ (for large collections) |
| **Disk** | 50 MB (application) | Depends on document volume |
| **OS** | Windows 10+, macOS 12+, Linux | Any |
| **API Key** | At least one embedding provider | Gemini (free tier available) |

### 1.2 Installation (Step by Step)

**Step 1: Clone the repository**

```bash
git clone https://github.com/reddynalamari/staged-rag-mcp.git
cd staged-rag-mcp
```

**Step 2: Create and activate a virtual environment**

```bash
# Create
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.venv\Scripts\activate.bat

# Activate (macOS / Linux)
source .venv/bin/activate
```

**Step 3: Install the package**

```bash
# Core installation (includes Gemini embedding support)
pip install -e .
```

**Step 4 (Optional): Install additional embedding providers**

```bash
# Pick one or more:
pip install -e ".[openai]"          # OpenAI / Azure OpenAI / LM Studio
pip install -e ".[ollama]"          # Ollama local models
pip install -e ".[huggingface]"     # HuggingFace sentence-transformers
pip install -e ".[together]"        # Together AI

# Or install everything at once:
pip install -e ".[all-providers]"

# For development (tests, linting):
pip install -e ".[all-providers,dev]"
```

**Step 5: Verify installation**

```bash
python -c "from staged_rag import __version__; print(f'Staged RAG MCP v{__version__}')"
```

Expected output:
```
Staged RAG MCP v0.1.0
```

### 1.3 Setting Up Your API Key

Create a `.env` file in the project root directory:

```bash
# For Google Gemini (default provider — free tier available at https://aistudio.google.com/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Tip:** If you don't want to use any API key, you can use Ollama for fully local, free embeddings. See [section 11.3](#113-ollama-local-no-api-key). The system also has a deterministic fallback that works without any API, but produces lower quality search results.

### 1.4 Starting the Server

**HTTP Mode (default — recommended for VS Code)**

```bash
python -m staged_rag.server
```

You should see output like:
```
INFO: Starting Staged RAG MCP Server...
INFO: Embedding provider: gemini (gemini-embedding-001)
INFO: Knowledge-base watcher active – monitoring ./knowledge_base
INFO: Server listening on http://127.0.0.1:8090
```

**STDIO Mode (for Claude Desktop or clients that spawn the process)**

First, update `config.local.yaml`:
```yaml
server:
  transport: stdio
```

Then the MCP client will start the server automatically — you don't run it manually.

### 1.5 Verifying the Server is Running

After starting in HTTP mode, test with a simple MCP request:

```bash
# Using curl (the server listens for MCP protocol, not REST)
curl -s http://127.0.0.1:8090/mcp -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python -m json.tool
```

You should see a list of 17 available tools. If the server is running correctly, you can now connect an MCP client.

---

## 2. Configuration Guide

### 2.1 Configuration File Hierarchy

The system uses a three-layer configuration merge:

```
Built-in Defaults (config.py)   ← lowest priority
         ↓
config.yaml (base config)       ← project-level settings
         ↓
config.local.yaml (overrides)   ← your personal overrides (highest priority)
```

**Best practice:** Keep `config.yaml` as-is (version controlled defaults). Put all your customizations in `config.local.yaml` (which should be gitignored).

### 2.2 Choosing a Transport Mode

| Mode | When to Use | Configuration |
|---|---|---|
| `streamable-http` | VS Code, custom HTTP clients, development | `server.transport: streamable-http` |
| `stdio` | Claude Desktop, MCP clients that spawn processes | `server.transport: stdio` |

**Example — HTTP mode on a custom port:**

```yaml
# config.local.yaml
server:
  transport: streamable-http
  host: 127.0.0.1
  port: 9000
```

**Example — STDIO mode:**

```yaml
# config.local.yaml
server:
  transport: stdio
```

### 2.3 Embedding Provider Setup

This is the most important configuration choice. It determines how your documents are converted to vectors for similarity search.

**Quick comparison:**

| Provider | API Key? | Local? | Quality | Speed | Cost |
|---|---|---|---|---|---|
| Gemini | Yes | No | High | Fast | Free tier |
| OpenAI | Yes | No | Very High | Fast | Paid |
| Ollama | No | Yes | Good | Medium | Free |
| HuggingFace | Optional | Yes/No | Good | Varies | Free locally |
| Azure OpenAI | Yes | No | Very High | Fast | Enterprise |
| Together AI | Yes | No | Good | Fast | Paid |
| LM Studio | No | Yes | Good | Medium | Free |

See [Section 11](#11-embedding-providers--setup--examples) for detailed setup instructions for each provider.

### 2.4 Chunking Configuration

Chunks control how documents are split for granular retrieval. The defaults work well for most cases.

```yaml
chunking:
  chunk_size: 200       # Target words per chunk
  chunk_overlap: 20     # Overlapping words between chunks (context continuity)
  min_chunk_size: 50    # Discard chunks smaller than this
```

**Tuning guidelines:**

| Scenario | chunk_size | chunk_overlap | min_chunk_size |
|---|---|---|---|
| Short documents (< 500 words) | 100 | 10 | 30 |
| Standard documents | 200 | 20 | 50 |
| Long documents / books | 400 | 40 | 80 |
| Code files | 150 | 15 | 30 |
| Legal / precise documents | 300 | 30 | 60 |

### 2.5 Search & Retrieval Tuning

```yaml
retrieval:
  default_top_k: 5              # Default number of results
  max_top_k: 50                 # Maximum allowed
  default_collection: default   # Default collection name
  hybrid_semantic_weight: 0.7   # Semantic weight in hybrid search
  hybrid_keyword_weight: 0.3    # Keyword weight in hybrid search
  min_similarity_score: 0.0     # Global minimum score threshold
```

**Tuning tips:**

- **Increase `default_top_k`** to 10–15 if you frequently search large collections and want more candidates.
- **Raise `min_similarity_score`** to 0.3–0.5 to filter out low-quality matches automatically.
- **Adjust hybrid weights** — set `hybrid_keyword_weight: 0.5` and `hybrid_semantic_weight: 0.5` when exact keyword matches are important (e.g., technical documentation with specific terms).

### 2.6 Knowledge Base Configuration

```yaml
knowledge_base:
  enabled: true                       # Set false to disable file watching
  kb_dir: ./knowledge_base            # Folder to watch
  manifest_file: ./data/kb_manifest.json
  collection: default                 # Collection for KB documents
  poll_interval: 5.0                  # Check for changes every N seconds
  max_file_size: 10485760             # 10 MB max file size
```

**When to adjust `poll_interval`:**
- **Active editing** (files changing frequently): `2.0` seconds
- **Stable knowledge base** (rarely changes): `30.0` or `60.0` seconds
- **Large number of files** (1000+): `15.0` seconds (to reduce CPU usage)

### 2.7 Full Configuration Example

Here is a complete `config.local.yaml` for a team using Ollama locally with a large knowledge base:

```yaml
server:
  name: team-knowledge-rag
  transport: streamable-http
  host: 127.0.0.1
  port: 8090

embedding:
  provider: ollama
  model: nomic-embed-text
  dimensions: 768
  batch_size: 16

generation:
  model: gemini-2.5-flash-lite
  summary_max_sentences: 3

chunking:
  chunk_size: 250
  chunk_overlap: 25
  min_chunk_size: 50

retrieval:
  default_top_k: 10
  max_top_k: 50
  hybrid_semantic_weight: 0.6
  hybrid_keyword_weight: 0.4
  min_similarity_score: 0.1

ingestion:
  max_document_tokens: 100000
  max_batch_size: 100
  auto_summary: true

knowledge_base:
  enabled: true
  kb_dir: ./knowledge_base
  poll_interval: 10.0
  max_file_size: 20971520    # 20 MB

logging:
  log_level: INFO
```

---

## 3. Connecting MCP Clients

### 3.1 VS Code / GitHub Copilot (HTTP Mode)

This is the simplest setup. Start the server first, then point VS Code to it.

**Step 1:** Start the server:
```bash
python -m staged_rag.server
```

**Step 2:** Create or edit `.vscode/mcp.json` in your project:

```json
{
  "mcpServers": {
    "staged-rag": {
      "url": "http://127.0.0.1:8090/mcp"
    }
  }
}
```

**Step 3:** Restart VS Code or reload the window. The MCP server tools now appear in GitHub Copilot's tool list.

### 3.2 VS Code / GitHub Copilot (STDIO Mode)

The server is spawned directly by VS Code — no need to start it manually.

**Step 1:** Set STDIO transport in `config.local.yaml`:
```yaml
server:
  transport: stdio
```

**Step 2:** Create `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "staged-rag": {
      "command": "python",
      "args": ["-m", "staged_rag.server"],
      "cwd": "C:/path/to/staged-rag-mcp",
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

> **Note:** Replace `C:/path/to/staged-rag-mcp` with the actual path to your project. On macOS/Linux, use forward slashes.

**Step 3:** Restart VS Code. The server starts automatically when Copilot needs it.

### 3.3 Claude Desktop

**Step 1:** Set STDIO transport in `config.local.yaml`:
```yaml
server:
  transport: stdio
```

**Step 2:** Edit Claude Desktop's configuration file:

- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "staged-rag": {
      "command": "python",
      "args": ["-m", "staged_rag.server"],
      "cwd": "C:\\path\\to\\staged-rag-mcp",
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Step 3:** Restart Claude Desktop. You should see "staged-rag" listed as an available MCP server.

### 3.4 Custom MCP Clients

Any MCP-compatible client can connect. The server exposes 17 tools across 6 categories:

| Category | Tools |
|---|---|
| **Retrieval** | `search_summaries`, `get_documents`, `get_document_chunk` |
| **Advanced Search** | `hybrid_search`, `multi_query_search`, `find_similar` |
| **Management** | `ingest_document`, `ingest_batch`, `update_document`, `delete_document` |
| **Metadata** | `get_document_metadata` |
| **Observability** | `collection_stats`, `list_collections`, `explain_retrieval`, `retrieval_log` |
| **Knowledge Base** | `kb_status`, `kb_resync` |

---

## 4. Document Ingestion

### 4.1 Ingest a Single Document

The simplest way to add a document:

```python
result = ingest_document(
    title="Introduction to Machine Learning",
    text="Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves. The process begins with observations or data, such as examples, direct experience, or instruction, in order to look for patterns in data and make better decisions in the future."
)
```

**Response:**
```json
{
  "doc_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "Introduction to Machine Learning",
  "collection": "default",
  "chunk_count": 2,
  "token_count": 64,
  "summary": "Machine learning is a subset of artificial intelligence that enables systems to learn from experience. It focuses on developing programs that access data to learn autonomously.",
  "status": "indexed"
}
```

The system automatically:
1. Counted tokens (64)
2. Generated a summary using Gemini (or local extractive fallback)
3. Split the text into 2 chunks with overlap
4. Created an embedding for the summary
5. Indexed the document in vector and BM25 indexes
6. Recorded an audit log entry

### 4.2 Ingest with Tags and Metadata

Tags make documents filterable. Metadata stores arbitrary information.

```python
result = ingest_document(
    title="REST API Design Best Practices",
    text="RESTful APIs should follow standard HTTP methods: GET for retrieving resources, POST for creating new resources, PUT for updating existing resources, and DELETE for removing resources. Use proper status codes: 200 for success, 201 for created, 400 for bad request, 404 for not found, and 500 for server errors. Version your APIs using URL path versioning (e.g., /api/v1/users) for clarity and backward compatibility.",
    source="https://example.com/api-guide",
    tags=["api", "rest", "backend", "best-practices"],
    metadata={
        "author": "Jane Doe",
        "category": "Engineering",
        "difficulty": "intermediate",
        "year": 2026
    }
)
```

Now you can search with tag filters:
```python
results = search_summaries("API design", tags_filter=["api"])
results = search_summaries("backend practices", tags_filter=["backend", "best-practices"])
```

### 4.3 Ingest with a Pre-Computed Summary

If you already have a high-quality summary, pass it directly to avoid the auto-generation step:

```python
result = ingest_document(
    title="Quarterly Sales Report Q1 2026",
    text="...full report text...",
    summary="Q1 2026 sales totalled $4.2M, a 15% increase over Q4 2025. The EMEA region led growth at 22%, while North America grew 12%. Three new enterprise contracts were signed, contributing $800K in annual recurring revenue.",
    tags=["sales", "quarterly-report", "2026"],
    metadata={"quarter": "Q1", "year": 2026, "total_revenue": 4200000}
)
```

### 4.4 Batch Ingestion

Ingest multiple documents in a single call (up to `max_batch_size`, default 50):

```python
result = ingest_batch(
    documents=[
        {
            "title": "Python Data Types",
            "text": "Python supports several built-in data types including integers, floats, strings, lists, tuples, dictionaries, and sets. Each type has specific behaviors and methods...",
            "tags": ["python", "basics"]
        },
        {
            "title": "Python Functions",
            "text": "Functions in Python are defined using the def keyword. They can accept positional arguments, keyword arguments, default values, and variable-length arguments using *args and **kwargs...",
            "tags": ["python", "functions"]
        },
        {
            "title": "Python Classes",
            "text": "Python supports object-oriented programming with classes. Classes are defined using the class keyword and can include attributes, methods, constructors (__init__), and support inheritance...",
            "tags": ["python", "oop"]
        }
    ],
    collection="tutorials"
)
```

**Response:**
```json
{
  "total": 3,
  "succeeded": 3,
  "failed": 0,
  "results": [
    {"doc_id": "...", "title": "Python Data Types", "status": "indexed"},
    {"doc_id": "...", "title": "Python Functions", "status": "indexed"},
    {"doc_id": "...", "title": "Python Classes", "status": "indexed"}
  ],
  "total_tokens_indexed": 142
}
```

### 4.5 Ingesting into Named Collections

Collections provide isolated namespaces. Documents in different collections are completely independent.

```python
# Ingest engineering docs into "engineering" collection
ingest_document(
    title="Microservice Architecture",
    text="...",
    collection="engineering",
    tags=["architecture"]
)

# Ingest product docs into "product" collection
ingest_document(
    title="Product Roadmap 2026",
    text="...",
    collection="product",
    tags=["roadmap"]
)

# Search only within engineering
results = search_summaries("architecture", collection="engineering")

# Search only within product
results = search_summaries("roadmap", collection="product")
```

---

## 5. The Two-Level Retrieval Workflow

This is the core innovation of Staged RAG. Instead of retrieving full documents immediately, you first get lightweight summaries, evaluate them, and then selectively expand only the relevant ones.

### 5.1 Level 1 — Search Summaries

Always start here. This is the cheapest operation — it returns only summaries and similarity scores, not full document text.

```python
results = search_summaries(
    query="How do neural networks learn?",
    top_k=5
)
```

**Response:**
```json
{
  "query": "How do neural networks learn?",
  "results": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Backpropagation in Neural Networks",
      "summary": "Neural networks learn through backpropagation, adjusting weights based on error gradients. The process involves forward pass, loss computation, and backward pass through the network layers.",
      "similarity_score": 0.94,
      "token_count": 2500,
      "tags": ["ml", "deep-learning"],
      "collection": "default"
    },
    {
      "doc_id": "e5f6g7h8-...",
      "title": "Gradient Descent Optimisation",
      "summary": "Gradient descent is the primary optimisation algorithm used to train neural networks. Variants include SGD, Adam, and RMSProp, each with different convergence properties.",
      "similarity_score": 0.87,
      "token_count": 1800,
      "tags": ["ml", "optimisation"],
      "collection": "default"
    },
    {
      "doc_id": "i9j0k1l2-...",
      "title": "History of Artificial Intelligence",
      "summary": "AI has evolved from symbolic reasoning in the 1950s through expert systems to modern deep learning approaches. Key milestones include the perceptron, convolutional networks, and transformers.",
      "similarity_score": 0.62,
      "token_count": 5200,
      "tags": ["ai", "history"],
      "collection": "default"
    }
  ],
  "total_candidates": 25,
  "search_time_ms": 145.3
}
```

### 5.2 Evaluating Summaries

Before expanding documents, evaluate the summaries:

- **Score 0.94** — "Backpropagation in Neural Networks" → Highly relevant, EXPAND
- **Score 0.87** — "Gradient Descent Optimisation" → Relevant, EXPAND
- **Score 0.62** — "History of Artificial Intelligence" → Tangentially related, SKIP (saves 5200 tokens)

By skipping the third document, you save **5200 tokens** from your LLM context window — tokens that would have been wasted on a mostly irrelevant document.

### 5.3 Level 2 — Get Full Documents

Now fetch only the documents you decided to expand:

```python
full = get_documents(
    doc_ids=["a1b2c3d4-...", "e5f6g7h8-..."],
    include_chunks=True
)
```

**Response:**
```json
{
  "documents": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Backpropagation in Neural Networks",
      "full_text": "Complete document text about backpropagation...",
      "source": "manual",
      "token_count": 2500,
      "tags": ["ml", "deep-learning"],
      "metadata": {},
      "chunks": [
        {"chunk_index": 0, "text": "First chunk...", "token_count": 195, "start_char": 0, "end_char": 1024},
        {"chunk_index": 1, "text": "Second chunk...", "token_count": 200, "start_char": 980, "end_char": 2100}
      ]
    },
    {
      "doc_id": "e5f6g7h8-...",
      "title": "Gradient Descent Optimisation",
      "full_text": "Complete document text about gradient descent...",
      "source": "manual",
      "token_count": 1800,
      "tags": ["ml", "optimisation"],
      "metadata": {},
      "chunks": [...]
    }
  ],
  "total_tokens": 4300
}
```

### 5.4 Level 2.5 — Get a Specific Chunk

If a document is very long, you may only need a specific section. Use chunk retrieval for surgical precision.

**By index (you know which chunk you want):**

```python
chunk = get_document_chunk(
    doc_id="a1b2c3d4-...",
    chunk_index=3
)
```

**Response:**
```json
{
  "doc_id": "a1b2c3d4-...",
  "chunk_index": 3,
  "total_chunks": 12,
  "text": "The backward pass computes gradients using the chain rule...",
  "token_count": 195,
  "has_previous": true,
  "has_next": true
}
```

**By semantic query (find the most relevant chunk):**

```python
chunk = get_document_chunk(
    doc_id="a1b2c3d4-...",
    chunk_query="learning rate scheduling"
)
```

**Response:**
```json
{
  "doc_id": "a1b2c3d4-...",
  "chunk_index": 7,
  "total_chunks": 12,
  "text": "Learning rate scheduling adjusts the learning rate during training...",
  "token_count": 180,
  "has_previous": true,
  "has_next": true,
  "relevance_score": 0.91
}
```

Use `has_previous` and `has_next` to navigate through adjacent chunks for more context.

### 5.5 Complete Retrieval Walkthrough

Here is a complete end-to-end example showing the staged retrieval protocol:

```python
import json

# STEP 1: Search summaries (Level 1)
results = search_summaries("best practices for database indexing", top_k=5)

print(f"Found {len(results['results'])} candidates in {results['search_time_ms']:.0f}ms")
print()

# STEP 2: Evaluate summaries
docs_to_expand = []
for r in results["results"]:
    decision = "EXPAND" if r["similarity_score"] >= 0.75 else "SKIP"
    print(f"  [{r['similarity_score']:.2f}] {r['title']} → {decision}")
    if decision == "EXPAND":
        docs_to_expand.append(r["doc_id"])

print(f"\nExpanding {len(docs_to_expand)} of {len(results['results'])} documents")

# STEP 3: Fetch full documents (Level 2)
if docs_to_expand:
    full = get_documents(docs_to_expand, include_chunks=True)
    print(f"\nTotal tokens retrieved: {full['total_tokens']}")

    for doc in full["documents"]:
        print(f"\n--- {doc['title']} ({doc['token_count']} tokens, {len(doc['chunks'])} chunks) ---")
        print(doc["full_text"][:300] + "...")

    # STEP 4 (optional): Get a specific chunk for targeted analysis
    for doc in full["documents"]:
        if doc["token_count"] > 2000:
            relevant_chunk = get_document_chunk(
                doc_id=doc["doc_id"],
                chunk_query="index types B-tree hash"
            )
            print(f"\nMost relevant chunk from '{doc['title']}':")
            print(f"  Chunk {relevant_chunk['chunk_index']}/{relevant_chunk['total_chunks']}")
            print(f"  Relevance: {relevant_chunk.get('relevance_score', 'N/A')}")
            print(f"  Text: {relevant_chunk['text'][:200]}...")
```

---

## 6. Advanced Search

### 6.1 Hybrid Search (Semantic + Keyword)

Hybrid search combines the best of both worlds: semantic understanding (catches synonyms and meaning) with keyword matching (catches exact terms). This is especially useful for technical content where specific terms matter.

```python
results = hybrid_search(
    query="PostgreSQL EXPLAIN ANALYZE query plan",
    top_k=5,
    semantic_weight=0.5,    # Give equal weight to meaning
    keyword_weight=0.5      # and exact term matches
)
```

**When to use hybrid search:**

| Scenario | Recommended Weights |
|---|---|
| Technical documentation with specific terms | semantic: 0.5, keyword: 0.5 |
| General knowledge queries | semantic: 0.7, keyword: 0.3 (default) |
| Exact phrase lookups | semantic: 0.3, keyword: 0.7 |
| Cross-language / synonym-heavy queries | semantic: 0.9, keyword: 0.1 |

**How scoring works internally:**

```
1. Semantic search → cosine similarity scores (already 0.0–1.0)
2. BM25 keyword search → raw scores → normalised by dividing by max score → (0.0–1.0)
3. Weights are normalised to sum to 1.0
4. Final score = (normalised_semantic_weight × semantic_score) + (normalised_keyword_weight × bm25_score)
5. Results sorted by final score, top_k returned
```

### 6.2 Multi-Query Search with Rank Fusion

When a topic has multiple facets, use multi-query search to capture all angles:

```python
results = multi_query_search(
    queries=[
        "containerisation with Docker",
        "Kubernetes orchestration",
        "microservice deployment strategies"
    ],
    top_k=5,
    fusion_method="rrf"    # Reciprocal Rank Fusion
)
```

**Fusion methods explained:**

**RRF (Reciprocal Rank Fusion)** — Default, generally best:
- Each document gets a score based on its rank position in each sub-query result
- Formula: `score = Σ 1/(60 + rank + 1)` for each query where the document appears
- Documents appearing across multiple queries get boosted
- The constant `k=60` dampens extreme rank differences

**Max Score** — Simpler alternative:
- Takes the highest similarity score across all queries
- Good when queries are very different aspects of the same topic

```python
# Using max-score fusion
results = multi_query_search(
    queries=["Python web frameworks", "Django vs Flask comparison"],
    top_k=5,
    fusion_method="max"
)
```

### 6.3 Find Similar Documents

Given a document you already know is relevant, find more like it:

```python
# You have a good document about React hooks
similar = find_similar(
    doc_id="a1b2c3d4-...",
    top_k=5,
    exclude_same_source=True    # Exclude docs from the same source file
)
```

**Use cases:**
- "More like this" recommendations
- Discovering related content you didn't know existed
- Finding duplicate or near-duplicate documents
- Building document clusters

### 6.4 Filtering by Tags

Tags let you scope searches to specific categories:

```python
# Only search in engineering documents
results = search_summaries(
    query="deployment pipeline",
    tags_filter=["folder:engineering"]
)

# Only search PDF documents
results = search_summaries(
    query="quarterly performance",
    tags_filter=["filetype:pdf"]
)

# Only search knowledge base documents
results = search_summaries(
    query="API design patterns",
    tags_filter=["source:knowledge_base"]
)

# Multiple tags (OR logic — matches any of the tags)
results = search_summaries(
    query="testing strategies",
    tags_filter=["backend", "testing", "qa"]
)
```

### 6.5 Choosing the Right Search Strategy

| Your Situation | Recommended Tool | Why |
|---|---|---|
| General question | `search_summaries` | Fast, semantic understanding |
| Technical query with specific terms | `hybrid_search` | Catches exact keywords |
| Multi-aspect topic | `multi_query_search` | Covers all facets |
| "More like this" | `find_similar` | Uses known-good document as reference |
| Known category | `search_summaries` + `tags_filter` | Scoped to relevant subset |
| Debugging low-quality results | `explain_retrieval` | Shows why docs ranked as they did |

---

## 7. Document Management

### 7.1 Update a Document

**Update metadata only (no re-embedding):**

```python
result = update_document(
    doc_id="a1b2c3d4-...",
    title="Updated Title",
    tags=["new-tag-1", "new-tag-2"],           # Replaces all existing tags
    metadata={"reviewed": True, "version": 2}   # Merged with existing metadata
)
```

**Update text (triggers full re-processing):**

```python
result = update_document(
    doc_id="a1b2c3d4-...",
    text="Completely new document content with updated information about machine learning advances in 2026..."
)
```

When you update `text`:
1. Document is re-chunked (old chunks replaced)
2. New summary is auto-generated
3. New embedding is computed and vector index updated
4. BM25 index is rebuilt
5. `updated_at` timestamp is set

**Update just the summary (triggers re-embedding but not re-chunking):**

```python
result = update_document(
    doc_id="a1b2c3d4-...",
    summary="Improved summary that better captures the key points of the document."
)
```

### 7.2 Delete a Document

```python
result = delete_document(doc_id="a1b2c3d4-...")
```

**Response:**
```json
{
  "doc_id": "a1b2c3d4-...",
  "deleted": true
}
```

If the document doesn't exist:
```json
{
  "doc_id": "nonexistent-id",
  "deleted": false
}
```

**What gets cleaned up automatically:**
- Document removed from JSON store
- Embedding vector removed from NumPy index
- BM25 index rebuilt without the document
- Audit log entry recorded

### 7.3 Inspect Document Metadata

Get document metadata without loading the full text (lightweight operation):

```python
meta = get_document_metadata(doc_id="a1b2c3d4-...")
```

**Response:**
```json
{
  "doc_id": "a1b2c3d4-...",
  "title": "Introduction to Machine Learning",
  "source": "manual",
  "collection": "default",
  "tags": ["ml", "tutorial"],
  "token_count": 2500,
  "chunk_count": 12,
  "created_at": "2026-02-08T10:30:00+00:00",
  "updated_at": "2026-02-09T14:20:00+00:00",
  "metadata": {"author": "Jane Doe", "difficulty": "beginner"}
}
```

**Use cases:**
- Checking if a document exists before updating
- Verifying chunk count and token count
- Reviewing tags and metadata
- Checking creation/update timestamps

---

## 8. Knowledge Base (Auto-Sync Folder)

The Knowledge Base is a powerful feature that automatically ingests, updates, and removes documents based on file system changes — no manual `ingest_document` calls needed.

### 8.1 Enabling the Knowledge Base

In `config.yaml` or `config.local.yaml`:

```yaml
knowledge_base:
  enabled: true
  kb_dir: ./knowledge_base
  poll_interval: 5.0
```

When the server starts, you'll see:
```
INFO: Knowledge-base watcher active – monitoring ./knowledge_base
INFO: Running initial KB sync...
INFO: Initial KB sync complete: {'created': 5, 'modified': 0, 'deleted': 0, 'errors': 0}
```

### 8.2 Adding Files

Simply drop files into the `knowledge_base/` directory:

```
knowledge_base/
├── meeting-notes.md
├── project-plan.txt
├── quarterly-report.pdf
└── api-spec.yaml
```

Within `poll_interval` seconds (default 5), the files are automatically:
1. Detected by the file watcher (SHA-256 hash tracking)
2. Read and text-extracted (PDF support via `pypdf`)
3. Text cleaned (CamelCase splits, page numbers removed, whitespace normalized)
4. Summarised (Gemini API or local extractive fallback)
5. Chunked and embedded
6. Indexed in the vector store
7. Recorded in the KB manifest

**Modifying a file?** The watcher detects the hash change and automatically re-indexes it.

**Deleting a file?** The watcher detects the removal and cleans up the document from all indexes.

### 8.3 Organising with Subfolders

Subfolder names automatically become searchable tags:

```
knowledge_base/
├── engineering/
│   ├── architecture.md          → tags: [filetype:md, source:knowledge_base, folder:engineering]
│   ├── testing-guide.md         → tags: [filetype:md, source:knowledge_base, folder:engineering]
│   └── apis/
│       └── rest-design.md       → tags: [filetype:md, source:knowledge_base, folder:engineering, folder:apis]
├── product/
│   ├── roadmap.md               → tags: [filetype:md, source:knowledge_base, folder:product]
│   └── specs/
│       └── feature-x.pdf        → tags: [filetype:pdf, source:knowledge_base, folder:product, folder:specs]
└── meeting-notes.txt            → tags: [filetype:txt, source:knowledge_base]
```

**Searching by folder:**
```python
# Find only engineering documents
results = search_summaries("API design", tags_filter=["folder:engineering"])

# Find only product specs
results = search_summaries("feature requirements", tags_filter=["folder:specs"])
```

### 8.4 Working with PDFs

PDF files are fully supported with automatic text extraction:

**Capabilities:**
- Full text extraction page-by-page via `pypdf`
- Metadata title extraction from PDF `/Title` field
- Smart text cleaning: page numbers removed, CamelCase words split, whitespace normalised
- Fallback title: first meaningful line of text, or cleaned filename

**Example:** Drop `annual-report-2025.pdf` into `knowledge_base/`. The system:
1. Extracts text from all pages
2. Reads PDF metadata for the title (e.g., "Annual Report 2025")
3. Cleans extracted text (e.g., "SalesRevenue" → "Sales Revenue")
4. Generates a summary and indexes the document

**Limitations:**
- **Scanned/image-only PDFs** produce no extractable text (recorded as error in manifest)
- **Encrypted PDFs** that require a password are skipped
- **Very large PDFs** may exceed `max_file_size` (default 10 MB — increase if needed)

### 8.5 Checking Knowledge Base Status

```python
status = kb_status()
```

**Response:**
```json
{
  "kb_dir": "C:/projects/staged-rag-mcp/knowledge_base",
  "collection": "default",
  "watcher_running": true,
  "manifest": {
    "total_files": 15,
    "total_indexed": 14,
    "total_errors": 1,
    "last_scan": "2026-02-09T12:00:00+00:00"
  }
}
```

### 8.6 Force Re-Synchronisation

If something goes wrong (manifest out of sync, index corruption), force a complete rebuild:

```python
result = kb_resync()
```

**What happens:**
1. All documents with source `knowledge_base:*` are deleted from the store and vector index
2. The KB manifest is completely cleared
3. Full folder scan runs from scratch
4. All files are re-ingested as if for the first time

**Response:**
```json
{
  "created": 15,
  "modified": 0,
  "deleted": 0,
  "errors": 1
}
```

> **Warning:** This is a destructive operation. All KB-sourced documents get new `doc_id` values after resync.

### 8.7 Understanding Auto-Generated Tags

Every file from the knowledge base is automatically tagged:

| Tag Pattern | Example | Meaning |
|---|---|---|
| `source:knowledge_base` | `source:knowledge_base` | File came from the KB folder |
| `filetype:<ext>` | `filetype:pdf` | File extension |
| `folder:<name>` | `folder:engineering` | Subfolder name (one tag per level) |

**Supported file extensions:**

`.txt`, `.md`, `.markdown`, `.rst`, `.json`, `.yaml`, `.yml`, `.csv`, `.tsv`, `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.h`, `.go`, `.rs`, `.html`, `.htm`, `.xml`, `.log`, `.cfg`, `.ini`, `.toml`, `.pdf`

---

## 9. Collections

### 9.1 Creating and Using Collections

Collections are created implicitly when you first ingest a document into them:

```python
# This creates the "research" collection automatically
ingest_document(
    title="Quantum Computing Basics",
    text="...",
    collection="research"
)

# This creates the "internal-docs" collection
ingest_document(
    title="Employee Handbook",
    text="...",
    collection="internal-docs"
)
```

Each collection has its own:
- JSON document store file: `data/store/research.json`
- Vector index file: `data/index/research.npz`
- In-memory BM25 index

### 9.2 Multi-Collection Strategies

| Strategy | When to Use | Example |
|---|---|---|
| **Single `default`** | Small projects, prototyping | Everything in `default` |
| **Topic-based** | Medium projects with distinct domains | `engineering`, `product`, `hr` |
| **Tenant-based** | Multi-tenant SaaS | `user_123`, `org_456` |
| **Temporal** | Time-series archives | `2026_q1`, `2026_q2` |
| **Environment** | Dev/staging/prod separation | `dev`, `staging`, `production` |

### 9.3 Listing All Collections

```python
result = list_collections()
```

**Response:**
```json
{
  "collections": [
    {"name": "default", "document_count": 25, "total_tokens": 37500, "description": ""},
    {"name": "research", "document_count": 10, "total_tokens": 18000, "description": ""},
    {"name": "internal-docs", "document_count": 5, "total_tokens": 8000, "description": ""}
  ]
}
```

### 9.4 Collection Statistics

Get detailed statistics for any collection:

```python
stats = collection_stats(collection="default")
```

**Response:**
```json
{
  "collection": "default",
  "document_count": 25,
  "total_tokens": 37500,
  "avg_tokens_per_doc": 1500.0,
  "total_chunks": 200,
  "tag_distribution": {
    "ml": 10,
    "tutorial": 5,
    "source:knowledge_base": 8,
    "filetype:md": 6,
    "filetype:pdf": 2
  },
  "source_distribution": {
    "manual": 15,
    "knowledge_base:notes.md": 5,
    "batch": 5
  },
  "oldest_document": "2026-01-15T08:00:00+00:00",
  "newest_document": "2026-02-09T12:00:00+00:00",
  "index_size_bytes": 245760
}
```

---

## 10. Observability & Debugging

### 10.1 Explain Why a Document Ranked

When search results seem unexpected, use `explain_retrieval` to understand the scoring:

```python
explanation = explain_retrieval(
    query="neural network training",
    doc_ids=["a1b2c3d4-...", "e5f6g7h8-..."]
)
```

**Response:**
```json
{
  "query": "neural network training",
  "explanations": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Backpropagation in Neural Networks",
      "cosine_similarity": 0.94,
      "bm25_score": 18.5,
      "top_matching_terms": ["neural", "network", "training"],
      "query_doc_term_overlap": 1.0,
      "explanation_text": "Combined semantic and keyword scores to rank this document."
    },
    {
      "doc_id": "e5f6g7h8-...",
      "title": "History of Computing",
      "cosine_similarity": 0.45,
      "bm25_score": 2.1,
      "top_matching_terms": ["network"],
      "query_doc_term_overlap": 0.33,
      "explanation_text": "Combined semantic and keyword scores to rank this document."
    }
  ]
}
```

**How to interpret:**
- **`cosine_similarity`** — Semantic relevance (0.0 = unrelated, 1.0 = perfect match)
- **`bm25_score`** — Keyword matching score (higher = more keyword overlap)
- **`query_doc_term_overlap`** — Fraction of query terms found in document (1.0 = all terms found)
- **`top_matching_terms`** — Which query words the system looked for

### 10.2 Viewing the Audit Log

Every tool call is logged. Review recent activity:

```python
# Get last 10 entries
log = retrieval_log(last_n=10)

# Filter by specific tool
log = retrieval_log(last_n=20, tool_filter="search_summaries")

# Filter by session
log = retrieval_log(last_n=50, session_id="session-abc-123")
```

**Response:**
```json
{
  "entries": [
    {
      "timestamp": "2026-02-09T12:34:56.789+00:00",
      "tool": "search_summaries",
      "params": {"query": "machine learning", "top_k": 5, "collection": "default"},
      "result_count": 3,
      "doc_ids": ["a1b2c3d4-...", "e5f6g7h8-...", "i9j0k1l2-..."],
      "latency_ms": 145.3
    },
    {
      "timestamp": "2026-02-09T12:34:57.123+00:00",
      "tool": "get_documents",
      "params": {"doc_ids": ["a1b2c3d4-..."], "include_chunks": true},
      "result_count": 1,
      "doc_ids": ["a1b2c3d4-..."],
      "latency_ms": 12.5
    }
  ],
  "total_entries": 156
}
```

**Use cases:**
- Debugging slow queries (check `latency_ms`)
- Monitoring usage patterns (which tools are called most)
- Auditing data access (who retrieved which documents)
- Performance analysis (average search times)

### 10.3 Monitoring System Health

Combine `collection_stats` and `list_collections` for a health dashboard:

```python
# Check all collections
collections = list_collections()
for col in collections["collections"]:
    print(f"Collection '{col['name']}': {col['document_count']} docs, {col['total_tokens']} tokens")

# Detailed stats for the main collection
stats = collection_stats("default")
print(f"Average tokens/doc: {stats['avg_tokens_per_doc']:.0f}")
print(f"Index size: {stats['index_size_bytes'] / 1024:.1f} KB")
print(f"Tag distribution: {stats['tag_distribution']}")
```

---

## 11. Embedding Providers — Setup & Examples

### 11.1 Google Gemini (Default)

**Setup:**

```yaml
# config.local.yaml
embedding:
  provider: gemini
  model: gemini-embedding-001
  dimensions: 3072
```

```bash
# .env
GEMINI_API_KEY=your_key_here
```

No additional pip install needed — `google-genai` is a core dependency.

**Getting a free API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key into your `.env` file

**Available models:**

| Model | Dimensions | Notes |
|---|---|---|
| `gemini-embedding-001` | 768–3072 | Configurable output dimensionality, best quality |

### 11.2 OpenAI

**Setup:**

```yaml
embedding:
  provider: openai
  model: text-embedding-3-small
  dimensions: 1536
```

```bash
# Install
pip install -e ".[openai]"

# .env
OPENAI_API_KEY=your_openai_key
```

**Available models:**

| Model | Dimensions | Cost | Notes |
|---|---|---|---|
| `text-embedding-3-small` | 1536 | Low | Best balance of quality and cost |
| `text-embedding-3-large` | 3072 | Higher | Highest quality |
| `text-embedding-ada-002` | 1536 | Low | Legacy, still works |

### 11.3 Ollama (Local, No API Key)

The best option for fully local, free operation. No data leaves your machine.

**Setup:**

```yaml
embedding:
  provider: ollama
  model: nomic-embed-text
  dimensions: 768
  provider_config:
    ollama_base_url: http://localhost:11434
```

```bash
# Install Ollama from https://ollama.ai
# Install the Python package
pip install -e ".[ollama]"

# Pull an embedding model
ollama pull nomic-embed-text
```

**Available models:**

| Model | Dimensions | Size | Notes |
|---|---|---|---|
| `nomic-embed-text` | 768 | 274 MB | Best general-purpose local model |
| `all-minilm` | 384 | 23 MB | Very lightweight, fast |
| `mxbai-embed-large` | 1024 | 669 MB | Higher quality, uses more RAM |

**Verify Ollama is running:**
```bash
ollama list
# Should show nomic-embed-text or your chosen model
```

### 11.4 HuggingFace (Local or API)

**Local mode (sentence-transformers — runs on your machine):**

```yaml
embedding:
  provider: huggingface
  model: all-MiniLM-L6-v2
  dimensions: 384
```

```bash
pip install -e ".[huggingface]"
```

The model downloads automatically on first use (~80 MB for all-MiniLM-L6-v2).

**API mode (HuggingFace Inference API):**

```yaml
embedding:
  provider: huggingface
  model: sentence-transformers/all-MiniLM-L6-v2
  dimensions: 384
  provider_config:
    huggingface_base_url: https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2
```

```bash
# .env
HUGGINGFACE_API_KEY=your_hf_key

# Uses OpenAI-compatible client
pip install -e ".[openai]"
```

### 11.5 Azure OpenAI

For enterprise Azure deployments:

```yaml
embedding:
  provider: azure_openai
  model: text-embedding-3-small
  dimensions: 1536
  provider_config:
    azure_kwargs:
      azure_deployment: my-embedding-deployment
      azure_endpoint: https://my-resource.openai.azure.com/
      api_version: 2024-02-01
```

```bash
# .env
EMBEDDING_AZURE_OPENAI_API_KEY=your_azure_key

pip install -e ".[openai]"
```

### 11.6 Together AI

```yaml
embedding:
  provider: together
  model: togethercomputer/m2-bert-80M-8k-retrieval
  dimensions: 768
```

```bash
# .env
TOGETHER_API_KEY=your_together_key

pip install -e ".[together]"
```

### 11.7 LM Studio (Local)

Run embeddings through LM Studio's OpenAI-compatible API:

```yaml
embedding:
  provider: lmstudio
  model: text-embedding-nomic-embed-text-v1.5
  dimensions: 768
  provider_config:
    openai_base_url: http://localhost:1234/v1
```

```bash
# No API key needed
pip install -e ".[openai]"    # Uses OpenAI-compatible client
```

**Steps:**
1. Download and install [LM Studio](https://lmstudio.ai)
2. Download an embedding model in LM Studio
3. Start the local server in LM Studio (default port 1234)
4. Configure as shown above

### 11.8 Switching Providers Safely

When changing embedding providers, existing embeddings become incompatible because different providers produce vectors in different dimensions and semantic spaces.

**Safe migration process:**

```bash
# 1. Stop the server

# 2. Update config.local.yaml with the new provider
# 3. Delete existing vector indexes
rm data/index/*.npz

# 4. If using knowledge base, force resync after starting:
#    Call kb_resync() to re-ingest all KB files with the new provider

# 5. For manually ingested documents, you'll need to re-ingest them
#    or write a migration script that reads from the JSON store and re-embeds

# 6. Start the server with the new provider
python -m staged_rag.server
```

### 11.9 Deterministic Fallback

If no embedding API is available (no key, network down, rate limited), the system automatically falls back to a deterministic vector generator:

1. SHA-256 hash of the input text → seed for NumPy random generator
2. Normal distribution → random vector of the configured dimensions
3. L2 normalisation → unit vector

**Properties:**
- **Deterministic** — same text always produces the same vector
- **Consistent** — similarity scores are stable but lower quality
- **Never crashes** — the server continues operating even without an API

**When this activates:**
- No API key configured for the selected provider
- API rate limit exceeded (429 errors)
- Network connectivity issues
- Provider service downtime

You'll see a log warning:
```
WARNING: Embedding API unavailable, using deterministic fallback
```

---

## 12. Prompt Engineering for Staged RAG

The `prompts.py` module provides structured prompts you can use in your LLM applications to implement the staged retrieval protocol.

### 12.1 System Prompt

Sets up the LLM to follow the two-level retrieval protocol:

```python
from staged_rag.prompts import staged_rag_system_prompt

prompt = staged_rag_system_prompt("What are the benefits of microservices?")
```

**Generated prompt:**
```
You are a knowledge assistant with access to a staged RAG system.

RETRIEVAL PROTOCOL:
1) SEARCH: call search_summaries with the user's question.
2) EVALUATE: read summaries and scores.
3) EXPAND: call get_documents for relevant docs only.
4) SYNTHESIZE: answer using retrieved content.
5) CITE: reference doc_ids for claims.

USER QUESTION: What are the benefits of microservices?
```

### 12.2 Evaluate Summaries Prompt

After Level 1, instruct the LLM to decide which documents warrant expansion:

```python
from staged_rag.prompts import evaluate_summaries_prompt
import json

summaries = results["results"]  # From search_summaries()
prompt = evaluate_summaries_prompt(json.dumps(summaries, indent=2))
```

This prompt asks the LLM to review each summary and classify it as EXPAND (fetch full text) or SKIP (not relevant enough).

### 12.3 Deep Analysis Prompt

After Level 2, instruct the LLM to synthesize an answer from the retrieved content:

```python
from staged_rag.prompts import deep_analysis_prompt

prompt = deep_analysis_prompt(
    question="What are the benefits of microservices?",
    context="[Full text from get_documents() concatenated here]"
)
```

This prompt instructs the LLM to:
- Answer only from the provided context (no hallucination)
- Cite specific `doc_id` values for claims
- Indicate when information is insufficient

---

## 13. Real-World Use Cases

### 13.1 Internal Knowledge Base for a Team

**Scenario:** Your engineering team has documentation spread across markdown files, PDFs, meeting notes, and code comments.

**Setup:**

```yaml
# config.local.yaml
knowledge_base:
  enabled: true
  kb_dir: /shared/team-docs
  poll_interval: 30.0        # Less frequent polling for stable docs
```

```
/shared/team-docs/
├── engineering/
│   ├── architecture-decisions/
│   │   ├── ADR-001-database-choice.md
│   │   ├── ADR-002-auth-strategy.md
│   │   └── ADR-003-api-versioning.md
│   ├── runbooks/
│   │   ├── deployment.md
│   │   └── incident-response.md
│   └── onboarding.md
├── product/
│   ├── PRD-feature-search.pdf
│   └── roadmap-2026.md
└── meeting-notes/
    ├── sprint-review-2026-02-03.md
    └── sprint-review-2026-02-10.md
```

**Usage:**
```python
# New engineer asking about deployment
results = search_summaries("how to deploy to production", tags_filter=["folder:runbooks"])

# Product manager searching for feature specs
results = search_summaries("search feature requirements", tags_filter=["folder:product"])

# Finding all architecture decisions about databases
results = hybrid_search("database selection PostgreSQL MongoDB", tags_filter=["folder:architecture-decisions"])
```

### 13.2 Research Paper Collection

**Scenario:** Manage a collection of research papers (PDFs) for academic research.

**Setup:**

```yaml
knowledge_base:
  enabled: true
  kb_dir: ./research-papers
  max_file_size: 52428800    # 50 MB for large papers

chunking:
  chunk_size: 400            # Larger chunks for academic content
  chunk_overlap: 40
```

**Workflow:**
```python
# Search across all papers
results = search_summaries("transformer attention mechanism self-attention", top_k=10)

# Multi-query for comprehensive review
results = multi_query_search(
    queries=[
        "self-attention mechanism in transformers",
        "multi-head attention computation",
        "positional encoding strategies"
    ],
    top_k=10,
    fusion_method="rrf"
)

# Find papers similar to one you're reading
similar = find_similar(doc_id="paper-a1b2c3...", top_k=5)

# Get a specific section from a long paper
chunk = get_document_chunk(
    doc_id="paper-a1b2c3...",
    chunk_query="experimental results accuracy comparison"
)
```

### 13.3 Codebase Documentation Search

**Scenario:** Index your project's code comments, docstrings, READMEs, and technical docs.

```
knowledge_base/
├── docs/
│   ├── api-reference.md
│   ├── contributing.md
│   └── changelog.md
├── src/
│   ├── auth.py          # Docstrings get indexed
│   ├── database.py
│   └── api_handler.py
└── configs/
    ├── settings.yaml
    └── docker-compose.yml
```

**Usage:**
```python
# "How does the authentication work?"
results = search_summaries("authentication flow login", tags_filter=["folder:src"])

# "What changed in the last release?"
results = search_summaries("recent changes updates", tags_filter=["filetype:md"])

# "How to configure the database?"
results = hybrid_search("database configuration connection string", tags_filter=["folder:configs"])
```

### 13.4 Customer Support Knowledge Base

**Scenario:** Build a knowledge base for customer support agents.

```python
# Ingest FAQ entries
ingest_batch(
    documents=[
        {
            "title": "How to Reset Password",
            "text": "To reset your password, go to Settings > Security > Reset Password. Enter your email address and click 'Send Reset Link'. Check your email for the reset link. The link expires in 24 hours.",
            "tags": ["faq", "account", "password"],
            "metadata": {"category": "Account Management", "difficulty": "easy"}
        },
        {
            "title": "Billing Cycle Explanation",
            "text": "Your billing cycle starts on the date you first subscribed. Charges are processed on the same day each month. If you upgrade mid-cycle, you're charged the prorated difference immediately.",
            "tags": ["faq", "billing", "subscription"],
            "metadata": {"category": "Billing", "difficulty": "medium"}
        }
    ],
    collection="support"
)

# Agent searching for answer
results = search_summaries("customer can't log in password not working", collection="support")
```

### 13.5 Personal Note-Taking System

**Scenario:** Use as a personal knowledge management tool.

```yaml
knowledge_base:
  enabled: true
  kb_dir: ~/notes
  poll_interval: 10.0
```

Organize your notes:
```
~/notes/
├── daily/
│   ├── 2026-02-09.md
│   └── 2026-02-08.md
├── projects/
│   ├── home-renovation.md
│   └── garden-planning.md
├── learning/
│   ├── rust-notes.md
│   └── ml-course-notes.md
└── recipes/
    ├── pasta-carbonara.md
    └── sourdough-bread.md
```

**Usage:**
```python
# "What did I note about Rust error handling?"
results = search_summaries("Rust error handling Result Option", tags_filter=["folder:learning"])

# "What's my sourdough recipe?"
results = search_summaries("sourdough bread recipe", tags_filter=["folder:recipes"])
```

### 13.6 Multi-Tenant SaaS Application

**Scenario:** Each tenant has isolated documents in separate collections.

```python
# Tenant A uploads a document
ingest_document(
    title="Tenant A Internal Policy",
    text="...",
    collection="tenant_a",
    metadata={"tenant_id": "a"}
)

# Tenant B uploads a document
ingest_document(
    title="Tenant B Strategy Doc",
    text="...",
    collection="tenant_b",
    metadata={"tenant_id": "b"}
)

# Tenant A searches — only sees their documents
results = search_summaries("policy", collection="tenant_a")
# Returns only Tenant A's documents

# Tenant B searches — only sees their documents
results = search_summaries("strategy", collection="tenant_b")
# Returns only Tenant B's documents
```

Collections provide complete data isolation — no cross-tenant data leakage.

---

## 14. Testing

### 14.1 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=staged_rag --cov-report=term-missing

# Run a specific test file
pytest tests/test_document_store.py -v

# Run a specific test function
pytest tests/test_vector_index.py::test_upsert_and_search -v

# Run only fast tests (no API calls)
pytest tests/ -v -k "not embedding"
```

**Test files and what they cover:**

| File | Coverage |
|---|---|
| `test_document_store.py` | CRUD on JSON store, collection isolation |
| `test_vector_index.py` | Vector upsert, delete, search, persistence |
| `test_embeddings.py` | Provider initialization, encoding |
| `test_tools.py` | MCP tool function signatures and responses |
| `test_agent_flow.py` | End-to-end staged retrieval workflows |

### 14.2 Seeding Sample Data

Load sample documents for testing:

```bash
python scripts/seed_mock_data.py
```

This populates the default collection with sample documents from `data/mock/documents.json`.

### 14.3 Inspecting Data Store State

View the current state of your data:

```bash
python scripts/inspect_state.py
```

This shows:
- Number of documents per collection
- Total tokens indexed
- Index file sizes
- Recent document titles

---

## 15. Performance Tuning

### 15.1 Optimising Search Quality

| Issue | Solution |
|---|---|
| Results are semantically related but miss exact terms | Use `hybrid_search` with `keyword_weight: 0.5` |
| Single query doesn't capture the full topic | Use `multi_query_search` with 2-4 query variations |
| Too many irrelevant results | Increase `min_score` to 0.3–0.5 |
| Auto-generated summaries are poor | Provide custom summaries via `summary` parameter |
| Documents about the same topic but using different terminology | Use `multi_query_search` with synonyms as separate queries |
| Need to understand why results ranked poorly | Use `explain_retrieval` to debug scoring |

### 15.2 Reducing API Costs

| Strategy | How |
|---|---|
| Use local embeddings | Switch to Ollama or HuggingFace (free, no API calls) |
| Reduce embedding dimensions | Lower `dimensions` (e.g., 768 instead of 3072) |
| Provide pre-computed summaries | Skip Gemini summary generation by passing `summary` |
| Disable auto_summary | Set `ingestion.auto_summary: false` in config |
| Use the deterministic fallback | No API key needed (lower quality but free) |
| Rate limiting built-in | The engine paces at 80 RPM automatically |

### 15.3 Handling Large Collections

For collections with 10,000+ documents:

```yaml
# config.local.yaml
retrieval:
  default_top_k: 10         # Don't retrieve too many at once
  max_top_k: 100             # Allow larger retrieval when needed

chunking:
  chunk_size: 300            # Larger chunks = fewer chunks = smaller index
  min_chunk_size: 80         # Don't keep tiny fragments

ingestion:
  max_batch_size: 100        # Larger batches for efficiency
```

**Additional tips:**
- Install FAISS for faster vector search: `pip install -e ".[faiss]"`
- Use collections to partition documents by topic
- Archive old documents to separate collections
- Monitor index size with `collection_stats`

---

## 16. Security Best Practices

| Area | Recommendation |
|---|---|
| **API Keys** | Store in `.env` file (gitignored). Never hardcode in YAML or Python files. |
| **Network** | Bind to `127.0.0.1` (localhost only, default). Use reverse proxy for remote access. |
| **Data at rest** | Document store is plaintext JSON. Enable disk encryption for sensitive data. |
| **Audit logs** | May contain query text. Set appropriate `max_log_entries` for retention. |
| **File permissions** | Restrict access to `data/` directory and `.env` file. |
| **KB folder** | Only place trusted files in `knowledge_base/`. The server reads and processes them. |
| **HTTPS** | Use a reverse proxy (nginx, Caddy) with TLS for production HTTP transport. |
| **Authentication** | MCP server has no built-in auth. Use VPN, firewall, or reverse proxy auth. |

---

## 17. Troubleshooting

### 17.1 Installation Problems

**Problem:** `pip install -e .` fails with Python version error.

```
ERROR: This project requires Python >=3.11
```

**Solution:**
```bash
python --version
# If below 3.11, install Python 3.11+ from https://python.org
# Or use pyenv: pyenv install 3.12 && pyenv local 3.12
```

---

**Problem:** `ModuleNotFoundError: No module named 'google.genai'`

**Solution:**
```bash
pip install google-genai
# Or reinstall the package:
pip install -e .
```

---

**Problem:** `ModuleNotFoundError: No module named 'fastmcp'`

**Solution:**
```bash
pip install "fastmcp>=0.5.0"
```

---

**Problem:** `ModuleNotFoundError: No module named 'openai'` (when using OpenAI/Azure/LMStudio)

**Solution:**
```bash
pip install -e ".[openai]"
```

---

**Problem:** `ModuleNotFoundError: No module named 'ollama'`

**Solution:**
```bash
pip install -e ".[ollama]"
# Also ensure Ollama is installed and running: https://ollama.ai
```

---

**Problem:** `ModuleNotFoundError: No module named 'sentence_transformers'`

**Solution:**
```bash
pip install -e ".[huggingface]"
```

---

**Problem:** `pip install -e .` hangs or takes very long.

**Solution:**
```bash
# Use a faster index
pip install -e . --index-url https://pypi.org/simple/

# Or install with verbose output to see what's happening
pip install -e . -v
```

### 17.2 Server Startup Issues

**Problem:** Server starts but immediately exits.

**Possible causes:**
1. Missing `.env` file or API key
2. Port already in use
3. Invalid configuration

**Debug steps:**
```bash
# Run with debug logging
# Add to config.local.yaml:
#   logging:
#     log_level: DEBUG

python -m staged_rag.server
```

---

**Problem:** `OSError: [Errno 48] Address already in use` (or `[WinError 10048]` on Windows)

**Solution:**
```bash
# Find what's using the port (Windows)
netstat -ano | findstr :8090

# Kill the process (replace PID)
taskkill /F /PID <PID>

# Or use a different port in config.local.yaml:
# server:
#   port: 9090
```

---

**Problem:** `PermissionError: [Errno 13] Permission denied: 'data/store/default.json'`

**Solution:**
```bash
# Check file permissions
ls -la data/store/

# Fix permissions (Linux/macOS)
chmod -R 755 data/

# On Windows, right-click → Properties → Security → edit permissions
```

---

**Problem:** Server starts but no tools are available in the MCP client.

**Solution:**
1. Verify the transport mode matches your client setup
2. For HTTP mode: ensure the URL is `http://127.0.0.1:8090/mcp` (note the `/mcp` path)
3. For STDIO mode: ensure `config.local.yaml` has `server.transport: stdio`
4. Restart the MCP client after configuration changes

### 17.3 Embedding & API Errors

**Problem:** `WARNING: Embedding API unavailable, using deterministic fallback`

**Cause:** The embedding provider API is not accessible.

**Solutions:**
1. Check your API key: `echo $GEMINI_API_KEY` (or `$env:GEMINI_API_KEY` on Windows PowerShell)
2. Verify the `.env` file is in the project root directory
3. Test the API key directly:
   ```bash
   curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_KEY"
   ```
4. If using Ollama, verify it's running: `ollama list`
5. If using LM Studio, verify the server is started

---

**Problem:** `429 Too Many Requests` / Rate limit errors

**Solution:**
The system automatically handles rate limiting (80 RPM pacing), but if you're hitting limits:
```yaml
# Reduce batch size
embedding:
  batch_size: 8       # Default is 32; lower = fewer simultaneous requests

# Or switch to a local provider (no rate limits)
embedding:
  provider: ollama
  model: nomic-embed-text
  dimensions: 768
```

---

**Problem:** `Error: Document exceeds max tokens (50000)`

**Solution:**
```yaml
# Increase the limit in config.local.yaml
ingestion:
  max_document_tokens: 100000
```

Or split the document into smaller parts before ingesting.

---

**Problem:** Embedding dimensions mismatch error

**Cause:** You changed the embedding provider or model without clearing old indexes.

**Solution:**
```bash
# Delete old vector indexes
rm data/index/*.npz

# Restart the server
python -m staged_rag.server

# If using knowledge base, force resync
# Call kb_resync() from your MCP client
```

### 17.4 Search Quality Issues

**Problem:** Search returns no results.

**Checklist:**
1. Verify documents are indexed: `collection_stats("default")`
2. Check the collection name matches: `list_collections()`
3. Try with `min_score=0.0` (the default)
4. Check if the query is empty or whitespace-only
5. If using `tags_filter`, verify documents have the expected tags

---

**Problem:** Search returns irrelevant results.

**Solutions:**
1. Use `hybrid_search` to combine semantic and keyword scoring
2. Try `multi_query_search` with query variations
3. Use `explain_retrieval` to understand why documents ranked:
   ```python
   explain_retrieval(
       query="your query",
       doc_ids=["id-of-irrelevant-result"]
   )
   ```
4. Improve document summaries (custom summaries often outperform auto-generated ones)
5. Increase `min_score` to filter low-quality matches

---

**Problem:** Low similarity scores even for obviously relevant documents.

**Possible causes:**
1. Using deterministic fallback instead of real embeddings (check logs for warnings)
2. Embedding dimensions mismatch between config and provider
3. Mixed embedding providers in the same collection (old vectors from provider A, new from provider B)

**Solution:**
```bash
# Force re-index everything
rm data/index/*.npz
# Restart and re-ingest, or call kb_resync()
```

---

**Problem:** Exact keyword matches not found.

**Solution:** Use `hybrid_search` with higher keyword weight:
```python
results = hybrid_search(
    query="exact-technical-term",
    semantic_weight=0.3,
    keyword_weight=0.7
)
```

### 17.5 Knowledge Base Issues

**Problem:** Files in `knowledge_base/` are not being indexed.

**Checklist:**
1. Verify KB is enabled: check `knowledge_base.enabled: true` in config
2. Check file extension is supported (see supported extensions list in [Section 8.7](#87-understanding-auto-generated-tags))
3. Check file size: default limit is 10 MB
4. Check KB status: `kb_status()`
5. Check manifest for errors: review `data/kb_manifest.json`
6. Look for watcher log messages in server output

---

**Problem:** PDF files show "error" in the manifest.

**Common causes:**
1. **Image-only/scanned PDF** — no extractable text. Solution: use OCR externally first
2. **Encrypted PDF** — requires password. Solution: decrypt first
3. **Corrupted PDF** — invalid file. Solution: re-download or re-create
4. **pypdf not installed** — Solution: `pip install pypdf>=4.0.0`

---

**Problem:** Knowledge base files have incorrect titles.

**How titles are determined (in priority order):**
1. For PDFs: `/Title` from PDF metadata
2. First meaningful line of text (≥5 characters, not a number)
3. Cleaned filename (hyphens/underscores → spaces, title-cased)

**Solution:** For better titles:
- Set the PDF `/Title` metadata field before ingesting
- Start your text files with a clear title on the first line
- Use descriptive filenames

---

**Problem:** Manifest out of sync / stale data.

**Solution:**
```python
# Force complete re-sync
kb_resync()
```

This deletes all KB documents, clears the manifest, and re-ingests everything from scratch.

### 17.6 Data & Storage Issues

**Problem:** Index file is corrupted or inconsistent.

**Solution:**
```bash
# Delete the corrupted index
rm data/index/default.npz        # For default collection
# Or: rm data/index/<collection>.npz

# Restart the server — the index rebuild happens automatically
# For KB documents, run kb_resync()
# For manually ingested documents, you'll need to re-ingest them
```

---

**Problem:** Audit log file is very large.

**Solution:**
```yaml
# Reduce max entries in config.local.yaml
logging:
  max_log_entries: 1000        # Default is 10000
```

Or manually clear the log:
```bash
# Delete the log file (a new one is created automatically)
rm data/logs/audit.jsonl
```

---

**Problem:** JSON store file is corrupted.

**Solution:**
```bash
# Check if the file is valid JSON
python -c "import json; json.load(open('data/store/default.json'))"

# If corrupted, you may need to restore from backup
# Or delete and re-ingest all documents:
rm data/store/default.json
rm data/index/default.npz
# Re-ingest all documents
```

### 17.7 MCP Client Connection Issues

**Problem:** VS Code shows "MCP server not responding."

**Solutions:**
1. **HTTP mode:** Verify the server is running (`python -m staged_rag.server`) and check the URL includes `/mcp`:
   ```json
   {"url": "http://127.0.0.1:8090/mcp"}
   ```
2. **STDIO mode:** Verify the path to the Python executable and the working directory are correct
3. Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"

---

**Problem:** Claude Desktop doesn't show the MCP server.

**Solutions:**
1. Verify `config.local.yaml` has `server.transport: stdio`
2. Check the path in `claude_desktop_config.json` is absolute and correct
3. Ensure the Python executable in the config can find the `staged_rag` module
4. Restart Claude Desktop completely (not just the window)

---

**Problem:** Tools show in client but calls fail with timeout.

**Possible cause:** Long embedding API calls or large document processing.

**Solutions:**
1. Switch to a faster embedding provider or reduce batch size
2. Increase client-side timeout settings
3. Check network connectivity to the embedding API

### 17.8 Common Error Messages Explained

| Error Message | Cause | Fix |
|---|---|---|
| `{"error": "Title must not be empty"}` | Empty string passed as `title` to `ingest_document` | Provide a non-empty title |
| `{"error": "Text must not be empty"}` | Empty string passed as `text` to `ingest_document` | Provide document text |
| `{"error": "Document exceeds max tokens"}` | Document text exceeds `max_document_tokens` | Increase limit in config or split document |
| `{"error": "Document not found"}` | Invalid `doc_id` passed to `get_document_chunk`, `update_document`, or `get_document_metadata` | Verify the doc_id exists (use `search_summaries` first) |
| `{"error": "Provide chunk_index or chunk_query"}` | Neither `chunk_index` nor `chunk_query` provided to `get_document_chunk` | Pass one of the two parameters |
| `{"error": "chunk_index out of range"}` | `chunk_index` exceeds the number of chunks in the document | Check `total_chunks` in the response or first call `get_document_metadata` |
| `{"error": "Batch size exceeds maximum"}` | More documents than `max_batch_size` in `ingest_batch` | Reduce batch size or increase `ingestion.max_batch_size` in config |
| `{"deleted": false}` | `delete_document` called with non-existent `doc_id` | The document was already deleted or never existed |
| `{"enabled": false}` | KB tool called but KB is disabled | Set `knowledge_base.enabled: true` in config |

---

## 18. FAQ

**Q: Can I use this without any API key?**

A: Yes. Use Ollama for fully local embeddings (free, no API needed). The system also has a built-in deterministic fallback that works without any API, though similarity search quality is lower. Summary generation falls back to local extractive summarisation.

---

**Q: How many documents can the system handle?**

A: The JSON + NumPy storage backend handles up to ~100K documents efficiently. Vector search is O(n) linear scan — still fast with NumPy for up to 100K vectors. For larger collections, install FAISS: `pip install -e ".[faiss]"`.

---

**Q: Can I use multiple embedding providers at the same time?**

A: Not simultaneously. The system uses one provider at a time (configured in `config.yaml`). If you switch providers, delete old vector indexes and re-ingest to avoid dimension mismatches.

---

**Q: Is the data stored locally or in the cloud?**

A: Everything is stored locally:
- Documents: `data/store/*.json`
- Vectors: `data/index/*.npz`
- Audit logs: `data/logs/audit.jsonl`
- KB manifest: `data/kb_manifest.json`

No external database is needed. Only API calls for embeddings and summary generation leave your machine (unless using local providers like Ollama).

---

**Q: What happens if the server crashes mid-ingestion?**

A: Each document is persisted immediately after ingestion. The JSON store and vector index are saved to disk after each operation. If the server crashes, you may lose only the in-progress document. The BM25 index (in-memory) is rebuilt automatically on next startup.

---

**Q: Can I backup and restore data?**

A: Yes. Simply copy the `data/` directory:
```bash
# Backup
cp -r data/ data-backup-$(date +%Y%m%d)/

# Restore
cp -r data-backup-20260209/ data/
```

---

**Q: How does the two-level retrieval save tokens?**

A: Traditional RAG retrieves 5 full documents and pushes them all into the LLM context. If each document is 2000 tokens, that's 10,000 tokens. With Staged RAG:
- Level 1 returns only summaries (~100 tokens each × 5 = ~500 tokens)
- You evaluate and decide only 2 of 5 are relevant
- Level 2 fetches only those 2 documents = 4,000 tokens
- **Savings: 6,000 tokens (60%)**

For Level 2.5 (single chunk retrieval), savings can be even greater when dealing with very long documents.

---

**Q: Can I use this for real-time search in a web application?**

A: Yes, via the HTTP transport mode. The server listens on a configurable host:port and exposes tools via the MCP protocol. Your web backend can make MCP calls to the server. For production use, place it behind a reverse proxy (nginx/Caddy) with TLS and authentication.

---

**Q: How do I migrate from another RAG system?**

A: Extract your documents and use `ingest_batch` to load them:
```python
# Export from your old system and format as:
documents = [
    {"title": "Doc 1", "text": "...", "tags": ["..."], "metadata": {...}},
    {"title": "Doc 2", "text": "...", "tags": ["..."], "metadata": {...}},
    # ...
]

# Ingest in batches of 50
for i in range(0, len(documents), 50):
    batch = documents[i:i+50]
    result = ingest_batch(documents=batch)
    print(f"Batch {i//50 + 1}: {result['succeeded']}/{result['total']} succeeded")
```

---

**Q: What file types does the knowledge base support?**

A: Text files (`.txt`, `.md`, `.markdown`, `.rst`), data files (`.json`, `.yaml`, `.yml`, `.csv`, `.tsv`), code files (`.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.h`, `.go`, `.rs`), web files (`.html`, `.htm`, `.xml`), config files (`.log`, `.cfg`, `.ini`, `.toml`), and documents (`.pdf`).

---

**Q: How do I reset everything and start fresh?**

A: Delete the data directory and restart:
```bash
# Stop the server first
rm -rf data/store/ data/index/ data/logs/ data/kb_manifest.json
python -m staged_rag.server
# The directories are recreated automatically
```

---

<p align="center">
  <strong>Staged RAG MCP Server — How to Use Guide</strong><br>
  <em>Search smart. Retrieve less. Answer better.</em><br><br>
  Copyright &copy; 2026-present Shashidhar Reddy Nalamari. All Rights Reserved.<br>
  For the full project documentation, see <a href="README.md">README.md</a>.
</p>
