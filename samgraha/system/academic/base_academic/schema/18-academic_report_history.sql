-- One row per assemble-final-document.py run.
-- Tracks report generation history with is_latest flag.
-- Every new run sets prior is_latest=1 rows (same paper+format) to 0,
-- then inserts the new row with is_latest=1.
-- Because all data lives in the DB, regenerating any past report is just
-- re-running assemble-final-document.py against the same paper_id.

CREATE TABLE IF NOT EXISTS academic_report_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html','pdf','docx')),
    final_score   REAL,
    score_band    TEXT,
    file_path     TEXT    NOT NULL,
    is_latest     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_report_history_lookup
    ON academic_report_history(paper_id, format, is_latest);
