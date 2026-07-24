# base_academic — Documentation-Gated Pipeline & Dual-Track Rendering Proposal

## 0. Why This Document Exists

Directive this session, verified against what's actually on disk in
`samgraha/system/academic/base_academic/`:

1. **The pipeline must only run against repos that already have real
   documentation.** No usecase, in any classification branch, may generate
   documentation as a substitute when a repo doesn't have it.
2. **The usecase order is wrong.** After verifying documentation exists, the
   sequence should be: novelty analysis → gap analysis → find the
   documentation and derive the mathematical detail + diagrams (mermaid or
   similar) a paper needs → convert the documentation into paper structure
   using the novelty findings, the gap findings (gaps become future-scope
   material, not dropped), and the math/diagrams → audit each phase with
   both a deterministic and a semantic check → fix based on that audit
   feedback until quality clears a threshold → AI-plagiarism + AI-humanizer
   audit (also split deterministic/semantic) → fix based on that feedback →
   render.
3. Every generation step needs a predefined template markdown (content
   shape) plus a scaffolding script (file/DB writes) — no exceptions. The
   audit report itself follows the same rule: an audit-report template
   markdown gets populated once deterministic+semantic audit scores exist,
   the score/audit outcome decides which visualizations apply, a script
   renders those visualizations, and markdown + visualizations + an HTML
   template combine into an HTML audit report, then a PDF. Separately, the
   paper track is markdown + diagram images → HTML → DOCX (and/or PDF).

**Confirmed bug that makes point 1 concrete, not hypothetical.** The
existing gate doesn't check for real documentation at all.
`classify_repo.py:36-46`'s `has_analysis_docs()` only looks at
`docs/paper/{system}/` — that is **this pipeline's own output tree**, not
the target repo's README, `docs/`, or docstrings. Consequence, read
straight off `classify_repo.py:58-65`:

```python
if not has_impl and not has_docs:
    classification = "NO_DOCS_NO_IMPL"
elif not has_impl:
    classification = "DOCS_ONLY"
elif not has_docs:          # <- fires for almost every real repo on first run,
    classification = "IMPL_NO_ANALYSIS"   #    because docs/paper/{system}/ never exists yet
else:
    classification = "IMPL_WITH_ANALYSIS"
```

`DOCS_ONLY` never fires off a repo's actual authored documentation — it
fires when there's no implementation *and* we haven't generated our own
analysis tree yet. Any repo with source code and a normal `README.md` +
`docs/` folder still lands in `IMPL_NO_ANALYSIS` on a fresh run, because
`has_docs` is asking "did we already generate our own paper-support docs,"
not "does this repo have documentation." `IMPL_NO_ANALYSIS` then routes to
`generate-analysis-docs` (`plan/usecase/1-generate-analysis-docs.md`),
which synthesizes summary/architecture/mathematics/novelty/gaps content
from source code alone and writes it into `docs/paper/{system}/modules/**`
— documentation-shaped output manufactured to route around the precondition
that real documentation doesn't exist yet. That is exactly the fallback
behavior point 1 above rules out, and it is the default path for most
repos today, not an edge case.

**Scope of this document.** Supersedes `base_academic-usecase-proposal.md`
§1's usecase taxonomy and `base_academic-data-pipeline-proposal.md` §3's
4-state classification gate. Does **not** reopen the data-pipeline
proposal's other mechanics — schema-as-files (§1), score-history append-only
design (§5), master-schema/HTML/DOCX template layer (§6.1-6.2, §6.6),
mermaid extraction (§6.4), visualization tables (§7), or the
`expand_triads()` runtime-expansion approach (§8) — those stay as specified
and this proposal builds on them. It narrows the entry gate, replaces the
usecase sequence built on top of it, and adds the deterministic-audit layer
and dual-track (audit-report vs. paper) rendering split that were previously
either missing or under-specified.

**Boundary, restated.** Everything this document touches lives under
`Kriti/samgraha/system/academic/base_academic/` — schema, scripts,
templates, `plan/usecase/*.md`, `standard.yaml`. Samgraha's own engine
schema (`samgraha/schema/knowledge/` — the separate `samgraha` repo, not
this one) is never written to directly and nothing here proposes touching
it, same boundary `base_academic-data-pipeline-proposal.md` §2 already
established (`register_standard` reads our `standard.yaml`; only it writes
`usecase`/`step`/`step_script`/`step_prompt`).

**No migration — nothing is deployed.** None of this is implemented
anywhere yet: no live `knowledge.db` has `academic_repos` rows under the
old 4-value classification, no report has ever been rendered. Every schema
delta below is written as the final `CREATE TABLE`/`CHECK` shape directly —
not as an `ALTER TABLE` against existing data, not as a backfill. Treat
every `.sql` file under `base_academic/schema/` as freely rewritable until
this pipeline actually runs against a real repo for the first time.

