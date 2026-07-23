# 08. Results

**Domain:** `results`
**Audit Target:** The generated results section.

## Standard Definition

The measured outcomes of the experiments defined in `experimental-setup`,
reported with standard metrics and statistical rigor — not raw accuracy
numbers alone. Every claim of improvement must be backed by a statistical
significance test, not an unqualified percentage-point comparison.

### Expected Evidence (Deterministic)

1. **Standard metrics reported**, matching the problem type declared in
   `problem-definition` (accuracy/precision/recall/F1 for classification,
   RMSE/MAE for regression, latency/memory where performance is claimed).
2. **At least one statistical significance test is named** (paired t-test,
   Wilcoxon signed-rank, McNemar's, confidence intervals, or equivalent) —
   presence of test-name + a p-value or CI figure is mechanically
   checkable.
3. **Every number reported here that also appears in the abstract matches
   exactly** — a direct cross-reference check against the `abstract`
   domain's output.
4. **Tables/figures are captioned and referenced from the prose**, not
   inserted with no in-text pointer.

### Semantic Judgment Criteria

- Do the interpreted claims match what the numbers actually show, or
  overstate the result (e.g., "significantly better" attached to a
  marginal, non-significant delta)?
- Is the ablation study (if the methodology has multiple components)
  actually isolating each component's contribution, or conflating several
  changes into one ablation row?
- Are failure cases and edge cases acknowledged, or does the section only
  report favorable configurations?
