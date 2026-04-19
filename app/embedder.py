from __future__ import annotations

from typing import Any

import httpx

from app.llm_client import LLMClient, LLMClientError


class OpenAIEmbedder:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def embed(self, text: str) -> list[float]:
        settings = self.llm_client.settings
        if not settings.openai_api_key:
            raise LLMClientError("OpenAI embedding is not configured. Set OPENAI_API_KEY to enable embeddings.")

        body = {
            "model": settings.openai_embedding_model,
            "input": text,
            "encoding_format": "float",
            "dimensions": settings.openai_embedding_dimensions,
        }

        async with httpx.AsyncClient(timeout=settings.openai_timeout_seconds) as client:
            response = await client.post(
                f"{settings.openai_base_url.rstrip('/')}/embeddings",
                json=body,
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
            )

        if not 200 <= response.status_code < 300:
            raise LLMClientError(f"OpenAI Embeddings API request failed: {response.status_code} {response.text}")

        return _extract_embedding(response.json())


def _extract_embedding(payload: dict[str, Any]) -> list[float]:
    data = payload.get("data")
    if not isinstance(data, list) or not data:
        raise LLMClientError("OpenAI Embeddings API response did not include embedding data")

    embedding = data[0].get("embedding") if isinstance(data[0], dict) else None
    if not isinstance(embedding, list) or not embedding:
        raise LLMClientError("OpenAI Embeddings API response did not include an embedding")

    if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in embedding):
        raise LLMClientError("OpenAI Embeddings API response included a non-numeric embedding value")

    return [float(value) for value in embedding]
