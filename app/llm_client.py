from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from app.config import OpenAISettings
from app.models.answer import CompletionResult, TokenUsage

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, settings: OpenAISettings) -> None:
        self.settings = settings

    async def complete(
        self,
        prompt: str,
        instructions: str | None = None,
        max_output_tokens: int | None = None,
    ) -> CompletionResult:
        if not self.settings.openai_api_key:
            logger.warning("OpenAI API key is not configured; returning placeholder LLM response")
            return CompletionResult(
                text="LLM answering is not configured yet. Set OPENAI_API_KEY to enable generated answers.",
                token_usage=TokenUsage(input_tokens=0, output_tokens=0, total_tokens=0),
            )

        logger.info(
            "Sending completion request model=%s prompt_chars=%s max_output_tokens=%s",
            self.settings.openai_answer_model,
            len(prompt),
            self.settings.openai_answer_max_output_tokens,
        )
        system_message = instructions or (
            "You answer questions about a code repository. Use only the supplied context. "
            "When the context is insufficient, say what is missing instead of guessing."
        )
        body: dict[str, Any] = {
            "model": self.settings.openai_answer_model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": max_output_tokens or self.settings.openai_answer_max_output_tokens,
        }

        url = f"{self.settings.openai_base_url.rstrip('/')}/chat/completions"
        try:
            async with httpx.AsyncClient(timeout=self.settings.openai_timeout_seconds) as client:
                response = await client.post(
                    url,
                    json=body,
                    headers={
                        "Authorization": f"Bearer {self.settings.openai_api_key}",
                        "Content-Type": "application/json",
                    },
                )
        except httpx.ConnectError as exc:
            logger.error("Cannot connect to LLM server url=%s error=%s", url, exc)
            raise LLMClientError(
                f"Cannot connect to LLM server at {self.settings.openai_base_url} — "
                f"is the vLLM/inference server running? (error: {exc})"
            ) from exc
        except httpx.TimeoutException as exc:
            logger.error("LLM request timed out url=%s timeout=%s error=%s", url, self.settings.openai_timeout_seconds, exc)
            raise LLMClientError(
                f"LLM request timed out after {self.settings.openai_timeout_seconds}s "
                f"to {self.settings.openai_base_url} (error: {exc})"
            ) from exc

        if response.status_code == 429:
            retry_after = float(response.headers.get("retry-after", 0))
            wait = max(retry_after, 10.0)
            logger.warning("Rate limited (429), retrying in %.1fs", wait)
            await asyncio.sleep(wait)
            return await self.complete(prompt, instructions, max_output_tokens)

        if not 200 <= response.status_code < 300:
            logger.error("LLM API request failed url=%s status=%s body=%s", url, response.status_code, response.text)
            raise LLMClientError(f"LLM API request failed: {response.status_code} {response.text}")

        try:
            payload = response.json()
        except Exception as exc:
            logger.error("LLM response is not valid JSON url=%s body=%s", url, response.text[:500])
            raise LLMClientError(f"LLM returned non-JSON response: {response.text[:200]}") from exc
        result = CompletionResult(
            text=_extract_text(payload),
            token_usage=_extract_token_usage(payload),
        )
        logger.info(
            "Completion finished model=%s output_chars=%s total_tokens=%s",
            self.settings.openai_answer_model,
            len(result.text),
            result.token_usage.total_tokens,
        )
        return result


class LLMClientError(RuntimeError):
    pass


def _extract_text(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content.strip()

    raise LLMClientError("Chat completions response did not include message content")


def _extract_token_usage(payload: dict[str, Any]) -> TokenUsage:
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return TokenUsage()

    input_tokens = _optional_int(usage.get("prompt_tokens"))
    output_tokens = _optional_int(usage.get("completion_tokens"))
    total_tokens = _optional_int(usage.get("total_tokens"))
    if total_tokens is None and input_tokens is not None and output_tokens is not None:
        total_tokens = input_tokens + output_tokens

    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
    )


def _optional_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    return None
