-- Per (paper, domain, run_number): deterministic audit verdict + per-check findings.
-- Append-only, same pattern as academic_semantic_runs / academic_plagiarism_findings.
-- findings is a JSON array of {check_id, rule, passed, detail} objects
-- matching the check structure in calculation/deterministic/{domain}.yaml.

CREATE TABLE IF NOT EXISTS academic_deterministic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    run_number    INTEGER NOT NULL DEFAULT 1,
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    findings      TEXT    NOT NULL DEFAULT '[]',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, run_number)
);