## 1. Entry Gate — Real Documentation Required, No Generation Fallback

`classify-repo` collapses from 4 states to 2. Implementation presence stops
being a classification input entirely — it only matters later, as optional
grounding evidence for claims (§2), never as a trigger that manufactures
documentation.

| State | Meaning | Downstream |
|---|---|---|
| `NO_DOCS` | Repo has no author-supplied documentation | **Refuse — terminal.** No usecase runs past this point, regardless of whether an implementation exists. |
| `HAS_DOCS` | Repo has author-supplied documentation | → `novelty-analysis` (§2.1) |

**`has_repo_documentation()` replaces `has_analysis_docs()`.** Scans the
target repo's actual documentation surface, explicitly excluding this
pipeline's own output tree:

- `README.md` / `README.rst` at repo root
- `docs/**` — **except** `docs/paper/**`, which is `base_academic`'s own
  generated tree and must not count as evidence the repo already had
  documentation
- Any top-level `*.md` (`CONTRIBUTING.md`, `ARCHITECTURE.md`, etc.)
- Module/package-level docstrings, as a secondary corroborating signal only
  — a repo with docstrings but zero prose documentation still needs a
  human judgment call, not an automatic pass

**Minimum content threshold**: total word count across README + `docs/**`
(excluding `docs/paper/**`) + top-level `*.md` must be `>= 200` words to
satisfy `HAS_DOCS` — a one-line placeholder `README.md` doesn't count as
documentation. `200` is a starting default, not a claim it's calibrated;
it lives in `standard.yaml` as a configurable value
(`classify_repo.min_doc_words`), not hardcoded in `classify_repo.py`, so
adjusting it later doesn't require a code change.

Concrete deltas:

- `classify_repo.py:36-46` — `has_analysis_docs()` renamed
  `has_repo_documentation()`, rewritten per the scan above.
- `classify_repo.py:58-65` — collapses to the 2-branch `if/else` for
  `NO_DOCS`/`HAS_DOCS`. `has_impl`/`count_source_files()` stay (still
  recorded in `academic_repos` metadata — implementation-grounding is still
  useful later, see §2), just no longer branch the classification.
- `schema/02-academic_repos.sql` — `CHECK (classification IN (...))`
  narrows to `('NO_DOCS','HAS_DOCS')`.
- `run_full_workflow.py` — every `IMPL_NO_ANALYSIS`/`DOCS_ONLY`/
  `IMPL_WITH_ANALYSIS`/`NO_DOCS_NO_IMPL` branch (lines ~493-510 per current
  grep) collapses to one `if classification == "NO_DOCS": refuse` /
  `else: proceed`.
- **`generate-analysis-docs` is retired as an entry-fallback usecase.**
  `plan/usecase/1-generate-analysis-docs.md` is deleted as a standalone
  usecase. Its machinery isn't thrown away — `discover-modules`,
  `gather-module-evidence`, `gather-cross-module-evidence` and the 5+7
  analysis-kind prompts under `templates/generation/analysis/**` are
  repurposed as the evidence layer for the three new usecases in §2. The
  difference is what those prompts are told to treat as ground truth:
  previously they could invent module documentation from source code alone;
  now they must cite the repo's actual documentation as the primary source
  and use source code only as corroborating/verifying evidence. Where
  documentation is silent on something a claim would need, the existing
  `[NEEDS AUTHOR INPUT]` flag (`humanifier.md`'s convention, already reused
  by `2a-draft-from-docs-only.md`) applies instead of fabricating content.

**Disposition of all 12 old analysis-kind template files**, so none are
silently dropped or left ambiguous between §2.1-2.3's three new usecases:

