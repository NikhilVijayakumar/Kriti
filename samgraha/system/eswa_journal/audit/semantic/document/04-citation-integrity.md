# Citation Integrity Audit

This section details the Citation Integrity Audit.

## Version
1.0.0

## Engineering Intent
Enforces the Q1 Reviewer Persona rules for citation quality, reference matching, and target journal relevance.

## Audit Objectives
- Flag the use of blogs, non-peer-reviewed URLs, and known predatory journals.
- Verify that 60-70% of citations fall within the recent 3-4 year window (2022-2026).
- Ensure 2-4 citations are directly from the target journal (ESWA).
- Cross-check that every citation referenced in the text (especially in Related Work) appears in the References section.

## Expected Quality
- Citations are exclusively from high-impact (Q1/Q2 Scopus, CORE A/A*) venues.
- 100% match between in-text citations and the References list.

## Red Flags
- Links to Medium articles, generic tech blogs, or pre-print servers (if excessive).
- Missing references for in-text citations.

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Zero unverified/predatory sources |
| C2 | mandatory | 0 or 40 | 100% in-text to reference list match |
| C3 | recommended | 0 or 20 | Meets recent citation ratio and ESWA target quotas |
