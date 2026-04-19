from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenUsage:
    input_tokens: int | None = 0
    output_tokens: int | None = 0
    total_tokens: int | None = 0


@dataclass(frozen=True)
class CompletionResult:
    text: str
    token_usage: TokenUsage
