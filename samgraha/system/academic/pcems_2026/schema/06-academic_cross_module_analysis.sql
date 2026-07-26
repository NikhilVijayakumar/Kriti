-- Per (paper, analysis_kind) cross-module section content.
-- persist-cross-module-analysis writes one row per kind; docs-first
-- ingestion (load_docs_cross_module_analysis.py) also writes here from
-- docs/paper/{system}/cross_module/*.md files.
-- analysis_kind covers 8 kinds: architecture, dependencies, interactions,
-- patterns, gaps, mathematics, novelty (base_academic's original 7,
-- code-based cross-module analysis) + consistency_check (docs-first
-- ingestion's convention — e.g. Bodha's cross_module/consistency_check.md
-- has no code-based equivalent).

CREATE TABLE IF NOT EXISTS academic_cross_module_analysis (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    analysis_kind   TEXT    NOT NULL CHECK (analysis_kind IN ('architecture','dependencies','interactions','patterns','gaps','mathematics','novelty','consistency_check')),
    content         TEXT    NOT NULL DEFAULT '',
    model           TEXT    NOT NULL DEFAULT '',
    file_path       TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, analysis_kind)
);
