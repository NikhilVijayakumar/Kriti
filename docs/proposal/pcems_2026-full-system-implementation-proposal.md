# pcems_2026 — Full System Implementation Proposal

## 0. Why This Document Exists

`pcems_2026` today has exactly two directories: `guide/` (45 files — Conference
Guidelines, Writing Guide, Figures, Tables, Mathematics, Reviewer Expectations,
Examples, Checklists, Common Mistakes, Assets, Philosophy — complete per
`a689e66`) and `reference/` (11 sample-paper PDFs + extracted text + the
template PDF). Neither is a runnable standard. There is no `system.yaml`, no
`domains/`, no `calculation/`, no `plan/`, no `prompt/`, no `schema/`, no
`script/`, no `templates/` — none of the machinery `base_academic` has that
turns a knowledge base into something samgraha can generate, audit, and score
against.

`base_academic/system.yaml` (lines 1–13) is explicit about the relationship:

> Concrete systems ... inherit from \[`base_academic`] and provide their own
> domain lists, documentation-standards, audit rubrics, and generation
> templates.

This proposal builds that concrete system: every category `base_academic` has,
populated for `pcems_2026`'s own 6-section-plus-5-cross-cutting-domain shape
(§1), with content authored from `pcems_2026/guide/` instead of generic
academic prose — and registered with the samgraha engine the same way
`base_academic` is.

---

## 1. The 6 Section Domains + 5 Cross-Cutting Domains (not base_academic's 12 + 3)

`base_academic/system.yaml` states directly: `pcems_2026: 6 domains` (line
24, comment). The guide confirms the exact
list and — critically — already names the target filenames for content that
doesn't exist yet. Every `Writing Guide/*.md` file cites a
`Documentation-Standards/NN-{domain}-standards.md` source that has never been
written:

| # | Domain | Writing Guide source | Cited (not-yet-existing) standard file |
|---|--------|----------------------|------------------------------------------|
| 1 | `title-and-metadata` | `Writing Guide/02-title-and-metadata.md` | `Documentation-Standards/01-title-and-metadata-standards.md` |
| 2 | `introduction` | `Writing Guide/03-introduction.md` | `Documentation-Standards/02-introduction-standards.md` |
| 3 | `methodology` | `Writing Guide/04-methodology.md` | `Documentation-Standards/03-methodology-standards.md` |
| 4 | `findings` | `Writing Guide/05-findings.md` | `Documentation-Standards/04-findings-standards.md` |
| 5 | `conclusion` | `Writing Guide/06-conclusion.md` | `Documentation-Standards/05-conclusion-standards.md` |
| 6 | `references` | `Writing Guide/07-references.md` | `Documentation-Standards/06-references-standards.md` |

This table is not a guess — it is transcribed from the `> *Source: ...*` line
at the top of each of the six `Writing Guide/` files. The numbering,
filenames, and domain order below all follow from it directly.

Note: `findings` absorbs what `base_academic` splits into
`experimental-setup` + `results` + `discussion` (per
`Writing Guide/05-findings.md`: "experimental setup → results → analysis" all
inside one section), and PCEMS has no `related-work`, `problem-definition`,
or `limitations` domain — `Conference Guidelines/02-manuscript-structure.md`
lists exactly five main sections (Introduction, Methodology, Findings,
Conclusion, References) plus the title/author/affiliation/keyword front
matter, which is why `title-and-metadata` is the 6th domain.

These 6 are the domains that get their own manuscript heading. They are not
the whole picture.

### 1.1 Cross-Cutting Domains: novelty, gaps, mathematics, tables, figures

A paper isn't constructed by writing 6 headings in isolation — it's
constructed by first understanding what's novel, what gap that novelty
closes, and what mathematics grounds the method, then writing the 6 sections
so that understanding shows up in them. `base_academic/domains/13-novelty.md`,
`14-gaps.md`, and `15-mathematics.md` formalize exactly this distinction, and
the mechanism that makes it real is
`base_academic/templates/generation/markdown/_master-schema.yaml`:

```yaml
# 12 structural domains (map 1:1 to an actual section, in document order)
# + 3 cross-cutting domains (novelty, gaps, mathematics — audited across
# the whole document, not confined to one section; woven into whichever
# structural sections they're relevant to rather than rendered as their
# own headings). cross_cutting entries are NOT in `sections:` — they are
# audit-only domains...

sections: [title-and-metadata, abstract, introduction, related-work,
  problem-definition, methodology, experimental-setup, results, discussion,
  limitations, conclusion, references]        # 12 — get a heading
cross_cutting: [novelty, gaps, mathematics]    # 3 — do not
```

