-- knowledge.db — lookup table: the 10 scoring domains, seeded once by
-- init_schema.py's seed_domains() from weights.yaml (key/display_name/
-- sort_order/weight) joined with each domain's real deterministic/semantic
-- split from calculation/aggregation/domain/*.yaml (det_weight/sem_weight).
-- Every other hackathon_* table references this by domain_id instead of a
-- freetext domain string — gives relational integrity + a single place to
-- look up a domain's weight instead of re-reading weights.yaml everywhere.

CREATE TABLE IF NOT EXISTS hackathon_domains (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    key           TEXT    NOT NULL UNIQUE,   -- 'infrastructure', matches DOMAIN_AUDIT_MODULES keys
    display_name  TEXT    NOT NULL,          -- 'Infrastructure'
    sort_order    INTEGER NOT NULL,          -- 0-based; +1 zero-padded = the '01-' filename prefix
    weight        REAL    NOT NULL DEFAULT 0,     -- out of the 100-point base_total (weights.yaml)
    det_weight    REAL    NOT NULL DEFAULT 0.60,  -- this domain's deterministic share of its own 100
    sem_weight    REAL    NOT NULL DEFAULT 0.40   -- this domain's semantic share of its own 100
);
