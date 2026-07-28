# pcems_2026 — Proposal-Phase System: Gaps + Generic-Schema Alignment

## 0. Context

Merges two prior passes into one document (both archived under
`docs/proposal/archive/`):
1. An understanding-check of the `propose-*` system against a stated model
   ("per-domain phase-wise plan, considering usecase/step, deterministic or
   semantic, analysing the repo, rendered via `templates/`") — found one
   blocking bug and two model mismatches.
2. Owner decision on the resulting architecture question: use samgraha's
   generic `proposal` table (`schema/knowledge/15-proposal.sql`) as the
   anchor row, and add meaning via satellite tables (git detail, usecase/
   step alignment, repo-analysis grounding) instead of duplicating the same
   data in a standalone pcems-only table.

`.samgraha/knowledge.db` has zero rows in both `academic_proposals` and
`proposal` today — this is a clean-slate redesign, not a migration.

---

## 1. What already exists (traced against live code)

The `propose-*` pipeline is real and already domain-scoped — not something
being built from scratch:

| Piece | Status | Where |
|---|---|---|
| 4 propose usecases, not 3 | Built | `standard.yaml:561-631` — `propose-generation`, `propose-audit`, `propose-report`, `propose-fix` |
| Each phase gathers domain-level context | Built | `gather_proposal_context.py` — `_gather_generation_context`, `_gather_audit_context`, `_gather_report_context`, `_gather_fix_context` |
| Persist + append-only history + redraft/rejection tracking | Built | `persist_proposal.py`, `academic_proposals` table (`is_latest`, `status`, `iteration`, `scope_domain_id`) |
| Approval gate | Built | `approve_proposal.py`, completion predicates `_make_proposal_predicate` (`academic_schema.py:1116-1132`) for generation/audit/report; `propose-fix` intentionally has no whole-paper predicate (domain-scoped, checked per-domain — `academic_schema.py:1109-1113`) |
| Render to markdown/html | **Broken** | `render_proposal.py:28-31,92` — see §2 |

---

## 2. Gap 1 (blocking) — `templates/proposal/` is empty

`render_proposal.py:28-31` reads templates from:
```
templates/proposal/markdown/{phase}.md
templates/proposal/html/{phase}.html
```
Both directories **do exist** (`templates/proposal/markdown/`,
`templates/proposal/html/`) — corrected from an earlier pass of this doc
that claimed they didn't exist at all. They are empty: 0 files in either.
Same practical effect (render writes nothing), different cause (empty dir,
not a missing one) — worth getting right since it changes what "fix" means
(create files in an existing location, not `mkdir` first).
`_load_template` (`render_proposal.py:34-39`) returns `None` when the file
is missing, and `main()` just skips that format — **no error, no
exception**, `write_envelope(status="ok", rendered=[])`. Every `propose-*`
run today completes "successfully" while writing zero files, for all 4
phases, every time. `standard.metadata.json` only declares one
`role: "proposal"` template name (`"generation-proposal"`) with no physical
file behind it either — the metadata-level template catalog and the
physical chevron files `render_proposal.py` actually loads are two
different things, and neither exists for audit/fix/report.

The three prompts (`propose/audit-proposal.md`, `fix-proposal.md`,
`generation-proposal.md`) all explicitly instruct the model to match
`templates/proposal/markdown/{phase}.md`'s shape — so the prompts were
written assuming these files would exist, and they were never created.
This is the actual, concrete, fixable gap — a missing-file problem, not a
design problem. Folded into the fix order (§6, phase 5) below.

---

## 3. Gap 2 — proposals don't consult usecase/step at all (today)

The stated model was "considering usecase and step, step can be
deterministic or semantic." Traced `gather_proposal_context.py` end to end:
none of its four `_gather_*_context` functions query samgraha's `usecase`
or `step` tables. Generation/audit context is built from `academic_domains`,
`calculation/generation/{domain}.yaml` rule counts, `audit/semantic/document/
{domain}.md` rubric counts, and `academic_narratives` stage. This is
domain-and-rule-file granularity, not usecase-and-step granularity.

samgraha's own generic `proposal` table and its `phases:
[{domain, usecases[], steps[]}]` schema (`step_execution.rs:142-155`,
`metadata_validate.rs`) was, until this proposal, wired but **unused** —
`persist_proposal.py`/`render_proposal.py` never emitted the top-level
`"proposal"` envelope key that triggers it. §4-§7 below close this gap for
real, per the owner's architecture decision.

---

## 4. Gap 3 — "analyse the repo" already happens, but earlier, not at propose time

Generation-phase context reads already-persisted
`academic_cross_module_analysis` rows (novelty/gaps/mathematics/
architecture — `gather_proposal_context.py:96-102`). Repo analysis itself
runs earlier, in the `*-analysis` usecases (`novelty-analysis`,
`gap-analysis`, `mathematics-analysis`, `diagram-architecture-analysis`),
well before `propose-generation` runs. Audit/fix/report phases don't
reference repo analysis at all. §7.3 below gives generation-phase grounding
a durable, queryable link (`academic_proposal_analysis_ref`) instead of the
current copy-into-JSON-blob approach — it does not add fresh repo analysis
at propose time, since that would duplicate the `*-analysis` usecases.

---

## 5. What samgraha's generic schema already gives for free

Traced `schema/knowledge/*.sql` + `metadata/proposal.schema.json` +
`step_execution.rs:288-360` (`validate_proposal_envelope`) — more is built
here than it looked from the outside:

| Need | Already exists | Where |
|---|---|---|
| Git commit details on a proposal | Yes, via `proposal.execution_id -> execution.git_detail_id -> git_detail(commit_sha, branch, dirty)` | `07-execution.sql`, `09-git_detail.sql` |
| Usecase/step alignment analysis | Schema-validated already: `phases[].usecases[]` + `phases[].steps[]` (step **IDs**, not names) are cross-checked against the real `usecase`/`step`/`domain` tables at insert time — usecase must belong to the phase's domain, steps must belong to one of the phase's usecases | `step_execution.rs:305-360` |
| A phase-wise, per-domain plan | Literally the `phases: [{domain, phase_number, usecases[], steps[], rationale}]` array shape | `proposal.schema.json:17-74` |
| Anchor row (title/location/status) | `proposal` table itself | `15-proposal.sql` |

**The gap:** samgraha validates `phases[]` against live data and then
**discards it** — only `title`/`location` get written to the `proposal`
row (`step_execution.rs:157-160`). Nothing durable remembers which
usecases/steps a given proposal covered, or what analysis it grounded in.
pcems_2026 needs its own satellite tables to keep that — §6.

---

## 6. New tables (all pcems custom_data_tables, all FK'd to `proposal.id`)

Replaces `academic_proposals` (single wide table) with three narrow ones,
each holding only what the generic schema has no place for.

### 6.1 `academic_proposal_review` — decision workflow + content
The one piece with no generic equivalent: samgraha's `proposal.status` is a
3-state `draft/final/archived` enum with no redraft/rejection-reason
concept. This table holds the real state machine — **correction**: the old
`academic_proposals` DDL (`schema/22-academic_proposals.sql:15-43`) never
had `title` or `location` columns (those live only on the generic
`proposal` table; an earlier pass of this doc wrongly implied they were
being dropped from here). What's actually dropped versus the old table:
`commit_sha` (superseded by `proposal.execution_id -> execution.git_detail_id
-> git_detail`) and `metadata` (renamed to `computed_context`, same JSON
blob role). `decided_at` is added — `approve_proposal.py:44` writes it and
the old table had it; missing it here would silently break approval
timestamping:

```sql
CREATE TABLE academic_proposal_review (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id      INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    paper_id         INTEGER NOT NULL REFERENCES academic_papers(id),
    phase            TEXT    NOT NULL CHECK (phase IN ('generation','audit','fix','report')),
    scope_domain_id  INTEGER REFERENCES academic_domains(id),  -- fix only
    review_status    TEXT    NOT NULL DEFAULT 'pending'
                     CHECK (review_status IN ('pending','approved','rejected','superseded')),
    source           TEXT    NOT NULL DEFAULT '',  -- pipeline | user-request
    user_comment     TEXT    NOT NULL DEFAULT '',
    iteration        INTEGER NOT NULL DEFAULT 0,
    is_latest        INTEGER NOT NULL DEFAULT 1,
    summary          TEXT    NOT NULL DEFAULT '',
    content_md       TEXT    NOT NULL DEFAULT '',
    computed_context TEXT,   -- JSON: audit rule/rubric counts, fix triggering_findings — see §6.4
    created_at       TEXT    NOT NULL DEFAULT (datetime('now')),
    decided_at       TEXT
);
```
`paper_id` stays here (not on generic `proposal`) since samgraha has no
concept of "paper" — that's pcems domain data.

### 6.2 `academic_proposal_scope` — usecase/step alignment (durable)
One row per (domain, usecase, step) the proposal's validated `phases[]`
covered — the part samgraha validates but doesn't keep:

```sql
CREATE TABLE academic_proposal_scope (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id  INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    domain_id    INTEGER NOT NULL REFERENCES domain(id),     -- samgraha's generic domain, not academic_domains
    usecase_id   INTEGER NOT NULL REFERENCES usecase(id),
    step_id      INTEGER NOT NULL REFERENCES step(id),
    UNIQUE(proposal_id, step_id)
);
```
Joining `step_id -> step.kind` answers "how many deterministic vs semantic
steps does this proposal round touch" without pcems tracking `kind` itself
— it's already on samgraha's `step` row.

### 6.3 `academic_proposal_analysis_ref` — repo-analysis grounding
Generation-phase only: which `academic_cross_module_analysis` rows
(novelty/gaps/mathematics/architecture) this proposal's content grounded
in, instead of copying the analysis text into a JSON blob:

```sql
CREATE TABLE academic_proposal_analysis_ref (
    id                       INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id              INTEGER NOT NULL REFERENCES proposal(id) ON DELETE CASCADE,
    cross_module_analysis_id INTEGER NOT NULL REFERENCES academic_cross_module_analysis(id),
    UNIQUE(proposal_id, cross_module_analysis_id)
);
```

### 6.4 What's deliberately NOT normalized
Audit-phase per-domain rule/rubric counts (`det_rule_count`,
`rubric_criterion_count`, etc.) and fix-phase `triggering_findings` stay as
the `computed_context` JSON blob on `academic_proposal_review`. These are
point-in-time snapshot numbers rendered once into `content_md` and never
queried back out relationally — normalizing them into more tables buys no
real query value. Deliberate scope limit, not an oversight.

---

## 7. The plumbing problem: getting `proposal.id` back to pcems

`run_script_step` (`step_execution.rs:74-182`) inserts into `proposal`
**after** the calling script (`persist-proposal`) has already exited — the
script's own envelope can request the insert (by including a top-level
`"proposal": {...}` key) but can never see the resulting `proposal.id`,
since samgraha computes it after the script process is gone. A later step
that needs to write `academic_proposal_scope`/`_review` rows against that
`proposal.id` has to look it back up.

**No Rust change needed.** `proposal` has no direct pointer back to "which
step run produced me" by ID, but it does have `execution_id`, and
`execution` has `step_id` — so the just-inserted row is the one matching
this standard's `persist-proposal` step's most recent execution:
```sql
SELECT p.id FROM proposal p
JOIN execution e ON e.id = p.execution_id
WHERE e.step_id = ? -- persist-proposal's step id for this usecase
ORDER BY e.id DESC LIMIT 1
```
Safe because the pipeline runs one paper's steps sequentially — no
concurrent `persist-proposal` executions for the same step_id in practice.
This lookup becomes a new function in `academic_schema.py`
(`get_latest_proposal_id(conn, step_id)`), used by the *next* step in the
chain to attach `academic_proposal_review`/`_scope`/`_analysis_ref` rows.

---

## 8. Wiring changes

### 8.1 `standard.yaml` — new step per `propose-*` usecase
**All four** `propose-*` usecases gain a linking step — including
`propose-report`, resolving the ambiguity in an earlier pass of this doc.
Reason: `_make_proposal_predicate` (`academic_schema.py:1116-1132`) checks
`status='approved'` for `generation`/`audit`/`report` alike — report's own
usecase-completion gate depends on an approved row exactly like the other
two, so report needs an `academic_proposal_review` row written just as much
as generation/audit do, even though it has no semantic step and no
domain/usecase scope to record:
```yaml
- order: 4   # 5 for generation/audit/fix (after their semantic step); report has no semantic step, so this is order 4 there
  kind: deterministic
  description: "Link proposal to its usecase/step/analysis scope"
  script: link-proposal-scope
```
For `propose-report`: `link_proposal_scope.py` still writes the
`academic_proposal_review` row (needed for the approval predicate), but
skips `academic_proposal_scope`/`_analysis_ref` entirely — report isn't
domain/usecase-scoped in the same sense, and forcing a synthetic
`phases[]` entry just to satisfy the schema's `minItems: 1` would be
inventing structure that doesn't reflect anything real. **Open item**: the
generic `proposal` envelope's `phases[]` is `required, minItems: 1`
(`proposal.schema.json:76`) — report's `persist_proposal.py` call still has
to supply *some* non-empty phases array to get a `proposal` row inserted at
all. Recommend one synthetic phase referencing the render usecases already
in play (`render-charts`, `render-audit-report`, `render-paper`) as
`usecases[]`, with `steps[]` pulled from those usecases' real step IDs —
this is at least true (those usecases really do run this phase), just not
domain-scoped the way generation/audit phases are. Confirm this reading
against `render-*` usecases' actual `domain_id` (likely `NULL`, whole-
document usecases) before implementing — `phases[].domain` is required and
must resolve against the `domain` table, so a whole-document usecase needs
*some* domain value; check what `diagram-architecture-analysis` and other
whole-document usecases use for their `domain_id` today, if anything, and
mirror that.

### 8.2 `persist_proposal.py` — rewritten
Instead of `INSERT INTO academic_proposals`, this now:
1. Builds `phases[]` from `computed_context.domains` using a static
   phase→usecase-name-suffix map (see §8.2.1 — this is the piece
   `gather_proposal_context.py` does **not** provide, resolved here
   instead of adding usecase/step queries to that script):
   one phase per domain, `usecases: [the domain's phase-relevant usecase
   name(s)]`, `steps: [step IDs queried from the `step`/`usecase` tables
   for those usecase names]`, `rationale` from `summary`.
2. Emits `write_envelope(..., proposal={"title": ..., "location": ...,
   "phases": phases})` — this is the top-level key `run_script_step`
   reads to do the generic `INSERT INTO proposal`.
3. **Deletes the existing `conn.execute("UPDATE academic_proposals ...")`
   and `conn.execute("INSERT INTO academic_proposals ...")` calls
   entirely** (`persist_proposal.py:31-51` today) — if both the old insert
   and the new envelope key ran, every proposal round would produce two
   rows in two different tables, one of them (`academic_proposals`) never
   read by anything after this rewrite ships. The append-only/supersede
   write moves entirely to the new `link-proposal-scope` step (§8.3), once
   `proposal_id` is resolvable. This script now only builds and emits the
   envelope.

#### 8.2.1 Phase → usecase-name mapping (new, in `persist_proposal.py`)
`gather_proposal_context.py`'s `domains[]` gives domain keys, not usecase
names — that mapping doesn't exist anywhere today and has to be added.
Static per-phase suffix lists, expanded against each domain in
`computed_context.domains`:
```python
_PHASE_USECASE_SUFFIXES = {
    "generation": ["generate-section-draft-{domain}"],
    "audit": ["section-citations-{domain}", "section-enrichment-{domain}",
              "section-budget-fit-{domain}", "deterministic-audit-{domain}",
              "semantic-audit-{domain}", "plagiarism-forensic-audit-{domain}"],
    "fix": ["generate-section-draft-{domain}"],  # the usecase a fix redrafts
}
```
For each domain key + suffix, format the usecase name, then
`SELECT id FROM step WHERE usecase_id = (SELECT id FROM usecase WHERE
standard=? AND name=?) ORDER BY step_order` to collect that usecase's step
IDs. `fix` only expands for `target_domain` (single domain, not the whole
`domains[]` list) since it's domain-scoped.

### 8.3 New script: `link_proposal_scope.py`
```
Expected --in payload: {paper_id, phase, scope_domain_id (optional),
  step_id (this usecase's own persist-proposal step id, known statically
  per phase), review: {status, source, user_comment, iteration, summary,
  content_md, computed_context}, analysis_ids: [cross_module_analysis ids
  grounded in, generation-phase only],
  domain_usecase_steps: [{domain_key, usecase_name, step_id}] (the same
  expansion persist_proposal.py computed for phases[] — passed through
  here rather than re-derived, so both steps agree on exactly one
  computation)}
```
1. `proposal_id = get_latest_proposal_id(conn, step_id)`
2. Insert `academic_proposal_review` row — append-only, with the
   supersede-previous-pending logic the old `persist_proposal.py` had
   (flip prior `is_latest=1` row to `is_latest=0`, `status='superseded'`
   only if it was still `pending`)
3. For each `{domain_key, usecase_name, step_id}` in
   `domain_usecase_steps`: resolve `domain_key -> domain_id` via
   `SELECT id FROM domain WHERE standard=? AND key=?` (samgraha's generic
   `domain` table, seeded by `seeder.py:529-534` — **not**
   `academic_domains`, a different table with a different id space) and
   `usecase_name -> usecase_id` via `SELECT id FROM usecase WHERE
   standard=? AND name=?`, then insert one `academic_proposal_scope` row
   per `(domain_id, usecase_id, step_id)` triple. This key-to-id
   resolution isn't optional bookkeeping — the FK columns are integers,
   the payload only has strings, and no other step in this chain has
   already done the lookup.
4. Insert `academic_proposal_analysis_ref` rows if `analysis_ids` given
5. For `phase == "fix"`: `scope_domain_id` in the payload is already the
   resolved `academic_domains.id` (per `gather_proposal_context.py`'s own
   docstring — `request_fix.py` resolves the key to an id itself,
   exact-match-or-error, before this chain ever starts). No additional
   resolution needed for the `academic_proposal_review.scope_domain_id`
   column — pass it straight through. It's only the `domain_usecase_steps`
   entries above that need the *generic* `domain` table's id, since that's
   a different id space than `academic_domains`.

### 8.4 `render_proposal.py` — read path changes
Currently reads `academic_proposals` directly. Now reads
`academic_proposal_review` joined through `proposal_id` (still keyed by
`paper_id, phase, scope_domain_id, is_latest=1`). Template context (`ctx`)
shape is unchanged from the reader's perspective — same
`content_md`/`summary`/`computed_context` fields, just sourced from the new
table. **This is also where the template-file gap from §2 gets fixed**:
create `templates/proposal/markdown/{generation,audit,fix,report}.md`
(+ html) matching each prompt's documented shape — sequenced into this same
rewrite since `render_proposal.py` is being touched anyway. Template
content itself needs to mirror each prompt's `## Input`/`## Output Format`
section (`prompt/propose/{generation,audit,fix}-proposal.md`) — e.g.
`generation.md` needs a domains-table loop plus
`novelty_summary`/`gaps_summary`/`math_summary`/`diagram_summary`
placeholders; `audit.md` needs `models[]` plus the same domains-table shape
with rubric/rule counts; `fix.md` needs `target_domain`,
`triggering_findings[]`, `triggering_finding_count`. Write these against
the prompts' documented input shape directly, not invented fresh.

### 8.5 `academic_schema.py` — predicate updates
`_make_proposal_predicate` (line 1116-1132) currently queries
`academic_proposals` directly for `status='approved'`. Update to join
through `academic_proposal_review` (same query shape, new table name,
`review_status='approved'` instead of `status='approved'`).

### 8.6 `standard.metadata.json` — custom_tables + templates catalog
Current `custom_tables` entry for `academic_proposals`
(`standard.metadata.json:104-107`) has `required_columns: ["id", "paper_id",
"phase", "status", "title"]` — `title` was already wrong (the real DDL
never had it, per §6.1's correction); this entry needs replacing, not
patching. Add three entries for the new tables with their real required
columns (`proposal_id`, `paper_id`, `phase`, `review_status`, etc. per
§6.1-6.3's DDL — no `title`/`location`, those are the generic `proposal`
table's job). Separately, `templates` currently lists only
`generation-proposal` (role: proposal) and `audit-report` (role: report)
— add `audit-proposal`, `fix-proposal`, `report-proposal` as templates
too. Note `validate_proposal_template_consistency`
(`metadata_validate.rs:85-136`) requires **exactly one** template with
`role: "proposal"` — adding 3 more `role: "proposal"` entries would fail
that check. Keep the 4 phase templates as `role: "generation"` (or another
non-"proposal" role) in the metadata catalog; the `role: "proposal"` /
`proposal_template` field is a different, coarser concept (which single
template represents "the" proposal shape for validation purposes) than
"which 4 files does `render_proposal.py` load by phase name" — don't
conflate them when editing this file.

---

## 9. Proposed Fix Order

`academic_proposals` (the old table) stays in place, untouched, through
phases 1-7 below — it's simply stopped being written to once phase 3
lands, and nothing reads it after phase 4/7 land. It is only physically
dropped in phase 8, after everything that used to depend on it (approve,
render, the completion predicate) has been cut over and verified. Dropping
it in phase 1 instead would break `approve_proposal.py`/`render_proposal.py`
for the entire window between phase 1 and phase 7 — avoid that ordering.

| Phase | What | Depends on |
|---|---|---|
| 1 | Add 3 new tables (`academic_proposal_review`, `_scope`, `_analysis_ref`) to `academic_schema.py::ensure_schema`. Leave `academic_proposals` table/DDL in place for now (see note above) | None |
| 2 | Write `get_latest_proposal_id()` helper in `academic_schema.py` | Phase 1 |
| 3 | Rewrite `persist_proposal.py`: add the phase→usecase-name mapping (§8.2.1), build `phases[]`, emit the generic `proposal` envelope key, **delete** its existing `academic_proposals` UPDATE/INSERT calls | Phase 1 |
| 4 | Write new `link_proposal_scope.py`, add as a step in `standard.yaml` for **all four** `propose-*` usecases (report included — see §8.1 for its trimmed write + the open `phases[]` question to resolve before coding it) | Phases 2-3 |
| 5 | Update `render_proposal.py` to read `academic_proposal_review` instead of `academic_proposals`; write the 4 template files (markdown + html) against each prompt's documented input shape (§8.4) — closes §2's blocking bug | Phase 1 |
| 6 | Update `_make_proposal_predicate` in `academic_schema.py` to join through `academic_proposal_review` (`review_status='approved'`) | Phase 1 |
| 7 | Update `approve_proposal.py` to read/write `academic_proposal_review` (`review_status`, `decided_at` — both now present on the new table per §6.1's correction) instead of `academic_proposals` (`status`, `decided_at`) | Phases 1, 4 (needs `proposal_id` resolvable) |
| 8 | Drop `academic_proposals` table + its `standard.metadata.json` `custom_tables` entry; add the 3 new tables' entries there instead (§8.6); update `templates` catalog with the 4 phase templates under a non-`"proposal"` role (§8.6) | Phases 1-7 |
| 9 | Full re-verify: run one full `propose-generation` cycle against a test paper, confirm `proposal` + all 3 satellite tables populate correctly, confirm rendered files land in `docs/paper/paper-{id}/proposal/`, confirm `approve_proposal.py` flips `review_status` and the completion predicate sees it | Phases 1-8 |
