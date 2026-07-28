-- Decision workflow + content for each proposal. Replaces the old
-- academic_proposals table — anchored on the generic proposal table via
-- proposal_id FK. review_status replaces the old status column (renamed
-- to avoid collision with generic proposal.status).

CREATE TABLE IF NOT EXISTS academic_proposal_review (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id      INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    paper_id         INTEGER NOT NULL REFERENCES academic_papers(id),
    phase            TEXT    NOT NULL CHECK (phase IN ('generation','audit','fix','report')),
    scope_domain_id  INTEGER REFERENCES academic_domains(id),
    review_status    TEXT    NOT NULL DEFAULT 'pending'
                     CHECK (review_status IN ('pending','approved','rejected','superseded')),
    source           TEXT    NOT NULL DEFAULT '',
    user_comment     TEXT    NOT NULL DEFAULT '',
    iteration        INTEGER NOT NULL DEFAULT 0,
    is_latest        INTEGER NOT NULL DEFAULT 1,
    summary          TEXT    NOT NULL DEFAULT '',
    content_md       TEXT    NOT NULL DEFAULT '',
    computed_context TEXT,
    created_at       TEXT    NOT NULL DEFAULT (datetime('now')),
    decided_at       TEXT
);
CREATE INDEX IF NOT EXISTS idx_apr_lookup
    ON academic_proposal_review(paper_id, phase, scope_domain_id, is_latest);
CREATE INDEX IF NOT EXISTS idx_apr_proposal
    ON academic_proposal_review(proposal_id);
