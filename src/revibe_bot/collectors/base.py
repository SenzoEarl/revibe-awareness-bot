"""Compliant public-source collector interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from revibe_bot.domain import NormalizedReview


class SourcePolicyError(RuntimeError):
    """Raised when a collector is not allowed to access a source."""


class ReviewCollector(ABC):
    """Adapter contract for a public review source.

    Implementations must use an official API when available and must not
    bypass authentication, CAPTCHAs, robots restrictions, anti-bot controls,
    paywalls, or source rate limits.
    """

    source_name: str

    @abstractmethod
    async def collect(self, *, since: str | None = None) -> AsyncIterator[NormalizedReview]:
        """Yield normalized public reviews according to source policy."""
        raise NotImplementedError
