# Use-case 4d-introduction — Budget Fit — introduction

**Depends on**: `4c-enrich-introduction`

**Script**: `budget-fit` (domain=introduction) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: introduction's stage='enrich' draft, word-count ranges from calculation/generation/introduction.yaml

**Action**: Verify word count is within budget. Trim or expand as needed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_introduction.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
