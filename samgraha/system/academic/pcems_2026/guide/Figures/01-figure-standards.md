# Figure Standards

> *Source: PCEMS 2026 Template + Conference Guidelines/04-figures-and-tables.md + Sample Paper Analysis*

## Purpose

Figures communicate technical information that cannot be explained more effectively using text alone. Every figure must improve understanding by illustrating system architecture, workflows, algorithms, component interactions, experimental setup, or research outcomes.

## Requirements

### Placement

- Figures must appear **immediately after their first reference** in the text
- Do not collect figures at the end of the manuscript
- Do not place figures before their first textual reference

### Resolution and Quality

- Minimum resolution: 300 DPI for photographs, 600 DPI for line art
- All fonts within figures must be legible at the final print size
- No transparent pixels or alpha channels in embedded images
- Use vector formats (SVG, EPS, PDF) when possible for line art

### Labeling

- Figure number: "Fig. 1.", "Fig. 2.", etc. (sequential throughout paper)
- Caption: Below the figure, Arial
- Axis labels: Clear, with units in parentheses
- Legend: Present when multiple data series are shown

### Color

- Ensure figures are readable in grayscale (reviewers may print in black and white)
- Use distinct colors or patterns for different data series
- Avoid relying solely on color to convey meaning

## Figure Types

### Block Diagrams

Used for: System architecture, workflow, pipeline description.

**Standards**:
- Rectangular boxes for components
- Arrows for data flow direction
- Labels inside or below each box
- Consistent box sizes
- Clean, minimal design

### Charts and Graphs

Used for: Performance comparison, trend visualization, distribution display.

**Standards**:
- Bar charts for categorical comparison
- Line charts for trends over time/parameters
- Scatter plots for correlation analysis
- Clear axis labels with units
- Grid lines (light, not dominant)
- Legend when multiple series present

### Photographs

Used for: Experimental setup, hardware implementation, physical samples.

**Standards**:
- High resolution (minimum 300 DPI)
- Annotations with arrows pointing to key features
- Scale bar when size is relevant
- Consistent lighting and background

### Flowcharts

Used for: Algorithm description, decision processes, procedural steps.

**Standards**:
- Standard flowchart symbols (oval for start/end, rectangle for process, diamond for decision)
- Left-to-right or top-to-bottom flow
- Clear labels in each shape
- Consistent sizing

## Writing Strategy

### Do

- Reference every figure in the text before it appears
- Place figures immediately after first reference
- Use figures when they communicate more than text alone
- Ensure figures are legible when printed in grayscale
- Label all axes, components, and data series
- Use consistent numbering throughout the paper

### Do Not

- Use figures as decoration
- Place figures at the end of the paper
- Use screenshots of code (use formatted text instead)
- Rely solely on color to convey meaning
- Use figures without captions
- Include figures that are not referenced in the text

## LaTeX Formatting

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/architecture.pdf}
    \caption{System architecture of the proposed approach.}
    \label{fig:architecture}
\end{figure}

As shown in Figure~\ref{fig:architecture}, the system consists of...
```

## Revision Checklist

- [ ] Every figure is referenced in the text before it appears
- [ ] Every figure is placed immediately after its first reference
- [ ] Every figure has a clear caption
- [ ] All axes are labeled with units
- [ ] Figures are legible in grayscale
- [ ] Resolution meets minimum requirements (300 DPI)
- [ ] No transparent pixels or alpha channels
- [ ] Figure numbering is sequential throughout the paper
- [ ] Figures communicate information not better conveyed by text
