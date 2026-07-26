-- One row per calculate.py run, independent of any single domain.
-- Tracks the whole-paper trend over time — this is what the score-over-time
-- visualization queries, not a live re-scoring.
-- domain_id IS NULL means whole-paper final_score; non-NULL means per-domain.
-- Append-only: never updated, same "backtrace, never regenerate silently"
-- principle as academic_visualizations.
-- trend_delta is vs previous snapshot for this (paper, domain) pair.

CREATE TABLE IF NOT EXISTS academic_score_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    final_score   REAL    NOT NULL,
    score_band    TEXT    NOT NULL,
    trend_delta   REAL,
    calculated_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_score_history_lookup
    ON academic_score_history(paper_id, domain_id, calculated_at);
