# pcems_2026 — Production-Readiness Gaps Proposal

## 0. Why This Document Exists

The prior proposals in this repo built and verified `pcems_2026`'s content
engine end to end: domains, calculation/audit rules, semantic rubrics, and
a guide-grounded prompt layer for generation, plagiarism, and humanize
(all confirmed working across multiple verification passes). The
feasibility assessment that preceded this document asked the direct
question — "if I register this standard against a real docs repo, can I
get an in-depth PCEMS paper out, matching the sample papers, following the
real template, as PDF and DOCX, then audit-and-fix it?" — and the honest
answer was: the content engine, yes; the actual deliverable, not yet, for
two hard blockers and four things worth checking first.

This proposal is the fix list for all six, plus two optimization items
found along the way that aren't blockers but are worth closing while in
this part of the system.

---

## 1. Blocker: No DOCX/PDF Renderer Exists

Confirmed in the prior assessment: `assemble-final-document.py`,
`extract-mermaid-images.py`, and `render-docx.py` — the three scripts
`plan/usecase/6c-render-paper.md` names — do not exist anywhere in
`samgraha/system/academic/`. Neither does a PDF renderer. `pandoc` and
`playwright` are named exactly once in the whole repo, in that one
aspirational doc.

### 1.1 `assemble-final-document.py`

**Inputs**: `templates/generation/markdown/_master-schema.yaml`'s
`sections:` order (6 domains), each domain's latest `academic_narratives`
row (post-humanize, highest iteration), and the 3 cross-cutting domains'
content (`novelty`, `gaps`, `mathematics` — stored via
`academic_module_analysis`/`academic_cross_module_analysis`, not
`academic_narratives`, per the system-build proposal's §1.1 distinction).

**The unsolved design piece**: cross-cutting content needs to be *woven
into* whichever structural section it belongs to (per each cross-cutting
domain's `domains/*.md` "Content lives primarily in..." note —
`novelty`→`introduction`/`methodology`, `gaps`→`introduction`, `mathematics`
→`methodology`), not appended as its own heading. This weaving has never
been designed at the mechanism level, only stated as an intent. Concretely
this script needs to:
1. Concatenate the 6 structural domains in `_master-schema.yaml` order.
2. For each cross-cutting domain, locate its target section(s) and insert
   its content at a defined point — simplest defensible approach: append
   as a labeled sub-block at the end of the target section's own content
   (e.g. `## Novelty Positioning` inside `introduction`), not literally
   interleaved sentence-by-sentence, since sentence-level interleaving
   would require NLP alignment this system has no component for.

   **Flagged in review as under-specified — real open decisions, not yet
   resolved by this proposal**: (a) the three cross-cutting domains' own
   `domains/*.md` files disagree in phrasing about their target —
   `07-novelty.md` says content is "woven into" `introduction`
   (implying multiple insertion points), `09-mathematics.md` says content
   "lives primarily in" `methodology` (implying one primary home) — these
   need a single consistent placement rule, not two different verbs
   pointing at different mechanisms; (b) which exact point within a target
   section — end of section, after a specific named heading, before the
   section's own closing paragraph? Not decided; (c) no defined behavior
   when cross-cutting content is long relative to a short target section
   (does it get budget-fit-trimmed the way structural domains are, or does
   it bypass `calculation/generation/{domain}.yaml`'s word-count check
   entirely since it's appended after that check already ran on the
   structural section alone?). None of these are resolved here — they're
   real design decisions the implementation of 1.1 will have to make, not
   details this proposal is deferring casually.
3. Render the concatenated markdown into
   `templates/generation/html/_master-schema.html`'s `{{{ assembled_sections }}}`
   slot, running each domain's own HTML fragment template
   (`templates/generation/html/{domain}.html`) rather than raw markdown,
   so `_style.css` typography (built in the alignment proposal) actually
   applies.

### 1.2 `extract-mermaid-images.py`

Rasterizes any mermaid fences (mainly `methodology`'s architecture
diagrams, per `calculation/generation/methodology.yaml`'s
`contains_mermaid_diagram` check) before DOCX/PDF conversion — neither
format renders mermaid natively. Needs `mmdc` (mermaid-cli) available;
`plan/usecase/6c-render-paper.md`'s own note says "hard-fail if `mmdc`
unavailable" — confirm this dependency is acceptable before building
against it, or fall back to a hosted mermaid-render API if a CLI
dependency is unwanted.

### 1.3 `render-docx.py`

Minimal form is `pandoc assembled.html -o output.docx`. Getting
`Assets/01`'s exact font/size spec (Arial 14/12/11/8pt, H1 bold/H2 normal/
H3 italic — same spec `_style.css` already encodes for HTML) to survive
the conversion needs a **pandoc reference doc** — a `.docx` file with those
styles pre-defined that pandoc uses as the style source
(`--reference-doc=pcems-reference.docx`). This reference `.docx` should be
derived from `Template_PCEMS2026.docx.pdf` directly (§4 below) rather than
hand-built from `Assets/*`'s prose description, so it's provably the real
template's styling, not a paraphrase of it.

