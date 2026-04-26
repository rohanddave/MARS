from __future__ import annotations

import asyncio
import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

MODEL_NAME = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIMENSIONS = 1024


class OpenAIEmbedder:
    def __init__(self) -> None:
        logger.info("Loading sentence-transformer model=%s", MODEL_NAME)
        self._model = SentenceTransformer(MODEL_NAME, device="cpu")
        self.model_name = MODEL_NAME
        self.embedding_dimensions = EMBEDDING_DIMENSIONS
        logger.info("Sentence-transformer model loaded dimensions=%s", EMBEDDING_DIMENSIONS)

    async def embed(self, text: str) -> list[float]:
        logger.info("Embedding text text_chars=%s model=%s", len(text), MODEL_NAME)
        embedding = await asyncio.to_thread(self._encode, text)
        logger.info("Embedding finished vector_dimensions=%s", len(embedding))
        return embedding

    def _encode(self, text: str) -> list[float]:
        vector = self._model.encode(text, normalize_embeddings=True)
        return vector.tolist()
