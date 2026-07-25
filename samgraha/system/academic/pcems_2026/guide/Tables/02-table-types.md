# Table Types

> *Source: Sample Paper Analysis + PCEMS Publication Philosophy*

## Purpose

This document describes the table types commonly used in PCEMS papers, their appropriate use cases, and construction guidelines.

## Table Type Catalog

### 1. Performance Comparison Table

**Use when**: Comparing multiple methods across multiple metrics.

**Construction guidelines**:
- Rows: Methods (proposed method first, then baselines)
- Columns: Metrics (accuracy, precision, recall, F1-score, etc.)
- Proposed method highlighted (bold or first row)
- Consistent decimal places
- Best result in bold

**Example from sample papers**:
> Table I in Credit Card Fraud Detection — compares Naive Bayes, Logistic Regression, Random Forest, Decision Trees, and SVM across accuracy, recall, F1-score, and precision.

### 2. Dataset Description Table

**Use when**: Describing the dataset used for experiments.

**Construction guidelines**:
- Rows: Dataset characteristics (source, size, features, class distribution)
- Columns: Characteristic name and value
- Include relevant statistics (mean, std, min, max) for numerical features

**Example from sample papers**:
> "Dataset summary: The dataset taken is from Kaggle, which has two days of transactions of European Credit card holders. The dataset consists of 2,84,807 transactions with only 492 fraud transactions."

### 3. Configuration / Parameters Table

**Use when**: Listing experimental parameters, hardware specifications, or software versions.

**Construction guidelines**:
- Rows: Parameters
- Columns: Parameter name and value
- Group related parameters (hardware, software, hyperparameters)

### 4. Results Across Conditions Table

**Use when**: Showing how a method performs under different conditions.

**Construction guidelines**:
- Rows: Conditions (test sizes, noise levels, dataset variants)
- Columns: Metrics
- Highlight the best-performing condition

### 5. Qualitative Comparison Table

**Use when**: Comparing methods on non-numerical criteria.

**Construction guidelines**:
- Rows: Methods
- Columns: Criteria (complexity, scalability, interpretability)
- Values: Checkmarks, ratings, or descriptive text

### 6. Feature Description Table

**Use when**: Describing features used in a machine learning model.

**Construction guidelines**:
- Rows: Features
- Columns: Feature name, type, description, range
- Group by feature category if applicable

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Table as image | Not editable, not accessible, violates template |
| Inconsistent decimal places | Makes comparison difficult |
| Missing units | Values are meaningless without context |
| Too many columns | Hard to read; split into multiple tables |
| Empty cells without explanation | Reader cannot interpret missing data |
| Table before first reference | Violates placement rule |
| Table without caption | Incomplete; violates template |

## Revision Checklist

- [ ] Table type matches the information being presented
- [ ] Table is constructed according to type-specific guidelines
- [ ] Table is created using Word table tools
- [ ] Table is referenced in text before placement
- [ ] Table is placed immediately after first reference
- [ ] Caption is clear and descriptive
- [ ] Headers are bold and descriptive
- [ ] Units are specified
- [ ] Decimal places are consistent
- [ ] No empty cells without explanation
