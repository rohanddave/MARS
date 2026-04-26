from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class OpenAISettings:
    openai_api_key: str | None = None
    openai_base_url: str = "http://localhost:8000/v1"
    openai_answer_model: str = "google/gemma-4-26B-A4B-it"
    openai_answer_max_output_tokens: int = 512
    openai_timeout_seconds: float = 120.0

    @classmethod
    def from_env(cls) -> "OpenAISettings":
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_base_url=os.getenv("OPENAI_BASE_URL", cls.openai_base_url),
            openai_answer_model=os.getenv("OPENAI_ANSWER_MODEL", cls.openai_answer_model),
            openai_answer_max_output_tokens=int(
                os.getenv("OPENAI_ANSWER_MAX_OUTPUT_TOKENS", cls.openai_answer_max_output_tokens)
            ),
            openai_timeout_seconds=float(os.getenv("OPENAI_TIMEOUT_SECONDS", cls.openai_timeout_seconds)),
        )


@dataclass(frozen=True)
class PineconeSettings:
    vector_store_path: str = "data/vector_store.json"

    @classmethod
    def from_env(cls) -> "PineconeSettings":
        return cls(
            vector_store_path=os.getenv("VECTOR_STORE_PATH", cls.vector_store_path),
        )
