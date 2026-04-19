from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from app.embedder import OpenAIEmbedder
from app.vector_store import PineconeVectorStore

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RetrievedChunk:
    id: str
    text: str
    score: float | None
    metadata: Mapping[str, Any]


class ResearchPaperRetriever:
    def __init__(self, embedder: OpenAIEmbedder, vector_store: PineconeVectorStore) -> None:
        self.embedder = embedder
        self.vector_store = vector_store

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        logger.info("Retrieving chunks query_chars=%s top_k=%s", len(query), top_k)
        query_embedding = await self.embedder.embed(query)
        records = self.vector_store.query(query_embedding, top_k=top_k)

        chunks: list[RetrievedChunk] = []
        for record in records:
            text = record.metadata.get("text")
            chunks.append(
                RetrievedChunk(
                    id=record.id,
                    text=text if isinstance(text, str) else "",
                    score=record.score,
                    metadata=record.metadata,
                )
            )

        logger.info("Retrieved chunks count=%s", len(chunks))
        return chunks
