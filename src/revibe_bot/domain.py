"""Core evidence-domain models.

These models deliberately separate what a reviewer said from what the system
can establish. A claim is attributed and carries an evidence status; it is not
silently promoted to fact.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class EvidenceStatus(StrEnum):
    ALLEGATION = "allegation"
    OPINION = "opinion"
    VERIFIED_FACT = "verified_fact"
    PATTERN = "pattern"
    COMPANY_RESPONSE = "company_response"
    NEEDS_VERIFICATION = "needs_verification"


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


class NormalizedReview(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    source_url: HttpUrl
    source_review_id: str | None = None
    published_at: datetime | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    text: str = Field(min_length=1)
    company_response: str | None = None
    content_hash: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExtractedClaim(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    evidence_status: EvidenceStatus
    category: ComplaintCategory
    confidence: float = Field(ge=0, le=1)
    source_review_hash: str
    requires_verification: bool = False


class EvidenceRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    claim_text: str = Field(min_length=1)
    source_url: HttpUrl
    source: str
    source_published_at: datetime | None = None
    evidence_status: EvidenceStatus
    supporting_review_hashes: list[str] = Field(min_length=1)
    independent_source_count: int = Field(default=1, ge=1)
    confidence: float = Field(ge=0, le=1)
    company_response_available: bool = False
    verified_at: datetime | None = None


class PostCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=280)
    evidence_ids: list[str] = Field(min_length=1)
    requires_human_review: bool = True
    privacy_passed: bool = False
    evidence_passed: bool = False
    safety_passed: bool = False
    duplicate: bool = False
    created_at: datetime


class PatternSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: ComplaintCategory
    period_start: date
    period_end: date
    review_count: int = Field(ge=1)
    independent_source_count: int = Field(ge=1)
    percentage_of_reviews: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    company_response_count: int = Field(ge=0)
