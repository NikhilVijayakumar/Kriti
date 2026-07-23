-- Per (paper, analysis_kind) cross-module section content.
-- persist-cross-module-analysis writes one row per kind.
-- analysis_kind covers 7 kinds: architecture, dependencies, interactions,
-- patterns, gaps, mathematics, novelty — the full set of cross-module
-- analysis perspectives the prompts produce.

CREATE TABLE IF NOT EXISTS academic_cross_module_analysis (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    analysis_kind   TEXT    NOT NULL CHECK (analysis_kind IN ('architecture','dependencies','interactions','patterns','gaps','mathematics','novelty')),
    content         TEXT    NOT NULL DEFAULT '',
    model           TEXT    NOT NULL DEFAULT '',
    file_path       TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, analysis_kind)
);
