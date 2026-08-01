# rust_dev — Samgraha Generic-Schema Alignment (Proposal 6 of 7)

## 0. Series + what this corrects

Sixth of a growing proposal set — see
[`1-rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
**This proposal corrects proposals 2 and 4**, which were written against
`pcems_2026`'s `standard.yaml`/`academic_*` tables as the only reference
model, without checking the actual samgraha engine
(`E:\Python\samgraha`, separate repo from `Kriti`) that both standards run
on. Read `E:\Python\samgraha\schema\knowledge\*.sql` (17 files) and
`crates/services/src/seed_standard.rs` directly for this pass — corrects
two concrete mistakes:

- **Proposal 2 §3** implied `rust_dev` needs its own
  `common/script/academic_schema.py`-equivalent and its own `usecase`/
  `step`-shaped tables. It doesn't — `usecase`, `step`, `script`, `prompt`,
  `domain`, `step_script`, `step_prompt` are **samgraha's own generic
  tables**, one shared set for every standard (`WHERE standard = ?`
  scoping, not per-standard schemas). `pcems_2026`'s `academic_*` tables
  are that standard's **custom_data_tables** — content pcems owns because
  academic-paper narratives/citations/findings have no generic shape
  samgraha could provide — not a pattern to copy wholesale for
  orchestration metadata that already has a generic home.
- **Proposal 4 §4** invented `dev_tier_usecase_map` as a new
  `custom_data_tables` entry to store what's substantially already free
  once usecases are registered generically (§2 below).

**Status**: this proposal is corrections-only by design (§8) — it has no
build list of its own. Its corrections are already load-bearing in the
live `common/schema-manifest/standard.yaml`, not just theoretical: real
`domains:` (13 entries, no `dev_schema.py`-equivalent), no `data:` block
on any usecase, `dev_tier_usecase_map` never built (proposal 4's doc
retired it), `dev_proposal_phase_scope` is the table proposal 5's doc now
points at instead of the dropped one (§6 below). §7's 3 open questions:
1 and 2 resolved this pass (direct source reads, not inference); 3
(`dev_repo_domain_state` append-only) stands as recommended — building it
is proposal 7's job, not this one's.

## 1. The generic tables, read directly

| Table | Columns (from `.sql`) | Role |
|---|---|---|
| `usecase` | `id, standard, name, description, data (JSON, opaque to samgraha), domain_id` | one row per usecase, `UNIQUE(standard, name)` |
| `step` | `id, usecase_id, step_order, kind (deterministic\|semantic), description` | ordered steps within a usecase |
| `script` | `id, standard, name, location, purpose` | deterministic step implementations, `UNIQUE(standard, name)` |
| `prompt` | `id, standard, name, purpose, content` | semantic step content, stored **inline**, not a path — *"read once at register time, handed to the calling agent verbatim at dispatch time"* |
| `step_script` / `step_prompt` | `(step_id, script_id\|prompt_id)` | wires a step to its implementation |
| `domain` | `id, standard, key, sort_order, description` | *"discovery-only domain mirror... metadata for filtering and grouping usecases"* |
| `proposal` | `id, standard, usecase_id, template_id, execution_id, title, status, location, metadata_json` | generic proposal lifecycle |
| `custom_data_tables` | `id, standard, table_name, purpose, owner_script_id, shape_json` | **catalog only** — *"samgraha never creates, migrates, or manages the data of these tables — it only records that they exist"* |

This is exactly the shape `standard.yaml`'s `scripts:`/`prompts:`/`usecases:`
blocks (proposal 2 §2, §3) map onto. **Confirmed by reading
`crates/services/src/register_standard.rs` directly** (not guessed, as
flagged open in an earlier pass of this proposal — see §7): its own doc
comment states it *"Registers a knowledge standard into knowledge.db's
core schema (usecase/script/prompt/step/step_script/step_prompt/
custom_data_tables)"* — 7 named tables; the code additionally populates
`domain` (lines 211-217, `domain_ids` map built from `manifest.domains`
and used to resolve `usecase.domain_id`) — 8 tables actually touched, the
doc comment just doesn't list `domain` by name. Proposal 2's
`standard.yaml` skeleton was already correctly shaped for this; what
proposal 2 got wrong was *layering a second, parallel schema on top*
(`dev_schema.py`, `dev_*.sql`) as if `rust_dev` needed its own copy of
what `usecase`/`step`/`script`/`prompt` already are.

**Critical caveat, confirmed by the same file (line 29-32's doc comment on
the `seeder_script` field): *"When present, the seeder is invoked instead
of parsing YAML workflow declarations."*** Any standard that declares
`seeder_script` (pcems_2026 does: `seeder_script: ../script/seeder.py`,
confirmed in its `standard.yaml`) does **not** go through the direct
`manifest.scripts`/`manifest.prompts`/`manifest.usecases` struct-parsing
path (`register_standard.rs` lines 265-277) at all — `register_standard`
instead shells out to that Python script (`crate::seeder::run_seeder`,
confirmed at lines 509-530), and the Python script does its own inserts.
Read `pcems_2026`'s real `seeder.py` directly: its own docstring —
*"Reads common/schema-manifest/standard.yaml, creates academic_* tables,
seeds domains, scripts, prompts, usecases (with expanded steps),
templates, and custom_data_tables into knowledge.db"* — it re-implements
the same ingestion register_standard.rs would otherwise do, in Python,
because it also needs to `CREATE TABLE` its custom `academic_*` tables in
the same pass (something the generic Rust path has no reason to do).
Proposal 2 already correctly flagged `seeder_script: ../script/seeder.py`
as net-new required work (§4) — this proposal's §2 below assumed the
*generic* Rust path was what mattered; in fact, because `rust_dev` will
have its own custom table (`dev_repo_domain_state`, §5) exactly like
pcems does, `rust_dev` will also declare `seeder_script` and therefore
also bypass the generic path — **`rust_dev`'s own `seeder.py`, not
`register_standard.rs`'s struct fields, is what actually constructs every
row this proposal describes.**

**Built**: `seeder_script: ../script/seeder.py` is declared and
`common/script/seeder.py` exists, ported from pcems's own seeder.py.
Verified end-to-end against a real `knowledge.db` bootstrapped from
samgraha's actual core schema, not just eyeballed — creates all 10
`dev_*` tables (§5, §7), seeds 13 domains + 96 usecases, resolves `tier`
correctly per usecase, idempotent on re-run. Also confirmed empirically
while building it: the struct-parsing `register_standard` function this
section describes as bypassed is dead code in the current engine —
`activate_standard` (the function the `register_standard` MCP tool
actually calls) never calls it, for *any* standard, `seeder_script` or
not. `custom_data_tables` rows are populated automatically by
`activate_standard` itself post-seeder, via `standard.metadata.json` +
`PRAGMA table_info` introspection — `seeder.py` doesn't touch that table.

## 2. Where "tier" actually lives — `usecase.data`, no *SQL* schema change, but not a bare YAML key either

Proposal 2 §6's open question #2 and proposal 4's entire premise both
assumed tier needs a first-class column somewhere. It doesn't need a
**SQL** schema change — `usecase.data TEXT NOT NULL DEFAULT '{}'` is
explicitly documented as *"additional data, opaque to samgraha"* — but
getting `tier` into it is **not** a matter of writing an arbitrary `data:`
block in `standard.yaml` and expecting it to pass through. Read
`register_standard.rs`'s `UsecaseDecl` struct directly (lines 66-79): its
fields are exactly `name, description, driver, depends_on, domain,
verify_script, steps` — **no generic `data` field at all**. The `data`
JSON actually written to the `usecase` row (lines 269-273) is Rust-code
that *constructs* `{"driver": ..., "depends_on": ..., "verify_script": ...}`
from those three named fields — any other key a `standard.yaml` author
writes under a `data:` block on that path is silently dropped by serde
(unknown fields, no `deny_unknown_fields`), not stored. `domain:` **is**
already a first-class top-level field this path resolves to `domain_id`
(line 267) — confirmed real, not proposed — but there's no `tier:`
equivalent anywhere in this struct.

That said, §1's caveat resolves this cleanly: `rust_dev` will declare
`seeder_script` (same as pcems, both need it for their custom tables), so
`register_standard.rs`'s `UsecaseDecl` struct **never runs** for either
standard — `rust_dev`'s own `seeder.py` builds every `INSERT INTO usecase`
statement itself, in Python, exactly like pcems's `seeder.py` does for
`academic_*` (confirmed: pcems's `seeder.py` docstring says it *"seeds...
usecases (with expanded steps)... into knowledge.db"* directly). Since
`rust_dev`'s `seeder.py` is standard-owned code, not samgraha's generic
struct, it can put `tier` into `usecase.data`'s JSON freely — the
constraint above only applies to the bypassed generic path. Concretely:
`rust_dev`'s `standard.yaml` still declares `domain: security` per usecase
(first-class, self-documenting, matches what `register_standard.rs`
*would* read if there were no seeder), but `tier` is computed by
`seeder.py` itself from `plan/core/tiers.yaml`'s domain→tier partition at
seed time and written into `usecase.data` alongside `driver`/`depends_on`
— **the generator this proposal's §3 needs is logic inside `seeder.py`,
not a separate script that patches `standard.yaml` before some other
generic step reads it** (corrects this proposal's own §3, written before
this distinction was confirmed).

`seed_standard.rs` (a *different* file from `register_standard.rs` — one
ingests, the other executes; see §4) already parses two keys out of
`usecase.data` in production once it's populated, regardless of which
path wrote it: `data.driver` (defaults to `"samgraha"`, used to skip
externally-driven usecases) and `data.depends_on` (an array of usecase
names, walked transitively for topological execution order —
`seed_standard.rs`'s own doc-comment: *"Walks depends_on transitively,
executes every driver: samgraha prerequisite in topological order"*).
`tier`, once `seeder.py` writes it, is available to any reader of
`usecase.data` the same way — nothing about it needing engine-level
recognition; it only needs to be *written* correctly, which is `seeder.py`'s
job, not `register_standard.rs`'s.

`depends_on` here is the concrete, engine-enforced replacement for
`loop.yaml`'s prose `tier_gate` rule (*"every domain in the tier must
reach threshold before the next tier starts"*) — instead of a rule an
external orchestrator has to interpret, every tier-2+ usecase's
`depends_on` names the specific prior-tier usecases (per `tiers.yaml`'s
`relationships:`) that must complete first, and `seed_standard`'s
topological sort enforces it directly. This is a better mechanism than
what proposal 1/3 assumed existed (nothing did — `loop.yaml`'s tier_gate
was always just prose, no engine reads it today).

## 3. Proposal 4, corrected — "usecase map" is mostly a query, not a table

Once every rust_dev usecase carries `data.tier` (§2), the tier usecase map
proposal 4 designed a whole generator+table for is one query:

```sql
SELECT u.name, u.data, d.key AS domain_key,
       s.step_order, s.kind, s.description
FROM usecase u
JOIN domain d ON d.id = u.domain_id
LEFT JOIN step s ON s.usecase_id = u.id
WHERE u.standard = 'rust_dev'
  AND json_extract(u.data, '$.tier') = ?1
ORDER BY u.name, s.step_order;
```

What proposal 4 gets **right** and should keep: the *algorithm* that
computes `tier` for every usecase from `tiers.yaml`'s domain→tier
partition (§2's `generate_tier_usecase_map.py` — but per §2's corrected
mechanism, this isn't a standalone script patching `standard.yaml` before
some other generic ingestion step reads it; it's logic **inside
`rust_dev`'s own `common/script/seeder.py`**, the same file pcems's
`seeder.py` already builds `academic_domains` sort orders from
`_DOMAIN_SORT_ORDERS`-style dicts in — `rust_dev`'s `seeder.py` reads
`tiers.yaml` the same way and folds `tier` into the `data` JSON it
constructs per usecase before its own `INSERT INTO usecase` call). What it
gets **wrong** and should drop: `dev_tier_usecase_map` (proposal 4
§4's `CREATE TABLE`), `persist_usecase_map.py`, and the `generate-usecase-map`
usecase — all three are now redundant with the query above plus
`usecase.data` already being persisted at registration time. The
fingerprint-cache idea (proposal 4 §5) still applies, but to a much
smaller thing: skip re-running the generator script (not re-registering)
when `standard.yaml`'s usecase list is unchanged.

**What's still genuinely missing and does need a real custom table**:
nothing about the *map* — but §5 below (repo-state audit findings) is
real, standard-owned content with no generic home, exactly the kind of
thing `custom_data_tables` exists for.

## 4. `register_standard` vs `seed_standard` — proposal 2's registration sequence, corrected

Proposal 2 §5 conflated two different operations, confirmed by reading
`seed_standard.rs` directly: **`seed_standard`'s actual job is executing
usecases against a target repo** (it queries `step_script` joins and calls
`run_script_step` — this is runtime orchestration, not metadata
ingestion), not populating lookup tables. Corrected sequence:

1. **Ingest `standard.yaml` into the generic tables** (§1) — whatever MCP
   tool or CLI path does this (not independently confirmed which one in
   this pass — `mcp__samgraha__register_standard` is the best candidate
   given its name, but this needs verifying against
   `crates/mcp`/`crates/registry` source before proposal 2's §5 sequence
   is trusted as-is; flagged as an open question, §7).
2. `mcp__samgraha__validate_standard_metadata` — as proposal 2 §5 already
   said, still correct.
3. `mcp__samgraha__register_standard_globally` — promote to global
   registry, as proposal 2 §5 already said.
4. **`mcp__samgraha__seed_standard`** — this is where proposal 2 was
   wrong to place it: it's not a one-time "seed lookup rows" call, it's
   the actual **run** of a standard's usecases against a specific target
   repo (per `seed_standard.rs`'s signature: `knowledge_db_path, standard,
   repo_root, usecase_filter`) — a per-*evaluation-run* operation, not a
   per-*registration* operation. `pcems_2026`'s own `seeder_script` field
   in `standard.yaml` (`seeder_script: ../script/seeder.py`) is a
   **third, separate thing** — a standard-owned Python script that seeds
   *that standard's own* `custom_data_tables` lookup rows (pcems's
   `academic_domains`, `academic_visualization_types` — data the standard
   itself defines, not samgraha's generic tables). Three distinct
   concepts sharing the word "seed"; proposal 2 blurred them into one
   step.

## 5. Repo-state findings — the one thing that legitimately needs a new `custom_data_tables` entry

Proposal 7 (next) needs somewhere to persist what a propose-time repo scan
finds — per domain, does documentation exist, does it conform, what's
missing. This has no generic home (`domain`/`usecase`/`step` describe the
*standard's* declared shape, not a *specific target repo's* observed
state against that shape) — legitimate custom table, registered the way
`pcems_2026`'s `academic_repos` is: declared twice, for two different
purposes, both confirmed by direct read. `standard.yaml`'s own
`custom_tables:` block (`table_name, purpose, owner_script`) is what gets
ingested into `knowledge.db`'s `custom_data_tables` catalog
(`08-custom_data_tables.sql`) at registration — the record that the table
exists and which script owns it. `standard.metadata.json`'s separate
`custom_tables[]` (`required_columns`) is the schema-conformance contract,
*"validated at global registration time and checked again at activation"*
per `metadata/standard.metadata.schema.json`'s own description. Both
files exist for `pcems_2026` today (confirmed) — `rust_dev` needs the
same pair, not a choice of one.

```sql
-- registered in both standard.yaml's custom_tables: (owner_script) and
-- standard.metadata.json's custom_tables[] (required_columns) — owner_script
-- points at whichever proposal-7 script first writes it
CREATE TABLE IF NOT EXISTS dev_repo_domain_state (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    domain_key    TEXT    NOT NULL,
    tier_number   INTEGER NOT NULL,
    doc_exists    INTEGER NOT NULL CHECK (doc_exists IN (0,1)),
    conforms      INTEGER,             -- NULL until assessed; 0/1 after
    gap_notes     TEXT,                -- what's missing/non-conforming, freeform
    scanned_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_key, scanned_at)
);
```

**Correction (post-implementation)**: this was written before §7 below was
found — not the *only* legitimately new table after all, just the first
one identified. Everything proposals 2 and 4 invented
(`dev_tier_usecase_map`, `dev_schema.py`, a parallel `academic_schema.py`-
style module) is still dropped per §2-§4; §7's findings/score/report
tables are additional real ones, not a reversal of that.

## 6. What proposal 5's `dev_proposal_usecase_scope` becomes

Proposal 5 §4 invented a link table pointing at proposal 4's now-dropped
`dev_tier_usecase_map`. Read `metadata/proposal.schema.json` directly
(the actual validated envelope shape) — the correct shape already exists
and matches what `pcems_2026-proposal-phase-generic-schema-proposal.md`
(archived in `docs/proposal/archive/`) already found for pcems: a proposal
envelope's `phases: [{domain, phase_number, usecases[], steps[], rationale,
git}]` is validated against live `usecase`/`step`/`domain` rows **at
insert time**, then only `title`/`location` persist to the `proposal` row
— exactly the same *"validates... and then discards it"* gap that doc
already diagnosed for pcems. `proposal.usecase_id` is a **singular** FK
(one anchor usecase per proposal row), which doesn't fit a `propose-tierN-*`
usecase that spans every domain in a tier — so proposal 5's link table is
still the right fix, same reasoning pcems's own satellite tables use, just
renamed and corrected to link against real `usecase`/`step`/`domain` ids
instead of the dropped `dev_tier_usecase_map`:

```sql
CREATE TABLE IF NOT EXISTS dev_proposal_phase_scope (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id  INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    phase_number INTEGER NOT NULL,
    domain_id    INTEGER NOT NULL REFERENCES domain(id),
    usecase_id   INTEGER NOT NULL REFERENCES usecase(id),
    step_id      INTEGER REFERENCES step(id)
);
```

Proposal 5 §4 should be read as superseded by this table definition; the
durable-link *reasoning* in proposal 5 §4 was correct, only the target
table name/shape was wrong (pointed at something this proposal now drops).

## 7. Findings/score/report persistence — the DB-backed report pipeline

Gap in the whole 7-proposal series, surfaced by owner review, not caught
in any earlier pass: proposal 3 §3 names `persist-deterministic-findings`
and `persist-semantic-score` as steps, but **no proposal in this series
ever defined a table for either to write to.** Every other `dev_*` table
this series designed (`dev_repo_domain_state`, `dev_proposal_phase_scope`)
is scan/proposal-lifecycle metadata, not audit *content*. pcems has a
whole family for this rust_dev has no equivalent of at all:
`academic_deterministic_findings`, `academic_semantic_runs`,
`academic_semantic_dimension_scores`, `academic_semantic_findings`,
`academic_score_history`, `academic_visualization_types`,
`academic_visualizations`, `academic_report_history` (all confirmed live
in pcems's `standard.metadata.json`, read in full this pass).

**Decided (owner direction)**: proposals stay markdown-only (proposal 5
§6 Q3) — a proposal is a reviewed-once artifact, not a report. But audit
findings and scores are different: they persist to `dev_*` tables as
structured data, get assembled into a markdown report via template (same
mechanism every other rendered artifact in this series uses), and *that*
markdown is the thing a later, out-of-scope step can convert to
HTML/PDF/DOCX — conversion itself isn't designed here, only the fact that
the underlying data already lives in DB, not just in a rendered file, is
what makes that conversion possible later without re-deriving anything.
rust_dev's tables, same shape as pcems's, `dev_*`-prefixed, keyed on
`repo_root` instead of `paper_id` (rust_dev evaluates repos, not papers):

```sql
CREATE TABLE IF NOT EXISTS dev_deterministic_findings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root   TEXT    NOT NULL,
    domain_id   INTEGER NOT NULL REFERENCES domain(id),
    tier_number INTEGER NOT NULL,
    scope       TEXT    NOT NULL CHECK (scope IN ('document','section')),
    run_number  INTEGER NOT NULL,
    verdict     TEXT    NOT NULL,
    findings_json TEXT,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_id, scope, run_number)
);

