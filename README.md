# Revibe Consumer Awareness Bot

Evidence-first consumer information monitoring and responsible social-media publishing platform.

## Status

Initial production architecture scaffold. Publishing defaults to `PAUSED` until credentials, source adapters, privacy controls, and human-review policy are configured.

## Principles

- Public evidence only.
- Attribute allegations to their source.
- Never invent claims, statistics, dates, URLs, reviews, or responses.
- Minimize and redact personal information.
- Respect source terms, robots.txt, authentication boundaries, CAPTCHAs, and rate limits.
- Never evade platform enforcement or manipulate engagement.
- Maintain an auditable link from every published post to supporting evidence.

## Architecture

`collect -> normalize -> deduplicate -> privacy -> extract -> classify -> evidence -> analyze -> generate -> fact-check -> moderate -> publish`

See `docs/ARCHITECTURE.md` for the detailed design.

## Publishing modes

- `SAFE`: only low-risk informational content can be automatically published.
- `REVIEW`: candidate posts require human approval.
- `PAUSED`: publishing is disabled.

The default is `PAUSED`.

## Development

Python 3.12+, PostgreSQL 16+, Docker, and GitHub Actions are supported. Copy `.env.example` to `.env` for local development. Never commit credentials.

## License

Apache-2.0
