# base_academic — Template + Visualization Depth Proposal

## 0. Why This Document Exists

`base_academic-usecase-atomicity-proposal.md` (implemented — `plan/usecase/`
now has 121 usecases: 106 per-domain (2 `GENERATED_DOMAINS` loops × 11 +
7 `STRUCTURAL_DOMAINS` loops × 12, `academic_schema.py:663-912`) + 15
whole-pipeline (13 `@_register_usecase` decorators + 2 standalone
`_register_usecase_fn` calls — `section-citations-references`,
`section-budget-fit-total`), each domain
running through a 5-stage content pipeline — generate → cite → enrich →
budget-fit → polish — plus its own deterministic + semantic + plagiarism +
humanize audit chain) changed what the pipeline *produces and tracks*.
`templates/` was not touched by that work and still reflects the pipeline
from before the split — one flat generation skeleton per domain, one flat
score row per domain in every report, four chart types, none of them aware
that a domain's content or audit trail now has stages.

Confirmed on disk today:

- **Every `templates/generation/markdown/{domain}.md` file is a bare
  heading + placeholder skeleton** — e.g. `methodology.md` is 4 headings
  (`Overview` / `Algorithm-Procedure` / `Complexity Analysis` /
  `Architecture`) each holding one `{{ placeholder }}`, `title-and-
  metadata.md` is 4 metadata lines. Nothing in any of the 16 generation
  templates has a slot for citations (4b), enrichment/math-table content
  (4c), or budget metadata (4d) — the three pipeline stages the atomicity
  proposal added between "generate" and "audit." A rendered section today
  looks identical whether or not it went through citation attachment,
  math/table enrichment, or budget fitting — those stages' work is invisible
  in the template output.
- **`templates/generation/html/_master-schema.html` is a single generic
  shell** — `<h1>{{ title }}</h1>` + one `{{{ content }}}` blob. No
  per-domain structure at all; the per-domain markdown templates' richer
  (if still shallow) structure is flattened into one HTML injection point.
