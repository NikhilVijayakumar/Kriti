# Notation Conventions

> *Source: Sample Paper Analysis + PCEMS Publication Philosophy*

## Purpose

This document establishes consistent notation conventions for mathematical symbols, variables, and abbreviations in PCEMS 2026 papers.

## Core Principle

Notation must remain consistent throughout the manuscript. The same concept must not be described using multiple names. Variables, abbreviations, figures, tables, equations, and technical terminology must remain uniform across all sections.

## Variable Naming Conventions

### General Rules

- Use lowercase italic for scalar variables: *x*, *y*, *n*
- Use bold lowercase for vectors: **v**, **w**
- Use bold uppercase for matrices: **A**, **B**
- Use uppercase italic for sets: *S*, *D*
- Use Greek letters for parameters: *θ*, *α*, *β*

### Standard Variable Names

| Variable | Meaning | Usage |
|----------|---------|-------|
| *n* | Sample count | Dataset size, number of iterations |
| *p* | Probability | Class probability, p-value |
| *N* | Population size | Total population |
| *d* | Dimension | Feature count, embedding size |
| *k* | Index or count | k-fold, k-nearest neighbors |
| *t* | Threshold or time | Decision threshold, time step |
| *x* | Input | Input sample, feature vector |
| *y* | Output | True label, predicted label |
| *ŷ* | Prediction | Model output |
| *L* | Loss | Loss function value |
| *η* | Learning rate | Optimization step size |

### Standard Abbreviations

| Abbreviation | Full Form |
|-------------|-----------|
| ML | Machine Learning |
| DL | Deep Learning |
| CNN | Convolutional Neural Network |
| RNN | Recurrent Neural Network |
| LSTM | Long Short-Term Memory |
| SVM | Support Vector Machine |
| RF | Random Forest |
| ANN | Artificial Neural Network |
| KNN | K-Nearest Neighbors |
| TP | True Positive |
| TN | True Negative |
| FP | False Positive |
| FN | False Negative |
| ROC | Receiver Operating Characteristic |
| AUC | Area Under the Curve |
| IoT | Internet of Things |
| IoT | Internet of Things |

## Notation for Specific Domains

### Machine Learning

| Symbol | Meaning |
|--------|---------|
| *f*(·) | Model function |
| *θ* | Model parameters |
| *D* | Dataset |
| *D*<sub>train</sub> | Training set |
| *D*<sub>test</sub> | Test set |
| *y*<sub>i</sub> | True label of sample *i* |
| *ŷ*<sub>i</sub> | Predicted label of sample *i* |

### Signal Processing

| Symbol | Meaning |
|--------|---------|
| *x*(*t*) | Signal in time domain |
| *X*(*f*) | Signal in frequency domain |
| *fs* | Sampling frequency |
| *N* | Number of samples |
| *T* | Signal duration |

### Statistics

| Symbol | Meaning |
|--------|---------|
| *μ* | Mean |
| *σ* | Standard deviation |
| *σ*² | Variance |
| *r* | Correlation coefficient |
| *p* | p-value |

## Rules for Abbreviations

1. **Define at first use**: Spell out the full form at first mention, with the abbreviation in parentheses
2. **Use consistently**: Once defined, use only the abbreviation
3. **Do not define standard abbreviations**: CNN, SVM, ML are universally understood
4. **Do not define abbreviations used only once**: If an abbreviation appears only once, spell it out instead

**Example**:
> "The system uses a Convolutional Neural Network (CNN) for feature extraction. The CNN architecture consists of..."

## Rules for Equations

1. **Define all variables** in the text before the equation
2. **Use consistent notation** across all equations
3. **Number equations** sequentially
4. **Reference equations** by number in the text

## Revision Checklist

- [ ] All variables are defined at first use
- [ ] Notation is consistent throughout the paper
- [ ] Abbreviations are defined at first use
- [ ] Standard abbreviations are not re-defined
- [ ] Greek letters are used consistently
- [ ] Vectors and matrices follow naming conventions
- [ ] No concept is described using multiple names
