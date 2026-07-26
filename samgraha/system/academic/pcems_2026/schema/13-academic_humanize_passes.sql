-- Per (paper, domain, iteration, pass_kind): change summary + risk flags.
-- iteration increments per humanize pass (usecase 5c/5d).
-- pass_kind distinguishes deterministic (NLP-lib mechanical fix) from
-- semantic (LLM rewrite) passes — both can run for the same domain+iteration.
-- change_summary is a human-readable description of what changed.
-- risk_flags is JSON array of claims that needed weakening or verification.

CREATE TABLE IF NOT EXISTS academic_humanize_passes (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    iteration     INTEGER NOT NULL DEFAULT 0,
    pass_kind     TEXT    NOT NULL DEFAULT 'semantic'
                  CHECK (pass_kind IN ('deterministic','semantic')),
    change_summary TEXT   NOT NULL DEFAULT '',
    risk_flags    TEXT    NOT NULL DEFAULT '[]',
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, iteration, pass_kind)
);
