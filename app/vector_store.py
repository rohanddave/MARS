from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from pinecone import ServerlessSpec
from pinecone.grpc import GRPCClientConfig, PineconeGRPC

from app.config import PineconeSettings


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
        self._client = PineconeGRPC(api_key=settings.pinecone_api_key, host=settings.pinecone_host)
        self._ensure_index()
        index_host = self._client.describe_index(name=settings.pinecone_index_name).host
        self._index = self._client.Index(host=index_host, grpc_config=GRPCClientConfig(secure=False))

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
        vectors = [
            {
                "id": record.id,
                "values": record.values,
                "metadata": dict(record.metadata),
            }
            for record in records
        ]
        self._index.upsert(vectors=vectors, namespace=self.settings.pinecone_namespace)

    def query(self, embedding: list[float], top_k: int = 5) -> list[RetrievedRecord]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        response = self._index.query(
            vector=embedding,
            top_k=top_k,
            namespace=self.settings.pinecone_namespace,
            include_metadata=True,
        )

        matches = getattr(response, "matches", None) or []
        return [
            RetrievedRecord(
                id=match.get("id") if isinstance(match, dict) else match.id,
                score=match.get("score") if isinstance(match, dict) else match.score,
                metadata=match.get("metadata", {}) if isinstance(match, dict) else match.metadata or {},
            )
            for match in matches
        ]

    def _ensure_index(self) -> None:
        if self._client.has_index(self.settings.pinecone_index_name):
            return

        self._client.create_index(
            name=self.settings.pinecone_index_name,
            vector_type="dense",
            dimension=self.settings.pinecone_dimension,
            metric=self.settings.pinecone_metric,
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            deletion_protection="disabled",
            tags={"environment": "local"},
        )
