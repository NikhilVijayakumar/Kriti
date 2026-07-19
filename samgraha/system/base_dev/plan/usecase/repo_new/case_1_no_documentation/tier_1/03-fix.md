# Stage 3 → Fix

**Use case:** `repo_new/case_1_no_documentation`
**Tier:** 1
**Domains:** vision, philosophy

## Input

Reports from stage 2 (`02-audit.md`): per-domain scores and failure details.

## Procedure

For each domain, check the final score against the gate threshold. If below threshold, decide fix scope, apply the fix, then re-run stage 2. Loop stages 2→3 until gate clears or fallback triggers.

### Threshold

- **Score:** the Acceptable band minimum — score_bands (resolved at runtime))
- **Rating:** Acceptable

### Fix Scope Decision

Read the stage 2 report. For each failing domain:

- **Section-level fix** if ALL of the following are true:
  - Failures are isolated to ≤2 sections
  - No whole-document criterion (`deterministic_whole` or `semantic_whole`) failed
  
  Apply via `templates/generation/section/{domain}/{section}.md`'s `## Audit Fix` slot for each failing section.

- **Whole-document regeneration** otherwise (failures spread across 3+ sections, OR any whole-document criterion failed).
  
  Apply via `templates/generation/document/{domain}.md` → regenerate the full document, incorporating the findings from the audit report.

### Fix Loop

1. Apply fix (section-level or whole-document, per above).
2. Re-run stage 2 (`02-audit.md`) on the fixed document.
3. Check score against threshold.
4. If below threshold and iterations < 5: repeat from step 1.
5. If iterations = 5: **fallback** → flag remaining failures for human review. Domain does not clear gate until human resolves.

### Max Iterations

`max_iterations: 5` — per `core/loop.yaml`. After 5 iterations, fallback to `human_review`. The tier gate stays hard: the domain does not advance until the human resolves the flagged failures and the domain re-audits above threshold.

### Tier Gate

Once every domain in Tier 1 (vision, philosophy) has a final score ≥ the Acceptable band minimum, the tier clears and Tier 2 can begin.

## Output

- If gate clears: confirmation that both domains pass threshold, ready for Tier 2.
- If fallback triggers: list of flagged failures per domain, awaiting human review.

## Differs From Other Use Cases

- **vs. `repo_new/case_2_has_documentation`:** No difference at Tier 1 → same fix procedure.
- **vs. `repo_existing/case_1_no_documentation`:** No difference at Tier 1 → same fix procedure.
- **vs. `repo_existing/case_2_has_documentation`:** No difference at Tier 1 → same fix procedure.
