# base_academic — Usecase Granularity + Document-Level Audit Proposal

## 0. Why This Document Exists

Scoped to `base_academic/plan/usecase/*.md` and the audit stage's scope
coverage. Doesn't touch `templates/` (already restructured, see
`base_academic-template-restructure-proposal.md`) or the archived
data-pipeline proposal's remaining open items.

Confirmed gaps on disk today:

- **Zero verify scripts exist.** `find base_academic -iname '*verify*'`
  returns nothing. Compare `python_hackathon/script/verify/` — 10 files
  (`uc1_init.py` ... `uc7_pdf.py`), each a standalone PASS/FAIL CLI that
  queries the DB directly and exits non-zero on failure. Every
  `base_academic` usecase's "Completion criteria" section is prose nobody
  checks — a workflow report saying a usecase ran is the only evidence
  that exists.
- **No usecase file has a "Verify script:" line.** `python_hackathon`'s
  usecase docs do — e.g. `python_hackathon/plan/usecase/5-markdown-visualization.md:18`
  names `verify_usecase_5_markdown_charts.py` explicitly. Every
  `base_academic/plan/usecase/*.md` file stops at "Completion criteria" /
  "Rule" with no pointer to anything that checks those criteria.
- **No usecase file has an explicit "Depends on" field.** Dependency is
  buried in free prose inside "**Rule**": e.g.
  `5a-semantic-audit.md`'s "Runs after deterministic-audit... Only runs for
  domains that passed deterministic audit" is a sentence, not a check —
  nothing in `deterministic_audit.py` or `persist_domain_semantic_score.py`
  queries the other's completion state before proceeding.
- **No completeness gate between section-by-section generation and
  document assembly.** `6b-render-paper.md`'s (renumbered to
  `6c-render-paper.md` by this proposal — §6) Inputs list "Each domain's
  latest `academic_narratives` row" but nothing verifies all 12 structural
  domains (+ conditional literature-review) actually have one before
  `assemble-final-document.py` concatenates them — a partially-generated
  paper would render silently with missing sections.
- **No cross-section semantic audit exists.** `5a-semantic-audit.md` scores
  each domain independently against its own rubric; nothing checks
  consistency *between* domains (abstract promising a result the results
  section doesn't contain, terminology drift, a claim in introduction
  contradicted in discussion).
