-- One row per rendered chart image.
-- render_charts.py writes here after rendering; extract-mermaid-images.py
-- also writes here for mermaid-diagram entries.
-- content_hash dedupes re-rendering: if the same mermaid block is encountered
-- again, the existing image is reused instead of re-rendering.
-- file_path is relative to the repo root.

CREATE TABLE IF NOT EXISTS academic_visualizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_type_id INTEGER NOT NULL REFERENCES academic_visualization_types(id) ON DELETE CASCADE,
    paper_id      INTEGER REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    content_hash  TEXT,
    file_path     TEXT    NOT NULL,
    created_at    TEXT    NOT NULL
);
