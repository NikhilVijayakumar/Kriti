# Dependencies — Generation Template

> **Domain:** external-context
> **Section:** dependencies
> **Source:** `documentation-standards/08-external-context-standards.md` §Dependencies
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate the Dependencies section for an External Context document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `informs` | engineering / build_standards | Dependencies must distinguish runtime from build-time requirements for engineering setup |
| `informs` | feature_technical / communication_paths | Dependencies must surface companion systems that affect integration availability |

## Template

```markdown
## Dependencies

[1 paragraph: overview of transitive requirements the external system itself needs to function]

### Runtime Dependencies

| Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
|-----------|---------|-------------|------------------------|--------|
| [Name] | [what it provides] | [critical/nice-to-have] | [what fails] | [where documented] |

### Build-Time Dependencies

| Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
|-----------|---------|-------------|------------------------|--------|
| [Name] | [what it provides] | [critical/nice-to-have] | [what fails] | [where documented] |
```

## Examples

**Correct:**
> The external platform requires a running message broker as a runtime dependency — without it, webhook delivery fails silently. It also requires a valid TLS certificate for all inbound connections. At build time, the platform's CLI tool must be installed for schema validation.
>
> ### Runtime Dependencies
> | Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
> |-----------|---------|-------------|------------------------|--------|
> | Message broker | Webhook delivery | Critical | Webhooks fail silently | Platform documentation §6.2 |
> | TLS certificate | Inbound connections | Critical | All connections rejected | Platform security requirements |
>
> ### Build-Time Dependencies
> | Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
> |-----------|---------|-------------|------------------------|--------|
> | Platform CLI | Schema validation | Nice-to-have | Validation skipped at build time | Platform developer guide |

**Incorrect:**
> This project depends on Express.js for HTTP routing, Mongoose for database access, and Jest for testing.
> *Why wrong: These are internal project dependencies (package.json entries), not transitive dependencies of the external system. The Dependencies section describes what the external dependency itself requires.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Distinguish runtime from build-time dependencies explicitly; note criticality level for each transitive dependency; cross-reference other External Context documents when a transitive dependency is itself documented; include ALL subsections as part of this one section
- **Don't:** List this repository's package.json or requirements.txt entries; include development tooling or test frameworks; omit companion systems that the integration silently depends on; treat subsections as standalone sections

**Minimum content:** 1 subsection
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** other External Context documents for transitive dependencies

**Required subsections:** none
**Optional subsections:** Runtime Dependencies, Build-Time Dependencies

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
