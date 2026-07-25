-- knowledge.db — catalog of every report template actually on disk under
-- templates/reports/{markdown,html}/. Seeded once by init_schema.py's
-- seed_templates() by walking the real filesystem (not guessed) —
-- templates/reports/{markdown,html}/domain/{NN-domain}/{deterministic,
-- semantic,summary}.{md,html} (10 domains x 3 report_types x 2 formats) and
-- the two global ones, global-leaderboard.{md,html} and
-- team-final-summary.{md,html} (domain_id NULL for those). Answers "what
-- report templates are available, markdown and html, per domain" directly
-- from the DB instead of walking the filesystem every time a report step
-- runs.

CREATE TABLE IF NOT EXISTS hackathon_templates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html')),
    report_type   TEXT    NOT NULL CHECK (report_type IN ('deterministic','semantic','summary','leaderboard','team-final-summary')),
    domain_id     INTEGER REFERENCES hackathon_domains(id) ON DELETE CASCADE,  -- NULL for leaderboard/team-final-summary
    file_path     TEXT    NOT NULL,
    UNIQUE(format, report_type, domain_id)
);
