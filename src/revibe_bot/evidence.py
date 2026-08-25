"""Evidence linking and publication preconditions."""
from __future__ import annotations

from revibe_bot.domain import EvidenceRecord, EvidenceStatus, PostCandidate


def evidence_is_publishable(evidence: list[EvidenceRecord]) -> bool:
    if not evidence:
        return False
    return all(
        item.evidence_status in {EvidenceStatus.ALLEGATION, EvidenceStatus.OPINION, EvidenceStatus.VERIFIED_FACT, EvidenceStatus.PATTERN, EvidenceStatus.COMPANY_RESPONSE}
        and item.confidence >= 0.70
        and item.source_url
        and item.supporting_review_hashes
        for item in evidence
    )


def bind_evidence(candidate: PostCandidate, evidence: list[EvidenceRecord]) -> PostCandidate:
    if not evidence_is_publishable(evidence):
        candidate.evidence_passed = False
        candidate.requires_human_review = True
        return candidate
    candidate.evidence_passed = True
    return candidate
