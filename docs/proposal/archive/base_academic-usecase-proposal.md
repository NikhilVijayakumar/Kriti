# base_academic — Usecase & Pipeline Proposal

## 0. Why This Document Exists

`academic/base_academic/` (and `pcems_2026`/`eswa_journal` on top of it) currently
contains **zero registered usecases**. Confirmed by direct inspection:

- `base_academic/` has no `standard.yaml`, no `script/`, no `prompt` content —
  only static YAML (`calculation/`, `plan/core/loop.yaml`, `docs/`). Nothing in
  it is dispatchable through samgraha's `usecase`/`step`/`step_script`/
  `step_prompt` tables (`schema/knowledge/01-05.sql`).
- `pcems_2026/plan/usecase/` and `eswa_journal/plan/usecase/` both exist as
  **empty directories**. No `.md`, no `standard.yaml`, no scripts anywhere
  under either system.
- Compare to `python_hackathon`: `script/schema/standard.yaml` registers 12
  scripts, 20 prompts, 12 custom tables, and 8 usecases with fully expanded
  ordered steps, wired to real `wrap_*.py` adapters over the samgraha
  `--repo-root/--in/--out` capability contract. That system is executable
  today. The academic class is not — it is a set of design documents with no
  execution surface. That is the "unusable" gap this proposal closes.

This document proposes the usecase/step/script/prompt layer for
**`base_academic` only** — generic across every academic-paper system, not
`pcems_2026`- or `eswa_journal`-specific. Per-system domain lists, rubric
content, and generation templates stay owned by the concrete systems exactly
as the earlier `base_academic-proposal.md` (now archived) established.

## 1. Usecase Taxonomy

Three entry usecases, keyed off one classification fact about the target
repo: does an implementation exist, and does paper-support analysis
documentation already exist for it.

| # | State | Can validate against implementation? | Entry usecase |
|---|-------|----------------------------------------|----------------|
| 1 | New repo, no implementation (or docs-only repo) | **No** — nothing to validate against | `draft-from-docs-only` |
| 2 | Existing repo, implementation present, **no** analysis docs yet | Yes, once analysis docs exist | `generate-analysis-docs` → falls through to #3 |
| 3 | Existing repo, implementation present, analysis docs already present | Yes | `generate-paper-draft` |

Samgraha's schema has no branching primitive — `step.kind` is the only thing
it interprets (`deterministic` vs `semantic`). Routing between these three
usecases is therefore not a schema concept; it is one deterministic script
(`classify-repo`) whose output an orchestrator (same shape as the existing
`run_full_workflow.py` design from the archived proposal §7.6) reads before
deciding which usecase to invoke next. This matches how samgraha already
works — the MCP client decides which usecase to call; samgraha just executes
what it's told.

```
classify-repo (deterministic, always runs first)
  ├─ NEW_NO_IMPL          → draft-from-docs-only
  ├─ EXISTING_NO_ANALYSIS → generate-analysis-docs → generate-paper-draft
  └─ EXISTING_WITH_ANALYSIS → generate-paper-draft
```

### 1.1 Usecase: `schema-init`

Same role as `python_hackathon`'s `schema-init` — must run once before
anything else writes to `knowledge.db`.

```yaml
- name: schema-init
  description: "create base_academic's own tables before anything else writes to them"
  steps:
    - order: 1
      kind: deterministic
      script: init-schema
```

### 1.2 Usecase: `classify-repo`

```yaml
- name: classify-repo
  description: "entry router — inspect target repo, classify into NEW_NO_IMPL / EXISTING_NO_ANALYSIS / EXISTING_WITH_ANALYSIS, persist to academic_repos"
  steps:
    - order: 1
      kind: deterministic
      description: "Scan repo for implementation evidence (source files beyond docs/config) and docs/paper/{system}/ analysis tree; persist classification"
      script: classify-repo
```

No semantic step — classification is a filesystem fact, not a judgment call.

### 1.3 Usecase: `draft-from-docs-only` (entry #1 — new repo)

No implementation evidence exists, so every quantitative claim in the draft
is unverifiable by construction. The generation prompt must know this and
flag accordingly — reusing the same `[NEEDS AUTHOR INPUT]` convention
`humanifier.md` already established, rather than inventing a second flag
vocabulary.

