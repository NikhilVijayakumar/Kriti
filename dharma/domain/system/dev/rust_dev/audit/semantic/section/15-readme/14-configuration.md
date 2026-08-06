# Configuration Audit

This section details the Configuration Audit.

## Version
1.0.0

## Engineering Intent
Configuration documents the environment variables and config files that control runtime behavior — each with a default, valid values, and a working example. It exists so a reader can configure the project without reading source code.

## Audit Objectives
- Environment variables listed with default and description (table form)
- Configuration files named with their purpose
- Valid values and defaults stated per option
- Working examples provided, not just option names

## Expected Quality
- Environment Variables presented as a table: variable, default, description
- Configuration Files subsection names actual files and links to an example/reference file
- At least one of Environment Variables or Configuration Files present (required)

## Red Flags
- "The config file is in YAML, you can set env vars too" with no actual options listed
- Options listed without default values
- No working example — reader can't tell what a valid config actually looks like

## Edge Cases
- Project with configuration entirely via a single file, no env vars — acceptable, Configuration Files subsection alone satisfies the requirement
- Secrets/credentials among the config options — name the variable and its purpose without exposing example secret values

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Configuration options listed with defaults (table form) |
| C2 | mandatory | 0 or 30 | Valid values stated per option |
| C3 | recommended | 0 or 30 | Working example provided |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.83,
  "severity": "error",
  "evidence": { "section_id": 14, "paragraph_index": 0, "excerpt": "The config file is in YAML. You can set environment variables too." },
  "message": "Configuration lists no actual options, defaults, or valid values."
}
```
