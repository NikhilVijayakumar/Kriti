# License Audit

This section details the License Audit.

## Version
1.0.0

## Engineering Intent
License states the exact license name with a direct link to the full text and copyright notice. It exists so the legal terms of use are unambiguous, not something a reader has to infer.

## Audit Objectives
- Specific license name stated (not "see license file")
- Direct link to the full license text provided
- Copyright notice included where applicable

## Expected Quality
- License name matches a recognized license identifier (Apache-2.0, MIT, GPL-3.0, etc.) or explicitly states a custom/proprietary license
- Link resolves to an actual license file/page in the repo
- Copyright year and holder stated if the project claims copyright

## Red Flags
- "You can use this however you want, see the license file" with no name or link
- License name omitted, only a link (or vice versa)
- Legal advice or comparisons between licenses included — out of scope for a README

## Edge Cases
- Multi-license project (e.g. dual-licensed, or different licenses per package in a monorepo) — state which license applies to which part, not one blanket claim
- Proprietary/closed-source project — state that explicitly ("All rights reserved") rather than leaving the section silent

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 50 | Specific license name stated |
| C2 | mandatory | 0 or 30 | Direct link to full license text provided |
| C3 | recommended | 0 or 20 | Copyright notice included |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.9,
  "severity": "error",
  "evidence": { "section_id": 15, "paragraph_index": 0, "excerpt": "You can use this software however you want. See the license file for details." },
  "message": "License section names no specific license and provides no link to the full text."
}
```
