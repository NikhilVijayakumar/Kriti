# Project Name Audit

This section details the Project Name Audit.

## Version
1.0.0

## Engineering Intent
Project Name states the canonical name exactly as it appears in package manifests. It exists so every reference to the project — docs, packages, repos — resolves to one unambiguous name.

## Audit Objectives
- States only the name, no description or tagline
- Matches the name used in package manifests (package.json, Cargo.toml, pyproject.toml, etc.)
- No abbreviation, codename, or marketing variant substituted for the canonical name

## Expected Quality
- Single line or heading, name only
- Verified consistent with the manifest file(s) in the repo
- No surrounding descriptive prose in this section specifically

## Red Flags
- A description or one-liner appended to the name ("Acme Platform is a comprehensive solution...")
- Name doesn't match the package manifest
- Codename or internal nickname used instead of the published name

## Edge Cases
- Monorepo with multiple package names — state the repository/product name, not every package name
- Name change in progress — README should reflect the current published name, not the target rename

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 60 | Section contains only the canonical name, no description |
| C2 | mandatory | 0 or 40 | Name matches package manifest(s) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.9,
  "severity": "error",
  "evidence": { "section_id": 2, "paragraph_index": 0, "excerpt": "The Acme Platform is a comprehensive project management solution." },
  "message": "Project Name section contains a description instead of only the canonical name."
}
```
