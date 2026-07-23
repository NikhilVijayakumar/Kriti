-- Views for common query patterns.
-- Mirrors python_hackathon's 12-views.sql convention.

-- Latest semantic score per (paper, domain, model)
CREATE VIEW IF NOT EXISTS academic_v_latest_semantic_run AS
SELECT s.*
FROM academic_semantic_runs s
INNER JOIN (
    SELECT paper_id, domain_id, model, MAX(run_number) AS max_run
    FROM academic_semantic_runs
    GROUP BY paper_id, domain_id, model
) latest ON s.paper_id = latest.paper_id
        AND s.domain_id = latest.domain_id
        AND s.model = latest.model
        AND s.run_number = latest.max_run;

-- Per-domain mean score across models (latest run per model)
CREATE VIEW IF NOT EXISTS academic_v_domain_means AS
SELECT
    s.paper_id,
    s.domain_id,
    d.key AS domain_key,
    AVG(s.overall_score) AS mean_score,
    MIN(s.overall_score) AS min_score,
    MAX(s.overall_score) AS max_score,
    COUNT(DISTINCT s.model) AS model_count
FROM academic_v_latest_semantic_run s
JOIN academic_domains d ON d.id = s.domain_id
GROUP BY s.paper_id, s.domain_id;

-- Whole-paper final score (mean of domain means, weighted if weights differ)
CREATE VIEW IF NOT EXISTS academic_v_paper_scores AS
SELECT
    dm.paper_id,
    SUM(dm.mean_score * COALESCE(d.weight, 1.0)) / SUM(COALESCE(d.weight, 1.0)) AS final_score
FROM academic_v_domain_means dm
JOIN academic_domains d ON d.id = dm.domain_id
GROUP BY dm.paper_id;

-- Latest report per (paper, format)
CREATE VIEW IF NOT EXISTS academic_v_latest_report AS
SELECT r.*
FROM academic_report_history r
INNER JOIN (
    SELECT paper_id, format, MAX(id) AS max_id
    FROM academic_report_history
    WHERE is_latest = 1
    GROUP BY paper_id, format
) latest ON r.id = latest.max_id;
