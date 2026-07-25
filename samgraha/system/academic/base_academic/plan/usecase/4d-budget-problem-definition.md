# Use-case 4d-problem-definition — Section Budget Fit — problem-definition

**Depends on**: `section-supplementary-content-problem-definition` (4c)

**Script**: `check-word-budget` (det, domain=problem-definition) -> `fit-to-budget` (prompt, conditional — only if out of range) -> `persist-section-draft` (stage=budget-fit)

**Inputs**: `problem-definition`'s stage='enrich' draft, `calculation/deterministic/problem-definition.yaml`'s word_count_in_range config

**Action**: Fit `problem-definition` into its configured min/max word range. In-range drafts pass through unchanged (still get a stage='budget-fit' row); out-of-range drafts get trimmed or expanded toward the target.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='problem-definition') AND stage='budget-fit'` >= 1

**Verify script**: `script/verify/uc4d_budget_problem_definition.py --paper-id <id>`

**Rule**: Runs after this domain's own 4c. Does NOT check the whole-paper total — see section-budget-fit-total.
