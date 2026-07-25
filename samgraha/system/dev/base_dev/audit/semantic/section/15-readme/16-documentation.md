# Documentation Audit

This section details the Documentation Audit.

## Version
1.0.0

## Engineering Intent
Documentation sections explain architecture, configuration, API, or usage of the project. They must be correct, navigable, and maintainable.

## Audit Objectives
- Section has a clear purpose (one topic per section)
- Content is accurate (reflects current code behavior)
- Internal and external links resolve
- Examples are runnable or verified
- Consistent terminology with other docs

## Expected Quality
- Heading hierarchy is logical (no skipped levels)
- Code blocks have language annotations
- API docs specify inputs, outputs, and errors
- Configuration docs list all keys, types, defaults
- TOC or cross-references for long sections

## Red Flags
- Outdated screenshots or version numbers
- Links to files that no longer exist
- Copy-paste errors from other docs
- Missing or wrong code examples
- Jargon without definition or glossary link

## Edge Cases
- Empty section (heading with no content)
- Auto-generated docs mixed with hand-written
- Single massive page vs. split topics
- Deprecated features not marked as deprecated

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Accurate and reflects current code |
| C2 | mandatory | 0 or 30 | All links resolve |
| C3 | recommended | 0 or 20 | Code examples are runnable |
| C4 | recommended | 0 or 20 | Consistent terminology used |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 5, "paragraph_index": 2, "excerpt": "The config file supports env, apiKey, and timeout." },
  "message": "Documentation accurate and reflects current code behavior."
}
```