| File | Level | New home |
|---|---|---|
| `analysis/module/novelty.md` | module | §2.1 `novelty-analysis` |
| `analysis/cross_module/novelty.md` | cross-module | §2.1 `novelty-analysis` |
| `analysis/module/gaps.md` | module | §2.2 `gap-analysis` |
| `analysis/cross_module/gaps.md` | cross-module | §2.2 `gap-analysis` |
| `analysis/module/mathematics.md` | module | §2.3 `mathematics-and-diagrams` |
| `analysis/cross_module/mathematics.md` | cross-module | §2.3 `mathematics-and-diagrams` |
| `analysis/module/architecture.md` | module | §2.3 `mathematics-and-diagrams` — diagram half (`classDiagram`), not just the math half; the usecase name covers both |
| `analysis/cross_module/architecture.md` | cross-module | §2.3, same reason |
| `analysis/cross_module/dependencies.md` | cross-module | §2.3, same reason (`flowchart TD`) |
| `analysis/cross_module/interactions.md` | cross-module | §2.3, same reason |
| `analysis/module/summary.md` | module | **Retired as a standalone template.** Folded into `assemble-paper-structure`'s `gather-domain-evidence` pre-step (§2.4) as raw evidence gathering, not a separately persisted/audited analysis doc — a plain module summary isn't novelty, a gap, math, or a diagram; it's context `gather-domain-evidence` already needs to read to write any structural domain. |
| `analysis/cross_module/patterns.md` | cross-module | **Retired as a standalone template**, same reasoning — design-pattern rollup feeds `methodology`/`discussion` generation as evidence, not a separately audited deliverable. |

`mathematics-and-diagrams`'s YAML sketch in §2.3 above is written narrowly
(mathematics prompt only) for readability; per this table it actually runs
two semantic prompts per module/cross-module unit —
`module-analysis-mathematics` and `module-analysis-architecture` (plus
cross-module `dependencies`/`interactions`) — same triad shape repeated per
prompt, not a second usecase.

## 2. Revised Usecase Sequence

Old vs. new mapping, so nothing in §1's usecase files gets silently
orphaned:

| Step | New usecase | Replaces / absorbs |
|---|---|---|
| 0 | `classify-repo` (revised, 2-state) | `0-classify-repo.md`, narrowed |
| 1 | `novelty-analysis` | novelty kind out of old usecase 1 (`generate-analysis-docs`) |
| 2 | `gap-analysis` | gaps kind out of old usecase 1 |
| 3 | `mathematics-and-diagrams` | mathematics kind out of old usecase 1 + `figures` enrichment out of old usecase 3 (`3-deepen-sections.md`) |
| 4 | `assemble-paper-structure` | unifies `2a-draft-from-docs-only.md` + `2b-generate-paper-draft.md` — one usecase, not a branch (§2.4) |
| 5 | `deterministic-audit` | **new** — no deterministic layer exists today (§5) |
| 6 | `semantic-audit` | `4-semantic-audit.md`, unchanged in shape |
| 7 | fix-loop (det+sem) | `plan/core/loop.yaml`'s existing `fix_loop`/`tier_gate`, now fed by two audit kinds (merge rule: §2.5) |
| 8 | `plagiarism-forensic-audit` (det+sem sub-checks, Pass 1+2) | `5a-plagiarism-forensic-audit.md`, split internally (§6) |
| 9 | `humanize` (Pass 3) | `5b-humanize.md`, unchanged |
| 10 | AI-plagiarism fix-loop | same `loop.yaml` mechanism, re-enters 8/9 |
| 11 | `calculate` | `6-calculate.md`, now built (§7), gains a deterministic bucket |
| 12a | `render-audit-report` | **new track** (§4) |
| 12b | `render-paper` | `7-render.md`, unchanged mechanics, now explicitly one of two tracks (§4) |

### 2.1 Usecase: `novelty-analysis`

```yaml
- name: novelty-analysis
  description: "usecase 1 — identify what's novel, sourced from the repo's actual documentation, corroborated (not invented) by implementation evidence where present"
  steps:
    - order: 1
      kind: deterministic
      description: "Pre: gather repo documentation (README, docs/**, docstrings) + module source as corroborating evidence"
      script: gather-module-evidence   # reused, doc-primary mode
    - order: 2
      kind: semantic
      description: "Write module-level novelty findings, citing documentation passages; [NEEDS AUTHOR INPUT] where docs don't support a claim source code alone would suggest"
      prompt: module-analysis-novelty   # reused unchanged, per-module
    - order: 3
      kind: deterministic
      description: "Post: persist to academic_module_analysis + docs/paper/{system}/modules/{module}/novelty.md"
      script: persist-module-analysis
    # cross-module rollup, once per repo, same pre/semantic/post shape
```

Same triad shape and scripts `1-generate-analysis-docs.md` already used
(`gather-module-evidence` → `module-analysis-novelty` →
`persist-module-analysis`), narrowed to one analysis kind and re-scoped to
documentation-primary evidence per §1.

### 2.2 Usecase: `gap-analysis`

Same shape as §2.1, `gaps` kind only. Its output is not terminal prose the
way it is today (`docs/paper/{system}/modules/{module}/gaps.md` sitting
unused past generation) — it is a required input to §2.4's assembly step,
where each finding becomes one future-scope item (§2.4, §8.1) rather than a
document nobody downstream reads.

### 2.3 Usecase: `mathematics-and-diagrams`

