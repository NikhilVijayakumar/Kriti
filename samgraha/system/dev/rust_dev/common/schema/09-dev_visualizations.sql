-- One row per rendered chart image, written by render-charts (proposal 6
-- §7). Mirrors pcems's academic_visualizations.

CREATE TABLE IF NOT EXISTS dev_visualizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    chart_type_id INTEGER NOT NULL REFERENCES dev_visualization_types(id),
    file_path     TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);
