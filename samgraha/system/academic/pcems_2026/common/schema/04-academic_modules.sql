-- One row per module (code-discovered or metadata-declared).
-- discover-modules / discover-docs-modules write code-discovered modules
-- (role='primary'). commit-modules writes metadata.yaml-declared modules
-- (primary/dependent/cross_library). No more JSON blob -- all fields are
-- real columns.

CREATE TABLE IF NOT EXISTS academic_modules (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id                 INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    module_name              TEXT    NOT NULL,
    module_path              TEXT    NOT NULL DEFAULT '',
    role                     TEXT    NOT NULL DEFAULT 'primary' CHECK (role IN ('primary','dependent','cross_library')),
    interest_weight          REAL    NOT NULL DEFAULT 0.5,
    reason                   TEXT    NOT NULL DEFAULT '',
    existing_draft_publisher TEXT    NOT NULL DEFAULT '',
    existing_draft_status    TEXT    NOT NULL DEFAULT '',
    existing_draft_path      TEXT    NOT NULL DEFAULT '',
    sort_order               INTEGER NOT NULL DEFAULT 0,
    UNIQUE(paper_id, module_name)
);
