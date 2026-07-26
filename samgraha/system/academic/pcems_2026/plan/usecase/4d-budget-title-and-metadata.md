# Use-case 4d-title-and-metadata — Budget Fit — title-and-metadata

**Depends on**: `4c-enrich-title-and-metadata`

**Script**: `budget-fit` (domain=title-and-metadata) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: title-and-metadata's stage='enrich' draft, word-count ranges from calculation/generation/title-and-metadata.yaml

**Action**: Verify word count is within budget. Trim or expand as needed to fit target range.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='title-and-metadata') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_title_and_metadata.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
