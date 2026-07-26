-- Per (paper, domain, run_number, pass_type, check_kind): PASS/FAIL + flagged spans.
-- Append-only like semantic_runs — run_number increments per audit pass.
-- pass_type distinguishes forensic audit (Pass 1) from targeted-rewrite
-- verification (Pass 2) in the 3-pass plagiarism flow.
-- check_kind distinguishes deterministic sub-checks (mechanical fingerprint
-- pre-screen) from semantic sub-checks (LLM judgment), so both land in the
-- same table without collision.
-- flagged_spans is JSON array of {text, start_line, end_line, pattern,
-- severity, suggestion} objects.

CREATE TABLE IF NOT EXISTS academic_plagiarism_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    run_number    INTEGER NOT NULL DEFAULT 1,
    pass_type     TEXT    NOT NULL DEFAULT 'forensic' CHECK (pass_type IN ('forensic','targeted-rewrite')),
    check_kind    TEXT    NOT NULL DEFAULT 'semantic' CHECK (check_kind IN ('deterministic','semantic')),
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    flagged_spans TEXT    NOT NULL DEFAULT '[]',
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, run_number, pass_type, check_kind)
);
