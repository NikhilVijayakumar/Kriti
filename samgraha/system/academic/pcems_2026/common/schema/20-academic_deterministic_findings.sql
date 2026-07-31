-- Per (paper, domain?, scope, run_number): deterministic audit verdict + per-check findings.
-- Append-only, same pattern as academic_semantic_runs / academic_plagiarism_findings.
-- findings is a JSON array of {check_id, rule, passed, detail} objects
-- matching the check structure in calculation/deterministic/{domain}.yaml.
-- domain_id is NULL for scope='document' (whole-paper deterministic checks).
--
-- commit_sha is the git HEAD this audit ran against. Pre-upgrade rows
-- backfill with '' (never matches a real SHA — no false skip-cache hits).

CREATE TABLE IF NOT EXISTS academic_deterministic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    scope         TEXT    NOT NULL DEFAULT 'section'
                  CHECK (scope IN ('section','document')),
    run_number    INTEGER NOT NULL DEFAULT 1,
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    findings      TEXT    NOT NULL DEFAULT '[]',
    commit_sha    TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, scope, run_number)
);
