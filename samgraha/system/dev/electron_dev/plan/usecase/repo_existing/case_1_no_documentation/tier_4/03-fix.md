# Stage 3 → Fix

**Use case:** `repo_existing/case_1_no_documentation`
**Tier:** 4
**Domains:** prototype

## Input

Report from stage 2 (`02-audit.md`).

## Procedure

Check score against threshold (the Acceptable band minimum). Below threshold → decide fix scope, apply, re-run stage 2. Loop until gate clears or fallback triggers.

### Fix Scope Decision

- **Section-level fix** if failures isolated to ≤2 sections AND no whole-document criterion failed.
- **Whole-document regeneration** otherwise.

### Fix Loop

`max_iterations: 5`, then `human_review` fallback. Tier gate stays hard.

### Tier Gate

Once prototype has final score ≥ the Acceptable band minimum, the tier clears and Tier 5 can begin.

## Differs From Other Use Cases

No difference → same fix procedure.
