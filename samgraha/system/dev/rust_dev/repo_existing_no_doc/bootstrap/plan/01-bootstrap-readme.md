# Stage 0 — Bootstrap (before tier 1, runs once)

**Use case:** `repo_existing_no_doc/bootstrap`
**Tier:** none (cross-tier, runs once before tier 1)
**Domains:** readme (one artifact — an in-depth README drafted from the existing codebase)

## Context Available

Code exists, *zero* documentation anywhere. Distinct from `repo_existing` because there's nothing to audit yet, and distinct from `repo_new` because there's a whole codebase this README grounds itself in before any tier starts.

## Procedure

Draft one in-depth README from the existing codebase. This is the one cross-tier, one-time step in the `repo_existing_no_doc` workflow — not nested under any `tierN/`.

### Bootstrap Steps

1. **Scan repo structure:** inventory crates/modules, entry points, binaries, public API surfaces, build/publish configuration, and any informal notes (code comments, CI config, manifests) that document intent.
2. **Gather existing context:** every source of truth the code itself carries — `Cargo.toml` metadata, `lib.rs`/`main.rs` doc comments, CI workflows, example files.
3. **Draft the README:** use `common/tier8/templates/generation/document/readme.md` as the structural template, grounded in the actual codebase — real crate names, real commands, real file paths, real install/run instructions.
4. **Persist:** write `README.md` at the repo root.

### Relationship to Tier 8's `readme` Domain

The bootstrap README is the **same artifact** tier 8's `readme` domain eventually audits/finalizes — not a throwaway scaffold. It is deliberately drafted before tier 1 so it can serve as grounding context for every tier's generation, then passes through the ordinary tier-8 `deterministic-audit-readme`/`semantic-audit-readme`/`fix-readme` loop like any other domain deliverable. No scoring at this stage.

## Output

One `README.md` at the repo root. After this completes, the workflow is identical to `repo_existing` from tier 1 onward.

## Differs From Other Use Cases

- **vs. repo_new/tier8:** repo_new has no code — its README describes the planned product. This use case drafts against real, existing code.
- **vs. repo_existing/tier8:** repo_existing audits existing docs first. Here there is nothing to audit yet — the README is created, not restructured, and created *before* tier 1, not as part of tier 8.
- **vs. repo_existing_no_doc/tier{1..8}:** this is the only use case that runs outside a tier; every tier after it reuses `repo_existing`'s plan files unchanged.
