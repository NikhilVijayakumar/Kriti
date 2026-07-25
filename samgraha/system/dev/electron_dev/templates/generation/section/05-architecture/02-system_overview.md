# System Overview — Generation Template

> **Domain:** architecture
> **Section:** system_overview
> **Source:** `documentation-standards/05-architecture-standards.md` §System Overview
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the System Overview section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | System Overview must be consistent with the Feature document's Purpose |

## Template

```markdown
## System Overview

### Overview
[1-2 paragraphs: system purpose, primary capabilities, high-level approach]

### Structural Approach
[1 paragraph: how the system is organized at the top level]

### Diagram
[High-level component or system context diagram]
```

## Examples

**Correct:**
> DataSync is a distributed data synchronization platform that coordinates data exchange between enterprise systems. It provides reliable, ordered delivery of data changes across heterogeneous datastores, supporting both real-time and batch synchronization modes. The system is organized into an ingestion layer, a transformation engine, and a distribution layer, each with distinct ownership and scaling characteristics.

**Incorrect:**
> DataSync uses Apache Kafka 3.4 with Spring Boot 3.1 for event streaming, PostgreSQL 15 for metadata storage, and Redis 7 for caching. The backend runs on AWS EKS with Kubernetes 1.27.
> *Why wrong: names specific library versions, frameworks, and cloud infrastructure — this is Engineering detail, not architectural overview.*

## Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** Open with the system's purpose in one sentence; describe capabilities before structure; use a diagram to anchor the overview
- **Don't:** Name specific libraries or frameworks; describe component internals; assume the reader knows the codebase

**Required subsections:** Overview, Diagram
**Optional subsections:** Structural Approach, Key Capabilities
**Required diagrams:** system context or component overview diagram
**Required cross-references:** Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
