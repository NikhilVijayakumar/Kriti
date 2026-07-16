# Repository Structure Audit

This section details the Repository Structure Audit.

## Version
1.0.0

## Engineering Intent
Repository Structure orients a new contributor to the directory layout at a glance — top-level directories and their purpose, not a file-level map.

## Audit Objectives
- Lists major top-level directories with one-sentence purpose each
- Stays at directory level, no individual files or modules
- Descriptions focus on purpose, not internal implementation

## Expected Quality
- Bullet list, one line per directory
- Directories match what's actually in the repo (not aspirational/stale)
- Purpose descriptions are specific enough to be useful ("Application source code" over "code stuff")

## Red Flags
- Lists individual files or deeply nested paths instead of top-level directories
- Directory list is stale — references directories that no longer exist, or omits major ones that do
- Descriptions describe internal code organization (class names, module internals) instead of directory purpose

## Edge Cases
- Monorepo with many top-level packages — group by category if an exhaustive flat list would exceed a scannable length
- Repository with a conventional/obvious layout (e.g. standard framework scaffold) — brief entries are acceptable, omission is not

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Major directories listed with purpose, not files |
| C2 | mandatory | 0 or 30 | Directory list matches actual repository contents |
| C3 | recommended | 0 or 30 | Descriptions are purpose-focused, not implementation-focused |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.8,
  "severity": "error",
  "evidence": { "section_id": 7, "paragraph_index": 0, "excerpt": "- src/core/scheduler/worker.py — The main worker loop" },
  "message": "Repository Structure lists a specific file path instead of a top-level directory."
}
```
