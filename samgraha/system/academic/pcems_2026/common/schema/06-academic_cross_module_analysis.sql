-- Per (paper, analysis_kind) cross-module section content.
-- persist-cross-module-analysis writes one row per kind; docs-first
-- ingestion (load_docs_cross_module_analysis.py) also writes here from
-- docs/paper/{system}/cross_module/*.md files.
-- analysis_kind FK-references the analysis_kind lookup table (04a) —
-- adding a new kind is a data insert there, not a schema edit here.
-- The CHECK-constraint version of this table was missing figures/tables
-- after Proposal 15 added them — exactly the failure mode this lookup
-- table exists to prevent from recurring.

CREATE TABLE IF NOT EXISTS academic_cross_module_analysis (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    analysis_kind   TEXT    NOT NULL REFERENCES analysis_kind(key),
    content         TEXT    NOT NULL DEFAULT '',
    relevance_note  TEXT    NOT NULL DEFAULT '',
    model           TEXT    NOT NULL DEFAULT '',
    file_path       TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, analysis_kind)
);
