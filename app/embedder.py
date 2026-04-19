from __future__ import annotations

import logging
from typing import Any

import httpx

from app.llm_client import LLMClient, LLMClientError
from app.openai_rate_limit import retry_after_seconds, trigger_openai_cooldown, wait_for_openai_cooldown

logger = logging.getLogger(__name__)


class OpenAIEmbedder:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    async def embed(self, text: str) -> list[float]:
        settings = self.llm_client.settings
        if not settings.openai_api_key:
            logger.error("OpenAI API key is not configured; embedding request cannot run")
            raise LLMClientError("OpenAI embedding is not configured. Set OPENAI_API_KEY to enable embeddings.")

        logger.info(
            "Sending embedding request model=%s text_chars=%s dimensions=%s",
            settings.openai_embedding_model,
            len(text),
            settings.openai_embedding_dimensions,
        )
        body = {
            "model": settings.openai_embedding_model,
            "input": text,
            "encoding_format": "float",
            "dimensions": settings.openai_embedding_dimensions,
        }

        response = await _post_embedding_with_rate_limit_retry(settings, body)

        if not 200 <= response.status_code < 300:
            logger.error("OpenAI Embeddings API failed status=%s body=%s", response.status_code, response.text)
            raise LLMClientError(f"OpenAI Embeddings API request failed: {response.status_code} {response.text}")

        embedding = _extract_embedding(response.json())
        logger.info("Embedding finished vector_dimensions=%s", len(embedding))
        return embedding


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


async def _post_embedding_with_rate_limit_retry(settings: object, body: dict[str, Any]) -> httpx.Response:
    url = f"{settings.openai_base_url.rstrip('/')}/embeddings"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    max_retries = max(0, settings.openai_max_retries)

    for attempt in range(1, max_retries + 2):
        await wait_for_openai_cooldown("embeddings")
        async with httpx.AsyncClient(timeout=settings.openai_timeout_seconds) as client:
            response = await client.post(url, json=body, headers=headers)

        if response.status_code != 429:
            return response

        if attempt > max_retries:
            return response

        sleep_seconds = retry_after_seconds(
            response.headers,
            fallback_seconds=settings.openai_rate_limit_fallback_seconds,
            attempt=attempt,
        )
        logger.warning(
            "OpenAI rate limited embedding request attempt=%s/%s sleep_seconds=%.1f body=%s",
            attempt,
            max_retries + 1,
            sleep_seconds,
            response.text[:500],
        )
        await trigger_openai_cooldown(sleep_seconds, "embeddings")

    raise LLMClientError("OpenAI embedding retry loop ended unexpectedly")
