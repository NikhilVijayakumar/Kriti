# Problem — Generation Template

> **Domain:** vision
> **Section:** problem
> **Source:** `documentation-standards/01-vision-standards.md` §Problem
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Problem section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / problem_framing | Problem's description of pain must inspire Philosophy's framing of the problem space |

## Template

```markdown
[Description of the real-world pain or gap the product addresses]
[Concrete example illustrating the problem in context]
[Quantified impact where possible — cost, time, frequency]
```

## Examples

**Correct:**
> Teams that need to consolidate data from multiple sources spend hours each week on manual copying and pasting between spreadsheets. A mid-size operations team reports losing 12 hours per week to data reconciliation tasks, leading to delayed reports and costly errors.

**Incorrect:**
> Teams struggle with data silos. DataSync solves this by using scheduled Python scripts and a Redis cache layer to automatically merge CSV files.
> *Why wrong: Mixes solution details (technology, mechanism) into the Problem section. The Problem section should describe pain, not how the product addresses it.*

## Writing Guidance

- **Tone:** concrete
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Use specific, quantifiable examples of the pain; describe the problem from the user's perspective; include the cost of inaction
- **Don't:** Mention the product name or any solution approach; describe the problem in abstract or theoretical terms; include technical error messages or stack traces

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Purpose

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
