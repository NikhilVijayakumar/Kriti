# Installation Audit

This section details the Installation Audit.

## Version
1.0.0

## Engineering Intent
Installation gets the project onto a machine — prerequisites and exact commands, with a way to verify it worked. Unlike Getting Started (project running end-to-end), Installation is scoped to "the thing is installed."

## Audit Objectives
- Prerequisites listed with version numbers
- Step-by-step install commands, copy-paste safe
- A verification step confirming installation succeeded

## Expected Quality
- Prerequisites and Install as distinct, clearly separated subsections
- Commands shown in fenced code blocks, not prose descriptions of commands
- Verification command's expected output is shown, not just implied

## Red Flags
- Vague instructions ("clone the repo and it works") with no explicit commands
- Prerequisites omitted or version numbers missing
- No verification step — reader can't tell if installation succeeded

## Edge Cases
- Multiple install methods (package manager vs. source build) — cover the primary path fully; secondary paths can be lighter but must still be runnable
- Platform-specific install differences — note them explicitly rather than assuming one OS

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 35 | Prerequisites listed with version numbers |
| C2 | mandatory | 0 or 35 | Step-by-step commands, copy-paste safe |
| C3 | recommended | 0 or 30 | Verification step with expected output |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.9,
  "severity": "error",
  "evidence": { "section_id": 9, "paragraph_index": 0, "excerpt": "Just clone the repo and it works. You might need to install some things first." },
  "message": "Installation gives no explicit commands or prerequisites — reader is left guessing."
}
```
