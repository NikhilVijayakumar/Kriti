-- Catalog of prompt/scaffold content on disk.
-- seed_templates walks prompt/ (dispatched semantic prompt content, scoped
-- by owning usecase folder name) and templates/ (scaffold manifests/output
-- templates a script reads directly, never dispatched as a semantic step —
-- _master-schema.yaml, the audit-report markdown/HTML shells). scope is
-- directory-derived, not a fixed enum: usecase folders are added/removed
-- over time (novelty-analysis, gap-analysis, mathematics-and-diagrams,
-- assemble-paper-structure, semantic-audit, plagiarism-forensic-audit,
-- humanize, _shared, common), and a hand-maintained enum would only ever
-- lag that.

CREATE TABLE IF NOT EXISTS academic_templates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    template_kind TEXT    NOT NULL CHECK (template_kind IN ('prompt','scaffold')),
    scope         TEXT    NOT NULL,
    name          TEXT    NOT NULL,
    file_path     TEXT    NOT NULL,
    UNIQUE(template_kind, scope, name)
);
