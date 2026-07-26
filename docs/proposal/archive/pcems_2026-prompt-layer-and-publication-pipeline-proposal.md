# pcems_2026 — Own Prompt Layer, Corner-Case Audit Coverage, and Publication Pipeline Proposal

## 0. Why This Document Exists, and Why the Earlier Decision Reverses

The system-build proposal (`pcems_2026-full-system-implementation-proposal.md`)
had `pcems_2026` reuse `base_academic/prompt/*` unchanged — 24 `location:`
entries in `script/schema/standard.yaml` pointing at
`../../../base_academic/prompt/...`, on the reasoning that prompts are
generic and domain-parametrized.

That reasoning is wrong for `pcems_2026` specifically, for two reasons this
proposal's requester gave directly:

1. **Isolation.** If `base_academic/prompt/*` changes for any reason —
   someone else's system needs different wording, a bug fix, a rewrite —
   `pcems_2026` breaks with it, silently, with no local copy to fall back
   to. A concrete system's content should not be hostage to an abstract
   parent's edits.
2. **`pcems_2026` has its own guide, and `base_academic` doesn't.**
   `base_academic/prompt/assemble-paper-structure/generate-section.md`
   grounds its generation instructions in "analysis docs or implementation
   evidence" — repo-introspection language, because `base_academic` has no
   equivalent of `guide/Writing Guide/`, `guide/Examples/`,
   `guide/Common Mistakes/`, or `guide/Reviewer Expectations/`. Reusing that
   prompt means `pcems_2026`'s generation is grounded in generic academic
   convention instead of the 45-file, sample-paper-verified knowledge base
   this system actually has. That's a strictly worse prompt for this system
   to run, even before considering the isolation risk.

`pcems_2026` gets its own `prompt/` tree, organized into the same three
kinds `templates/` already uses (`generation/`, `report`→here `audit/`,
`proposal`→here `propose/`), content written from `pcems_2026/guide/`
directly.

---

## 1. Target Structure: `prompt/{generation,audit,propose}/`

### 1.1 `prompt/generation/{domain}.md` — 9 files

One per domain that actually gets generated content (6 sections + the 3
repo-analysis cross-cutting domains; `tables`/`figures` are validation-only,
established in the earlier alignment proposal §1.1 — no generation prompt
for them).

| File | Primary guide sources | Must avoid (Common Mistakes) | Must satisfy (Reviewer Expectations) |
|---|---|---|---|
| `title-and-metadata.md` | `Writing Guide/02`, `Conference Guidelines/02+03`, `Assets/01+03`, `Examples/01-title-examples.md` | `01-formatting-mistakes.md` (font/size), `02-content-mistakes.md`'s Abstract Mistakes | Rejection Patterns' "Structural Missing" (no abstract, >250 words, no keywords) |
| `introduction.md` | `Writing Guide/03`, `Examples/02-introduction-examples.md` | `02-content-mistakes.md`'s Introduction Mistakes ("vague problem statement," "too broad opening") | "Unclear Contribution" pattern; Strengthening/Introduction Checklist (6 items) |
| `methodology.md` | `Writing Guide/04`, `Examples/03-methodology-examples.md`, `Mathematics/01+02` | `02-content-mistakes.md`'s Methodology Mistakes (missing hardware/hyperparameters) | "Insufficient Methodology" pattern; Strengthening/Methodology's 6-row "Required Details" table |
| `findings.md` | `Writing Guide/05`, `Examples/04-findings-examples.md`, `Tables/*`, `Figures/*` | `02-content-mistakes.md`'s Results Mistakes (no baseline, "best" without evidence) | "Weak or Missing Evaluation" pattern; ≥3 baselines, multiple metrics |
| `conclusion.md` | `Writing Guide/06`, `Examples/05-conclusion-examples.md` | `02-content-mistakes.md`'s Conclusion Mistakes (new results, verbatim abstract repeat) | Conclusion Anti-Patterns list (4 items) |
| `references.md` | `Writing Guide/07` (now corrected to 15–30), `Examples/06-reference-examples.md` | `03-citation-mistakes.md` (all subsections) | Reference Quality Checklist (7 items) |
| `novelty.md`, `gaps.md` | No guide equivalent — these are repo-code-analysis domains (§1.1 of the system-build proposal), content stays generic since PCEMS's guide doesn't discuss "novelty analysis of a codebase." Kept structurally identical to `base_academic/domains/13`/`14`'s approach. | — | — |
| `mathematics.md` | `Mathematics/01-equation-formatting.md`, `02-notation-conventions.md`, `03-math-examples.md` | — | — |

