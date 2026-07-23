-- Per (paper, domain, iteration): change summary + risk flags.
-- iteration increments per humanize pass (usecase 5b).
-- change_summary is a human-readable description of what changed.
-- risk_flags is JSON array of claims that needed weakening or verification.

CREATE TABLE IF NOT EXISTS academic_humanize_passes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    iteration     INTEGER NOT NULL DEFAULT 0,
    change_summary TEXT   NOT NULL DEFAULT '',
    risk_flags    TEXT    NOT NULL DEFAULT '[]',
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, iteration)
);
