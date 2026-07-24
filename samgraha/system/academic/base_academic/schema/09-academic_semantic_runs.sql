-- One row per (paper, domain?, scope, model, run_number) semantic evaluation.
-- Append-only: each audit pass inserts a new row with run_number incremented.
-- This preserves score history — callers that want "the latest score" query
-- MAX(run_number) or ORDER BY run_number DESC LIMIT 1.
--
-- scope distinguishes three kinds of run:
--   'section'       — per-domain audit (domain_id NOT NULL)
--   'cross-section' — consistency review across all sections (domain_id NULL)
--   'document'      — whole-document holistic review (domain_id NULL)
--
-- UNIQUE constraint includes scope so section/cross-section/document runs
-- coexist for the same paper+model+run_number.

CREATE TABLE IF NOT EXISTS academic_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    scope         TEXT    NOT NULL DEFAULT 'section'
                  CHECK (scope IN ('section','cross-section','document')),
    model         TEXT    NOT NULL,
    run_number    INTEGER NOT NULL DEFAULT 1,
    overall_score REAL    NOT NULL,
    reasoning     TEXT    NOT NULL DEFAULT '',
    computed_against TEXT NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, scope, model, run_number)
);
