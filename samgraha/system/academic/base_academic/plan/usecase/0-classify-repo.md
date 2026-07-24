# Use-case 0 — Classify Repo

**Script**: `classify_repo.py` (deterministic, single step)

**Inputs**:
- Target repo's filesystem: documentation surface (README, docs/, top-level .md)
  and implementation evidence (source files)

**Action**: 2-state classification based on author-supplied documentation:

| State | Meaning | Downstream |
|---|---|---|
| `NO_DOCS` | Repo has no author-supplied documentation (or < 200 words) | **Refuse — terminal.** No usecase runs past this point. |
| `HAS_DOCS` | Repo has author-supplied documentation (>= 200 words) | Proceed to novelty-analysis |

Also records `has_implementation` as metadata (useful for claim grounding)
but it no longer drives branching.

**Completion criteria**:
1. Exactly one `academic_repos` row exists for this `(standard, repo_root)`
2. `classification` is one of `NO_DOCS` or `HAS_DOCS`

**Rule**: Always runs first. Idempotent — re-running produces the same classification.
