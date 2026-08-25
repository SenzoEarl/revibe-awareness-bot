from datetime import datetime, timezone

from revibe_bot.domain import PostCandidate
from revibe_bot.moderation.gate import Decision, PublishingMode, evaluate


def candidate(text: str, *, review: bool = False) -> PostCandidate:
    return PostCandidate(
        text=text,
        evidence_ids=["e1"],
        requires_human_review=review,
        privacy_passed=True,
        evidence_passed=True,
        safety_passed=True,
        duplicate=False,
        created_at=datetime.now(timezone.utc),
    )


def test_paused_never_approves():
    assert evaluate(candidate("Neutral consumer information"), mode=PublishingMode.PAUSED).decision == Decision.REJECT


def test_review_mode_requires_human():
    assert evaluate(candidate("Neutral consumer information"), mode=PublishingMode.REVIEW).decision == Decision.REVIEW


def test_high_risk_language_requires_review():
    assert evaluate(candidate("Customers say the company stole their money"), mode=PublishingMode.SAFE).decision == Decision.REVIEW


def test_duplicate_requires_review():
    assert evaluate(candidate("Neutral consumer information"), mode=PublishingMode.SAFE, duplicate=True).decision == Decision.REVIEW


def test_missing_evidence_rejects():
    c = candidate("Neutral consumer information")
    c.evidence_passed = False
    assert evaluate(c, mode=PublishingMode.SAFE).decision == Decision.REJECT
