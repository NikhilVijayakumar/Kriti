-- knowledge.db — python_hackathon's own table: one row per registered team.
-- Replaces reuse of the archived doc-audit `documents` table (path=team_name,
-- metadata=JSON) with a table this standard owns outright. Created by
-- init_schema.py (../scripts/schema/init_schema.py), not by samgraha — see
-- README.md in this directory for why a standard's own tables can't be
-- Rust-migrated the way schema/knowledge/*.sql at the samgraha repo root is.

CREATE TABLE IF NOT EXISTS hackathon_teams (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_name     TEXT    NOT NULL,
    repo_path     TEXT    NOT NULL DEFAULT '',
    team_leader   TEXT    NOT NULL DEFAULT '',
    team_code     TEXT    NOT NULL DEFAULT '',
    repo_https    TEXT    NOT NULL DEFAULT '',
    repo_ssh      TEXT    NOT NULL DEFAULT '',
    members       TEXT    NOT NULL DEFAULT '[]',  -- JSON array of {name, employee_id}
    metadata      TEXT    NOT NULL DEFAULT '{}',  -- opaque extra fields from teams.json
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL,
    UNIQUE(standard, team_name)
);
