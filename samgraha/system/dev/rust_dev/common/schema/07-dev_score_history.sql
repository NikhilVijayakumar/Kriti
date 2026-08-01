-- One row per calculate run (repo_root, domain, final_score, score_band)
-- — trend tracking. Written by the calculate usecase (proposal 3 §3).
-- Mirrors pcems's academic_score_history (proposal 6 §7).

CREATE TABLE IF NOT EXISTS dev_score_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    domain_id     INTEGER NOT NULL REFERENCES domain(id),
    final_score   REAL    NOT NULL,
    score_band    TEXT    NOT NULL,
    calculated_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
