-- Per-dimension score + evidence for a dev_semantic_runs row. Mirrors
-- pcems's academic_semantic_dimension_scores (proposal 6 §7).

CREATE TABLE IF NOT EXISTS dev_semantic_dimension_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES dev_semantic_runs(id) ON DELETE CASCADE,
    dimension_key TEXT    NOT NULL,
    score         REAL    NOT NULL,
    evidence      TEXT
);
