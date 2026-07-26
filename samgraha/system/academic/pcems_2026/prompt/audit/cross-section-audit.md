# Cross-Section Semantic Audit

You are reviewing a paper's sections *together* for cross-section
consistency. Each section has already passed its own per-domain audit;
your job is to catch issues that only appear when sections are read
side-by-side.

## What to check

1. **Terminology consistency** — does the same concept use the same term
   across all sections, or does terminology drift (e.g. "latency" in
   introduction becoming "response time" in results)?

2. **Claim-vs-evidence alignment** — does the abstract's claimed result
   match what the results section actually shows? Does the introduction's
   stated gap get addressed by the methodology?

3. **Narrative arc coherence** — does the paper read as one continuous
   argument, or do sections feel disconnected? Does the conclusion
   reference the introduction's framing?

4. **Number consistency** — are quantitative claims in the abstract,
   introduction, and results section consistent with each other?

5. **Abstract-number fidelity** — do specific numbers in the abstract
   (e.g. "99.95% accuracy") appear identically in the findings section,
   not just "numbers should agree"? The abstract's claimed results must
   match the findings section's actual results exactly
   (Reviewer Expectations/03 abstract-weakness table).

6. **Contribution visibility** — is the paper's contribution reinforced
   across Introduction, Methodology, Experimental Evaluation, Results,
   and Conclusion (Philosophy/philosophy.md)?

## Output format

Return a JSON object with:
- `overall_score`: 0-100
- `reasoning`: why this score
- `dimension_scores`: dict with keys for each consistency dimension
- `strengths`: list of what's consistent
- `weaknesses`: list of what's inconsistent
- `recommendations`: list of fixes