This is confirmed structurally, not just by the comment: `calculation/
report/aggregation/domain/` has exactly 12 files and `calculation/report/
semantic/ensemble/` has exactly 48 (12 × 4) — both match `sections:` exactly
and exclude all 3 `cross_cutting:` entries. Cross-cutting domains still get
`domains/*.md` (13, 14, 15), `calculation/generation/{domain}.yaml`
(word-count and content checks against their own generated analysis text),
and a `templates/generation/*` file — they're generated and checked, just
never assembled into the final document as their own section and never
scored via `report/aggregation`/`semantic/ensemble`. Per `domains/15-
mathematics.md`: "Content lives primarily in `problem-definition`
(formal statement) and `methodology` (derivations, complexity), audited
here as its own domain because mathematical rigor is a distinct failure
mode from either section's structural completeness." Novelty and gaps feed
`introduction`/`methodology`/`discussion` the same way.

`pcems_2026` needs the same 3 for the same reason — a PCEMS paper is still
constructed by identifying novelty and gaps before writing `introduction`,
and still needs `methodology`'s formulas grounded — and adds 2 more that
`base_academic` has no equivalent for at all: `tables` and `figures`.
`pcems_2026/guide/Tables/` (3 files: standards, types, examples) and
`guide/Figures/` (3 files, same shape) are dense with checkable, cross-
cutting craft rules that apply to whichever section actually contains a
table or figure (almost always `findings`, sometimes `methodology`) — e.g.
`Tables/01-table-standards.md`: "Tables must be created using Microsoft
Word table tools... Do not insert tables as images", "Caption: above the
table, Arial, bold". These are exactly the shape of rule `novelty`/`gaps`/
`mathematics` already formalize as cross-cutting (a document-wide quality
concern that isn't itself a heading), just sourced from guide content
instead of generic academic-writing convention.

**Where this differs mechanically from novelty/gaps/mathematics**:
`base_academic`'s 3 cross-cutting domains are populated by analyzing the
*target repo's source code* (`discover-modules` → `gather-module-evidence` →
`module-analysis-{novelty,gaps}` → `persist-module-analysis`/
`persist-cross-module-analysis`, writing into `academic_module_analysis`/
`academic_cross_module_analysis` — confirmed in `plan/usecase/
1-novelty-analysis.md` and `2-gap-analysis.md`, neither of which names any
specific section domain, so both are reusable by `pcems_2026` verbatim, no
pcems-specific copy needed). `tables`/`figures` have no source-code
equivalent to analyze — their checks apply to the *already-drafted*
`findings`/`methodology` manuscript text itself (does a table exist as a
Word table vs. an image, does every table have a caption).

