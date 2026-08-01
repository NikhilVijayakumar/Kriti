-- One row per (repo_root, domain, scope, model, run) semantic evaluation,
-- written by persist-semantic-score (proposal 3 §3). Mirrors pcems's
-- academic_semantic_runs (proposal 6 §7).

CREATE TABLE IF NOT EXISTS dev_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    domain_id     INTEGER NOT NULL REFERENCES domain(id),
    tier_number   INTEGER NOT NULL,
    scope         TEXT    NOT NULL CHECK (scope IN ('document','section')),
    model         TEXT    NOT NULL,
    run_number    INTEGER NOT NULL,
    overall_score REAL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_id, scope, run_number)
);
