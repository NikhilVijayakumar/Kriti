# Rejection Patterns

> *Source: PCEMS 2026 Template + Sample Paper Analysis + Conference Guidelines*

## Purpose

Papers are rejected for predictable reasons. Identifying these patterns before submission prevents avoidable desk rejections and weak reviews. This document catalogs the most common rejection triggers observed in conference review processes.

## Desk Rejection Triggers

These issues cause papers to be rejected without full review:

### Formatting Violations
- Wrong document format (PDF instead of Word, or LaTeX)
- Multi-column layout instead of required single-column
- Incorrect font families or sizes
- Missing IEEE copyright notice
- Page limit exceeded

### Structural Missing
- No abstract, or abstract exceeds 250 words
- No keywords
- Missing sections prescribed by template
- No references, or fewer than 10 references

### Plagiarism and Originality
- Excessive similarity to previously published work
- Self-plagiarism without citation
- Missing acknowledgment of prior versions

## Common Review Rejection Reasons

### 1. Unclear Contribution

**Pattern**: Paper describes what was done without explaining why it matters.

**Example of weak contribution statement**:
> "This paper presents a machine learning model for fraud detection. We trained several models and compared their accuracy."

**Example of strong contribution statement**:
> "This paper addresses the limitation that existing fraud detection methods fail under class imbalance ratios exceeding 100:1. We propose an adaptive sampling technique that maintains detection accuracy across imbalance ratios from 10:1 to 1000:1, demonstrated on a dataset of 284,807 transactions."

**Prevention**: Every paper must answer: What problem? Why now? What did you contribute? Why does it work?

### 2. Insufficient Methodology

**Pattern**: Methods section describes the approach but omits critical implementation details.

**Common omissions**:
- Dataset preprocessing steps
- Model hyperparameters
- Training configuration (learning rate, epochs, optimizer)
- Hardware used for experiments
- Random seed or cross-validation strategy

**Prevention**: Include enough detail that a graduate student could reproduce the work from the methods section alone.

### 3. Weak or Missing Evaluation

**Pattern**: Results section presents numbers without context or comparison.

**Anti-patterns**:
- Reporting accuracy without baseline comparison
- Claiming "best results" without statistical testing
- Presenting results without explaining their significance
- Missing ablation study for composite methods

**Prevention**: Every result must be compared against at least one established baseline. Every claim of improvement must quantify the margin.

### 4. Poor Literature Review

**Pattern**: Related work section reads as a list of summaries rather than a critical analysis.

**Anti-patterns**:
- Summarizing papers one-by-one without synthesis
- Citing only recent papers while ignoring foundational work
- Failing to identify the gap the current paper fills
- Missing citations for key techniques used

**Prevention**: Organize related work thematically. End each theme with what remains unsolved. Connect the unsolved problems to your contribution.

### 5. Writing Quality Issues

**Patterns that signal poor quality**:
- Excessive passive voice ("it was found that," "experiments were conducted")
- Informal language ("a lot of," "basically," "very good")
- AI-generated language markers (delve, tapestry, landscape, paramount, crucial, pivotal)
- Inconsistent terminology (calling the same thing by different names)
- Run-on sentences exceeding 40 words
- Paragraphs exceeding 12 sentences

**Prevention**: Read the paper aloud. If any sentence requires re-reading for clarity, rewrite it.

### 6. Formatting and Citation Errors

**Patterns**:
- In-text citations don't match reference list entries
- Figures appear at end of paper instead of after first reference
- Tables lack captions or headers
- Inconsistent citation numbering
- References in wrong format

**Prevention**: Use a reference manager. Verify every citation resolves. Check figure placement against template requirements.

## Sample Paper Observations

Analysis of 11 accepted PCEMS 2026 sample papers reveals:

| Pattern | Frequency | Implication |
|---------|-----------|-------------|
| IEEE numbered citations | 11/11 | Use [1], [2] format |
| Roman numeral sections | 11/11 | Use I., II., III. numbering |
| Abstract < 250 words | 10/11 | Keep abstracts concise |
| 15-30 references | 9/11 | Target this range |
| Keywords after abstract | 11/11 | Always include keywords |
| Figures inline after first reference | 11/11 | Never collect figures at end |
| Results with baseline comparison | 9/11 | Always compare with baselines |

## Self-Assessment Protocol

Before submission, evaluate the paper against these questions:

1. Can a reader identify the contribution within the first page?
2. Is every claim supported by evidence?
3. Could another researcher reproduce the work from the methods section?
4. Are all figures and tables necessary and properly placed?
5. Does the abstract stand alone as a summary of the paper?
6. Are all references cited in the text present in the reference list?
7. Is the formatting compliant with all PCEMS template requirements?
8. Does the conclusion avoid introducing new information?