**Explicit answer**: `tables`/`figures` do not need a generated standalone
document the way `novelty`/`gaps`/`mathematics` do (a `novelty` domain
without generation would have nothing to score — `nv-001`'s `word_count_
in_range` needs actual generated text). `tables`/`figures` have no
equivalent "draft" to word-count; they are pure validation of content
`findings`/`methodology` already produced. Concretely: no
`persist-module-analysis`/`academic_cross_module_analysis` row, no
generation usecase, no entry in `_master-schema.yaml`'s assembly step
beyond the `cross_cutting:` list membership itself. Their
`calculation/generation/{tables,figures}.yaml` checks (e.g. `no_image_
tables`, `caption_present`) run as *additional* rows consulted during
`findings`'s and `methodology`'s own `5-audit-det-*` scans (§2.5's existing
usecases, not new ones) — reusing `deterministic_audit.py`'s existing
per-domain scan rather than inventing a new persistence path. This is
still a genuine design decision to confirm before Phase 4 (exactly how
`5-audit-det-findings.md` pulls in a second yaml file's checks isn't
something any existing `base_academic` usecase does today), but the
generation-side question — do they need their own drafted document — is
settled: no.

### 1.2 Domain Count Recap

| Kind | Domains | Gets a heading? | Scored via report/aggregation? |
|---|---|---|---|
| Section (6) | title-and-metadata, introduction, methodology, findings, conclusion, references | Yes | Yes |
| Cross-cutting, repo-analysis-sourced (3) | novelty, gaps, mathematics | No | No |
| Cross-cutting, guide-sourced (2, new — no base_academic precedent) | tables, figures | No | No |

`domains/` therefore needs **11 files**, not 6; `calculation/generation/`
needs **11 files**, not 6; `templates/generation/{markdown,html}/` needs
**22 files**, not 12. `calculation/report/aggregation/domain/` and
`calculation/report/semantic/ensemble/` stay at **6** and **24**
respectively — unaffected, because cross-cutting domains were never in
scope for those two categories (§2.4 below still holds as written).

---

## 2. Target Structure, Category by Category

Every category mirrors `base_academic`'s, scaled from 16 total domains (12
section + novelty/gaps/mathematics/future-scope) down to `pcems_2026`'s 11
(6 section + novelty/gaps/mathematics/tables/figures), with content sourced
from `pcems_2026/guide/` instead of written fresh.

### 2.1 `system.yaml` (new)

```yaml
name: pcems_2026
abstract: false
description: >
  PCEMS 2026 conference-paper system. 6 domains, single-column manuscript,
  Word-native submission. Content standards sourced from guide/. Inherits
  base_academic's shared schema, scripts, and relationship-type vocabulary
  by directory-fallback convention (see below) — not a declared field.
domains:                                    # scored sections only — matches
  - { key: title-and-metadata, sort_order: 1 } # aggregation/domain + semantic/
  - { key: introduction,       sort_order: 2 } # ensemble scope (§2.4). Cross-
  - { key: methodology,        sort_order: 3 } # cutting domains (novelty, gaps,
  - { key: findings,           sort_order: 4 } # mathematics, tables, figures —
  - { key: conclusion,         sort_order: 5 } # §1.1) are NOT listed here, same
  - { key: references,         sort_order: 6 } # as base_academic's own domains:[]
```                                            # never carrying novelty/gaps/mathematics.

**Correction from review**: `extends: base_academic` was in the first draft
of this section as a declared key. `grep -rn "extends" samgraha/system`
across every academic and dev system returns nothing — no `system.yaml`
anywhere in this repo defines or reads an `extends:` field. The inheritance
`base_academic/system.yaml`'s comment describes ("samgraha resolves by
checking the concrete system's directory first, then falling back to
base_academic") is a directory-resolution *convention* the engine applies by
path, not a value read out of `system.yaml`. Dropped the key; kept the
relationship as a description-only note so a reader isn't misled into
thinking it's mechanically enforced by this file.

`pcems_2026` does not have this file today, missing the one file
`base_academic`'s own comment says a concrete system needs so samgraha's
domain-fallback resolution has something concrete to resolve against. Adding
it here is a prerequisite, not scope creep.

### 2.2 `domains/` (11 files, new) — was called `documentation-standards/` pre-refactor

`base_academic/domains/01-title-and-metadata.md` is the shape to match:
`**Domain:**`, `**Audit Target:**`, `## Standard Definition`, `### Expected
Evidence (Deterministic)`, `### Semantic Judgment Criteria`. The 6 section
files are written from `Writing Guide/` (each file's own `> *Source:*` line
per §1's table):

| File | Sourced from |
|------|--------------|
| `01-title-and-metadata.md` | `Writing Guide/02-title-and-metadata.md`, `Conference Guidelines/02-manuscript-structure.md`, `Examples/01-title-examples.md`, `Common Mistakes/01-formatting-mistakes.md` |
| `02-introduction.md` | `Writing Guide/03-introduction.md`, `Examples/02-introduction-examples.md`, `Reviewer Expectations/01-reviewer-criteria.md` |
| `03-methodology.md` | `Writing Guide/04-methodology.md`, `Examples/03-methodology-examples.md` |
| `04-findings.md` | `Writing Guide/05-findings.md`, `Examples/04-findings-examples.md` |
| `05-conclusion.md` | `Writing Guide/06-conclusion.md`, `Examples/05-conclusion-examples.md` |
| `06-references.md` | `Writing Guide/07-references.md`, `Examples/06-reference-examples.md`, `Common Mistakes/03-citation-mistakes.md` |

"Expected Evidence (Deterministic)" rows are drawn from concrete,
checkable rules already sitting in the guide — e.g.
`Checklists/02-per-domain.md`'s CS/ML checklist ("at least 3 baseline methods
compared", "multiple metrics reported") becomes `findings.md`'s deterministic
checks; `Writing Guide/02-title-and-metadata.md`'s "4–6 keywords" becomes a
`min_keyword_count`/`max_keyword_count` rule. "Semantic Judgment Criteria"
are drawn from `Reviewer Expectations/` and `Common Mistakes/`.

The 5 cross-cutting files (§1.1) follow numbering `07`–`11`, matching
`base_academic`'s convention of appending cross-cutting domains after the
section domains (its `13-novelty.md`/`14-gaps.md`/`15-mathematics.md` come
after 12 section files):

| File | Shape to match | Sourced from |
|------|-----------------|--------------|
| `07-novelty.md` | `base_academic/domains/13-novelty.md` verbatim structure | No guide equivalent — generic academic-class standard, reused as written (repo-code novelty, not manuscript-specific) |
| `08-gaps.md` | `base_academic/domains/14-gaps.md` | Same — reused as written |
| `09-mathematics.md` | `base_academic/domains/15-mathematics.md` | Same, cross-checked against `guide/Mathematics/01-equation-formatting.md` + `02-notation-conventions.md` for PCEMS-specific notation rules (e.g. required LaTeX-in-Word conventions) layered on top |
| `10-tables.md` | New — no `base_academic` precedent | `guide/Tables/01-table-standards.md`, `02-table-types.md`, `03-table-examples.md` |
| `11-figures.md` | New — no `base_academic` precedent | `guide/Figures/01-figure-standards.md`, `02-figure-types.md`, `03-figure-examples.md` |

### 2.3 `calculation/generation/{domain}.yaml` (11 files, new)

Shape: `base_academic/calculation/generation/methodology.yaml` (10 checks:
`word_count_in_range`, `min_diagram_count`, `min_formula_count`,
`min_citation_count`, `no_placeholders`, etc.). Word-count bounds and
required-element checks come from each `Writing Guide/*.md`'s own
"Required Elements" list (e.g. `05-findings.md`'s "Experimental Setup: 1
paragraph / Results: 2-4 subsections / Analysis: 1-2 paragraphs" is a
checkable structural rule, not just prose guidance) and from
`Conference Guidelines/03-formatting-guidelines.md`'s page-limit math.

### 2.4 `calculation/report/**` (aggregation/domain, semantic/ensemble, semantic/document.yaml, summary/*, validation/*)

Same shape as `base_academic/calculation/report/`, one
`aggregation/domain/{domain}.yaml` and one `semantic/ensemble/{domain}.yaml`
(+ its 3 stage variants: `-citations`, `-enrichment`, `-budget-fit`) per
domain — 6 + 24 = 30 files instead of base_academic's 12 + 48 = 60.
`summary/final_score.yaml`, `score_bands.yaml`, `trend.yaml`, and
`validation/scoring_validation.yaml` are close to boilerplate (base_academic's
versions are generic weighted-sum/threshold-lookup logic) — copy and rename
`id:`, no new logic needed.

### 2.5 `plan/core/loop.yaml` (1 file, tiers/relationships inlined) + `plan/usecase/*` (55 section-domain-specific + reuse 13 shared usecases + tables/figures gap)

`plan/core/loop.yaml`'s `within_tier_ordering` **already has a worked
pcems_2026 example** (base_academic `plan/core/loop.yaml` lines 22–27):

```yaml
# Example (pcems_2026):
#   - tier: 1
#     from: introduction
#     to: methodology
#     rule: introduction (the stated gap) must complete before methodology is generated/audited
```

`docs/relationship-types.md`'s usage example (lines 30–31) independently
uses the same two domains in the same order plus `findings`:
`introduction --guides--> methodology`, `methodology --validates-->
findings`. Both citations agree on ordering.

**Correction from review**: the first draft proposed a separate
`plan/core/tiers.yaml` alongside `loop.yaml`, modeled on a file this repo's
`eswa_journal` happens to have. `base_academic` itself has no `tiers.yaml` —
its own `plan/core/` contains `loop.yaml` only, and `loop.yaml` has no
`tiers:` key of its own either (it has `within_tier_ordering`, which
assumes tiers exist but doesn't define them). Since this isn't a codebase
being reverse-engineered from an existing multi-file convention — it's a
fresh concrete system with exactly one real file to model against — the
tier grouping and relationship edges are inlined directly into
`pcems_2026/plan/core/loop.yaml` as new top-level keys, keeping `plan/core/`
at **1 file**, matching `base_academic`:

```yaml
# pcems_2026/plan/core/loop.yaml — extends base_academic's loop.yaml shape
# with two keys base_academic's own copy leaves undefined (tiers, relationships),
# since within_tier_ordering has nothing to order without them.

tiers:
  - tier: 1
    domains: [introduction]
  - tier: 2
    domains: [methodology]
  - tier: 3
    domains: [findings]
  - tier: 4
    domains: [conclusion, title-and-metadata]
  - tier: 5
    domains: [references]

relationships:
  - { from: introduction, type: guides,    to: methodology, mandatory: true }
  - { from: methodology,  type: validates, to: findings,    mandatory: true }
  - { from: findings,     type: guides,    to: conclusion,  mandatory: true }
  - { from: methodology,  type: informs,   to: title-and-metadata, mandatory: false }
  - { from: findings,     type: informs,   to: title-and-metadata, mandatory: false }

relationship_types: [guides, requires, validates, informs]

within_tier_ordering: []  # every tier above is single-domain except tier 4
  # (conclusion, title-and-metadata — the two are independent within the
  # tier, per the "informs, mandatory: false" edges above, so no ordering
  # rule is needed between them).
```

`00-domain-relationships.md` (§2.5 below) carries the narrative explanation
of *why* each edge exists; `loop.yaml` carries the machine-readable version
consumed at execution time — same terse-config-vs-narrative-doc split
`base_academic` uses elsewhere (e.g. `calculation/*.yaml` vs. `domains/*.md`).

`title-and-metadata` sharing tier 4 with `conclusion` mirrors
`base_academic`'s own reasoning for why title/abstract-equivalent content
is written last: it needs the paper's actual contribution to already exist
(`domains/01-title-and-metadata.md`: "a title that's vague... undercuts
everything drafted after it" only makes sense once there's something
specific to name). **This tier layout is this proposal's one genuine
judgment call — flagging it for explicit sign-off rather than treating it
as settled.**

`novelty`/`gaps`/`mathematics`/`tables`/`figures` don't appear in `tiers:`
at all — same as `base_academic`, where cross-cutting domains sit outside
the tier system entirely (§1.1). `novelty`/`gaps`/`mathematics` run as an
analysis pass *before* tier 1, the same ordering `base_academic`'s own
`plan/usecase/` numbering implies (`1-novelty-analysis.md`,
`2-gap-analysis.md`, `3a-mathematics-analysis.md` are numbered ahead of
`4a-generate-*`, which is tier-gated) — their output becomes input context
for `introduction`'s and `methodology`'s own generation, not a tiered
dependency of their own. `tables`/`figures` don't run as a pre-pass at all
(§1.1's mechanical-difference note) — they're consulted at whatever point
`findings`/`methodology` are audited, i.e. inside tier 3.

`00-domain-relationships.md` location: `base_academic` itself doesn't have
this file — only its `plan/core/loop.yaml` comment refers to one
(`from/to are the machine-readable domain keys (see
00-domain-relationships.md)`), with no directory prefix, implying it sits
alongside `loop.yaml`'s own reference point rather than nested deeper.
Proposed placement for `pcems_2026/00-domain-relationships.md` is the
**system root** — sibling to `guide/` and `reference/`, not nested under
`plan/` — since it's a content-level cross-domain map (like
`docs/relationship-types.md`'s shared vocabulary), not a per-loop execution
config. Flagging this as a placement default to confirm during review, not
a filesystem-verified fact. The two other stale paths in `loop.yaml` are
handled separately in §2.7 and §2.8 below.

`plan/usecase/`: `base_academic` has one literal file per domain per stage
(`4a-generate-introduction.md`, `4b-cite-introduction.md`, ... — not a
`{domain}`-templated file, an authored file per domain). Reused as-is
(fallback resolution, no pcems copy needed) because they don't name any
specific domain inside: `00-schema-init.md`, `0-classify-repo.md`,
`1-novelty-analysis.md`, `2-gap-analysis.md`, `3a-mathematics-analysis.md`,
`3b-diagram-architecture-analysis.md`, `4e-document-narrative-polish.md`,
`5e-cross-section-semantic-audit.md`, `5f-document-semantic-audit.md`,
`6a-render-charts.md`, `6b-render-audit-report.md`, `6c-render-paper.md`,
`calculate.md` — 13 files. `1-novelty-analysis.md`, `2-gap-analysis.md`, and
`3a-mathematics-analysis.md` in this reused set are exactly the usecases
that produce `novelty`/`gaps`/`mathematics`' cross-cutting content (§1.1) —
no separate pcems copy needed for those 3 domains' generation mechanism.
Needs pcems' own literal copy, one per section domain, for the 9 stages
that do name a domain (`4a-generate`, `4b-cite`, `4c-enrich`, `4d-budget`,
`5-audit-det`, `5a-audit-sem`, `5b-plagiarism`, `5c-humanize-det`,
`5d-humanize-sem`) — 6 × 9 = 54, + `4d-budget-total.md` (document-level, 1)
= **55 new files**.

**Gap, not covered by any reused or new-copy usecase above**: `tables` and
`figures` have no `base_academic` usecase to reuse (no repo-code analysis
applies, per §1.1) and aren't one of the 6 section domains needing an
`4a-9-stage` copy either. A new usecase — something like `3c-table-figure-
craft-audit.md`, run against `findings`'/`methodology`'s already-drafted
text rather than repo source — is needed and doesn't have a precedent
anywhere in `base_academic` to model it on. Left as an open item for Phase
6 rather than designed here.

### 2.6 `prompt/*` — mostly reused, a handful need pcems content

`prompt/semantic-audit/semantic-audit.md`, `prompt/humanize/humanifier.md`,
`prompt/propose/*.md`, `prompt/document-audit/*`, `prompt/cross-section-audit/*`
read their rubric/rule paths from `{domain}` placeholders already — reused
unchanged. `prompt/assemble-paper-structure/generate-section.md` likely needs
a pcems-aware variant only if it hardcodes domain names (needs a read at
implementation time, not blocking this proposal).

### 2.7 `templates/generation/{markdown,html}/{domain}.md` (11 + 11 = 22, new) + `_master-schema.yaml`

**Path correction from review**: `base_academic/plan/core/loop.yaml:57` says
`template: templates/generation/document/{domain}.md`. That directory does
not exist — confirmed (`find templates -maxdepth 2 -type d` on
`base_academic` returns only `templates/generation/html` and
`templates/generation/markdown`, no `document/`). The real, on-disk path is
`templates/generation/{markdown,html}/{domain}.md` — e.g.
`templates/generation/markdown/methodology.md` (named slots: `Overview`,
`Algorithm/Procedure`, `Complexity Analysis`, `Architecture`,
`{{#citations}}` loop — confirmed in
`base_academic-proposal-template-depth-proposal.md` §0). `loop.yaml`'s
`document/` path is stale; `pcems_2026` should use the real `markdown`/
`html` split, and this proposal does not attempt to fix `base_academic`'s
own `loop.yaml` (out of scope here — flag separately if desired). PCEMS
slots for the 6 section domains come straight from each `Writing Guide/
*.md`'s "Required Elements" list — e.g. `findings.md`'s slots are
`Experimental Setup`, `Results Presentation`, `Analysis`. The 5
cross-cutting domains get the same treatment as `base_academic`'s
`novelty.md`/`gaps.md`/`mathematics.md` generation templates for `novelty`/
`gaps`/`mathematics`; `tables`/`figures` templates are new, structured from
`guide/Tables/02-table-types.md` and `guide/Figures/02-figure-types.md`
(each enumerates the types of table/figure a PCEMS paper actually uses —
natural template slots).

`pcems_2026/templates/generation/markdown/_master-schema.yaml` (new,
mirroring `base_academic`'s exactly per §1.1):

```yaml
sections: [title-and-metadata, introduction, methodology, findings,
  conclusion, references]                          # 6 — get a heading
cross_cutting: [novelty, gaps, mathematics, tables, figures]  # 5 — do not
```

### 2.8 `templates/report/{markdown,html}/domain/{domain}/*` (72, new)

**Path correction from review**: `base_academic/plan/core/loop.yaml`'s
`audit: report_templates` key says
`templates/audit/summary/{domain}-report.md`. `base_academic` has no
`templates/audit/` directory at all — that path was never built; it's the
same kind of aspirational reference as `templates/generation/document/` in
§2.7. The real
pattern, confirmed on disk (`base_academic/templates/report/`, 148 files
total across `markdown/` and `html/`), is one directory per domain under
`templates/report/{markdown,html}/domain/{domain}/`, each holding **6 report
types**: `summary.{md,html}`, `deterministic.{md,html}`,
`semantic-full.{md,html}`, `semantic-part.{md,html}`,
`plagiarism.{md,html}`, `humanize.{md,html}` — confirmed by listing
`templates/report/*/domain/methodology/`. That's 6 types × 2 formats × 12
domains = 144 files for `base_academic` (plus 4 document-level files outside
any single domain's folder, totaling the observed 148) and, scaled to
`pcems_2026`'s 6 domains, **6 × 2 × 6 = 72 files**, not the 6 this proposal
originally stated.

Every one of the 6 report types corresponds to a pipeline stage this
proposal already commits to in §2.5 (`5-audit-det` → `deterministic.md`,
`5a-audit-sem` → `semantic-full.md`/`semantic-part.md`, `5b-plagiarism` →
`plagiarism.md`, `5c/5d-humanize-*` → `humanize.md`, plus the always-present
`summary.md`) — so the 72-file count is not new scope, it's the correct
count for the scope already proposed. Same "100% computed fields, zero free
text" discipline as `base_academic/templates/report/markdown/domain/
methodology/summary.md`.

### 2.9 `schema/` and `script/` — reused, not duplicated

This is the one place *not* to mirror file-for-file. `base_academic/schema/*.sql`
(23 files) is explicitly a **read-only reference copy**, not a runtime
dependency — the same convention `python_hackathon/schema/README.md` states
outright: "No runtime dependency on this directory's `.sql` files... the
canonical reference copy of what `hackathon_schema.py`'s `SCHEMA_SQL`
actually creates." The real source of truth is
`script/common/academic_schema.py`'s `ensure_schema()`/table-creation logic,
and `academic_domains` is seeded per-system from `system.yaml`'s own
`domains:` list (§2.1) at `init-schema` time (`03-academic_domains.sql`'s own
comment: "Seeded by init-schema from the concrete system's payload[\"domains\"]").
`pcems_2026` reuses these same 23 tables and the same
`script/common/academic_schema.py` — no new tables, no new columns, just a
different `system.yaml` payload feeding the same schema.

**Samgraha-engine registration** (this is what makes the tables visible to
samgraha outside this repo, at `E:\Python\samgraha\schema\knowledge\
08-custom_data_tables.sql` — the engine's generic `custom_data_tables`
catalog: `standard, table_name, purpose, owner_script_id, shape_json`,
`UNIQUE(standard, table_name)`). `base_academic/script/schema/standard.yaml`
lines 196–236+ carry a `custom_tables:` list, one entry per table
(`table_name`, `purpose`, `owner_script` — matching a `scripts:` entry's
`name:`). `pcems_2026` needs its own `script/schema/standard.yaml` with the
**same 23 `table_name` values** (same physical tables, shared schema) so that
when `pcems_2026` is registered as its own standard
(`mcp__samgraha__register_standard`), the engine's catalog carries a
`standard="pcems_2026"` row for each table alongside the existing
`standard="base_academic"` rows — exactly the mechanism
`python_hackathon/schema/README.md` describes: *"Catalogued... by samgraha's
`custom_data_tables` table, one row per table here, set at `register_standard`
time from `standard.yaml`'s `custom_tables:` list."*

`pcems_2026/script/schema/standard.yaml`'s `scripts:` entries point at
`../../../base_academic/script/...` (reuse) rather than duplicating `.py`
files — the scripts are already domain-parametrized and read whichever
system's `domains`/`calculation`/`prompt` paths are active at runtime.

### 2.10 `docs/relationship-types.md`, `plan/core/` vocabulary — reused

Already shared and already names `pcems_2026` explicitly (§2.5 citation). No
pcems-specific copy needed.

### 2.11 `audit/semantic/document/{domain}.md` (6, new) — closing a gap `base_academic` never closed for itself

**Gap found in review, not previously in this proposal.** `base_academic/
plan/core/loop.yaml:67`'s `audit: semantic_document:` key points at
`audit/semantic/document/{domain}.md`. `prompt/semantic-audit/
semantic-audit.md` reads its scoring rubric from that exact path and
returns `"error": "rubric not found"` if the file is missing (confirmed at
that prompt's own lines ~12, 17, 59). `calculation/report/semantic/
document.yaml`'s `inputs.from` also names this path as its source. None of
this is aspirational the way `templates/generation/document/` (§2.7) or
`templates/audit/summary/` (§2.8) are — `audit/semantic/document/` is on
the *critical path* for the `5a-audit-sem-*` stage this proposal already
commits to building 6 copies of (§2.5's 55-file count includes
`5a-audit-sem-{domain}.md` for every section domain).

**Confirmed**: `base_academic` has no `audit/` directory anywhere in its own
tree. It defined the consuming prompt and the scoring formula that reads
from this path, and never authored the rubric files themselves — its own
semantic audit stage is non-functional today, independent of anything in
this proposal.

For `pcems_2026` this isn't optional to skip, since Phase 6 already builds
the `5a-audit-sem-*` usecases that call into this exact path — building
them against a directory that will never contain anything reproduces
`base_academic`'s dead end for a system this proposal is trying to make
actually run. The fix is cheap: each section domain's `domains/*.md` (§2.2)
already has a `### Semantic Judgment Criteria` section — the rubric content
`audit/semantic/document/{domain}.md` needs already exists, just not yet in
the `criterion_id`/`points`/`mandatory` shape `calculation/report/semantic/
document.yaml`'s `formula` expects (`score = min(100, sum(points) where
passed=true)`). Six files, one per section domain (`01-title-and-metadata.md`
… `06-references.md`), each restating its `domains/*.md` counterpart's
judgment criteria as scored, machine-readable rows. Cross-cutting domains
(§1.1) don't need one — there's no `5a-audit-sem-novelty` (etc.) usecase in
this proposal's scope for them to serve.

Added to Phase 4 (§5) rather than left as a footnote, since it blocks a
stage this proposal already commits to, not a hypothetical future one.

---

## 3. File-Count Summary

All `base_academic` counts below are re-verified against the actual
filesystem (not the domain-count arithmetic from the first draft, which
undercounted in several rows — see corrections inline).

| Category | base_academic (confirmed count) | pcems_2026 (6 section + 5 cross-cutting) |
|---|---|---|
| `system.yaml` | 1 (abstract, `domains: []`) | 1 (new, concrete) |
| `domains/` | 16 (12 sections + novelty/gaps/mathematics + future-scope) | 11 (6 sections + novelty/gaps/mathematics/tables/figures) |
| `calculation/generation/*.yaml` | 15 = 12 sections + novelty + gaps + mathematics. (`future-scope` is domain #16 but has no file in this directory at all — its orphaned `calculation/future-scope.yaml` lives one level up, outside `generation/`, see §4) | 11 (6 sections + novelty/gaps/mathematics/tables/figures) |
| `templates/generation/{markdown,html}/{domain}.*` + `_master-schema.yaml` | 30 (15 domains × 2 formats) + 1 | 22 (11 domains × 2 formats) + 1 |
| `calculation/report/aggregation/domain/*` | 12 (sections only — confirmed: `ls calculation/report/aggregation/domain/*.yaml \| wc -l`) | 6 (sections only — cross-cutting excluded, §1.1) |
| `calculation/report/semantic/ensemble/*` (4 per domain) | 48 (12 sections × 4) | 24 (6 sections × 4) |
| `calculation/report/summary+validation` | 4 | 4 |
| `plan/core/loop.yaml` | 1 (abstract template — no `tiers.yaml`, no `tiers:` key of its own) | 1 (tiers/relationships inlined as new keys, §2.5 correction) |
| `plan/usecase/*` (section-domain-specific: generate/cite/enrich/budget/audit-det/audit-sem/plagiarism/humanize-det/humanize-sem) | 109 (12 sections × 9 stages + 1 `4d-budget-total.md`) | 55 (6 sections × 9 + 1) |
| `plan/usecase/*` (shared, reused unchanged — includes the 3 usecases that generate novelty/gaps/mathematics) | 13 | 0 (reused) |
| `plan/usecase/*` (new — tables/figures craft-audit, undesigned, §2.5) | — (no `base_academic` equivalent) | 1+ (open item, not designed here) |
| `templates/report/{markdown,html}/domain/{domain}/*` (6 report types × 2 formats, sections only) | 144 domain-scoped + 4 document-level = 148 confirmed total | 72 (6 sections × 6 types × 2 formats) |
| `audit/semantic/document/{domain}.md` (§2.11 — gap `base_academic` never closed) | 0 (directory doesn't exist; `5a-audit-sem-*` non-functional today) | 6 (sections only — closes the gap this proposal's own Phase 6 would otherwise reproduce) |
| `schema/*.sql` | 23 (reference copy, not a runtime dependency — see §2.9) | 0 (reused) |
| `script/schema/standard.yaml` `custom_tables:` | 23 entries | 23 entries (own `standard.yaml`) |
| `script/*.py` | ~90 | 0 (reused) |
| `prompt/*` | ~20 | 0–2 (mostly reused) |

**≈215 new files** for `pcems_2026` (≈210 in the prior revision, +6 for
the `audit/semantic/document/` rubric layer in §2.11, -1 for the
`tiers.yaml` correction above — net +5), vs. duplicating none of
`base_academic`'s ~90 Python scripts, 23 schema files, or generic prompts.

---

## 4. Known Inconsistencies to Not Carry Forward

Found while reading the existing pattern; noted so they aren't silently
repeated:

- Two guide files ship with a leading space in their filename
  (` 02-manuscript-structure.md`, ` 06-pdf-compliance.md` per the archived
  `pcems_2026-guide-implementation-proposal.md` §0) — current tree shows them
  without the leading space now, so this looks already fixed; worth a quick
  `ls -la` confirmation at execution time rather than assuming.
- `base_academic/calculation/future-scope.yaml` and
  `domains/16-future-scope.md` are orphaned: `future-scope` is domain #16 in
  `domains/` but has no entry in `calculation/generation/`, no
  `templates/generation/*` file, no `calculation/report/aggregation/domain/`
  or `semantic/ensemble/` entry — it exists in the standard definition but
  was never wired into generation or scoring. Not this proposal's problem to
  fix (pcems_2026 has no `future-scope` domain at all), noted only so the
  same half-wired pattern isn't accidentally reproduced for any pcems
  domain during execution.
- `base_academic/plan/core/loop.yaml`'s two stale template paths
  (`templates/generation/document/{domain}.md`,
  `templates/audit/summary/{domain}-report.md` — see §2.7, §2.8) are a
  pre-existing issue in that file, not something introduced by this
  proposal. `pcems_2026`'s own `loop.yaml` should be authored with the
  correct, real paths from the start rather than copying the stale ones
  forward.

---

## 5. Phases

1. **`system.yaml`** (§2.1) — unblocks domain-fallback resolution; nothing
   else depends on it being wrong.
2. **`domains/` (11 files: 6 sections + 5 cross-cutting)** (§2.2) — content
   foundation everything else cites.
3. **`00-domain-relationships.md` + `plan/core/loop.yaml`** (§2.5, 1 file —
   no separate `tiers.yaml`, corrected from the prior revision) — needs
   `domains/` vocabulary settled first; tier layout flagged for sign-off.
4. **`calculation/generation/*.yaml` + `calculation/report/**` +
   `audit/semantic/document/{domain}.md` (§2.3–2.4, §2.11)** — the rubric
   files are added to this phase rather than left as a footnote, since
   Phase 6's `5a-audit-sem-*` usecases call into them directly; depends on
   `domains/`'s "Expected Evidence" and "Semantic Judgment Criteria"
   sections being concrete enough to encode as checks/scored rows.
5. **`templates/generation/{markdown,html}/**` + `templates/report/
   {markdown,html}/domain/**`** (§2.7–2.8) — depends on
   `calculation/generation/*.yaml`'s check IDs (templates should reflect
   what's actually being checked).
6. **`plan/usecase/*` (55 section-domain files, reusing 13 shared usecases
   unchanged, plus the undesigned tables/figures craft-audit usecase from
   §2.5)** — mechanical for the 55 once 1–5 exist, one file per (section
   domain × stage), same shape as the base_academic file it's modeled on;
   the tables/figures usecase needs its own design pass first (no
   base_academic precedent to copy).
7. **`script/schema/standard.yaml` + `register_standard`** (§2.9) — last,
   since `custom_tables:` and `scripts:` entries reference names/paths
   settled in every prior phase.

Phases 2–4 are the only ones requiring net-new judgment (turning guide prose
into checkable rules); 1, 3, 5–7 are mechanical once their inputs exist.
