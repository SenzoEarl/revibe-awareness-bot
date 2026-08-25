from datetime import datetime, timezone

from revibe_bot.analysis.patterns import summarize
from revibe_bot.domain import ComplaintCategory, NormalizedReview


def review(i: int, source: str) -> NormalizedReview:
    return NormalizedReview(
        source=source,
        source_url=f"https://example.test/review/{i}",
        published_at=datetime(2026, 8, i, tzinfo=timezone.utc),
        text="A public review",
        content_hash=f"hash-{i}",
    )


def test_pattern_requires_multiple_reviews() -> None:
    reviews = [review(1, "a"), review(2, "a"), review(3, "b")]
    categories = {r.content_hash: ComplaintCategory.REFUND for r in reviews}
    result = summarize(reviews, categories, period_start=datetime(2026, 8, 1).date(), period_end=datetime(2026, 8, 31).date())
    assert result[0].review_count == 3
    assert result[0].independent_source_count == 2


def test_single_review_is_not_a_pattern() -> None:
    r = review(1, "a")
    result = summarize([r], {r.content_hash: ComplaintCategory.REFUND}, period_start=datetime(2026, 8, 1).date(), period_end=datetime(2026, 8, 31).date())
    assert result == []
