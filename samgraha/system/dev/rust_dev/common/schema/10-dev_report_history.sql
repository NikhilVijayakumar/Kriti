-- One row per render-report run (repo_root, report_kind, file_path) —
-- markdown output, DB-backed so a later HTML/PDF/DOCX conversion step
-- doesn't need to re-derive anything (proposal 6 §7). Mirrors pcems's
-- academic_report_history.

CREATE TABLE IF NOT EXISTS dev_report_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root   TEXT    NOT NULL,
    report_kind TEXT    NOT NULL,
    file_path   TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