```yaml
- name: draft-from-docs-only
  description: "usecase 1 — draft paper/journal domains from documentation alone, no implementation to validate against. Every domain is a pre/semantic/post triad."
  steps:
    # repeated per domain in the concrete system's own domain list
    - order: 1
      kind: deterministic
      description: "Pre: gather whatever documentation exists (README, docstrings, author notes) for {domain}. No implementation evidence available."
      script: gather-domain-evidence
    - order: 2
      kind: semantic
      description: "Draft {domain} from documentation only. Flag every claim needing implementation proof as [NEEDS AUTHOR INPUT] rather than inventing numbers."
      prompt: generate-section-docs-only
    - order: 3
      kind: deterministic
      description: "Post: persist draft, mark academic_narratives.validated = false for this domain"
      script: persist-section-draft
```

Output is explicitly marked unvalidated in the data model (§4) so downstream
audit/scoring never silently treats it as evidence-grounded.

### 1.4 Usecase: `generate-analysis-docs` (entry #2, step A — existing repo, no analysis docs)

This formalizes what `Bodha/docs/paper/**` already does **by hand** today —
per-module analysis, then cross-module rollup. That tree is the working
precedent for depth (`architecture.md` with mermaid diagrams, `mathematics.md`
with formal notation, `novelty.md` with evidence-linked claims, `gaps.md`,
plus `patterns.md`/`dependencies.md`/`interactions.md` at the cross-module
level). This usecase is what makes that process repeatable through samgraha
instead of manual per-project effort.

**Per-module pass** (one pre/semantic/post triad per analysis kind, per
detected module):

```yaml
- name: generate-analysis-docs
  description: "usecase 2, step A — generate paper-support analysis docs from an existing implementation, module-by-module then cross-module. Owned entirely by base_academic — not a base_dev delegation, since this is paper-writing evidence, not general project documentation."
  steps:
    - order: 1
      kind: deterministic
      description: "Discover module boundaries (top-level packages) in the target repo; persist to academic_modules"
      script: discover-modules

    # --- repeated per (module, analysis_kind) where analysis_kind in
    #     [summary, architecture, mathematics, novelty, gaps] ---
    - order: 2
      kind: deterministic
      description: "Pre: gather one module's source files, imports, docstrings, signatures"
      script: gather-module-evidence
    - order: 3
      kind: semantic
      description: "Write module {analysis_kind} section (architecture includes a ```mermaid block per docs/mermaid-diagram-standards.md)"
      prompt: module-analysis-{analysis_kind}
    - order: 4
      kind: deterministic
      description: "Post: persist section to academic_module_analysis + write docs/paper/{system}/modules/{module}/{analysis_kind}.md"
      script: persist-module-analysis

    # --- cross-module pass, runs once all modules complete, repeated per
    #     analysis_kind in [architecture, dependencies, interactions,
    #     patterns, gaps, mathematics, novelty] ---
    - order: 5
      kind: deterministic
      description: "Pre: aggregate every module's evidence + repo-wide import graph"
      script: gather-cross-module-evidence
    - order: 6
      kind: semantic
      description: "Write cross-module {analysis_kind} section"
      prompt: cross-module-analysis-{analysis_kind}
    - order: 7
      kind: deterministic
      description: "Post: persist to academic_cross_module_analysis + write docs/paper/{system}/cross_module/{analysis_kind}.md"
      script: persist-cross-module-analysis
```

Real expansion (like `python_hackathon`'s `semantic-audit` usecase expanding
10 domains into 30 concrete steps) turns this into `5 module-kinds × N
modules × 3 steps` plus `7 cross-kinds × 3 steps`, all flat ordered steps —
no dependency graph needed, cross-module steps simply come after every
module's steps in `step_order`.

### 1.5 Usecase: `generate-paper-draft` (entry #3 — analysis docs present)

This is what §1.4 falls through to once analysis docs exist, and what entry
#3 goes to directly. Extends the existing `run_domain_evidence.py` /
`path_selection.evidence` mechanism already specified in
`base_academic/plan/core/loop.yaml` — the evidence source is now the analysis
docs tree from §1.4, not just author-supplied notes.

```yaml
- name: generate-paper-draft
  description: "usecase 3 — generate paper/journal domain drafts from analysis docs + implementation evidence. Same pre/semantic/post triad shape as draft-from-docs-only, but evidence-grounded."
  steps:
    # repeated per domain in the concrete system's own domain list
    - order: 1
      kind: deterministic
      description: "Pre: pull analysis-doc excerpts relevant to {domain} + evidence.applies_to_domains implementation numbers (loop.yaml)"
      script: gather-domain-evidence
    - order: 2
      kind: semantic
      description: "Generate {domain} per templates/generation/document/{domain}.md, citing analysis docs as evidence"
      prompt: generate-section
    - order: 3
      kind: deterministic
      description: "Post: persist draft, mark academic_narratives.validated = true where evidence backs the claim"
      script: persist-section-draft
