from __future__ import annotations

import json
import logging
import numpy as np
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EmbeddingRecord:
    id: str
    values: list[float]
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievedRecord:
    id: str
    score: float | None
    metadata: Mapping[str, Any]


class PineconeVectorStore:
    """In-process vector store using numpy cosine similarity.
    Drop-in replacement for the Pinecone-backed store — same public API.
    Persists to a JSON file so data survives across runs.
    """

    def __init__(self, settings: Any) -> None:
        self.settings = settings
        self._store_path = Path(getattr(settings, "vector_store_path", "data/vector_store.json"))
        self._ids: list[str] = []
        self._vectors: list[list[float]] = []
        self._metadata: list[dict[str, Any]] = []
        self._load()
        logger.info(
            "Local vector store ready path=%s records=%s",
            self._store_path,
            len(self._ids),
        )

    def insert_embedding(
        self,
        record_id: str,
        embedding: list[float],
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        self.insert_embeddings(
            [
                EmbeddingRecord(
                    id=record_id,
                    values=embedding,
                    metadata=metadata or {},
                )
            ]
        )

    def insert_embeddings(self, records: list[EmbeddingRecord]) -> None:
        logger.info("Upserting embeddings count=%s", len(records))
        existing_ids = {rid: idx for idx, rid in enumerate(self._ids)}
        for record in records:
            meta = dict(record.metadata)
            if record.id in existing_ids:
                idx = existing_ids[record.id]
                self._vectors[idx] = record.values
                self._metadata[idx] = meta
            else:
                existing_ids[record.id] = len(self._ids)
                self._ids.append(record.id)
                self._vectors.append(record.values)
                self._metadata.append(meta)
        self._save()
        logger.info("Upsert complete count=%s total=%s", len(records), len(self._ids))

    def query(self, embedding: list[float], top_k: int = 5) -> list[RetrievedRecord]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if not self._ids:
            logger.info("Query on empty store, returning no results")
            return []

        logger.info("Querying local vector store top_k=%s records=%s", top_k, len(self._ids))
        query_vec = np.array(embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return []

        matrix = np.array(self._vectors, dtype=np.float32)
        norms = np.linalg.norm(matrix, axis=1)
        norms[norms == 0] = 1.0
        scores = matrix @ query_vec / (norms * query_norm)

        top_indices = np.argsort(scores)[::-1][:top_k]

        records = [
            RetrievedRecord(
                id=self._ids[i],
                score=float(scores[i]),
                metadata=self._metadata[i],
            )
            for i in top_indices
        ]
        logger.info("Query returned matches=%s", len(records))
        return records

    def _load(self) -> None:
        if not self._store_path.exists():
            logger.info("No existing vector store at path=%s", self._store_path)
            return
        try:
            payload = json.loads(self._store_path.read_text(encoding="utf-8"))
            self._ids = payload.get("ids", [])
            self._vectors = payload.get("vectors", [])
            self._metadata = payload.get("metadata", [])
            logger.info("Loaded vector store path=%s records=%s", self._store_path, len(self._ids))
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("Could not load vector store path=%s error=%s, starting fresh", self._store_path, exc)

    def _save(self) -> None:
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self._store_path.with_suffix(".json.tmp")
        payload = {
            "ids": self._ids,
            "vectors": self._vectors,
            "metadata": self._metadata,
        }
        tmp_path.write_text(json.dumps(payload), encoding="utf-8")
        tmp_path.replace(self._store_path)
