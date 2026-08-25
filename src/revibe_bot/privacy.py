"""Privacy filtering and conservative PII redaction."""

import hashlib
import re
from dataclasses import dataclass

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE = re.compile(r"(?<!\w)(?:\+?27\s?|0)(?:\d[\s-]?){8,10}(?!\w)")
ID_NUMBER = re.compile(r"(?<!\w)\d{13}(?!\w)")
ORDER = re.compile(r"\b(?:order|tracking|ticket|reference|ref)\s*[:#-]?\s*[A-Z0-9-]{5,}\b", re.I)


@dataclass(frozen=True)
class RedactionResult:
    text: str
    redactions: tuple[str, ...]


def redact_pii(text: str) -> RedactionResult:
    """Redact high-confidence PII while preserving the surrounding claim text."""
    redactions: list[str] = []
    rules = ((EMAIL, "EMAIL"), (PHONE, "PHONE"), (ID_NUMBER, "ID_NUMBER"), (ORDER, "REFERENCE"))
    result = text
    for pattern, label in rules:
        result, count = pattern.subn(f"[{label}_REDACTED]", result)
        if count:
            redactions.append(label)
    return RedactionResult(result, tuple(redactions))


def privacy_passes(text: str) -> bool:
    return not redact_pii(text).redactions


def content_hash(text: str) -> str:
    normalized = " ".join(text.casefold().split())
    return hashlib.sha256(normalized.encode()).hexdigest()
