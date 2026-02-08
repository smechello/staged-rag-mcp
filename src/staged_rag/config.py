from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class ServerConfig:
    name: str
    transport: str
    host: str
    port: int


@dataclass(frozen=True)
class EmbeddingConfig:
    provider: str
    model: str
    dimensions: int
    batch_size: int
    provider_config: dict


@dataclass(frozen=True)
class GenerationConfig:
    model: str
    summary_max_sentences: int


@dataclass(frozen=True)
class ChunkingConfig:
    chunk_size: int
    chunk_overlap: int
    min_chunk_size: int


@dataclass(frozen=True)
class RetrievalConfig:
    default_top_k: int
    max_top_k: int
    default_collection: str
    hybrid_semantic_weight: float
    hybrid_keyword_weight: float
    min_similarity_score: float


@dataclass(frozen=True)
class StorageConfig:
    data_dir: Path
    store_dir: Path
    index_dir: Path
    log_dir: Path


@dataclass(frozen=True)
class IngestionConfig:
    max_document_tokens: int
    max_batch_size: int
    auto_summary: bool


@dataclass(frozen=True)
class LoggingConfig:
    audit_file: Path
    max_log_entries: int
    log_level: str


@dataclass(frozen=True)
class KnowledgeBaseConfig:
    enabled: bool
    kb_dir: Path
    manifest_file: Path
    collection: str
    poll_interval: float
    max_file_size: int


@dataclass(frozen=True)
class Settings:
    server: ServerConfig
    embedding: EmbeddingConfig
    generation: GenerationConfig
    chunking: ChunkingConfig
    retrieval: RetrievalConfig
    storage: StorageConfig
    ingestion: IngestionConfig
    logging: LoggingConfig
    knowledge_base: KnowledgeBaseConfig


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def load_settings(root: Path | None = None) -> Settings:
    load_dotenv()
    root_path = root or Path(__file__).resolve().parents[2]
    base_path = root_path / "config.yaml"
    local_path = root_path / "config.local.yaml"

    base = _load_yaml(base_path)
    local = _load_yaml(local_path)

    def merged(section: str, default: dict[str, Any]) -> dict[str, Any]:
        return {**default, **base.get(section, {}), **local.get(section, {})}

    server = merged(
        "server",
        {"name": "staged-rag", "transport": "stdio", "host": "127.0.0.1", "port": 8000},
    )
    embedding = merged(
        "embedding",
        {"provider": "gemini", "model": "gemini-embedding-001", "dimensions": 3072, "batch_size": 16, "provider_config": {}},
    )
    generation = merged(
        "generation",
        {"model": "gemini-1.5-flash", "summary_max_sentences": 4},
    )
    chunking = merged(
        "chunking",
        {"chunk_size": 200, "chunk_overlap": 20, "min_chunk_size": 50},
    )
    retrieval = merged(
        "retrieval",
        {
            "default_top_k": 5,
            "max_top_k": 50,
            "default_collection": "default",
            "hybrid_semantic_weight": 0.7,
            "hybrid_keyword_weight": 0.3,
            "min_similarity_score": 0.0,
        },
    )
    storage = merged(
        "storage",
        {
            "data_dir": "./data",
            "store_dir": "./data/store",
            "index_dir": "./data/index",
            "log_dir": "./data/logs",
        },
    )
    ingestion = merged(
        "ingestion",
        {"max_document_tokens": 50000, "max_batch_size": 50, "auto_summary": True},
    )
    logging_cfg = merged(
        "logging",
        {"audit_file": "./data/logs/audit.jsonl", "max_log_entries": 10000, "log_level": "INFO"},
    )
    knowledge_base = merged(
        "knowledge_base",
        {
            "enabled": False,
            "kb_dir": "./knowledge_base",
            "manifest_file": "./data/kb_manifest.json",
            "collection": "default",
            "poll_interval": 5.0,
            "max_file_size": 10485760,
        },
    )

    storage_cfg = StorageConfig(
        data_dir=root_path / storage["data_dir"],
        store_dir=root_path / storage["store_dir"],
        index_dir=root_path / storage["index_dir"],
        log_dir=root_path / storage["log_dir"],
    )

    return Settings(
        server=ServerConfig(**server),
        embedding=EmbeddingConfig(**embedding),
        generation=GenerationConfig(**generation),
        chunking=ChunkingConfig(**chunking),
        retrieval=RetrievalConfig(**retrieval),
        storage=storage_cfg,
        ingestion=IngestionConfig(**ingestion),
        logging=LoggingConfig(
            audit_file=root_path / logging_cfg["audit_file"],
            max_log_entries=int(logging_cfg["max_log_entries"]),
            log_level=str(logging_cfg["log_level"]),
        ),
        knowledge_base=KnowledgeBaseConfig(
            enabled=bool(knowledge_base["enabled"]),
            kb_dir=root_path / knowledge_base["kb_dir"],
            manifest_file=root_path / knowledge_base["manifest_file"],
            collection=str(knowledge_base["collection"]),
            poll_interval=float(knowledge_base["poll_interval"]),
            max_file_size=int(knowledge_base["max_file_size"]),
        ),
    )
