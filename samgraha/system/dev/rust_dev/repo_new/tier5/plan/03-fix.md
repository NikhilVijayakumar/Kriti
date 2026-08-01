# Stage 3 → Fix

**Use case:** `repo_new/tier5`
**Tier:** 5
**Domains:** implementation

## Input

Report from stage 2 (`02-audit.md`): score and failure details.

## Procedure

Check score against threshold (the Acceptable band minimum). Below threshold → decide fix scope, apply, re-run stage 2. Loop until gate clears or fallback triggers.

### Fix Scope Decision

- **Section-level fix** if failures isolated to ≤2 sections AND no whole-document criterion failed.
- **Whole-document regeneration** otherwise.

### Fix Loop

`max_iterations: 5`, then `human_review` fallback. Tier gate stays hard.

### Tier Gate

Once implementation has final score ≥ the Acceptable band minimum, the tier clears and Tier 6 can begin.

## Differs From Other Use Cases

No difference across the 3-way split (repo_new/tier5, repo_existing/tier5, repo_existing_no_doc/tier5) - same fix procedure.