Merges old usecase 1's `mathematics` analysis kind with old usecase 3's
`figures` enrichment pass — both exist to extract/derive formal content
from documentation, and splitting them into two separate usecases (one at
"analysis" time, one at "enrichment" time three usecases later) was
unnecessary distance between two things that read the same source material.

```yaml
- name: mathematics-and-diagrams
  description: "usecase 3 — derive mathematical formalization and mermaid diagrams from the repo's documentation, module-by-module then cross-module"
  steps:
    - order: 1
      kind: deterministic
      script: gather-module-evidence
    - order: 2
      kind: semantic
      description: "Formalize {module}'s documented behavior mathematically (LaTeX) and/or as a mermaid diagram per docs/mermaid-diagram-standards.md, sourced from documentation"
      prompt: module-analysis-mathematics
    - order: 3
      kind: deterministic
      script: persist-module-analysis
    # cross-module rollup: architecture/dependencies/interactions diagrams, mathematics, same shape
```

`docs/mermaid-diagram-standards.md`'s existing rules (classDiagram for
module architecture, flowchart TD + classDef tiers for cross-module
dependencies/interactions, LaTeX-only for mathematics — no diagram) apply
unchanged; this usecase is the single place that convention now gets
applied, instead of being split across an analysis pass and a later
enrichment pass with the same rules duplicated in two prompt files.

### 2.4 Usecase: `assemble-paper-structure`

Replaces both `2a-draft-from-docs-only.md` and `2b-generate-paper-draft.md`
with one usecase. The old split existed because the old 3-way/4-way
classification distinguished "docs only" from "impl + analysis present" —
under the new binary gate (§1), documentation is *always* present by the
time this usecase runs, so there's no classification branch left to justify
two separate usecases. What still varies is per-claim, not per-usecase:
whether a specific claim is implementation-backed decides
`academic_narratives.validated` (true/false) the same way it always did —
that's a row-level flag set by the post-script, not a reason to fork the
whole usecase.

```yaml
- name: assemble-paper-structure
  description: "usecase 4 — generate every structural domain from documentation, weaving in novelty-analysis/gap-analysis/mathematics-and-diagrams findings; gaps become future-scope content, not dropped"
  steps:
    # repeated per structural domain in _master-schema.yaml's sections: list
    - order: 1
      kind: deterministic
      description: "Pre: gather documentation excerpts for {domain} + academic_module_analysis novelty/gaps/mathematics rows + implementation evidence where it exists (grounding only, never invented)"
      script: gather-domain-evidence
    - order: 2
      kind: semantic
      description: "Generate {domain}, citing documentation as primary evidence and novelty/gap/math findings where relevant. For the future-scope domain specifically: one item per unresolved gap-analysis finding, not a generic wishlist."
      prompt: generate-section
    - order: 3
      kind: deterministic
      description: "Post: persist draft; validated=true only for claims an implementation-evidence pointer backs, false otherwise"
      script: persist-section-draft
```

New structural domain: `future-scope`, inserted into
`_master-schema.yaml`'s `sections:` list immediately after `limitations`,
before `conclusion`:

```yaml
sections:
  - title-and-metadata
  - abstract
  - introduction
  - related-work
  - problem-definition
  - methodology
  - experimental-setup
  - results
  - discussion
  - limitations
  - future-scope        # NEW
  - conclusion
  - references
```

`limitations` describes weaknesses of the current work; `future-scope` is
structurally distinct — it is what the gap-analysis usecase found,
reframed as forward-looking direction rather than a shortcoming, and it is
the reason `gap-analysis` (§2.2) is a required upstream usecase rather than
a nice-to-have. New golden-standard file `domains/16-future-scope.md`,
same Standard Definition + Expected Evidence shape as the other 15.

**`literature-review`, resolved.** Old `3-deepen-sections.md`'s
`literature-review` enrichment kind doesn't fit §2.3 (it adds *external*
citation context, not something extractable from the repo's own docs) —
it doesn't get its own usecase either; that would be a step for a step's
sake. It becomes a conditional 4th step inside `assemble-paper-structure`,
gated by a new `cite_context:` list in `_master-schema.yaml` naming which
domains need it (`related-work`, `introduction`, `discussion` by default —
the domains where external citation grounding actually matters, not all 13):

```yaml
- order: 4
  kind: semantic
  description: "Literature-review pass — only runs for domains listed in _master-schema.yaml's cite_context:"
  prompt: literature-review-pass   # reused unchanged from templates/generation/enrichment/literature-review.md
```

### 2.5 Fix-Loop Trigger — Deterministic + Semantic Merge Rule

