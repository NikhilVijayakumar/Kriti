# Findings Writing Guide

> *Source: PCEMS 2026 Template + Documentation-Standards/04-findings-standards.md + Sample Paper Analysis*

## Purpose

The Findings section presents the experimental results with strict emphasis on correct table and media formatting. It answers: "What was observed, and what does it mean?"

## Structure

A PCEMS Findings section follows an evidence-presentation pattern: experimental setup → results → analysis.

### Required Elements

1. **Experimental Setup** (1 paragraph): Dataset description, evaluation metrics, experimental conditions
2. **Results Presentation** (2-4 subsections): Tables and figures with accompanying text
3. **Analysis** (1-2 paragraphs): Interpretation of results

### Template

```markdown
[Describe the experimental setup: dataset, metrics, conditions]
[Present results using tables and figures]
[Analyze and interpret the results]
```

## Content Requirements

### Experimental Setup

Before presenting results, describe:
- **Dataset**: Source, size, features, train/test split
- **Evaluation metrics**: Accuracy, precision, recall, F1-score, etc.
- **Experimental conditions**: Hardware, software, parameters
- **Comparison methods**: Baseline methods used for comparison

**Example pattern**:
> "The proposed method was evaluated on the [Dataset Name] dataset, which contains [N] samples with [M] features. The dataset was split into 80% training and 20% testing. The following metrics were used: accuracy, precision, recall, and F1-score."

### Results Presentation

Present results using tables and figures. Every table and figure must:

1. **Be referenced in the text** before it appears
2. **Have a clear caption** describing what it shows
3. **Be placed immediately after its first reference**
4. **Be created using Microsoft Word table tools** (not images)

**Text pattern for introducing a table**:
> "Table I presents the performance comparison of the proposed method with existing approaches. The proposed method achieves the highest accuracy of 99.95%."

**Text pattern for introducing a figure**:
> "Fig. 2 illustrates the performance of each method across different test sizes. Random Forest consistently outperforms other methods."

### Analysis

After presenting results, analyze:
- What the results mean
- Why certain methods perform better
- What the key factors are
- How results compare to existing work

**Example pattern**:
> "The results demonstrate that [method] achieves [metric] of [value], which is [X]% higher than the best existing approach. This improvement is attributed to [reason]. The key factor contributing to this performance is [analysis]."

## Media Placement Rules

These rules are mandatory per PCEMS 2026 guidelines:

- **All images** (illustrations, charts, photos, diagrams) must appear immediately after their first reference in the text
- **Tables** must be created using Microsoft Word table functions and placed immediately after the first reference
- **Do not** collect figures at the end of the manuscript
- **Do not** insert tables as images
- **Do not** place media before their first textual reference

## Typography

- **Section heading**: Heading 1 (Arial, 12pt, Bold)
- **Body text**: Arial, 11pt
- **Table text**: Arial, 8-10pt (legible but compact)
- **Figure captions**: Below the figure, Arial
- **Table captions**: Above the table, Arial

## Table Formatting

### Requirements

- Created using Microsoft Word table tools
- Placed inline with text (not floating)
- Clear header row with labels
- Consistent decimal places for numerical data
- Units specified in column headers

### Example

```
Table I. Performance of ML Models (Test Size 20%)

Approach       Accuracy   Recall   F1-Score   Precision
Naive Bayes     99.30%    0.68     0.25       0.15
Logistic Reg.   99.90%    0.73     0.72       0.70
Random Forest   99.95%    0.74     0.84       0.97
SVM (linear)    99.85%    0.64     0.46       0.36
```

## Length Guidelines

Based on sample paper analysis:

| Metric | Range | Target |
|--------|-------|--------|
| Word count | 600-1,200 words | 800-1,000 words |
| Tables | 1-4 | 2-3 |
| Figures | 1-4 | 2-3 |

## Writing Strategy

### Do

- Present results objectively (no interpretation in the results subsection)
- Reference every table and figure before it appears
- Place media immediately after first reference
- Use tables for precise numerical comparison
- Use figures for trends and patterns
- Include units in all measurements
- Round numbers consistently

### Do Not

- Interpret results before presenting them
- Place figures at the end of the paper
- Use screenshots of tables (use Word table tools)
- Omit units from measurements
- Present raw data without analysis
- Mix results and discussion in the same subsection

## Common Patterns from Sample Papers

1. **Tables per paper**: Average of 2.5 tables
2. **Figures per paper**: Average of 2.8 figures
3. **Results structure**: Most papers present results by experiment or by metric
4. **Comparison tables**: 9 of 11 papers include a comparison with existing methods
5. **Average length**: ~900 words

## Revision Checklist

- [ ] Experimental setup is described (dataset, metrics, conditions)
- [ ] Every table is referenced in the text before it appears
- [ ] Every figure is referenced in the text before it appears
- [ ] All tables are created using Word table tools
- [ ] All media is placed immediately after first reference
- [ ] Units are specified for all measurements
- [ ] Decimal places are consistent within each table
- [ ] Results are presented objectively (interpretation in Discussion)
- [ ] Comparison with existing methods is included
- [ ] Length is within 600-1,200 words
