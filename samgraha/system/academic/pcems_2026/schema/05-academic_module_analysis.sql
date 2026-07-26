-- Per (module, analysis_kind) section content.
-- persist-module-analysis writes one row per module × kind combination.
-- analysis_kind is constrained to the 5 kinds the module-analysis prompts
-- produce: summary, architecture, mathematics, novelty, gaps.
-- content is the full markdown output from the semantic step.
-- file_path is where the content was also written on disk (docs/paper/...).

CREATE TABLE IF NOT EXISTS academic_module_analysis (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id       INTEGER NOT NULL REFERENCES academic_modules(id) ON DELETE CASCADE,
    analysis_kind   TEXT    NOT NULL CHECK (analysis_kind IN ('summary','architecture','mathematics','novelty','gaps')),
    content         TEXT    NOT NULL DEFAULT '',
    model           TEXT    NOT NULL DEFAULT '',
    file_path       TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(module_id, analysis_kind)
);