### 1.4 PDF renderer (not yet named as a script anywhere)

`6c-render-paper.md` says "playwright for PDF" but doesn't name a script.

**Correction from review**: the first draft of this section said
Playwright "is not currently a dependency anywhere in this repo" and
suggested weighing it against `weasyprint`/`wkhtmltopdf` before committing.
That was wrong — checked and found `python_hackathon/script/usecase-7-pdf/
export_team_pdfs.py` already uses it successfully: `from playwright.sync_api
import sync_playwright`, then `with sync_playwright() as p: ... page.pdf(
path=temp_pdf, ...)`, merging per-page PDFs with `pypdf.PdfWriter`. This is
a known-good, already-installed dependency with a working reference
implementation in this exact codebase — no need to re-litigate the tool
choice. `render-pdf.py` should adapt this script's pattern directly
(single assembled HTML page instead of per-team batch, otherwise the same
`sync_playwright()` → `page.pdf()` shape), not evaluate alternatives.

**Phase**: build 1.1 first (nothing else in this section works without an
assembled document), then 1.2 (only blocks documents containing diagrams),
then 1.3/1.4 in parallel (independent output formats from the same input).

---

## 2. Blocker: No External Literature Search

Confirmed: `collate-references` collates *in-repo* citation markers only —
nothing in this pipeline discovers or cites real external prior work. The
11 sample papers average ~24 external citations each (range 13–47,
established in the alignment proposal). A `Bodha`-sourced paper with no
external citations already embedded in its docs will produce a References
section of whatever's already there — likely far short of "in-depth,
sample-paper-equivalent."

**Provenance note from review**: that 13–47/~24 figure isn't traceable to
a stored artifact — `reference/sample_paper/extracted/_summary.json` only
records `pages`/`word_count`/`chars` per file, no citation counts. The
number came from a live `grep -oE "\[[0-9]+\]"` over the extracted `.txt`
files earlier in this proposal's history, correct but not reproducible
from anything checked into this repo. Doesn't change the recommendation
below, but if this number matters again later, regenerate it rather than
citing this document as the source.

This is a capability gap the guide's own Philosophy explicitly wouldn't
want papered over dishonestly: "does not attempt to... fabricate
experiments" and (by the same logic) shouldn't fabricate citations to
papers that were never actually consulted. Two honest paths, not one:

**Option A — human-supplied bibliography.** Add an input step before
generation: the author supplies a real reading list (BibTeX or a plain
list of titles/DOIs) as part of repo registration. `collate-references`
gains a second source besides in-repo markers. This requires no new
external-API dependency and keeps citation integrity fully human-owned —
consistent with the Philosophy's "Human and AI Collaboration" principle
("scientific judgment, originality, and research responsibility remain
with the human author").

**Option B — literature search API integration** (Semantic Scholar,
CrossRef, or arXiv API) — a new usecase (`3c-literature-search.md`-style)
that takes the novelty/gap analysis output, searches for related real
papers, and proposes candidates for the author to confirm before they
enter the reference list (never auto-inserted without approval — same
proposal-gate discipline the rest of the pipeline uses). Bigger build,
genuinely closes the gap rather than working around it, but introduces a
new external dependency and a new judgment call (is a search result
actually relevant, or a false positive) this system has no existing
component for evaluating.

**Recommendation**: Option A first (cheap, no new dependency, ships this
quarter), Option B as a real follow-up proposal of its own scope — this
document doesn't design it further than naming it, since API selection,
rate limits, and relevance-filtering are each non-trivial decisions on
their own.

---

## 3. Gap: `discover-modules` Targets Source Code, Not a Docs Folder

Confirmed: `discover_modules.py` finds "module boundaries (top-level
packages)" in a repo — it's a code-structure walker that docs support,
not a docs-only analyzer. Registering `Bodha/docs/paper` itself as the
target repo would likely return zero or near-zero modules, starving
`novelty-analysis`/`gap-analysis`/`mathematics-analysis`/
`diagram-architecture-analysis` of anything to analyze.

