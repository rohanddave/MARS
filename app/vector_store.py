from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from pinecone import ServerlessSpec
from pinecone.grpc import GRPCClientConfig, PineconeGRPC

from app.config import PineconeSettings

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
    def __init__(self, settings: PineconeSettings) -> None:
        self.settings = settings
        logger.info(
            "Connecting to Pinecone host=%s index=%s namespace=%s",
            settings.pinecone_host,
            settings.pinecone_index_name,
            settings.pinecone_namespace,
        )
        self._client = PineconeGRPC(api_key=settings.pinecone_api_key, host=settings.pinecone_host)
        self._ensure_index()
        index_host = self._client.describe_index(name=settings.pinecone_index_name).host
        self._index = self._client.Index(host=index_host, grpc_config=GRPCClientConfig(secure=False))
        logger.info("Pinecone index ready index=%s host=%s", settings.pinecone_index_name, index_host)

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
        logger.info(
            "Upserting embeddings count=%s index=%s namespace=%s",
            len(records),
            self.settings.pinecone_index_name,
            self.settings.pinecone_namespace,
        )
        vectors = [
            {
                "id": record.id,
                "values": record.values,
                "metadata": dict(record.metadata),
            }
            for record in records
        ]
        self._index.upsert(vectors=vectors, namespace=self.settings.pinecone_namespace)
        logger.info("Upsert complete count=%s", len(records))

    def query(self, embedding: list[float], top_k: int = 5) -> list[RetrievedRecord]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        logger.info(
            "Querying Pinecone index=%s namespace=%s top_k=%s vector_dimensions=%s",
            self.settings.pinecone_index_name,
            self.settings.pinecone_namespace,
            top_k,
            len(embedding),
        )
        response = self._index.query(
            vector=embedding,
            top_k=top_k,
            namespace=self.settings.pinecone_namespace,
            include_metadata=True,
        )

        matches = getattr(response, "matches", None) or []
        records = [
            RetrievedRecord(
                id=match.get("id") if isinstance(match, dict) else match.id,
                score=match.get("score") if isinstance(match, dict) else match.score,
                metadata=match.get("metadata", {}) if isinstance(match, dict) else match.metadata or {},
            )
            for match in matches
        ]
        logger.info("Pinecone query returned matches=%s", len(records))
        return records

    def _ensure_index(self) -> None:
        if self._client.has_index(self.settings.pinecone_index_name):
            logger.info("Pinecone index already exists index=%s", self.settings.pinecone_index_name)
            return

        logger.info(
            "Creating Pinecone index index=%s dimension=%s metric=%s",
            self.settings.pinecone_index_name,
            self.settings.pinecone_dimension,
            self.settings.pinecone_metric,
        )
        self._client.create_index(
            name=self.settings.pinecone_index_name,
            vector_type="dense",
            dimension=self.settings.pinecone_dimension,
            metric=self.settings.pinecone_metric,
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            deletion_protection="disabled",
            tags={"environment": "local"},
        )
