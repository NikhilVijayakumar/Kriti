-- Catalog of report/generation templates on disk.
-- seed_templates scans the templates/ directory and populates this table.
-- scope categorizes by what the template operates on: module-level,
-- cross-module, document-level, plagiarism audit, humanizer, or enrichment.

CREATE TABLE IF NOT EXISTS academic_templates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    template_kind TEXT    NOT NULL CHECK (template_kind IN ('generation','audit','enrichment','analysis')),
    scope         TEXT    NOT NULL CHECK (scope IN ('module','cross_module','document','plagiarism','humanizer','enrichment')),
    name          TEXT    NOT NULL,
    file_path     TEXT    NOT NULL,
    UNIQUE(template_kind, scope, name)
);
