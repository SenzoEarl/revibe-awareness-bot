from revibe_bot.classification import classify
from revibe_bot.domain import ComplaintCategory
from revibe_bot.privacy import content_hash, redact_pii, privacy_passes


def test_redacts_contact_and_reference_data() -> None:
    result = redact_pii("Email me at test@example.com, order REF-12345, phone 082 123 4567")
    assert "test@example.com" not in result.text
    assert "REF-12345" not in result.text
    assert "082 123 4567" not in result.text
    assert {"EMAIL", "REFERENCE", "PHONE"}.issubset(result.redactions)
    assert not privacy_passes("Call 082 123 4567")


def test_content_hash_normalizes_whitespace_and_case() -> None:
    assert content_hash("Refund  please") == content_hash(" refund please ")


def test_refund_classification() -> None:
    category, confidence = classify("The refund has not arrived and I want my money back")
    assert category is ComplaintCategory.REFUND
    assert confidence >= 0.5


def test_unknown_classification_is_low_confidence() -> None:
    category, confidence = classify("The weather is sunny today")
    assert category is ComplaintCategory.OTHER
    assert confidence < 0.5
