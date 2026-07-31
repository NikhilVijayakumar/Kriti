# Use-case 4d-references — Budget Fit — references

**Depends on**: `4c-enrich-references`

**Script**: `budget-fit` (domain=references) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: references's stage='enrich' draft, word-count ranges from calculation/generation/references.yaml

**Action**: Verify reference count is within budget (15-25 references). Flag if too few or too many.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='references') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_references.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
