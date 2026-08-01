-- Per-run strengths/weaknesses/recommendations for a dev_semantic_runs
-- row. Mirrors pcems's academic_semantic_findings (proposal 6 §7).

CREATE TABLE IF NOT EXISTS dev_semantic_findings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       INTEGER NOT NULL REFERENCES dev_semantic_runs(id) ON DELETE CASCADE,
    finding_type TEXT    NOT NULL CHECK (finding_type IN ('strength','weakness','recommendation')),
    text         TEXT    NOT NULL
);
