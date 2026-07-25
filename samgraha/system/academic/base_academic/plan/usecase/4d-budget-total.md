# Use-case 4d-total — Section Budget Fit — whole-paper total (fan-in)

**Depends on**: all 12 `section-budget-fit-{domain}` usecases

**Script**: No script of its own — reads the sum of every domain's stage='budget-fit' word count against `calculation/summary/paper-budget.yaml`

**Inputs**: Every domain's stage='budget-fit' narrative + `calculation/summary/paper-budget.yaml`

**Action**: Check that 12 independently-in-range sections still sum to a whole-paper total within the venue's page/word limit.

**Completion criteria** (checked by verify script):
- `SUM(word_count)` across all stage='budget-fit' narratives is within `calculation/summary/paper-budget.yaml`'s `total_word_count` range

**Verify script**: `script/verify/uc4d_budget_total.py --paper-id <id>`

**Rule**: Fan-in, whole-paper concern — gates deterministic-audit-* the same way every other domain-level 4d usecase does.
