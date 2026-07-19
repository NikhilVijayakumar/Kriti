# eswa_journal — System Proposal

## 1. Class / Position in Taxonomy

Class `academic`, subclass `journal`, proposed `extends: base_academic`
(see `base_academic-proposal.md`) once that base exists. Proposed path
`academic/journal/eswa_journal/` (currently flat at
`samgraha/system/eswa_journal/`, no `system.yaml` exists yet — this
document specifies what it should say).

`plan/core/loop.yaml` confirms the LIM-001 class shape in its own
words, same framing as `pcems_2026`'s: *"Academic-paper class...
eswa_journal has no deterministic layer and no section-scoped audits,
so this loop only ever touches the semantic_document bucket."* No trace
of the hackathon-shaped `loop.yaml` LIM-001 flags as the original
mistake — already academic-paper-shaped. Same caveat as `pcems_2026`'s
proposal: "no deterministic layer" is stated as settled design here,
but every `documentation-standards/*.md` file references a
`audit/deterministic/document/{domain}.yaml` path that doesn't exist
(§6) — worth resolving one way or the other.

## 2. What It Has

11 domains: abstract, introduction, related-work, problem-definition,
methodology, experimental-setup, results, implications, limitations,
conclusion, references.

**Tier structure** (`00-domain-relationships.md`):

| Tier | Domains |
|---|---|
| 1 | problem-definition, related-work |
| 2 | methodology |
| 3 | experimental-setup, results, implications, limitations |
| 4 | introduction, abstract, conclusion, references |

Denser edge set than `pcems_2026`'s (per LIM-001's characterization,
confirmed): `related-work --guides--> problem-definition`,
`problem-definition --requires--> methodology`, `methodology
--requires--> experimental-setup`, `experimental-setup --validates-->
results`, `results --informs--> implications` (non-mandatory), `results
--guides--> conclusion`, `methodology --informs--> abstract`, `results
--informs--> abstract`. Two `within_tier_ordering` exceptions (vs.
`pcems_2026`'s one): tier 1 `related-work` before `problem-definition`,
tier 3 `experimental-setup` before `results`.

**File inventory:**
- `documentation-standards/`: 11 files, each with genuinely rich,
  specific, quantified rules (not just typography, unlike `pcems_2026`)
  — read in full, examples: `01-abstract`: 150-250 word count limit,
  "Must contain specific numbers/percentages... claims like 'high
  accuracy' are rejected"; `03-related-work`: "evaluating 15+ recent
  references (2022-2026), including 2-4 recent ESWA citations,"
  mandatory comparison table; `05-methodology`: mandatory pseudocode
  block, mandatory Big-O complexity table with a comparison row;
  `06-experimental-setup`: "Minimum of 3 baselines required (at least 1
  classical, 2 recent)," explicit statistical test + p-value threshold
  required; `07-results`: mandatory Sensitivity/Robustness subsection,
  mandatory 4-part Threats to Validity (internal/external/construct/dataset
  bias); `11-references`: 35-45 reference target with a specific
  percentage distribution (60-70% recent, 20% classics, 10-20%
  architecture, 2-4% ESWA-specific), explicit rejection of "blog posts,
  non-peer-reviewed URLs, or known predatory journals"
- `audit/`: **only `audit/semantic/document/*.md`, 11 files** —
  `audit/deterministic/` does not exist, confirmed by directory listing
- `calculation/`: same shape as `pcems_2026`'s —
  `semantic/document.yaml`, `summary/{final_score,score_bands,trend}.yaml`,
  `validation/scoring_validation.yaml`
- `templates/`: **almost entirely empty — only one file exists,
  `templates/generation/humanifier.md`**, not a per-domain generation
  template at all. `loop.yaml` confirms: *"templates/generation/document/{domain}.md
  is not yet authored for eswa_journal (only templates/generation/humanifier.md
  exists today)."*

## 3. What It Would Inherit From `base_academic` vs Keep Its Own

