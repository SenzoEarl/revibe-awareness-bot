"""Core domain models for evidence-first review processing."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Optional

class EvidenceStatus(StrEnum):
    UNVERIFIED = "unverified"
    VERIFIED_PUBLIC_SOURCE = "verified_public_source"
    INSUFFICIENT = "insufficient_evidence"

class PublishingMode(StrEnum):
    SAFE = "safe"
    REVIEW = "review"
    PAUSED = "paused"

class ComplaintCategory(StrEnum):
    REFUND = "refund"
    DEVICE_CONDITION = "device_condition"
    DEVICE_FUNCTIONALITY = "device_functionality"
    WARRANTY = "warranty"
    DELIVERY = "delivery"
    CANCELLATION = "cancellation"
    CUSTOMER_SERVICE = "customer_service"
    COMMUNICATION = "communication"
    PRICING = "pricing"
    TRADE_IN = "trade_in"
    REPLACEMENT = "replacement"
    REPAIR = "repair"
    TERMS = "terms"
    ACCOUNT = "account"
    OTHER = "other"

@dataclass(frozen=True)
class Review:
    source: str
    source_url: str
    published_at: datetime
    text: str
    rating: Optional[float] = None
    external_id: Optional[str] = None
    company_response: Optional[str] = None
    content_hash: str = ""
    duplicate_of: Optional[str] = None

@dataclass(frozen=True)
class Claim:
    statement: str
    attribution: str
    category: ComplaintCategory
    confidence: float
    evidence_status: EvidenceStatus

@dataclass
class CandidatePost:
    text: str
    claim_ids: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    requires_human_review: bool = True
    status: str = "draft"
