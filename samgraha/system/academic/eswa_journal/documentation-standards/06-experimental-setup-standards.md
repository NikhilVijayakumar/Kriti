# Experimental Setup Standard

> *Deterministic rules for this domain: `audit/deterministic/document/06-experimental-setup.yaml`*

## Table of Contents
- [Purpose](#purpose)
- [Reproducibility Checklist](#reproducibility-checklist)
- [Baselines](#baselines)
- [Metrics & Statistical Tests](#metrics--statistical-tests)

## Purpose
Ensure total reproducibility of the proposed system.

## Reproducibility Checklist
**Template:**
```markdown
[Hardware specs: CPU/GPU/RAM]
[Software versions]
[Dataset source and preprocessing]
[Parameter settings and random seed]
```

## Baselines
**Template:**
```markdown
The proposed method is compared against the following baselines:
1. [Classical Baseline]
2. [Recent SOTA 1 (2023-2025)]
3. [Recent SOTA 2 (2023-2025)]
4. [Ablation Baseline]
```
**Audit Rule:** Minimum of 3 baselines required (at least 1 classical, 2 recent).

## Metrics & Statistical Tests
**Template:**
```markdown
Performance is evaluated using [Accuracy/Precision/Recall/F1/AUC/RMSE].
Statistical significance is verified using [Paired t-test / Wilcoxon signed-rank test] with $p < 0.05$.
```
**Audit Rule:** Must explicitly state the statistical significance test used and the p-value threshold.
