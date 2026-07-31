# Use-case 4d-findings — Budget Fit — findings

**Depends on**: `4c-enrich-findings`

**Script**: `budget-fit` (domain=findings) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: findings's stage='enrich' draft, word-count ranges from calculation/generation/findings.yaml

**Action**: Verify word count is within budget. Trim or expand as needed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='findings') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_findings.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
