# Obfuscation & Optimization Audit

This section details the Obfuscation & Optimization Audit.

## Version
1.0.0

## Engineering Intent
Obfuscation & Optimization defines which build-time transformations (minification, obfuscation, tree-shaking) apply, under what configuration, and their cost to debuggability. It exists so a production stack trace problem isn't a mystery.

## Audit Objectives
- Transformations specified per build type (dev/staging/prod)
- Configuration referenced (tool, settings, or profile used)
- Impact on debuggability stated (source maps, symbol retention, etc.)

## Expected Quality
- Distinguishes which transformations run in which build type — not one blanket policy for all
- Names the actual tool/mechanism, not just "we optimize the build"
- Explicitly addresses how debugging a production issue is still possible (or states the tradeoff if it isn't)

## Red Flags
- "We minify and obfuscate for production" with no configuration or debuggability discussion
- No distinction between build types — same transformations implied everywhere
- Debuggability impact omitted entirely, leaving an operational gap undocumented

## Edge Cases
- Projects with no obfuscation step at all (e.g. open-source, server-side only) — acceptable to state that explicitly with the reason, rather than leaving the section silent
- Third-party bundled dependencies excluded from obfuscation — note the exclusion and why

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Transformations specified per build type |
| C2 | mandatory | 0 or 30 | Configuration/tooling referenced |
| C3 | recommended | 0 or 30 | Debuggability impact addressed |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C3",
  "passed": false,
  "confidence": 0.78,
  "severity": "warning",
  "evidence": { "section_id": 24, "paragraph_index": 0, "excerpt": "Production builds are minified and obfuscated." },
  "message": "Obfuscation & Optimization doesn't address debuggability impact of the production transform."
}
```
