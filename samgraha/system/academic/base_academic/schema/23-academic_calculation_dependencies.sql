-- One row per declared dependency edge from a calculation/**/*.yaml
-- file to whatever it reads (another calc file, or a DB table+scope).
-- consumed_by is the crux: a comma-joined list of every script that
-- actually loads calc_path at runtime (a single calc_path can
-- legitimately have more than one real reader — generation/{domain}.yaml
-- is read by both check-word-budget and deterministic-audit, confirmed
-- by reading both scripts), or NULL if none do. NULL = dead calculation
-- file: declared, maybe even internally correct, never read by anything.
-- audit_calculation_wiring.py populates this by grepping every known
-- reader script's source for calc_path refs and joining every match —
-- deliberately a single string column, not a join table or a UNIQUE key
-- that admits one row per reader: a dependency *edge* (calc_path reads
-- depends_on) is one fact regardless of how many scripts happen to read
-- the calc_path side of it, and folding readers into row identity
-- created exactly the bug this comment is warning against (an earlier
-- version keyed UNIQUE on consumed_by too, which meant two genuinely
-- different readers of the same edge fought over the same row identity
-- the moment the audit tried to update both — reverted).

CREATE TABLE IF NOT EXISTS academic_calculation_dependencies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    calc_path       TEXT    NOT NULL,   -- relative to calculation/, e.g. 'report/aggregation/domain/methodology.yaml'
    depends_on_kind TEXT    NOT NULL CHECK (depends_on_kind IN ('calc_file','db_table','db_scope')),
    depends_on      TEXT    NOT NULL,   -- calc_file: another calc_path; db_table: table name; db_scope: 'table.scope_value'
    consumed_by     TEXT,               -- comma-joined reader script names, NULL = dead
    last_audited_at TEXT,               -- set by audit_calculation_wiring.py each run
    UNIQUE(calc_path, depends_on_kind, depends_on)
);
CREATE INDEX IF NOT EXISTS idx_calc_deps_calc_path
    ON academic_calculation_dependencies(calc_path);
CREATE INDEX IF NOT EXISTS idx_calc_deps_consumed_by
    ON academic_calculation_dependencies(consumed_by);
