-- Per (repo_root, domain, scope, run): deterministic audit verdict +
-- findings, written by persist-deterministic-findings (proposal 3 §3).
-- Mirrors pcems's academic_deterministic_findings, keyed on repo_root
-- instead of paper_id (proposal 6 §7).

CREATE TABLE IF NOT EXISTS dev_deterministic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    domain_id     INTEGER NOT NULL REFERENCES domain(id),
    tier_number   INTEGER NOT NULL,
    scope         TEXT    NOT NULL CHECK (scope IN ('document','section')),
    run_number    INTEGER NOT NULL,
    verdict       TEXT    NOT NULL,
    findings_json TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_id, scope, run_number)
);
