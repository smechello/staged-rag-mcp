<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/License-Custom-green" alt="License">
  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blueviolet" alt="MCP">
  <img src="https://img.shields.io/badge/RAG-Retrieval%20Augmented%20Generation-orange" alt="RAG">
  <img src="https://img.shields.io/badge/Version-0.1.0-brightgreen" alt="Version 0.1.0">
</p>

<h1 align="center">Staged RAG MCP Server</h1>

<p align="center">
  <strong>A production-grade, two-level Retrieval-Augmented Generation server built on the Model Context Protocol (MCP)</strong>
</p>

<p align="center">
  <em>Search smart. Retrieve less. Answer better.</em>
</p>

<p align="center">
  Created by <strong>Shashidhar Reddy Nalamari</strong> &bull;
  <a href="mailto:nalamarishashidharreddy@gmail.com">nalamarishashidharreddy@gmail.com</a>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
  - [System Architecture Diagram](#system-architecture-diagram)
  - [Two-Level Retrieval Pipeline](#two-level-retrieval-pipeline)
  - [Data Flow](#data-flow)
  - [Component Architecture](#component-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Basic Installation](#basic-installation)
  - [Installation with Optional Providers](#installation-with-optional-providers)
  - [Development Installation](#development-installation)
- [Configuration](#configuration)
  - [Configuration Files](#configuration-files)
  - [Server Configuration](#server-configuration)
  - [Embedding Configuration](#embedding-configuration)
  - [Generation Configuration](#generation-configuration)
  - [Chunking Configuration](#chunking-configuration)
  - [Retrieval Configuration](#retrieval-configuration)
  - [Storage Configuration](#storage-configuration)
  - [Ingestion Configuration](#ingestion-configuration)
  - [Logging Configuration](#logging-configuration)
  - [Knowledge Base Configuration](#knowledge-base-configuration)
  - [Environment Variables](#environment-variables)
  - [Full Configuration Reference](#full-configuration-reference)
- [Quick Start](#quick-start)
- [How to Use Guide](#how-to-use-guide)
- [Running the Server](#running-the-server)
  - [Standard Mode (Streamable HTTP)](#standard-mode-streamable-http)
  - [STDIO Mode](#stdio-mode)
  - [With Knowledge Base Watcher](#with-knowledge-base-watcher)
- [Embedding Providers](#embedding-providers)
  - [Google Gemini (Default)](#google-gemini-default)
  - [OpenAI](#openai)
  - [Ollama (Local)](#ollama-local)
  - [HuggingFace](#huggingface)
  - [Azure OpenAI](#azure-openai)
  - [Together AI](#together-ai)
  - [LM Studio (Local)](#lm-studio-local)
  - [Switching Providers](#switching-providers)
  - [Deterministic Fallback](#deterministic-fallback)
- [MCP Tools Reference](#mcp-tools-reference)
  - [Retrieval Tools](#retrieval-tools)
    - [search_summaries](#search_summaries)
    - [get_documents](#get_documents)
    - [get_document_chunk](#get_document_chunk)
  - [Advanced Search Tools](#advanced-search-tools)
    - [hybrid_search](#hybrid_search)
    - [multi_query_search](#multi_query_search)
    - [find_similar](#find_similar)
  - [Document Management Tools](#document-management-tools)
    - [ingest_document](#ingest_document)
    - [ingest_batch](#ingest_batch)
    - [update_document](#update_document)
    - [delete_document](#delete_document)
  - [Metadata Tools](#metadata-tools)
    - [get_document_metadata](#get_document_metadata)
  - [Observability Tools](#observability-tools)
    - [collection_stats](#collection_stats)
    - [list_collections](#list_collections)
    - [explain_retrieval](#explain_retrieval)
    - [retrieval_log](#retrieval_log)
  - [Knowledge Base Tools](#knowledge-base-tools)
    - [kb_status](#kb_status)
    - [kb_resync](#kb_resync)
- [Knowledge Base System](#knowledge-base-system)
  - [Overview](#kb-overview)
  - [How It Works](#how-it-works)
  - [Supported File Types](#supported-file-types)
  - [Auto-Generated Tags](#auto-generated-tags)
  - [PDF Support](#pdf-support)
  - [Manifest Tracking](#manifest-tracking)
  - [Folder Organization](#folder-organization)
  - [Initial Sync vs Background Watcher](#initial-sync-vs-background-watcher)
- [Document Lifecycle](#document-lifecycle)
  - [Ingestion Pipeline](#ingestion-pipeline)
  - [Document Model](#document-model)
  - [Chunking Strategy](#chunking-strategy)
  - [Summary Generation](#summary-generation)
  - [Embedding and Indexing](#embedding-and-indexing)
- [Search and Retrieval](#search-and-retrieval)
  - [Semantic Search](#semantic-search)
  - [BM25 Keyword Search](#bm25-keyword-search)
  - [Hybrid Search](#hybrid-search-details)
  - [Multi-Query Fusion](#multi-query-fusion)
  - [Similarity Search](#similarity-search)
  - [Scoring and Ranking](#scoring-and-ranking)
- [Collections](#collections)
  - [What Are Collections](#what-are-collections)
  - [Creating Collections](#creating-collections)
  - [Multi-Collection Strategy](#multi-collection-strategy)
  - [Collection Statistics](#collection-statistics)
- [Storage Backend](#storage-backend)
  - [Document Store (JSON)](#document-store-json)
  - [Vector Index (NumPy)](#vector-index-numpy)
  - [BM25 Index (In-Memory)](#bm25-index-in-memory)
  - [Audit Log (JSONL)](#audit-log-jsonl)
  - [KB Manifest (JSON)](#kb-manifest-json)
- [Observability and Auditing](#observability-and-auditing)
  - [Audit Logging](#audit-logging)
  - [Retrieval Explanation](#retrieval-explanation)
  - [Collection Monitoring](#collection-monitoring)
- [Integration with MCP Clients](#integration-with-mcp-clients)
  - [VS Code / GitHub Copilot](#vs-code--github-copilot)
  - [Claude Desktop](#claude-desktop)
  - [Custom MCP Clients](#custom-mcp-clients)
- [Prompt Engineering for Staged RAG](#prompt-engineering-for-staged-rag)
  - [System Prompt](#system-prompt)
  - [Evaluate Summaries Prompt](#evaluate-summaries-prompt)
  - [Deep Analysis Prompt](#deep-analysis-prompt)
- [Testing](#testing)
  - [Running Tests](#running-tests)
  - [Test Structure](#test-structure)
  - [Writing New Tests](#writing-new-tests)
- [Performance Considerations](#performance-considerations)
  - [Rate Limiting](#rate-limiting)
  - [Token Budget Management](#token-budget-management)
  - [Embedding Caching](#embedding-caching)
  - [Index Performance](#index-performance)
- [Security](#security)
  - [API Key Management](#api-key-management)
  - [Data Privacy](#data-privacy)
  - [Access Control](#access-control)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Author](#author)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**Staged RAG MCP Server** is a sophisticated retrieval-augmented generation system that implements a two-level retrieval pipeline via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Unlike traditional RAG systems that dump entire documents into LLM context windows, Staged RAG uses a **search-then-expand** strategy: first retrieve lightweight summaries to identify relevant documents, then selectively fetch full content only for the documents that matter.

This approach dramatically reduces token consumption, improves response quality, and provides full auditability of every retrieval decision.

### Why Staged RAG?

Traditional RAG systems have a fundamental problem: they retrieve K documents and push all of them into the LLM context, whether or not every document is truly relevant. This leads to:

- **Wasted tokens**: Irrelevant documents consume expensive context window space
- **Diluted attention**: Important information gets lost among noise
- **No transparency**: Users can't see why certain documents were selected
- **Higher latency**: Processing unnecessary text slows responses

Staged RAG solves these problems by introducing a two-level retrieval pipeline:

```
Level 1: Search Summaries    →    Compact summaries + scores (cheap)
         ↓ (evaluate)
Level 2: Get Full Documents   →    Complete text + chunks (selective)
         ↓ (optional)
Level 2.5: Get Specific Chunk →    Single chunk (surgical)
```

The LLM (or user) inspects Level 1 results and decides which documents warrant full expansion. This means you only pay for the tokens you actually need.

### Key Differentiators

| Feature | Traditional RAG | Staged RAG MCP |
|---------|----------------|----------------|
| Retrieval strategy | Single-pass: retrieve & inject | Two-pass: summarize → expand |
| Token efficiency | Low — all K docs in context | High — only relevant docs expanded |
| Transparency | Black box | Full audit trail per retrieval |
| Search modes | Typically one (semantic) | Semantic, BM25, Hybrid, Multi-query |
| Protocol | Custom API | MCP standard — works with any MCP client |
| Knowledge base | Manual ingestion only | Auto-sync folder with file watcher |
| Embedding providers | Usually one | 7 providers: Gemini, OpenAI, Ollama, HuggingFace, Azure, Together, LM Studio |

---

## Key Features

### Core Retrieval

- **Two-Level Staged Retrieval** — Search summaries first (Level 1), then expand selected documents (Level 2), with optional single-chunk retrieval (Level 2.5)
- **Semantic Search** — Vector similarity search using state-of-the-art embedding models
- **BM25 Keyword Search** — Classic TF-IDF-based keyword matching via Okapi BM25
- **Hybrid Search** — Configurable blend of semantic and keyword scores with normalised weights
- **Multi-Query Fusion** — Run multiple queries and merge results using Reciprocal Rank Fusion (RRF) or max-score aggregation
- **Similar Document Discovery** — Find documents semantically similar to a reference document

### Document Management

- **Single Document Ingestion** — Add documents with title, text, tags, metadata, and optional pre-computed summaries
- **Batch Ingestion** — Bulk ingest up to 50 documents in a single operation
- **Document Updates** — Modify metadata, tags, or full text (triggers automatic re-chunking and re-embedding)
- **Document Deletion** — Remove documents with automatic index cleanup (vector index + BM25 rebuild)
- **Token Counting** — Automatic token counting for budget management

### Knowledge Base (Auto-Sync Folder)

- **Folder Watcher** — Background polling-based file watcher (no OS-specific event dependencies)
- **Automatic Ingestion** — Drop files into `knowledge_base/` and they're instantly indexed
- **Change Detection** — SHA-256 hash-based change detection; modified files are automatically re-indexed
- **Deletion Tracking** — Removed files are automatically cleaned from the vector store
- **PDF Support** — Full PDF text extraction via `pypdf` with metadata title extraction
- **Manifest Tracking** — Persistent JSON manifest maps files to document IDs across server restarts
- **Auto-Tagging** — Files are automatically tagged by extension, source, and subfolder location
- **Text Cleaning** — Smart cleanup of PDF artifacts: page numbers, CamelCase joins, excessive whitespace

### Embedding Providers

- **Google Gemini** — Default provider using `gemini-embedding-001` (3072 dimensions)
- **OpenAI** — `text-embedding-3-small` / `text-embedding-3-large`
- **Ollama** — Local models like `nomic-embed-text` (no API key needed)
- **HuggingFace** — Local `sentence-transformers` or HuggingFace Inference API
- **Azure OpenAI** — Enterprise Azure OpenAI deployments
- **Together AI** — Together AI embedding models
- **LM Studio** — Local OpenAI-compatible embeddings via LM Studio
- **Deterministic Fallback** — SHA-256-based deterministic vectors when no API is available

### Observability

- **Audit Logging** — Every tool call logged to JSONL with timestamp, parameters, result count, doc IDs, and latency
- **Retrieval Explanation** — Inspect cosine similarity, BM25 scores, and term overlap for any query-document pair
- **Collection Statistics** — Document counts, token totals, tag/source distributions, index sizes
- **Retrieval Log** — Query recent audit entries with tool and session filters
- **Rate Limiting** — Built-in request pacing (80 RPM) to stay within API free tiers

### Architecture

- **MCP Standard** — Built on the Model Context Protocol via FastMCP; works with VS Code, Claude Desktop, and any MCP client
- **Provider-Agnostic Embeddings** — Factory pattern with lazy imports; optional dependencies only loaded when selected
- **Thread-Safe** — All stores, indexes, and loggers use thread locks for concurrent safety
- **Crash-Resilient Tools** — Every MCP tool is wrapped in error-catching decorator; server never crashes on tool failures
- **Configurable via YAML** — Base config + local overrides; environment variables for secrets
- **Zero External Services** — No database server required; everything stored as local JSON + NumPy files

---

## Architecture

### System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          MCP CLIENT                                      │
│                  (VS Code / Claude / Custom)                             │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │  MCP Protocol (HTTP / STDIO)
                           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        MCP SERVER (FastMCP)                              │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    server.py — Tool Registry                       │  │
│  │                                                                    │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │  │
│  │  │  Retrieval   │  │  Management  │  │  Observability           │  │  │
│  │  │  Tools       │  │  Tools       │  │  Tools                   │  │  │
│  │  │              │  │              │  │                          │  │  │
│  │  │ search_      │  │ ingest_      │  │ collection_stats         │  │  │
│  │  │  summaries   │  │  document    │  │ list_collections         │  │  │
│  │  │ get_         │  │ ingest_batch │  │ explain_retrieval        │  │  │
│  │  │  documents   │  │ update_      │  │ retrieval_log            │  │  │
│  │  │ get_document │  │  document    │  │                          │  │  │
│  │  │  _chunk      │  │ delete_      │  │                          │  │  │
│  │  │ hybrid_      │  │  document    │  │                          │  │  │
│  │  │  search      │  │              │  │                          │  │  │
│  │  │ multi_query  │  │              │  │                          │  │  │
│  │  │  _search     │  │              │  │                          │  │  │
│  │  │ find_similar │  │              │  │                          │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER (service.py)                          │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │ RAGService     │  │ KBManager      │  │ SummaryGenerator           │  │
│  │ (Singleton)    │  │ (Singleton)    │  │ (Gemini / Local Fallback)  │  │
│  └───────┬────────┘  └───────┬────────┘  └────────────────────────────┘  │
│          │                   │                                           │
└──────────┼───────────────────┼───────────────────────────────────────────┘
           │                   │
           ▼                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         CORE LAYER                                       │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐   │
│  │ DocumentStore│  │ VectorIndex  │  │ BM25Scorer   │  │ ChunkManager│   │
│  │ (JSON)       │  │ (NumPy)      │  │ (rank-bm25)  │  │ (Sentence)  │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘  └─────────────┘   │
│         │                 │                                              │
│  ┌──────┴─────────────────┴──────────────────────────────────────────┐   │
│  │                    EmbeddingEngine                                │   │
│  │  ┌─────────┐ ┌────────┐ ┌────────┐ ┌────────────┐ ┌────────────┐  │   │
│  │  │ Gemini  │ │ OpenAI │ │ Ollama │ │ HuggingFace│ │ Together   │  │   │
│  │  └─────────┘ └────────┘ └────────┘ └────────────┘ └────────────┘  │   │
│  │  ┌──────────────┐ ┌──────────┐ ┌──────────────────────────────┐   │   │
│  │  │ Azure OpenAI │ │ LMStudio │ │ Deterministic Fallback       │   │   │
│  │  └──────────────┘ └──────────┘ └──────────────────────────────┘   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐    │
│  │ FileWatcher  │  │ KBManifest   │  │ AuditLogger                  │    │
│  │ (Polling)    │  │ (JSON)       │  │ (JSONL)                      │    │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
           │                 │                            │
           ▼                 ▼                            ▼
┌──────────────┐  ┌──────────────┐             ┌──────────────────┐
│ data/store/  │  │ data/index/  │             │ data/logs/       │
│ *.json       │  │ *.npz        │             │ audit.jsonl      │
└──────────────┘  └──────────────┘             └──────────────────┘
```

### Two-Level Retrieval Pipeline

The core innovation of Staged RAG is the two-level retrieval pipeline:

```
                    User Query
                        │
                        ▼
              ┌─────────────────┐
              │  LEVEL 1:       │
              │  search_        │     Lightweight — returns only
              │  summaries()    │     summaries + similarity scores
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  EVALUATE:      │     LLM or user inspects summaries
              │  Inspect scores │     and decides which docs to expand
              │  & summaries    │
              └────────┬────────┘
                       │
            ┌──────────┼──────────┐
            │          │          │
            ▼          ▼          ▼
     ┌──────────┐ ┌──────────┐ ┌──────────┐
     │ SKIP     │ │ LEVEL 2: │ │ LEVEL 2: │     Selective — only fetch
     │ (low     │ │ get_     │ │ get_     │     documents that scored
     │  score)  │ │ documents│ │ documents│     above threshold
     └──────────┘ └────┬─────┘ └────┬─────┘
                       │            │
                       ▼            ▼
              ┌─────────────────┐
              │  LEVEL 2.5:     │     Surgical — retrieve specific
              │  get_document_  │     chunks within a document
              │  chunk()        │     by index or semantic query
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  SYNTHESIZE:    │     Generate answer using only
              │  Answer with    │     the relevant retrieved content
              │  citations      │
              └─────────────────┘
```

### Data Flow

```
Document Ingestion Flow:
─────────────────────────

  Input Text ──→ Token Count Check ──→ Chunking (sentence-based)
       │                                      │
       ▼                                      ▼
  Summary Generation ──────────────→  Document Model (Pydantic)
       │                                      │
       ▼                                      ▼
  Embedding (provider) ───────────→  Vector Index (NumPy cosine)
       │                                      │
       ▼                                      ▼
  BM25 Index (rebuild) ───────────→  JSON Document Store
       │                                      │
       ▼                                      ▼
  Audit Log Entry ────────────────→  Return doc_id + metadata


Search Flow:
────────────

  Query ──→ Embedding (provider) ──→ Vector Index Search (cosine)
       │                                      │
       ▼                                      ▼
  (Optional) BM25 Score ──────────→  Score Fusion (weighted)
       │                                      │
       ▼                                      ▼
  Filter (tags, min_score) ───────→  Ranked SummaryResults
       │                                      │
       ▼                                      ▼
  Audit Log Entry ────────────────→  Return SearchResponse
```

### Component Architecture

| Component | File | Responsibility |
|-----------|------|----------------|
| **MCP Server** | `server.py` | Tool registration, error wrapping, server lifecycle |
| **RAG Service** | `service.py` | Core orchestration: ingestion, search, updates |
| **Config** | `config.py` | YAML loading, settings dataclasses, merge logic |
| **Document Store** | `core/document_store.py` | JSON-backed per-collection document persistence |
| **Vector Index** | `core/vector_index.py` | NumPy-based cosine similarity index with NPZ persistence |
| **BM25 Scorer** | `core/bm25.py` | Okapi BM25 keyword scoring using `rank-bm25` |
| **Chunk Manager** | `core/chunk_manager.py` | Sentence-based text chunking with overlap |
| **Embedding Engine** | `core/embeddings.py` | Multi-provider embedding with rate limiting and fallback |
| **Summary Generator** | `core/summary_generator.py` | Gemini-based summaries with extractive fallback |
| **KB Manager** | `core/kb_manager.py` | File watcher orchestration, ingestion, re-sync |
| **File Watcher** | `core/file_watcher.py` | Polling-based directory monitor with hash tracking |
| **KB Manifest** | `core/kb_manifest.py` | File-to-doc_id mapping persistence |
| **Audit Logger** | `logging/audit.py` | Thread-safe JSONL audit log with auto-truncation |
| **Embedder Factory** | `embeddings/factory.py` | Lazy-import provider factory |
| **Prompts** | `prompts.py` | Prompt templates for staged retrieval workflow |
| **Utils** | `utils.py` | Text cleaning, sentence splitting, chunking, vector ops |

---

## Project Structure

```
staged-rag-mcp/
│
├── LICENSE                          # Custom license (free use, no false ownership claims)
├── README.md                        # This file — comprehensive project documentation
├── HOWTOUSE.md                      # Detailed usage guide with examples
├── pyproject.toml                   # Python project metadata and dependencies
├── config.yaml                      # Base configuration (version controlled)
├── config.local.yaml                # Local overrides (not version controlled)
├── .env                             # Environment variables (API keys — not committed)
│
├── src/
│   └── staged_rag/                  # Main package
│       ├── __init__.py              # Package version and exports
│       ├── server.py                # MCP server: tool registration, lifecycle
│       ├── service.py               # RAG service: core business logic
│       ├── config.py                # Configuration loading and dataclasses
│       ├── prompts.py               # Prompt templates for staged retrieval
│       ├── utils.py                 # Text processing utilities
│       │
│       ├── core/                    # Core engine components
│       │   ├── __init__.py
│       │   ├── document_store.py    # JSON-backed document persistence
│       │   ├── vector_index.py      # NumPy cosine similarity index
│       │   ├── bm25.py              # BM25 keyword scorer
│       │   ├── chunk_manager.py     # Sentence-based text chunking
│       │   ├── embeddings.py        # Multi-provider embedding engine
│       │   ├── summary_generator.py # AI summary with local fallback
│       │   ├── kb_manager.py        # Knowledge base folder orchestrator
│       │   ├── kb_manifest.py       # File → doc_id manifest tracker
│       │   └── file_watcher.py      # Polling-based file system watcher
│       │
│       ├── embeddings/              # Embedding provider implementations
│       │   ├── __init__.py
│       │   ├── base.py              # Abstract base class (EmbeddingBase)
│       │   ├── configs.py           # Provider configuration dataclasses
│       │   ├── factory.py           # Lazy-import provider factory
│       │   ├── gemini.py            # Google Gemini provider
│       │   ├── openai.py            # OpenAI provider
│       │   ├── ollama.py            # Ollama local provider
│       │   ├── huggingface.py       # HuggingFace (local + API)
│       │   ├── azure_openai.py      # Azure OpenAI provider
│       │   ├── together.py          # Together AI provider
│       │   └── lmstudio.py          # LM Studio local provider
│       │
│       ├── models/                  # Pydantic data models
│       │   ├── __init__.py
│       │   ├── document.py          # Document and DocumentChunk models
│       │   ├── search.py            # SearchResponse and SummaryResult models
│       │   └── audit.py             # AuditLogEntry model
│       │
│       ├── tools/                   # MCP tool implementations
│       │   ├── __init__.py          # Tool re-exports
│       │   ├── retrieval.py         # search_summaries, get_documents, get_document_chunk
│       │   ├── advanced.py          # hybrid_search, multi_query_search, find_similar
│       │   ├── management.py        # ingest, update, delete, kb_status, kb_resync
│       │   ├── metadata.py          # get_document_metadata
│       │   └── observability.py     # collection_stats, explain_retrieval, retrieval_log
│       │
│       ├── resources/               # MCP resource providers
│       │   ├── __init__.py
│       │   └── providers.py         # Document and collection resource URIs
│       │
│       └── logging/                 # Logging and audit
│           ├── __init__.py
│           └── audit.py             # Thread-safe JSONL audit logger
│
├── data/                            # Runtime data directory
│   ├── store/                       # Document store (JSON per collection)
│   │   └── default.json
│   ├── index/                       # Vector indexes (NPZ per collection)
│   │   └── default.npz
│   ├── logs/                        # Audit logs
│   │   └── audit.jsonl
│   ├── mock/                        # Mock data for testing
│   │   └── documents.json
│   └── kb_manifest.json             # Knowledge base manifest
│
├── knowledge_base/                  # Drop files here for auto-ingestion
│   └── README.md
│
├── scripts/                         # Utility scripts
│   ├── seed_mock_data.py            # Seed document store with sample data
│   ├── full_test.py                 # Run comprehensive test suite
│   ├── inspect_state.py             # Inspect current data store state
│   ├── run_eval.py                  # Run retrieval evaluation
│   ├── test_mcp_search.py           # Test MCP search functionality
│   └── test_search.py              # Test search functionality
│
└── tests/                           # Automated tests
    ├── test_agent_flow.py           # End-to-end agent flow tests
    ├── test_document_store.py       # Document store unit tests
    ├── test_embeddings.py           # Embedding provider tests
    ├── test_tools.py                # Tool function tests
    └── test_vector_index.py         # Vector index unit tests
```

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|----------------|-------|
| **Python** | 3.11+ | Uses `match` statements, `X \| Y` type unions |
| **pip** | 21.0+ | For `pyproject.toml` support |
| **API Key** | — | At least one embedding provider API key (see [Embedding Providers](#embedding-providers)) |

### Optional Prerequisites

| Tool | Required For | Install |
|------|-------------|---------|
| **Ollama** | Local embedding models | [ollama.ai](https://ollama.ai) |
| **LM Studio** | Local LM Studio embeddings | [lmstudio.ai](https://lmstudio.ai) |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |

---

## Installation

### Basic Installation

```bash
# Clone the repository
git clone https://github.com/reddynalamari/staged-rag-mcp.git
cd staged-rag-mcp

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install the package in editable mode
pip install -e .
```

### Installation with Optional Providers

```bash
# Install with OpenAI support
pip install -e ".[openai]"

# Install with Ollama support
pip install -e ".[ollama]"

# Install with HuggingFace support
pip install -e ".[huggingface]"

# Install with Together AI support
pip install -e ".[together]"

# Install with FAISS support (faster vector search)
pip install -e ".[faiss]"

# Install ALL optional providers
pip install -e ".[all-providers]"

# Install with development tools
pip install -e ".[dev]"
```

### Development Installation

```bash
# Install everything (all providers + dev tools)
pip install -e ".[all-providers,dev]"

# Verify installation
python -c "from staged_rag import __version__; print(f'Staged RAG MCP v{__version__}')"
```

---

## Configuration

### Configuration Files

The system uses a layered YAML configuration:

1. **Built-in defaults** — Hardcoded in `config.py`
2. **`config.yaml`** — Base project config (version controlled)
3. **`config.local.yaml`** — Local overrides (gitignored, takes highest precedence)

Settings are merged in order: defaults → `config.yaml` → `config.local.yaml`. Any key in a later file overrides the same key from an earlier file.

### Server Configuration

```yaml
server:
  name: staged-rag              # Server name (shown in MCP clients)
  transport: streamable-http    # Transport protocol: "streamable-http" or "stdio"
  host: 127.0.0.1              # Bind address for HTTP transport
  port: 8090                   # Port for HTTP transport
```

**Transport options:**
- `streamable-http` — HTTP-based transport; server runs as a web service on host:port
- `stdio` — Standard I/O transport; used when MCP client spawns the server process

### Embedding Configuration

```yaml
embedding:
  provider: gemini              # Provider name (see Embedding Providers section)
  model: gemini-embedding-001   # Model name (provider-specific)
  dimensions: 3072              # Embedding vector dimensions
  batch_size: 32                # Max texts per embedding batch
  provider_config: {}           # Additional provider-specific config
```

### Generation Configuration

```yaml
generation:
  model: gemini-2.5-flash-lite  # Model for summary generation
  summary_max_sentences: 4      # Max sentences in generated summaries
```

### Chunking Configuration

```yaml
chunking:
  chunk_size: 200               # Target tokens per chunk
  chunk_overlap: 20             # Overlap tokens between adjacent chunks
  min_chunk_size: 50            # Minimum tokens for a chunk to be kept
```

**How chunking works:**
- Text is split into sentences at sentence-ending punctuation (`.`, `!`, `?`)
- Sentences are accumulated until the chunk reaches `chunk_size` tokens
- When a chunk boundary is reached, the last `chunk_overlap` tokens carry over to the next chunk
- Chunks smaller than `min_chunk_size` tokens are discarded (unless they're the only content)

### Retrieval Configuration

```yaml
retrieval:
  default_top_k: 5             # Default number of results per search
  max_top_k: 50                # Maximum allowed top_k (safety cap)
  default_collection: default  # Default collection name
  hybrid_semantic_weight: 0.7  # Semantic score weight in hybrid search
  hybrid_keyword_weight: 0.3   # Keyword score weight in hybrid search
  min_similarity_score: 0.0    # Minimum score threshold for results
```

### Storage Configuration

```yaml
storage:
  data_dir: ./data              # Root data directory
  store_dir: ./data/store       # Document JSON store directory
  index_dir: ./data/index       # Vector index (NPZ) directory
  log_dir: ./data/logs          # Audit log directory
```

**Storage files created:**
- `data/store/<collection>.json` — One JSON file per collection with all documents
- `data/index/<collection>.npz` — One NumPy compressed file per collection with all vectors
- `data/logs/audit.jsonl` — Append-only audit log

### Ingestion Configuration

```yaml
ingestion:
  max_document_tokens: 50000    # Maximum tokens per document (rejects larger)
  max_batch_size: 50            # Maximum documents per batch ingest
  auto_summary: true            # Auto-generate summaries on ingestion
```

### Logging Configuration

```yaml
logging:
  audit_file: ./data/logs/audit.jsonl  # Audit log file path
  max_log_entries: 10000               # Auto-truncate after this many entries
  log_level: INFO                      # Python logging level
```

### Knowledge Base Configuration

```yaml
knowledge_base:
  enabled: true                       # Enable/disable the folder watcher
  kb_dir: ./knowledge_base            # Directory to watch for documents
  manifest_file: ./data/kb_manifest.json  # Manifest tracking file
  collection: default                 # Target collection for KB documents
  poll_interval: 5.0                  # Seconds between file system scans
  max_file_size: 10485760             # Maximum file size in bytes (10 MB)
```

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required for Gemini (default provider)
GEMINI_API_KEY=your_gemini_api_key_here

# Alternative: Google API Key
GOOGLE_API_KEY=your_google_api_key_here

# For OpenAI provider
OPENAI_API_KEY=your_openai_api_key_here

# For Azure OpenAI provider
EMBEDDING_AZURE_OPENAI_API_KEY=your_azure_api_key
EMBEDDING_AZURE_DEPLOYMENT=your_deployment_name
EMBEDDING_AZURE_ENDPOINT=https://your-resource.openai.azure.com/
EMBEDDING_AZURE_API_VERSION=2024-02-01

# For Together AI provider
TOGETHER_API_KEY=your_together_api_key

# For HuggingFace Inference API
HUGGINGFACE_API_KEY=your_hf_api_key
```

### Full Configuration Reference

<details>
<summary>Click to expand — Complete config.yaml with all options and defaults</summary>

```yaml
# ============================================================
# Staged RAG MCP Server — Full Configuration Reference
# ============================================================

server:
  name: staged-rag                   # Server display name
  transport: streamable-http         # "streamable-http" or "stdio"
  host: 127.0.0.1                   # HTTP bind address
  port: 8090                        # HTTP port

embedding:
  provider: gemini                   # gemini | openai | ollama | huggingface
                                     # | azure_openai | together | lmstudio
  model: gemini-embedding-001       # Model name (varies by provider)
  dimensions: 3072                   # Output vector dimensions
  batch_size: 32                     # Batch size for embedding calls
  provider_config: {}                # Provider-specific overrides:
    # ollama_base_url: http://localhost:11434
    # openai_base_url: https://api.openai.com/v1
    # huggingface_base_url: https://api-inference.huggingface.co/...
    # azure_kwargs:
    #   azure_deployment: my-deployment
    #   azure_endpoint: https://my-resource.openai.azure.com/
    #   api_version: 2024-02-01

generation:
  model: gemini-2.5-flash-lite      # Summary generation model
  summary_max_sentences: 4           # Max sentences in summaries

chunking:
  chunk_size: 200                    # Target tokens per chunk
  chunk_overlap: 20                  # Overlap between chunks
  min_chunk_size: 50                 # Minimum tokens per chunk

retrieval:
  default_top_k: 5                  # Default results per search
  max_top_k: 50                     # Maximum allowed top_k
  default_collection: default       # Default collection name
  hybrid_semantic_weight: 0.7       # Semantic weight in hybrid search
  hybrid_keyword_weight: 0.3        # Keyword weight in hybrid search
  min_similarity_score: 0.0         # Score threshold

storage:
  data_dir: ./data
  store_dir: ./data/store
  index_dir: ./data/index
  log_dir: ./data/logs

ingestion:
  max_document_tokens: 50000        # Max tokens per document
  max_batch_size: 50                # Max documents per batch
  auto_summary: true                # Auto-generate summaries

logging:
  audit_file: ./data/logs/audit.jsonl
  max_log_entries: 10000
  log_level: INFO                   # DEBUG | INFO | WARNING | ERROR

knowledge_base:
  enabled: true                     # true = active, false = disabled
  kb_dir: ./knowledge_base
  manifest_file: ./data/kb_manifest.json
  collection: default
  poll_interval: 5.0                # Seconds between scans
  max_file_size: 10485760           # 10 MB
```

</details>

---

## Quick Start

Get up and running in 5 minutes:

```bash
# 1. Clone and install
git clone https://github.com/reddynalamari/staged-rag-mcp.git
cd staged-rag-mcp
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e .

# 2. Set your API key
echo GEMINI_API_KEY=your_key_here > .env

# 3. Seed sample data (optional)
python scripts/seed_mock_data.py

# 4. Start the server
python -m staged_rag.server
```

The server starts on `http://127.0.0.1:8090`. Connect any MCP client to start querying.

---

## How to Use Guide

For a comprehensive, step-by-step usage guide with real-world examples, detailed walkthroughs for every feature, and extensive troubleshooting, see **[HOWTOUSE.md](HOWTOUSE.md)**.

The guide covers:

| Section | What You'll Learn |
|---------|-------------------|
| **Getting Started** | Installation, API key setup, server startup, verification |
| **Configuration** | All config options with tuning guidelines and full examples |
| **Connecting MCP Clients** | VS Code (HTTP/STDIO), Claude Desktop, custom clients |
| **Document Ingestion** | Single, batch, tagged, and collection-based ingestion |
| **Two-Level Retrieval** | Complete walkthrough of the staged search → expand → chunk workflow |
| **Advanced Search** | Hybrid search, multi-query fusion, similar documents, tag filtering |
| **Document Management** | Updates, deletes, metadata inspection |
| **Knowledge Base** | Auto-sync folder setup, PDFs, subfolders, re-sync, auto-tagging |
| **Collections** | Creating, organising, and monitoring isolated document namespaces |
| **Observability** | Explain retrieval scoring, audit logs, system health monitoring |
| **Embedding Providers** | Detailed setup for all 7 providers with examples |
| **Prompt Engineering** | System, evaluation, and analysis prompts for LLM integration |
| **Real-World Use Cases** | Team KB, research papers, codebase docs, support, personal notes, multi-tenant |
| **Performance Tuning** | Search quality, API cost reduction, large collection handling |
| **Troubleshooting** | 40+ problems with step-by-step solutions and error message reference |
| **FAQ** | Answers to the most common questions |

> **New to Staged RAG?** Start with the [HOWTOUSE.md](HOWTOUSE.md) guide — it's designed to take you from zero to productive in minutes.

---

### Quick Test with Python

```python
from staged_rag.tools import search_summaries, get_documents

# Level 1: Search summaries
results = search_summaries("machine learning", top_k=3)
for r in results["results"]:
    print(f"  [{r['similarity_score']:.2f}] {r['title']}: {r['summary'][:80]}...")

# Level 2: Expand top result
if results["results"]:
    top_doc_id = results["results"][0]["doc_id"]
    full = get_documents([top_doc_id], include_chunks=True)
    print(f"\nFull text ({full['total_tokens']} tokens):")
    print(full["documents"][0]["full_text"][:200])
```

---

## Running the Server

### Standard Mode (Streamable HTTP)

```bash
python -m staged_rag.server
```

Output:
```
2026-02-09 10:00:00 [staged_rag.server] INFO: Starting Staged RAG MCP Server...
2026-02-09 10:00:01 [staged_rag.server] INFO: Server listening on http://127.0.0.1:8090
```

### STDIO Mode

For MCP clients that spawn the server process (e.g., Claude Desktop):

```yaml
# In config.local.yaml
server:
  transport: stdio
```

Then the client starts the server with:
```bash
python -m staged_rag.server
```

### With Knowledge Base Watcher

```yaml
# In config.yaml or config.local.yaml
knowledge_base:
  enabled: true
```

Output includes:
```
2026-02-09 10:00:02 [staged_rag.server] INFO: Knowledge-base watcher active – monitoring ./knowledge_base
2026-02-09 10:00:02 [staged_rag.core.kb_manager] INFO: Running initial KB sync...
2026-02-09 10:00:03 [staged_rag.core.kb_manager] INFO: Initial KB sync complete: {'created': 3, 'modified': 0, 'deleted': 0, 'errors': 0}
```

---

## Embedding Providers

Staged RAG supports 7 embedding providers through a factory pattern with lazy imports. You only need the dependencies for the provider you actually use.

### Google Gemini (Default)

```yaml
embedding:
  provider: gemini
  model: gemini-embedding-001
  dimensions: 3072
```

```bash
# Required environment variable
GEMINI_API_KEY=your_key

# No additional pip install needed (google-genai is a core dependency)
```

| Model | Dimensions | Notes |
|-------|-----------|-------|
| `gemini-embedding-001` | 768–3072 | Configurable output dimensionality |

### OpenAI

```yaml
embedding:
  provider: openai
  model: text-embedding-3-small
  dimensions: 1536
```

```bash
OPENAI_API_KEY=your_key
pip install -e ".[openai]"
```

| Model | Dimensions | Notes |
|-------|-----------|-------|
| `text-embedding-3-small` | 1536 | Fast, cost-effective |
| `text-embedding-3-large` | 3072 | Higher quality |
| `text-embedding-ada-002` | 1536 | Legacy model |

### Ollama (Local)

```yaml
embedding:
  provider: ollama
  model: nomic-embed-text
  dimensions: 768
  provider_config:
    ollama_base_url: http://localhost:11434
```

```bash
# No API key needed — runs locally
pip install -e ".[ollama]"
ollama pull nomic-embed-text
```

| Model | Dimensions | Notes |
|-------|-----------|-------|
| `nomic-embed-text` | 768 | Good general-purpose |
| `all-minilm` | 384 | Lightweight |
| `mxbai-embed-large` | 1024 | Higher quality |

### HuggingFace

**Local mode (sentence-transformers):**

```yaml
embedding:
  provider: huggingface
  model: all-MiniLM-L6-v2
  dimensions: 384
```

```bash
pip install -e ".[huggingface]"
```

**API mode (HuggingFace Inference):**

```yaml
embedding:
  provider: huggingface
  model: sentence-transformers/all-MiniLM-L6-v2
  dimensions: 384
  provider_config:
    huggingface_base_url: https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2
```

```bash
HUGGINGFACE_API_KEY=your_key
pip install -e ".[openai]"   # Uses OpenAI-compatible client
```

### Azure OpenAI

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
EMBEDDING_AZURE_OPENAI_API_KEY=your_key
pip install -e ".[openai]"
```

### Together AI

```yaml
embedding:
  provider: together
  model: togethercomputer/m2-bert-80M-8k-retrieval
  dimensions: 768
```

```bash
TOGETHER_API_KEY=your_key
pip install -e ".[together]"
```

### LM Studio (Local)

```yaml
embedding:
  provider: lmstudio
  model: text-embedding-nomic-embed-text-v1.5
  dimensions: 768
  provider_config:
    openai_base_url: http://localhost:1234/v1
```

```bash
# No API key needed — runs locally via LM Studio
pip install -e ".[openai]"   # Uses OpenAI-compatible client
```

### Switching Providers

To switch providers, update `config.local.yaml`:

```yaml
embedding:
  provider: ollama
  model: nomic-embed-text
  dimensions: 768
```

Then restart the server. Existing documents retain their embeddings; new documents use the new provider.

> **Important**: If you change embedding providers or models, existing vector indexes become incompatible. Delete `data/index/*.npz` and re-ingest documents, or use `kb_resync()` for knowledge base documents.

### Deterministic Fallback

If the embedding API is unavailable (no API key, rate limited, network error), the engine falls back to a deterministic vector generator:

1. SHA-256 hash of the input text → seed
2. NumPy random normal distribution with that seed → vector
3. L2 normalize → unit vector

This ensures the server never crashes due to embedding failures. Deterministic vectors produce consistent (but lower quality) similarity scores.

---

## MCP Tools Reference

All tools are exposed via the Model Context Protocol and can be called from any MCP client. Each tool is wrapped in an error-catching decorator (`@_safe_tool`) — if a tool throws an exception, it returns `{"error": "ExceptionType: message"}` instead of crashing the server.

### Retrieval Tools

#### search_summaries

**Level 1 retrieval** — the entry point for every search. Returns compact summaries with similarity scores.

```
search_summaries(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    min_score: float = 0.0,
    tags_filter: list[str] | None = None
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | *required* | Natural language search query |
| `top_k` | `int` | `5` | Number of results (capped at `max_top_k`) |
| `collection` | `str` | `"default"` | Collection to search |
| `min_score` | `float` | `0.0` | Minimum similarity score threshold (0.0–1.0) |
| `tags_filter` | `list[str]` | `None` | Only return documents with at least one matching tag |

**Returns:**

```json
{
  "query": "machine learning algorithms",
  "results": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Introduction to ML",
      "summary": "This document covers fundamental machine learning concepts...",
      "similarity_score": 0.92,
      "token_count": 1500,
      "tags": ["ml", "tutorial"],
      "collection": "default"
    }
  ],
  "total_candidates": 25,
  "search_time_ms": 145.3
}
```

---

#### get_documents

**Level 2 retrieval** — fetch full document text for selected document IDs.

```
get_documents(
    doc_ids: list[str],
    include_chunks: bool = False,
    collection: str = "default"
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc_ids` | `list[str]` | *required* | Document IDs to retrieve |
| `include_chunks` | `bool` | `False` | Include individual chunk data |
| `collection` | `str` | `"default"` | Collection to search |

**Returns:**

```json
{
  "documents": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Introduction to ML",
      "full_text": "Complete document text...",
      "source": "manual",
      "token_count": 1500,
      "tags": ["ml", "tutorial"],
      "metadata": {"author": "John"},
      "chunks": [
        {
          "chunk_index": 0,
          "text": "First chunk text...",
          "token_count": 195,
          "start_char": 0,
          "end_char": 1024
        }
      ]
    }
  ],
  "total_tokens": 1500
}
```

---

#### get_document_chunk

**Level 2.5 retrieval** — retrieve a single chunk by index or semantic query.

```
get_document_chunk(
    doc_id: str,
    chunk_index: int | None = None,
    chunk_query: str | None = None,
    collection: str = "default"
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc_id` | `str` | *required* | Document ID |
| `chunk_index` | `int` | `None` | Specific chunk index (0-based) |
| `chunk_query` | `str` | `None` | Semantic query to find the most relevant chunk |
| `collection` | `str` | `"default"` | Collection name |

> Provide either `chunk_index` OR `chunk_query`, not both.

**Returns (by index):**

```json
{
  "doc_id": "a1b2c3d4-...",
  "chunk_index": 2,
  "total_chunks": 8,
  "text": "The chunk text content...",
  "token_count": 195,
  "has_previous": true,
  "has_next": true
}
```

**Returns (by query, includes relevance score):**

```json
{
  "doc_id": "a1b2c3d4-...",
  "chunk_index": 5,
  "total_chunks": 8,
  "text": "Most relevant chunk...",
  "token_count": 180,
  "has_previous": true,
  "has_next": true,
  "relevance_score": 0.87
}
```

---

### Advanced Search Tools

#### hybrid_search

Combines semantic (vector) search with BM25 keyword matching for better recall.

```
hybrid_search(
    query: str,
    top_k: int = 5,
    collection: str = "default",
    semantic_weight: float = 0.7,
    keyword_weight: float = 0.3
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | `str` | *required* | Search query |
| `top_k` | `int` | `5` | Number of results |
| `collection` | `str` | `"default"` | Collection name |
| `semantic_weight` | `float` | `0.7` | Weight for vector similarity (0.0–1.0) |
| `keyword_weight` | `float` | `0.3` | Weight for BM25 keyword matching (0.0–1.0) |

**How it works:**
1. Run semantic search → get cosine similarity scores (already 0–1)
2. Run BM25 keyword search → normalize scores to 0–1 (divide by max)
3. Compute weighted combination: `score = (semantic_weight × sem_score) + (keyword_weight × kw_score)`
4. Weights are auto-normalised to sum to 1.0
5. Return top_k results ranked by combined score

**Best for:** Queries where exact keyword matches matter alongside semantic meaning.

---

#### multi_query_search

Run multiple queries and merge results using rank fusion.

```
multi_query_search(
    queries: list[str],
    top_k: int = 5,
    collection: str = "default",
    fusion_method: str = "rrf"
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `queries` | `list[str]` | *required* | Two or more search queries |
| `top_k` | `int` | `5` | Number of final results |
| `collection` | `str` | `"default"` | Collection name |
| `fusion_method` | `str` | `"rrf"` | Fusion method: `"rrf"` (Reciprocal Rank Fusion) or `"max"` (maximum score) |

**Fusion methods:**
- **`rrf`** (Reciprocal Rank Fusion): `score = Σ 1/(60 + rank + 1)` for each query where the document appears. Documents appearing in multiple query results get boosted.
- **`max`**: Takes the maximum similarity score across all queries for each document.

**Best for:** Capturing multiple aspects of a topic. E.g., search for "neural networks", "deep learning", "backpropagation" simultaneously.

---

#### find_similar

Find documents similar to a reference document.

```
find_similar(
    doc_id: str,
    top_k: int = 5,
    exclude_same_source: bool = False,
    collection: str = "default"
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `doc_id` | `str` | *required* | Reference document ID |
| `top_k` | `int` | `5` | Number of similar documents |
| `exclude_same_source` | `bool` | `False` | Exclude documents from the same source |
| `collection` | `str` | `"default"` | Collection name |

**How it works:**
1. Retrieve the reference document's summary (or title)
2. Embed the summary text
3. Search the vector index for nearest neighbors
4. Exclude the reference document itself from results

---

### Document Management Tools

#### ingest_document

Add a single document to the system.

```
ingest_document(
    title: str,
    text: str,
    source: str = "manual",
    collection: str = "default",
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | *required* | Document title (must not be empty) |
| `text` | `str` | *required* | Full document text (must not be empty) |
| `source` | `str` | `"manual"` | Source identifier (URL, path, label) |
| `collection` | `str` | `"default"` | Target collection |
| `tags` | `list[str]` | `None` | Searchable tags |
| `metadata` | `dict` | `None` | Arbitrary key-value metadata |
| `summary` | `str` | `None` | Pre-computed summary (skips auto-generation if provided) |

**Processing pipeline:**
1. Validate title and text are non-empty
2. Check token count against `max_document_tokens`
3. Generate summary (Gemini API → local extractive fallback)
4. Chunk text into overlapping segments
5. Create `Document` model with UUID
6. Save to JSON store
7. Embed summary (or title) → upsert into vector index
8. Rebuild BM25 index
9. Write audit log entry

**Returns:**

```json
{
  "doc_id": "a1b2c3d4-e5f6-...",
  "title": "My Document",
  "collection": "default",
  "chunk_count": 8,
  "token_count": 1500,
  "summary": "Generated or provided summary...",
  "status": "indexed"
}
```

---

#### ingest_batch

Bulk ingest multiple documents in a single operation.

```
ingest_batch(
    documents: list[dict],
    collection: str = "default"
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `documents` | `list[dict]` | *required* | List of document dicts (each must have `title` and `text`) |
| `collection` | `str` | `"default"` | Target collection |

Each document dict supports the same keys as `ingest_document`: `title`, `text`, `source`, `tags`, `metadata`, `summary`.

**Returns:**

```json
{
  "total": 10,
  "succeeded": 9,
  "failed": 1,
  "results": [
    {"doc_id": "...", "title": "Doc 1", "status": "indexed"},
    {"title": "Doc 2", "status": "error", "error": "Text must not be empty"}
  ],
  "total_tokens_indexed": 12500
}
```

---

#### update_document

Update an existing document's metadata, text, or summary.

```
update_document(
    doc_id: str,
    text: str | None = None,
    title: str | None = None,
    tags: list[str] | None = None,
    metadata: dict | None = None,
    summary: str | None = None,
    collection: str = "default"
) → dict
```

All parameters except `doc_id` are optional — only provided fields are updated.

**Behavior:**
- `title`, `tags`: Direct replacement
- `metadata`: Shallow merge with existing metadata
- `text`: Triggers full re-chunking, re-summarization, and re-embedding
- `summary` (without `text`): Updates summary and re-embeds

---

#### delete_document

Remove a document and all associated data.

```
delete_document(
    doc_id: str,
    collection: str = "default"
) → dict
```

**What gets cleaned up:**
1. Document removed from JSON store
2. Vector removed from NumPy index
3. BM25 index rebuilt without the document
4. Audit log entry recorded

---

### Metadata Tools

#### get_document_metadata

Retrieve document metadata without loading the full text (lightweight).

```
get_document_metadata(
    doc_id: str,
    collection: str = "default"
) → dict
```

**Returns:**

```json
{
  "doc_id": "a1b2c3d4-...",
  "title": "Document Title",
  "source": "manual",
  "collection": "default",
  "tags": ["tag1", "tag2"],
  "token_count": 1500,
  "chunk_count": 8,
  "created_at": "2026-02-08T10:30:00+00:00",
  "updated_at": "2026-02-09T14:20:00+00:00",
  "metadata": {"author": "Jane Doe"}
}
```

---

### Observability Tools

#### collection_stats

Get comprehensive statistics for a collection.

```
collection_stats(
    collection: str = "default"
) → dict
```

**Returns:**

```json
{
  "collection": "default",
  "document_count": 25,
  "total_tokens": 37500,
  "avg_tokens_per_doc": 1500.0,
  "total_chunks": 200,
  "tag_distribution": {"ml": 10, "tutorial": 5, "source:knowledge_base": 8},
  "source_distribution": {"manual": 15, "knowledge_base:notes.md": 5, "batch": 5},
  "oldest_document": "2026-01-15T08:00:00+00:00",
  "newest_document": "2026-02-09T12:00:00+00:00",
  "index_size_bytes": 245760
}
```

---

#### list_collections

Enumerate all collections with summary stats.

```
list_collections() → dict
```

**Returns:**

```json
{
  "collections": [
    {"name": "default", "document_count": 25, "total_tokens": 37500, "description": ""},
    {"name": "research", "document_count": 10, "total_tokens": 18000, "description": ""}
  ]
}
```

---

#### explain_retrieval

Understand why documents ranked as they did for a given query.

```
explain_retrieval(
    query: str,
    doc_ids: list[str],
    collection: str = "default"
) → dict
```

**Returns:**

```json
{
  "query": "neural networks",
  "explanations": [
    {
      "doc_id": "a1b2c3d4-...",
      "title": "Deep Learning Basics",
      "cosine_similarity": 0.92,
      "bm25_score": 15.7,
      "top_matching_terms": ["neural", "networks"],
      "query_doc_term_overlap": 0.8,
      "explanation_text": "Combined semantic and keyword scores to rank this document."
    }
  ]
}
```

---

#### retrieval_log

Query the audit log for recent retrieval events.

```
retrieval_log(
    last_n: int = 10,
    tool_filter: str | None = None,
    session_id: str | None = None
) → dict
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `last_n` | `int` | `10` | Number of recent entries to return |
| `tool_filter` | `str` | `None` | Filter by tool name (e.g., `"search_summaries"`) |
| `session_id` | `str` | `None` | Filter by session ID |

---

### Knowledge Base Tools

#### kb_status

Check the current status of the knowledge base watcher.

```
kb_status() → dict
```

**Returns:**

```json
{
  "kb_dir": "/path/to/knowledge_base",
  "collection": "default",
  "watcher_running": true,
  "manifest": {
    "total_files": 12,
    "total_indexed": 11,
    "total_errors": 1,
    "last_scan": "2026-02-09T12:00:00+00:00"
  }
}
```

---

#### kb_resync

Force a complete re-synchronisation of the knowledge base folder.

```
kb_resync() → dict
```

**What happens:**
1. All KB-sourced documents are deleted from the vector store
2. The manifest is cleared completely
3. A fresh initial sync is performed (full folder scan + ingestion)

**Returns:**

```json
{
  "created": 12,
  "modified": 0,
  "deleted": 0,
  "errors": 0
}
```

---

## Knowledge Base System

<a name="kb-overview"></a>

### Overview

The Knowledge Base (KB) system provides automatic, folder-based document ingestion. Instead of manually calling `ingest_document` for every file, you simply drop files into the `knowledge_base/` directory and the server handles everything automatically.

### How It Works

```
                   knowledge_base/
                   ├── notes.md          ← File appears
                   ├── report.pdf
                   └── data/
                       └── analysis.txt
                            │
                            ▼
                   ┌─────────────────┐
                   │  File Watcher   │    Polls every N seconds
                   │  (Polling)      │    Computes SHA-256 hashes
                   └────────┬────────┘
                            │
                   ┌────────┴────────┐
                   │  Diff Engine    │    Compares with known state
                   │  Created?       │    Created → ingest
                   │  Modified?      │    Modified → re-ingest
                   │  Deleted?       │    Deleted → remove
                   └────────┬────────┘
                            │
                   ┌────────┴────────┐
                   │  KB Manager     │    Reads file, cleans text
                   │  _ingest_file() │    Derives title and tags
                   │                 │    Calls RAGService.ingest
                   └────────┬────────┘
                            │
                   ┌────────┴────────┐
                   │  KB Manifest    │    Records file → doc_id
                   │  (JSON)         │    Persists across restarts
                   └─────────────────┘
```

### Supported File Types

| Category | Extensions |
|----------|-----------|
| **Text** | `.txt`, `.md`, `.markdown`, `.rst` |
| **Data** | `.json`, `.yaml`, `.yml`, `.csv`, `.tsv` |
| **Code** | `.py`, `.js`, `.ts`, `.java`, `.c`, `.cpp`, `.h`, `.go`, `.rs` |
| **Web** | `.html`, `.htm`, `.xml` |
| **Config** | `.log`, `.cfg`, `.ini`, `.toml` |
| **Documents** | `.pdf` (text extraction via pypdf) |

### Auto-Generated Tags

Every file ingested from the knowledge base receives automatic tags:

- **`source:knowledge_base`** — Identifies KB-sourced documents
- **`filetype:<ext>`** — File extension (e.g., `filetype:md`, `filetype:py`)
- **`folder:<name>`** — Subfolder names (e.g., `folder:research`, `folder:docs`)

### PDF Support

PDF files are automatically processed with:

1. **Text extraction** via `pypdf` (page-by-page)
2. **Title extraction** from PDF `/Title` metadata field
3. **Text cleaning** — removes page numbers, fixes CamelCase joins, normalises whitespace
4. **Fallback title** — first substantive line of text, or cleaned filename

Limitations:
- Image-only/scanned PDFs produce no text (recorded as "error" in manifest)
- Encrypted PDFs that can't be decrypted with empty password are skipped
- Very large PDFs may hit the `max_file_size` limit (default 10 MB)

### Manifest Tracking

The `kb_manifest.json` file persists file-to-document mappings:

```json
{
  "version": 1,
  "kb_dir": "/absolute/path/to/knowledge_base",
  "files": {
    "notes.md": {
      "relative_path": "notes.md",
      "doc_id": "a1b2c3d4-e5f6-7890-...",
      "content_hash": "sha256_hex_string",
      "file_size": 2048,
      "indexed_at": "2026-02-09T10:00:00+00:00",
      "updated_at": "2026-02-09T10:00:00+00:00",
      "status": "indexed"
    },
    "broken.pdf": {
      "relative_path": "broken.pdf",
      "doc_id": "",
      "content_hash": "sha256_hex_string",
      "file_size": 5242880,
      "indexed_at": "2026-02-09T10:00:00+00:00",
      "updated_at": "2026-02-09T10:00:00+00:00",
      "status": "error",
      "error": "No extractable text found in PDF"
    }
  },
  "stats": {
    "total_files": 2,
    "total_indexed": 1,
    "total_errors": 1,
    "last_scan": "2026-02-09T10:00:00+00:00"
  }
}
```

**Status values:**
- `indexed` — Successfully ingested and searchable
- `skipped` — File was readable but empty
- `error` — File could not be processed (reason in `error` field)

### Folder Organization

Use subfolders to organize documents by topic. Subfolder names become searchable tags:

```
knowledge_base/
├── engineering/
│   ├── architecture.md        → tags: [filetype:md, source:knowledge_base, folder:engineering]
│   ├── testing-guide.md       → tags: [filetype:md, source:knowledge_base, folder:engineering]
│   └── apis/
│       └── rest-design.md     → tags: [filetype:md, source:knowledge_base, folder:engineering, folder:apis]
├── product/
│   ├── roadmap.md             → tags: [filetype:md, source:knowledge_base, folder:product]
│   └── specs/
│       └── feature-x.pdf      → tags: [filetype:pdf, source:knowledge_base, folder:product, folder:specs]
└── meeting-notes.txt          → tags: [filetype:txt, source:knowledge_base]
```

Search with tag filters:
```python
# Find only engineering documents
results = search_summaries("API design", tags_filter=["folder:engineering"])

# Find only PDF documents
results = search_summaries("specification", tags_filter=["filetype:pdf"])
```

### Initial Sync vs Background Watcher

| Phase | Timing | What Happens |
|-------|--------|-------------|
| **Initial Sync** | Server startup | Full folder scan; compares manifest vs. filesystem; ingests new, re-ingests modified, removes deleted |
| **Background Watcher** | Every `poll_interval` seconds | Incremental scan; detects and processes changes since last scan |

The background watcher runs in a daemon thread and automatically stops when the server shuts down.

---

## Document Lifecycle

### Ingestion Pipeline

```
Input Text
    │
    ├─→ Token Count Check (max_document_tokens)
    │       │ fail → return error
    │       │ pass ↓
    ├─→ Summary Generation
    │       ├─→ Gemini API (if available + auto_summary=true)
    │       │       │ fail → local fallback
    │       └─→ Local Extractive Fallback
    │               ├─→ Clean text (PDF noise, CamelCase, whitespace)
    │               ├─→ Split sentences
    │               ├─→ Filter noise (short, numeric, header-like)
    │               └─→ Select top N substantive sentences
    │
    ├─→ Chunking (sentence-based)
    │       ├─→ Split into sentences
    │       ├─→ Accumulate until chunk_size tokens
    │       ├─→ Carry over chunk_overlap tokens
    │       └─→ Filter chunks < min_chunk_size
    │
    ├─→ Document Model (Pydantic)
    │       ├─→ UUID4 generation for doc_id
    │       ├─→ Created/updated timestamps
    │       └─→ Full model validation
    │
    ├─→ Storage
    │       ├─→ JSON Document Store (data/store/<collection>.json)
    │       ├─→ Vector Index (data/index/<collection>.npz)
    │       └─→ BM25 Index (in-memory rebuild)
    │
    └─→ Audit Log (data/logs/audit.jsonl)
```

### Document Model

Every document is stored as a Pydantic `Document` model:

```python
class Document(BaseModel):
    doc_id: str          # UUID4 — stable unique identifier
    title: str           # Human-readable title
    source: str          # Origin: path, URL, or label
    full_text: str       # Complete document text
    summary: str         # 2–4 sentence summary for Level 1 retrieval
    chunks: list[DocumentChunk]  # Overlapping text segments
    tags: list[str]      # Searchable tags (e.g., ["ml", "tutorial"])
    collection: str      # Collection name (default: "default")
    token_count: int     # Token count of full_text
    created_at: datetime # UTC creation timestamp
    updated_at: datetime # UTC last-update timestamp
    metadata: dict       # Arbitrary key-value metadata
```

Each chunk:

```python
class DocumentChunk(BaseModel):
    chunk_index: int     # 0-based position in document
    text: str            # Chunk text content
    token_count: int     # Token count of this chunk
    start_char: int      # Start character offset in full_text
    end_char: int        # End character offset in full_text
```

### Chunking Strategy

The system uses **sentence-based chunking with overlap**:

1. **Sentence splitting** — Text is split at sentence-ending punctuation (`.`, `!`, `?`), with single newlines joined into paragraphs
2. **Accumulation** — Sentences accumulate into a chunk until `chunk_size` tokens is reached
3. **Overlap** — When a chunk boundary is reached, the last `chunk_overlap` tokens carry over to the next chunk, providing context continuity
4. **Minimum size** — Chunks with fewer than `min_chunk_size` tokens are discarded (unless they're the sole content)

### Summary Generation

Summaries are critical for Level 1 retrieval efficiency. The system provides two paths:

**Path 1: Gemini API (default)**
- Sends the full document text with a structured prompt
- Generates a 2–4 sentence abstractive summary
- Focuses on key facts and document intent

**Path 2: Local Extractive Fallback**
- Automatically activated when:
  - No API key is configured
  - API call fails (rate limit, network error, etc.)
- Pipeline:
  1. Clean text (PDF artifacts, CamelCase joins, whitespace)
  2. Split into sentences
  3. Filter noise (too short, mostly numbers, all-caps headers, boilerplate)
  4. Select top N substantive sentences from the beginning (topic-stating position)

### Embedding and Indexing

**Embedding** — The document's summary (or title, if summary is empty) is encoded into a fixed-dimension float vector using the configured embedding provider.

**Vector Index** — Vectors are stored in a NumPy compressed file (`.npz`). Search uses normalised cosine similarity:

```
similarity(q, d) = (q · d) / (|q| × |d|)
```

Vectors are L2-normalised before storage, so similarity reduces to a dot product.

**BM25 Index** — An in-memory Okapi BM25 index is built from document titles, summaries, and full text. This index is rebuilt on every ingestion, update, or deletion to ensure consistency.

---

## Search and Retrieval

### Semantic Search

The primary search mode. Embeds the query, then finds the nearest document vectors using cosine similarity.

**Strengths:** Understands meaning, handles synonyms, works across languages
**Weaknesses:** May miss exact term matches, relies on embedding quality

### BM25 Keyword Search

Classic term-frequency inverse-document-frequency scoring using the Okapi BM25 algorithm.

**Strengths:** Exact term matching, fast, no API calls needed
**Weaknesses:** No semantic understanding, sensitive to vocabulary mismatch

### Hybrid Search Details

Combines semantic and BM25 scores with configurable weights:

```
final_score = (semantic_weight × cosine_sim) + (keyword_weight × normalized_bm25)
```

Where:
- `cosine_sim` ∈ [0, 1] — cosine similarity from vector search
- `normalized_bm25` = `bm25_score / max(bm25_scores)` — normalised to [0, 1]
- Weights are auto-normalised: if `semantic_weight=0.7` and `keyword_weight=0.3`, they're divided by their sum

### Multi-Query Fusion

Runs multiple independent queries and merges results:

**Reciprocal Rank Fusion (RRF):**
```
score(d) = Σ_{q ∈ queries} 1 / (60 + rank_q(d) + 1)
```

Documents appearing in multiple query results accumulate higher RRF scores. The constant 60 dampens the effect of rank differences.

**Max Score:**
```
score(d) = max_{q ∈ queries} similarity_q(d)
```

Simply takes the highest similarity score across all queries.

### Similarity Search

`find_similar` uses the reference document's summary as a query:

1. Retrieve reference document
2. Embed its summary (or title)
3. Search vector index for nearest neighbors
4. Exclude the reference document from results
5. Optionally exclude documents with the same `source`

### Scoring and Ranking

All scores are clamped to [0.0, 1.0] before being returned to the client. This ensures consistent interpretation regardless of the underlying scoring method.

---

## Collections

### What Are Collections

Collections are isolated document namespaces. Each collection has its own:
- JSON document store (`data/store/<name>.json`)
- Vector index (`data/index/<name>.npz`)
- BM25 index (in-memory)

Documents in different collections don't interact during search.

### Creating Collections

Collections are created implicitly — just ingest a document with a new collection name:

```python
ingest_document(
    title="My Doc",
    text="Content...",
    collection="research"  # Creates "research" collection automatically
)
```

### Multi-Collection Strategy

Recommended patterns:

| Pattern | When to Use |
|---------|------------|
| Single `default` collection | Small projects, prototyping |
| Topic-based (`research`, `docs`, `code`) | Medium projects with distinct document categories |
| Tenant-based (`user_123`, `org_456`) | Multi-tenant applications |
| Temporal (`2026_q1`, `2026_q2`) | Time-series document archives |

### Collection Statistics

Monitor collections with `collection_stats`:

```python
stats = collection_stats("research")
# Check document count, token usage, tag distribution, etc.
```

---

## Storage Backend

### Document Store (JSON)

- **Location:** `data/store/<collection>.json`
- **Format:** JSON object mapping `doc_id` → full document record
- **Thread safety:** `threading.Lock` for concurrent access
- **Caching:** In-memory cache per collection (lazy loaded)

### Vector Index (NumPy)

- **Location:** `data/index/<collection>.npz`
- **Format:** NumPy compressed archive with `doc_ids` array and `vectors` matrix
- **Operations:** `upsert`, `delete`, `search` (cosine similarity)
- **Thread safety:** `threading.Lock` for all operations
- **Persistence:** Auto-saved to disk after every mutation

### BM25 Index (In-Memory)

- **Library:** `rank-bm25` (Okapi BM25)
- **Rebuild trigger:** Every document ingestion, update, or deletion
- **Corpus:** Title + summary + full_text per document
- **No persistence** — rebuilt from document store on service initialization

### Audit Log (JSONL)

- **Location:** `data/logs/audit.jsonl`
- **Format:** One JSON object per line (append-only)
- **Auto-truncation:** Oldest entries removed when exceeding `max_log_entries`
- **Thread safety:** `threading.Lock` for writes

### KB Manifest (JSON)

- **Location:** `data/kb_manifest.json`
- **Purpose:** Tracks which files have been ingested, their doc IDs, and content hashes
- **Persistence:** Updated on every file event (create, modify, delete)

---

## Observability and Auditing

### Audit Logging

Every tool call is logged with:

```json
{
  "timestamp": "2026-02-09T12:34:56.789+00:00",
  "tool": "search_summaries",
  "params": {
    "query": "machine learning",
    "top_k": 5,
    "collection": "default"
  },
  "result_count": 3,
  "doc_ids": ["a1b2c3d4-...", "e5f6g7h8-...", "i9j0k1l2-..."],
  "latency_ms": 145.3
}
```

### Retrieval Explanation

For any query-document pair, `explain_retrieval` provides:
- **Cosine similarity** — Raw semantic similarity score
- **BM25 score** — Raw keyword matching score
- **Term overlap ratio** — Fraction of query terms found in document
- **Top matching terms** — Which query terms matched

### Collection Monitoring

Track system health with `collection_stats`:
- Document count and growth over time
- Token budget consumption
- Tag and source distribution analysis
- Index file sizes

---

## Integration with MCP Clients

### VS Code / GitHub Copilot

Add to your VS Code MCP settings (`.vscode/mcp.json` or user settings):

```json
{
  "mcpServers": {
    "staged-rag": {
      "command": "python",
      "args": ["-m", "staged_rag.server"],
      "cwd": "/path/to/staged-rag-mcp",
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

For HTTP transport:

```json
{
  "mcpServers": {
    "staged-rag": {
      "url": "http://127.0.0.1:8090/mcp"
    }
  }
}
```

### Claude Desktop

Add to Claude Desktop's MCP configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "staged-rag": {
      "command": "python",
      "args": ["-m", "staged_rag.server"],
      "cwd": "/path/to/staged-rag-mcp",
      "env": {
        "GEMINI_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Custom MCP Clients

Any MCP-compatible client can connect. The server exposes 17 tools:

| Category | Tools |
|----------|-------|
| Retrieval | `search_summaries`, `get_documents`, `get_document_chunk` |
| Advanced Search | `hybrid_search`, `multi_query_search`, `find_similar` |
| Management | `ingest_document`, `ingest_batch`, `update_document`, `delete_document` |
| Metadata | `get_document_metadata` |
| Observability | `collection_stats`, `list_collections`, `explain_retrieval`, `retrieval_log` |
| Knowledge Base | `kb_status`, `kb_resync` |

---

## Prompt Engineering for Staged RAG

The `prompts.py` module provides structured prompts for implementing the staged retrieval workflow in LLM applications.

### System Prompt

```python
from staged_rag.prompts import staged_rag_system_prompt

prompt = staged_rag_system_prompt("What are the benefits of microservices?")
```

Generates:
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

### Evaluate Summaries Prompt

```python
from staged_rag.prompts import evaluate_summaries_prompt

prompt = evaluate_summaries_prompt(json.dumps(summaries, indent=2))
```

Instructs the LLM to review search results and decide which to expand vs. skip.

### Deep Analysis Prompt

```python
from staged_rag.prompts import deep_analysis_prompt

prompt = deep_analysis_prompt(
    question="What are the benefits?",
    context=retrieved_text
)
```

Instructs the LLM to synthesize an answer from retrieved context with citations.

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=staged_rag --cov-report=term-missing

# Run specific test file
pytest tests/test_document_store.py -v

# Run specific test
pytest tests/test_vector_index.py::test_upsert_and_search -v
```

### Test Structure

| Test File | What It Tests |
|-----------|--------------|
| `test_document_store.py` | CRUD operations on JSON document store |
| `test_vector_index.py` | Vector upsert, delete, search, persistence |
| `test_embeddings.py` | Embedding provider initialization and encoding |
| `test_tools.py` | MCP tool function signatures and responses |
| `test_agent_flow.py` | End-to-end retrieval workflows |

### Writing New Tests

```python
import pytest
from staged_rag.core.document_store import DocumentStore

def test_save_and_retrieve(tmp_path):
    store = DocumentStore(tmp_path)
    doc = {"doc_id": "test-1", "title": "Test", "full_text": "Content"}
    store.save("default", doc)

    result = store.get("default", "test-1")
    assert result is not None
    assert result["title"] == "Test"

def test_delete_nonexistent(tmp_path):
    store = DocumentStore(tmp_path)
    result = store.delete("default", "nonexistent")
    assert result is None
```

---

## Performance Considerations

### Rate Limiting

The embedding engine includes built-in rate pacing:
- **Default limit:** 80 requests per minute (RPM)
- **Window:** 60-second sliding window
- **Behavior:** Automatically sleeps when approaching the limit
- **Purpose:** Stay within free-tier API quotas

### Token Budget Management

- Each document's token count is tracked at ingestion
- `collection_stats` reports total and average tokens per collection
- `max_document_tokens` rejects documents exceeding the budget
- Level 1 (summaries) returns `token_count` so LLMs can make informed expansion decisions

### Embedding Caching

- Embeddings are persisted in NumPy `.npz` files — never recomputed for existing documents
- Only new or updated documents trigger embedding API calls
- BM25 index is rebuilt in-memory (fast, no API calls)

### Index Performance

- **Vector search:** O(n) linear scan with NumPy matrix multiplication — efficient for collections up to ~100K documents
- **BM25 search:** O(n × m) where n = documents, m = query terms
- **Document lookup:** O(1) hash map lookup from in-memory cache

For larger collections (100K+ documents), consider the FAISS optional dependency:
```bash
pip install -e ".[faiss]"
```

---

## Security

### API Key Management

- Store API keys in `.env` file (gitignored)
- Keys are loaded via `python-dotenv` at startup
- Never hardcode keys in configuration files
- Use environment variables in CI/CD pipelines

### Data Privacy

- All data stored locally (no external databases)
- Document content stored in plaintext JSON — encrypt at rest if needed
- Audit logs may contain query text — configure retention via `max_log_entries`
- KB manifest contains file paths and hashes (no content)

### Access Control

- The MCP server does not implement authentication by default
- When using HTTP transport, restrict access via:
  - Bind to `127.0.0.1` (localhost only, default)
  - Use a reverse proxy with authentication
  - Deploy behind a VPN or firewall

---

## Troubleshooting

### Installation Issues

| Problem | Solution |
|---------|----------|
| `pip install -e .` fails | Ensure Python 3.11+: `python --version` |
| `ModuleNotFoundError: google.genai` | Run `pip install google-genai` |
| `ModuleNotFoundError: fastmcp` | Run `pip install fastmcp>=0.5.0` |
| `ModuleNotFoundError: openai` | Run `pip install -e ".[openai]"` for OpenAI/Azure/LMStudio |

### Runtime Issues

| Problem | Solution |
|---------|----------|
| Server won't start | Check `.env` has valid API key; check port isn't in use |
| "Document exceeds max tokens" | Increase `ingestion.max_document_tokens` in config |
| Embedding API rate limit | Wait and retry; reduce `batch_size`; use local provider |
| Deterministic fallback active | Set valid API key or use Ollama for local embeddings |
| Empty search results | Check collection name; try `min_score=0.0`; verify documents indexed |
| KB files not being indexed | Ensure `knowledge_base.enabled: true`; check file extension support |
| PDF extraction fails | Install `pypdf`: `pip install pypdf>=4.0.0` |

### Search Quality Issues

| Problem | Solution |
|---------|----------|
| Irrelevant results | Use `hybrid_search` with keyword boost; improve document summaries |
| Missing obvious matches | Try `multi_query_search` with query variations |
| Low similarity scores | Check embedding dimensions match between config and provider |
| Inconsistent scores after provider change | Delete `data/index/*.npz` and re-ingest all documents |

### Data Issues

| Problem | Solution |
|---------|----------|
| Index out of sync | Delete `data/index/<collection>.npz` and re-ingest |
| KB manifest stale | Run `kb_resync()` to force full rebuild |
| Audit log too large | Reduce `logging.max_log_entries` or delete `audit.jsonl` |
| Corrupted JSON store | Restore from backup; document store is `data/store/<collection>.json` |

---

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/my-feature`
3. **Make** your changes with clear, descriptive commits
4. **Test** your changes: `pytest tests/ -v`
5. **Submit** a pull request with a clear description

### Development Setup

```bash
git clone https://github.com/reddynalamari/staged-rag-mcp.git
cd staged-rag-mcp
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[all-providers,dev]"
pytest tests/ -v
```

### Code Style

- Follow PEP 8 conventions
- Use type hints for all function signatures
- Add docstrings for public functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

### Contribution Agreement

By submitting contributions, you agree to the terms in the [LICENSE](LICENSE) file. Your contributions are provided under the same license terms and you grant the original author perpetual rights to use them.

---

## Roadmap

### Planned Features

- [ ] FAISS vector index backend for large-scale collections
- [ ] Streaming ingestion for very large documents
- [ ] Multi-modal embeddings (image + text)
- [ ] Webhook notifications for KB file events
- [ ] REST API alongside MCP for non-MCP clients
- [ ] Document versioning and history
- [ ] Export/import collections
- [ ] Web UI dashboard for collection management
- [ ] Pluggable summary generators (OpenAI, Anthropic, local LLMs)
- [ ] OCR support for scanned PDFs
- [ ] Incremental vector index updates (avoid full rebuild)
- [ ] Collection-level access control
- [ ] Distributed storage backends (S3, GCS)

---

## Author

**Shashidhar Reddy Nalamari**

- Email: [nalamarishashidharreddy@gmail.com](mailto:nalamarishashidharreddy@gmail.com)

This project was designed, architected, and developed by Shashidhar Reddy Nalamari. The two-level staged retrieval architecture, multi-provider embedding system, knowledge base auto-sync engine, and the complete MCP server implementation are original work by the author.

---

## License

This project is released under a **custom license** that allows free use for any purpose (personal, commercial, educational) with two key conditions:

1. **Attribution Required** — You must give credit to the original author (Shashidhar Reddy Nalamari)
2. **No False Ownership Claims** — You may not claim this project as your own original creation

See the [LICENSE](LICENSE) file for complete terms.

### Quick Summary

| Allowed | Not Allowed |
|---------|------------|
| Use for any purpose (free) | Claim as your own creation |
| Modify and distribute | Remove author attribution |
| Commercial use (free) | Register IP on the software |
| Create derivative works | Present as original in portfolios without credit |
| Learn from and teach with | Submit as your own for academic credit |

---

## Acknowledgments

This project builds upon and is grateful to the following open-source projects:

- **[FastMCP](https://github.com/jlowin/fastmcp)** — Python framework for building MCP servers
- **[Model Context Protocol](https://modelcontextprotocol.io/)** — The protocol specification by Anthropic
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation and serialization
- **[NumPy](https://numpy.org/)** — Numerical computing for vector operations
- **[rank-bm25](https://github.com/dorianbrown/rank_bm25)** — BM25 implementation in Python
- **[google-genai](https://github.com/googleapis/python-genai)** — Google Generative AI SDK
- **[pypdf](https://github.com/py-pdf/pypdf)** — PDF text extraction
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** — Environment variable management
- **[PyYAML](https://pyyaml.org/)** — YAML configuration parsing
- **[sentence-transformers](https://www.sbert.net/)** — Local HuggingFace embedding models

The embedding provider architecture pattern is inspired by the [mem0ai/mem0](https://github.com/mem0ai/mem0) project's embedder abstraction.

---

<p align="center">
  <strong>Staged RAG MCP Server</strong><br>
  <em>Search smart. Retrieve less. Answer better.</em><br><br>
  Copyright &copy; 2026-present Shashidhar Reddy Nalamari. All Rights Reserved.<br>
  Released under a custom license — see <a href="LICENSE">LICENSE</a> for details.
</p>
