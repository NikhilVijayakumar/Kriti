# Stage 3 → Fix

**Use case:** `repo_existing/case_2_has_documention`
**Tier:** 8
**Domains:** readme, product-guide

## Input

Reports from stage 2 (`02-audit.md`).

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

No difference → same fix procedure.
