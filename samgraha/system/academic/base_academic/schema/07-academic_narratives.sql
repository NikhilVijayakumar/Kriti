-- One row per (paper, domain) — stores section drafts with stage tracking
-- and iteration history.  stage progresses generate → humanize (no separate
-- deepen stage — enrichment passes are folded into the generation step).
-- iteration increments within each stage.  The orchestrator always reads
-- the most-processed version (latest stage, then latest iteration).
-- validated=1 means the narrative has passed both deterministic and semantic audit.

CREATE TABLE IF NOT EXISTS academic_narratives (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    stage         TEXT    NOT NULL DEFAULT 'generate' CHECK (stage IN ('generate','humanize')),
    iteration     INTEGER NOT NULL DEFAULT 0,
    validated     INTEGER NOT NULL DEFAULT 0,
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, stage, iteration)
);
CREATE INDEX IF NOT EXISTS idx_academic_narratives_lookup
    ON academic_narratives(standard, paper_id, domain_id);
