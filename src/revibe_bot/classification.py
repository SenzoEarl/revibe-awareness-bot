"""Deterministic first-pass complaint classifier.

LLM classification can be added later, but it must remain advisory and retain
its confidence and original evidence. This baseline makes the pipeline useful
without requiring an AI provider.
"""

from __future__ import annotations

import re

from revibe_bot.domain import ComplaintCategory

_RULES: tuple[tuple[ComplaintCategory, tuple[str, ...]], ...] = (
    (ComplaintCategory.REFUND, ("refund", "money back", "reimburse")),
    (ComplaintCategory.DEVICE_CONDITION, ("scratched", "condition", "dent", "grade")),
    (ComplaintCategory.DEVICE_FUNCTIONALITY, ("not working", "doesn't work", "battery", "broken")),
    (ComplaintCategory.WARRANTY, ("warranty", "guarantee")),
    (ComplaintCategory.DELIVERY, ("delivery", "courier", "shipping", "delivered")),
    (ComplaintCategory.CANCELLATION, ("cancel", "cancellation")),
    (ComplaintCategory.CUSTOMER_SERVICE, ("customer service", "support", "agent")),
    (ComplaintCategory.COMMUNICATION, ("no response", "respond", "communication", "email")),
    (ComplaintCategory.PRICING, ("price", "pricing", "charged", "cost")),
    (ComplaintCategory.TRADE_IN, ("trade-in", "trade in", "tradein")),
    (ComplaintCategory.REPLACEMENT, ("replacement", "replace")),
    (ComplaintCategory.REPAIR, ("repair", "fixed")),
    (ComplaintCategory.TERMS, ("terms", "conditions", "policy")),
    (ComplaintCategory.ACCOUNT, ("account", "login", "password")),
)


def classify(text: str) -> tuple[ComplaintCategory, float]:
    normalized = re.sub(r"\s+", " ", text.casefold())
    matches = [(category, sum(term in normalized for term in terms)) for category, terms in _RULES]
    category, score = max(matches, key=lambda item: item[1], default=(ComplaintCategory.OTHER, 0))
    if score == 0:
        return ComplaintCategory.OTHER, 0.2
    return category, min(0.5 + score * 0.15, 0.95)
