-- knowledge.db — one row per (team, domain) narrative-generation run, from
-- usecase 4's analysis/*.md prompts. team_id and domain_id are BOTH
-- nullable — NULL/NULL is the competition-wide leaderboard narrative
-- (analysis/00-leaderboard.md), a real case the old semantic_reports.domain
-- NOT NULL constraint could never store. `model` answers "which model wrote
-- this narrative" — same reasoning as hackathon_semantic_runs.model.
--
-- No UNIQUE constraint here: SQLite treats every NULL as distinct, so
-- UNIQUE(team_id, domain_id) wouldn't actually stop duplicate NULL/NULL
-- rows. Dedup is handled at the application level instead — see
-- common/hackathon_schema.py's upsert_narrative(), which does an explicit
-- `team_id IS ? AND domain_id IS ?` lookup before deciding insert vs update.

CREATE TABLE IF NOT EXISTS hackathon_narratives (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_hackathon_narratives_lookup
    ON hackathon_narratives(standard, team_id, domain_id);
