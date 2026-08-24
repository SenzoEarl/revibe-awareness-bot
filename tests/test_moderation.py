from revibe_bot.models import CandidatePost, PublishingMode
from revibe_bot.moderation import review_post

def test_paused_never_publishes():
    post = CandidatePost(text="consumer education", requires_human_review=False)
    decision = review_post(post, PublishingMode.PAUSED)
    assert not decision.allowed

def test_blocked_flag_never_publishes():
    post = CandidatePost(text="x", risk_flags=["harassment"], requires_human_review=False)
    decision = review_post(post, PublishingMode.SAFE)
    assert not decision.allowed
