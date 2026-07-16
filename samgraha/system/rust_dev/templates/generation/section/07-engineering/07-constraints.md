# Constraints — Generation Template

> **Domain:** engineering
> **Section:** constraints
> **Source:** `documentation-standards/07-engineering-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate the Constraints section for an Engineering document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / constraints | Engineering Constraints must derive from architecture constraints |
| `constrains` | feature-technical / runtime_constraints | Engineering Constraints bound feature-technical runtime constraints |

## Template

```markdown
## Constraints

> [metadata block]

[1–2 paragraphs explaining non-functional requirements and engineering limitations, categorized by type (performance, security, compliance), each with source attribution and verifiability]

### Performance Constraints

| Constraint | Threshold | Source | Verifiability |
|-----------|-----------|--------|---------------|
| [Constraint name] | [specific value] | [where it comes from] | [how to verify] |

### Security Constraints

| Constraint | Requirement | Source | Verifiability |
|-----------|-------------|--------|---------------|
| [Constraint name] | [specific requirement] | [where it comes from] | [how to verify] |

### Compliance Constraints

[Optional: regulatory, organizational policy requirements]
```

## Examples

**Correct:**
> ### Performance Constraints
> | Constraint | Threshold | Source | Verifiability |
> |-----------|-----------|--------|---------------|
> | API response time | ≤200ms at p95 | Architecture Section 4.3 | Load testing |

**Incorrect:**
> The application should be fast and secure. We follow industry best practices.
> *Why wrong: Not verifiable, no specific thresholds, no source attribution, and no categorization by type — making it impossible to audit.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Categorize every constraint by type (performance, security, compliance); cite the source of each constraint (Architecture section, External Context); make every constraint verifiable with specific thresholds.
- **Don't:** State vague requirements like "the application should be fast"; omit source attribution for constraints; list constraints without categorization or verification criteria.

**Required subsections:** none
**Optional subsections:** Performance Constraints, Security Constraints, Compliance Constraints
**Required diagrams:** none
**Required cross-references:** Architecture(05), External Context

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
