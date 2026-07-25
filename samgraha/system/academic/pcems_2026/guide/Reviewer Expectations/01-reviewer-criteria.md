# Reviewer Criteria

> *Source: PCEMS 2026 Template + Sample Paper Analysis + Conference Guidelines*

## Purpose

Understanding what reviewers evaluate determines whether a paper succeeds or fails. This document describes the criteria reviewers apply when assessing PCEMS manuscripts, derived from the conference template structure and patterns observed in accepted sample papers.

## Primary Evaluation Dimensions

### 1. Technical Contribution

Reviewers assess whether the paper presents a clearly identifiable engineering contribution.

**Strong contribution indicators**:
- Novel method, system, or analysis with measurable outcomes
- Comparative evaluation against existing approaches
- Reproducible experimental methodology
- Quantitative results with statistical significance

**Weak contribution indicators**:
- Incremental improvement without clear justification
- No comparison with existing methods
- Qualitative-only evaluation
- Missing or inconclusive results

### 2. Methodological Rigor

Reviewers verify that the research methodology is sound, complete, and appropriate for the stated problem.

| Criterion | Acceptable | Unacceptable |
|-----------|------------|--------------|
| Dataset description | Source, size, attributes, preprocessing steps | "A dataset was used" |
| Experimental setup | Hardware/software specs, parameters, environment | "Experiments were conducted" |
| Evaluation metrics | Standard metrics with clear definitions | "Accuracy was measured" |
| Baseline comparison | Multiple established methods | No comparison or trivial baseline |
| Reproducibility | Enough detail to replicate | Missing parameters or configurations |

### 3. Presentation Quality

Reviewers evaluate clarity, organization, and adherence to formatting requirements.

- **Structure**: Follows standard IMRAD or template-prescribed sections
- **Abstract**: Summarizes problem, method, results, and contribution in 150-250 words
- **Figures and tables**: Appear immediately after first reference, properly labeled, legible
- **Citations**: Consistent numbered style, all references cited in text, all citations in reference list
- **Language**: Formal engineering prose, no informal or AI-generated patterns

### 4. Literature Engagement

Reviewers check whether the paper situates itself within existing work.

- Related work covers key prior approaches (not just recent papers)
- Gap in existing work is clearly identified
- Proposed solution directly addresses the identified gap
- Appropriate number of references (15-30 based on sample paper analysis)

### 5. Writing and Formatting Compliance

Reviewers enforce PCEMS formatting requirements:

- Single-column Word document
- Arial fonts at prescribed sizes (14pt title, 12pt headings, 11pt body)
- Roman numeral section numbering
- IEEE numbered citation style ([1], [2])
- Figures and tables inline after first reference
- Keywords listed after abstract

## Reviewer Workflow

1. **First pass**: Scan title, abstract, figures, and conclusion (2-3 minutes)
2. **Second pass**: Read introduction, methodology, and results (10-15 minutes)
3. **Third pass**: Detailed evaluation against criteria (20-30 minutes)
4. **Decision**: Accept, minor revisions, major revisions, or reject

## First-Pass Red Flags

Reviewers form initial impressions quickly. These patterns trigger immediate skepticism:

- Title is vague or overly broad
- Abstract lacks quantitative results
- No figures or tables in the paper
- Obvious formatting violations
- References are outdated or sparse (< 10)
- AI-generated language patterns (delve, tapestry, landscape, paramount)

## Second-Pass Evaluation

If the first pass passes, reviewers examine:

- Introduction clearly states the problem and contribution
- Methodology is detailed enough to replicate
- Results section presents data, not just claims
- Discussion interprets results in context
- Conclusion summarizes without introducing new information

## Domain-Specific Expectations

### Computer Science / Machine Learning
- Model architecture diagram required
- Training details (hyperparameters, epochs, hardware)
- Comparison with 3+ baselines
- Ablation study when proposing composite methods
- Dataset statistics and class distribution

### Electronics / VLSI
- Device structure or circuit diagram
- Simulation tool and model parameters
- Performance metrics (power, delay, area)
- Comparison with analytical models or measured data
- Scaling behavior across technology nodes

### IoT / Embedded Systems
- System architecture diagram
- Hardware components with specifications
- Software stack description
- Real-world deployment or prototype demonstration
- Power consumption and latency measurements

## Revision Checklist

- [ ] Paper has a clearly stated contribution in abstract and introduction
- [ ] Methodology is described in sufficient detail for replication
- [ ] Results include quantitative comparison with existing methods
- [ ] All figures and tables are referenced in text before appearance
- [ ] Formatting complies with PCEMS template requirements
- [ ] References cover key prior work in the domain
- [ ] No AI-generated language patterns remain
- [ ] All abbreviations defined at first use
