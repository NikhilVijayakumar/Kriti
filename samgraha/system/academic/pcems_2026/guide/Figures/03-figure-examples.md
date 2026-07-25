# Figure Examples

> *Source: PCEMS 2026 Sample Papers — Annotated Excerpts*

## Purpose

This document presents annotated examples of effective and ineffective figure usage from PCEMS 2026 sample papers, with analysis tied to the figure standards.

## Good Patterns

### Example 1: System Architecture Block Diagram

**Source**: IoT Based Smart Food Grain Warehouse

> "Fig. 1. Block diagram of IoT based smart food grain warehouse"

The figure shows sensor nodes (DHT11, MQ135, PIR) connected to a microcontroller (NodeMCU), which connects to a cloud platform (Blynk) and a display unit. Arrows indicate data flow direction. Each component is labeled.

**Why this works**:
- Clearly illustrates the system architecture
- Each component is labeled and identifiable
- Data flow direction is indicated with arrows
- The caption describes what the figure shows
- The figure is referenced in the text before it appears

### Example 2: Performance Comparison Bar Chart

**Source**: Credit Card Fraud Detection Using Machine Learning Techniques

> "Fig. 1. Performance of ML models with test size 20%"

The figure shows a grouped bar chart with six methods (LR, NB, DT(E), DT(GI), SVM, RF) on the x-axis and four metrics (accuracy, precision, recall, F1-score) as grouped bars.

**Why this works**:
- Enables direct comparison across methods
- Multiple metrics shown simultaneously
- Clear axis labels
- Consistent color/pattern coding
- Caption is descriptive

### Example 3: Observed vs. Safe Values

**Source**: IoT Based Smart Food Grain Warehouse

> "Fig. 5. Observed values and safe values for wheat and rice."

The figure shows two side-by-side charts comparing observed sensor readings against safe threshold values for different grain types.

**Why this works**:
- Direct visual comparison of observed vs. expected
- Side-by-side layout enables comparison
- Clear labeling of what each bar represents
- Practical engineering value

## Anti-Patterns

### Anti-Pattern 1: Figure Without Text Reference

**Issue**: A figure appears in the manuscript without being referenced in the body text.

**Why it fails**:
- Reader cannot locate the figure through text navigation
- Violates the "reference before placement" rule
- Creates confusion about the figure's purpose

**Fix**: Add a sentence referencing the figure before its placement: "Fig. X illustrates..."

### Anti-Pattern 2: Figure at End of Manuscript

**Issue**: All figures collected at the end instead of inline.

**Why it fails**:
- Violates PCEMS template requirement
- Reader must flip back and forth between text and figures
- Breaks the logical flow of the narrative

**Fix**: Move each figure to immediately after its first reference.

### Anti-Pattern 3: Low-Resolution Screenshot

**Issue**: A screenshot of a software interface used as a figure.

**Why it fails**:
- Low resolution (often 72 DPI)
- Contains unnecessary UI elements
- Text within the screenshot is often illegible
- Not a proper engineering figure

**Fix**: Recreate the content as a proper figure (block diagram, chart, or formatted screenshot with annotations).

### Anti-Pattern 4: Color-Only Distinction

**Issue**: A chart where different data series are distinguished only by color.

**Why it fails**:
- Cannot be read when printed in black and white
- Reviewers may print in grayscale
- Accessibility issue for color-blind readers

**Fix**: Use distinct patterns (solid, dashed, dotted) in addition to color.

## Comparison: Good vs. Bad

### Good Figure Introduction
> "The proposed system architecture is illustrated in Fig. 1. The input data passes through three preprocessing stages before classification."

- Figure is referenced before it appears
- Context is provided
- Reader knows what to look for

### Bad Figure Introduction
> "[Figure 1 placed here without text reference]"

- No context provided
- Reader does not know why the figure exists
- Violates template requirements

## Revision Checklist

- [ ] Every figure is referenced in the text before it appears
- [ ] Every figure provides context through its caption
- [ ] Figures use appropriate type for the information
- [ ] Figures are legible in grayscale
- [ ] Figures are placed inline, not at the end
- [ ] No screenshots used as figures without annotation
- [ ] Color is not the only distinguishing feature
