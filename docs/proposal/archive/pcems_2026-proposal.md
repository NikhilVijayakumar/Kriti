# pcems_2026 — System Proposal

## 1. Class / Position in Taxonomy

Class `academic`, subclass `paper`, proposed `extends: base_academic`
(see `base_academic-proposal.md`) once that base exists. Proposed path
`academic/paper/pcems_2026/` (currently flat at
`samgraha/system/pcems_2026/`, no `system.yaml` exists yet — this
document specifies what it should say).

`plan/core/loop.yaml` confirms the LIM-001 class shape directly, in its
own words: *"Academic-paper class — generates a paper's domains from
existing project documentation/evidence, audits for PCEMS 2026
compliance, fixes what fails... pcems_2026 has no deterministic layer
and no section-scoped audits, so this loop only ever touches the
semantic_document bucket."* No trace of the hackathon-shaped
`loop.yaml` LIM-001 describes as the original mistake — this file is
already academic-paper-shaped, not a leftover copy. **However, see §6 —
"no deterministic layer" is stated as a design decision here, but the
`documentation-standards/` files themselves reference deterministic
YAML files that don't exist, which is a real, separate inconsistency,
not evidence the LIM-001 issue persists.**

## 2. What It Has

6 domains: title-and-metadata, introduction, methodology, findings,
conclusion, references.

**Tier structure** (`00-domain-relationships.md`):

| Tier | Domains |
|---|---|
| 1 | introduction, methodology |
| 2 | findings |
| 3 | conclusion, references |
| 4 | title-and-metadata |

Edges: `introduction --requires--> methodology`, `methodology
--requires--> findings`, `findings --validates--> conclusion`,
`findings --informs--> references`, `conclusion --guides-->
title-and-metadata`. `title-and-metadata` is written *last* (tier 4),
after everything it describes exists — sensible, a title/abstract
naturally comes after the content it summarizes.

**File inventory:**
- `documentation-standards/`: 6 files, each with a strict, concrete
  formatting spec — e.g. `01-title-and-metadata`: "Title must be Arial
  Bold 14pt, centered," "at least 4-5 keywords"; `06-references`: "All
  references MUST be formatted in APA style," "reference items must be
  strictly in 8pt font." These are PCEMS 2026's actual submission
  formatting rules, not generic prose guidance.
- `audit/`: **only `audit/semantic/document/*.md`, 6 files** —
  `audit/deterministic/` does not exist, confirmed by directory listing
- `calculation/`: `semantic/document.yaml`,
  `summary/{final_score,score_bands,trend}.yaml`,
  `validation/scoring_validation.yaml` — no `deterministic/` bucket,
  matching `loop.yaml`'s stated design
- `templates/`: **completely empty.** `loop.yaml` says so itself:
  *"templates/generation/document/{domain}.md is not yet authored for
  pcems_2026 (templates/generation/ is currently empty); this loop
  describes the target shape."* This system currently cannot generate
  anything — the workflow is fully specified in `loop.yaml` but has no
  templates to execute against.

## 3. What It Would Inherit From `base_academic` vs Keep Its Own

Per the taxonomy proposal's design: `introduction`, `methodology`,
`conclusion`, `references` would come from `base_academic`;
`title-and-metadata` and `findings` stay `pcems_2026`-specific — these
2 are the domains with no counterpart in `eswa_journal` at all.
`00-domain-relationships.md`/`tiers.yaml` always stay `pcems_2026`-own
(confirmed necessary: this system's tier graph — 4 tiers, `requires`/
`validates`/`informs`/`guides` edges — has no direct counterpart in
`eswa_journal`'s denser graph, per `base_academic-proposal.md`).

Proposed `system.yaml`:
```yaml
name: pcems_2026
class: academic
subclass: paper
extends: base_academic
description: >
  PCEMS 2026 conference paper generation and audit. Inherits
  introduction/methodology/conclusion/references from base_academic,
  adds title-and-metadata + findings.
```

## 4. Use Cases

`plan/usecase/` doesn't exist as a directory (confirmed — only
`plan/core/{loop.yaml,tiers.yaml}` are present, no `plan/usecase/`
subtree at all, unlike every dev-class system). The single implied use
case, read from `loop.yaml`'s framing: **"existing project with
implementation/evidence, no PCEMS-formatted paper written yet"** —
`loop.yaml`'s `path_selection.evidence` step explicitly pulls "concrete
numbers" from an available implementation artifact before generating
`findings`, degrading gracefully to "author-supplied figures, flagged
by audit if unverifiable" when no implementation exists. This is a
genuinely different use-case *shape* from the dev class's 4 explicit
repo-state combinations — academic generation here is evidence-driven
from one starting state, not branched by repo/doc existence.

## 5. Workflow per Use Case (target `init.py` phase plan)

Full ordered phase table for the one use case, following
`loop.yaml`'s `within_tier_ordering` (tier 1: introduction before
methodology) and the semantic-only audit shape (no `validate.py`
deterministic step — see §6):

```
tier1-introduction-scaffold    script    depends_on: []
tier1-introduction-content     semantic  depends_on: [tier1-introduction-scaffold]
tier1-methodology-scaffold     script    depends_on: []
tier1-methodology-content      semantic  depends_on: [tier1-methodology-scaffold, tier1-introduction-content]  # mandatory ordering, not just data dependency
tier1-audit-semantic           semantic  depends_on: [tier1-introduction-content, tier1-methodology-content]
tier1-calculate                script    depends_on: [tier1-audit-semantic]
tier1-report                   script    depends_on: [tier1-calculate]
tier1-fix                      semantic  depends_on: [tier1-report]

tier2-findings-evidence        script    depends_on: [tier1-fix]   # loop.yaml's evidence step, pulls from implementation if available
tier2-findings-scaffold        script    depends_on: [tier1-fix]
tier2-findings-content         semantic  depends_on: [tier2-findings-scaffold, tier2-findings-evidence]
tier2-audit/calculate/report/fix   (same script→script→script→semantic pattern)

tier3-{conclusion,references}-scaffold/content/audit/calculate/report/fix   (parallel, no ordering constraint)

tier4-title-and-metadata-scaffold/content/audit/calculate/report/fix        depends_on: [tier3-fix]
```

