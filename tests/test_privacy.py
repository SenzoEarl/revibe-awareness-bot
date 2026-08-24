from revibe_bot.privacy import redact_pii, content_hash

def test_redacts_email_and_phone():
    result = redact_pii("Email test@example.com or call 082 123 4567")
    assert "test@example.com" not in result.text
    assert "082 123 4567" not in result.text
    assert "EMAIL_REDACTED" in result.text
    assert "PHONE_REDACTED" in result.text

def test_hash_is_stable():
    assert content_hash("Hello   World") == content_hash(" hello world ")
