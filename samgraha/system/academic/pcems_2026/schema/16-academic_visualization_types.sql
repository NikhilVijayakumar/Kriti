-- Catalog of chart types that render_charts.py can produce.
-- Seeded on init-schema; chart_key is the machine-readable identifier
-- used by render_charts.py to decide which data to pull.
-- scope controls whether the chart is per_domain, per_paper, or global.

CREATE TABLE IF NOT EXISTS academic_visualization_types (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key     TEXT    NOT NULL UNIQUE,
    scope         TEXT    NOT NULL CHECK (scope IN ('per_domain','per_paper','global')),
    description   TEXT    NOT NULL DEFAULT ''
);
