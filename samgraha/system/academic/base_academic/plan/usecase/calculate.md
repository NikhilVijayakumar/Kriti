# Use-case 6 — Calculate

**Script**: `calculate.py` (deterministic, single step)

**Inputs**:
- `calculation/summary/final_score.yaml` — two-bucket weights (semantic_document + deterministic_document)
- `calculation/summary/score_bands.yaml` — score → band lookup
- `calculation/summary/trend.yaml` — trend thresholds
- Latest `academic_semantic_runs` + `academic_semantic_dimension_scores` per (paper, domain)
- Latest `academic_deterministic_findings` per (paper, domain)

**Action**: Two-bucket scoring — `final_score = w_sem * semantic_document + w_det * deterministic_document`.
Runs validation pre-checks, writes one `academic_score_history` row per domain + one whole-paper row. Append-only.

**Completion criteria**:
- One new `academic_score_history` row per domain + one whole-paper row
- `trend_delta` populated against the prior snapshot
- `score_band` set from `score_bands.yaml` lookup

**Rule**: Runs after both audits have scored every domain. Re-runnable.
