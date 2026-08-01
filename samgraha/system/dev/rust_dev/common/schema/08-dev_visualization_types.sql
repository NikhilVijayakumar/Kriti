-- Chart type catalog, written by render-charts (proposal 6 §7). Mirrors
-- pcems's academic_visualization_types.

CREATE TABLE IF NOT EXISTS dev_visualization_types (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT    NOT NULL UNIQUE,
    scope       TEXT    NOT NULL,
    description TEXT
);