- **`templates/report/markdown/semantic.md` and its `.html` twin show one
  score per domain** (`{{#domains}}| {{ domain_key }} | {{ score }} |
  ...{{/domains}}`) — a single number. `academic_semantic_runs.scope`
  already distinguishes `section-part` (per-artifact: citations,
  enrichment, budget-fit — three separate scored runs per domain, per the
  atomicity proposal's §6) from `section-full` (the whole-domain score),
  but the report template has no row, column, or section for `section-
  part` data — it renders as if every domain still gets exactly one score,
  the pre-split shape.
- **`templates/report/markdown/deterministic.md` doesn't distinguish which
  checks ran.** It renders `{{ passed_count }} / {{ total_count }}` per
  domain — a single fraction. The two new checks the atomicity proposal
  added (`citation_marker_present`, `budget_fit_applied` — added to 13 of
  16 `calculation/deterministic/*.yaml` files) are invisible; a reader
  can't tell from the report whether a domain failed on `word_count_in_
  range` or on the new citation check, both collapse into one number.
  Nor does the report have any row for the new document-scope check
  (`academic_deterministic_findings.scope='document'`, whole-paper budget
  total).
- **No report surfaces per-domain pipeline progress.** A domain now passes
  through 9 usecase stages before it's audit-eligible
  (`generate-section-draft-{d}` → `section-citations-{d}` →
  `section-supplementary-content-{d}` → `section-budget-fit-{d}` →
  `deterministic-audit-{d}` → `semantic-audit-{d}` →
  `plagiarism-forensic-audit-{d}` → `humanize-deterministic-{d}` →
  `humanize-semantic-{d}`, each independently checkable via
  `academic_schema.usecase_status()`). Nothing renders this — a reader
  checking "is `methodology` done" has no view of it short of running 9
  separate verify scripts.
- **`academic_humanize_passes` has no report presence at all.** Neither
  `deterministic.md`/`.html` nor `semantic.md`/`.html` mentions humanize —
  not pass counts, not the `pass_kind` (`deterministic`/`semantic`) split
  the atomicity proposal added, not risk flags.
- **`academic_section_citations` (new table, atomicity proposal §4b) has
  no report presence.** A reader can't see how many citations a domain has,
  which are `in-repo` vs `literature`, or whether the `references` domain's
  collation actually pulled from all 11 other domains.
- **Only 4 chart types are seeded**
  (`script/schema-init/init_schema.py:29-34`): `domain-score-bar`,
  `deterministic-findings-heatmap`, `cross-section-score`, `document-
  review-score`. All four are coarse — one bar/cell per domain or one
  number per paper. None chart per-stage data: no citation counts, no
  budget-fit word-count-vs-range, no section-part-vs-full score
  comparison, no humanize pass counts, no pipeline-progress view across
  the 9 per-domain stages.
- **`generate_audit_report.py`'s two data-gathering functions
  (`_get_domain_data`, `_get_plag_data`) don't query the new tables/columns**
  — `academic_section_citations`, `academic_humanize_passes.pass_kind`,
  `academic_semantic_runs.scope='section-part'`, or `usecase_status()` for
  per-domain pipeline progress. The report templates couldn't render this
  data even if the templates had slots for it — the Python side doesn't
  fetch it either.
- **`_get_domain_data()`'s existing semantic-score query has a latent
  scope-ambiguity bug** (`generate_audit_report.py:43-48`):
  `SELECT overall_score FROM academic_semantic_runs WHERE paper_id=?
  AND domain_id=? ORDER BY run_number DESC LIMIT 1` doesn't filter by
  `scope`. `run_number` auto-increments per `(paper, domain, scope,
  model)` (`academic_schema.py:414`), so once `section-part` runs exist,
  a part-level run can carry the highest `run_number` for that
  `(paper_id, domain_id)` and get returned as the domain's primary score
  instead of the `section-full` run. Pre-existing, but §4a's full/part
  split (below) makes it load-bearing — needs `AND scope='section-full'`
  added to this query as part of this proposal's §7 changes.

## 1. Scope

`base_academic/templates/**`, the two report-generation scripts that
populate them (`script/render-audit-report/generate_audit_report.py`,
`render_charts.py`), and the visualization-type catalog
(`academic_visualization_types`, seeded in `init_schema.py`). Doesn't touch
`plan/usecase/*.md` (already atomic, prior proposal), `calculation/**`
(rubrics/rules — already extended for the new checks, prior proposal),
or the pipeline/orchestrator (`run_full_workflow.py`,
`script/common/academic_schema.py` — already updated for the per-domain
split).

## 2. Generation Templates (Markdown) — Add Pipeline-Stage Slots

Each of the 16 `templates/generation/markdown/{domain}.md` files gains
three new sections, appended after the domain's existing content headings
(not replacing them — the existing `Overview`/`Algorithm`/etc. headings in
`methodology.md` stay, this is additive):

```markdown
## References
{{#citations}}
[{{ index }}] {{ citation }}
{{/citations}}

<!-- budget: {{ word_count }} / {{ budget_min }}-{{ budget_max }} words -->
```

- **`## References`** (rendered only if `{{#citations}}` is non-empty —
  mustache section, not a hardcoded heading every domain gets) — makes 4b's
  work visible in the rendered section instead of only queryable via
  `academic_section_citations`. For domains that get external-literature
  citations too (`CITE_CONTEXT_DOMAINS` — `introduction`, `related-work`,
  `discussion`), the same block renders both `in-repo` and `literature`
  rows undifferentiated by design — a reader doesn't need the source-kind
  distinction in the paper itself, only in the audit report (§4).
- **Budget HTML comment** (`<!-- budget: ... -->`) — invisible in rendered
  output (both markdown preview and the eventual PDF/DOCX render strip
  HTML comments), but greppable in the raw `.md` file for anyone debugging
  why a section is short/long. Sourced from 4d's `check-word-budget`
  output, not re-computed by the template layer.
- **No explicit slot for 4c's enrichment output** — enrichment content
  (equations, tables, diagram references) is woven *into* the domain's
  existing headings by `section-enrichment.md`'s prompt (that's the whole
  point of 4c, per the atomicity proposal — it edits the existing draft
  in place, it doesn't append a new section). Nothing to add here beyond
  what 4a's headings already provide room for.

`references.md` itself (the domain whose entire content *is* a citation
list, per 4b's collation) is the one file that doesn't need the new `##
References` block appended — it already renders as a citation list at
the top level. Leave `references.md` as-is.

## 3. Generation Templates (HTML) — Per-Domain Structure, Not One Blob

`_master-schema.html`'s single `{{{ content }}}` injection point stays
(it's correct — the final paper is one continuous document, per
`assemble-final-document.py`'s concatenation), but the *markdown→HTML*
conversion step gains two things the raw `{{{ content }}}` blob doesn't
have today:

- **A citation-numbering pass** — the `## References` blocks §2 adds
  render as `[1]`, `[2]`, ... per-domain today (each domain's own citation
  list starts at 1). The HTML render needs a whole-document renumbering
  pass so citation `[3]` in `methodology` doesn't collide with citation
  `[3]` in `results` — this is a `render-paper` (6c) concern, not a
  template concern, so it's named here as a dependency this proposal
  creates but `render-paper`'s own script must resolve, not something
  `_master-schema.html` itself can fix by template structure alone.
- **`<!-- budget: ... -->` HTML comments strip silently** — confirmed
  behavior of every markdown→HTML converter in use here (pandoc,
  standard CommonMark), no template change needed, noted so nobody adds
  redundant stripping logic later.

No structural change to `_master-schema.html` itself — it already does
the one thing it needs to (wrap `{{{ content }}}`), and the atomicity
proposal's new stages don't change the final paper's HTML shape, only
what's inside the concatenated markdown feeding it.

## 4. Report Templates — Section-Part/Full Split, Pipeline Progress, Humanize, Citations

Four new sections across `semantic.md`/`.html`, `deterministic.md`/`.html`,
and one new report file pair (`pipeline-progress.md`/`.html`) not created
by the template-restructure proposal because the pipeline wasn't atomic
yet when that proposal shipped.

### 4a. `semantic.md`/`.html` — split `Per-Domain Scores` into parts + full

Replace the single flat table with two:

```markdown
## Per-Domain Full Scores

| Domain | Full Score | Band | Strengths | Weaknesses |
|--------|-----------|------|-----------|------------|
{{#domains_full}}
| {{ domain_key }} | {{ score }} | {{ band }} | {{ strengths }} | {{ weaknesses }} |
{{/domains_full}}

## Per-Domain Part Scores

| Domain | Citations | Enrichment | Budget-Fit |
|--------|-----------|------------|------------|
{{#domains_parts}}
| {{ domain_key }} | {{ citations_score }} | {{ enrichment_score }} | {{ budget_fit_score }} |
{{/domains_parts}}
```

`domains_full` sources `scope='section-full'` runs (today's existing
query, renamed context key, plus the `AND scope='section-full'` fix
noted in §0). `domains_parts` is new — sources `scope='section-part'`
runs grouped by `part_kind` (the atomicity proposal's §6
`semantic-audit-part.md` prompt's three rubrics: citations, enrichment,
budget-fit) pivoted into one row per domain, three columns, via
conditional aggregation over each domain's latest `run_number` per
`part_kind`:

```sql
SELECT domain_id,
  MAX(CASE WHEN part_kind='citations'  THEN overall_score END) AS citations_score,
  MAX(CASE WHEN part_kind='enrichment' THEN overall_score END) AS enrichment_score,
  MAX(CASE WHEN part_kind='budget-fit' THEN overall_score END) AS budget_fit_score
FROM (
  SELECT domain_id, part_kind, overall_score,
         ROW_NUMBER() OVER (PARTITION BY domain_id, part_kind ORDER BY run_number DESC) AS rn
  FROM academic_semantic_runs
  WHERE paper_id=? AND scope='section-part'
) latest
WHERE rn = 1
GROUP BY domain_id;
```

Requires the `part_kind` column on `academic_semantic_runs` to group by
(checked — **not present today**, §6 below).

### 4b. `deterministic.md`/`.html` — per-check breakdown, not one fraction

```markdown
## Per-Domain Check Breakdown

| Domain | word_count_in_range | citation_marker_present | budget_fit_applied | Other | Verdict |
|--------|---------------------|--------------------------|---------------------|-------|---------|
{{#domains}}
| {{ domain_key }} | {{ wc_status }} | {{ citation_status }} | {{ budget_status }} | {{ other_summary }} | {{ verdict }} |
{{/domains}}

## Whole-Paper Check

| Check | Status |
|-------|--------|
| total_word_count_in_range | {{ document_budget_status }} |
```

Sources `academic_deterministic_findings.findings` (already a JSON array
of `{check_id, rule, passed, detail}` per §0's schema comment — the data
exists, only the template and `_get_domain_data()`'s projection of it are
missing) plus the new `scope='document'` row (atomicity proposal §6) for
the whole-paper total-budget check.

### 4c. New — `pipeline-progress.md`/`.html`

```markdown
# Pipeline Progress — {{ title }}

| Domain | Generate | Cite | Enrich | Budget | Det-Audit | Sem-Audit | Plagiarism | Humanize-Det | Humanize-Sem |
|--------|----------|------|--------|--------|-----------|-----------|------------|---------------|---------------|
{{#domains}}
| {{ domain_key }} | {{ generate }} | {{ cite }} | {{ enrich }} | {{ budget }} | {{ det_audit }} | {{ sem_audit }} | {{ plagiarism }} | {{ humanize_det }} | {{ humanize_sem }} |
{{/domains}}

## Whole-Pipeline

| Stage | Status |
|-------|--------|
| section-citations-references (collation) | {{ collation_status }} |
| section-budget-fit-total | {{ budget_total_status }} |
| document-narrative-polish | {{ polish_status }} |
| cross-section-semantic-audit | {{ cross_section_status }} |
| document-semantic-audit | {{ document_status }} |
```

Each per-domain cell is a ✓/✗/— rendered from
`academic_schema.usecase_status(conn, paper_id, f"{stage}-{domain}")` —
the same predicate the 106 per-domain verify scripts already call,
reused here for a report view instead of a CLI PASS/FAIL exit code. This
is the report the "reader checking is methodology done" gap (§0) needs —
a 12×9 grid instead of running 106 individual verify scripts (some cells
render `—` for domains that skip a stage, e.g. `references` has no
`generate`/`cite` cell of its own — it's `GENERATED_DOMAINS`-only).

### 4d. `deterministic.md` gains a Humanize section

Placed in `deterministic.md` only, not duplicated into `semantic.md` —
humanize is audit-adjacent (`academic_humanize_passes` is triggered by
the deterministic audit result), and `deterministic.md` already carries
the trigger-side data (§4b). One partial, one location, no cross-file
duplication to keep in sync.

```markdown
## Humanize Passes

| Domain | Flagged | Deterministic Pass | Semantic Pass | Risk Flags |
|--------|---------|---------------------|-----------------|------------|
{{#humanize}}
| {{ domain_key }} | {{ flagged }} | {{ det_pass }} | {{ sem_pass }} | {{ risk_flags }} |
{{/humanize}}
```

Sources `academic_humanize_passes` grouped by `pass_kind`
(`deterministic`/`semantic` — atomicity proposal §7's schema addition).
Domains never flagged by `plagiarism-forensic-audit-{domain}` render
`flagged=No` and blank pass columns — same "still runs, trivially passes,
renders as a row" pattern the per-domain humanize usecases themselves use.

## 5. Visualization — New Chart Types

Six new chart types, seeded alongside the existing four in
`init_schema.py` (`academic_visualization_types`, no schema change — same
`scope IN ('per_domain','per_paper','global')` constraint already covers
every shape below):

| `chart_key` | `scope` | What it charts | Backs |
|---|---|---|---|
| `pipeline-progress-matrix` | `per_paper` | 12×9 heatmap, domains × stages, PASS(green)/FAIL(red)/pending(grey) | §4c's report |
| `section-part-score-comparison` | `per_domain` | Grouped bar per domain: citations / enrichment / budget-fit / full scores side by side | §4a |
| `citation-count-bar` | `per_domain` | Bar per domain, in-repo vs literature citation counts stacked | New — `academic_section_citations` had no chart |
| `budget-fit-gauge` | `per_domain` | Per-domain word count vs its configured `[min,max]`, gauge/bullet style | §4b's per-check breakdown, visual form |
| `whole-paper-budget-gauge` | `per_paper` | Total word count vs `calculation/summary/paper-budget.yaml`'s range | `section-budget-fit-total`'s own check, visual form |
| `humanize-pass-chart` | `per_domain` | Bar per domain: deterministic-only resolved vs needed-semantic-pass count | §4d |

`render_charts.py` gains 6 new functions (`_pipeline_progress_matrix()`,
`_section_part_score_comparison()`, `_citation_count_bar()`, `_budget_fit_
gauge()`, `_whole_paper_budget_gauge()`, `_humanize_pass_chart()`),
matching the existing 4 functions' shape (`(plt, ..., output_path)` →
saves a PNG, same `matplotlib` `Agg` backend already in use — no new
dependency).

## 6. Schema Change Needed — `academic_semantic_runs` Gains `part_kind`

§4a's per-domain part-score pivot (citations / enrichment / budget-fit as
three columns) needs a column to group by that doesn't exist today —
`scope='section-part'` rows (atomicity proposal §6) don't currently record
*which* part they scored, only that they're a part-level run:

```sql
-- schema/09-academic_semantic_runs.sql
part_kind TEXT CHECK (part_kind IN ('citations','enrichment','budget-fit') OR part_kind IS NULL),
-- NULL for scope IN ('section-full','cross-section','document') — only
-- 'section-part' rows populate this.
```

`persist_domain_semantic_score.py` gains two arguments: `--scope`
(optional, default `"section-full"` — matches `upsert_semantic_score()`'s
existing default, `academic_schema.py:412`, so every current caller stays
unchanged) and `--part-kind` (optional, default `None`, only meaningful
when `--scope section-part`). 5a's part-level audit script passes
`--scope section-full` for whole-domain runs and `--scope section-part
--part-kind {citations|enrichment|budget-fit}` for part runs — today the
script has neither flag and always relies on the `upsert_semantic_score()`
default, so it cannot currently write a `section-part` row at all. No
migration needed, same standing precedent (no deployed rows).

## 7. New/Changed Files — Consolidated

**Changed generation templates (16 files):** every
`templates/generation/markdown/{domain}.md` gains the `## References` +
budget-comment block from §2, except `references.md` (unchanged, §2's
carve-out).

**Changed report templates (6 files):**
`templates/report/markdown/semantic.md` + `.html` (§4a),
`templates/report/markdown/deterministic.md` + `.html` (§4b + §4d).

**New report templates (2 files):**
`templates/report/markdown/pipeline-progress.md`,
`templates/report/html/pipeline-progress.html` (§4c).

**Changed scripts:**

| File | Change |
|---|---|
| `script/render-audit-report/generate_audit_report.py` | `_get_domain_data()`'s existing semantic-score query gains `AND scope='section-full'` (fixes §0's scope-ambiguity bug); extended to query `academic_section_citations`, `academic_semantic_runs` grouped by `part_kind` (§4a's pivot), `academic_humanize_passes` grouped by `pass_kind`; new `_get_pipeline_progress_data()` calling `usecase_status()` per (stage, domain) for §4c |
| `script/render-audit-report/render_charts.py` | 6 new chart functions (§5) |
| `script/semantic-audit/persist_domain_semantic_score.py` | New optional `--scope` (default `section-full`) and `--part-kind` (default `None`) arguments (§6) |
| `script/schema-init/init_schema.py` | 6 new `academic_visualization_types` seed rows (§5) |

**Schema:** `schema/09-academic_semantic_runs.sql` gains `part_kind` (§6).

## 8. Open Questions

- **Citation renumbering at render time** (§3) — whether `render-paper`
  (6c)'s existing `assemble-final-document.py` gains the renumbering pass
  itself, or a new script is inserted between assembly and HTML render.
  Named as a dependency this proposal creates, not resolved here — out of
  this proposal's scope (`render-paper`'s internals weren't touched by
  the atomicity proposal either).
- **Whether `pipeline-progress.md`/`.html` is generated per-run or only
  on-demand** — every other report in `templates/report/` is generated by
  `render-audit-report` (6b) as part of the standard pipeline run. Given
  ~106 `usecase_status()` calls per generation (12 domains × 9 stages,
  minus the 2 stages `references` skips as a non-`GENERATED_DOMAINS`
  domain), this is cheap (all SQLite reads, no LLM calls) but not free —
  leaning
  toward "always generated, same as the other three reports," not locked
  in here.

## 9. Explicitly Out of Scope

The 16 generation templates' actual edited content beyond the one worked
example (§2's `## References` + budget-comment block — applies uniformly,
not written out per-file), the 6 new report template files' full markup
beyond the fragments shown (§4), the 6 new chart functions' actual
matplotlib code, `_get_domain_data()`/`_get_pipeline_progress_data()`'s
actual query implementations, and `persist_domain_semantic_score.py`'s
`--part-kind` plumbing. This proposal specifies each template's new
sections, each chart's data source and scope, and the one schema column
needed — not the finished template markup or script code.
