# Architecture

## Pipeline

Source adapters collect only permitted public material. The normalizer creates a canonical `Review`; deduplication prevents repeated source records; the privacy layer redacts unnecessary PII before downstream processing. Claims are attributed and linked to reviews. Pattern analysis uses independent source counts and time windows. Post generation receives evidence records rather than unrestricted source text. Fact-checking and moderation run before publication.

## Evidence model

A claim can be `unverified`, `verified_public_source`, or `insufficient_evidence`. `INSUFFICIENT_EVIDENCE` is a terminal state for publication.

A pattern is descriptive: it reports that multiple public sources describe similar experiences. It does not establish systemic misconduct, illegality, fraud, or criminality.

## Source adapters

Implement each source behind a common interface with explicit source policy. Prefer official APIs. A collector must fail closed when a source disallows automated access, requires authentication/CAPTCHA, returns a rate-limit response, or otherwise signals that access should stop.

## Privacy

PII is redacted before LLM processing where practical. Raw source content should be retained only where necessary for evidence integrity and according to applicable retention policy. Public customer identities are not needed for posts.

## Publishing

The publisher accepts only an approved `CandidatePost` with evidence links and a successful safety decision. It uses an authorized X account and never rotates identities, proxies, locations, or accounts to evade enforcement.

## Human control

`PAUSED` is the emergency stop. `REVIEW` is the default operating mode for allegations and individual experiences. `SAFE` is restricted to low-risk educational/data content after deterministic gates pass.

## Auditability

Every generated and published post receives audit events recording the evidence IDs, checks performed, decision, actor, and publication ID. Evidence relationships are immutable from the application's perspective.
