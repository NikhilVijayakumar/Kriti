# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Purpose defines what the README is and is not — the boundary between README and the rest of the documentation ecosystem. It exists so a reader knows when to stop reading the README and go to Vision, Feature, or Architecture docs instead.

## Audit Objectives
- States what the README covers and what it deliberately excludes
- References the broader documentation ecosystem (Vision, Features, Architecture) rather than absorbing their content
- Does not duplicate detailed documentation from other standards

## Expected Quality
- One to two paragraphs, boundary stated explicitly ("this covers X, not Y")
- Points the reader toward the right downstream doc for anything out of scope
- Distinguishes README's entry-point role from a comprehensive reference

## Red Flags
- Claims to cover API references, database schemas, or deployment procedures that belong to other standards
- No boundary statement at all — reads as an unscoped introduction
- Scope language is vague ("this README has everything you need") instead of explicit inclusion/exclusion

## Edge Cases
- Very small project where README genuinely is the only documentation — acceptable, but should still state that explicitly rather than imply a boundary that doesn't exist
- Monorepo README describing multiple sub-projects' documentation entry points

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Explicitly states README's scope boundary (what it is, what it is not) |
| C2 | mandatory | 0 or 30 | References the broader documentation ecosystem rather than duplicating it |
| C3 | recommended | 0 or 20 | Boundary is specific (named exclusions), not vague |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.87,
  "severity": "error",
  "evidence": { "section_id": 5, "paragraph_index": 0, "excerpt": "This README covers all project documentation including API references, database schemas, and deployment procedures." },
  "message": "Purpose claims to cover content that belongs to other documentation standards instead of stating a boundary."
}
```
