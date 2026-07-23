-- knowledge.db — hackathon_semantic_domain_means: AVG(overall_score) per
-- (team, domain) across every model in hackathon_semantic_runs. This is
-- "semantic mean calculated per domain based on model" as a live SQL
-- aggregate over what's already stored — never recomputed by calling an
-- LLM again. A VIEW, not a table: always in sync with hackathon_semantic_runs
-- with no separate write path to keep consistent, and nothing for
-- custom_data_tables to catalog since it owns no data of its own.

CREATE VIEW IF NOT EXISTS hackathon_semantic_domain_means AS
    SELECT standard, team_id, domain_id,
           AVG(overall_score) AS semantic_mean,
           COUNT(*) AS model_count
    FROM hackathon_semantic_runs
    GROUP BY standard, team_id, domain_id;
