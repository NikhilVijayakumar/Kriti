# 07. Experimental Setup

**Domain:** `experimental-setup`
**Audit Target:** The generated experimental-setup section.

## Standard Definition

Everything a reader would need to reproduce the paper's experiments:
hardware/software environment, dataset provenance and preprocessing,
parameter settings, and the baselines the proposed approach is compared
against. This section is the reproducibility floor — its completeness is
one of the few domains where a deterministic check can carry most of the
weight, since "is a hardware spec present" is a presence check, not a
judgment call.

### Expected Evidence (Deterministic)

1. **Hardware specification present** (CPU/GPU/RAM or equivalent, as
   relevant to the approach).
2. **Software versions listed** for any library/framework the methodology
   depends on.
3. **Dataset source and preprocessing steps described**, not just a
   dataset name with no provenance.
4. **Random seed mentioned**, if the methodology is stochastic/ML-based.
5. **Baseline count meets the concrete system's configured minimum**
   (a classical baseline + recent comparable methods; exact count and
   recency window are venue-specific, set by the concrete system).
6. **Ablation baseline present**, if the methodology has more than one
   component.

### Semantic Judgment Criteria

- Are the chosen baselines actually comparable (same problem, same input
  assumptions), or superficially similar methods chosen because they're
  easy to beat?
- Is the preprocessing pipeline described completely enough that a
  difference in results couldn't be explained by an undocumented
  preprocessing step?
- Are parameter settings justified (why this window size, this learning
  rate) or just listed with no rationale?
