# Guiding Principles — Generation Template

> **Domain:** vision
> **Section:** guiding_principles
> **Source:** `documentation-standards/01-vision-standards.md` §Guiding Principles
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Guiding Principles section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / guiding_principles | Guiding principles must inspire Philosophy's guiding_principles section — same values, Vision-level framing |

## Template

```markdown
[Introductory paragraph explaining that these principles guide all downstream decisions]

## [Principle 1]

[One-sentence statement of the principle and its rationale]

## [Principle 2]

[One-sentence statement of the principle and its rationale]

## [Principle 3]

[One-sentence statement of the principle and its rationale]
```

## Examples

**Correct:**
> **Fail Safely** — When a connection to an external system fails, the product preserves existing data and retries automatically rather than losing work.
> **Show, Don't Assume** — Every automated action should be visible to the user so they can verify correctness.

**Incorrect:**
> **Use Kubernetes** — The product should always be deployed on Kubernetes for orchestration.
> **TypeScript Everywhere** — All frontend and backend code must use TypeScript.
> *Why wrong: States technology mandates rather than enduring principles. Principles should survive technology changes and guide decisions regardless of implementation stack.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Phrase each principle as a decision rule that applies across technologies; include a one-sentence rationale for each; ensure principles are testable against real decisions
- **Don't:** Name programming languages, frameworks, or cloud providers; write principles that are only true for one implementation; list more than five principles

**Required subsections:** 3-5 principles
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Philosophy

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