CREATE TABLE IF NOT EXISTS dev_semantic_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root   TEXT    NOT NULL,
    domain_id   INTEGER NOT NULL REFERENCES domain(id),
    tier_number INTEGER NOT NULL,
    scope       TEXT    NOT NULL CHECK (scope IN ('document','section')),
    model       TEXT    NOT NULL,
    run_number  INTEGER NOT NULL,
    overall_score REAL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE(repo_root, domain_id, scope, run_number)
);

CREATE TABLE IF NOT EXISTS dev_semantic_dimension_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES dev_semantic_runs(id) ON DELETE CASCADE,
    dimension_key TEXT    NOT NULL,
    score         REAL    NOT NULL,
    evidence      TEXT
);

CREATE TABLE IF NOT EXISTS dev_semantic_findings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       INTEGER NOT NULL REFERENCES dev_semantic_runs(id) ON DELETE CASCADE,
    finding_type TEXT    NOT NULL CHECK (finding_type IN ('strength','weakness','recommendation')),
    text         TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS dev_score_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root   TEXT    NOT NULL,
    domain_id   INTEGER NOT NULL REFERENCES domain(id),
    final_score REAL    NOT NULL,
    score_band  TEXT    NOT NULL,
    calculated_at TEXT  NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS dev_visualization_types (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key   TEXT    NOT NULL UNIQUE,
    scope       TEXT    NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS dev_visualizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root     TEXT    NOT NULL,
    chart_type_id INTEGER NOT NULL REFERENCES dev_visualization_types(id),
    file_path     TEXT    NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS dev_report_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_root   TEXT    NOT NULL,
    report_kind TEXT    NOT NULL,
    file_path   TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

**Two new cross-tier usecases** (same shape as `calculate` — no `domain:`
field, spans everything): `render-report` (assembles a markdown report
from `dev_deterministic_findings`/`dev_semantic_*`/`dev_score_history`
via template, writing a `dev_report_history` row) and `render-charts`
(generates chart images from the same tables into `dev_visualizations`,
consumed by `render-report`'s template, mirroring pcems's
`render-charts` → `generate-audit-report` dependency order).

`persist-deterministic-findings` (proposal 3 §3, tier usecases) now has a
real target: `dev_deterministic_findings`. `persist-semantic-score`
(proposal 3 §3) targets `dev_semantic_runs` +
`dev_semantic_dimension_scores` + `dev_semantic_findings` (three inserts,
same run). `calculate` (proposal 3 §3) targets `dev_score_history`.

## 8. Open questions

1. ~~Which MCP tool actually performs `standard.yaml` → generic-table
   ingestion?~~ **Fully resolved**: confirmed by reading `crates/mcp/src/main.rs`
   directly (while implementing proposals 2/3/5 against the live registry)
   — no naming ambiguity after all. `register_standard_globally` (MCP tool)
   only touches `standards.db` (upserts `standard_registry`, runs the
   optional `smoke_test` gate) — its own tool description confirms *"Does
   not register the standard's scripts/prompts/usecases into any repo's
   knowledge.db."* The knowledge.db ingestion (`manifest.scripts`/
   `prompts`/`usecases`/`domains`/`custom_tables` → `register_standard.rs`'s
   `register_standard` function, lines 149-358) is the **same-named**
   `register_standard` MCP tool — *"Activate an already-globally-registered
   standard in a repository... writes local rows into knowledge.db."* Two
   MCP tools, two Rust functions, matching names, matching jobs — the
   ambiguity this question worried about doesn't exist in the real code.
   §1's `seeder_script` bypass caveat still applies on top of this.
