-- knowledge.db — one row per (team, domain) deterministic audit result.
-- Split out of the old single hackathon_domain_scores table so
-- deterministic and semantic scoring — genuinely different shapes (one
-- score vs N-per-model scores with dimensions/findings) — each get their
-- own properly-typed table instead of a shared `kind` discriminator column.
-- Written by common/det_audit.py's run_domain_audit() via
-- hackathon_schema.upsert_domain_score(kind='deterministic').

CREATE TABLE IF NOT EXISTS hackathon_deterministic_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER NOT NULL REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    score         REAL    NOT NULL,
    rules_passed  INTEGER,  -- NULL: not threaded through from evaluate_rules.py's result yet
    rules_total   INTEGER,
    evidence      TEXT    NOT NULL DEFAULT '{}',  -- raw audit_*.py stdout JSON, verbatim
    created_at    TEXT    NOT NULL,
    UNIQUE(team_id, domain_id)
);