Every one of the 6 section prompts must additionally instruct: (a) avoid
the `Writing Guide/01`'s "AI-Generated Language Flags" list and
`Common Mistakes/04-language-mistakes.md`'s full word-substitution tables
(delve, tapestry, landscape, crucial, paramount, pivotal, leverage,
harness, robust-when-overused), (b) match the register demonstrated in the
relevant `Examples/*` excerpts — these are real accepted-paper sentences,
the closest thing to ground truth this system has for "what good actually
looks like," not just abstract rules.

### 1.2 `prompt/audit/` — reorganized by audit scope, not by base_academic's flat category names

```
prompt/audit/
├── semantic-document/{domain}.md   (6 — one per section domain)
├── cross-section-semantic-audit.md (1)
├── document-semantic-audit.md      (1)
├── plagiarism-fingerprint-audit.md (1)
└── humanifier.md                   (1)
```

Same shape as `base_academic`'s `semantic-audit/`, `cross-section-audit/`,
`document-audit/`, `plagiarism-forensic-audit/`, `humanize/` directories —
consolidated one level, and every file's content grounded in PCEMS's guide
instead of generic academic-writing rubric language. See §2 for what
"grounded in the guide" means concretely for each.

### 1.3 `prompt/propose/` — 4 files, one new kind added

```
prompt/propose/
├── generation-proposal.md          (whole-run, same shape as base_academic's)
├── section-generation-proposal.md  (NEW — see §3)
├── audit-proposal.md
└── fix-proposal.md
```

**Correction from review**: the first draft of this list included
`report-proposal.md`, copied from `base_academic/prompt/propose/`'s 4
files on disk without checking whether it's actually wired to anything.
It isn't. `base_academic/script/schema/standard.yaml` (lines 812–820)
documents this explicitly: `propose-report`'s usecase is 3 deterministic
steps only (`gather-proposal-context` → `persist-proposal` →
`render-proposal`), no `prompt:` step, with the comment spelling out why —
"render-charts/render-audit-report/render-paper are 100% script+template+DB
(no LLM step anywhere in that chain)... every fact in a report proposal is
already computed by `gather-proposal-context` — nothing for a model to
judge." Its own `prompts:` list (lines 181–183) has a matching comment:
"propose-report has no prompt — deterministic-only." `report-proposal.md`
exists as a file in `base_academic/prompt/propose/` but is never referenced
by `standard.yaml`'s `prompts:` list — an orphan, same category as
`calculation/future-scope.yaml` flagged in an earlier proposal. The same
reasoning applies identically to `pcems_2026` (report proposals restate
computed scores/report-kind lists regardless of which concrete system —
nothing PCEMS-specific changes this), so `pcems_2026` should not create
this file at all, not even as a copy — creating it would just reproduce
the same orphan.

`section-generation-proposal.md` is the new artifact requested — see §3
for its full design, it doesn't have a `base_academic` equivalent to model
structurally beyond the shared Role/Input/Task/Rules/Output-Format shape
every other prompt in this repo already uses.

**Total new content**: 9 (generation) + 9 (audit) + 4 (propose) = **22
prompt files**, replacing 24 reused `location:` references in
`script/schema/standard.yaml` (the count is close but not required to
match 1:1 — the reorganization consolidates some base_academic categories,
e.g. `semantic-audit/` + `document-audit/` + `cross-section-audit/` +
`plagiarism-forensic-audit/` + `humanize/`, five directories, into one
`prompt/audit/` tree).

---

## 2. Corner-Case Audit Coverage — "check all possible corner cases... section-wise, cross-section, entire document, plagiarism, humanizer"

This is a coverage matrix, not just a restructure. Each audit layer needs
its corner cases named explicitly, sourced from the guide, not left
implicit the way `base_academic`'s generic audit prompts leave them.

### 2.1 Per-section (`prompt/audit/semantic-document/{domain}.md`)

Already partially covered by `audit/semantic/document/{domain}.md`'s
scoring criteria (built in the earlier proposal). The *prompt* wrapping
that rubric needs to additionally instruct the model to check for the
specific failure patterns `Reviewer Expectations/02-rejection-patterns.md`
names per section — e.g. for `methodology`, explicitly check the 5
"Common omissions" it lists (dataset preprocessing, hyperparameters,
training configuration, hardware, random seed/cross-validation) as
corner cases beyond the rubric's own criteria, since a model scoring
generically against "is there enough detail" will miss specific omissions
a checklist names explicitly.

