# Purpose — Generation Template

> **Domain:** build
> **Section:** purpose
> **Source:** `documentation-standards/14-build-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Purpose section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Build Purpose must align with Vision(01) purpose and scope |

## Template

```markdown
## Purpose

The Build Plan defines how verified code is packaged, validated, and delivered as shippable artifacts. It covers [scope], establishes what Build does not define by referencing [out-of-scope standards], and describes Build's role in the documentation ecosystem.

> **Scope:**
> - **Covers:** [artifact generation, quality gates, security validation, versioning]
> - **Does not cover:** [implementation details, QA testing strategy, deployment procedures]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* build purpose: what the pipeline packages, what gates apply, and which standards handle what Build does not. The meta-level "This document defines the standard for Build Plans..." language belongs in the standard itself, not in a generated document.

## Examples

**Correct:**
> The Build Plan defines how verified code is packaged, validated, and delivered as shippable artifacts. It covers artifact generation, quality gates, security validation, and versioning — but does not define what to build (Implementation(13)), how to test it (QA(12)), or how to deploy it.

**Incorrect:**
> The Build Plan defines the CI/CD pipeline configuration, deployment procedures, and release management workflows.
> *Why wrong: Deployment procedures and release management are out of scope for Build(14) — they belong to their own documentation standards.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State scope boundaries as definitive exclusions; explicitly name which standards handle what Build does not cover; define Build's role in the documentation ecosystem
- **Don't:** Conflate Build with CI/CD implementation details; describe deployment or release procedures; leave scope boundaries ambiguous

**Minimum content:** 3 paragraphs
**Length guidance:** moderate
**Required diagrams:** flowchart
**Required cross-references:** Implementation(13), QA(12), Engineering(07)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
