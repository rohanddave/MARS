from __future__ import annotations

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
        body = {
            "model": self.settings.openai_answer_model,
            "instructions": instructions
            or (
                "You answer questions about a code repository. Use only the supplied context. "
                "When the context is insufficient, say what is missing instead of guessing."
            ),
            "input": prompt,
            "max_output_tokens": max_output_tokens or self.settings.openai_answer_max_output_tokens,
        }

        async with httpx.AsyncClient(timeout=self.settings.openai_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.openai_base_url.rstrip('/')}/responses",
                json=body,
                headers={
                    "Authorization": f"Bearer {self.settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
            )

        if not 200 <= response.status_code < 300:
            logger.error("OpenAI Responses API failed status=%s body=%s", response.status_code, response.text)
            raise LLMClientError(f"OpenAI Responses API request failed: {response.status_code} {response.text}")

        payload = response.json()
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
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    parts: list[str] = []
    for item in payload.get("output") or []:
        for content in item.get("content") or []:
            text = content.get("text")
            if isinstance(text, str) and text:
                parts.append(text)

    answer = "\n".join(parts).strip()
    if not answer:
        raise LLMClientError("OpenAI Responses API response did not include output text")
    return answer


def _extract_token_usage(payload: dict[str, Any]) -> TokenUsage:
    usage = payload.get("usage")
    if not isinstance(usage, dict):
        return TokenUsage()

    input_tokens = _optional_int(usage.get("input_tokens"))
    output_tokens = _optional_int(usage.get("output_tokens"))
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
