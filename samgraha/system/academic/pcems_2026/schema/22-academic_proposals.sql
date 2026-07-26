-- One row per proposal draft/decision. A phase's *latest* row for a given
-- (paper, phase, scope_domain) is authoritative — same is_latest pattern
-- as academic_report_history (schema/18).
--
-- status lifecycle: pending -> approved | rejected (terminal, human-
-- decided, immutable once set — is_latest flipping to 0 later does NOT
-- change a decided row's status, it stays true history). A *pending* row
-- that gets superseded by a redraft *before* anyone decided it (stale
-- context, new commit) flips to status='superseded' instead — the one
-- case persist_proposal.py is allowed to rewrite status on an old row
-- (§7b). rejected != superseded: rejected means a human said no;
-- superseded means nobody ever got the chance to decide before the
-- draft went stale.

CREATE TABLE IF NOT EXISTS academic_proposals (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    phase           TEXT    NOT NULL CHECK (phase IN ('generation','audit','report','fix')),
    scope_domain_id INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    -- NULL = whole-paper scope (generation/audit/report, and most fix
    -- proposals). Set only when a fix proposal targets one named domain.
    source          TEXT    NOT NULL CHECK (source IN ('pipeline','user-request')),
    status          TEXT    NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending','approved','rejected','superseded')),
    commit_sha      TEXT    NOT NULL DEFAULT '',
    -- same mechanism as academic_deterministic_findings.commit_sha.
    iteration       INTEGER NOT NULL DEFAULT 0,
    -- redraft count for this (paper, phase, scope_domain) — mirrors
    -- fix_loop.max_iterations (loop.yaml), reused as the same ceiling
    -- for repeated rejection (§6b).
    summary         TEXT    NOT NULL DEFAULT '',
    content_md      TEXT    NOT NULL,
    user_comment    TEXT    NOT NULL DEFAULT '',
    -- raw text driving a user-request fix proposal, OR a rejection
    -- reason on a decided row (§6b) — same column, different moment.
    metadata        TEXT,
    -- JSON blob of computed context from gather_proposal_context.py
    -- (domains, triggering_findings, score counts, etc.) — rendered
    -- into template computed-field sections by render_proposal.py.
    is_latest       INTEGER NOT NULL DEFAULT 1,
    created_at      TEXT    NOT NULL,
    decided_at      TEXT
);
CREATE INDEX IF NOT EXISTS idx_academic_proposals_lookup
    ON academic_proposals(paper_id, phase, scope_domain_id, is_latest);
