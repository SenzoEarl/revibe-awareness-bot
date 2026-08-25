"""Collector registry with explicit enablement."""

from __future__ import annotations

from revibe_bot.collectors.base import ReviewCollector


class CollectorRegistry:
    def __init__(self) -> None:
        self._collectors: dict[str, ReviewCollector] = {}

    def register(self, collector: ReviewCollector) -> None:
        if collector.source_name in self._collectors:
            raise ValueError(f"collector already registered: {collector.source_name}")
        self._collectors[collector.source_name] = collector

    def get(self, source_name: str) -> ReviewCollector:
        try:
            return self._collectors[source_name]
        except KeyError as exc:
            raise KeyError(f"collector is not enabled: {source_name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._collectors))
