from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Mapping

logger = logging.getLogger(__name__)

_COOLDOWN_LOCK: asyncio.Lock | None = None
_COOLDOWN_UNTIL = 0.0


def _cooldown_lock() -> asyncio.Lock:
    global _COOLDOWN_LOCK
    if _COOLDOWN_LOCK is None:
        _COOLDOWN_LOCK = asyncio.Lock()
    return _COOLDOWN_LOCK


async def wait_for_openai_cooldown(label: str) -> None:
    while True:
        async with _cooldown_lock():
            sleep_seconds = _COOLDOWN_UNTIL - time.monotonic()

        if sleep_seconds <= 0:
            return

        logger.warning(
            "OpenAI global cooldown active label=%s sleep_seconds=%.1f",
            label,
            sleep_seconds,
        )
        await asyncio.sleep(sleep_seconds)


async def trigger_openai_cooldown(seconds: float, label: str) -> None:
    if seconds <= 0:
        return

    global _COOLDOWN_UNTIL
    async with _cooldown_lock():
        now = time.monotonic()
        cooldown_until = now + seconds
        if cooldown_until > _COOLDOWN_UNTIL:
            _COOLDOWN_UNTIL = cooldown_until
            logger.warning(
                "OpenAI global cooldown set label=%s sleep_seconds=%.1f",
                label,
                seconds,
            )
        sleep_seconds = max(0.0, _COOLDOWN_UNTIL - now)

    if sleep_seconds > 0:
        await asyncio.sleep(sleep_seconds)


def retry_after_seconds(headers: Mapping[str, str], fallback_seconds: float, attempt: int) -> float:
    retry_after = headers.get("retry-after") or headers.get("Retry-After")
    if retry_after:
        parsed_seconds = _parse_retry_after(retry_after)
        if parsed_seconds is not None:
            return max(0.0, parsed_seconds)

    return max(fallback_seconds, fallback_seconds * attempt)


def _parse_retry_after(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        pass

    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=timezone.utc)
    return (retry_at - datetime.now(timezone.utc)).total_seconds()
