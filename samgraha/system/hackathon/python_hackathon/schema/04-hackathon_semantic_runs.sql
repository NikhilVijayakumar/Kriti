-- knowledge.db — one row per (team, domain, model) semantic evaluation.
-- audit/semantic/document/*.yaml declares an `ensemble.required_models`
-- list (e.g. claude-3-5-sonnet, gemini-1.5-pro, gpt-4o) — several models
-- independently score the same (team, domain), and hackathon_domain_scores
-- (see 05/06 below) breaks each run's dimension scores and findings out
-- into their own rows instead of one JSON blob, so they're queryable and
-- backtraceable without re-running the LLM. `model` is what answers "which
-- model produced this analysis". The per-domain mean across models is the
-- hackathon_semantic_domain_means VIEW (12-views.sql) — a live aggregate
-- over this table, never recomputed by calling a model again.
-- Written by usecase 2b's post-script, persist_domain_semantic_score.py,
-- via hackathon_schema.upsert_domain_score(kind='semantic').

CREATE TABLE IF NOT EXISTS hackathon_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER NOT NULL REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    model         TEXT    NOT NULL,
    overall_score REAL    NOT NULL,
    reasoning     TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(team_id, domain_id, model)
);
