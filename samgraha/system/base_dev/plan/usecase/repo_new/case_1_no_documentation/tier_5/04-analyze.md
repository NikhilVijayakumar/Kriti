# Tier 5 — Analysis & Fix Plan

**Use case:** New repo, no code, no docs — only a product idea as input
**Threshold:** `Acceptable`

## What This Phase Does

After scores are calculated and reports rendered, the analyze phase
reads all evaluation results and produces a structured fix plan.
The fix plan identifies:
- Which domains/sections are failing
- Why they are failing (specific rule/criterion violations)
- Whether the fix should be section-level or whole-document
- Prioritized list of fixes by severity and score impact

## Script

`scripts/analyze.py` — reads `{domain}-scores.json`, `{domain}-validation.json`,
`{domain}-det-eval.json`, and `{domain}-sem-eval.json` from the output directory.
Produces `{domain}-fix-plan.json`.

## Fix Plan Structure

```json
{
  "domain": "01-vision",
  "status": "fix_needed",
  "final_score": 45.5,
  "threshold": "Acceptable",
  "fix_scope": "section_level",
  "fix_scope_reason": "3 sections failing",
  "fixes": [
    {
      "priority": 1,
      "type": "error",
      "source": "deterministic_rule",
      "id": "vis-doc-001",
      "scope": "document",
      "message": "Missing sections: problem, solution"
    }
  ]
}
```

## Fix Scope Decision

- **Section-level**: ≤5 sections failing, targeted fixes to specific sections
- **Whole-document**: >5 sections failing or >15 section-level findings — regenerate from scratch
- **Document-level**: only document-wide issues (e.g. technology references)

## Confirmation Checkpoint

After the fix plan is generated, it is presented to the user via the
rendered HTML report. The user can:
- **Approve** the plan as-is
- **Edit** scope (e.g. 'also fix this section' / 'skip that one')
- **Reject** the plan entirely (falls back to human review)

The fix phase executes ONLY the confirmed plan.

## Domains

- `implementation`

## Outputs

Per domain in this tier:
- `{domain}-fix-plan.json` — structured fix plan
- Reviewed via HTML report before fix phase executes