Note: `loop.yaml`'s own `fix_loop.mechanism` is explicitly
document-level only ("pcems_2026 has no section-scoped generation
templates to target a narrower regenerate at") — a failing fix
regenerates the *entire* domain document, not a single section, unlike
the dev class's per-section fix loop.

## 6. Deterministic Audit via Script

`audit/deterministic/` is confirmed absent. But **this is worth
revisiting, not accepting as permanently semantic-only** — every one of
the 6 `documentation-standards/*.md` files already cites a specific
`audit/deterministic/document/{domain}.yaml` path in its own header
(e.g. `01-title-and-metadata-standards.md`: *"Deterministic rules for
this domain: `audit/deterministic/document/01-title-and-metadata.yaml`"*)
that doesn't exist. That's either a stale forward-reference (written
when a deterministic layer was still planned, then dropped without
updating the doc headers) or a genuine gap. Either way, concrete
candidates exist, straight from the actual rules read:

- **`01-title-and-metadata`**: keyword count ≥ 4-5 (`len(keywords) >=
  4`), corresponding-author email present (regex) — directly
  script-checkable against plain text
- **`06-references`**: APA-style pattern matching (author-year format
  is regex-checkable to a reasonable confidence), reference count
  present
- **`04-findings`**: media-placement rule ("not aggregated at the end")
  is structurally checkable if the source format preserves figure/table
  position relative to first text reference (markdown/LaTeX source,
  not just rendered PDF)
- Typography rules (Arial 14pt/12pt/11pt/8pt, Heading 1/2/3 styles)
  are **only** script-checkable if the paper is authored in a format
  carrying real font metadata (`.docx` via `python-docx`, LaTeX
  `\fontsize` commands) — not checkable from plain Markdown source at
  all, by script or by LLM, since the font information simply doesn't
  exist in that format. This is a source-format dependency worth
  surfacing before assuming these become script checks.

## 7. Generation via Script (`scaffold.py`)

**Cannot be built yet as specified** — `templates/generation/` is
empty (§2). This is the actual blocker for `pcems_2026`'s entire
generation pipeline, not a script-language or capability-contract
question. Once `templates/generation/document/{domain}.md` exists for
each of the 6 domains (content matching what `documentation-standards/`
already specifies), `scaffold.py` follows the same mechanical pattern
as every other system: create the file, headings from the template.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

`calculate.py` implements: `semantic_document_v1`-equivalent (no stable
ID confirmed in this system's `calculation/semantic/document.yaml` —
worth checking it uses the same ID as `base_dev`'s or its own),
`final_score_v1`, `score_bands_v1`, `trend_v1`, plus
`calculation/validation/scoring_validation.yaml`'s own bounds-checking
(`val-001`: semantic score in [0,100], `val-002`: final score in
[0,100], `severity: critical, invalidate_audit: true` — this is a
genuinely new capability not present in `base_dev`'s calculation shape:
a validation pre-check on the scoring pipeline itself, run before
trusting `calculate.py`'s output). No deterministic bucket, so
`final_score`'s formula is necessarily simpler than `base_dev`'s
25/25/25/25 four-bucket weighting — worth confirming exactly what
`final_score.yaml` weights against (likely semantic-only, single
input). `report.py` renders `templates/audit/summary/{domain}-report.md`.

## 9. Script Language Priority Applied

All greenfield, no `script/` directory exists today:
- `scripts/init.py` — §5's phase plan
- `scripts/scaffold.py` — blocked on templates existing first (§7)
- `scripts/validate.py` — minimal/no-op today (§6 — no deterministic
  rules exist yet), becomes real once the candidates in §6 are built
- `scripts/calculate.py` — §8
- `scripts/report.py` — §8
- `scripts/plan_generation.py`

## 10. Open Questions / Risks Specific to `pcems_2026`

- **`templates/generation/` is empty — this system cannot generate a
  paper today.** This is the single most important finding: everything
  else in this proposal (§5's phase plan, §7's scaffold logic) is
  correctly *specified* by `loop.yaml` and `documentation-standards/`,
  but has no templates to actually execute against. This blocks
  generation entirely, independent of any script/semantic policy
  question.
- The `documentation-standards/*.md` files' dangling references to
  `audit/deterministic/document/{domain}.yaml` paths that don't exist
  (§6) should be resolved one way or the other — either author those 6
  files (favoring §6's candidates), or edit the doc headers to stop
  citing a path that was apparently abandoned, since `loop.yaml`
  explicitly and confidently states "no deterministic layer" as if it
  were a settled design choice, not an in-progress gap.
- `calculation/semantic/document.yaml`'s stable ID wasn't confirmed
  against `base_dev`'s `semantic_document_v1` — if `base_academic`
  extraction (per that proposal) assumes a shared calculation shape,
  this needs verifying, not assuming.

## 11. Explicitly Out of Scope

Actual script implementation. Extraction of `base_academic` itself —
separate document. Authoring the missing `templates/generation/`
content (§10's primary finding) — flagged here as the system's actual
blocker, not resolved in this proposal. Any change to the 6 domains'
existing formatting rules.
