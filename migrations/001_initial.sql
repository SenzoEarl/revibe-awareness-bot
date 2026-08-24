CREATE TABLE sources (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    base_url TEXT NOT NULL,
    adapter TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    policy_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE reviews (
    id UUID PRIMARY KEY,
    source_id UUID NOT NULL REFERENCES sources(id),
    external_id TEXT,
    source_url TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL,
    rating NUMERIC(3,1),
    original_text TEXT NOT NULL,
    redacted_text TEXT NOT NULL,
    content_hash CHAR(64) NOT NULL,
    duplicate_of UUID REFERENCES reviews(id),
    evidence_status TEXT NOT NULL DEFAULT 'unverified',
    processing_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(source_id, external_id)
);

CREATE TABLE complaint_categories (
    id SMALLSERIAL PRIMARY KEY,
    slug TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL
);

CREATE TABLE claims (
    id UUID PRIMARY KEY,
    review_id UUID REFERENCES reviews(id),
    statement TEXT NOT NULL,
    attribution TEXT NOT NULL,
    category_id SMALLINT REFERENCES complaint_categories(id),
    confidence NUMERIC(4,3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    evidence_status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE company_responses (
    id UUID PRIMARY KEY,
    review_id UUID NOT NULL REFERENCES reviews(id),
    response_text TEXT NOT NULL,
    response_url TEXT,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE generated_posts (
    id UUID PRIMARY KEY,
    body TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_score NUMERIC(4,3),
    requires_human_review BOOLEAN NOT NULL DEFAULT TRUE,
    generated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE post_evidence (
    post_id UUID NOT NULL REFERENCES generated_posts(id) ON DELETE CASCADE,
    claim_id UUID NOT NULL REFERENCES claims(id),
    PRIMARY KEY(post_id, claim_id)
);

CREATE TABLE moderation_queue (
    post_id UUID PRIMARY KEY REFERENCES generated_posts(id),
    decision TEXT NOT NULL DEFAULT 'pending',
    reviewer TEXT,
    reason TEXT,
    decided_at TIMESTAMPTZ
);

CREATE TABLE published_posts (
    id UUID PRIMARY KEY,
    post_id UUID NOT NULL UNIQUE REFERENCES generated_posts(id),
    platform TEXT NOT NULL,
    platform_post_id TEXT NOT NULL,
    published_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    action TEXT NOT NULL,
    actor TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX reviews_published_at_idx ON reviews(published_at);
CREATE INDEX claims_category_idx ON claims(category_id);
CREATE INDEX audit_entity_idx ON audit_logs(entity_type, entity_id);
