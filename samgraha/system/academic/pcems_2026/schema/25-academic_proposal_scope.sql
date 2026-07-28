-- Durable usecase/step alignment for each proposal. One row per
-- (domain, usecase, step) the proposal's validated phases[] covered.
-- Joining step_id -> step.kind answers deterministic vs semantic count.

CREATE TABLE IF NOT EXISTS academic_proposal_scope (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id  INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    domain_id    INTEGER NOT NULL REFERENCES domain(id),
    usecase_id   INTEGER NOT NULL REFERENCES usecase(id),
    step_id      INTEGER NOT NULL REFERENCES step(id),
    UNIQUE(proposal_id, step_id)
);
CREATE INDEX IF NOT EXISTS idx_aps_proposal
    ON academic_proposal_scope(proposal_id);
