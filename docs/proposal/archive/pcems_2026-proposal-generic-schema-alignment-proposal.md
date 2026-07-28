# pcems_2026 — Align `propose-*` onto samgraha's Generic `proposal` Table

## 0. Context

Supersedes the "keep `academic_proposals`" recommendation in
`pcems_2026-proposal-phase-template-gaps-proposal.md` §5 — owner decision:
use samgraha's generic `proposal` table (`schema/knowledge/15-proposal.sql`)
as the anchor row, and build the extra meaning (decision workflow, git
provenance, usecase/step alignment, repo-analysis grounding) as satellite
tables hanging off `proposal.id`, instead of one wide pcems-only table
duplicating what the generic schema already has a place for.

`.samgraha/knowledge.db` has zero rows in both `academic_proposals` and
`proposal` today — this is a clean-slate redesign, not a migration.

The blocking bug from the prior doc (§2 there — `templates/proposal/`
directory doesn't exist, `render_proposal.py` silently writes 0 files every
run) still applies and is folded into this proposal's fix order, since the
template shape changes slightly with this redesign (see §4).

---

## 1. What samgraha's generic schema already gives for free

Traced `schema/knowledge/*.sql` + `metadata/proposal.schema.json` +
`step_execution.rs:288-360` (`validate_proposal_envelope`) end to end —
this is more built than it looked from the outside:

| Need (from the owner's ask) | Already exists | Where |
|---|---|---|
| Git commit details on a proposal | Yes, via `proposal.execution_id -> execution.git_detail_id -> git_detail(commit_sha, branch, dirty)` | `07-execution.sql`, `09-git_detail.sql` |
| Usecase/step alignment analysis | Schema-validated already: `proposal.schema.json`'s `phases[].usecases[]` + `phases[].steps[]` (step **IDs**, not names) are cross-checked against the real `usecase`/`step`/`domain` tables at insert time — usecase must belong to the phase's domain, steps must belong to one of the phase's usecases | `step_execution.rs:305-360` |
| A phase-wise, per-domain plan | Literally the `phases: [{domain, phase_number, usecases[], steps[], rationale}]` array shape | `proposal.schema.json:17-74` |
| Anchor row (title/location/status) | `proposal` table itself | `15-proposal.sql` |

**The gap:** samgraha validates `phases[]` against live data and then
**discards it** — only `title`/`location` get written to the `proposal`
row (`step_execution.rs:157-160`). Nothing durable remembers which
usecases/steps a given proposal covered, or what analysis it grounded in.
pcems_2026 needs its own satellite tables to keep that.

---

## 2. New tables (all pcems custom_data_tables, all FK'd to `proposal.id`)

Replaces `academic_proposals` (single wide table) with three narrow ones,
each holding only what the generic schema has no place for:

### 2.1 `academic_proposal_review` — decision workflow + content
The one piece with no generic equivalent: samgraha's `proposal.status` is a
3-state `draft/final/archived` enum with no redraft/rejection-reason
concept. This table holds the real state machine, unchanged from the old
`academic_proposals` shape minus the columns now covered elsewhere
(`title`, `location`, `commit_sha` — dropped, read via the `proposal` FK
chain instead):

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
    created_at       TEXT    NOT NULL DEFAULT (datetime('now'))
);
```
`paper_id` stays here (not on generic `proposal`) since samgraha has no
concept of "paper" — that's pcems domain data.

### 2.2 `academic_proposal_scope` — usecase/step alignment (durable)
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

### 2.3 `academic_proposal_analysis_ref` — repo-analysis grounding
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

### 2.4 What's deliberately NOT normalized
Audit-phase per-domain rule/rubric counts (`det_rule_count`,
`rubric_criterion_count`, etc.) and fix-phase `triggering_findings` stay as
a JSON blob on `academic_proposal_review` (add one `computed_context TEXT`
column back). These are point-in-time snapshot numbers rendered once into
`content_md` and never queried back out relationally — normalizing them
into more tables buys no real query value. Flagging this as a deliberate
scope limit, not an oversight.

---

## 3. The plumbing problem: getting `proposal.id` back to pcems

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

## 4. Wiring changes

### 4.1 `standard.yaml` — new step per `propose-*` usecase
Each `propose-{generation,audit,fix}` usecase gains a 5th step (report
stays 3-step, unchanged, still deterministic-only):
```yaml
- order: 5
  kind: deterministic
  description: "Link proposal to its usecase/step/analysis scope"
  script: link-proposal-scope
