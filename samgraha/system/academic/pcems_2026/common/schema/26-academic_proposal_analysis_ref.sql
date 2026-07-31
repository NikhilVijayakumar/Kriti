-- Generation-phase only: links a proposal to the cross_module_analysis
-- rows it grounded in (novelty/gaps/mathematics/architecture), instead
-- of copying analysis text into a JSON blob.

CREATE TABLE IF NOT EXISTS academic_proposal_analysis_ref (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id              INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    cross_module_analysis_id INTEGER NOT NULL REFERENCES academic_cross_module_analysis(id),
    UNIQUE(proposal_id, cross_module_analysis_id)
);
CREATE INDEX IF NOT EXISTS idx_par_proposal
    ON academic_proposal_analysis_ref(proposal_id);
