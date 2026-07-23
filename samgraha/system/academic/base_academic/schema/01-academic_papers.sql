-- One row per registered paper (repo + system).
-- A "paper" here is a concrete system's paper-generation target: one repo +
-- one standard name = one paper row.  Multiple concrete systems targeting
-- the same repo (unlikely but allowed) get separate rows.
-- title/paper_type/status are metadata — the actual content lives in
-- academic_narratives, not here.

CREATE TABLE IF NOT EXISTS academic_papers (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    repo_root     TEXT    NOT NULL,
    title         TEXT    NOT NULL DEFAULT '',
    paper_type    TEXT    NOT NULL DEFAULT 'paper',
    status        TEXT    NOT NULL DEFAULT 'draft',
    metadata      TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL,
    UNIQUE(standard, repo_root)
);