```

### 4.2 `persist_proposal.py` — rewritten
Instead of `INSERT INTO academic_proposals`, this now:
1. Builds `phases[]` from `computed_context.domains` — one phase per
   domain, `usecases: [the domain's phase-relevant usecase name(s)]`,
   `steps: [step IDs queried from the `step`/`usecase` tables for those
   usecase names]`, `rationale` from `summary`.
2. Emits `write_envelope(..., proposal={"title": ..., "location": ...,
   "phases": phases})` — this is the top-level key `run_script_step`
   reads to do the generic `INSERT INTO proposal`.
3. Also inserts the pcems-specific row into `academic_proposal_review`
   (content_md, summary, review_status='pending', phase, scope_domain_id,
   user_comment, iteration, is_latest flip logic — same append-only /
   supersede-previous-pending logic the old script had) — but this row's
   `proposal_id` FK isn't known yet (see §3), so it's inserted with
   `proposal_id = NULL` and back-filled by the new `link-proposal-scope`
   step, OR (simpler) this insert moves entirely into the new
   `link-proposal-scope` step, once `proposal_id` is resolved. **Recommend
   the latter** — keeps `persist_proposal.py` focused on building the
   envelope, and `link_proposal_scope.py` (new script) does all the writes
   that need `proposal_id`.

### 4.3 New script: `link_proposal_scope.py`
```
Expected --in payload: {paper_id, phase, scope_domain_id (optional),
  step_id (this usecase's own persist-proposal step id, known statically
  per phase — hardcoded per phase or looked up by usecase+step name),
  review: {status, source, user_comment, iteration, summary, content_md,
  computed_context}, analysis_ids: [cross_module_analysis ids grounded in,
  generation-phase only]}
```
1. `proposal_id = get_latest_proposal_id(conn, step_id)`
2. Insert `academic_proposal_review` row (with the supersede-previous-
   pending logic moved here from old `persist_proposal.py`)
3. Insert `academic_proposal_scope` rows — one per (domain_id, usecase_id,
   step_id) the phases[] envelope declared (re-derive from the same
   domains/usecases list `persist_proposal.py` built, not by re-reading the
   envelope — simplest to pass it through in the payload)
4. Insert `academic_proposal_analysis_ref` rows if `analysis_ids` given

### 4.4 `render_proposal.py` — read path changes
Currently reads `academic_proposals` directly. Now reads
`academic_proposal_review` joined through `proposal_id` (still keyed by
`paper_id, phase, scope_domain_id, is_latest=1` the same way). Template
context (`ctx`) shape is unchanged from the reader's perspective — same
`content_md`/`summary`/`computed_context` fields, just sourced from the new
table. **This is also where the still-open template-file gap from the
prior doc gets fixed**: create
`templates/proposal/markdown/{generation,audit,fix,report}.md` (+ html)
matching each prompt's documented shape — unchanged requirement, just
sequenced into this same rewrite since `render_proposal.py` is being
touched anyway.

### 4.5 `academic_schema.py` — predicate updates
`_make_proposal_predicate` (line 1116-1132) currently queries
`academic_proposals` directly for `status='approved'`. Update to join
through `academic_proposal_review` (same query shape, new table name).

---

## 5. Proposed Fix Order

| Phase | What | Depends on |
|---|---|---|
| 1 | Add 3 new tables to `academic_schema.py::ensure_schema` + `standard.metadata.json`'s `custom_tables` (drop `academic_proposals` entry, add the 3 new ones) | None |
| 2 | Write `get_latest_proposal_id()` helper in `academic_schema.py` | Phase 1 |
| 3 | Rewrite `persist_proposal.py` to emit the generic `proposal` envelope key (phases[] built from `computed_context.domains`) | Phase 1 |
| 4 | Write new `link_proposal_scope.py`, add as step 5 in `standard.yaml` for generation/audit/fix (report unaffected) | Phases 2-3 |
| 5 | Update `render_proposal.py` to read `academic_proposal_review` instead of `academic_proposals`; create the 4 missing template files (markdown + html) | Phase 1 |
| 6 | Update `_make_proposal_predicate` in `academic_schema.py` to join through the new table | Phase 1 |
| 7 | Update `approve_proposal.py` (writes `review_status`, not `status`, into `academic_proposal_review`) | Phase 1 |
| 8 | Full re-verify: run one full `propose-generation` cycle against a test paper, confirm `proposal` + all 3 satellite tables populate correctly, confirm rendered files land in `docs/paper/paper-{id}/proposal/` | Phases 1-7 |

Not yet checked: `approve_proposal.py`'s current column writes — needs
reading before phase 7 lands, flagged here rather than assumed.
