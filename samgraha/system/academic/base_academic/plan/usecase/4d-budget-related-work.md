# Use-case 4d-related-work — Section Budget Fit — related-work

**Depends on**: `section-supplementary-content-related-work` (4c)

**Script**: `check-word-budget` (det, domain=related-work) -> `fit-to-budget` (prompt, conditional — only if out of range) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: `related-work`'s stage='enrich' draft, `calculation/deterministic/related-work.yaml`'s word_count_in_range config

**Action**: Fit `related-work` into its configured min/max word range. In-range drafts pass through unchanged (still get a stage='budget-fit' row); out-of-range drafts get trimmed or expanded toward the target.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='related-work') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_related_work.py --paper-id <id>`

**Rule**: Runs after this domain's own 4c. Does NOT check the whole-paper total — see section-budget-fit-total.
