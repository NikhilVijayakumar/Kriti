-- Per-claim verification findings for Step 0 extracted items.
-- Append-only, one row per (claim, check_kind, model).
-- module_id is NULL for per-paper items (cross_module_analysis, map tables).
-- check_kind covers all 4 verification checks: 2 deterministic + 2 semantic.
-- verdict is PASS/FAIL. evidence_note captures the check's detail.
-- model enables multi-model tracking — 2 semantic checks can be run with
-- different LLMs and compared per model.

CREATE TABLE IF NOT EXISTS academic_step0_claim_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    module_id     INTEGER REFERENCES academic_modules(id) ON DELETE CASCADE,
    table_name    TEXT    NOT NULL,
    row_id        INTEGER NOT NULL,
    check_kind    TEXT    NOT NULL CHECK (check_kind IN ('evidence-resolves','evidence-contains-claim','claim-grounded','no-drift')),
    model         TEXT    NOT NULL DEFAULT '',
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    evidence_note TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, module_id, table_name, row_id, check_kind, model)
);
