-- One row per detected module in a repo.
-- discover-modules writes this; module boundaries are top-level packages.
-- Modules drive the generate-analysis-docs usecase's per-module triads.

CREATE TABLE IF NOT EXISTS academic_modules (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    module_name   TEXT    NOT NULL,
    module_path   TEXT    NOT NULL DEFAULT '',
    sort_order    INTEGER NOT NULL DEFAULT 0,
    metadata      TEXT    NOT NULL DEFAULT '{}',
    UNIQUE(paper_id, module_name)
);
