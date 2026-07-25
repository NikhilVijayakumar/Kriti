# Table Standards

> *Source: PCEMS 2026 Template + Conference Guidelines/04-figures-and-tables.md + Sample Paper Analysis*

## Purpose

Tables organize factual information for comparison and analysis. They should support analysis rather than repeat narrative text.

## Requirements

### Creation

- Tables must be created using **Microsoft Word table tools**
- Tables must be placed **immediately after their first reference** in the text
- Tables must be **part of the document flow** (inline, not floating)
- Do not insert tables as images

### Placement

- Reference the table in the text before it appears
- Place the table immediately after the reference
- Place the table caption above the table

### Formatting

- **Caption**: Above the table, Arial, bold
- **Header row**: Bold, with clear labels
- **Body text**: Arial, 8-10pt (legible but compact)
- **Alignment**: Text left-aligned, numbers right-aligned or decimal-aligned
- **Borders**: Use borders to separate headers from body, not grid lines for every cell
- **Decimal places**: Consistent within each column
- **Units**: Specified in column headers (e.g., "Accuracy (%)", "Time (ms)")

## Table Construction

### Header Row

The header row must clearly describe what each column contains. Use:
- Descriptive labels (not abbreviations unless universally understood)
- Units in parentheses
- Consistent capitalization

**Example**:
```
| Method      | Accuracy (%) | Precision | Recall | F1-Score |
|-------------|-------------|-----------|--------|----------|
```

### Data Rows

- One row per data point
- Consistent decimal places within each column
- No empty cells (use "—" if data is not available)
- Sort rows logically (by performance, alphabetical, or by experimental condition)

### Footnotes

Use footnotes (a, b, c) to add notes that apply to specific cells or rows:

```
| Method    | Accuracy |
|-----------|----------|
| Method A  | 95.2%    |
| Method B  | 94.8%<sup>a</sup> |

<sup>a</sup> Method B uses a reduced feature set.
```

## Table Types

### Comparison Table

Used for: Comparing multiple methods across multiple metrics.

**Structure**: Methods as rows, metrics as columns.

**Example**:
```
Table I. Performance Comparison

Method       Accuracy   Precision   Recall   F1-Score
Random F.    99.95%     0.97        0.74     0.84
SVM          99.85%     0.36        0.64     0.46
Log. Reg.    99.90%     0.70        0.73     0.72
```

### Configuration Table

Used for: Describing experimental parameters, hardware specifications, or dataset characteristics.

**Structure**: Parameter as rows, values as columns.

**Example**:
```
Table II. Experimental Configuration

Parameter        Value
Dataset          Credit Card Fraud (Kaggle)
Samples          284,807
Features         31 (PCA-transformed)
Train/Test Split 80/20
```

### Results Table

Used for: Presenting detailed results for a single method across conditions.

**Structure**: Conditions as rows, metrics as columns.

**Example**:
```
Table III. Results Across Test Sizes

Test Size   Accuracy   Recall   F1-Score
20%         99.95%     0.74     0.84
40%         99.95%     0.74     0.84
60%         99.95%     0.74     0.84
80%         99.95%     0.74     0.84
```

## LaTeX Formatting

```latex
\begin{table}[htbp]
    \centering
    \caption{Performance Comparison}
    \label{tab:performance}
    \begin{tabular}{lcccc}
        \hline
        Method & Accuracy & Precision & Recall & F1-Score \\
        \hline
        Random Forest & 99.95\% & 0.97 & 0.74 & 0.84 \\
        SVM           & 99.85\% & 0.36 & 0.64 & 0.46 \\
        \hline
    \end{tabular}
\end{table}

As shown in Table~\ref{tab:performance}, Random Forest achieves...
```

## Revision Checklist

- [ ] Every table is created using Word table tools
- [ ] Every table is referenced in the text before it appears
- [ ] Every table is placed immediately after its first reference
- [ ] Table caption is above the table, bold
- [ ] Header row has clear, descriptive labels
- [ ] Units are specified in column headers
- [ ] Decimal places are consistent within each column
- [ ] No empty cells (use "—" if data unavailable)
- [ ] Table numbering is sequential throughout the paper
- [ ] Table text is legible (minimum 8pt)
