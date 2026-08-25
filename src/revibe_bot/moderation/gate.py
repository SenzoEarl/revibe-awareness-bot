"""Fail-closed moderation and publication gate."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import re

from revibe_bot.domain import PostCandidate


class PublishingMode(StrEnum):
    SAFE = "safe"
    REVIEW = "review"
    PAUSED = "paused"


class Decision(StrEnum):
    APPROVE = "approve"
    REVIEW = "review"
    REJECT = "reject"


@dataclass(frozen=True)
class GateResult:
    decision: Decision
    flags: tuple[str, ...]
    reason: str


HIGH_RISK_PATTERNS = (
    r"\b(scam|fraud|stole|stealing|criminal|thief|thieves)\b",
    r"\b(harass|harassment|brigade|brigading|mass[- ]report)\b",
    r"\b(doxx|doxxing|personal information|home address)\b",
)


def _risk_flags(text: str) -> list[str]:
    flags: list[str] = []
    lowered = text.lower()
    for pattern in HIGH_RISK_PATTERNS:
        if re.search(pattern, lowered):
            flags.append(pattern)
    if len(text) > 280:
        flags.append("length")
    return flags


def evaluate(candidate: PostCandidate, *, mode: PublishingMode, duplicate: bool = False) -> GateResult:
    flags = _risk_flags(candidate.text)
    if duplicate:
        flags.append("duplicate")
    if mode == PublishingMode.PAUSED:
        return GateResult(Decision.REJECT, tuple(flags + ["publishing_paused"]), "publishing is paused")
    if not candidate.evidence_passed or not candidate.privacy_passed:
        return GateResult(Decision.REJECT, tuple(flags + ["precondition_failed"]), "evidence/privacy precondition failed")
    if flags:
        return GateResult(Decision.REVIEW, tuple(flags), "risk or duplication requires human review")
    if mode == PublishingMode.REVIEW or candidate.requires_human_review:
        return GateResult(Decision.REVIEW, tuple(flags), "human approval required")
    if not candidate.safety_passed:
        return GateResult(Decision.REJECT, ("safety_failed",), "safety gate failed")
    return GateResult(Decision.APPROVE, tuple(flags), "all publication gates passed")
