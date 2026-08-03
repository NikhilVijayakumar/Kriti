# Render the verification report

You are given the collected verdicts of a verification run. Render the merged
per-domain and system-level verification report.

## Input

`verdicts` — per-level verdicts, each with findings and evidence.

## Report structure

Render, in order:

1. **System-level summary** — overall verdict, total elements checked, counts
   of pass/fail findings, and the counts reconciliation (maps vs profiles,
   epics vs usecases, tasks vs usecases).
2. **Per-domain sections** — for each domain: its verdict, then its findings.
3. **Findings** — each finding with `id`, `condition`, `message`, `severity`,
   `weight`, `mandatory`, `evidence`, and its tag (`defect` or `gap`).
4. **Gap summary** — the findings tagged `gap` (unresolved capabilities,
   missing task contracts, uncovered work), the hand-off to the provisioning
   scenario.

## Rules

- A failed check is a `defect` (fixable in the Domain System's declaration) or
  a `gap` (something the provisioning scenario must address). The tag comes
  from the finding itself — do not reclassify.
- Every verdict must carry its evidence in the report. No finding appears
  without the row, field, or value it rests on.
- Do not fix what the report describes. Name no specific repository or Domain
  System.

## Output

`report` — the full rendered report text.
