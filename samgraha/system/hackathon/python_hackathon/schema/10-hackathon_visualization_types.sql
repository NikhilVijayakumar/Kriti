-- knowledge.db — catalog of every chart kind common/render_charts.py can
-- produce, and its scope. Seeded once by init_schema.py's
-- seed_visualization_types() from the real chart_*() functions in that
-- file (not guessed) — answers "what visualizations are available, and are
-- they per-domain, per-team, or global" directly from the DB.
--
-- scope meanings (see render_charts.py's generate_charts() dispatch):
--   per_team_domain — one chart per (team, domain): field_distribution,
--                     det_sem_contribution, rule_pass_rate, model_spread
--   per_domain      — one chart per domain, shared across all teams: rank_distribution
--   per_team        — one chart per team, across all domains: team_radar
--   global          — one chart, once: domain_weights

CREATE TABLE IF NOT EXISTS hackathon_visualization_types (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key     TEXT    NOT NULL UNIQUE,
    scope         TEXT    NOT NULL CHECK (scope IN ('per_team_domain','per_domain','per_team','global')),
    description   TEXT    NOT NULL DEFAULT ''
);
