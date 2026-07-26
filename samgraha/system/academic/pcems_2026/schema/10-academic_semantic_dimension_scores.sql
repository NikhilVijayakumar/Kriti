-- Per-dimension score + evidence for a semantic run.
-- FK to academic_semantic_runs with ON DELETE CASCADE — deleting a run
-- deletes its dimension scores.  No separate history concern: each run_id
-- is unique (append-only semantic_runs), so there's never a stale row to
-- clear at insert time.

CREATE TABLE IF NOT EXISTS academic_semantic_dimension_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES academic_semantic_runs(id) ON DELETE CASCADE,
    dimension_key TEXT    NOT NULL,
    score         REAL    NOT NULL,
    evidence      TEXT    NOT NULL DEFAULT '',
    UNIQUE(run_id, dimension_key)
);
