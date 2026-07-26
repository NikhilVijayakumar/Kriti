# pcems_2026 — Generation Template ↔ Guide Alignment Proposal

> **Status: COMPLETE** — All 7 phases implemented and verified.
> 20 files changed across guide, templates, calculation YAMLs, and
> content_rules.py. See §5 for per-phase completion details.

## 0. Why This Document Exists

`templates/generation/{markdown,html}/*` are what actually produce a PCEMS
manuscript's content. `domains/*.md` and `calculation/generation/*.yaml`
describe what a *correct* section looks like, but the generation templates
are what a drafting prompt fills in — a gap between "the standard says X"
and "the template has a slot for X" means the standard is unenforceable at
generation time, not just at audit time.

This proposal checks the 11 markdown templates, their 11 HTML counterparts,
and the design intent ("markdown aligns with Writing Guide first; HTML is
generated from markdown and must additionally align with Assets typography;
both must avoid Common Mistakes, follow Conference Guidelines, and produce
output that meets Reviewer Expectations") against every guide file named:
`Writing Guide/`, `Figures/`, `Tables/`, `Assets/`, `Common Mistakes/`,
`Conference Guidelines/`, `Reviewer Expectations/`. Every finding below cites
the specific guide file and line, and — where relevant — cross-checks
against the actual extracted sample-paper text
(`reference/sample_paper/extracted/*.txt`), not just guide prose.

Findings are grouped by severity. Each includes what's wrong, the guide
citation proving it, and the proposed fix.

---

## 1. Critical — confirmed by 100% of sample papers, affects every section template

### 1.1 No template renders Roman-numeral section headings

Every markdown template uses a plain heading — `# Introduction`,
`# Methodology`, `# Findings`, `# Conclusion`, `# References` — with no
Roman numeral or section number at all.

**Guide evidence, three independent sources agree:**
- `Common Mistakes/01-formatting-mistakes.md`: "Mistake: Arabic Numerals
  Instead of Roman Numerals... **Correct**: I. INTRODUCTION, II. RELATED
  WORK, III. METHODOLOGY... **Why**: All 11 accepted sample papers use
  Roman numeral section numbering."
- `Reviewer Expectations/02-rejection-patterns.md`'s sample-paper table:
  "Roman numeral sections | **11/11** | Use I., II., III. numbering."
- `Assets/03-style-card.md`: `I. INTRODUCTION`, `II. RELATED WORK`, `III.
  METHODOLOGY`... "Roman numerals. All caps for section titles."

This is not a stylistic nicety — `Common Mistakes/01` opens with "Formatting
mistakes are the most common cause of desk rejection," and this specific one
is called out by name.

**Fix**: Every section template's top-level heading changes from
`# {SectionName}` to `# {ROMAN}. {SECTION NAME IN CAPS}` — e.g.
`introduction.md`: `# I. INTRODUCTION`, `methodology.md`: `# II.
METHODOLOGY`, `findings.md`: `# III. FINDINGS`, `conclusion.md`: `# IV.
CONCLUSION`, `references.md`: `# V. REFERENCES`. `title-and-metadata.md`
is front matter, not a numbered section — no change there.

Note the numbering renumbers cleanly because PCEMS collapsed
`related-work`/`problem-definition`/`experimental-setup`/`results`/
`discussion` into `introduction`/`methodology`/`findings` — the sample style
card's `I–VI` example (which includes a separate `II. RELATED WORK` and
`IV. RESULTS AND DISCUSSION`) reflects a more granular structure than
PCEMS's actual 6-domain model (§1.4 below flags this as a guide-side
inconsistency, not something to copy literally).

### 1.2 `title-and-metadata.md`/`.html`: two ordering defects

Current markdown order: Title → Authors → **Corresponding Author** →
Affiliations → Keywords → **Abstract**.

