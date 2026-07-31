-- Per-run strengths / weaknesses / recommendations.
-- FK to academic_semantic_runs with ON DELETE CASCADE.
-- finding_type is constrained to the three kinds the rubric prompts produce.
-- sort_order preserves the order the semantic step returned.

CREATE TABLE IF NOT EXISTS academic_semantic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES academic_semantic_runs(id) ON DELETE CASCADE,
    finding_type  TEXT    NOT NULL CHECK (finding_type IN ('strength','weakness','recommendation')),
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);