- **No whole-document semantic audit exists.** Audit stops at per-domain
  scores rolled up arithmetically by `calculate.py`
  (`calculation/summary/final_score.yaml`'s two-bucket weights). Nobody
  reviews the assembled document the way a reader or reviewer actually
  would — as one continuous document, not 12 independent domain scores
  averaged together.
- **Schema can't represent a non-section-scoped semantic run today.**
  `academic_semantic_runs.domain_id` is `NOT NULL`
  (`schema/09-academic_semantic_runs.sql:13`) — there's no row shape for a
  cross-section or whole-document run. `academic_score_history` already
  solved this exact problem for scores (`domain_id` is nullable,
  `schema/15-academic_score_history.sql:12`, "NULL means whole-paper") —
  `academic_semantic_runs` is the one table in this set that didn't get the
  same treatment.
- **`calculation/summary/final_score.yaml` has no slot for a paper-level
  score.** It's a strict 2-bucket formula
  (`final_score = 0.5*semantic_document + 0.5*deterministic_document`) —
  both inputs are per-domain. There's nowhere for a `scope='cross-section'`
  or `scope='document'` run (§5) to feed into the number `calculate.py`
  writes, even after the schema change lands.
- **`templates/report/html/summary.html` never got rewritten for the
  3-way report split.** It's still the pre-split combined file verbatim
  (moved, not edited, during the template-restructure proposal) — a single
  per-domain table with a `Plagiarism` column and a `{{#charts}}` block,
  while `templates/report/markdown/summary.md` (its markdown sibling,
  written fresh for the split) is a rollup-with-links shape with **no**
  chart section at all. The two "same report, two formats" templates
  currently disagree with each other structurally.

## 1. What "Usecase" Means Here, and Why It Stays One File

Not proposing a 4-tier epic/story/task directory split — that adds
structure nobody asked for over what's actually broken. The request is
that a usecase file read like a **checkable task**, not an idea: it already
has Script/Inputs/Action/Completion-criteria/Rule headings
(`0-classify-repo.md` is a reasonable example of the current shape) — what
it's missing is three fields, retrofitted onto every existing file, plus a
real script backing the one that was always aspirational:

| Field | Today | Proposed |
|---|---|---|
| **Depends on** | Buried in a "Rule:" sentence, unchecked | Explicit field, naming the upstream usecase(s) by name |
| **Completion criteria** | Prose bullets | Unchanged heading, but each bullet must be phrased as a literal SQL predicate — the acceptance criteria a script can evaluate, not aspiration |
| **Verify script** | Doesn't exist | `script/verify/uc{N}_{name}.py` — real file, PASS/FAIL exit code, same shape as `python_hackathon/script/verify/*.py` |

One shared predicate per usecase, used twice — not duplicated logic in two
places:

```python
# script/common/academic_schema.py — new function per usecase's dependency
def usecase_status(conn, paper_id, usecase_name):
    """Returns (complete: bool, detail: list[str]) for a usecase's own
    completion criteria. Same predicate backs both the CLI verify script
    and the runtime dependency gate below — one source of truth."""
```

`script/verify/uc{N}_{name}.py` is a thin CLI wrapper around
`usecase_status()`. The dependent usecase's first script step calls the
*same* function against its upstream usecase's name and hard-fails
(`write_envelope(status="error", ...)`) if incomplete — this is the literal
"each usecase checks its dependent usecase is completed" requirement,
turning today's "Rule: Runs after X" sentence into an enforced
precondition instead of an ordering hint the orchestrator happens to
follow.

## 2. Retrofit Example — `5a-semantic-audit.md`

Before (current file, unchanged fields shown for contrast) →

```markdown
**Rule**: Runs after deterministic-audit. Only runs for domains that
passed deterministic audit (deterministic FAIL short-circuits semantic —
§2.5 of proposal). Accumulates indefinitely.
```

After:

```markdown
# Use-case 5a — Semantic Audit

**Depends on**: `deterministic-audit` (per domain — this usecase's first
step calls `usecase_status(conn, paper_id, "deterministic-audit")` scoped
to the current domain; hard-fails if that domain's latest
`academic_deterministic_findings.verdict` isn't `PASS`)

**Script**: Per-domain triad — `gather-domain-evidence` (mode=`audit`) →
`semantic-audit` (prompt) → `persist-domain-semantic-score`

**Inputs**: [unchanged]

**Action**: [unchanged]

**Completion criteria** (checked by `verify script`, not aspirational):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE paper_id=? AND scope='section'`
  >= 1 per structural domain that has a `PASS` deterministic verdict
- Full bar: every configured model has scored every eligible domain

**Verify script**: `script/verify/uc5a_semantic_audit.py --standard base_academic --paper-id <id>`
- Queries `academic_deterministic_findings` for eligible domains (PASS verdict)
- Confirms >= 1 `academic_semantic_runs` row per eligible domain
- Exits 1 with a per-domain list on any gap

**Rule**: Accumulates indefinitely — re-running adds `run_number`s, never
overwrites.
```

Same retrofit (Depends on / rephrased Completion criteria / Verify script
line) applies to all 13 existing files. Not reproduced file-by-file here —
the shape above is the template; §6 lists the dependency edge for each.

## 3. Section-by-Section Generation → Completeness Gate → Document Review → Scaffolding

This is the actual pipeline shape the request asks for, made explicit
rather than implied by file adjacency:

```
4-assemble-paper-structure   (generate, per-section — unchanged)
        │
        ▼  [[GATE]] every structural domain has an academic_narratives row
        │            + conditional literature-review done for cite_context domains
        │
5 + 5a  (deterministic + semantic audit, per-section — unchanged, both exist today)
        │
        ▼  [[GATE]] every domain PASS on both deterministic and semantic
        │
5d      (cross-section semantic audit — NEW, §4)
5e      (whole-document semantic audit — NEW, §4)
        │
        ▼  [[GATE]] cross-section AND document-level PASS
        │
        ├──────────────────────────────────────────────┐
        ▼                                               ▼
6c (render-paper — scaffolding,          calculate  (score aggregation — now also
    gate added to Depends on)                        reads scope='cross-section'/'document'
                                                       runs, §7)
                                                              │
                                                              ▼
                                                       6a-render-charts (visualization —
                                                       now also charts the two new
                                                       scopes, §7)
                                                              │
                                                              ▼
                                                       6b-render-audit-report (report
                                                       assembly — only starts once
                                                       BOTH calculate and render-charts
                                                       are done; it populates templates
                                                       from scores AND embeds chart
                                                       images, so neither can be partial)
```

**Renumbering.** Today's `6a-render-audit-report.md` / `6b-render-paper.md`
become `6b-render-audit-report.md` / `6c-render-paper.md` — `6a` is freed
up for the new `render-charts` usecase (`6a-render-charts.md`) that used
to be an undocumented sub-step bundled inside the old `6a`'s Script line.
This keeps the render-track lettering in actual execution order
(`6a` charts → `6b` audit report → `6c` paper) instead of leaving a gap
number (`6a0`) ahead of an existing `6a`.

Calculation and visualization both finish **before** report rendering
starts, and in that order — `render-audit-report`'s templates (§7) embed
chart images (`{{#charts}}`) that don't exist until `render-charts` runs,
and `render-charts`'s score-trend/domain-score charts read
`academic_score_history` rows that don't exist until `calculate` runs.
Today's `6a-render-audit-report.md` (renumbered `6b-render-audit-report.md`)
bundles `render_charts.py` into the *same* "Script:" line as
`generate-audit-report.py` as if they're one step — this proposal splits
them into two explicit sequential dependencies (§6) so a report render
can't silently proceed with stale or missing charts.

`6c-render-paper.md` (renumbered from `6b-render-paper.md`) gains:

```markdown
**Depends on**: `assemble-paper-structure` (all structural domains
drafted), `deterministic-audit` + `semantic-audit` (all domains PASS),
`cross-section-semantic-audit`, `document-semantic-audit` (both PASS) —
`assemble-final-document.py`'s first action calls `usecase_status()` for
each and hard-fails, listing which domains/audits are still outstanding,
rather than concatenating a partial document silently.
```

The render-audit-report track (now `6b-render-audit-report.md`) is not
gated by `5d`/`5e` — it's explicitly independent of the paper-rendering
track and doesn't wait on cross-section/document review. It *is* gated on
`6a-render-charts` (previous paragraph) — that dependency is new, not a
carry-over from today's file, which didn't distinguish it as a separate
usecase at all.

## 4. Two New Usecases — Cross-Section and Whole-Document Semantic Audit

Both are semantic-only, per the request (deterministic checks stay
section-scoped — §8 flags whole-document deterministic checks as a
possible follow-up, not proposed here). Both reuse
`academic_semantic_runs` with the schema change in §5, rather than a new
table — same table, a `scope` column distinguishes the three kinds of run.

```markdown
# Use-case 5d — Cross-Section Semantic Audit

**Depends on**: `deterministic-audit` + `semantic-audit` (every structural
domain PASS — this is a review of already-individually-passing sections
for consistency, not a substitute for per-section scoring)

**Script**: `gather-cross-section-evidence` (new, det) → `cross-section-semantic-audit`
(new prompt) → `persist-domain-semantic-score` (extended, §5, to accept
`scope='cross-section'` with `domain_id=NULL`)

**Inputs**:
- Every structural domain's latest `academic_narratives` draft, concatenated in `_master-schema.yaml` order
- New rubric: `calculation/semantic/cross-section.yaml` — terminology
  consistency, claim-vs-evidence alignment across sections (e.g. abstract
  claims vs results section numbers), narrative-arc coherence

**Action**: Score the *set* of sections together for consistency issues no
single-domain audit can see — each domain already passed its own rubric;
this catches contradictions between domains.

**Completion criteria**:
- >= 1 `academic_semantic_runs` row with `scope='cross-section'`, `domain_id=NULL`, per paper per pass

**Verify script**: `script/verify/uc5d_cross_section_audit.py --standard base_academic --paper-id <id>`

**Rule**: Runs once all domains individually PASS (§3's gate). Re-runs on
any domain's content changing (a targeted rewrite or humanize pass
invalidates the last cross-section run — re-run before proceeding to 5e).
```

```markdown
# Use-case 5e — Document Semantic Audit

**Depends on**: `cross-section-semantic-audit` (PASS)

**Script**: `gather-document-evidence` (new, det — concatenates all
sections per `_master-schema.yaml` order, same concatenation
`assemble-final-document.py` does, run here *before* rendering rather than
duplicating it there) → `document-semantic-audit` (new prompt) →
`persist-domain-semantic-score` (extended, §5, `scope='document'`, `domain_id=NULL`)

**Inputs**:
- Full concatenated document text
- New rubric: `calculation/semantic/document-review.yaml` — reads as one
  document: does the introduction's stated gap get closed by the
  conclusion, does methodology actually support the results shown, overall
  readability/flow a per-section score can't capture

**Action**: One holistic pass over the whole assembled document — the
"full document review" step the request names explicitly, distinct from
both per-section audit (5/5a) and cross-section consistency (5d).

**Completion criteria**:
- >= 1 `academic_semantic_runs` row with `scope='document'`, `domain_id=NULL`, per paper per pass

**Verify script**: `script/verify/uc5e_document_audit.py --standard base_academic --paper-id <id>`

**Rule**: Runs after 5d PASS. Gates `render-paper` (§3) — this is the last
check before `assemble-final-document.py`'s scaffolding.
```

## 5. Schema Change — `academic_semantic_runs` Gains a `scope` Column

Mirrors `academic_score_history`'s already-established
nullable-`domain_id`-means-non-section pattern (§0), rather than inventing
a new table for something this table's sibling already solved:

```sql
-- schema/09-academic_semantic_runs.sql
CREATE TABLE IF NOT EXISTS academic_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,  -- now nullable
    scope         TEXT    NOT NULL DEFAULT 'section'
                  CHECK (scope IN ('section','cross-section','document')),   -- NEW
    model         TEXT    NOT NULL,
    run_number    INTEGER NOT NULL DEFAULT 1,
    overall_score REAL    NOT NULL,
    reasoning     TEXT    NOT NULL DEFAULT '',
    computed_against TEXT,  -- NEW, NULL for scope='section' — see below
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, scope, model, run_number)
);
```

`domain_id` stays `NOT NULL` in practice for `scope='section'` rows (every
existing call site already passes a domain) — the column only goes `NULL`
for the two new scopes, same convention `academic_score_history` already
uses. `persist_domain_semantic_score.py` gains a `--scope` argument
(default `section`, backward compatible with every existing caller).

No migration or backfill needed — `base_academic` has no deployed rows yet
(this proposal precedes any of it shipping), so `schema/09` is edited in
place with the final shape rather than written as an `ALTER TABLE` path
for existing data.

**Staleness tracking (`computed_against`), resolved here rather than left
open.** A `5d`/`5e` run needs to know if it's still valid after a
downstream targeted-rewrite or humanize pass changes a domain's draft.
`computed_against` stores a JSON snapshot at compute time —
`{"abstract": 2, "introduction": 1, ...}` — one entry per structural
domain, value is that domain's `academic_narratives.iteration` the run was
computed against. `NULL` for `scope='section'` rows (they only ever depend
on their own domain, already covered by `run_number` ordering). Before
`document-semantic-audit` (or its own re-run) trusts a `cross-section`/
`document` row as current, it compares `computed_against` against every
domain's live `MAX(iteration)` — any mismatch means that domain changed
since the snapshot, and the row is stale (treated as if it doesn't exist
for gating purposes, forcing a re-run). One JSON column, no new table,
same effort as the schema change already proposed.

## 6. Dependency Graph — All Usecases

| Usecase | Depends on | Verify script (new) |
|---|---|---|
| `schema-init` | — | `uc0_schema_init.py` |
| `classify-repo` | `schema-init` | `uc0b_classify_repo.py` |
| `novelty-analysis` | `classify-repo` (HAS_DOCS) | `uc1_novelty.py` |
| `gap-analysis` | `classify-repo` (HAS_DOCS) | `uc2_gaps.py` |
| `mathematics-and-diagrams` | `classify-repo` (HAS_DOCS) | `uc3_math_diagrams.py` |
| `assemble-paper-structure` | `novelty-analysis` + `gap-analysis` + `mathematics-and-diagrams` | `uc4_assemble.py` |
| `deterministic-audit` | `assemble-paper-structure` (per domain) | `uc5_det_audit.py` |
| `semantic-audit` | `deterministic-audit` (per domain, PASS) | `uc5a_semantic_audit.py` |
| `plagiarism-forensic-audit` | `assemble-paper-structure` (per domain) | `uc5b_plagiarism.py` |
| `humanize` | `plagiarism-forensic-audit` (FAIL after targeted rewrite) | `uc5c_humanize.py` |
| `cross-section-semantic-audit` **(new)** | `deterministic-audit` + `semantic-audit` (all domains PASS) | `uc5d_cross_section_audit.py` |
| `document-semantic-audit` **(new)** | `cross-section-semantic-audit` (PASS) | `uc5e_document_audit.py` |
| `calculate` | `semantic-audit` + `deterministic-audit` (all domains scored) + `cross-section-semantic-audit` + `document-semantic-audit` (§7) | `uc6_calculate.py` |
| `render-charts` **(new — file `6a-render-charts.md`, promoted out of the old `6a`'s Script line)** | `calculate` | `uc6a_render_charts.py` |
| `render-audit-report` (renumbered — file `6b-render-audit-report.md`) | `render-charts` | `uc6b_render_audit_report.py` |
| `render-paper` (renumbered — file `6c-render-paper.md`) | `document-semantic-audit` (PASS) | `uc6c_render_paper.py` |

13 existing usecases get the retrofit (§2) — 12 already have a
`plan/usecase/*.md` file; `schema-init` is registered in `standard.yaml`
but has no usecase doc yet, so it gets one authored for the first time as
part of this retrofit, not just edited. 3 new usecase files get authored
fresh: `5d-cross-section-semantic-audit.md`, `5e-document-semantic-audit.md`,
and `6a-render-charts.md` (§3's renumbering — the old `6a`/`6b` render-track
files shift to `6b`/`6c`, letters stay in execution order rather than
leaving a `6a0` gap ahead of an existing `6a`). 16 verify scripts get
written total (13 retrofit + 3 new) — none exist today.

## 7. Additional Scripts, Templates, and Schema This Proposal Needs

§4-§6 named some of these inline; consolidated here so nothing gets missed
during implementation.

**New scripts:**

| File | Purpose |
|---|---|
| `script/cross-section-audit/gather_cross_section_evidence.py` | Concatenate all structural domains' latest drafts, per `_master-schema.yaml` order |
| `script/document-audit/gather_document_evidence.py` | Same concatenation, reused verbatim by `assemble-final-document.py`'s pre-render step (§3) — one function, two callers, not two implementations |
| `script/common/academic_schema.py` — `usecase_status()` | §1's shared predicate function, 13 usecase-specific bodies |
| `script/render-audit-report/render_charts.py` — 2 new functions | `_cross_section_score_chart()`, `_document_review_score_chart()` (schema below) |
| `script/calculate/calculate.py` — formula change | Reads `scope='cross-section'`/`'document'` runs; writes their contribution into the whole-paper `academic_score_history` row (`domain_id IS NULL`) only — per-domain rows are unaffected, since 5d/5e don't score individual domains |
| 16 verify scripts | §6's table |

**New prompts:**

| File | Purpose |
|---|---|
| `prompt/cross-section-audit/cross-section-semantic-audit.md` | 5d's semantic step |
| `prompt/document-audit/document-semantic-audit.md` | 5e's semantic step |

**New/changed templates:**

| File | Change |
|---|---|
| `calculation/semantic/cross-section.yaml` | New rubric (§4) |
| `calculation/semantic/document-review.yaml` | New rubric (§4) |
| `calculation/summary/final_score.yaml` | Gains a 3rd, whole-paper-only input: `{ name: document_coherence, weight: ... }`, sourced from the mean of the latest `cross-section` + `document` scope runs — applies only to the `domain_id IS NULL` whole-paper `academic_score_history` row, per-domain rows keep the existing 2-bucket formula unchanged |
| `templates/report/markdown/semantic.md` + `.html` | New "Cross-Section & Document Scores" section below the existing per-domain table — 2 rows (`cross-section`, `document`), not one row per domain |
| `templates/report/markdown/summary.md` | New `## Charts` section with a `{{#charts}}` block (currently absent — §0) |
| `templates/report/html/summary.html` | Rewritten to match `summary.md`'s rollup-with-links shape instead of the stale pre-split combined-table version (§0) |

**Schema:**

- §5's `academic_semantic_runs.scope` column (already specified).
- `academic_visualization_types` seed data gains 2 rows:
  `cross-section-score` and `document-review-score`, both `scope='per_paper'`
  — fits the existing `CHECK (scope IN ('per_domain','per_paper','global'))`
  (`schema/16-academic_visualization_types.sql:9`) with no constraint
  change needed, since a cross-section/document score is inherently a
  whole-paper quantity.
- No change needed to `academic_deterministic_findings` or
  `academic_report_history` — neither is scope-widened by this proposal
  (§8's open question on whole-document deterministic checks is the only
  place that table could need this later).

## 8. Open Questions

- **Whole-document deterministic checks** (total word/reference count
  against a journal's limit, duplicate-paragraph detection across
  sections) — same schema shape (§5's pattern) would extend to
  `academic_deterministic_findings` if a concrete system needs it. Not
  proposed now — the request named semantic scope for cross-section/
  document explicitly, deterministic stays section-only until a system
  actually needs the whole-document version.
- ~~Re-run invalidation~~ — resolved in §5 (`computed_against` column).
- **`usecase_status()`'s per-usecase predicate bodies** — §1 specifies the
  function's shape and that it's shared between verify script and runtime
  gate; the 13 individual SQL predicates themselves are the bulk of the
  actual implementation work and aren't written out here beyond the
  worked `5a` example (§2).

## 9. Explicitly Out of Scope

The 13 retrofitted usecase file bodies beyond the one worked example
(§2), the 3 new usecase files' full text (`5d`, `5e`, `6a-render-charts.md`),
the 2 new prompts' content (`cross-section-semantic-audit.md`,
`document-semantic-audit.md`), the 2 new rubric YAMLs
(`calculation/semantic/cross-section.yaml`, `document-review.yaml`), the
actual code for `gather_cross_section_evidence.py`,
`gather_document_evidence.py`, `render_charts.py`'s 2 new chart functions,
`calculate.py`'s formula change, and the rewritten `summary.html`/extended
`semantic.md`/`.html` markup (§7) — and all 16 verify scripts' actual
assertions. This proposal specifies each file's location, dependency, data
source, and completion-predicate shape, not its finished text.
