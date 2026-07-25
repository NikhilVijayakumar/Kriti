# Use-case 4d-limitations — Section Budget Fit — limitations

**Depends on**: `section-supplementary-content-limitations` (4c)

**Script**: `check-word-budget` (det, domain=limitations) -> `fit-to-budget` (prompt, conditional — only if out of range) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: `limitations`'s stage='enrich' draft, `calculation/deterministic/limitations.yaml`'s word_count_in_range config

**Action**: Fit `limitations` into its configured min/max word range. In-range drafts pass through unchanged (still get a stage='budget-fit' row); out-of-range drafts get trimmed or expanded toward the target.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='limitations') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_limitations.py --paper-id <id>`

**Rule**: Runs after this domain's own 4c. Does NOT check the whole-paper total — see section-budget-fit-total.
