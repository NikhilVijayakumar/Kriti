# base_academic — Schema Depth, Calculation Dependency Graph, and Optimization Proposal

## 0. Why This Document Exists

`base_academic/schema/` has grown to 22 files (21 tables + 1 view file)
across six proposals without ever being audited as a whole for index
coverage, engine-catalog completeness, or whether the `calculation/**`
tree it backs is actually wired to the scripts that are supposed to
read it. Confirmed on disk today:

- **`academic_proposals` (schema/22) was never added to `standard.yaml`'s
  `custom_tables:` catalog list** — confirmed by grep: `academic_section_
  citations` (schema/21) has a `custom_tables:` entry, `academic_proposals`
  does not. This matters because `custom_tables:` isn't documentation —
  `E:\Python\samgraha\crates\services\src\register_standard.rs` (the real
  engine, confirmed by reading its source) reads this exact list on every
  `register_standard` MCP call and `INSERT`s one row per entry into
  `custom_data_tables` (`E:\Python\samgraha\schema\knowledge\
  08-custom_data_tables.sql`'s table — the engine's own catalog of
  "what tables does this standard own and why," populated by rows, not
  by hand-written DDL in that file). `register_standard` already runs
  as Phase 1 of every `run_full_workflow.py` invocation — the mechanism
  is live and working, `academic_proposals` is just missing from the
  list it reads, so the engine has zero record that the table exists.
