# Stage 3 → Fix

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 2
**Domains:** security, feature, architecture, design, engineering, external-context

## Input

Reports from stage 2 (`02-audit.md`): per-domain scores and failure details.

## Procedure

For each domain, check the final score against the gate threshold. If below threshold, decide fix scope, apply the fix, then re-run stage 2. Loop stages 2→3 until gate clears or fallback triggers.

### Threshold

- **Score:** the Acceptable band minimum)
- **Rating:** Acceptable

### Fix Scope Decision

- **Section-level fix** if failures are isolated to ≤2 sections AND no whole-document criterion failed. Apply via `templates/generation/section/{domain}/{section}.md`'s `## Audit Fix` slot.
- **Whole-document regeneration** otherwise. Apply via `templates/generation/document/{domain}.md`.

### Fix Loop

1. Apply fix (section-level or whole-document).
2. Re-run stage 2 on the fixed document.
3. Check score against threshold.
4. If below threshold and iterations < 5: repeat from step 1.
5. If iterations = 5: fallback → flag remaining failures for human review.

### Max Iterations

`max_iterations: 5` — per `core/loop.yaml`. After 5 iterations, fallback to `human_review`. Tier gate stays hard.

### Tier Gate

Once every domain in Tier 2 (security, feature, architecture, design, engineering, external-context) has a final score ≥ the Acceptable band minimum, the tier clears and Tier 3 can begin.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documentation`:** No difference → same fix procedure.
- **vs. `repo_existing/case_1_no_documentation`:** No difference → same fix procedure.
- **vs. `repo_existing/case_2_has_documentation`:** No difference → same fix procedure.
