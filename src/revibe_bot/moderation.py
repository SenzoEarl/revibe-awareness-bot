from dataclasses import dataclass
from .models import CandidatePost, PublishingMode

@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    requires_review: bool
    flags: tuple[str, ...]

BLOCKED = {
    "harassment", "brigading", "impersonation", "private_information",
    "fabricated_evidence", "unsupported_criminal_claim", "engagement_manipulation",
    "enforcement_evasion", "threat", "targeted_employee_attack", "spam"
}

def review_post(post: CandidatePost, mode: PublishingMode) -> SafetyDecision:
    flags = tuple(sorted(set(post.risk_flags)))
    if BLOCKED.intersection(flags):
        return SafetyDecision(False, True, flags)
    if mode is PublishingMode.PAUSED:
        return SafetyDecision(False, True, flags)
    if post.requires_human_review or mode is PublishingMode.REVIEW:
        return SafetyDecision(False, True, flags)
    return SafetyDecision(True, False, flags)
