# Use-case 4d-conclusion — Budget Fit — conclusion

**Depends on**: `4c-enrich-conclusion`

**Script**: `budget-fit` (domain=conclusion) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: conclusion's stage='enrich' draft, word-count ranges from calculation/generation/conclusion.yaml

**Action**: Verify word count is within budget. Trim or expand as needed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
