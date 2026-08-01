-- One row per (repo_root, domain_key, scan) — propose-tierN-assess's
-- structural repo scan. Append-only (proposal 6 §7 Q3): "latest" is
-- ORDER BY scanned_at DESC LIMIT 1, matching academic_deterministic_
-- findings' run_number-keyed pattern, not an update-in-place row.

CREATE TABLE IF NOT EXISTS dev_repo_domain_state (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    domain_key    TEXT    NOT NULL,
    tier_number   INTEGER NOT NULL,
    doc_exists    INTEGER NOT NULL CHECK (doc_exists IN (0,1)),
    conforms      INTEGER,             -- NULL until assessed; 0/1 after
    gap_notes     TEXT,                -- what's missing/non-conforming, freeform
    scanned_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_key, scanned_at)
);
