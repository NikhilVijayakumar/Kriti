# Equation Formatting

> *Source: Sample Paper Analysis + PCEMS Publication Philosophy*

## Purpose

This document establishes the formatting standards for mathematical equations in PCEMS 2026 papers.

## Requirements

### Equation Numbering

- All equations must be numbered sequentially: (1), (2), (3)...
- Equation numbers appear right-aligned
- Reference equations by number in the text

### Equation Placement

- Equations appear on their own line (display equations)
- Centered within the column
- Blank line before and after for readability

### Variable Definitions

- All variables must be defined at first use
- Definitions appear in the text, not in the equation itself
- Use consistent notation throughout the paper

## Formatting Rules

### In Text

When referencing an equation:
- "As shown in Equation (1)..."
- "The Dice coefficient is defined as follows: (1)"
- "Equation (2) calculates the accuracy..."

### Variable Naming

- Use italic for scalar variables: *x*, *y*, *n*
- Use bold for vectors: **v**, **w**
- Use uppercase for matrices: **A**, **B**
- Use standard notation for common quantities:
  - *n*: sample count
  - *p*: probability
  - *N*: population size
  - *μ*: mean
  - *σ*: standard deviation
  - *θ*: parameters

### Units

- Units appear in parentheses after the equation
- Use SI units where applicable
- Define non-standard units

## Common Equation Patterns

### Classification Metrics

```
Accuracy = (TP + TN) / (TP + TN + FP + FN) ... (1)

Precision = TP / (TP + FP) ... (2)

Recall = TP / (TP + FN) ... (3)

F1-Score = 2 × (Precision × Recall) / (Precision + Recall) ... (4)
```

### Distance Metrics

```
Euclidean Distance = √(Σ(xi - yi)²) ... (1)

Dice Coefficient = 2|A ∩ B| / (|A| + |B|) ... (2)

Cosine Similarity = (A · B) / (||A|| × ||B||) ... (3)
```

### Optimization

```
Loss = -Σ[yi × log(ŷi) + (1 - yi) × log(1 - ŷi)] ... (1)

Accuracy = (1/n) × ΣI(yi = ŷi) ... (2)
```

## LaTeX Formatting

### Single Equation

```latex
\begin{equation}
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
\label{eq:accuracy}
\end{equation}

As shown in Equation~\ref{eq:accuracy}, accuracy measures...
```

### Aligned Equations

```latex
\begin{align}
\text{Precision} &= \frac{TP}{TP + FP} \label{eq:precision} \\
\text{Recall} &= \frac{TP}{TP + FN} \label{eq:recall} \\
\text{F1} &= 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \label{eq:f1}
\end{align}
```

### Inline Math

```latex
The accuracy is calculated as $Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$.
```

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Unnumbered equations | Cannot be referenced in text |
| Undefined variables | Reader cannot interpret the equation |
| Inconsistent notation | Same variable means different things |
| Equations without context | Reader does not know why the equation exists |
| Excessive equations | Adds complexity without understanding |

## Revision Checklist

- [ ] All equations are numbered sequentially
- [ ] All variables are defined at first use
- [ ] Notation is consistent throughout the paper
- [ ] Equations are referenced by number in the text
- [ ] Equations appear on their own line (display equations)
- [ ] Units are specified where applicable
- [ ] Equation count is appropriate (not excessive)
- [ ] Each equation serves a clear purpose
