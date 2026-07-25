# Strengthening Your Paper

> *Source: PCEMS 2026 Template + Sample Paper Analysis + Conference Guidelines*

## Purpose

This document provides concrete actions for strengthening papers at each stage of revision. Rather than abstract advice, each section targets specific weaknesses with measurable improvements.

## Pre-Revision Assessment

Before revising, identify the paper's weakest section. Rate each dimension:

| Dimension | Weak (1) | Adequate (2) | Strong (3) |
|-----------|----------|---------------|------------|
| Contribution clarity | Unclear what is new | Stated but not compelling | Clear, specific, compelling |
| Methodology detail | Missing critical steps | Most steps present | Fully reproducible |
| Results strength | No comparison | Basic comparison | Comprehensive comparison with statistics |
| Writing quality | Many clarity issues | Occasional issues | Clear and precise |
| Literature coverage | Missing key works | Adequate coverage | Comprehensive and current |
| Formatting compliance | Multiple violations | Minor issues | Fully compliant |

Total score below 10: Major revision needed. Score 10-14: Targeted revision. Score 15-18: Minor polish.

## Strengthening the Abstract

The abstract is the most-read and most-consequential part of the paper.

### Structure (150-250 words)

1. **Context** (1-2 sentences): Why does this problem matter?
2. **Gap** (1 sentence): What is missing in current approaches?
3. **Contribution** (1-2 sentences): What does this paper propose?
4. **Method** (1-2 sentences): How does it work?
5. **Results** (1-2 sentences): What quantitative outcomes were achieved?
6. **Impact** (1 sentence): Why do these results matter?

### Common Abstract Weaknesses

| Weak | Strong |
|------|--------|
| "This paper presents a new method" | "This paper proposes an adaptive sampling technique that..." |
| "Experiments show good results" | "Experiments on 284,807 transactions show 99.95% accuracy, improving the baseline by 0.05%" |
| "The proposed system is efficient" | "The proposed system reduces inference latency by 40% compared to the state-of-the-art" |
| No keywords | Keywords: fraud detection, machine learning, class imbalance, random forest |

## Strengthening the Introduction

The introduction must convince reviewers that the paper is worth reading.

### The Problem-Solution-Gap Framework

1. **Problem significance** (1 paragraph): Why does this problem matter? Use data.
2. **Existing approaches** (1 paragraph): What has been tried?
3. **Limitations** (1 paragraph): What is missing in current approaches?
4. **Proposed solution** (1 paragraph): What does this paper contribute?
5. **Paper organization** (optional, 1 sentence): Brief outline of remaining sections.

### Introduction Checklist

- [ ] Problem is stated within the first 3 sentences
- [ ] Significance is supported by data or citations
- [ ] At least 3 existing approaches are mentioned
- [ ] Limitations of existing work are specific, not vague
- [ ] Proposed solution directly addresses the identified limitations
- [ ] Contribution is stated explicitly using "this paper proposes" or "we present"

## Strengthening the Methodology

The methodology must be detailed enough for replication.

### Required Details

| Element | Minimum Detail |
|---------|---------------|
| Dataset | Source, size, attributes, preprocessing |
| Model/Method | Architecture, parameters, training procedure |
| Hardware | CPU/GPU, memory, operating system |
| Software | Framework versions, libraries used |
| Hyperparameters | Learning rate, epochs, batch size, optimization |
| Evaluation | Metrics, cross-validation strategy, statistical tests |

### Methodology Writing Pattern

For each component of the method:

1. **What**: Describe the component
2. **Why**: Justify the design choice
3. **How**: Explain the implementation
4. **Parameters**: Specify all configurable values

## Strengthening Results

Results must present data, not claims.

### Results Section Structure

1. **Dataset summary**: Size, characteristics, train/test split
2. **Experimental setup**: Configuration, baselines selected
3. **Main results**: Primary comparison table/figure
4. **Analysis**: Interpretation of why the proposed method performs differently
5. **Ablation** (if applicable): Contribution of individual components

### Results Best Practices

- Present results in tables with clear headers
- Include multiple metrics (accuracy, precision, recall, F1)
- Compare with at least 3 baselines when possible
- Report standard deviations or confidence intervals
- Use figures for trends, tables for precise values
- Reference every table and figure in the text

## Strengthening the Conclusion

The conclusion summarizes without introducing new information.

### Conclusion Structure (200-300 words)

1. **Restate contribution** (1 sentence): What was achieved?
2. **Key results** (2-3 sentences): What were the main quantitative outcomes?
3. **Significance** (1-2 sentences): Why do these results matter?
4. **Limitations** (1 sentence): What are the acknowledged limitations?
5. **Future work** (1-2 sentences): What are the next logical steps?

### Conclusion Anti-Patterns

- Do not introduce new results or data
- Do not repeat the abstract verbatim
- Do not make claims unsupported by the results
- Do not end with vague future work ("we plan to improve the system")

## Strengthening References

### Reference Quality Checklist

- [ ] 15-30 references total (based on sample paper analysis)
- [ ] At least 5 references from the last 3 years
- [ ] At least 2 foundational/seminal works cited
- [ ] All in-text citations appear in the reference list
- [ ] All reference list entries are cited in the text
- [ ] Consistent citation format throughout
- [ ] No broken citation numbers (e.g., jumping from [5] to [8])

## Revision Sequence

Optimal revision order:

1. **Abstract**: Hardest to write, most impactful. Revise first.
2. **Introduction**: Must align with the revised abstract.
3. **Methodology**: Must match what was actually done.
4. **Results**: Must support the claims in abstract and introduction.
5. **Discussion/Conclusion**: Must synthesize everything.
6. **References**: Fill gaps identified during revision.
7. **Figures and Tables**: Ensure all are referenced, placed correctly, and legible.
8. **Formatting**: Final compliance check against PCEMS template.
