-- knowledge.db — one row per (semantic run, evaluation dimension). This is
-- the "separate table to save evidence" per model/domain: each
-- audit/semantic/document/*.prompt.md asks the agent to return a
-- dimension_scores object (e.g. environment_setup, dependency_management,
-- ... — see each prompt's "## Evaluation Dimensions" / "## Expected
-- Output"); rather than keep that nested inside one JSON blob, each
-- dimension becomes its own row, joined to the run it belongs to. Lets a
-- query like "which teams scored low on offline_execution across every
-- domain" run directly in SQL.

CREATE TABLE IF NOT EXISTS hackathon_semantic_dimension_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES hackathon_semantic_runs(id) ON DELETE CASCADE,
    dimension_key TEXT    NOT NULL,   -- e.g. 'environment_setup', from evaluation_dimensions
    score         REAL    NOT NULL,
    evidence      TEXT    NOT NULL DEFAULT '',  -- the agent's own evidence string for this dimension
    UNIQUE(run_id, dimension_key)
);
