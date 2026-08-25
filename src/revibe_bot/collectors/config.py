"""Load and validate source policies without enabling collectors implicitly."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class SourceConfig:
    name: str
    enabled: bool
    mode: str
    official_api_required: bool
    respect_robots: bool
    min_interval_seconds: float
    notes: str = ""


def load_source_config(path: str | Path) -> dict[str, SourceConfig]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    result: dict[str, SourceConfig] = {}
    for name, raw in data.get("sources", {}).items():
        result[name] = SourceConfig(
            name=name,
            enabled=bool(raw.get("enabled", False)),
            mode=str(raw.get("mode", "disabled")),
            official_api_required=bool(raw.get("official_api_required", True)),
            respect_robots=bool(raw.get("respect_robots", True)),
            min_interval_seconds=max(0.5, float(raw.get("min_interval_seconds", 2))),
            notes=str(raw.get("notes", "")),
        )
    return result
