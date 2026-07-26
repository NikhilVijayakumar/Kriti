# Semantic Rubric: Findings

## Scoring Criteria

### C1: Experimental Setup Completeness
- **criterion_id**: C1
- **points**: 20
- **mandatory**: true
- **description**: Is the experimental setup described with enough detail for reproduction (dataset source, size, features, split, metrics, hardware)?
- **pass_condition**: Dataset, metrics, and conditions all specified with concrete values

### C2: Objective Results Presentation
- **criterion_id**: C2
- **points**: 20
- **mandatory**: false
- **description**: Are results presented objectively in the Results subsection, with interpretation reserved for Analysis?
- **pass_condition**: Results subsection contains data without interpretation

### C3: Table/Figure Quality
- **criterion_id**: C3
- **points**: 15
- **mandatory**: false
- **description**: Do tables have captions above, header labels, units, consistent decimals? Do figures have captions below, are placed after first reference, legible in grayscale?
- **pass_condition**: All media follows PCEMS formatting rules

### C4: Baseline Comparison
- **criterion_id**: C4
- **points**: 20
- **mandatory**: true
- **description**: Is the comparison with existing methods fair and comprehensive (at least 3 baselines, multiple metrics)?
- **pass_condition**: 3+ baseline methods compared, multiple metrics reported

### C5: Analysis Depth
- **criterion_id**: C5
- **points**: 10
- **mandatory**: false
- **description**: Does the Analysis subsection interpret results, identify key factors, and explain performance differences?
- **pass_condition**: Analysis goes beyond restating numbers to explain why
