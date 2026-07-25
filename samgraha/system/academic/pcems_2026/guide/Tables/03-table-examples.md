# Table Examples

> *Source: PCEMS 2026 Sample Papers — Annotated Excerpts*

## Purpose

This document presents annotated examples of effective and ineffective table usage from PCEMS 2026 sample papers, with analysis tied to the table standards.

## Good Patterns

### Example 1: Performance Comparison Table

**Source**: Credit Card Fraud Detection Using Machine Learning Techniques

> Table I. Performance of ML models with test size 20%
>
> | Approach | Test size | Accuracy | Recall | F1-score | Precision |
> |----------|-----------|----------|--------|----------|-----------|
> | Naive bayes | 20% | 99.30 | 0.68 | 0.25 | 0.15 |
> | Logistic regression | 20% | 99.90 | 0.73 | 0.72 | 0.70 |
> | Random forest | 20% | 99.95 | 0.74 | 0.84 | 0.97 |
> | Decision trees(E) | 20% | 99.91 | 0.76 | 0.73 | 0.71 |
> | Decision trees(GI) | 20% | 99.92 | 0.77 | 0.76 | 0.76 |
> | SVM(linear) | 20% | 99.85 | 0.64 | 0.46 | 0.36 |

**Why this works**:
- Clear header row with metric names
- All methods listed for direct comparison
- Consistent decimal places within each column
- Test size specified for context
- Caption describes what the table shows

### Example 2: Configuration / Parameters Table

**Source**: IoT Based Smart Food Grain Warehouse

> Table I. Normal Range of the Parameters of Food Grains
>
> | Parameters | Food Grains | Temperature (C) | Relative Humidity (%) | CO2 levels (ppm) |
> |------------|-------------|-----------------|----------------------|------------------|
> | Wheat | 15-37 | 20-45 | 400-500 |
> | Rice | 22-32 | 50-70 | 400-550 |

**Why this works**:
- Groups related parameters (grain type, safe ranges)
- Units specified in headers
- Clear, concise labels
- Practical reference value

### Example 3: Results Across Conditions Table

**Source**: Credit Card Fraud Detection Using Machine Learning Techniques

> Table II. Performance of ML models with test size 80%
>
> | Approach | Test size | Accuracy | Recall | F1-score | Precision |
> |----------|-----------|----------|--------|----------|-----------|
> | Naive bayes | 80% | 99.43 | 0.65 | 0.27 | 0.17 |
> | Logistic regression | 80% | 99.89 | 0.71 | 0.69 | 0.67 |
> | Random forest | 80% | 99.93 | 0.67 | 0.77 | 0.90 |

**Why this works**:
- Enables comparison across test sizes (when read alongside Table I)
- Same structure as Table I for consistency
- Clear caption distinguishing it from Table I

## Anti-Patterns

### Anti-Pattern 1: Table as Image

**Issue**: A screenshot or image of a table instead of a Word table.

**Why it fails**:
- Not editable in Word
- Not accessible (screen readers cannot read)
- Violates PCEMS template requirement
- Often low resolution

**Fix**: Recreate the table using Word table tools.

### Anti-Pattern 2: Missing Units

**Issue**: Numerical values without units in headers.

**Why it fails**:
- Values are meaningless without context
- Reader cannot interpret the data
- Example: "Accuracy: 99.95" — is this a percentage, a ratio, or a raw count?

**Fix**: Add units in parentheses: "Accuracy (%)"

### Anti-Pattern 3: Inconsistent Decimal Places

**Issue**: Some values shown as 99.95, others as 99.9, others as 100.

**Why it fails**:
- Makes comparison difficult
- Appears unprofessional
- Suggests the data was not carefully prepared

**Fix**: Use consistent decimal places within each column (typically 2 decimal places for percentages).

### Anti-Pattern 4: Table Without Caption

**Issue**: A table appears without a descriptive caption.

**Why it fails**:
- Reader does not know what the table shows
- Violates template requirement
- Cannot be referenced properly in text

**Fix**: Add a caption above the table: "Table I. [Description]"

## Comparison: Good vs. Bad

### Good Table Introduction
> "Table I presents the performance comparison of the proposed method with existing approaches. The proposed method achieves the highest accuracy of 99.95%."

- Table is referenced before it appears
- Context is provided
- Key finding is highlighted

### Bad Table Introduction
> "[Table I placed here without text reference]"

- No context provided
- Reader does not know why the table exists
- Violates template requirements

## Revision Checklist

- [ ] Every table is created using Word table tools
- [ ] Every table is referenced in the text before it appears
- [ ] Every table has a clear caption
- [ ] All headers include units where applicable
- [ ] Decimal places are consistent within each column
- [ ] No empty cells without explanation
- [ ] Table numbering is sequential throughout the paper
- [ ] Best results are highlighted (bold)
- [ ] Tables are legible (minimum 8pt font)
- [ ] Tables are placed inline, not floating
