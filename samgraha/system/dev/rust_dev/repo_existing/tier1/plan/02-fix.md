# Stage 2 - Fix or Create

**Use case:** `repo_existing/tier1`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Reports from stage 1 (`01-audit.md`).

## Procedure

Check score against threshold (the Acceptable band minimum). Below threshold → decide fix scope, apply, re-run stage 2. Loop until gate clears or fallback triggers.

### Fix Scope Decision

- **Section-level fix** if failures isolated to ≤2 sections AND no whole-document criterion failed.
- **Whole-document regeneration** otherwise.

### Fix Loop

`max_iterations: 5`, then `human_review` fallback. Tier gate stays hard.

### Tier Gate

Once every domain in Tier 1 has final score ≥ the Acceptable band minimum, the tier clears and Tier 2 can begin.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier1 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier1: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the fix-or-create procedure is shared.