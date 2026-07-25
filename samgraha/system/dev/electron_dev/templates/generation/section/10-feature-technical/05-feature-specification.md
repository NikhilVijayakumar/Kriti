# Feature Specification — Generation Template

> **Domain:** feature-technical
> **Section:** feature_specification
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Feature Specification
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Feature Specification section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Must reference exactly one Feature Specification by name |
| `derives_from` | design / workflow | Scope must align with the feature's workflow scope |

## Template

```markdown
## Feature Specification

This Feature Technical Design realizes the **[Feature Name]** Feature Specification. The scope of this design covers [scope summary] — matching the Feature's defined scope. No additional features are addressed in this document.
```

## Examples

**Correct:**
> This Feature Technical Design realizes the **User Authentication** Feature Specification. The scope of this design covers credential validation, session management, and secure access — matching the Feature's defined scope. No additional features are addressed in this document.

**Incorrect:**
> This Feature Technical Design realizes the **User Authentication** Feature Specification, which requires: users must be able to log in with email and password, reset passwords via email link, enable two-factor authentication, and manage session devices.
> *Why wrong: duplicates Feature Specification content rather than referencing the Feature by name and confirming scope alignment.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Reference the Feature by exact name; confirm scope alignment; state that no additional features are addressed
- **Don't:** Duplicate Feature requirements, acceptance criteria, or user stories; paraphrase Feature content; list multiple Feature Specifications

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Feature(04)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
