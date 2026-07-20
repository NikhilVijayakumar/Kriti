# Tier 1 — Fix Loop

**Use case:** New repo, no code, no docs — only a product idea as input
**Max iterations:** 5
**Threshold:** `Acceptable`
**Fallback:** human_review

## Fix Procedure

For each domain in this tier that scores below threshold:

1. Identify failing sections from audit findings
2. Re-run content-fill with expanded context (all completed domains)
3. Re-validate and re-calculate
4. Repeat until threshold met or max iterations reached
5. If max iterations exceeded: flag for human review

## Domains

- `vision`
- `philosophy`

## Iteration Tracking

Each iteration is logged to console with:
- Current score vs threshold
- Which sections were re-filled
- Re-scored result after fix

Score history persisted to `score_history.json` after each successful calculate.
