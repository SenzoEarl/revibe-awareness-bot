from difflib import SequenceMatcher
from .models import Review

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, " ".join(a.casefold().split()), " ".join(b.casefold().split())).ratio()

def is_duplicate(review: Review, existing: list[Review], threshold: float = 0.94) -> str | None:
    if review.external_id:
        for item in existing:
            if item.source == review.source and item.external_id == review.external_id:
                return item.content_hash or item.external_id
    for item in existing:
        if similarity(review.text, item.text) >= threshold:
            return item.content_hash or item.external_id
    return None
