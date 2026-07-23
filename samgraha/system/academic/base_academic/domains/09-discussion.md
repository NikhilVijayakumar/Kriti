# 09. Discussion

**Domain:** `discussion`
**Audit Target:** The generated discussion section.

## Standard Definition

Interpretation of the results, not a restatement of them: why the method
performed as it did, where it fails, threats to the validity of the
conclusions drawn, and — where relevant — the practical/industrial impact
of deploying this approach. This is the section that most separates a
results *table* from a results *argument*.

### Expected Evidence (Deterministic)

1. **Threats-to-validity subsection present** (or equivalent labeled
   content), covering at minimum internal and external validity.
2. **Section does not merely repeat results-section sentences** —
   mechanically checkable as a similarity/overlap floor against the
   `results` domain's text (high overlap flags as a structural weakness:
   discussion isn't interpreting, just restating).

### Semantic Judgment Criteria

- Does the interpretation explain *why* the method outperformed (or
  underperformed) baselines, grounded in the methodology's actual design,
  rather than a generic "our method is more robust" claim?
- Are failure scenarios and edge cases discussed honestly, including ones
  unfavorable to the proposed approach?
- If industrial/practical impact is claimed, is deployment feasibility
  actually addressed (cost, integration effort, operational constraints),
  not just asserted as a benefit?
- Is dataset bias or other construct-validity concerns acknowledged where
  the experimental setup's data source could plausibly introduce one?
