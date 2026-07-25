# Methodology Writing Guide

> *Source: PCEMS 2026 Template + Documentation-Standards/03-methodology-standards.md + Sample Paper Analysis*

## Purpose

The Methodology section describes how the proposed solution works. It must provide sufficient detail for another researcher to understand, evaluate, and reproduce the approach. This section answers: "How does the proposed solution work, and why does it work?"

## Structure

A PCEMS Methodology section follows a systematic description pattern: overview → components → process → implementation details.

### Required Elements

1. **Methodology Overview** (1 paragraph): High-level description of the approach
2. **System Architecture / Workflow** (1-2 subsections): Components and their interactions
3. **Algorithms / Equations** (as needed): Mathematical formulation of key methods
4. **Implementation Details** (1 subsection): Tools, parameters, configuration

### Template

```markdown
[Explain the proposed methodology at a high level]
[Describe the system architecture or workflow]
[Present algorithms, equations, and mathematical formulations]
[Detail implementation specifics: tools, libraries, parameters]
```

## Content Requirements

### Methodology Overview

Begin with a high-level statement of what the methodology does and why this particular approach was chosen. Connect back to the gap identified in the Introduction.

**Example pattern**:
> "To address [gap from Introduction], this paper proposes [method name]. The approach consists of [number] main stages: [stage 1], [stage 2], and [stage 3]."

### System Architecture

Describe the system as a pipeline of components. For each component:
- What it does (function)
- What it takes as input
- What it produces as output
- Why it is designed this way (justification)

Use a block diagram (Figure X) to visualize the architecture. Reference the figure in the text:

> "Fig. 1 illustrates the overall architecture of the proposed system. The input data passes through [component 1], which produces [output]. This output is fed to [component 2]..."

### Algorithms and Equations

When the methodology involves algorithms or mathematical operations:

1. **Present the algorithm** in pseudocode or as a numbered list of steps
2. **Define all variables** used in equations
3. **Explain the rationale** for each step
4. **Number equations** sequentially: (1), (2), (3)...

**Example**:
> The feature selection process uses the Dice coefficient, defined as:
>
> Dice(A, B) = 2|A ∩ B| / (|A| + |B|) ... (1)
>
> where A and B represent feature sets, and |A| denotes the cardinality of set A.

### Implementation Details

Specify:
- Programming language and version
- Libraries and frameworks (with versions)
- Hardware configuration (if relevant)
- Parameter settings and hyperparameters
- Dataset characteristics (size, features, splits)

## Typography

- **Section heading**: Heading 1 (Arial, 12pt, Bold)
- **Subsection headings**: Heading 2 (Arial, 12pt) or Heading 3 (Arial, 12pt, Italic)
- **Body text**: Arial, 11pt
- **Equations**: Numbered, centered
- **Algorithm pseudocode**: Monospace font if possible, otherwise consistent formatting

## Length Guidelines

Based on sample paper analysis:

| Metric | Range | Target |
|--------|-------|--------|
| Word count | 600-1,200 words | 800-1,000 words |
| Subsections | 2-5 | 3-4 |
| Equations | 0-8 | 2-5 |
| Figures | 0-2 | 1 (block diagram) |

## Writing Strategy

### Do

- Describe the method in sufficient detail for reproduction
- Justify design decisions (why this algorithm, why these parameters)
- Use a block diagram to visualize the architecture
- Define all variables and abbreviations at first use
- Connect each component back to the problem it solves

### Do Not

- Present results in the Methodology section
- Describe the dataset in detail (save for Findings)
- Use vague descriptions ("a suitable algorithm was used")
- Skip implementation details that affect reproducibility
- Introduce new terminology without definition

## Common Patterns from Sample Papers

Analysis of 11 accepted PCEMS 2026 papers:

1. **Block diagram**: 9 of 11 papers include a system architecture figure
2. **Equations**: 7 of 11 papers include at least one equation
3. **Subsection structure**: Most papers use subsections for each major component
4. **Implementation details**: 8 of 11 papers specify tools and libraries
5. **Average length**: ~900 words

## LaTeX Formatting

For equations in LaTeX:

```latex
\begin{equation}
\text{Dice}(A, B) = \frac{2|A \cap B|}{|A| + |B|}
\label{eq:dice}
\end{equation}

As shown in Equation (\ref{eq:dice}), the Dice coefficient...
```

## Revision Checklist

- [ ] Methodology is described in sufficient detail for reproduction
- [ ] All design decisions are justified
- [ ] Block diagram is included and referenced
- [ ] All variables are defined at first use
- [ ] All equations are numbered and referenced
- [ ] Implementation details (tools, parameters) are specified
- [ ] No results appear in the Methodology section
- [ ] Subsections organize components logically
- [ ] Length is within 600-1,200 words
