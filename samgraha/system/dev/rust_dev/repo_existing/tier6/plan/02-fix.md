# Stage 2 - Fix or Create

**Use case:** `repo_existing/tier6`
**Tier:** 6
**Domains:** qa

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

Once QA has final score ≥ the Acceptable band minimum, the tier clears and Tier 7 can begin.

## Differs From Other Use Cases

No difference vs repo_existing_no_doc/tier6 (identical after its one-time bootstrap-readme usecase). vs repo_new/tier6: this workflow audits first - no generate/migrate stage, per-domain create runs only where the audit finds no conforming doc - but the fix-or-create procedure is shared.