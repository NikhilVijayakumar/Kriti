# Mathematics Examples

> *Source: PCEMS 2026 Sample Papers — Annotated Excerpts*

## Purpose

This document presents annotated examples of effective and ineffective mathematical notation from PCEMS 2026 sample papers, with analysis tied to the notation conventions.

## Good Patterns

### Example 1: Feature Selection Equation

**Source**: Hybrid Feature Selection and Optimized Deep CNN for Heart Disease Prediction

> The Kumar-Hassebrook coefficient is defined as:
>
> KH(A, B) = 2|A ∩ B| / (|A| + |B|) ... (1)
>
> where A and B represent feature sets, and |A| denotes the cardinality of set A.

**Why this works**:
- Equation is numbered (1)
- All variables are defined (A, B, |A|)
- Equation serves a clear purpose (feature selection)
- Variable definitions appear in the text, not in the equation
- Standard notation (cardinality notation is widely understood)

### Example 2: Performance Metrics

**Source**: Credit Card Fraud Detection Using Machine Learning Techniques

> Positive Predictive Value (or) Precision: Precision is the proportion of positive cases correctly identified. That means TP/(TP+FP).
>
> Accuracy: Accuracy is the proportion of the total number of correct predictions. That means (TN+TP)/(TP+TN+FN+FP).

**Why this works**:
- Standard abbreviations (TP, FP, TN, FN)
- Clear definitions before the formula
- Formula presented inline with the definition
- Metrics are well-known and widely used

### Example 3: Data Representation

**Source**: Hybrid Feature Selection and Optimized Deep CNN for Heart Disease Prediction

> Let us consider the input data acquired from heart disease dataset stated in [17] and it is represented as follows:
>
> V = {V₁, V₂, ..., Vᵢ, ..., Vₘ} ... (1)
>
> Each data in this instance has a dimension of p×q, and Vᵢ designates the ith data in the database that is preprocessed.

**Why this works**:
- Clear mathematical notation
- Variable dimensions specified (p×q)
- Subscript notation used consistently
- Reference to source dataset [17]

## Anti-Patterns

### Anti-Pattern 1: Undefined Variables

**Issue**: An equation introduces variables without defining them.

**Example**:
> "The accuracy is calculated as: Acc = (TP + TN) / (TP + TN + FP + FN)"

**Why it fails**:
- TP, TN, FP, FN are not defined
- Reader must guess their meaning
- Violates the "define at first use" rule

**Fix**: Define all variables before the equation:
> "The accuracy is calculated using True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN):
> Acc = (TP + TN) / (TP + TN + FP + FN) ... (1)"

### Anti-Pattern 2: Inconsistent Notation

**Issue**: The same variable is used with different meanings in different sections.

**Example**:
- Section II: "*n*" = number of features
- Section IV: "*n*" = number of samples

**Why it fails**:
- Reader cannot track variable meaning
- Creates confusion in equations
- Violates consistency principle

**Fix**: Use distinct variables for distinct quantities (e.g., *d* for features, *n* for samples).

### Anti-Pattern 3: Excessive Equations

**Issue**: A paper includes equations that do not serve the narrative.

**Example**: Including the derivation of a well-known formula that the reader is expected to know.

**Why it fails**:
- Adds complexity without understanding
- Consumes valuable page space
- Does not contribute to the paper's contribution

**Fix**: Reference the standard result and focus on your novel contribution:
> "The system uses standard CNN architecture [citation] with the following modifications: ..."

### Anti-Pattern 4: Equations Without Context

**Issue**: An equation appears without explaining why it is needed.

**Example**:
> "The loss function is:
> L = -Σ[yi × log(ŷi) + (1 - yi) × log(1 - ŷi)] ... (1)"

**Why it fails**:
- Reader does not know why this equation is included
- No connection to the paper's methodology
- Appears to be filler

**Fix**: Provide context before the equation:
> "To train the classification model, we minimize the binary cross-entropy loss:
> L = -Σ[yi × log(ŷi) + (1 - yi) × log(1 - ŷi)] ... (1)
> where yi is the true label and ŷi is the predicted probability."

## Comparison: Good vs. Bad

### Good Equation Introduction
> "The Dice coefficient, used for feature selection, is defined as:
> Dice(A, B) = 2|A ∩ B| / (|A| + |B|) ... (1)
> where A and B represent feature sets, and |A| denotes the cardinality of set A."

- Context provided (feature selection)
- All variables defined
- Equation numbered
- Purpose clear

### Bad Equation Introduction
> "The formula is:
> f(x) = ax² + bx + c"

- No context (why is this equation included?)
- Variables a, b, c not defined
- No equation number
- No connection to the paper's contribution

## Revision Checklist

- [ ] All variables are defined at first use
- [ ] Equations are numbered sequentially
- [ ] Notation is consistent throughout the paper
- [ ] Each equation serves a clear purpose
- [ ] Context is provided before each equation
- [ ] Standard notation is used where applicable
- [ ] Equations are referenced by number in the text
- [ ] No excessive equations that do not contribute to the narrative
