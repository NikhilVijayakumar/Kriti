# Stage 2 - Fix or Create

**Use case:** `repo_existing/tier8`
**Tier:** 8
**Domains:** readme, product-guide

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

Once every domain in Tier 8 has final score ≥ the Acceptable band minimum, the tier clears. **This is the finish line** → all 16 domains across all 8 tiers have cleared their gates. The repository's documentation is compliant.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier8 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier8: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the fix-or-create procedure is shared.