- **`calculation/report/aggregation/domain/*.yaml` (12 files) is dead —
  `calculate.py` never reads it.** Confirmed by reading `calculate.py`
  in full: its per-domain score is computed inline (`weights.get(
  "semantic_document", 50)` / `weights.get("deterministic_document", 50)`
  from `report/summary/final_score.yaml`'s flat `inputs:` list), never
  touching `calculation/report/aggregation/domain/{domain}.yaml` at all.
  This was already flagged once (`base_academic-report-granularity-and-
  audit-governance-proposal.md`'s own §0) and explicitly left unfixed by
  the next proposal in the series (`generation-content-depth-and-
  verification-proposal.md` §9: "a report-side problem... not fixed
  here"). Still true today.
- **These same 12 files have stale, broken path references from before
  the directory restructure** — `calculation/report/aggregation/domain/
  methodology.yaml`'s `inputs:` block (confirmed): `deterministic:
  calculation/deterministic/methodology.yaml` and `semantic: calculation/
  semantic/full-part-blend.yaml`. Neither path exists — `calculation/
  deterministic/` and `calculation/semantic/` were renamed to `calculation/
  generation/` and `calculation/report/semantic/` by the generation-
  content-depth proposal's §5 restructure (implemented). These 12 files
  are doubly broken: unwired *and* internally pointing at directories
  that no longer exist, so even a future integration attempt would fail
  against them as-is.
- **`calculation/report/semantic/ensemble/**` (48 files, the multi-model
  reliability-weighted-mean mechanism from the report-granularity
  proposal's §6) is also dead.** `calculate.py`'s semantic-score query
  (`SELECT overall_score FROM academic_semantic_runs WHERE paper_id=? AND
  domain_id=? ORDER BY run_number DESC LIMIT 1`) never groups by model or
  computes a mean/stdev/agreement — it takes whichever row has the
  highest `run_number`, full stop. `--models claude-sonnet-5,gpt-5` (the
  flag `run_full_workflow.py` already supports, confirmed) produces two
  rows per domain; `calculate.py` picks one of them arbitrarily by
  insertion order, silently discarding the other model's score instead
  of averaging them per the ensemble formula these 48 files define.
- **`calculate.py`'s semantic-score query has no `scope` filter at all —
  a real correctness bug, not just a wiring gap.** `academic_semantic_
  runs.scope` distinguishes `section-full` from `section-part` (schema/09,
  confirmed), both of which set `domain_id`. The query above filters only
  on `paper_id`/`domain_id`, ordering by `run_number` across *all* scopes
  for that domain — if a `section-part` run (citations-only, or budget-
  fit-only, generally a lower/different score) happens to have a higher
  `run_number` than the domain's `section-full` run, `calculate.py`
  silently blends a part-score into what's documented as the whole-
  domain final score. Nothing catches this today; the bug is silent.
- **21 tables, only 5 have an explicit `CREATE INDEX`** (confirmed by
  counting `CREATE INDEX` per file across `schema/*.sql`: `academic_
  narratives`, `academic_score_history`, `academic_report_history`,
  `academic_section_citations`, `academic_proposals`). Most of the
  remaining 16 are adequately covered by a `UNIQUE` constraint SQLite
  auto-indexes (`academic_modules`, `academic_module_analysis`,
  `academic_plagiarism_findings`, `academic_humanize_passes`,
  `academic_cross_module_analysis`, `academic_semantic_runs`, `academic_
  deterministic_findings` all have a `UNIQUE(...)` whose leftmost columns
  match their real lookup pattern) — but two do not: **`academic_
  narrative_sections`** (queried by `narrative_id` on every word-count
  and render call — `persist_section_draft.py`'s `_narrative_word_count()`,
  `generate_audit_report.py`'s section assembly — no `UNIQUE`, no index,
  full-table scan on every call) and **`academic_visualizations`**
  (queried by `paper_id`/`chart_type_id`/`domain_id` on every chart
  fetch — `generate_audit_report.py`'s chart embedding — no `UNIQUE`,
  no index).
- **`academic_visualizations` has no reproducibility or provenance
  columns** — confirmed, schema/17: `id`, `chart_type_id`, `paper_id`,
  `domain_id`, `content_hash`, `file_path`, `created_at`. No `commit_sha`
  (every other audit-adjacent table has one, §0 of the report-governance
  proposal established this as the reproducibility mechanism — a chart
  is exactly as "was this rendered against current data" as a
  deterministic finding, but has no way to answer that question today),
  and no record of what query/parameters actually produced it — `render_
  charts.py` regenerating a chart has no stored trail of what data window
  or config it used last time, only the output image.

## 1. Scope

Five new files under `schema/` (23-27, table definitions only — no
existing `.sql` file's `CREATE TABLE` body is edited in place, per
§6's migration note), one `standard.yaml` fix (the missing `custom_
tables:` entry, §2), `calculate.py` (scope-filtered query fix, §5a — a
correctness bug, not new scope creep), one new verification script
(`script/schema/audit_calculation_wiring.py`, §4), and `academic_
schema.py`'s `ensure_schema()` (new `ALTER TABLE` migrations for the
two index-only additions and the visualization columns, §6). **Does
not touch `E:\Python\samgraha\` at all** — the core engine's own seven
tables (`usecase`/`script`/`prompt`/`step`/`step_script`/`step_prompt`/
`execution`) plus its `custom_data_tables` catalog table stay exactly
as they are; the fix in §2 is a `standard.yaml` declaration this
standard already had the mechanism for, not a schema change to the
engine (§0's `register_standard.rs` reading confirms the mechanism
already exists and already works — this proposal populates it
correctly, doesn't build it). Does not fix `calculation/report/
aggregation/domain/**`'s or `calculation/report/semantic/ensemble/**`'s
dead-wiring by actually rewriting `calculate.py` to consume them (§9,
out of scope) — it makes both gaps *queryable* (§4) and *correct on
their own terms* (§3's path fix), the wiring itself is separately
scoped work.

## 2. Engine-Catalog Fix — `standard.yaml`

```yaml
# script/schema/standard.yaml, custom_tables: section
  - table_name: academic_proposals
    purpose: "one row per proposal draft/decision — generation/audit/report/fix gate (docs/proposal/base_academic-proposal-gate-workflow-proposal.md)"
    owner_script: persist-proposal
```

One entry, inserted alongside the existing 20. The next `register_
standard` call (Phase 1 of every `run_full_workflow.py` run, already
unconditional) picks it up with no other change required — confirmed
against `register_standard.rs`'s `for ct in &manifest.custom_tables`
loop, which runs on every registration, not just first-install. This
is the entirety of "register what we own into `08-custom_data_tables.
sql`" done correctly: through the declarative list the engine already
parses, not by hand-writing `INSERT`/`CREATE TABLE` statements into a
file `E:\Python\samgraha\schema\knowledge\08-custom_data_tables.sql`
that only defines the *catalog table's own shape* (confirmed by reading
it — it's one `CREATE TABLE custom_data_tables (...)`, not a place for
per-standard rows) and that this proposal does not touch, per §1.

## 3. Fix the Broken Path References (No Behavior Change, Just Correctness)

`calculation/report/aggregation/domain/*.yaml` (12 files) and any other
file still pointing at pre-restructure paths get their `inputs:` block
corrected to the real, current locations — worked example:

```yaml
# calculation/report/aggregation/domain/methodology.yaml, corrected
inputs:
  deterministic: calculation/generation/methodology.yaml
  semantic: calculation/report/semantic/full-part-blend.yaml
```

This doesn't make the file *consumed* (§0 — that's still `calculate.py`'s
job, out of scope here per §1) — it makes the file *correct*, so the
next person who wires it up isn't debugging a second, unrelated bug
(wrong paths) on top of the wiring gap. Applied to all 12
`aggregation/domain/*.yaml` files (same two-line substitution, domain
name varies).

## 4. Calculation Dependency Graph — New Table

### 4a. Schema — `academic_calculation_dependencies`

```sql
-- schema/23-academic_calculation_dependencies.sql
-- One row per declared dependency edge from a calculation/**/*.yaml
-- file to whatever it reads (another calc file, or a DB table+scope).
-- consumed_by is the crux of this table: the name of the script that
-- actually loads calc_path at runtime, or NULL. NULL is not "unknown" —
-- it's a signal, populated by audit_calculation_wiring.py (§4c) reading
-- calculate.py/deterministic_audit.py/check_word_budget.py's own source
-- for `_load_yaml(...)`/`open(...)` calls against calc_path. A row with
-- consumed_by IS NULL is a dead calculation file: declared, maybe even
-- internally correct, never read by anything. §0's two dead-wiring
-- findings (aggregation/domain, ensemble) are the first real rows here,
-- not hypothetical — this table exists because grepping for that
-- exact fact by hand is what produced §0's findings in the first place.

CREATE TABLE IF NOT EXISTS academic_calculation_dependencies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    calc_path       TEXT    NOT NULL,   -- relative to calculation/, e.g. 'report/aggregation/domain/methodology.yaml'
    depends_on_kind TEXT    NOT NULL CHECK (depends_on_kind IN ('calc_file','db_table','db_scope')),
    depends_on      TEXT    NOT NULL,   -- calc_file: another calc_path; db_table: table name; db_scope: 'table.scope_value'
    consumed_by     TEXT,               -- script name (script table's own naming) that reads calc_path, NULL = dead (§4c)
    last_audited_at TEXT,               -- set by audit_calculation_wiring.py each run, NULL until first audit
    UNIQUE(calc_path, depends_on_kind, depends_on)
);
CREATE INDEX IF NOT EXISTS idx_calc_deps_calc_path
    ON academic_calculation_dependencies(calc_path);
CREATE INDEX IF NOT EXISTS idx_calc_deps_consumed_by
    ON academic_calculation_dependencies(consumed_by);
```

The `idx_calc_deps_consumed_by` index is what makes "list every dead
calculation file" a fast, direct query (`WHERE consumed_by IS NULL`),
not a table scan — small table, but the query is exactly the point of
this feature, worth indexing on day one rather than after it's slow.

### 4b. Seed data — the real edges, including the two known-dead ones

```sql
-- Seeded by init_schema.py (§7), not hand-inserted per-paper — this is
-- standard-level metadata, one set of rows total, not one per paper_id
-- (no paper_id column above — deliberately, this describes the
-- standard's calculation graph, not a per-run fact).

INSERT INTO academic_calculation_dependencies (calc_path, depends_on_kind, depends_on, consumed_by) VALUES
  ('generation/methodology.yaml', 'db_table', 'academic_narratives', 'check-word-budget'),
  ('generation/methodology.yaml', 'db_table', 'academic_narratives', 'deterministic-audit'),
  ('report/summary/final_score.yaml', 'db_scope', 'academic_semantic_runs.section-full', 'calculate'),
  ('report/summary/final_score.yaml', 'db_table', 'academic_deterministic_findings', 'calculate'),
  ('report/aggregation/domain/methodology.yaml', 'calc_file', 'generation/methodology.yaml', NULL),
  ('report/aggregation/domain/methodology.yaml', 'calc_file', 'report/semantic/full-part-blend.yaml', NULL),
  ('report/semantic/full-part-blend.yaml', 'db_scope', 'academic_semantic_runs.section-full', NULL),
  ('report/semantic/full-part-blend.yaml', 'calc_file', 'report/semantic/section-parts.yaml', NULL),
  ('report/semantic/ensemble/methodology.yaml', 'db_scope', 'academic_semantic_runs.section-full', NULL);
  -- Full seed is one INSERT per domain × (generation.yaml, aggregation/
  -- domain, ensemble) + the shared summary/report files — worked
  -- examples above, complete 16-domain × N-edge seed is init_schema.py's
  -- implementation, not restated file-by-file here (§9).
```

The `NULL` `consumed_by` values above are not placeholders to fill in
later — they're §0's actual findings, encoded as data instead of prose,
which is the whole point: `calculate.py` really does not read `report/
aggregation/domain/*.yaml` or `report/semantic/ensemble/*.yaml` today,
confirmed by direct reading (§0), so the seed data says exactly that.

### 4c. `script/schema/audit_calculation_wiring.py` — keeps the graph honest

```python
"""audit_calculation_wiring.py — re-derives consumed_by for every row in
academic_calculation_dependencies by grepping known calculation-reading
scripts' source for references to calc_path. Static, source-level check
(not a runtime trace) — same trust level as the rest of this standard's
"confirmed by reading the script" evidence style. Run manually or as
part of a schema-health check; not wired into run_full_workflow.py's
per-paper pipeline (this is standard-level metadata, not per-run work,
§4b)."""
_READER_SCRIPTS = {
    "calculate": "script/calculate/calculate.py",
    "check-word-budget": "script/assemble-paper-structure/check_word_budget.py",
    "deterministic-audit": "script/deterministic-audit/deterministic_audit.py",
}

def audit(conn):
    rows = conn.execute(
        "SELECT id, calc_path, consumed_by FROM academic_calculation_dependencies").fetchall()
    changed = []
    for row in rows:
        actual_reader = None
        for script_name, script_path in _READER_SCRIPTS.items():
            with open(script_path, encoding="utf-8") as f:
                if row["calc_path"] in f.read():
                    actual_reader = script_name
                    break
        if actual_reader != row["consumed_by"]:
            changed.append((row["id"], row["calc_path"], row["consumed_by"], actual_reader))
        conn.execute(
            "UPDATE academic_calculation_dependencies SET consumed_by=?, last_audited_at=datetime('now') WHERE id=?",
            (actual_reader, row["id"]))
    conn.commit()
    return changed  # [(id, calc_path, old_consumed_by, new_consumed_by), ...] — drift report
```

Registered as its own usecase-adjacent script (not a `propose-*` step —
this is a schema-health tool an operator runs deliberately, same
category as `git_gate.py`, not part of the per-paper pipeline).

## 5. `calculate.py` — Fix the Silent Scope Bug

### 5a. The fix

```python
# calculate.py, sem_row query — before:
sem_row = conn.execute(
    "SELECT overall_score FROM academic_semantic_runs "
    "WHERE paper_id=? AND domain_id=? "
    "ORDER BY run_number DESC LIMIT 1",
    (paper_id, domain_id),
).fetchone()

# after:
sem_row = conn.execute(
    "SELECT overall_score FROM academic_semantic_runs "
    "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
    "ORDER BY run_number DESC LIMIT 1",
    (paper_id, domain_id),
).fetchone()
```

One clause. `scope='section-full'` is the whole-domain semantic
judgment (§0's schema/09 comment: "Whole-domain semantic judgment,"
report-granularity proposal §2b) — the only scope a per-domain final
score should ever blend in; `section-part` scores (citations/enrichment/
budget-fit) are inputs to `full-part-blend.yaml`'s formula, not
substitutes for the full-domain score on their own.

### 5b. Why this is in-scope for a schema proposal

This isn't drive-by scope creep — `academic_calculation_dependencies`
(§4) would have caught this the moment someone tried to seed the
correct edge (`final_score.yaml` depends on `academic_semantic_runs.
section-full`, §4b's seed) against the *actual* query and found it
doesn't filter scope at all. The graph and the bug are the same finding
looked at two ways: a schema meant to describe "what reads what, from
where" is incomplete if the "where" (`scope='section-full'`) isn't
even true of the reading code yet.

## 6. Visualization Detail — New Columns on `academic_visualizations`

```sql
-- Migration (academic_schema.py's ensure_schema(), same try/except-
-- OperationalError pattern as academic_proposals.metadata, §7 — not a
-- new numbered schema/*.sql file, since this edits an EXISTING table's
-- shape and CREATE TABLE IF NOT EXISTS is a no-op against a database
-- that already has the table without these columns):
ALTER TABLE academic_visualizations ADD COLUMN commit_sha TEXT NOT NULL DEFAULT '';
ALTER TABLE academic_visualizations ADD COLUMN generation_params TEXT;  -- JSON: query window, chart-specific args
ALTER TABLE academic_visualizations ADD COLUMN width INTEGER;
ALTER TABLE academic_visualizations ADD COLUMN height INTEGER;
```

`commit_sha` gives charts the same reproducibility story every other
audit-adjacent table already has (§0) — `render_charts.py` gains a
`commit_sha` parameter threaded the identical way `deterministic_
audit.py`'s was (report-granularity proposal §4b), letting a future
skip-if-unchanged check apply to chart rendering the same way it
already applies to deterministic/semantic audits. `generation_params`
is a debugging/regeneration aid — today, re-deriving what a chart shows
means reading `render_charts.py`'s current logic and guessing whether
it matches what produced the file on disk; storing the actual params
(date range, model filter, whatever a given `chart_key` takes) closes
that gap directly. `width`/`height` are metadata `generate_audit_
report.py`'s HTML embedding currently has no source for at all (every
`<img>` tag renders without explicit dimensions today).

## 7. `academic_calculation_dependencies` Seeding — `init_schema.py`

```python
# script/schema-init/init_schema.py, new call alongside seed_domains/
# seed_templates/seed_visualization_types:
academic_schema.seed_calculation_dependencies(conn, CALCULATION_DEPENDENCY_EDGES)
```

`seed_calculation_dependencies()` — new function in `academic_schema.py`,
same `INSERT ... ON CONFLICT DO UPDATE` idempotent shape `seed_domains()`
already uses (§4b's seed data is the literal argument, generated from
the domain list + the fixed per-domain edge pattern, not hand-typed
16 times — same "generated, not hand-duplicated" reasoning `generate_
per_domain_usecases.py` already applies to verify scripts).

## 8. New/Changed Files — Consolidated

| File | Change |
|---|---|
| `schema/23-academic_calculation_dependencies.sql` | New (§4a) |
| `calculation/report/aggregation/domain/*.yaml` (12 files) | Path fix only, `inputs:` block corrected (§3) |
| `script/schema/audit_calculation_wiring.py` | New (§4c) |
| `script/calculate/calculate.py` | `sem_row` query gains `AND scope='section-full'` (§5a) |
| `script/common/academic_schema.py` | New `ALTER TABLE` migrations for `academic_visualizations` (§6); new `seed_calculation_dependencies()` function (§7) |
| `script/schema-init/init_schema.py` | New `seed_calculation_dependencies()` call (§7) |
| `script/render-audit-report/render_charts.py` | Gains `commit_sha`/`generation_params`/`width`/`height` params threaded into `academic_visualizations` inserts (§6) |
| `script/schema/standard.yaml` | New `academic_proposals` entry under `custom_tables:` (§2) |

## 9. Explicitly Out of Scope

Actually wiring `calculate.py` to read `calculation/report/aggregation/
domain/**` or `calculation/report/semantic/ensemble/**` (§0/§4b — this
proposal makes both gaps *correct* (§3) and *queryable* (§4), not
*consumed*; that's a scoring-logic change with its own design questions
— does the whole-paper formula change too, does ensemble apply
retroactively to already-scored papers — deserving its own proposal,
not a schema-depth pass's drive-by). Any change to `E:\Python\samgraha\`
(§1 — confirmed the engine's own catalog mechanism already works,
nothing there needs fixing). The full 16-domain seed list for §4b/§7
(worked examples given, complete generation is `init_schema.py`
implementation work). A UI or report surface for the dependency graph
(the `WHERE consumed_by IS NULL` query in §4a is the deliverable — a
rendered report of it, if wanted, is a `propose-report`-adjacent
follow-on, not this proposal's job). `academic_narrative_sections` and
the other under-indexed-by-omission table already flagged (§0) —
**correction, these ARE in scope**: see below.

### 9a. `academic_narrative_sections` Index — Folded Into §6's Migration Batch

Not a separate section — same `ensure_schema()` migration batch as §6:

```python
try:
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_narrative_sections_lookup "
        "ON academic_narrative_sections(narrative_id)")
except sqlite3.OperationalError:
    pass
```

`CREATE INDEX IF NOT EXISTS` is itself idempotent (unlike `ALTER TABLE
ADD COLUMN`), so this doesn't strictly need the try/except — included
in the same migration function as §6's columns for one place to look,
not because it can fail the way `ADD COLUMN` on an existing column can.