```

## 2. Shared Downstream Pipeline

Everything below runs after a base draft exists, regardless of which entry
usecase produced it. This is the part of your ask that maps to "deepen each
section," "plagiarism check → validate → fix," and "humanify."

### 2.1 Usecase: `deepen-sections`

```yaml
- name: deepen-sections
  description: "usecase 4 — enrich an existing draft with literature review, mathematical formalization, and figures/diagrams. Runs after generate-paper-draft or draft-from-docs-only."
  steps:
    # repeated per domain, per enrichment_kind in [literature-review, mathematics, figures]
    - order: 1
      kind: deterministic
      description: "Pre: gather current draft text + analysis docs + citation notes for {domain}"
      script: gather-enrichment-context
    - order: 2
      kind: semantic
      description: "{enrichment_kind} pass over {domain} (figures pass emits ```mermaid blocks per docs/mermaid-diagram-standards.md)"
      prompt: "{enrichment_kind}-pass"
    - order: 3
      kind: deterministic
      description: "Post: persist enriched section, increment academic_narratives.iteration, stage={enrichment_kind}"
      script: persist-section-draft
```

### 2.2 Usecase: `semantic-audit`

This is the concrete wiring `base_academic/calculation/semantic/document.yaml`
already assumes exists but never registered — one rubric file per domain,
same triad shape as `python_hackathon`'s `2b`.

```yaml
- name: semantic-audit
  description: "usecase — score a domain draft against calculation/semantic/document.yaml + audit/semantic/document/{domain}.md (concrete-system-owned rubric)"
  steps:
    # repeated per domain
    - order: 1
      kind: deterministic
      description: "Pre: gather {domain}'s current draft + rubric criteria"
      script: gather-domain-evidence
    - order: 2
      kind: semantic
      description: "Score {domain} against its rubric"
      prompt: "semantic-audit-{domain}"   # concrete-system-owned, same as python_hackathon's per-domain prompts
    - order: 3
      kind: deterministic
      description: "Post: persist score, findings"
      script: persist-domain-semantic-score
```

Feeds `plan/core/loop.yaml`'s existing `fix_loop`/`tier_gate` machinery
unchanged — this usecase just makes Path B ("audit → fix") in that loop
actually dispatchable.

### 2.3 Usecase: `plagiarism-fingerprint-check`

New. `eswa_journal/templates/generation/humanifier.md` already names the
target failure mode ("linguistic fingerprints that will fail the AI
Plagiarism & Fingerprint Audits") but no audit that actually produces that
verdict exists anywhere in the codebase today — confirmed by grep, zero
hits beyond that one reference. This usecase is the audit `humanifier.md`
assumes is upstream of it.

```yaml
- name: plagiarism-fingerprint-check
  description: "usecase 5 — audit a section for AI-generated fingerprint patterns (low burstiness, hollow claims, mechanical structure) before humanize. PASS/FAIL, not a score — feeds fix_loop like semantic-audit does."
  steps:
    # repeated per domain
    - order: 1
      kind: deterministic
      description: "Pre: gather {domain}'s current draft text"
      script: gather-plagiarism-context
    - order: 2
      kind: semantic
      description: "Check for AI fingerprint patterns per templates/audit/plagiarism-fingerprint.md; flag specific spans, not just a verdict"
      prompt: plagiarism-fingerprint-audit
    - order: 3
      kind: deterministic
      description: "Post: persist PASS/FAIL + flagged spans to academic_plagiarism_findings"
      script: persist-plagiarism-findings
```

### 2.4 Usecase: `humanize`

Promotes `eswa_journal/templates/generation/humanifier.md` to
`base_academic/templates/generation/humanifier.md` — generalized (its
current text uses eswa-specific examples like "+8.4% F1"; the 3-layer
mechanism itself — structural rhythm, technical-DNA injection, voice
restoration — is not eswa-specific). Both `pcems_2026` and `eswa_journal`
inherit it once promoted, same override-resolution rule `system.yaml`
already documents (concrete system's own file wins if present).

```yaml
- name: humanize
  description: "usecase 6 — rewrite a section flagged by plagiarism-fingerprint-check using the 3-layer humanifier pass"
  steps:
    # repeated per domain, triggered when plagiarism-fingerprint-check returns FAIL
    - order: 1
      kind: deterministic
      description: "Pre: gather {domain}'s draft + this run's flagged spans from academic_plagiarism_findings"
      script: gather-humanize-context
    - order: 2
      kind: semantic
      description: "3-layer humanize rewrite (structural rhythm, technical-DNA injection, voice restoration)"
      prompt: humanize-section
    - order: 3
      kind: deterministic
      description: "Post: persist rewritten section + change summary + [NEEDS AUTHOR INPUT] risk flags to academic_humanize_passes"
      script: persist-humanize-pass
