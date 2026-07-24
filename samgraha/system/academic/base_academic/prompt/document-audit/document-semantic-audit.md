# Document Semantic Audit

You are reviewing the *entire assembled paper* as a single document —
the way a reviewer or reader would experience it. This is distinct from
per-section scoring (which checks each domain against its own rubric) and
cross-section consistency (which checks terminology/claim alignment).

## What to check

1. **Gap closure** — does the conclusion close the gap stated in the
   introduction? If the intro promises a contribution, does the paper
   deliver it?

2. **Methodology-results alignment** — does the methodology section
   describe an approach that actually produces the results shown? Are
   there results without a methodology, or methodology without results?

3. **Overall readability and flow** — does the paper read well as a
   continuous document? Are transitions between sections smooth?

4. **Completeness** — are there obvious holes (a section that's too short,
   missing references, promises of future work that should be here)?

5. **Abstract accuracy** — does the abstract accurately represent the
   full paper, or does it overclaim/underclaim?

## Output format

Return a JSON object with:
- `overall_score`: 0-100
- `reasoning`: why this score
- `dimension_scores`: dict with keys for each review dimension
- `strengths`: list of what works well
- `weaknesses`: list of what needs improvement
- `recommendations`: list of specific fixes
