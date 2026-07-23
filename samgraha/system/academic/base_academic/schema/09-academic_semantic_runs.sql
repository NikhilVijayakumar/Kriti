-- One row per (paper, domain, model, run_number) semantic evaluation.
-- Append-only: each audit pass inserts a new row with run_number incremented.
-- This preserves score history — callers that want "the latest score" query
-- MAX(run_number) or ORDER BY run_number DESC LIMIT 1.
--
-- UNIQUE constraint includes run_number so multiple passes coexist.
-- run_number starts at 1 and increments per (paper, domain, model).

CREATE TABLE IF NOT EXISTS academic_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    model         TEXT    NOT NULL,
    run_number    INTEGER NOT NULL DEFAULT 1,
    overall_score REAL    NOT NULL,
    reasoning     TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, model, run_number)
);
