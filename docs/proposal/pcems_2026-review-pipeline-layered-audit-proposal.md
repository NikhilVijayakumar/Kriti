# pcems_2026 — Layered Review Pipeline: Deterministic Writing Quality, Scientific Review, and Reviewer Simulation

## 0. Why This Document Exists

The review-system critique this proposal responds to argues for a hard
boundary between two classes of validation: **deterministic writing
quality** (grammar, style, readability, formatting, consistency —
"is the manuscript written correctly") and **semantic scientific review**
(novelty, evidence, methodology soundness — "is the research good"), plus
a third layer that doesn't exist in `pcems_2026` at all today: **reviewer
simulation** (persona-based scoring producing an Accept/Revise/Reject-style
recommendation).

`pcems_2026` already has real machinery for two of these four proposed
layers (`calculation/generation/*.yaml` for deterministic checks,
`audit/semantic/document/*.md` + `prompt/audit/*` for semantic review) —
this isn't a from-scratch build. But checking what's actually in each
existing file against the boundary the critique draws finds three concrete
problems: (1) real writing-quality tooling (grammar, readability,
style) doesn't exist at all — the closest thing is a handful of narrow
regex checks; (2) some checks that are objectively deterministic are
currently done by an LLM anyway, burning tokens on things a word-list scan
already handles; (3) the reviewer-simulation layer is entirely missing —
nothing in this system currently produces a PCEMS-reviewer-style verdict.
(The four-*layer* framing in the diagram maps directly onto these three
problems plus one already-adequate layer — Publication Compliance, §3 —
that needed no new build, only two small relocations already covered by
problems 1 and 2's fixes.)

**Scope, checked directly**: `content_rules.py` and `deterministic_audit.py`
are `base_academic`'s own files, reused by `pcems_2026` via path (per the
system-build proposal's reuse pattern) — any change to them is a
`base_academic` change, not a `pcems_2026`-local one. Checked which other
concrete systems actually depend on these two files: `grep`-ing the whole
`samgraha/system/` tree for references to either name outside
`base_academic/script/` itself returns only `pcems_2026`. `eswa_journal`
has no deterministic layer at all (established in the system-build
proposal — it only ever defined a `semantic_document` calculation bucket).
`python_hackathon` and the `*_dev` systems have their own separate
deterministic/semantic scripts, untouched by anything in this proposal.
**The actual blast radius of §2's and §4's `content_rules.py`/
`deterministic_audit.py` changes is `base_academic` + `pcems_2026` only** —
consistent with how every prior shared-script fix in this repo's history
(the `content_rules.py` rule additions, the `run_full_workflow.py` bug fix)
was already handled: edited once in `base_academic`, consumed by whichever
concrete system needs it. This proposal follows that same precedent, not a
new pattern — `calculation/generation/{domain}.yaml` additions are
`pcems_2026`-local either way, since those files were never shared.

---

## 1. Layer Mapping — What Exists, What's Misplaced, What's Missing

| Proposed Layer | `pcems_2026` mechanism today | Status |
|---|---|---|
| **Writing Quality** (grammar/style/readability/terminology/acronyms/consistency) | `content_rules.py`'s regex-based rules (`no_placeholders`, `regex_match`, `sequential_numbering`, etc.) | **Thin substitute, not the real thing** — no grammar checker, no readability scoring, no acronym-definition tracker, no cross-document terminology-consistency checker exist anywhere. §2. |
| **Publication Compliance** (PCEMS-specific: required sections, keywords, template, reference style, figure/table placement) | `calculation/generation/{domain}.yaml` (word counts, `keyword_count`, `author_block_present`, `table_created_with_word_tools`, etc.) + `audit/semantic/document/*.md` | **Substantially already built** — this is the one layer of the four that's genuinely close to done. §3 notes what's still misplaced into it from Layer 4-shaped LLM prompts. |
| **Scientific Review** (novelty, evidence, methodology, reproducibility) | `audit/semantic/document/{domain}.md` rubrics + `prompt/audit/semantic-audit.md`, `cross-section-audit.md`, `document-audit.md` | **Built, but not cleanly separated** — these files currently also carry deterministic-shaped checks that don't belong here. §4. |
| **Reviewer Simulation** (persona-based Accept/Revise/Reject verdict) | Nothing. `document-audit.md`'s Pre-Revision Assessment table is the closest analog, but it's self-assessment framing (a checklist score), not a simulated external reviewer producing weaknesses/questions/a decision. | **Missing entirely.** §5. |

---

## 2. Layer 1 — Real Writing-Quality Tooling (New Capability)

Checked `content_rules.py`'s full rule set (31 rules across the checks
built in this repo's history) against the critique's Writing Quality Engine
checklist. None of the following exist as automated checks anywhere in
`pcems_2026` or `base_academic`:

- **Grammar** (subject-verb agreement, article usage, sentence fragments) —
  zero coverage. `Writing Guide/01`'s and `Common Mistakes/04`'s guidance
  on this is currently prose instructions inside generation *prompts*
  (the model is asked to write correctly), never independently checked
  after the fact.
- **Readability** (Flesch-Kincaid, Gunning Fog, average sentence/paragraph
  length) — zero coverage. `Writing Guide/01`'s own numeric targets
  (15–25 words/sentence, 4–8 sentences/paragraph) exist as *prose
  guidance* only — no check measures a real draft against them.
- **Acronym-definition tracking** ("LLM" used before "Large Language
  Model (LLM)" is ever spelled out) — zero coverage.
- **Cross-document terminology consistency** (same concept, different
  names — "Judge Worker" vs. "Judge-Worker" vs. "JudgeWorker") — zero
  coverage. `cross-section-audit.md`'s "Terminology consistency" dimension
  asks an LLM to catch this by reading the whole paper — solvable
  deterministically instead (build a term-variant index, flag near-
  duplicate casing/hyphenation).

**Recommendation, settled — Option A, one pass**: the first draft of this
section hedged between adding these as new rules in the existing
`content_rules.py`/`calculation/generation/{domain}.yaml` (one pass) versus
a parallel `calculation/quality/{domain}.yaml` run by a new
`deterministic-quality-audit.py` script (two passes). Those are
contradictory, not two phrasings of the same plan — a second script
reading a second YAML file *is* a second pipeline stage, regardless of
where its output is logically filed. Committing to the one-pass option:
new rule names (`acronym_defined_at_first_use`, `terminology_consistency`,
`sentence_length_distribution`, `readability_score_in_range`, etc.) get
added to `content_rules.py`'s existing `evaluate_rule()` dispatch, and
new checks referencing them get added to each `calculation/generation/
{domain}.yaml` — the exact same mechanism §2.1's `ai_language_flags`
check uses. No new script, no new YAML category, no second deterministic
pass. This is also the simpler diff and matches this section's own
"keep them in one pass" reasoning, which the parallel-script option
contradicted from the start.

**Dependency decision, not resolved here**: this repo has no
`requirements.txt`/`pyproject.toml` anywhere — every script so far is
stdlib + PyYAML + sqlite3. Real grammar/readability checking needs an
actual library:
- `textstat` (pure Python, readability formulas only — Flesch-Kincaid,
  Gunning Fog, etc. — no grammar) is the lightest addition, no external
  runtime.
- `language_tool_python` (grammar + style, the closest match to the
  critique's "Harper/LanguageTool" suggestion) requires either a Java
  runtime and a bundled LanguageTool server, or a network call to the
  public LanguageTool API — meaningfully heavier than anything else this
  pipeline depends on today.
- A hand-rolled acronym-tracker and terminology-variant-index need no
  dependency at all — pure regex/string work, same style as
  `content_rules.py`'s existing rules.

**Proposed sequencing**: ship the zero-dependency pieces first (acronym
tracker, terminology-variant index, sentence/paragraph-length distribution
against `Writing Guide/01`'s numeric targets — all computable with
`re`/stdlib alone), add `textstat` for real readability scores next (cheap,
pure-Python), and treat full grammar-checking (`language_tool_python` or
equivalent) as a separate follow-up given its runtime footprint — this
repo has never taken on a dependency with an external service/JVM
requirement before, and that's a decision for whoever owns the deployment
environment, not something to default into here.

### 2.1 Move Into Layer 1: Checks Currently Burning LLM Calls For No Reason

Confirmed: the AI-generated-language word lists (delve, landscape,
tapestry, crucial, paramount, pivotal — `Writing Guide/01`,
`Common Mistakes/04`) exist **only** as prose instructions inside
`prompt/audit/plagiarism-audit.md` and `prompt/audit/humanize.md` — an LLM
call is currently the only thing that ever checks for these words.
`content_rules.py` already has a working `regex_match` rule; a plain word-
list scan needs no reasoning at all. **Fix**: add a deterministic check
(`ai_language_flags`, one `regex_match` per flagged term or a combined
alternation pattern) to each domain's `calculation/generation/{domain}.yaml`,
`severity: warning`. This doesn't remove the LLM-side check — the semantic
prompts should keep judging *whether flagged usage reads naturally in
context* (a judgment call), but the *presence* of a flagged word shouldn't
need an LLM round-trip to detect at all. Same principle the critique states
directly: "deterministic engines catch objective, repeatable issues without
consuming LLM tokens."

---

## 3. Layer 2 (Publication Compliance) — Already Mostly Built, One Cleanup Item

`calculation/generation/*.yaml` + the deterministic side of
`audit/semantic/document/*.md` already cover required sections, keywords,
metadata, word template numerics, and most formatting rules the critique's
"PCEMS Compliance Checker" describes. No new layer needed here — this
proposal's only addition is §2.1's `ai_language_flags` check and moving
the citation-figure-table-numbering-collision check out of
`cross-section-audit.md` (§4) into this deterministic layer, since it's
exactly the kind of "sequential numbering, no collisions" check
`sequential_numbering`/`referenced_before_appearance` already prove this
system can do without an LLM.

---

## 4. Layer 3 (Scientific Review) — Strip Out What Doesn't Need Reasoning

`audit/semantic/document/{domain}.md`'s rubrics are already the right
shape for this layer — evidence-graded criteria, mandatory/recommended
weighting, requires reading and judging, not just pattern-matching.
Two files built earlier in this repo's history currently mix in checks
that don't belong here, confirmed by re-reading them against the
critique's own boundary:

- **`cross-section-audit.md`**'s "Citation-figure-table numbering
  collision" check (added in the production-readiness proposal) asks an
  LLM to verify `[N]` never collides with `Fig. N`/`Table N` — this is
  exactly the kind of "no creativity, no reasoning, same input same
  output" check the critique says belongs in Layer 1. **Move it** to a
  new deterministic check instead (§3).
- **`document-audit.md`**'s "Template compliance" dimension ("title block
  order, section numbering, formatting per template/guide") is entirely
  deterministic — `_master-schema.yaml`'s section order and
  `Assets/01`'s font spec are already checked mechanically elsewhere
  (§1.1's title-and-metadata reordering, `_style.css`'s typography). Its
  presence as an LLM-scored "dimension" here duplicates a check that
  already exists and runs for free. **Remove it** from the semantic
  rubric; keep the deterministic version as the single source of truth.

What stays, correctly, in Layer 3: gap closure, methodology-results
alignment, narrative arc coherence, abstract-number fidelity, contribution
visibility, novelty/gap/evidence judgment in the per-domain rubrics — all
of these require reading and reasoning about content, not pattern-matching
against a fixed rule.

---

## 5. Layer 4 — Reviewer Simulation Engine (New)

Nothing in `pcems_2026` currently produces a reviewer-style verdict.
`document-audit.md`'s Pre-Revision Assessment (§ from the production-
readiness proposal) is the closest analog but it's framed as an author
self-check against a rubric, not a simulated external reviewer producing
independent weaknesses, questions, and a publication decision.

**Proposed**: `prompt/propose/reviewer-simulation.md` (or
`prompt/audit/reviewer-simulation.md` — naming decision, not load-bearing),
three personas grounded directly in material this system already has, not
invented from scratch:

| Persona | Focus | Grounded in |
|---|---|---|
| **Reviewer 1 — Novelty & Contribution** | Is the contribution real, specific, and adequately differentiated from prior work? | `domains/07-novelty.md`'s Standard Definition, `Reviewer Expectations/02`'s "Unclear Contribution" pattern |
| **Reviewer 2 — Methodology & Reproducibility** | Is there enough detail to reproduce? Are baselines and statistics adequate? | `Reviewer Expectations/02`'s "Insufficient Methodology"/"Weak or Missing Evaluation" patterns, `Reviewer Expectations/03`'s Methodology "Required Details" table |
| **Reviewer 3 — Writing, Organization, Figures** | Is it clearly organized, are figures/tables well-constructed and legible? | `Reviewer Expectations/02`'s "Writing Quality Issues"/"Formatting and Citation Errors" patterns, `Checklists/03-final-review.md` |

**Scoring rubric, specified rather than sketched** — the first draft's
"adapted to 3 reviewers x 10 instead of 6 dimensions x 3" line named a
target scale without defining it. Filled in below rather than left for
implementation to invent:

**Per-reviewer 1–10 anchors** (reusing `Reviewer Expectations/03`'s own
Weak/Adequate/Strong vocabulary rather than inventing new language — that
document's 3-tier scale mapped onto a 10-point range so each persona has
room to express degree, not just tier):

| Range | Tier | Meaning for that persona's focus area |
|---|---|---|
| 1–3 | Weak | Same failure patterns `Reviewer Expectations/02` names as desk-rejection/major-rejection triggers for this persona's focus (e.g. Reviewer 1: no differentiation target per any novelty claim) |
| 4–7 | Adequate | Present but not compelling — the specific "adequate" language `Reviewer Expectations/03`'s Pre-Revision table already uses per dimension |
| 8–10 | Strong | Matches the "strong" examples `Reviewer Expectations/03` and `Examples/*` show from accepted papers |

**Combining and decision**: `overall_score` = sum of the 3 reviewers'
scores (range 3–30, not an average — a single weak reviewer should pull
the total down, not get diluted by two strong ones, same "mandatory
criterion forfeits the whole criterion" philosophy the per-domain semantic
rubrics already use). Decision thresholds, scaled from `Reviewer
Expectations/03`'s own 6×3=18-point scale (which has no Accept tier by
design — it's a pre-submission self-check, not a final verdict) up to this
layer's 3×10=30-point range, and adding the Accept tier a real reviewer
verdict needs that the self-check version never did:

| Score | Decision |
|---|---|
| 25–30 | Accept |
| 18–24 | Minor Revision |
| 10–17 | Major Revision |
| 3–9 | Reject |

```json
{
  "reviewers": [
    {"persona": "novelty-contribution", "score": 8,
     "weaknesses": ["..."], "questions": ["..."]},
    {"persona": "methodology-reproducibility", "score": 7, "...": "..."},
    {"persona": "writing-organization", "score": 9, "...": "..."}
  ],
  "overall_score": 24,
  "decision": "Minor Revision"
}
```

**Where this runs in the pipeline**: after Layer 3 (per-domain +
cross-section + document semantic audits) pass, not instead of them —
reviewer simulation is a final gate simulating what happens *after*
submission, not a replacement for the pre-submission audits that catch
fixable problems earlier. Maps to a new `plan/usecase/5g-reviewer-
simulation.md`, gated the same way `5e`/`5f` are (runs once per assembled
document, invalidated by the same `computed_against`-staleness tracking
the prior proposal established for cross-section/document audits).

**This is genuinely new work**, not a restructure of something existing —
flagging it as the largest single item in this proposal, comparable in
scope to the renderer work in the production-readiness proposal.

---

## 6. What This Proposal Does Not Change

- The 9-stage per-domain pipeline (generate→cite→enrich→budget-fit→
  audit-det→audit-sem→plagiarism→humanize-det→humanize-sem) stays as-is —
  Layer 1/2's new checks slot into the existing `audit-det` stage
  (they're deterministic, same stage as everything else deterministic),
  Layer 3 stays at `audit-sem`, Layer 4 is a new stage after `5f`, not a
  replacement for any existing one.
- `plagiarism-audit.md`/`humanize.md` stay LLM-driven for the *contextual
  judgment* of whether flagged language reads naturally — only the raw
  word-list *detection* moves to deterministic (§2.1).
- No existing rubric criterion is deleted for being "too deterministic" —
  only the two specific items named in §4, which are genuine duplicates
  of checks that already exist elsewhere or belong there better.
- **Findings surface**: since §2's Option A adds these as ordinary
  `calculation/generation/{domain}.yaml` checks run by the existing
  `deterministic_audit.py`, their findings land exactly where every other
  deterministic finding already does — `academic_deterministic_findings`,
  surfaced in `templates/report/markdown/domain/{domain}/deterministic.md`.
  No new report section, no new metadata column, no change to
  `assemble-final-document.py` — that script reads `stage='polish'`
  content for the final document, not audit findings, and this proposal
  doesn't touch what it renders, only what the deterministic audit
  earlier in the pipeline checks.

---

## 7. Phases

**Correction from review**: the first draft listed phase 4
(zero-dependency writing-quality checks) as "independent of 1–3, can run
in parallel." Checked and that's wrong — phase 1's `ai_language_flags`
check and phase 4's acronym-tracker/terminology-index checks both add new
rule names to the *same* `content_rules.py` `evaluate_rule()` dispatch and
new check entries to the *same* `calculation/generation/{domain}.yaml`
files. Editing the same files in "parallel" phases means one supersedes
or conflicts with the other's diff — merged into one phase below instead
of pretending they're independent.

1. **§2.1 + §2 zero-dependency writing-quality checks, merged** — move
   AI-language-flags to deterministic (`regex_match`, no new dependency)
   and add the acronym tracker, terminology-variant index, and sentence/
   paragraph-length distribution checks (Option A, §2) in the same pass,
   since all four touch `content_rules.py` and
   `calculation/generation/{domain}.yaml` together. Also covers §3's two
   Publication Compliance additions (`ai_language_flags` is one of them;
   the layer doesn't warrant a separate phase of its own — it was never
   more than these two items, both already covered here and in phase 2).
2. **§4 strip duplicated checks from `cross-section-audit.md`/
   `document-audit.md`, then §3's citation-figure-table collision check**
   — sequenced together since the second half completes what the first
   half removes from the LLM side; independent of phase 1's files, so this
   pair can run in parallel with phase 1, not phases 1 and "4" separately
   as the first draft implied.
3. **`textstat` readability integration** — needs the dependency decision
   resolved first (this repo's first `requirements.txt`); depends on
   phase 1 existing since it adds one more check into the same files.
4. **§5 Reviewer Simulation Engine** — the largest phase, new capability
   rather than a fix to something existing. Sequence last: a reviewer
   simulation scored against a paper that still has uncaught mechanical
   issues is less useful than one scored after phases 1–3 land.

Full `language_tool_python`/grammar-checker integration is intentionally
not phased here — flagged in §2 as a decision for whoever owns the
deployment environment, given the JVM/network-service dependency it
introduces, unlike everything else in this proposal.
