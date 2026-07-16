# Traceability — Generation Template

> **Domain:** feature-technical
> **Section:** traceability
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Traceability
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Traceability section for a Feature Technical Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | feature / purpose | Feature Technical Design traceability must assert one-to-one mapping with exactly one Feature Specification |
| `traceable_to` | engineering / build_standards | Feature Technical Design must trace to Engineering build standards for implementation guidance |
| `traceable_to` | architecture / purpose | Feature Technical Design must trace to Architecture for shared architectural principles |

## Template

```markdown
Feature Technical Design remains traceable.

```text
Vision
    │
    ├─────────────────────────────────┐
    ↓                                 ↓
Feature                         Architecture
    ↓                           (technology decisions,
Design (optional)               platform constraints)
    ↓                                 │
Feature Design (optional)             │
    │                                 │
    └──────────────────────────────→ Feature Technical Design
                                      ↓
                                  Engineering
                                      ↓
                                  Implementation
```

Feature Specification and Architecture Documentation are required inputs. Feature Design is an optional input considered only where UX decisions influence architectural realization.

Every Feature Technical Design should trace directly to exactly one Feature Specification.
```

## Examples

**Correct:**
> Vision(01) → Feature: Authentication → Feature Technical Design: Authentication → Engineering: Authentication → Implementation: Authentication
>
> This Feature Technical Design traces to exactly one Feature Specification (Authentication). Architecture(05) security boundaries and External Context(08) identity provider constraints are applied as inputs.

**Incorrect:**
> Feature Technical Design: Authentication derives from the authentication API implementation in the source code.
> *Why wrong: Traceability must flow from Feature Specification and Architecture, not from source code. The derivation chain starts at Vision, not at implementation.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** mixed
- **Audience:** architect
- **Do:** Show the full derivation chain from Vision through Feature to Implementation; assert one-to-one mapping with Feature Specification; reference Architecture and External Context as inputs; include a flowchart
- **Don't:** Trace to source code or implementation artifacts; omit upstream or downstream standards; leave the one-to-one mapping unstated

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** flowchart showing derivation chain
**Required cross-references:** Vision(01), Feature(04), Architecture(05), Engineering(07), External Context(08)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