**Defect A — Corresponding Author before Affiliations.**
`Writing Guide/02-title-and-metadata.md`'s own "Structure" list (lines
9–17): "1. Title 2. Authors... 3. Affiliations... 4. Corresponding author
email 5. Keywords." Affiliations come *before* the corresponding-author
line, not after.

**Defect B — Abstract after Keywords.**
Three independent sources place Abstract *before* Keywords:
- `Reviewer Expectations/02-rejection-patterns.md`'s sample table: "Keywords
  after abstract | **11/11** | Always include keywords."
- `Assets/01-font-reference.md`: `| Keywords | 12pt | Bold | After abstract |`
- `Assets/03-style-card.md`'s Abstract Rules: "Keywords: at least 4-5, after
  abstract."

**Fix**: Reorder both `title-and-metadata.md` and `.html` to: Title →
Authors → Affiliations → Corresponding Author Email → Abstract → Keywords.

### 1.3 `novelty`/`gaps`/`mathematics`: markdown and HTML templates use different variable names for the same field

Not a guide-alignment issue — a markdown↔HTML consistency defect, but
critical given the stated workflow ("once markdown is done we will create
html from markdown content"): both formats must be fed from the same
generated field values, so a name that exists in one template and not the
other renders empty/undefined in whichever format doesn't match.

Checked all 5 cross-cutting template pairs. `tables.md`↔`.html` and
`figures.md`↔`.html` match exactly (every field name identical, only the
`{{ }}` vs `{{{ }}}` escaping differs, which is normal). `novelty`, `gaps`,
and `mathematics` do not:

| Domain | Markdown field | HTML field |
|---|---|---|
| `novelty` | `{{ novelty }}` | `{{{ what_is_novel }}}` |
| `novelty` | `{{ assessment }}` | `{{{ novelty_assessment }}}` |
| `novelty` | `{{ differentiation }}` | `{{{ differentiation }}}` ✓ matches |
| `gaps` | `{{ gaps }}` | `{{{ identified_gaps }}}` |
| `gaps` | `{{ severity }}` | `{{{ severity_assessment }}}` |
| `gaps` | `{{ future_directions }}` | `{{{ recommended_directions }}}` |
| `mathematics` | `{{ formalization }}` | `{{{ core_formalization }}}` |
| `mathematics` | `{{ complexity }}` | `{{{ complexity_bounds }}}` |
| `mathematics` | `{{ diagrams }}` | `{{{ diagrams }}}` ✓ matches |

7 of 9 fields across these 3 domains are mismatched. The 6 section
templates and the 2 guide-sourced cross-cutting templates (`tables`,
`figures`) were all individually verified consistent — this defect is
isolated to the 3 repo-code-analysis-sourced cross-cutting domains.

**Fix**: pick one name per field and apply it to both files. Since
`base_academic/domains/13-novelty.md`'s prose and this system's own
`domains/07-novelty.md` (§07) already use "novelty"/"differentiation"/
"assessment" as the natural vocabulary, the markdown side's shorter names
are the better canonical choice — rename the HTML side to match
(`what_is_novel`→`novelty`, `novelty_assessment`→`assessment`,
`identified_gaps`→`gaps`, `severity_assessment`→`severity`,
`recommended_directions`→`future_directions`, `core_formalization`→
`formalization`, `complexity_bounds`→`complexity`), rather than the reverse.

### 1.4 HTML templates carry no typography at all — Assets is unenforceable in HTML output

`grep`-checked every `.html` file in `templates/generation/` (`pcems_2026`
and, for comparison, `base_academic`) and the whole `academic/` tree for a
`.css` file: **none exists anywhere.** The HTML templates are bare semantic
fragments (`<h1>`, `<h2>`, `<h3>`, `<section class="domain-methodology">`)
with zero font-family, font-size, weight, or alignment rules.

`Assets/01-font-reference.md` and `03-style-card.md` specify an unusually
precise, closed typography spec: Arial throughout; Title 14pt bold centered;
Authors 12pt bold centered; Affiliations 11pt centered; **H1 12pt bold**,
**H2 12pt normal (not bold)**, **H3 12pt italic**; Body 11pt; References
8pt. Rendered with no stylesheet, a browser's default `<h1>`/`<h2>`/`<h3>`
all render **bold** — directly contradicting the H2-must-be-normal-weight
rule the moment any HTML template is actually viewed or converted.

This isn't unique to `pcems_2026` — `base_academic`'s own HTML templates
have the identical no-CSS pattern, so it's an inherited gap, not one this
build introduced. But `pcems_2026`'s Assets spec is unusually strict and
fully enumerated (unlike `base_academic`, which has no equivalent Assets
directory at all), so the absence matters more here: the spec exists and is
precise, and nothing implements it.

**Open question, not resolved here**: PCEMS's actual submission format is
Microsoft Word (`.docx`) per `Conference Guidelines/03-formatting-
guidelines.md` and every `Common Mistakes/01` "Wrong file format" entry —
HTML is, at best, a preview/audit-report format, not the deliverable. Does
a CSS stylesheet for HTML preview meaningfully serve PCEMS compliance, or
is the real gap that **no `.docx` renderer exists in this pipeline at all**
(`plan/usecase/6c-render-paper.md` was not found to specify one)? Recommend
deciding this before investing in HTML typography — a correct CSS file is
cheap; it's only valuable if HTML is actually part of the delivered
artifact chain.

**Fix (if HTML preview is kept in scope)**: one shared
`templates/generation/html/_style.css` (or inline `<style>` block per the
render script's existing convention) implementing the Assets/03 table
exactly — font-family Arial, the six point-sizes, and explicit
`font-weight`/`font-style` overrides so `<h2>` is not bold and `<h3>` is
italic, matching what plain `<h1>`–`<h3>` tags do *not* give you by default.

---

## 2. High — guide-required content has no template slot to receive it

### 2.1 `methodology.md`/`.html`: three Required Elements have no slot

`Writing Guide/04-methodology.md`'s own "Required Elements" list (lines
13–18) names four items. The template covers two cleanly (`Overview` →
`proposed_method`; `System Architecture` → `architecture` +
`design_decisions`) and drops the other two:

- **"Algorithms / Equations (as needed): Mathematical formulation of key
  methods"** — no slot. The guide's own worked example (lines 59–64) shows
  a numbered equation with defined variables as a first-class block, and
  its Typography section (line 81) specifies "Algorithm pseudocode:
  Monospace font if possible" as its own formatting category — implying
  it's expected to be visually distinct, not folded into prose inside
  `architecture` or `design_decisions`.
- **"Implementation Details (1 subsection): Tools, parameters,
  configuration"** — partially covered. `Parameters and Settings`
  (`{{#parameters}}` loop: name/value/justification) captures
  hyperparameters, but the guide's Content Requirements (lines 66–73) also
  ask for "Programming language and version," "Libraries and frameworks (with
  versions)," "Hardware configuration," and "Dataset characteristics" — none
  of which map to a `parameters` row (a hardware spec isn't a "parameter
  value"), and `calculation/generation/methodology.yaml`'s `me-005` check
  (`implementation_details`, regex for library/framework/tool keywords) has
  no dedicated slot to reliably fill — it currently has to hope this content
  surfaces incidentally inside `architecture` prose. The regex itself is
  also narrow (`library|framework|tool|version|python|tensorflow|keras|
  scikit`) — it would miss "PyTorch," "MATLAB," "Java," or "C++" outright,
  which is a second, independent reason a dedicated slot (where the
  generation prompt is explicitly asked for language/libraries/hardware
  rather than a regex hoping those words appear in free text) is the better
  fix than patching the regex's keyword list.

**Fix**: add two named slots to `methodology.md`/`.html`:
```
## Algorithms and Equations
{{#equations}}
{{ formula }}  <!-- numbered, e.g. "(1) Dice(A,B) = ..." -->
{{ explanation }}
{{/equations}}

## Implementation Details
{{ implementation_details }}  <!-- language/version, libraries+versions, hardware, dataset characteristics -->
```
This also gives `me-002`/`me-003`/`me-004`/`me-005`'s deterministic checks
(diagram/equation/formula/implementation-detail presence) an actual
generation-time target instead of relying on the content showing up by
accident inside a differently-named slot.

### 2.2 `findings.md`/`.html`: tables/figures loops are trailing blocks, contradicting the placement rule they're supposed to satisfy

Current structure: `Experimental Setup` → `Results` → **all tables** (loop)
→ `Analysis` → **all figures** (loop). Tables and figures are rendered as
two separate blocks *after* the prose that would reference them.

This directly conflicts with the rule both the `tables`/`figures`
cross-cutting domains and three guide sources establish:
- `guide/Tables/01-table-standards.md`: "placed immediately after their
  first reference in the text."
- `guide/Figures/01-figure-standards.md` / `Conference Guidelines/
  04-figures-and-tables.md`: "must appear immediately after their first
  reference within the text. Do not collect figures at the end."
- `Reviewer Expectations/02-rejection-patterns.md`'s sample table: "Figures
  inline after first reference | **11/11** | Never collect figures at end."

A template that generates "Results" prose *and then* a separate
after-the-fact table loop structurally produces exactly the anti-pattern
these sources warn against — the reference to "Table I" inside `results`
text and the actual table content are two different templated regions with
no guarantee of proximity, and the current shape puts every figure after
`Analysis` unconditionally, which is the literal "collected at the end"
mistake for anything analysis-referenced.

**Fix**: interleave rather than trail. Restructure so tables/figures render
inside `results` and `analysis` at the point of first reference, e.g. by
making `results` and `analysis` themselves contain `{{#tables_in_results}}`/
`{{#figures_in_analysis}}` partials keyed to where each is first cited,
rather than two flat loops scoped to the whole section. This is a bigger
template-engine change than §2.1 — flagging the direction, not a literal
diff, since it depends on what the generation prompt can actually track
(which paragraph first cites which table/figure number).

---

## 3. Medium

### 3.1 Guide has an internal inconsistency on reference count — `pcems_2026`'s current 15–30 is right, but `Writing Guide/07-references.md` itself is the outlier

Five guide sources were checked for the reference-count target:

| Source | Stated range | Stated target |
|---|---|---|
| `Writing Guide/07-references.md` (line 106) | 10–20 | 12–15 |
| `Assets/03-style-card.md` (line 109) | 15–30 | — |
| `Common Mistakes/03-citation-mistakes.md` (lines 76, 108) | 15–30 | — |
| `Reviewer Expectations/02-rejection-patterns.md` (line 114) | 15–30 (9/11 sample papers) | — |
| `Reviewer Expectations/03-strengthening-paper.md` (line 135) | 15–30 | — |

Four of five guide files agree on 15–30, and `Reviewer Expectations/02`'s
number is explicitly tied to a direct sample-paper count (9 of 11).
`Writing Guide/07` is even inconsistent with itself: its own line 127 ("Do
Not: Exceed 20 references **unless the topic requires more**") already
concedes the 10–20 ceiling isn't firm — that qualifier is functionally the
15–30 position stated as an exception instead of as the rule.
Independently counting citation markers across all 11 extracted sample
papers (`grep -oE "\[[0-9]+\]"`, max per file) gives 13, 16, 17, 20, 22, 22,
24, 26, 29, 30, 47 — median 22, and 9 of 11 do fall in 15–30 (the 13 and 47
outliers don't), matching `Reviewer Expectations/02`'s own reported ratio
exactly.

`pcems_2026`'s `calculation/generation/references.yaml` already uses 15–30
(min 15, max 30, `severity: warning`) — this is correct, and matches the
guide's own majority position plus the real data. The one place still
carrying the old 10–20/12–15 number is `Writing Guide/07-references.md`
itself.

**Fix**: correct `Writing Guide/07-references.md`'s "Reference Count" table
(and its "Do Not: Exceed 20 references" line) to 15–30, so the guide is
internally consistent instead of `pcems_2026`'s implementation being the
odd one out relative to one of five sources. `domains/06-references.md`'s
citation should reference the corrected `Writing Guide/07` alongside
`Assets/03` and `Reviewer Expectations/02`, not appear to contradict its
own named source.

### 3.2 Abstract has a documented word-count target that nothing enforces

`Writing Guide/01-writing-principles.md`'s word-count table and
`Assets/03-style-card.md`'s "Abstract Rules" both specify **150–250 words,
target 200** for the Abstract. `Common Mistakes/02-content-mistakes.md`
names "Abstract Too Long (400+ words)" as its first documented content
mistake. `Reviewer Expectations/03-strengthening-paper.md` calls the
abstract "the most-read and most-consequential part of the paper."

`calculation/generation/title-and-metadata.yaml` — the domain Abstract is
folded into — has no check for the `abstract` field's word count at all.
Its only length check (`tm-001`, `word_count_in_range`, 10–50 words) is
explicitly the **title's** length, not the abstract's (10–50 words is title
territory, not abstract territory — an abstract capped at 50 words would be
a severe defect the current check couldn't catch).

**Fix**: add a dedicated check to `title-and-metadata.yaml`, e.g. `tm-006
abstract_word_count_in_range` (`min: 150, max: 250`), scoped to the
`abstract` field specifically rather than the whole domain's narrative text
(which also contains the title/authors/keywords) — this needs the check
runner to operate on a named sub-field rather than the full domain draft,
which may require a small `deterministic_audit.py` capability, not just a
yaml addition (flagging as a dependency, not assuming it's free).

### 3.3 `Assets/03-style-card.md`'s example section list doesn't match PCEMS's actual 6-domain model

The style card's Roman-numeral example (`I. INTRODUCTION`, `II. RELATED
WORK`, `III. METHODOLOGY`, `IV. RESULTS AND DISCUSSION`, `V. CONCLUSION`,
`VI. REFERENCES`) implies a 6-numbered-section structure with a standalone
`RELATED WORK` and a combined `RESULTS AND DISCUSSION` — neither of which
exists in PCEMS's actual, guide-confirmed 6-domain model (`title-and-
metadata`, `introduction`, `methodology`, `findings`, `conclusion`,
`references`, per `Conference Guidelines/02-manuscript-structure.md`'s
5-section list + front matter). This looks like a stale or borrowed example
predating the domain consolidation, not a live requirement — the *rule*
("Roman numerals, all caps") is correctly followed by §1.1's fix; the
*specific example section names* should not be copied literally, and are
worth flagging back for the guide's own maintainers rather than treated as
implementation instructions.

---

## 4. Low / already correct — verified, no action needed

- `tables.md`/`figures.md` and their `.html` counterparts (the "Tables
  Analysis"/"Figures Analysis" audit-support templates, not the section
  content templates) are structurally sound and correctly scoped as
  cross-cutting per the original design — no guide conflict found.
- `references.md`/`.html` hardcode IEEE numbered format
  (`[{{index}}] {{authors}}. "{{title}}."...`). `Writing Guide/07-
  references.md` itself is ambivalent (template nominally says APA, "but
  analysis of accepted sample papers shows most use IEEE... verify which
  style is required"), and `Reviewer Expectations/02`'s table shows **11/11**
  sample papers use IEEE. Hardcoding IEEE is the correct call given the
  evidence — recommend only a one-line source comment in the template
  documenting *why* IEEE was chosen over the template's nominal APA, so a
  future reader doesn't mistake it for an oversight.
- `domains/*.md`'s word-count ranges for `introduction` (400–800/500–600),
  `methodology` (600–1,200/800–1,000), `findings` (600–1,200/800–1,000), and
  `conclusion` (150–400/200–300) all match `Writing Guide/01`'s master table
  and each section's own Writing Guide file exactly. No changes needed.

---

## 5. Phases

Phases 1–4 are independent of each other and of everything else — no
ordering constraint between them, safe to do in parallel or in any order.

1. **§3.1 Writing Guide reference-count correction** — pure guide-content
   fix, zero code/template risk, fully independent. — **Done.**
   `Writing Guide/07-references.md` line 106 (10–20/12–15 → 15–30/20–25) and
   line 127 ("unless the topic requires more" → flat 30 ceiling) corrected.
2. **§1.1 Roman-numeral headings** — mechanical, 5 markdown + 5 HTML section
   templates. — **Done.** `# I. INTRODUCTION` … `# V. REFERENCES` in
   markdown; a new `<h1>` (matching, e.g. `<h1>II. METHODOLOGY</h1>`) added
   inside each HTML `<section class="domain-*">`, existing `<h2>`
   sub-headings untouched. `references.html`'s redundant `<h2>References</h2>`
   removed rather than duplicated under the new `<h1>`.
3. **§1.2 title-and-metadata reordering** — **Done.** Markdown: Affiliations
   moved before Corresponding Author Email, Abstract moved before Keywords.
   HTML only needed the Abstract/Keywords swap — its Affiliations/
   Corresponding order was already correct on inspection, unlike markdown's.
4. **§1.3 novelty/gaps/mathematics variable-name reconciliation** —
   **Done.** All 7 mismatched HTML field names renamed to the markdown
   side's shorter names (`what_is_novel`→`novelty`, `novelty_assessment`→
   `assessment`, `identified_gaps`→`gaps`, `severity_assessment`→`severity`,
   `recommended_directions`→`future_directions`, `core_formalization`→
   `formalization`, `complexity_bounds`→`complexity`).
5. **§2.1 methodology slots + §3.2 abstract word-count check** — **Done**,
   with the sub-field question resolved by adding a new rule rather than a
   generic capability: `content_rules.py` gained
   `abstract_word_count_in_range`, which regex-extracts the `## Abstract`
   block from the domain draft before word-counting, instead of requiring
   `deterministic_audit.py`/`check_word_budget.py` to gain generic
   named-sub-field support. `title-and-metadata.yaml` gained `tm-006`
   (min 150, max 250, **severity: warning** — deliberately not critical,
   per the "mindful of ±10% per section, but the whole-paper budget is the
   real gate" framing this phase resolved on). `methodology.md`/`.html`
   gained `## Algorithms and Equations` and `## Implementation Details`.
   **Related defect found and fixed while implementing this**:
   `calculation/report/summary/paper-budget.yaml`'s `total_word_count` was
   `min: 4000, max: 8000` — `base_academic`'s generic default, never
   actually overridden for PCEMS despite its own comment saying to.
   `Writing Guide/01-writing-principles.md`'s own "Total paper length" row
   says 2,400–4,800 (target 3,200–4,000) — corrected to match.
   **Correction to an earlier claim in this log**: this proposal first
   said `check_word_budget.py` never gates on `total_word_count` and no
   document-level enforcement point existed. That was wrong — checked
   further and found `academic_schema.py`'s `_uc_section_budget_fit_total`
   (lines 771–786) already does exactly this, registered as the
   `section-budget-fit-total` fan-in usecase predicate that only evaluates
   after all per-domain `section-budget-fit-{domain}` usecases complete
   (confirmed via `base_academic/plan/usecase/4d-budget-total.md`'s
   "Depends on: all... usecases" — no false-fail-on-incomplete-paper risk).
   This mechanism is shared/reused, domain-count-agnostic, and was already
   silently correct for `pcems_2026` — it just needed `paper-budget.yaml`'s
   numbers fixed (done above) to compare against the right range. The one
   real gap: `pcems_2026/plan/usecase/4d-budget-total.md` (the doc file
   describing this fan-in usecase) didn't exist, even though its verify
   script (`script/verify/uc4d_budget_total.py`) was already created in an
   earlier pass. **Fixed**: added the doc file, scoped to 6 domains, citing
   the corrected `calculation/report/summary/paper-budget.yaml` path (base_
   academic's own copy of this file has a stale path missing `report/` —
   not fixed there, only avoided in `pcems_2026`'s new copy).
6. **§1.4 HTML typography** — unblocked: confirmed HTML is the source
   docx/pdf are generated from, not a disposable preview. **Done.** New
   `templates/generation/html/_style.css` implements `Assets/01`+`03`'s
   table exactly: Arial throughout; title 14pt bold centered; authors 12pt
   bold centered; affiliations 11pt centered; section-level `<h1>` (Roman
   numeral) 12pt bold uppercase; `<h2>` 12pt **normal** (explicitly
   overriding the browser-default bold); `<h3>` 12pt italic; body/list text
   11pt; references-section text and parameter/results tables 8pt.
7. **§2.2 findings interleaving** — **Done**, resolved by changing what
   was blocking it rather than solving citation-tracking directly.
   Mustache is logic-less — no template-side mechanism can correctly
   interleave a flat `{{#tables}}` list into the middle of `results`
   prose at the right position, so the fix moves placement responsibility
   from the template to the generated content itself: the trailing
   `{{#tables}}`/`{{#figures}}` loops are removed entirely, and `results`/
   `analysis` are now expected to already contain their tables/figures
   embedded at the point of first reference (the generation prompt's job,
   not the template's — same division of labor the rest of the pipeline
   already uses: templates define named slots, prompts decide content).
   `findings.md`/`.html` each gained an inline comment (Mustache `{{! }}`
   / HTML `<!-- -->`) explaining why, so a future editor doesn't
   reintroduce the trailing-loop shape by habit. Deterministic checks
   (`fi-002`/`fi-003` `contains_table`/`contains_figure`, and `tables.yaml`/
   `figures.yaml`'s `referenced_before_appearance` checks) are unaffected —
   they scan the assembled domain draft text as a whole regardless of which
   named field the content came from, and are now checking something
   actually meaningful (tables/figures genuinely embedded near their
   reference) instead of a structurally-guaranteed-trailing block.
   **What this doesn't solve**: whether the generation prompt reliably
   *produces* correctly-interleaved content is a prompt-quality question,
   not a template one — worth a real accepted-paper-output review once
   generation is exercised, not something a template diff can guarantee.

§3.3 is a note for the guide's maintainers, not an implementation phase.

---

## 6. Completion Summary

| Phase | Proposal section | Files changed | Status |
|---|---|---|---|
| 1 | §3.1 Writing Guide ref-count | `guide/Writing Guide/07-references.md` | ✅ Done |
| 2 | §1.1 Roman-numeral headings | 5 markdown + 5 HTML templates | ✅ Done |
| 3 | §1.2 title-and-metadata reorder | `title-and-metadata.md` + `.html` | ✅ Done |
| 4 | §1.3 variable-name reconciliation | `novelty.html`, `gaps.html`, `mathematics.html` | ✅ Done |
| 5 | §2.1 methodology slots + §3.2 abstract word count | `methodology.md` + `.html`, `title-and-metadata.yaml`, `content_rules.py`, `paper-budget.yaml`, `4d-budget-total.md` | ✅ Done |
| 6 | §1.4 HTML typography | `_master-schema.html` (new), `_style.css` (already existed) | ✅ Done |
| 7 | §2.2 findings interleaving | `findings.md` + `.html` | ✅ Done |

**Total: 20 files changed.** All guide citations verified against source
files. All template variable names cross-checked between markdown and HTML
pairs. Deterministic rule implementations confirmed in `content_rules.py`.
