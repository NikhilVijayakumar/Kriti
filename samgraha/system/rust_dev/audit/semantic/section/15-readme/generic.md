# Generic Audit

This section details the Generic Audit.

## Version
1.0.0

## Engineering Intent
A generic README section covers project overview, purpose, audience, and technology stack. It must orient a new reader within seconds.

## Audit Objectives
- Project name and one-liner present
- Target audience identified
- Technology stack or platform noted
- Problem statement or motivation clear
- Section avoids deep implementation detail
- Getting-started path is present and completable within 5 minutes by someone in the target audience (install, configure, run first command)
- Troubleshooting section or link covers at least the top 3 known first-run failure modes
- License and attribution are clearly stated

## Expected Quality
- First paragraph states what and why in ≤3 sentences
- Audience section or sentence present
- Links to deeper docs where appropriate
- Consistent tone with rest of README

## Red Flags
- Wall of text without structure
- Missing project name or purpose
- Generic filler ("this is a project")
- Stale year, version, or links
- No getting-started section (reader cannot run the project from the README alone)
- No license stated

## Edge Cases
- Single-sentence section that says nothing
- Section that duplicates later content (e.g. full installation copied here)
- Overly marketing language without substance

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 20 | Project name and one-liner present |
| C2 | mandatory | 0 or 20 | Target audience identified |
| C3 | mandatory | 0 or 20 | Getting-started path completable in ≤5 minutes; license stated |
| C4 | recommended | 0 or 20 | Technology stack noted |
| C5 | recommended | 0 or 20 | Problem statement clear; troubleshooting section present |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 1, "paragraph_index": 0, "excerpt": "Samgraha — AI-augmented knowledge base..." },
  "message": "Project name and one-liner present in first paragraph."
}
```
