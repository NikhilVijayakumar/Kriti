# Content Mistakes

> *Source: PCEMS 2026 Sample Papers + Reviewer Expectations*

## Purpose

Content mistakes weaken the paper's technical contribution. This document identifies patterns that reduce paper quality and provides corrections based on accepted sample paper analysis.

## Abstract Mistakes

### Mistake: Abstract Too Long
**Wrong**: 400+ word abstract that reads like a miniature paper
**Correct**: 150-250 words covering problem, method, results, contribution

### Mistake: Abstract Without Quantitative Results
**Wrong**: "The proposed method shows good performance"
**Correct**: "The proposed method achieves 99.95% accuracy, improving the baseline by 0.05%"

### Mistake: Citations in Abstract
**Wrong**: "As shown in [1], previous methods have limitations"
**Correct**: State the limitation directly without citation in abstract

## Introduction Mistakes

### Mistake: No Clear Contribution Statement
**Wrong**: Introduction describes the problem but never states what this paper contributes
**Correct**: Explicit statement: "This paper proposes [specific contribution]"

### Mistake: Vague Problem Statement
**Wrong**: "There are many problems in this area"
**Correct**: "Existing fraud detection methods fail when the class imbalance ratio exceeds 100:1"

### Mistake: Too Broad Opening
**Wrong**: "In today's world, technology is advancing rapidly"
**Correct**: Open with specific context relevant to the problem

## Methodology Mistakes

### Mistake: Missing Implementation Details
**Wrong**: "The model was trained using standard parameters"
**Correct**: "The model was trained for 100 epochs with batch size 32, learning rate 0.001 (Adam optimizer)"

### Mistake: No Dataset Description
**Wrong**: "We used a dataset for our experiments"
**Correct**: "The dataset contains 284,807 transactions with 492 fraud cases, sourced from Kaggle"

### Mistake: Missing Hardware Specification
**Wrong**: "Experiments were conducted on a computer"
**Correct**: "Experiments were performed on Intel i7-12700H, 16GB RAM, NVIDIA RTX 3060 GPU"

### Mistake: No Justification for Design Choices
**Wrong**: "We chose random forest for classification"
**Correct**: "Random forest was selected for its robustness to class imbalance and ability to handle high-dimensional feature spaces"

## Results Mistakes

### Mistake: No Baseline Comparison
**Wrong**: Presenting results without comparing to existing methods
**Correct**: Compare with at least 2-3 established baselines

### Mistake: Claiming "Best" Without Evidence
**Wrong**: "Our method achieves the best results"
**Correct**: "Our method achieves 99.95% accuracy, outperforming the next best method (SVM at 99.85%) by 0.10%"

### Mistake: Missing Statistical Significance
**Wrong**: Reporting single-run results
**Correct**: Report mean and standard deviation over multiple runs; test statistical significance

### Mistake: No Error Analysis
**Wrong**: Only reporting overall accuracy
**Correct**: Analyze failure cases, per-class performance, confusion matrix

## Conclusion Mistakes

### Mistake: Introducing New Results
**Wrong**: Presenting new data or comparisons in the conclusion
**Correct**: Summarize existing results from the findings section

### Mistake: Repeating Abstract Verbatim
**Wrong**: Copy-pasting the abstract into the conclusion
**Correct**: Synthesize and provide broader context

### Mistake: Vague Future Work
**Wrong**: "We plan to improve the system in the future"
**Correct**: "Future work will investigate the effect of increasing the training dataset size beyond 100,000 samples"

## Literature Review Mistakes

### Mistake: Paper-by-Paper Summary
**Wrong**: "Author A did X. Author B did Y. Author C did Z."
**Correct**: Group works thematically: "Three approaches exist for [problem]: method-based [1-3], model-based [4-6], and hybrid [7-9]. None address [specific limitation]."

### Mistake: Missing Foundational Works
**Wrong**: Citing only recent papers while ignoring seminal works
**Correct**: Include at least 2-3 foundational references that established the field

### Mistake: No Gap Identification
**Wrong**: Listing what others have done without identifying what's missing
**Correct**: End the related work section by explicitly stating the gap

## Writing Quality Mistakes

### Mistake: Excessive Passive Voice
**Wrong**: "The experiment was conducted by the researchers"
**Correct**: "The researchers conducted the experiment"

### Mistake: Overly Long Sentences
**Wrong**: Single sentences exceeding 40 words with multiple clauses
**Correct**: Split into two sentences, each under 25 words

### Mistake: Inconsistent Terminology
**Wrong**: Calling the same concept "model," "approach," "method," "technique" interchangeably
**Correct**: Pick one term and use it consistently

### Mistake: Informal Language
**Wrong**: "a lot of," "basically," "really good," "thing"
**Correct**: "numerous," [delete], "excellent," "component" or "element"
