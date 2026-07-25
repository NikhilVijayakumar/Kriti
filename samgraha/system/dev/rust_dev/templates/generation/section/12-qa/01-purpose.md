# Purpose — Generation Template

> **Domain:** qa
> **Section:** purpose
> **Source:** `documentation-standards/12-qa-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Purpose section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Verification scope must serve the Vision's quality goals |

## Template

```markdown
## Purpose

> **Verification scope:** [how features are verified against specifications]

> **Testing philosophy:** [the overall approach to verification — risk-driven, measurable, traceable]

> **Upstream relationships:** Feature(04) defines what to test; Architecture(05) defines boundaries; Feature Technical(10) defines runtime behavior to validate; Security(03) defines security requirements.

> **Downstream relationships:** Implementation(13) is what gets tested; Build(14) validates test results in pipeline.
```

> **Generation note:** The standard's Purpose section defines QA as a concept (meta-level) AND serves as the template for system-specific documents. When generating for a specific system, fill this template with *that system's* verification scope and philosophy. The meta-level language belongs in the standard itself, not in a generated document.

## Examples

**Correct (system-specific):**
> **Verification scope:** This document defines how Project Nova verifies that features meet their specifications. It derives verification targets from Feature requirements, Architecture boundaries, and Security constraints.
>
> **Testing philosophy:** The testing strategy is risk-driven — test types are prioritized by impact, and every test type traces back to the upstream documentation it validates.
>
> **Upstream relationships:** Feature(04) defines what to test; Architecture(05) defines system boundaries; Security(03) defines security test requirements.
>
> **Downstream relationships:** Implementation(13) is what gets tested against this QA contract; Build(14) validates test results in the CI/CD pipeline.

**Incorrect:**
> This document defines the QA process for Project Nova. The team uses Jest for unit tests and Cypress for E2E tests.
> *Why wrong: defines tool choices rather than verification scope and philosophy.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the verification scope before any implementation details; reference every upstream document by its standard number and role; use measurable language
- **Don't:** Mention specific test frameworks, tools, or CI/CD systems; describe what the team "does" — describe what the document "defines"

**Minimum content:** 2 paragraphs
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Feature(04), Architecture(05), Feature Technical(10), Security(03), Implementation(13)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