```

`humanize` re-enters `plagiarism-fingerprint-check` on its output — this is
the `fix_loop` from `plan/core/loop.yaml` applied to this specific failure
mode, capped by the same `max_iterations: 5` / `fallback: human_review`
already defined there. No new fix-loop mechanism needed, this usecase pair
just gives the existing one something concrete to call.

### 2.5 Usecases: `calculate`, `render`

Unchanged from the archived proposal's §10 — `calculate.py` /
`report.py` implementing `final_score_v1`/`score_bands_v1`/`trend_v1` from
the already-identical `calculation/summary/*.yaml` files. Still unbuilt;
included here only to show where they sit in the full chain (§5).

## 3. Folder Structure

Generated artifacts live **inside the target repo**, following the
`Bodha/docs/paper/` precedent exactly rather than inventing a new
convention:

```
<repo>/docs/paper/{system}/
├── modules/{module}/
│   ├── summary.md
│   ├── architecture.md        # includes ```mermaid blocks
│   ├── mathematics.md
│   ├── novelty.md
│   └── gaps.md
├── cross_module/
│   ├── architecture.md
│   ├── dependencies.md        # ```mermaid flowchart, classDef-styled
│   ├── interactions.md
│   ├── patterns.md
│   ├── gaps.md
│   ├── mathematics.md
│   └── novelty.md
├── drafts/
│   └── document/{domain}.md   # current draft, stage=generate|deepen|humanize
├── audit/
│   ├── {domain}-semantic-findings.md
│   └── {domain}-plagiarism-findings.md
└── final/
    └── {system}-{paper|journal}.md   # assembled, post tier_gate
```

Template ownership splits at the base/concrete boundary the same way
`calculation/` already does:

| Template | Owner | Reason |
|---|---|---|
| `templates/generation/analysis/module/{kind}.md` | `base_academic` | Module analysis structure (summary/architecture/mathematics/novelty/gaps) isn't paper-specific — same shape regardless of target venue |
| `templates/generation/analysis/cross_module/{kind}.md` | `base_academic` | Same reasoning |
| `templates/generation/enrichment/{kind}.md` | `base_academic` | Literature review / mathematics / figures passes are generic enrichment operations |
| `templates/generation/humanifier.md` | `base_academic` (promoted) | Mechanism is generic; per your decision this session |
| `templates/audit/plagiarism-fingerprint.md` | `base_academic` | New, generic detection criteria |
| `templates/generation/document/{domain}.md` | concrete system | Domain list and content depth differ per venue (confirmed divergent in the archived proposal §2) |
| `audit/semantic/document/{domain}.md` | concrete system | Same reasoning — rubric content is venue-specific |

## 4. New Custom Tables

Extends the 8 tables the archived proposal already specified
(`academic_papers`, `academic_domains`, `academic_semantic_runs`,
`academic_semantic_dimension_scores`, `academic_semantic_findings`,
`academic_narratives`, `academic_narrative_sections`, `academic_templates`).
`academic_narratives`/`academic_narrative_sections` are reused as the
section-draft store (not a new table) — in this class, the "narrative" a
domain produces *is* the paper section content, unlike `python_hackathon`
where narrative is commentary about an audited artifact. Two columns need
adding to support the fix-loop iteration history in §2.1/§2.4:
`academic_narratives.stage` (`generate`/`deepen`/`humanize`) and
`academic_narratives.iteration` (int).

New tables:

| Table | Purpose | Owner script |
|---|---|---|
| `academic_repos` | One row per (repo_root, system) classification result | `classify-repo` |
| `academic_modules` | One row per detected module in a repo | `discover-modules` |
| `academic_module_analysis` | Per (module, analysis_kind) section content | `persist-module-analysis` |
| `academic_cross_module_analysis` | Per (repo, analysis_kind) section content | `persist-cross-module-analysis` |
| `academic_plagiarism_findings` | Per (paper, domain, run): PASS/FAIL + flagged spans | `persist-plagiarism-findings` |
| `academic_humanize_passes` | Per (paper, domain, iteration): change summary + risk flags | `persist-humanize-pass` |

## 5. Full Workflow Orchestrator

Same shape as the archived proposal's §7.6 `run_full_workflow.py` — drives
everything through the real MCP `mcp` binary, never subprocess-calls scripts
directly:

```
1. register_standard        (re)registers base_academic's usecases/steps/scripts/prompts
2. schema-init               creates the 14 custom tables
3. classify-repo             NEW_NO_IMPL | EXISTING_NO_ANALYSIS | EXISTING_WITH_ANALYSIS
4. [if EXISTING_NO_ANALYSIS] generate-analysis-docs
5. draft-from-docs-only  OR  generate-paper-draft   (per classification)
6. deepen-sections            literature review / mathematics / figures, per domain
7. semantic-audit              score against rubric, per domain
8. plagiarism-fingerprint-check → humanize (loop until PASS or max_iterations)
9. fix_loop / tier_gate        existing plan/core/loop.yaml mechanism, now dispatchable
10. calculate                  final_score / score_bands / trend
11. render                     assemble docs/paper/{system}/final/{system}-{paper|journal}.md
```

Every semantic step (module analysis, cross-module analysis, section
generation, enrichment, plagiarism audit, humanize) is only **staged**
(`prepare_semantic_step`) — completing it needs a real model turn, same
`prepare`/`complete_semantic_step` split as the existing 2b/4 pattern.

## 6. Mermaid Diagram Convention

New: `base_academic/docs/mermaid-diagram-standards.md`. Codifies the pattern
already proven (by hand) in `Bodha/docs/paper/**`, so every semantic step
that emits a diagram produces the same style rather than each generation
producing its own ad hoc formatting:

- Every diagram is a fenced ` ```mermaid ` block, opening with
  `%%{init: {'theme': 'base'}}%%`.
- `architecture.md` (module level): `classDiagram`, one class per major
  component, `<<stereotype>>` annotations (e.g. `<<Singleton Component>>`,
  `<<Facade>>`) naming the design pattern, not just the class name.
- `dependencies.md` / `interactions.md` (cross-module level): `flowchart TD`
  with `classDef` color-coded tiers (e.g. `core`/`support`/`shared`/
  `external`) so coupling direction and layer are visible at a glance.
- `mathematics.md`: no diagram — LaTeX (`$...$` / `$$...$$`) blocks only.
- `novelty.md` / `gaps.md`: no diagram — prose with evidence links
  (`[Symbol](file:///path#Lline)`), matching the code-verified-claim pattern
  already used in `Bodha/docs/paper/Amsha/cross_module/novelty.md`.

This is a shared prompt fragment every diagram-emitting prompt
(`module-analysis-architecture`, `cross-module-analysis-dependencies`,
`cross-module-analysis-interactions`, `figures-pass`) includes verbatim, so
diagram style stays consistent without repeating the rules in each prompt
file.

## 7. Open Questions / Risks

- **Module boundary detection** (`discover-modules`): "top-level package"
  is the working heuristic (matches how `Bodha/docs/paper/Amsha/modules/`
  splits `crew_forge`/`llm_factory`/`crew_monitor`/`output_process`), but
  monorepos or flat single-module repos may need a different heuristic.
  Deferred to implementation — flagged, not resolved here.
- **`draft-from-docs-only` validation debt**: sections drafted from docs
  alone stay `validated = false` indefinitely unless someone later runs
  `generate-analysis-docs` + re-runs `generate-paper-draft` against real
  implementation evidence. No automatic promotion path is proposed here —
  worth deciding whether re-running should overwrite or version-append.
- **Humanifier promotion** touches an eswa-authored file; verify none of its
  current eswa-specific examples (F1 scores, RTX 4070 Ti, CRF-vs-softmax)
  leak into the generalized base version — needs an actual editing pass at
  implementation time, not just a `git mv`.
- **Cost**: `generate-analysis-docs`'s per-module × 5-kind × 3-step
  expansion is the same shape that made `python_hackathon`'s
  `semantic-audit` usecase 30 steps for 10 domains — for a repo with, say,
  8 modules, that's 8×5×3 = 120 steps for analysis alone, before any paper
  domain generation. Real but expected, same order of magnitude as the
  already-working reference system.

## 8. Explicitly Out of Scope

Actual script/prompt implementation — this document specifies the usecase
shape, not the Python. Migrating `pcems_2026`/`eswa_journal` to register
against this (their `plan/usecase/` dirs need the same `standard.yaml`
treatment, scoped to their own domain lists) — follow-up work, not this
document. Resolving the `conclusion` domain contradiction between the two
systems (archived proposal §2) — unrelated to usecase wiring.
