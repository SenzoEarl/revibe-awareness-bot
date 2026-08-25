"""Conservative descriptive pattern analysis.

Patterns are summaries of source records, not findings of misconduct.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date

from revibe_bot.domain import ComplaintCategory, NormalizedReview, PatternSummary


def summarize(
    reviews: list[NormalizedReview],
    categories: dict[str, ComplaintCategory],
    *,
    period_start: date,
    period_end: date,
    minimum_reviews: int = 3,
) -> list[PatternSummary]:
    eligible = [
        r for r in reviews
        if r.published_at and period_start <= r.published_at.date() <= period_end
    ]
    if not eligible:
        return []

    grouped: dict[ComplaintCategory, list[NormalizedReview]] = defaultdict(list)
    for review in eligible:
        category = categories.get(review.content_hash)
        if category:
            grouped[category].append(review)

    summaries: list[PatternSummary] = []
    for category, members in grouped.items():
        if len(members) < minimum_reviews:
            continue
        sources = {member.source for member in members}
        response_count = sum(bool(member.company_response) for member in members)
        independent = len(sources)
        # Conservative descriptive confidence: source diversity and volume help,
        # but this never represents proof of systemic misconduct.
        confidence = min(1.0, 0.4 + min(len(members), 10) * 0.04 + min(independent, 5) * 0.04)
        summaries.append(
            PatternSummary(
                category=category,
                period_start=period_start,
                period_end=period_end,
                review_count=len(members),
                independent_source_count=independent,
                percentage_of_reviews=round(len(members) / len(eligible) * 100, 2),
                confidence=round(confidence, 3),
                company_response_count=response_count,
            )
        )
    return sorted(summaries, key=lambda item: (-item.review_count, item.category.value))
