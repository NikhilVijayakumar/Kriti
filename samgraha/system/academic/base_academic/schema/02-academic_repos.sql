-- One row per (repo_root, standard) classification result.
-- classify-repo writes this; the 4-state classification determines which
-- entry usecase the orchestrator dispatches to.
--
-- CHECK constraint uses the 4-state model:
--   NO_DOCS_NO_IMPL   — refuse: nothing to draft from
--   DOCS_ONLY         — draft-from-docs-only (unvalidated)
--   IMPL_NO_ANALYSIS  — generate-analysis-docs first, then fall through
--   IMPL_WITH_ANALYSIS — generate-paper-draft directly
--
-- has_implementation/has_analysis_docs are redundant with the classification
-- value but kept for fast query without string matching.

CREATE TABLE IF NOT EXISTS academic_repos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    repo_root     TEXT    NOT NULL,
    classification TEXT   NOT NULL CHECK (classification IN (
        'NO_DOCS_NO_IMPL', 'DOCS_ONLY', 'IMPL_NO_ANALYSIS', 'IMPL_WITH_ANALYSIS'
    )),
    has_implementation INTEGER NOT NULL DEFAULT 0,
    has_analysis_docs  INTEGER NOT NULL DEFAULT 0,
    module_count  INTEGER NOT NULL DEFAULT 0,
    metadata      TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL,
    UNIQUE(standard, repo_root)
);