**Fix**: this isn't a code change, it's a registration-time and
documentation fix. `mcp__samgraha__register_repository`'s `repo_root`
should point at `Bodha`'s actual code root (wherever the top-level
packages live), not `Bodha/docs/paper` specifically — the docs folder is
supporting evidence `gather-module-evidence`/`gather-domain-evidence`
already pull in alongside source, not the analysis target itself. Add a
one-paragraph note to `pcems_2026`'s own onboarding material (or a new
`README.md` at `pcems_2026/`'s root, which doesn't currently exist) stating
this explicitly, since `classify-repo`'s `min_doc_words: 200` threshold
alone doesn't communicate this distinction to whoever registers a repo
next.

---

## 4. Gap: Template PDF Never Extracted — Formatting Rules Have Unverified Provenance

Confirmed twice now (this proposal and the alignment proposal): no
`reference/template/extracted/` exists, and this environment can't
produce one (`pdftoppm`/`poppler-utils` missing). `Conference Guidelines/*`
claims derivation from `Template_PCEMS2026.docx.pdf` with no diff on
record proving it, unlike the sample papers.

**Fix**: extract the template PDF to text in an environment that has PDF
tooling (install `poppler-utils`, or open the PDF in a tool that exports
text/the original `.docx` if it's recoverable — the filename
`Template_PCEMS2026.docx.pdf` suggests it may be a `.docx` exported to PDF,
in which case the original `.docx` might exist upstream and be a better
source than re-extracting from PDF). Save to
`reference/template/extracted/Template_PCEMS2026.txt`, matching the sample
papers' convention. Diff against `Conference Guidelines/*`'s specific
numeric claims (font sizes, margins, page limit, exact copyright-notice
text) and correct any mismatch found. This also directly produces the
input §1.3's pandoc reference-doc needs — same extraction serves both.

**This is the cheapest item in this proposal** — no design decisions, no
new dependencies beyond a tool install, and it de-risks every formatting
claim every generation and audit prompt in this system currently trusts
unverified.

---

## 5. Gap: Cross-Section and Document Audit Prompts — Close to the Original Design, Two Named Items Short

Checked both files against what the prompt-layer proposal (§2.2, §2.3)
specified. **Correction from review**: the first draft of this section was
titled "Partially Enriched, Not Complete," which undersells what's
actually there — restated more precisely below, credit first, gaps second.

**`prompt/audit/cross-section-audit.md`** already has all 4 dimensions the
prompt-layer proposal's base shape called for, *plus* a 5th
(`contribution-visibility`, citing `Philosophy/philosophy.md` directly) —
genuine PCEMS-specific work beyond what `base_academic`'s original had, not
a copy with one thing bolted on. What it's still short of, from the
original proposal's fuller spec:
- The specific **abstract-number-must-match-findings-number-exactly**
  check (not just generic "number consistency" — `Reviewer Expectations/
  03`'s own worked example, "99.95% accuracy" must appear identically in
  both places, not just "numbers should agree" in the abstract).
