# Purpose Audit

This section details the Purpose Audit.

## Version
1.0.0

## Engineering Intent
Every engineering artifact must carry an explicit, discoverable purpose statement. Purpose defines why the artifact exists, what problem it solves, and the context in which it is valid.

## Audit Objectives
- Every module, service, and configuration has a declared purpose
- Purpose statements are specific and not generic boilerplate
- Purpose distinguishes intent from implementation
- Purposes are discoverable via documentation or code annotations
- No zombie artifacts (code that runs but serves no documented purpose)

## Expected Quality
- Each top-level module has a purpose comment or docstring
- Configuration keys include rationale for non-obvious defaults
- Deprecated artifacts have explicit sunset purpose
- Purpose is stable across refactors (survives implementation changes)

## Red Flags
- Generic purpose statements ("utility functions")
- Missing purpose on entry points or public APIs
- Copy-pasted purpose across unrelated modules
- Purpose contradicts actual behavior
- Artifacts that exist but no purpose can be stated

## Edge Cases
- Framework boilerplate with implicit purpose (scaffolding)
- Generated code with auto-declared purpose
- Dead code purpose that outlives the code
- Monolithic files serving multiple undocumented purposes

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Every public module has a purpose statement |
| C2 | mandatory | 0 or 30 | Purpose is specific to the module's behavior |
| C3 | recommended | 0 or 20 | No purpose contradicts actual behavior |
| C4 | recommended | 0 or 20 | Deprecated artifacts carry sunset purpose |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 17, "paragraph_index": 3, "excerpt": "Module auth/service.py lacks a purpose statement." },
  "message": "Module auth/service.py: purpose statement missing."
}
```
