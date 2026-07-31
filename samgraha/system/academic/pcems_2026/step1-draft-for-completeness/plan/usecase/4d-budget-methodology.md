# Use-case 4d-methodology — Budget Fit — methodology

**Depends on**: `4c-enrich-methodology`

**Script**: `budget-fit` (domain=methodology) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: methodology's stage='enrich' draft, word-count ranges from calculation/generation/methodology.yaml

**Action**: Verify word count is within budget. Trim or expand as needed.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='methodology') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_methodology.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
