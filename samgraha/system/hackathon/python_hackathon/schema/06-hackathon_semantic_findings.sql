-- knowledge.db — one row per (semantic run, strength|weakness|
-- recommendation), from the same "## Expected Output" schema each
-- audit/semantic/document/*.prompt.md's agent result carries. Normalized
-- (not a JSON array column) so findings can be queried/counted per domain
-- or per model without parsing JSON — e.g. "how many recommendations did
-- gpt-4o raise for runtime across all teams".

CREATE TABLE IF NOT EXISTS hackathon_semantic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES hackathon_semantic_runs(id) ON DELETE CASCADE,
    finding_type  TEXT    NOT NULL CHECK (finding_type IN ('strength','weakness','recommendation')),
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);
