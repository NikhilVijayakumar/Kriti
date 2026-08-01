-- Durable link from a proposal row to the real domain/usecase/step ids it
-- was drafted against (proposal 6 §6). proposal.usecase_id is a singular
-- FK and doesn't fit a propose-tierN-* usecase spanning every domain in a
-- tier, and phases[] in the validated proposal envelope is discarded after
-- insert-time validation — this table keeps the link durable instead.

CREATE TABLE IF NOT EXISTS dev_proposal_phase_scope (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id  INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    domain_id    INTEGER NOT NULL REFERENCES domain(id),
    usecase_id   INTEGER NOT NULL REFERENCES usecase(id),
    step_id      INTEGER REFERENCES step(id)
);
