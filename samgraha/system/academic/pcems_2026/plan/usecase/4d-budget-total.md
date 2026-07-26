# Use-case 4d-total — Section Budget Fit — whole-paper total (fan-in)

**Depends on**: all 6 `section-budget-fit-{domain}` usecases
(title-and-metadata, introduction, methodology, findings, conclusion,
references)

**Script**: No script of its own — reads the sum of every domain's
stage='budget-fit' word count against
`calculation/report/summary/paper-budget.yaml`, via
`academic_schema._uc_section_budget_fit_total` (shared, reused from
base_academic — this predicate is domain-count-agnostic, it sums whatever
domains exist for the paper's registered system).

**Inputs**: Every domain's stage='budget-fit' narrative +
`calculation/report/summary/paper-budget.yaml`

**Action**: Check that 6 independently-in-range sections still sum to a
whole-paper total within PCEMS 2026's word limit (2,400-4,800 per
`guide/Writing Guide/01-writing-principles.md`'s "Total paper length" row).

**Completion criteria** (checked by verify script):
- `SUM(word_count)` across all stage='budget-fit' narratives is within
  `calculation/report/summary/paper-budget.yaml`'s `total_word_count` range

**Verify script**: `script/verify/uc4d_budget_total.py --paper-id <id>`

**Rule**: Fan-in, whole-paper concern — gates deterministic-audit-* the
same way every other domain-level 4d usecase does. A section individually
inside its own `calculation/generation/{domain}.yaml` range can still fail
here if the whole-paper sum falls outside 2,400-4,800 — this is the actual
enforcement point for the "sections have per-section tolerance, but the
whole paper must hit budget" policy; per-section `word_count_in_range`
checks (severity varies) are advisory relative to this fan-in gate.
