# Purpose — Generation Template

> **Domain:** implementation
> **Section:** purpose
> **Source:** `documentation-standards/13-implementation-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Purpose section for an Implementation Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Implementation Purpose must align with and derive from the Vision document's Purpose |
| `derives_from` | feature / purpose | Implementation Purpose must reference what Feature(04) defines to build |

## Template

```markdown
## Purpose

This Implementation Plan documents the as-built record for [feature/system name]. It defines [scope], establishes boundaries via [out of scope], and traces implementation decisions back to [upstream documents].

> **Upstream sources:**
> - Feature(04): [what this plan builds from]
> - Architecture(05): [structural constraints applied]
> - Engineering(07): [code standards followed]
> - Security(03): [security requirements addressed]

> **Out of scope:**
> - [domain or concern not covered, with reason]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* implementation purpose: what was built, what boundaries apply, and which upstream documents drove the decisions. The meta-level "This document defines the standard for Implementation Plans..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct:**
> This Implementation Plan documents the as-built record for the payment processing feature. It covers the payment flow from checkout to confirmation, excludes currency conversion and subscription billing, and traces every implementation decision back to Feature(04) payment requirements and Security(03) PCI-DSS constraints.

**Incorrect:**
> This section describes the purpose of the project and how we plan to build it.
> *Why wrong: Describes project intent rather than recording what was actually built; confuses Implementation Purpose with Vision or Feature documentation.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** State the feature name and scope explicitly; link every relationship to its upstream document number; define boundaries by listing what is excluded
- **Don't:** Use generic mission statements; describe project vision or strategy; conflate purpose with goals or success criteria; leave scope boundaries implicit

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Feature(04), Architecture(05), Engineering(07), Security(03)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