Per the taxonomy proposal's design: `introduction`, `methodology`,
`conclusion`, `references` would come from `base_academic`; `abstract`,
`related-work`, `problem-definition`, `experimental-setup`, `results`,
`implications`, `limitations` (7 domains) stay `eswa_journal`-specific
— no counterpart in `pcems_2026` at all. `00-domain-relationships.md`/
`tiers.yaml` stay own (this system's graph is denser and structurally
different from `pcems_2026`'s, confirmed in §2).

Proposed `system.yaml`:
```yaml
name: eswa_journal
class: academic
subclass: journal
extends: base_academic
description: >
  ESWA (Q1 journal) paper generation and audit. Inherits
  introduction/methodology/conclusion/references from base_academic,
  adds abstract + related-work + problem-definition +
  experimental-setup + results + implications + limitations.
```

## 4. Use Cases

Same shape as `pcems_2026`'s: `plan/usecase/` doesn't exist as a
directory, single implied use case — "existing project with
implementation/evidence, no ESWA-formatted paper written yet."
`loop.yaml`'s `path_selection.evidence` step is broader here than
`pcems_2026`'s — it applies to 3 domains (`abstract`,
`experimental-setup`, `results`), not just 1 (`findings`), reflecting
the deeper empirical-rigor bar a Q1 journal enforces across more of the
paper, not just its results section.

## 5. Workflow per Use Case (target `init.py` phase plan)

Full ordered phase table, following `loop.yaml`'s 2
`within_tier_ordering` exceptions:

```
tier1-related-work-scaffold/content         script/semantic  depends_on: []
tier1-problem-definition-scaffold           script           depends_on: []
tier1-problem-definition-content            semantic         depends_on: [tier1-problem-definition-scaffold, tier1-related-work-content]  # mandatory: related-work's gap-closing bridge must complete first
tier1-audit/calculate/report/fix            (standard pattern)

tier2-methodology-evidence                  script            depends_on: [tier1-fix]   # implicit: methodology needs problem-definition's formalization
tier2-methodology-scaffold/content/audit/calculate/report/fix

tier3-experimental-setup-evidence           script            depends_on: [tier2-fix]
tier3-experimental-setup-scaffold/content/audit/calculate/report/fix
tier3-results-evidence                      script            depends_on: [tier2-fix]
tier3-results-scaffold                      script            depends_on: [tier2-fix]
tier3-results-content                       semantic          depends_on: [tier3-results-scaffold, tier3-results-evidence, tier3-experimental-setup-content]  # mandatory: experimental-setup (baselines, reproducibility) before results
tier3-implications-scaffold/content/audit/calculate/report/fix    depends_on: [tier2-fix]   # parallel with experimental-setup/results, no ordering constraint
tier3-limitations-scaffold/content/audit/calculate/report/fix     depends_on: [tier2-fix]   # parallel

tier4-abstract-evidence                     script            depends_on: [tier3-fix]
tier4-{abstract,introduction,conclusion,references}-scaffold/content/audit/calculate/report/fix   depends_on: [tier3-fix]
```

Same document-level-only fix loop as `pcems_2026` — no section-scoped
generation templates to target.

## 6. Deterministic Audit via Script

`audit/deterministic/` confirmed absent, same dangling-reference issue
as `pcems_2026` (§1). But this system's actual rules (§2) are the
**richest set of deterministic-check candidates across every academic
system examined** — far more than `pcems_2026`'s mostly-typography
rules:

- **`01-abstract`**: word count in [150, 250] — trivially script-checkable
- **`03-related-work`**: reference count ≥ 15, presence of a markdown
  comparison table (structural check), presence of a closing
  gap-statement sentence (harder, borderline semantic)
- **`04-problem-definition`**: presence of LaTeX/math notation blocks
  (`$...$` or `$$...$$`) — structurally checkable
- **`05-methodology`**: presence of a pseudocode/algorithm block,
  presence of 2 distinct architecture subsections, presence of a
  complexity comparison table — all structurally checkable (regex/
  markdown-AST level, not full NLP judgment)