- **Citation-figure-table numbering collision**
  (`Checklists/03-final-review.md`: "No citation overlaps with figure/table
  numbers") — entirely absent.

**`prompt/audit/document-audit.md`** likewise already has all 5 dimensions
from the base shape plus a 6th (`template-compliance`) — also genuine
PCEMS-specific work, not a copy. Still short of the original proposal's
fuller spec:
- The **Reviewer Expectations/03 6-dimension Pre-Revision Assessment
  table** (Contribution clarity / Methodology detail / Results strength /
  Writing quality / Literature coverage / Formatting compliance, each 1–3,
  interpreted via the Major/Targeted/Minor-revision thresholds) — the
  document-level audit currently invents its own `dimension_scores` keys
  freely rather than scoring against this named, already-defined guide
  rubric. Since the rubric already exists in the guide with defined
  thresholds, the prompt should use it directly rather than reinvent
  scoring dimensions from scratch.

**Fix**: add the two missing cross-section checks and the named document
rubric to their respective prompt files. Small, contained diffs — both
files already have the right shape and partial PCEMS content, this closes
the remaining distance to what was originally specified.

---

## 6. Gap: Never Run End-to-End

Every verification in this repo's proposal history has been static —
file content, wiring, code-path tracing. No live
`register_standard`/`register_repository`/generation run has happened.
Static verification cannot catch schema-application errors, step-
orchestration bugs, or `prepare_semantic_step`/`complete_semantic_step`
plumbing issues — the class of bug the `run_full_workflow.py` `NameError`
(found and fixed in the prompt-layer proposal) demonstrates static reading
*can* catch some of, but not all of.

**Fix**: a smoke test, run once §1–4 above are addressed (running it
before §1 exists would only prove content generation works, not the full
"deliverable" claim this proposal is about closing):
1. Register `pcems_2026` as a standard.
2. Register a small, real repo (not `Bodha` for the first attempt — pick
   something with an intentionally short docs footprint, so a failure is
   fast and cheap to diagnose) as `HAS_DOCS`.
3. Run through `schema-init` → `classify-repo` → the analysis usecases →
   one domain's full 9-stage generation-through-humanize chain → render.
4. Confirm a real `.docx` and `.pdf` exist, non-zero size, and open
   correctly — the two completion criteria `plan/usecase/6c-render-paper.md`
   already specifies.

Not proposing to run this now (per the request this document responds to)
— sequencing it as the last phase, gated on §1 and §4 existing.

---

## 7. Optimization: `budget_fit_applied`'s Critical Severity Is Misleading

Found while fixing the prompt-layer proposal's rendering questions:
`budget_fit_applied` (in all 11 `calculation/generation/*.yaml` files, per
domain, marked `severity: critical`) is implemented in `content_rules.py`
as an unconditional `return True` — confirmed in the alignment proposal,
left as a documented no-op because the *real* gate is `4d-budget-total`'s
fan-in usecase predicate (`academic_schema._uc_section_budget_fit_total`),
which already correctly blocks progression before this check ever runs.

That's fine mechanically, but marking a check that can never fail as
`severity: critical` in 11 files is misleading to a human reading the
audit output — it looks like a real gate that's always passing, not a
structurally-redundant no-op.

**Confirmed from review**: `templates/report/markdown/whole-paper-summary.md`
and its `.html` counterpart do iterate every check and roll up
`det_passed`/`det_total`. Removing `budget_fit_applied` outright would
silently drop 9 guaranteed passes from `pcems_2026`'s per-domain totals —
a real, if small, distortion of the reported pass rate, not a neutral
cleanup. **Fix, settled by this**: downgrade severity to `info` (lowest)
across all 11 files, don't remove the check. This keeps `det_total`
correct while no longer displaying a no-op check as if it were a real
`critical` gate. Removal is only back on the table if
`templates/report/**` is also updated in the same change to exclude this
check from its counts — not proposed here, since that's strictly more
work for the same end result the severity downgrade already achieves.

## 8. Optimization: `pcems_2026/` Has No Root `README.md`

Every other concrete system's onboarding relies on tribal knowledge
scattered across `guide/README.md` (which documents the *knowledge base*,
not the *system*) and this repo's own proposal history. A short
`pcems_2026/README.md` — domains list, what's shared from `base_academic`
vs. owned locally, and the §3 code-root-vs-docs-folder registration note —
would have prevented at least one of this proposal's own findings (§3)
from needing to be a proposal item at all. Cheap, high leverage for
whoever registers this standard next without having read this repo's
entire proposal history first.

---

## 9. Phases

1. **§4 template extraction** — cheapest, no dependencies, de-risks
   everything downstream that trusts `Conference Guidelines/*`.
2. **§7, §8 optimizations** — independent of everything else, safe to do
   any time, bundled here only because they're small enough not to need
   their own phase.
3. **§5 audit prompt completion** — small diffs, independent of §1/§2/§3,
   can run in parallel with them.
4. **§3 registration guidance** — documentation-only, no code, can run
   any time, but logically belongs before §6's smoke test so the first
   real run doesn't repeat this proposal's own discovery.
5. **§2 references, Option A** (human-supplied bibliography) — needed
   before a genuinely "in-depth, sample-paper-equivalent" paper is
   possible; Option B stays a named-not-designed follow-up.
6. **§1 renderer** — the largest phase, 1.1 before 1.2 before 1.3/1.4 in
   parallel, as ordered in that section. Depends on §4's extraction for
   1.3's reference-doc.
7. **§6 smoke test** — last, gated on §1 and §4 both existing; the first
   time any of this gets verified by actually running it instead of
   reading it.