`deterministic-audit` (§5) runs before `semantic-audit` for every domain,
and the two verdicts don't average into one score — they gate
sequentially, cheapest check first:

1. `deterministic-audit` FAILs → fix-loop triggers immediately.
   `semantic-audit` does **not** run this pass — scoring a structurally
   broken draft (missing required diagram, under the reference-count floor)
   with a model call is wasted cost; fix the mechanical gap first, then
   re-audit from the top.
2. `deterministic-audit` PASSes → `semantic-audit` runs. Its own existing
   threshold (`calculation/validation/scoring_validation.yaml`'s bounds +
   whatever `tier_gate` in `plan/core/loop.yaml` already defines) decides
   PASS/FAIL as it always did — unchanged by this proposal.
3. A domain clears the fix-loop only once both checks PASS in the same
   pass (deterministic PASS **and** semantic PASS) — not "either," not
   "average." A domain that's mechanically sound but semantically weak
   still fails; a domain that's semantically strong but missing a required
   diagram still fails.

This is "fail-any, sequential, cheap-first" — not a new fix-loop mechanism,
just the existing `fix_loop`/`tier_gate` in `plan/core/loop.yaml` fed a
two-stage gate instead of one score.

## 3. Template + Scaffold-Script Rule

Formalizing an existing convention as a hard rule, not a per-usecase
choice: **every generation usecase has exactly one template (markdown or a
small template set) defining content shape, and exactly one deterministic
scaffold script performing the gather/persist mechanics.** No usecase
skips the template (that's an ungoverned prompt) and no usecase skips the
scaffold script (that's untracked output — nothing recorded in
`academic_*` tables, unverifiable by a `verify_usecase_*.py`).

| Usecase | Template | Scaffold script | Status |
|---|---|---|---|
| `novelty-analysis` | `templates/generation/analysis/{module,cross_module}/novelty.md` | `gather-module-evidence` / `persist-module-analysis` | existing, re-scoped |
| `gap-analysis` | `.../gaps.md` | same | existing, re-scoped |
| `mathematics-and-diagrams` | `.../mathematics.md` (+ diagram rules from `docs/mermaid-diagram-standards.md`) | same | existing, re-scoped |
| `assemble-paper-structure` | `templates/generation/document/{domain}.md` + `_master-schema.yaml` | `gather-domain-evidence` / `persist-section-draft` | existing |
| `deterministic-audit` | `calculation/deterministic/{domain}.yaml` | `deterministic-audit.py` (new) | **new** (§5) |
| `semantic-audit` | `audit/semantic/document/{domain}.md` + `calculation/semantic/document.yaml` | `gather-domain-evidence` / `persist-domain-semantic-score` | existing |
| `plagiarism-forensic-audit` | `templates/audit/plagiarism-fingerprint.md` (Pass 1) + `templates/generation/document/targeted-rewrite.md` (Pass 2) | `gather-plagiarism-context` / `persist-plagiarism-findings` | existing, Pass 2 dispatch gap fixed (§6) |
| `humanize` | `templates/generation/humanifier.md` | `gather-humanize-context` / `persist-humanize-pass` | existing |
| `render-audit-report` | `templates/audit/report/_audit-report-schema.md` (new) + `templates/generation/document/html/_audit-report-schema.html` (new) | `generate-audit-report.py` (new) + `render_charts.py` (new) | **new** (§4.1) |
| `render-paper` | `templates/generation/document/_master-schema.yaml` + `.../html/_master-schema.html` | `assemble-final-document.py` + `extract-mermaid-images.py` + `render-docx.py` (all still unbuilt per `7-render.md`) | planned, unchanged mechanics |

## 4. Dual-Track Rendering

Two independent output tracks share the mermaid-extraction and PDF
mechanics but differ in source data, template, and purpose. Conflating them
under one `render` usecase (as `7-render.md` currently implies) hides that
difference — this proposal makes them two usecases.

### 4.1 Track A — `render-audit-report`

Score-driven, not prose-driven. Input is audit *results*
(`academic_score_history`, latest `academic_semantic_runs` per domain, the
new `academic_deterministic_findings` from §5, `academic_plagiarism_findings`),
not the paper's narrative content.

1. `generate-audit-report.py` (deterministic) populates
   `templates/audit/report/_audit-report-schema.md` — per-domain
   deterministic + semantic score breakdown, plagiarism verdict summary,
   trend vs. prior run. Persists the populated markdown to
   `academic_report_history` (`format='markdown', report_kind='audit'` —
   see §5's schema note on the new `report_kind` column).
2. **Visualization selection is score/audit-driven, not fixed.** A domain
   whose latest `score_band` is below `PASS` pulls in
   `domain-score-bar` + a new `deterministic-findings-heatmap` chart kind
   (which deterministic checks failed, across domains); `score-trend-line`
   only renders once `run_count > 1` for that domain (a single data point
   has no trend to show); `model-agreement-radar` only renders if more than
   one model scored the domain. Table:

   | Condition | Chart(s) included |
   |---|---|
   | Always, if `run_count > 1` | `score-trend-line` (per domain), `overall-score-trend` |
   | Always | `domain-score-bar` (latest snapshot, all domains) |
   | `score_band != PASS` for any domain | `deterministic-findings-heatmap` (new) |
   | `> 1` model configured | `model-agreement-radar` |

3. `render_charts.py` (new, matplotlib + `Agg` backend, same pattern
   `base_academic-data-pipeline-proposal.md` §7 already specified but never
   built) generates only the charts §4.1.2 selects, recording each in
   `academic_visualizations`.
4. Assemble: populated markdown + generated chart images + new
   `_audit-report-schema.html` → HTML audit report. `format='html',
   report_kind='audit'`.
5. HTML → PDF via the same `playwright` approach `7-render.md` already
   specifies for the paper track (`python_hackathon/script/usecase-7-pdf/
   export_team_pdfs.py` precedent) — reused, not reimplemented a second way.
   `format='pdf', report_kind='audit'`.

### 4.2 Track B — `render-paper`

Unchanged from `7-render.md`'s planned mechanics: concatenate
`assemble-paper-structure`'s domain drafts (most-processed stage —
`humanize` if `5b` ran for that domain, else `generate` — there is no
separate `deepen` stage under this proposal; §2.3/§2.4 fold what used to be
the `deepen` enrichment passes directly into `mathematics-and-diagrams` and
`assemble-paper-structure`'s own generation step) per `_master-schema.yaml`
order, `extract-mermaid-images.py` rasterizes diagram
blocks (hard-fail if `mmdc` unavailable, no silent skip — per the existing
proposal's explicit warning), render through `_master-schema.html`,
`render-docx.py` shells to `pandoc` for `.docx`, `playwright` for `.pdf`.
`format IN (markdown,html,pdf,docx), report_kind='paper'`.

### 4.3 Schema delta: `report_kind`

`schema/18-academic_report_history.sql` gains one column so the two tracks
share the table without collision (both can produce `format='html'` for the
same paper). No live rows exist yet (§0) — this is a straight rewrite of
the file's `CREATE TABLE`, not an `ALTER TABLE`:

```sql
CREATE TABLE IF NOT EXISTS academic_report_history (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    report_kind   TEXT    NOT NULL DEFAULT 'paper' CHECK (report_kind IN ('paper','audit')),
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html','pdf','docx')),
    final_score   REAL,
    score_band    TEXT,
    file_path     TEXT    NOT NULL,
    is_latest     INTEGER NOT NULL DEFAULT 1,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_report_history_lookup
    ON academic_report_history(paper_id, report_kind, format, is_latest);
```

"Latest" is now scoped per track, not just per format.

## 5. Deterministic Audit Layer (New — Doesn't Exist Today)

Confirmed absent: no `calculation/deterministic/` directory, no
deterministic-check script, `domains/*.md`'s "Expected Evidence
(Deterministic)" sections describe what these checks *should* be but
nothing executes them. Every audit today is semantic-only
(`templates/audit/semantic-audit.md`), which is expensive (a model call per
domain per run) for checks that are actually mechanical — reference count,
presence of a complexity-analysis subsection, mermaid-diagram presence in a
domain that structurally needs one, banned AI-fingerprint phrase list.

```
calculation/deterministic/
├── title-and-metadata.yaml
├── abstract.yaml
├── ... (one per structural + cross-cutting domain, 16 total with future-scope)
```

Each file: mechanical rule + severity, same shape
`calculation/validation/scoring_validation.yaml` already uses for its 3
checks, generalized per-domain. New script `deterministic-audit.py`, one
step per domain, runs **before** `semantic-audit` in the fix-loop (§2, step
5 before step 6) — cheap fail-fast: a domain missing its required mermaid
diagram or under a reference-count floor doesn't need to spend a model call
on semantic scoring yet, it needs the mechanical gap fixed first.

New table `academic_deterministic_findings`, same append-only shape as
`academic_semantic_runs`/`academic_plagiarism_findings`:

```sql
CREATE TABLE IF NOT EXISTS academic_deterministic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    run_number    INTEGER NOT NULL DEFAULT 1,
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    findings      TEXT    NOT NULL DEFAULT '[]',   -- JSON array of {check_id, rule, passed, detail}
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, run_number)
);
```

`calculation/summary/final_score.yaml` gains a second bucket — it currently
passes `semantic_document_score` straight through as the only input
(`final_score.yaml:1-10`, single-bucket "no other calculation bucket
exists" note). That note stops being true once this layer exists:

```yaml
inputs:
  - { name: semantic_document, weight: 50 }
  - { name: deterministic_document, weight: 50 }
formula: |
  final_score = 0.5 * semantic_document_score + 0.5 * deterministic_document_score
```

Even split, not 70/30 — an arbitrary skew in either direction claims a
calibration this proposal hasn't done. `50/50` is the honest "no evidence
yet which should dominate" default. Revisit once real papers have run
through both audit kinds — recalibrate off actual score distributions, not
off a second guess made before any data exists (§9).

## 6. AI-Plagiarism/Humanizer — Deterministic + Semantic Split

Pass 1 (forensic, `5a`) currently is semantic-only
(`templates/audit/plagiarism-fingerprint.md`, one LLM call). Some of what
it checks is actually mechanical and shouldn't cost a model call to
compute — burstiness (sentence-length variance) and n-gram repetition
ratio are real formulas, not judgment calls. Split Pass 1 into two
sub-checks feeding one verdict:

```yaml
- name: plagiarism-forensic-audit
  steps:
    - order: 1
      kind: deterministic
      script: gather-plagiarism-context
    - order: 2
      kind: deterministic
      description: "Mechanical fingerprint pre-screen: sentence-length variance (burstiness), n-gram repetition ratio, banned-phrase list"
      script: deterministic-fingerprint-check   # new
    - order: 3
      kind: semantic
      description: "LLM fingerprint judgment (hollow-sentence detection, structural mechanicalness) per templates/audit/plagiarism-fingerprint.md"
      prompt: plagiarism-fingerprint-audit
    - order: 4
      kind: semantic
      description: "Pass 2 — targeted rewrite of only High/Critical-flagged sentences (only runs if step 2 or 3 flagged anything)"
      prompt: targeted-rewrite
    - order: 5
      kind: deterministic
      script: persist-plagiarism-findings
```

`schema/12-academic_plagiarism_findings.sql` gains a `check_kind` column so
both sub-checks' findings land in the same table without collision — again
a straight rewrite of the `CREATE TABLE`, no live rows to migrate (§0):

```sql
CREATE TABLE IF NOT EXISTS academic_plagiarism_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id      INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES academic_domains(id) ON DELETE CASCADE,
    run_number    INTEGER NOT NULL DEFAULT 1,
    pass_type     TEXT    NOT NULL DEFAULT 'forensic' CHECK (pass_type IN ('forensic','targeted-rewrite')),
    check_kind    TEXT    NOT NULL DEFAULT 'semantic' CHECK (check_kind IN ('deterministic','semantic')),
    verdict       TEXT    NOT NULL CHECK (verdict IN ('PASS','FAIL')),
    flagged_spans TEXT    NOT NULL DEFAULT '[]',
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id, run_number, pass_type, check_kind)
);
```

This also fixes the already-documented gap in
`5a-plagiarism-forensic-audit.md`: `expand_triads()` looks up
`targeted-rewrite`'s prompt id but never inserts a step for it, so Pass 2
never actually dispatches today. Step 4 above is that missing insert,
conditional on step 2 or 3 producing any High/Critical flag — `expand_triads()`
needs to check the prior step's output before deciding whether to insert
step 4, which is new logic (today `_insert_step()` inserts unconditionally
based on the domain/module list, not on a prior step's result).

Pass 3 (`humanize`, `5b`) is unchanged — whole-section rewrite, reserved
for what Pass 1+2 don't fix, same `loop.yaml` escalation.

## 7. `calculate` — Building It

`6-calculate.md` documents this as unbuilt; it stays unbuilt in scope here
too except for one addition this proposal requires: `calculate.py` must
read `academic_deterministic_findings` (§5) in addition to
`academic_semantic_runs`, since `final_score.yaml` now has two buckets
(§5). Otherwise unchanged from the existing plan — `scoring_validation.yaml`
pre-checks, `final_score_v1`/`score_bands_v1`/`trend_v1`, one
`academic_score_history` row per domain + one whole-paper row, append-only.

## 8. Concrete File Deltas

`base_academic` is not implemented anywhere yet (§0) — nothing below is a
migration against live data, all of it is "write it this way the first
time."

- `classify_repo.py` — `has_analysis_docs()` → `has_repo_documentation()`
  (§1), branch collapse.
- `schema/02-academic_repos.sql` — `CHECK` narrows to 2 values.
- `schema/18-academic_report_history.sql` — `+ report_kind` column (§4.3).
- `schema/12-academic_plagiarism_findings.sql` — `+ check_kind` column (§6).
- New `schema/20-academic_deterministic_findings.sql` (§5).
- `run_full_workflow.py` — classification branches collapse; `expand_triads()`
  gains the conditional-insert logic for Pass 2 (§6) and the deterministic
  → semantic sequencing/short-circuit for §2.5, and needs new per-usecase
  blocks for `novelty-analysis`/`gap-analysis`/`mathematics-and-diagrams`/
  `assemble-paper-structure`/`deterministic-audit` replacing the old
  `generate-analysis-docs`/`draft-from-docs-only`/`generate-paper-draft`
  blocks.
- **`script/schema/standard.yaml`** — registration deltas, the omission
  flagged in review:
  - Deregister `generate-analysis-docs`, `draft-from-docs-only`,
    `generate-paper-draft` usecase entries.
  - Register `novelty-analysis`, `gap-analysis`, `mathematics-and-diagrams`,
    `assemble-paper-structure`, `deterministic-audit`, `render-audit-report`
    as new usecase entries (steps populated at runtime by `expand_triads()`
    per the existing convention, not hardcoded here).
  - `calculate` and `render` currently have **no entries at all** in
    `standard.yaml` (`6-calculate.md`/`7-render.md` both say "not yet
    implemented" — confirmed, `standard.yaml` has nothing registered under
    either name today). Both need registering when built — `calculate`
    as-is, `render` split into `render-audit-report` (§4.1) and
    `render-paper` (§4.2).
  - New scripts (§ below) need `script:` entries; new prompts
    (`literature-review-pass` reuse aside, nothing new) need none beyond
    what already exists.
- `plan/usecase/` — delete `1-generate-analysis-docs.md`,
  `2a-draft-from-docs-only.md`, `2b-generate-paper-draft.md`,
  `3-deepen-sections.md` (mathematics/figures/architecture/dependencies/
  interactions kinds absorbed into §2.3, summary/patterns folded into §2.4,
  literature-review folded into §2.4 — full disposition table in §1 and
  §2.4); add `1-novelty-analysis.md`, `2-gap-analysis.md`,
  `3-mathematics-and-diagrams.md`, `4-assemble-paper-structure.md`,
  `5-deterministic-audit.md`, split `6a-render-audit-report.md` /
  `6b-render-paper.md` out of `7-render.md`.
- `templates/generation/document/_master-schema.yaml` — `+ future-scope`
  section, `+ cite_context:` list (§2.4).
- New `domains/16-future-scope.md`.
- New `calculation/deterministic/*.yaml` (16 files, §5).
- `calculation/summary/final_score.yaml` — two-bucket formula, 50/50 (§5).
- New `templates/audit/report/_audit-report-schema.md`,
  `templates/generation/document/html/_audit-report-schema.html` (§4.1).
- New scripts: `deterministic-audit.py`, `deterministic-fingerprint-check.py`,
  `generate-audit-report.py`, `render_charts.py`.
- `templates/generation/analysis/module/{summary,architecture}.md` and
  `templates/generation/analysis/cross_module/{architecture,dependencies,
  interactions,patterns}.md` — no file moves, but each needs its prompt
  text re-scoped from source-code-primary to documentation-primary
  evidence, per §1's `generate-analysis-docs` retirement note and the
  disposition table in §1.

## 9. Open Questions / Risks

- **`final_score.yaml`'s 50/50 weight split (§5)** is an honest
  no-evidence-yet default, not a calibrated value — revisit once real
  papers have run through both audit kinds and an actual score
  distribution exists to calibrate against.
- **`mmdc`/`pandoc` hard dependencies** — same risk the data-pipeline
  proposal already flagged (§11 there), unchanged by this document, still
  unresolved. Needs `shutil.which` + a smoke-render check with a hard
  failure at render time, not a silent skip.
- **`200`-word minimum documentation threshold (§1)** is a starting default
  in `standard.yaml`, not empirically tuned — worth revisiting once a
  handful of real repos have gone through `classify-repo` and it's clear
  whether it's too strict or too permissive in practice.

## 10. Explicitly Out of Scope

Actual script/prompt implementation — this document specifies usecase
shape, schema deltas, and template/script pairing, not the Python or the
finished prompt text. `domains/16-future-scope.md`'s full prose,
`templates/audit/report/_audit-report-schema.md`'s full markdown skeleton,
and `calculation/deterministic/*.yaml`'s actual rule content are named and
shaped here, not authored. Migrating `pcems_2026`/`eswa_journal` onto this
revised sequence — follow-up, not this document.
