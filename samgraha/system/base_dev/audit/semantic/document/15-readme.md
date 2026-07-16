# README Document Audit

This section details the README Document Audit.

## Version
1.0.0

## Engineering Intent
Verifies a README coheres as one accurate entry point — Usage examples must match Build/Installation instructions, Development must match Contributing, and nothing in the README contradicts itself. Section-level quality is owned by `audit/semantic/section/readme/`; this file owns cross-section consistency.

## Audit Objectives
- Usage examples are consistent with Build and Installation instructions — a command shown in Usage must actually exist given how Installation/Build set the project up
- Development's setup steps are consistent with Contributing's referenced workflow — no contradiction in branch naming, test commands, or review process
- Terminology is consistent across all README sections — the same command, flag, or concept isn't named differently in different sections

## Expected Quality
- Every command shown in Usage is reachable given Installation/Build's actual steps (e.g. the binary name matches)
- Development's local setup and Contributing's process reference the same branch/PR conventions
- Project/command names are used identically throughout the README

## Red Flags
- Usage shows a command that doesn't match the binary/package name established in Installation
- Development describes one test command, Contributing implies a different one is what CI actually runs
- Configuration's documented variables don't match what Usage's examples actually set
- Project name in Project Name section doesn't match the name used in Installation/Usage commands

## Edge Cases
- README covering multiple entry points (CLI + library usage) — acceptable if both are internally consistent and clearly distinguished, not merged into one ambiguous example
- Monorepo README aggregating multiple sub-projects — acceptable if per-project consistency holds, cross-project terminology drift is the actual concern

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Usage examples consistent with Build/Installation instructions |
| C2 | mandatory | 0 or 30 | Development and Contributing describe a consistent workflow |
| C3 | recommended | 0 or 30 | Terminology (commands, flags, names) consistent throughout |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.84,
  "severity": "error",
  "evidence": { "section_id": 8, "paragraph_index": 0, "excerpt": "Installation installs `acme-cli`. Usage shows `acmescheduler run`." },
  "message": "Usage example uses a command name that doesn't match the binary installed per Installation."
}
```
