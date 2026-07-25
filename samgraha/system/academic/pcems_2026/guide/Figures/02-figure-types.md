# Figure Types

> *Source: Sample Paper Analysis + PCEMS Publication Philosophy*

## Purpose

This document describes the figure types commonly used in PCEMS papers, their appropriate use cases, and construction guidelines.

## Figure Type Catalog

### 1. Block Diagram / System Architecture

**Use when**: Describing the overall system, pipeline, or component interactions.

**Construction guidelines**:
- Use rectangular boxes for components
- Use arrows for data flow (label arrows if the flow is not obvious)
- Group related components visually (proximity or shared border)
- Align boxes in a grid pattern
- Include a title or caption that explains the overall architecture

**Example from sample papers**:
> "Fig. 1. Block diagram of IoT based smart food grain warehouse" — shows sensor nodes, microcontroller, cloud platform, and mobile application as connected boxes.

### 2. Performance Bar Chart

**Use when**: Comparing accuracy, precision, recall, or other metrics across multiple methods.

**Construction guidelines**:
- X-axis: Methods (abbreviated if necessary)
- Y-axis: Metric value (0-100% or 0-1.0)
- One bar per method per metric
- Grouped bars when comparing multiple metrics
- Error bars when standard deviation is available
- Grid lines for readability

**Example from sample papers**:
> "Fig. 2. Performance of ML models with test size 80%" — grouped bar chart showing accuracy, precision, recall, F1-score for each method.

### 3. Line Graph

**Use when**: Showing trends across a continuous variable (time, iterations, parameter values).

**Construction guidelines**:
- X-axis: Continuous variable
- Y-axis: Measured outcome
- Distinct line styles (solid, dashed, dotted) for multiple series
- Markers at data points
- Legend when multiple lines present
- Smooth curves only if the underlying relationship is continuous

### 4. Confusion Matrix Heatmap

**Use when**: Presenting classification results for multi-class problems.

**Construction guidelines**:
- Rows: Actual class
- Columns: Predicted class
- Color intensity: Number of samples
- Labels on both axes
- Diagonal highlighted (correct predictions)

### 5. Flowchart

**Use when**: Describing an algorithm, decision process, or procedural workflow.

**Construction guidelines**:
- Standard symbols: oval (start/end), rectangle (process), diamond (decision), parallelogram (I/O)
- Consistent flow direction (top-to-bottom or left-to-right)
- One decision per diamond
- Clear labels in each shape
- Exit paths labeled (yes/no, true/false)

### 6. ROC Curve / Precision-Recall Curve

**Use when**: Evaluating classifier performance across thresholds.

**Construction guidelines**:
- X-axis: False Positive Rate (ROC) or Recall (PR)
- Y-axis: True Positive Rate (ROC) or Precision (PR)
- Diagonal reference line (ROC only, for random classifier)
- AUC value in the legend
- Multiple curves for multiple methods

### 7. Box Plot

**Use when**: Showing distribution of results across multiple runs or folds.

**Construction guidelines**:
- Box: Interquartile range (25th-75th percentile)
- Line inside box: Median
- Whiskers: Minimum/maximum or 1.5x IQR
- Points: Outliers
- One box per method or configuration

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Screenshot of code | Not a figure; use formatted text block |
| Decorative image | Adds no technical value |
| 3D bar chart | Distorts perception of values |
| Pie chart with many slices | Hard to read; use bar chart instead |
| Figure without caption | Incomplete; violates template |
| Figure not referenced in text | Orphaned;读者 cannot locate it |
| Color-only distinction | Fails in grayscale print |
| Low-resolution photograph | Unprofessional; below 300 DPI |

## Revision Checklist

- [ ] Figure type matches the information being communicated
- [ ] Figure is constructed according to type-specific guidelines
- [ ] Figure is legible in grayscale
- [ ] Figure has a clear caption
- [ ] Figure is referenced in the text before it appears
- [ ] Figure is placed immediately after first reference
- [ ] Figure number is sequential throughout the paper