- **`06-experimental-setup`**: baseline count ≥ 3, explicit mention of
  a named statistical test + a p-value threshold (`p < 0.05` pattern) —
  script-checkable via regex
- **`07-results`**: presence of "Sensitivity Analysis" and "Threats to
  Validity" subsections with all 4 required sub-parts
  (internal/external/construct/dataset bias) — structural, checkable
- **`11-references`**: reference count in [35, 45], rough category-count
  distribution if citation metadata is parseable — the most
  quantitatively precise rule in the whole system

Unlike `pcems_2026`'s typography rules (which need real font metadata
unavailable in plain Markdown), **most of these are checkable directly
against Markdown source** — word counts, table presence, regex pattern
matches, section-heading presence — making `eswa_journal` a much
stronger near-term candidate for adding a real deterministic layer than
`pcems_2026` is.

## 7. Generation via Script (`scaffold.py`)

**Cannot be built yet** — same blocker as `pcems_2026`:
`templates/generation/document/{domain}.md` doesn't exist for any of
the 11 domains. The one file that does exist,
`templates/generation/humanifier.md`, is not a per-domain scaffold
template at all — see §10, it's something structurally different and
worth separate attention.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

Same shape as `pcems_2026`'s `calculation/` directory — `semantic/document.yaml`,
`summary/{final_score,score_bands,trend}.yaml`,
`validation/scoring_validation.yaml`. **File names and directory
structure are identical between the two academic systems** — strong
evidence this part genuinely is shareable via `base_academic`, even
though the domain *content* isn't (per `base_academic-proposal.md`'s
own finding). Worth confirming the stable IDs inside each file actually
match too (not verified byte-for-byte in this pass), but the shape
match alone is a good signal.

## 9. Script Language Priority Applied

All greenfield:
- `scripts/init.py` — §5's phase plan
- `scripts/scaffold.py` — blocked on templates existing first (§7)
- `scripts/validate.py` — has real candidates to implement immediately
  (§6, unlike `pcems_2026`'s more constrained set)
- `scripts/calculate.py`, `report.py`, `plan_generation.py`

## 10. Open Questions / Risks Specific to `eswa_journal`

- **`templates/generation/` has no per-domain templates — this system
  cannot generate a paper today**, same primary blocker as
  `pcems_2026`.
- **`templates/generation/humanifier.md` needs explicit review before
  being treated as part of this system's normal workflow.** Read in
  full (§2): it's a "3-layer rewrite" applied when generated text
  "fails the AI Plagiarism & Fingerprint Audits" — its stated goal is
  making LLM-authored text pass AI-detection tooling (varying sentence
  rhythm, injecting "experimental memory a AI couldn't hallucinate,"
  replacing passive voice, etc.). This is materially different from
  every other file in this system — it's not a content-quality rule
  like §2's word-count/reference-count/statistical-rigor rules, it's
  specifically about evading AI-authorship detection. Whether this
  belongs in the workflow at all is a policy question (many journals,
  including Elsevier — ESWA's publisher — have explicit AI-content
  disclosure requirements), not a technical one, and deserves an
  explicit decision from whoever owns this system before it's wired
  into `init.py`'s phase plan, rather than being carried forward
  silently as just another generation step.
- Given §6's much richer deterministic-check candidate set vs.
  `pcems_2026`'s, and §8's finding that `calculation/` shapes already
  match structurally, this system's proposal author leans toward
  `eswa_journal` being the better candidate to prototype a real
  deterministic layer against first, then port the pattern to
  `pcems_2026` — a sequencing suggestion, not a decision made here.

## 11. Explicitly Out of Scope

Actual script implementation. Extraction of `base_academic` itself —
separate document. Authoring the missing `templates/generation/`
content. A policy decision on `humanifier.md` (§10) — flagged as
needing explicit review, not resolved in this proposal. Any change to
the 11 domains' existing rules.
