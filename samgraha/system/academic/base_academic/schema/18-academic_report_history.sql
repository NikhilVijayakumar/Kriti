-- One row per render run (paper track or audit track).
-- Tracks report generation history with is_latest flag per track.
-- report_kind distinguishes paper renders from audit-report renders,
-- so both tracks can produce format='html' for the same paper without
-- collision. "Latest" is scoped per (paper, report_kind, format).
-- audit is split into three sub-reports (deterministic, semantic, summary)
-- so each can be independently tracked as is_latest.

CREATE TABLE IF NOT EXISTS academic_report_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    report_kind   TEXT    NOT NULL DEFAULT 'paper' CHECK (report_kind IN ('paper','audit-deterministic','audit-semantic','audit-summary')),
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html','pdf','docx')),
    final_score   REAL,
    score_band    TEXT,
    file_path     TEXT    NOT NULL,
    is_latest     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_report_history_lookup
    ON academic_report_history(paper_id, report_kind, format, is_latest);
