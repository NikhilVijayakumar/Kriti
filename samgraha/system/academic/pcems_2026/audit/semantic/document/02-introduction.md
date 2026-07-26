# Semantic Rubric: Introduction

## Scoring Criteria

### C1: Problem Context Quality
- **criterion_id**: C1
- **points**: 20
- **mandatory**: false
- **description**: Does the problem context start with the engineering problem (not dictionary definitions or overly broad statements)?
- **pass_condition**: Opens with specific problem, statistics, or impact statement

### C2: Gap Specificity
- **criterion_id**: C2
- **points**: 25
- **mandatory**: true
- **description**: Is the gap specific and verifiable — would a reader be able to confirm it by reading the cited works?
- **pass_condition**: Gap is concrete, cites specific limitations of prior work, not vague "existing work is insufficient"

### C3: Contribution Statement
- **criterion_id**: C3
- **points**: 20
- **mandatory**: true
- **description**: Does the contribution statement directly address the identified gap with explicit numbered contributions?
- **pass_condition**: Numbered contribution list present, each contribution maps to the gap

### C4: No Methodology Leakage
- **criterion_id**: C4
- **points**: 10
- **mandatory**: false
- **description**: Does the Introduction avoid methodology details, results, or conclusions that belong in later sections?
- **pass_condition**: No algorithm descriptions, equations, or quantitative results

### C5: Citation Density
- **criterion_id**: C5
- **points**: 10
- **mandatory**: false
- **description**: Are there sufficient citations (5-15) supporting the problem context and gap?
- **pass_condition**: 5-15 in-text citations present