2. ~~Does `usecase.data.tier` collide with anything `seed_standard.rs`
   already reads from `data`?~~ **Resolved, confirmed safe**: read
   `seed_standard.rs` directly (line 56) — `data` is deserialized as an
   untyped `serde_json::Value`, then read via `.get("driver")`/
   `.get("depends_on")`, not a typed struct with `deny_unknown_fields`. An
   extra `tier` key is silently ignored by every current reader (grepped
   `crates/services/src` for other `.data` reads — `register_standard.rs`'s
   write side is the only other hit, and it only ever *writes*
   `{driver, depends_on, verify_script}`, never validates against a closed
   set on read). No collision risk, `tier` is a safe key name.
3. **Decided: append-only, and built that way.** `dev_repo_domain_state`
   (§5) — one row per scan (`UNIQUE(repo_root, domain_key, scanned_at)`)
   vs. one row per (repo_root, domain_key) updated in place. Append-only
   matches `academic_deterministic_findings`'s pattern (`run_number`-keyed,
   "latest" queried by `ORDER BY ... DESC LIMIT 1`) and preserves history
   for trend/audit purposes. Proposal 7's `standard.metadata.json` entry
   for this table carries `scanned_at` in `required_columns`, matching
   this decision — not just recommended, already the shape on disk.

## 9. Explicitly out of scope

Actually writing `generate_standard_yaml_tier_data.py` (§3) or any script
— `persist-deterministic-findings`/`persist-semantic-score`/`calculate`/
`render-report`/`render-charts` included; §7 only defines what they write
to and adds the two new usecase names, not their content. Proposal 7's
propose-time repo-scan logic that populates `dev_repo_domain_state` — this
proposal only defines the table it needs. HTML/PDF/DOCX conversion of
`render-report`'s markdown output (§7) — owner's own framing puts this
after the markdown+DB foundation lands, not designed here.
