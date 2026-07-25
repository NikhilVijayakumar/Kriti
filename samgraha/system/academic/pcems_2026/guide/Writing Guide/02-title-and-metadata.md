# Title and Metadata Writing Guide

> *Source: PCEMS 2026 Template + Conference Guidelines/02-manuscript-structure.md + Documentation-Standards/01-title-and-metadata-standards.md*

## Purpose

The title and metadata block is the first element reviewers evaluate. It must communicate the paper's scope, authorship, and institutional affiliation with exact typographic compliance.

## Structure

The metadata block appears in this order:

1. Title
2. Authors (with superscript institution numbers)
3. Affiliations (with institution numbers)
4. Corresponding author email
5. Keywords

## Title

### Requirements

- **Font**: Arial, 14pt, Bold
- **Alignment**: Center
- **Length**: 10-15 words (descriptive, not clever)
- **Content**: Must reflect the paper's actual contribution

### Writing Strategy

The title must communicate what the paper does, not what the paper is about. A strong title identifies the domain, the method, and the application.

| Weak Title | Strong Title |
|-----------|-------------|
| "A Study on Machine Learning" | "Credit Card Fraud Detection Using Random Forest Classification" |
| "IoT Application" | "IoT-Based Smart Food Grain Warehouse Monitoring System" |
| "Heart Disease Prediction" | "Hybrid Feature Selection and Optimized Deep CNN for Heart Disease Prediction" |

### Patterns

- **Method + Application**: "Deep CNN-Based Early Leaf Disease Prediction in Paddy Crops"
- **System + Function**: "IoT-Based Smart Food Grain Warehouse Monitoring System"
- **Comparative + Domain**: "Comparative Study of Data-Driven Methods for State of Charge Estimation"

### Anti-Patterns

- Vague titles: "A Novel Approach to X"
- Question titles: "Can Machine Learning Detect Fraud?"
- Overly long titles: More than 20 words
- Acronyms in title: Spell out unless universally known (IoT, CNN are acceptable)

## Authors

### Requirements

- **Font**: Arial, 12pt, Bold
- **Alignment**: Center
- **Format**: First name Last name (not initials unless that is the published convention in the field)
- **Superscript numbers**: Link each author to their institution

### Example

```
Indrani Vejalla, Preethi Battula, Kartheek Kalluri, and Hemantha Kumar Kalluri
1                        2                        3                        4
```

### Notes

- Use "and" before the final author (Oxford comma optional but be consistent)
- Superscript numbers must match affiliation entries exactly
- Corresponding author indicated by email placement, not by asterisk (unless template specifies otherwise)

## Affiliations

### Requirements

- **Font**: Arial, 11pt
- **Alignment**: Center
- **Format**: Department, Institution, City, Country

### Example

```
1 Department of Computer Science, VFSTR University, India
2 Department of Computer Science, VFSTR University, India
3 Department of ECE, RVR&JC College of Engineering, India
4 Department of CSE, SRM University AP, India
```

### Notes

- One affiliation per line
- Include department, institution, city, and country
- Corresponding author email on a separate line after affiliations

## Keywords

### Requirements

- **Font**: Arial, 12pt, Bold (label "Keywords:" and the keywords themselves)
- **Count**: Minimum 4, maximum 6
- **Placement**: After abstract, before Introduction

### Writing Strategy

Keywords serve two purposes: indexing and searchability. Choose terms that:

1. Identify the domain (e.g., "credit card fraud," "heart disease")
2. Identify the method (e.g., "machine learning," "deep CNN," "IoT")
3. Are searchable in academic databases

### Example

```
Keywords— Credit Card, Fraud Detection, Classification, Machine Learning, Random Forest
```

### Anti-Patterns

- Generic keywords: "research," "analysis," "method"
- Too few: fewer than 4 keywords
- Too many: more than 6 keywords
- Abbreviations without expansion: "CCFD" instead of "Credit Card Fraud Detection"

## LaTeX Formatting

For authors using LaTeX, the metadata block should use:

```latex
\title{\textbf{Title Here}}  % Arial 14pt Bold Centered
\author{
  Author A\thanks{email@example.com}\textsuperscript{1},
  Author B\textsuperscript{2}
}
\institute{
  \textsuperscript{1}Institution 1 \\
  \textsuperscript{2}Institution 2
}
\maketitle

\keywords{keyword1, keyword2, keyword3, keyword4}
```

Note: The final document must be submitted as a Microsoft Word document, even if drafted in LaTeX. The LaTeX source is for drafting purposes only.
