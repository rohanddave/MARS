from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OpenAISettings:
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_answer_model: str = "gpt-4.1-mini"
    openai_answer_max_output_tokens: int = 512
    openai_embedding_model: str = "text-embedding-3-small"
    openai_embedding_dimensions: int = 1536
    openai_timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> "OpenAISettings":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_base_url=os.getenv("OPENAI_BASE_URL", cls.openai_base_url),
            openai_answer_model=os.getenv("OPENAI_ANSWER_MODEL", cls.openai_answer_model),
            openai_answer_max_output_tokens=int(
                os.getenv("OPENAI_ANSWER_MAX_OUTPUT_TOKENS", cls.openai_answer_max_output_tokens)
            ),
            openai_embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", cls.openai_embedding_model),
            openai_embedding_dimensions=int(os.getenv("OPENAI_EMBEDDING_DIMENSIONS", cls.openai_embedding_dimensions)),
            openai_timeout_seconds=float(os.getenv("OPENAI_TIMEOUT_SECONDS", cls.openai_timeout_seconds)),
        )


@dataclass(frozen=True)
class PineconeSettings:
    pinecone_api_key: str = "pclocal"
    pinecone_host: str = "http://localhost:5080"
    pinecone_index_name: str = "mars-embeddings"
    pinecone_namespace: str = "__default__"
    pinecone_dimension: int = 1536
    pinecone_metric: str = "cosine"

    @classmethod
    def from_env(cls) -> "PineconeSettings":
        return cls(
            pinecone_api_key=os.getenv("PINECONE_API_KEY", cls.pinecone_api_key),
            pinecone_host=os.getenv("PINECONE_HOST", cls.pinecone_host),
            pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", cls.pinecone_index_name),
            pinecone_namespace=os.getenv("PINECONE_NAMESPACE", cls.pinecone_namespace),
            pinecone_dimension=int(os.getenv("PINECONE_DIMENSION", cls.pinecone_dimension)),
            pinecone_metric=os.getenv("PINECONE_METRIC", cls.pinecone_metric),
        )