### 2.2 Cross-section (`prompt/audit/cross-section-semantic-audit.md`)

`base_academic`'s version checks terminology consistency, claim-vs-evidence
alignment, narrative arc, number consistency — generic and reusable as a
starting shape, but PCEMS's guide names sharper, checkable cross-section
corner cases to add:

- **Gap↔contribution↔conclusion triangle** (`Philosophy`'s "contribution
  should remain visible... across Introduction, Methodology, Experimental
  Evaluation, Results, Conclusion" + `Common Mistakes/02`'s "Repeating
  Abstract Verbatim" in conclusion): does `introduction`'s stated gap match
  what `methodology` actually addresses, what `findings` actually shows,
  and what `conclusion` actually restates — four-way consistency, not just
  two-way.
- **Word budget cross-check**: does `findings`' claimed metrics match
  `title-and-metadata`'s abstract numbers exactly (`Reviewer Expectations/
  03`'s Abstract weakness table: "Experiments show good results" vs.
  "99.95% accuracy, improving the baseline by 0.05%" — the *specific
  number* must match between abstract and findings, not just both being
  present).
- **Citation-figure-table numbering collision** (`Checklists/03-final-
  review.md`: "No citation overlaps with figure/table numbers") — a
  cross-section concern because citation numbers are assigned globally
  across all sections' first-reference order.

### 2.3 Whole-document (`prompt/audit/document-semantic-audit.md`)

`base_academic`'s version checks gap closure, methodology-results
alignment, readability, completeness, abstract accuracy — add PCEMS's own
**Pre-Revision Assessment** rubric directly:
`Reviewer Expectations/03-strengthening-paper.md`'s 6-dimension table
(Contribution clarity / Methodology detail / Results strength / Writing
quality / Literature coverage / Formatting compliance, each scored 1–3,
total interpreted as Major/Targeted/Minor revision needed) — this is a
**document-level scoring rubric PCEMS's own guide already defines**; the
document-semantic-audit prompt should compute and report against it
directly rather than inventing its own scoring dimensions from scratch.

### 2.4 Plagiarism / AI-fingerprint (`prompt/audit/plagiarism-fingerprint-audit.md`)

`base_academic`'s 6 fingerprint patterns (low burstiness, hollow claims,
mechanical structure, template phrases, semantic saturation, missing
hedging) are sound and reusable as the pattern taxonomy — but the *word
lists* should be PCEMS's own, which are considerably more specific:
`Writing Guide/01`'s "AI-Generated Language Flags" + `Common Mistakes/
04-language-mistakes.md`'s full three-tier list (High-Risk: delve,
landscape, tapestry, crucial, paramount, pivotal, "it is worth noting";
Medium-Risk: leverage, harness, unlock, robust, novel-when-unjustified,
comprehensive). Also add: `Common Mistakes/02`'s "Plagiarism and
Originality" desk-rejection triggers (excessive similarity, self-plagiarism
without citation, missing acknowledgment of prior versions) as a distinct
check category this domain's audit doesn't currently cover at all —
`base_academic`'s fingerprint audit only checks *AI-generated* patterns, not
*copied-from-elsewhere* patterns, and PCEMS's guide names both as desk
rejection triggers.

### 2.5 Humanizer (`prompt/audit/humanifier.md`)

`base_academic`'s 3-layer fix strategy (structural rhythm, technical DNA
injection, voice restoration) is a sound mechanism — ground its
"Technical DNA Injection" layer (replacing generic claims with exact
numbers) in PCEMS's own worked example:
`Reviewer Expectations/03`'s abstract-weakness table already shows the
exact transformation this layer should perform ("Experiments show good
results" → "Experiments on 284,807 transactions show 99.95% accuracy").

---

## 3. New Artifact: Per-Section Generation Proposal

`prompt/propose/section-generation-proposal.md` — requested directly:
"generation proposal per section which should include what all steps we
should do both deterministic and semantic and how to do it with phasewise
plan combining deterministic and semantic from start to end."

`base_academic/prompt/propose/generation-proposal.md` is whole-run and
shallow by design ("one or two sentences" per domain, explicitly not
detailed — a reviewer approving 6-11 one-line claims at once). This new
artifact is the opposite: one domain, full depth, run before that domain's
9-stage pipeline (`4a-generate` → `4b-cite` → `4c-enrich` → `4d-budget` →
`5-audit-det` → `5a-audit-sem` → `5b-plagiarism` → `5c-humanize-det` →
`5d-humanize-sem`) begins.

**Proposed shape**:

```markdown
# Section Generation Proposal — {{ domain }}

## Role
You are proposing the full generation-through-audit plan for one domain
before any of its 9 pipeline stages run.

## Input
- `domain`, `domain_standard` (domains/{NN}-{domain}.md's Standard Definition)
- `deterministic_checks` (calculation/generation/{domain}.yaml, full list)
- `semantic_criteria` (audit/semantic/document/{domain}.md, full rubric)
- `guide_sources`: the specific Writing Guide + Examples + Common Mistakes
  + Reviewer Expectations files this domain's prompt.md cites (§1.1's table)
- `upstream_context`: completed upstream-tier domains' content

## Task
For this one domain, produce a phase-by-phase plan covering:
1. **Generate**: what evidence/guide sources ground the initial draft,
   which Examples/* pattern the structure will follow
2. **Cite**: which claims need citation support, how many (per this
   domain's citation-count deterministic check)
3. **Enrich**: what tables/figures/equations this domain needs (cross-
   referencing tables.yaml/figures.yaml/mathematics.yaml's checks if this
   domain is where those crafts land)
4. **Budget-fit**: the word-count range this domain must land in, and
   this run's plan if the draft risks over/under
5. **Audit-det**: name each deterministic check by ID and what evidence
   in the planned draft will satisfy it
6. **Audit-sem**: name each semantic criterion by ID and what the planned
   draft's content will do to earn its points
7. **Plagiarism/Humanize**: which of the 6 AI-fingerprint patterns this
   domain's typical content is most at risk for (e.g. `methodology`
   risks "template phrases" in tool/parameter listings; `introduction`
   risks "hollow claims" in the gap statement)

## Rules
1. Reference deterministic check IDs and semantic criterion IDs by name —
   a reviewer should be able to trace every claim in this proposal back
   to a specific rule, not prose restating what the rules already say
2. If `upstream_context` is empty for a domain that requires it (e.g.
   `methodology` before `introduction` completes), say so and note the
   plan is provisional
3. This proposal covers ALL 9 stages before any of them run — approval
   gates the entire chain for this domain, not stage-by-stage

## Output Format
[same JSON shape as generation-proposal.md: summary, content_md,
computed_context — content_md follows the 7-part structure above]
```

This needs a matching `templates/proposal/markdown/section-generation.md`
(and `.html`) — not designed here, flagged as a dependency of implementing
this file, same "propose-then-approve" gate the rest of the pipeline uses
(`docs/proposal/base_academic-proposal-gate-workflow-proposal.md`).

---

## 4. Quality Benchmark: Sample Papers + Real Template — Confirmed Gap

The requirement is explicit: generated output quality must equal or exceed
`reference/sample_paper/` and follow
`reference/template/Template_PCEMS2026.docx.pdf`.

**Checked**: `reference/sample_paper/extracted/` has all 11 sample papers
as `.txt` — this is the ground truth `Examples/*`, `Common Mistakes/*`, and
this proposal's own citation-count/figure-count numbers were derived from
(confirmed throughout the earlier alignment proposal).

**Gap found**: `reference/template/` has only the raw
`Template_PCEMS2026.docx.pdf` — **no extracted text exists for it**, unlike
the sample papers. Attempted to read it directly with the `Read` tool's PDF
support; failed — `pdftoppm is not installed` (poppler-utils missing in
this environment). This means:

- `Conference Guidelines/*`'s claim to be "extracted from the PCEMS 2026
  Template PDF" cannot be independently re-verified in this environment
  right now — there's no `reference/template/extracted/*.txt` to diff
  against, the way sample-paper claims could be checked against
  `extracted/*.txt` throughout this and the prior proposal.
- Any automated "does generated output match the template's actual layout"
  check needs the template's real content (margins, exact page limit,
  actual copyright-notice text, actual header/footer requirements) — none
  of which this system can currently verify weren't paraphrased or
  mis-transcribed when `Conference Guidelines/*` was first written.

**Recommendation**: before building the generation/audit prompts in §1–2,
extract `Template_PCEMS2026.docx.pdf` to text (install `poppler-utils`, or
convert via a Word-native tool, or run this in an environment that has PDF
tooling) and diff the result against `Conference Guidelines/*`'s claims.
This is cheap and blocks nothing else in this proposal, but skipping it
means `Conference Guidelines/*`'s formatting rules — which every generation
and audit prompt in §1–2 depends on — carry unverified provenance.

---

## 5. Output Pipeline: HTML → DOCX + PDF — Currently 100% Unbuilt

Checked for the actual rendering scripts the "create both pdf and docx
output using html" requirement needs. Found the target design already
written down, never implemented:

`base_academic/plan/usecase/6c-render-paper.md`:
> **Script**: `assemble-final-document.py` + `extract-mermaid-images.py` +
> `render-docx.py` (**planned, not yet built**)
>
> **Action**: Concatenate domain drafts... render through HTML template,
> shell to `pandoc` for DOCX, playwright for PDF.

**Confirmed**: none of these three scripts exist anywhere in
`samgraha/system/academic/` (`find`/`grep` both empty). `pandoc` and
`playwright` are named exactly once in the whole repo — in this one
aspirational usecase doc. `script/render-audit-report/` (the one render
directory that does exist) only has `generate_audit_report.py` and
`render_charts.py` — audit-report rendering, not paper rendering.

This is not a `pcems_2026`-specific gap — `base_academic` doesn't have this
either, and per the reuse pattern established for `script/*.py`, `pcems_2026`
would inherit whichever version exists there. Right now that's nothing.
**Building this is real, substantial, previously-unbuilt work**, not
something available to reuse:

1. `assemble-final-document.py` — reads `_master-schema.yaml`'s `sections:`
   order, concatenates each domain's latest narrative into one document,
   renders through `templates/generation/html/_master-schema.html` (built
   in the prior proposal). Cross-cutting domains' content gets woven into
   their target sections per each cross-cutting domain's `domains/*.md`
   "Content lives primarily in..." note — this weaving logic doesn't exist
   yet either and needs its own design (which cross-cutting content goes
   into which section's assembly, and where within it).
2. `extract-mermaid-images.py` — rasterizes any mermaid diagram fences in
   the assembled content (relevant mainly for `methodology`'s architecture
   diagrams) before DOCX/PDF conversion, since neither format renders
   mermaid natively.
3. `render-docx.py` — shells to `pandoc` (`pandoc input.html -o output.docx`
   is the minimal form; getting `Assets/01`'s exact font/size spec to
   survive the conversion needs a pandoc reference-doc — a `.docx` template
   with the correct styles pre-defined, which itself should probably be
   derived from `Template_PCEMS2026.docx.pdf`, tying back to §4's gap).
4. **PDF renderer** (`render-pdf.py`, not named in the usecase doc but
   implied by "playwright for PDF") — headless-browser-prints the same
   assembled HTML (with `_style.css` applied) to PDF. Playwright is not
   currently a dependency anywhere in this repo — confirm it's an
   acceptable new dependency before building against it, or consider
   `weasyprint`/`wkhtmltopdf` as lighter alternatives if Playwright's
   browser-download footprint is unwanted for a CI/CLI tool.

**This is the single largest remaining piece of work this proposal
surfaces** — everything in §1–3 produces correct *content*; without this,
none of it reaches the two formats actually required for submission.

---

## 6. Phases

1. **§4 template extraction** — cheapest, blocks nothing else, but every
   later phase's formatting claims are unverified until this runs.
2. **§1.1 `prompt/generation/*`** (9 files) — content-heavy but mechanical
   once §4 either confirms or corrects `Conference Guidelines/*`.
3. **§1.2 `prompt/audit/*`** (9 files) + **§2**'s corner-case additions —
   depends on §1.1 existing (audit prompts reference the same guide
   sources generation prompts cite, for consistency).
4. **§1.3 `prompt/propose/*`** (4 files, including the new
   `section-generation-proposal.md` from §3) + its matching
   `templates/proposal/markdown/section-generation.md` — depends on §1.1
   and §1.2's content existing to reference by name.
5. **`script/schema/standard.yaml` update** — remove the 24
   `base_academic/prompt` `location:` entries, point at the new local
   `prompt/{generation,audit,propose}/*` paths instead.
6. **§5 rendering pipeline** — the largest, independent of 1–5 in content
   terms but blocking for actually producing a submittable file; can start
   in parallel with 1–4 since it operates on whatever HTML content already
   exists, real or placeholder, to validate the mechanism.

Phase 6 is large enough that it likely warrants its own follow-up proposal
once a rendering approach (pandoc/playwright vs. alternatives) is chosen —
flagged here rather than designed to file-level detail, consistent with
how this proposal treats every other multi-unknown item.
