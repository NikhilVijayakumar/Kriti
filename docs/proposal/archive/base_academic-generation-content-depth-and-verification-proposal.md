# base_academic — Generation Template Depth + Calculation-Driven Content Minimums + Self-Verification Proposal

## 0. Why This Document Exists

The report-granularity proposal (implemented) fixed the *audit/report*
side — one template per domain per finding-kind, aggregation, commit-
gated reruns. It explicitly left `templates/generation/**` untouched
(its own §1: "Doesn't touch the generation templates... prior proposal's
territory"). That "prior proposal" — `base_academic-template-
visualization-depth-proposal.md` — is the one that actually touched
generation templates, and what it shipped there has three concrete
problems, plus the generation pipeline has no way to catch a missing
citation/table/diagram/formula before the paper reaches audit.

Confirmed on disk today:

- **`templates/generation/html/_master-schema.html` is still one
  generic shell**, unchanged since the visualization-depth proposal
  explicitly declined to touch it (its §3: "No structural change to
  `_master-schema.html` itself... the final paper's HTML shape [doesn't
  change], only what's inside the concatenated markdown"). Confirmed
  today: `<h1>{{ title }}</h1>` + one `{{{ content }}}` blob, no
  per-domain structure. The markdown generation templates
  (`templates/generation/markdown/{domain}.md`) each have real per-domain
  heading structure (`methodology.md`: `Overview`/`Algorithm-Procedure`/
  `Complexity Analysis`/`Architecture`) — the HTML side has never had an
  equivalent. **This is spec-level, not a live-script fix**: the script
  that would actually render through `_master-schema.html`,
  `assemble-final-document.py`, **does not exist on disk** — confirmed
  by direct file search (`assemble-final-document.py`, `extract-mermaid-
  images.py`, `render-docx.py` — none of the three scripts named in
  `plan/usecase/6c-render-paper.md:8-9` exist anywhere in the repo).
  That plan doc's own "(planned, not yet built)" qualifier on line 9 is
  ambiguously scoped in the prose (it trails a 3-script list, unclear if
  it describes all three or just the last one) — the filesystem check,
  not the prose, is what this claim rests on. Fixing the template now,
  before the script exists, means the script gets built against the
  right shape instead of the wrong one.
- **The budget indicator lives inside the generation markdown template,
  and is broken for 12 of 15 domains.** The visualization-depth
  proposal's §2 added `<!-- budget: {{ word_count }} / {{ budget_min
  }}-{{ budget_max }} words -->` to generation templates. Confirmed: 12
  of 15 `templates/generation/markdown/*.md` files have this comment.
  But the values it renders come from `calculation/deterministic/
  {domain}.yaml`'s `word_count_in_range` check config
  (`check_word_budget.py:26-34`, `_load_domain_config()`) — and **only 2
  of 16 domains define that check**: `abstract.yaml` (`min:100,max:500`)
  and `title-and-metadata.yaml` (`min:5,max:50`). The other 14 —
  including `methodology`, `introduction`, `results`, `discussion`, every
  domain that actually carries paper-length content — have no
  `word_count_in_range` check at all, so `_load_domain_config()` returns
  `None` and `{{ budget_min }}`/`{{ budget_max }}` render unresolved (or
  blank, depending on the mustache engine's undefined-variable handling)
  in every one of those 12 templates that carries the comment. The two
  domains that *do* have a real budget config (`abstract`, `title-and-
  metadata`) are, by contrast, the two domains that **don't** have the
  comment in their template at all (confirmed: `abstract.md` and
  `title-and-metadata.md` have no `<!-- budget -->` line) — the comment
  and the data that would fill it in don't overlap on a single domain.
- **No minimum/maximum counts exist for tables, diagrams, or formulas
  anywhere — only boolean presence checks.** `calculation/deterministic/
  methodology.yaml` has `diagram_present` (`rule: contains_mermaid_
  diagram`) and `equations_explained` (`rule: contains_equation`) —
  both yes/no, zero vs. one-or-more, no depth requirement. Citation
  minimums exist but are inconsistent: `min_citation_count` with
  `config: {min: N}` appears in `methodology.yaml` (min 1),
  `results.yaml` (min 1), `problem-definition.yaml` (min 1),
  `related-work.yaml` (two separate checks: `rw-001` min 5 severity
  `warning`, `relw-cit` min 1 severity `critical` — same rule type,
  different thresholds, undocumented why), `references.yaml` (min 10)
  — five domains defined, eleven
  not, no stated rationale for why `related-work` needs 5 and
  `methodology` needs 1. Nothing anywhere checks "how many tables" or
  "how many formulas" a section needs for the paper to read as properly
  in-depth — a `results` section can pass every existing check with zero
  tables.
- **Generation has no self-check — the first time any of this is
  actually verified is at `deterministic-audit-{d}`, a separate,
  downstream usecase.** `check_word_budget.py` (runs during `section-
  budget-fit-{d}`, the last generation-stage usecase before audit) reads
  exactly one rule out of a domain's full check list —
  `_load_domain_config()` (`check_word_budget.py:26-34`) specifically
  extracts only the check whose `rule == "word_count_in_range"` and
  ignores every other entry in the same YAML file (`min_citation_count`,
  `contains_mermaid_diagram`, `contains_equation`, `no_placeholders`,
  etc.). Those other checks aren't evaluated until `deterministic_audit.py`
  runs, at the next usecase stage (`deterministic-audit-{d}`,
  `run_full_workflow.py` Phase 6) — meaning generation can report itself
  "complete" (budget-fit PASS) while missing every citation, table,
  diagram, or formula requirement, and the gap only surfaces once the
  paper is already in the audit/report pipeline, not while it's still
  being written.
- **`calculation/` is flat — 5 subdirectories (`deterministic`,
  `semantic`, `summary`, `aggregation`, `validation`), no split between
  "what generation must produce" and "what the report scores after the
  fact,"** unlike `templates/`, which already separates `templates/
  generation/` from `templates/report/`. The distinction matters in
  practice, not just for tidiness: `calculation/deterministic/{domain}.yaml`
  is read by *both* `check_word_budget.py` (generation-time, one rule
  only, per the gap above) and `deterministic_audit.py` (audit-time, full
  rule set) — the same file serves two different pipeline stages under a
  name (`deterministic`) that describes neither stage, it describes the
  *kind* of check (mechanical vs. LLM-judged). **Bonus finding, flagged
  but out of scope for this proposal**: `calculation/aggregation/
  domain/*.yaml` (added by the report-granularity proposal) is confirmed
  dead at runtime — grepped `aggregation` across `script/**/*.py`, the
  only hits are the one-time generator scripts that *wrote* the 12 files
  (`generate_calc_yamls.py`, `generate_templates.py`); `calculate.py`
  (the score-computation script) never reads `calculation/aggregation/**`
  at all, it still computes the two-bucket score inline. Not fixed here
  — it's a different problem (a written-but-unwired calculation, not a
  missing one) — but worth knowing before this proposal adds more files
  under `calculation/` that need to actually get read.

## 1. Scope

`templates/generation/**` (both `.md` and `.html`), a new `calculation/
generation/` directory (replaces `calculation/deterministic/`'s role),
`calculation/report/` (existing `deterministic`→removed,`semantic`,
`summary`, `aggregation`, `validation` — moved under one parent to make
the two-category split real, not just implied), `check_word_budget.py`
(extended into a full generation-completeness check), `deterministic_
audit.py` (re-pointed at the moved calc directory), `calculate.py`
(re-pointed at the moved `summary/` path), and one new usecase-adjacent
verification step in `run_full_workflow.py`'s Phase 5d. Doesn't touch
`assemble-final-document.py` itself (still not built, per §0 — this
proposal specifies the HTML template shape it should be built against,
not the script), the report-side templates/calculation (report-
granularity proposal's territory, unaffected), or the dead `calculation/
aggregation/domain/*.yaml` wiring gap (§0's bonus finding, explicitly
out of scope, §9).

## 2. Generation HTML Templates — Per-Domain Structure, Not One Blob

### 2a. One HTML file per domain, mirroring the markdown twin

`templates/generation/html/{domain}.html` × 15 (matching the 15
`templates/generation/markdown/*.md` files — 12 structural domains +
`gaps`/`novelty`/`mathematics` cross-cutting, per `_master-schema.yaml`).
Each mirrors its markdown twin's heading structure directly:

```html
<!-- templates/generation/html/methodology.html -->
<section class="domain domain-methodology">
  <h2>Overview</h2>
  {{{ overview }}}
  <h2>Algorithm / Procedure</h2>
  {{{ algorithm }}}
  <h2>Complexity Analysis</h2>
  {{{ complexity }}}
  <h2>Architecture</h2>
  {{{ architecture }}}
  <h2>References</h2>
  <ol class="citations">
    {{#citations}}<li id="cite-{{ index }}">{{ citation }}</li>{{/citations}}
  </ol>
</section>
```

Same field names as the `.md` twin (`overview`, `algorithm`, `complexity`,
`architecture`, `citations`) — both templates render from the same
context object, one usecase's output, two output formats. No new data
requirement on the generation usecases themselves.

### 2b. `_master-schema.html` becomes the outer shell only

Today's single `{{{ content }}}` blob is replaced by a concatenation of
the per-domain fragments from §2a, in `_master-schema.yaml`'s `sections:`
order — not a Mustache-partials mechanism (`{{> domain }}`), since
**no partial rendering is used anywhere in this codebase today**
(grepped `chevron.render(` across `script/`: every call passes exactly
`(template_string, context)`, no `partials=` kwarg, confirmed zero
`{{>` references in any existing template). Introducing partials here
would be new machinery for a script (`assemble-final-document.py`) that
doesn't exist yet to learn — simpler to keep doing what markdown
concatenation already does: render each domain's `.html` fragment to a
string individually (one `chevron.render()` call per domain, using that
domain's own context), then join the resulting HTML strings in
document order, then wrap the joined result in `_master-schema.html`'s
now-slimmer shell:

```html
<!-- templates/generation/html/_master-schema.html, revised -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <style> ... (unchanged) ... </style>
</head>
<body>
  <h1>{{ title }}</h1>
  <p class="meta">{{ authors }} — {{ date }}</p>
  {{{ assembled_sections }}}
  <!-- assembled_sections = concatenation of each domain's rendered
       .html fragment, computed by assemble-final-document.py before
       this template is rendered, not by this template itself -->
</body>
</html>
```

This is the shape `assemble-final-document.py` (§0, not yet built)
should be built against — its job becomes "render each domain fragment,
concatenate, wrap in the shell," not "wrap one giant blob."

## 3. Budget Config Out of the Template, Into Calculation

### 3a. Remove the `<!-- budget: ... -->` comment from every generation
   markdown template

The comment (§0) is unresolvable for 12 of 15 domains today because the
backing calculation config doesn't exist for them, and even where it
*does* exist (`abstract`, `title-and-metadata`), the comment isn't
present. Rather than fix the coverage gap and keep operational metadata
baked into the paper's own draft text, remove the comment from all 15
templates — a generation template should hold content fields only,
nothing that's really a pipeline-status readout. The diagnostic value
the comment was going for (greppable word-count-vs-range in the raw
`.md`) moves to §4's generation-time verification step instead, which
already computes this number and can report it through the step's
envelope/log — a proper structured output, not a hidden HTML comment
riding along in the artifact.

### 3b. Every domain gets a real `word_count_in_range` entry

Extends today's 2-of-16 coverage to all 16 (§0), as part of §5's
`calculation/generation/{domain}.yaml`. Worked examples, not an
exhaustive table (full set is implementation work, §9):

```yaml
# calculation/generation/methodology.yaml (excerpt)
- id: meth-wc
  name: word_count_in_range
  rule: word_count_in_range
  severity: critical
  config: { min: 600, max: 1500 }
  description: "Methodology word count within configured range"
```

```yaml
# calculation/generation/introduction.yaml (excerpt)
- id: intro-wc
  name: word_count_in_range
  rule: word_count_in_range
  severity: critical
  config: { min: 400, max: 900 }
  description: "Introduction word count within configured range"
```

`abstract` and `title-and-metadata` are the highest-priority additions,
not just two more entries in the 14-domain gap — they're the two
domains where word count matters most operationally (abstracts have
hard venue limits, titles must stay short) and, per §0, the two domains
that already *have* a `word_count_in_range` check today, just no
template comment ever pointed at it. Their configs already exist
(`abstract.yaml`: min 100/max 500, `title-and-metadata.yaml`: min
5/max 50) — nothing to add for those two, they're proof the mechanism
works, the gap is purely the other 14.

Ranges are illustrative — the actual per-domain numbers are a content-
policy decision for whoever owns the paper standard (`pcems_2026`,
`eswa_journal`), same override mechanism every other `calculation/` file
already uses. What this proposal fixes is that the *mechanism* covers
every domain, not 2 of 16.

## 4. Content-Depth Minimums — Citations, Tables, Diagrams, Formulas

### 4a. New rule types, same `rule`/`config` shape as `min_citation_count`

```yaml
# calculation/generation/methodology.yaml (excerpt)
- id: meth-diagram-min
  name: min_diagram_count
  rule: min_diagram_count
  severity: critical
  config: { min: 1 }
  description: "At least 1 architecture/flow diagram (mermaid fence count)"
- id: meth-formula-min
  name: min_formula_count
  rule: min_formula_count
  severity: warning
  config: { min: 1 }
  description: "At least 1 formula/equation block"
```

```yaml
# calculation/generation/results.yaml (excerpt)
- id: res-table-min
  name: min_table_count
  rule: min_table_count
  severity: critical
  config: { min: 1, max: 8 }
  description: "At least 1 results table, no more than 8 (avoid table-dumping)"
```

`min_table_count` counts Markdown pipe-tables (`| ... | ... |` header +
separator rows); `min_diagram_count` counts fenced ```` ```mermaid ```` 
blocks (`contains_mermaid_diagram` already detects presence — this rule
counts occurrences instead of a single boolean); `min_formula_count`
counts LaTeX-delimited blocks (`$$...$$` or `\[...\]`) or explicit
`contains_equation`'s existing detection pattern, extended to a count.
All three follow `min_citation_count`'s existing `config: {min: N[, max: N]}`
shape — no new config vocabulary, just three new `rule` values the
checker script (`deterministic_audit.py` / §5's generation-time checker)
needs to implement, parallel to how `word_count_in_range`,
`contains_mermaid_diagram`, etc. are already implemented as named rules.

### 4b. Per-domain minimums are a content decision, not a mechanical default

Not every domain needs every kind of artifact — `abstract` shouldn't
need a diagram minimum, `related-work` needs a citation minimum but not
a table one. This proposal specifies the *mechanism* (§4a's three rule
types, usable in any domain's `calculation/generation/{domain}.yaml`)
and gives worked examples (methodology: diagram+formula, results:
table, related-work/references: citations, already partially present
today per §0) — assigning the full 16-domain matrix of which minimums
apply where is implementation work (§9), not decided file-by-file here.

## 5. `calculation/` Split — `generation/` vs `report/`

### 5a. New layout

```
calculation/generation/{domain}.yaml   × 15   -- §3b, §4, replaces calculation/deterministic/
calculation/deterministic/future-scope.yaml    -- unmoved, orphaned (§9 observation A)
calculation/report/deterministic/       -- empty; deterministic-audit-{d} now reads calculation/generation/ directly (§5b)
calculation/report/semantic/{cross-section,document,document-review,section-parts,full-part-blend,rerun-policy}.yaml
calculation/report/semantic/ensemble/{domain}[-{part_kind}].yaml   × 48
calculation/report/summary/{final_score,paper-budget,score_bands,trend}.yaml
calculation/report/aggregation/domain/{domain}.yaml   × 12
calculation/report/validation/scoring_validation.yaml
```

`calculation/deterministic/` is retired for its 15 real domains, not
duplicated — its content *is* `calculation/generation/{domain}.yaml`
now (§5b explains why one file serves both the generation-time check
and the audit-time one, rather than keeping two copies of the same
rules in sync by hand). `future-scope.yaml`, the 16th file, stays behind
unmoved per §9 observation A — it gates a domain that doesn't exist.
Everything else under `calculation/{semantic,summary,aggregation,
validation}/` moves under `calculation/report/` unchanged in content,
mirroring `templates/{generation,report}/`'s existing split exactly.

### 5b. Why `deterministic-audit-{d}` reads `calculation/generation/`, not a separate `calculation/report/deterministic/`

`deterministic_audit.py` and §4's generation-time checker are
conceptually the same check running at two pipeline stages (§0's core
finding) — generation's self-check is "does this draft satisfy the
domain's requirements," and `deterministic-audit-{d}` is "verify the
committed draft still satisfies them, for the record" (the audit-
governance proposal's commit-hash gating already treats this as a
verification re-run, not a distinct check). Keeping one rule file
(`calculation/generation/{domain}.yaml`) that both stages read means a
new minimum (say, raising `results`' table minimum from 1 to 2) takes
effect at both stages automatically — a `calculation/report/
deterministic/` copy would require every such change to be made twice
and would drift the moment someone forgot the second file.

### 5c. Script path updates required

| File | Current path | New path |
|---|---|---|
| `check_word_budget.py:27` (`_load_domain_config()`) | `calculation/deterministic/{domain}.yaml` | `calculation/generation/{domain}.yaml` |
| `check_word_budget.py:39` (`_load_paper_budget()`) | `calculation/summary/paper-budget.yaml` | `calculation/report/summary/paper-budget.yaml` |
| `deterministic_audit.py:17-18` (`DETERMINISTIC_DIR`) | `calculation/deterministic` | `calculation/generation` |
| `calculate.py:62-64` | `summary/final_score.yaml`, `summary/score_bands.yaml`, `summary/trend.yaml` | `report/summary/final_score.yaml`, `report/summary/score_bands.yaml`, `report/summary/trend.yaml` |

No other script references a `calculation/{deterministic,semantic,
summary,aggregation,validation}` subpath directly (confirmed by grep,
§0) — `render_charts.py`'s `calc_dir` reference (`render_charts.py:552`)
resolves to the `calculation/` root, not a named subdirectory, so it's
unaffected by the rename.

## 6. Generation-Time Self-Verification

### 6a. New check runs where `check_word_budget.py` runs today, checks everything

`check_word_budget.py` is extended (not replaced — same script, same
usecase slot, `section-budget-fit-{d}`, `run_full_workflow.py:791-799`)
to load the domain's **full** `calculation/generation/{domain}.yaml`
rule list instead of extracting only the `word_count_in_range` entry
(§0's `_load_domain_config()` gap) — runs every rule (`word_count_in_
range`, `min_citation_count`, `min_table_count`, `min_diagram_count`,
`min_formula_count`, `contains_*`, `no_placeholders`) against the
domain's current draft text, the same rule-evaluation logic
`deterministic_audit.py` already implements (reused, not reimplemented
— §6c).

### 6b. Failure reporting — itemized, not pass/fail

```python
write_envelope(out_path, status="ok" if all_passed else "error",
               message=("; ".join(f"{c['name']}: {c['detail']}"
                                   for c in failed_checks) or "all checks passed"),
               paper_id=paper_id, domain=domain,
               checks=check_results,  # full list: {id, name, passed, detail}
               missing=[c["name"] for c in failed_checks])
```

A domain missing its citation minimum sees `"min_citation_count: 2/5
minimum"` in the step's own output — at generation time, in the same
step that already runs right before hand-off to audit — not three
usecases later when `deterministic-audit-{d}` runs and a separate report
has to be opened to find out what's missing.

### 6c. Shared rule-evaluation code, not two implementations

`deterministic_audit.py` dispatches 15 rule types today (confirmed:
`word_count_in_range`, `no_placeholders`, `contains_number`,
`contains_mermaid_diagram`, `contains_pseudocode`, `contains_equation`,
`min_citation_count`, `regex_match`, `regex_absent`, `min_list_items`,
`cross_reference_numbers`, `no_new_results`, `length_proportion`,
`no_citations`, `severity_tagged` — one `elif rule == "..."` branch each,
`deterministic_audit.py:126-186`). All 15 move to a shared module
(`script/common/content_rules.py`, new) that both `check_word_budget.py`
(§6a, generation-time) and `deterministic_audit.py` (audit-time) import
and call, plus the 3 new ones from §4a (18 total) — same reasoning as
§5b's single calculation file: one implementation of "what does
`min_table_count` mean," not two that can drift. **This is a real
extraction of 15 existing dispatchers, not a small addition** — sizing
note for §9/implementation planning, not a redesign of any individual
rule's logic.

### 6d. Fail-fast, matching the existing deterministic→semantic gate pattern

`run_full_workflow.py` already fail-fasts semantic-audit on
deterministic-audit FAIL (`run_full_workflow.py:16`'s documented flow,
Phase 7's `skipped_domains` list, §0 of the report-granularity
proposal). This proposal's generation-time check gets the same
treatment one stage earlier: a domain that fails §6a's completeness
check doesn't proceed to `deterministic-audit-{d}` — it's reported as
`status: "generation-incomplete"` and skipped, same shape as today's
`"skipped: deterministic audit FAIL"` message
(`run_full_workflow.py:847`). Catches the gap at the earliest possible
pipeline point instead of the audit stage re-discovering the same
failure a step later.

## 7. Schema / Data Impact

None. This proposal adds no new tables or columns — `academic_
deterministic_findings` already stores a `findings` JSON array (§0 of
the report-granularity proposal confirms this shape); §6b's itemized
check results fit the existing schema unchanged. The generation-time
check (§6a) writes its result through the existing step-envelope
mechanism (`write_envelope`), not a new table — it's a gate, not a
persisted audit record (that's still `deterministic-audit-{d}`'s job).

## 8. New/Changed Files — Consolidated

**New generation templates (15 files):**
`templates/generation/html/{domain}.html` × 15 (§2a).

**Changed generation templates (13 files, §3a):**
every `templates/generation/markdown/{domain}.md` that has the
`<!-- budget -->` comment loses it (12 files); `_master-schema.html`
rewritten to the slim shell (1 file, §2b).

**Moved calculation files:**
`calculation/deterministic/{domain}.yaml` × 15 → `calculation/
generation/{domain}.yaml` (extended per §3b/§4) — `future-scope.yaml`
excluded, stays unmoved (§9 observation A). `calculation/
{semantic,summary,aggregation,validation}/**` → `calculation/report/**`
unchanged in content (§5a).

**Changed scripts:**

| File | Change |
|---|---|
| `script/common/content_rules.py` | New — shared rule-evaluation dispatch table (§6c); extracts all 15 of `deterministic_audit.py`'s existing rule handlers (non-trivial refactor, not a small extraction) plus 3 new: `min_table_count`, `min_diagram_count`, `min_formula_count` (§4a) |
| `script/assemble-paper-structure/check_word_budget.py` | Extended to run the domain's full rule list via `content_rules.py`, not just `word_count_in_range` (§6a); itemized failure reporting (§6b); path updated to `calculation/generation/` and `calculation/report/summary/` (§5c) |
| `script/deterministic-audit/deterministic_audit.py` | `DETERMINISTIC_DIR` re-pointed to `calculation/generation` (§5c); rule evaluation delegated to `content_rules.py` (§6c) |
| `script/calculate/calculate.py` | `_load_yaml()` calls re-pointed to `report/summary/*.yaml` (§5c) |
| `script/schema/run_full_workflow.py` | Phase 5d gains fail-fast on generation-completeness failure, same shape as Phase 6→7's existing deterministic→semantic gate (§6d) |

## 9. Open Questions

- **Full 16-domain minimums matrix** — §4b gives worked examples
  (methodology, results) but doesn't assign table/diagram/formula/
  citation minimums for all 16 domains. Needs a real editorial pass
  (what does `discussion` need vs. `limitations` vs. `conclusion`) —
  proposed here as a mechanism, not a filled-in spec.
- **`future-scope.yaml` exists in `calculation/deterministic/` with no
  matching `templates/generation/markdown/future-scope.md`** — noticed
  while auditing file counts (§0), pre-existing inconsistency, unrelated
  to this proposal's scope. `future-scope` is also not in `STRUCTURAL_
  DOMAINS` (`academic_schema.py:523-527`, 12 entries, no `future-scope`)
  — no domain ever generates content under that key, so `deterministic_
  audit.py` never loads this file for any real paper today. **Decision**:
  excluded from §5a's `calculation/deterministic/` → `calculation/
  generation/` move — it stays where it is, unmoved, flagged as orphaned
  dead weight rather than migrated into the new directory as if it
  gates something. Not deleted here either (same "flag, don't fix
  unrelated dead code" treatment as §0's `calculation/aggregation/`
  finding, observation C below) — a real cleanup decision needs to know
  why the file exists before removing it.
- **`calculation/aggregation/domain/*.yaml` dead-wiring** (§0's bonus
  finding) — `calculate.py` doesn't read it. Real gap, but a report-side
  problem (the report-granularity proposal's territory), not fixed here.

## 10. Explicitly Out of Scope

`assemble-final-document.py`'s actual implementation (still not built,
§0 — this proposal only specifies the template shape it should target),
the full 16-domain content-minimums matrix (§9), `content_rules.py`'s
actual rule-evaluator code beyond what's already in `deterministic_
audit.py` today (extracting existing logic, not rewriting it), and
`calculation/aggregation/domain/*.yaml`'s dead-wiring fix (§0, §9 — a
different, report-side problem).
