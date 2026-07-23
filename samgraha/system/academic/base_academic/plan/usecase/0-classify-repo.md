# Use-case 0 — Classify Repo

**Script**: `classify_repo.py` (deterministic, single step, no triad — one
run per repo)

**Inputs**:
- Target repo's filesystem: implementation evidence (source files beyond
  docs/config) and `docs/paper/{system}/` analysis-doc tree

**Action**: Resolves the repo to one of 4 states and persists to
`academic_repos` via `upsert_repo_classification`:

| State | Docs? | Impl? | Downstream |
|---|---|---|---|
| `NO_DOCS_NO_IMPL` | no | no | Refuse — no usecase runs past this point |
| `DOCS_ONLY` | yes | no | → 2a (`draft-from-docs-only`) |
| `IMPL_NO_ANALYSIS` | no | yes | → 1 (`generate-analysis-docs`), falls through to 2b |
| `IMPL_WITH_ANALYSIS` | yes | yes | → 2b (`generate-paper-draft`) directly |

Also registers the paper (`register_paper`) and records `module_count` for
`IMPL_*` states, used later by usecase 1's per-module step expansion.

**Completion criteria**:
1. Exactly one `academic_repos` row exists for this `(standard, repo_root)`
2. `classification` is one of the 4 valid values (enforced by the table's
   `CHECK` constraint)
3. If `classification IN ('IMPL_NO_ANALYSIS', 'IMPL_WITH_ANALYSIS')`,
   `academic_papers` has a matching row

**Verify script**: `verify_usecase_0_classify_repo.py --standard base_academic --repo-root <path>`
- Exits 0 + prints the resolved classification
- Exits 1 if no `academic_repos` row exists, or if `classification` is
  `NO_DOCS_NO_IMPL` (a valid classification, but the caller should treat a
  0 exit differently from "ready to proceed" — the workflow orchestrator
  checks this explicitly and stops, per `run_full_workflow.py`'s refused-path
  short-circuit)

**Rule**: Always runs first, before anything else including `schema-init`
reads its output. Idempotent — re-running on an unchanged repo produces the
same classification (via `UPDATE`, not a new row).
