
# Use-case 1 — Generate Analysis Docs

**Script**: `discover-modules` (deterministic, 1 step) + per-module and
cross-module pre/semantic/post triads (`expand_triads()` in
`run_full_workflow.py`, dynamically inserted after `classify-repo` runs —
step count depends on the target repo's actual module count, not fixed at
registration time)

**Inputs**:
- Target repo's source tree (module boundaries — top-level packages,
  per `discover_modules.py`)
- `templates/generation/analysis/module/{summary,architecture,mathematics,
  novelty,gaps}.md` prompts (5 kinds × N modules)
- `templates/generation/analysis/cross_module/{architecture,dependencies,
  interactions,patterns,gaps,mathematics,novelty}.md` prompts (7 kinds,
  once)

**Action**: Per module, per analysis kind: `gather-module-evidence` (pre)
→ semantic write → `persist-module-analysis` (post), writing to
`academic_module_analysis` and `docs/paper/{system}/modules/{module}/
{kind}.md`. Once every module's steps complete: per cross-module kind,
`gather-cross-module-evidence` (pre) → semantic write →
`persist-cross-module-analysis` (post), writing to
`academic_cross_module_analysis` and `docs/paper/{system}/cross_module/
{kind}.md`.

**Completion criteria**:
- One `academic_module_analysis` row per (module, kind) — `5 × module_count`
  rows total
- One `academic_cross_module_analysis` row per kind — 7 rows total
- `academic_repos.has_analysis_docs` flips to `1` for this repo once both
  are satisfied (checked by a subsequent `classify-repo` re-run, not this
  usecase itself — it doesn't self-update its own precondition)

**Verify script**: `verify_usecase_1_generate_analysis_docs.py --standard base_academic --paper-id <id>`
- Reports `N/5` per module and `N/7` cross-module
- Exits 0 only if every module has 5/5 and cross-module has 7/7

**Rule**: Only runs for `IMPL_NO_ANALYSIS` classification. Mandatory, not
optional — `classify-repo` refuses to hand `IMPL_NO_ANALYSIS` straight to
usecase 2b (see `docs/proposal/base_academic-data-pipeline-proposal.md`
§3). Falls through to usecase 2b once complete.
