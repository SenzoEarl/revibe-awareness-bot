"""Strict schemas for model-assisted analysis."""
from pydantic import BaseModel, Field
from revibe_bot.domain import ComplaintCategory, EvidenceStatus

class ClaimExtraction(BaseModel):
    claim: str = Field(min_length=1)
    attribution: str = Field(min_length=1)
    category: ComplaintCategory
    evidence_status: EvidenceStatus
    confidence: float = Field(ge=0, le=1)
    requires_verification: bool

class GeneratedPost(BaseModel):
    text: str = Field(min_length=1, max_length=280)
    claim_ids: list[str]
    evidence_ids: list[str]
    attribution_required: bool = True
    requires_human_review: bool = True
    rationale: str = Field(min_length=1)

class FactCheckResult(BaseModel):
    supported: bool
    contradictions: list[str] = []
    missing_evidence: list[str] = []
    privacy_issue: bool = False
    attribution_issue: bool = False
    recommended_action: str

class SafetyResult(BaseModel):
    safe: bool
    flags: list[str] = []
    requires_human_review: bool = True
    reason: str = Field(min_length=1)
