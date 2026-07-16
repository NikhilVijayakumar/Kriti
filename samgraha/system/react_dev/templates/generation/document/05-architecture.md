# Architecture Document — Generation Template

> **Domain:** architecture
> **Source standard:** `documentation-standards/05-architecture-standards.md`
> **Coherence source:** `audit/semantic/document/05-architecture.md`
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate a complete Architecture document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Root intent, why Architecture Documentation exists, scope boundaries |
| 2 | System Overview | `system_overview` | ✓ | System purpose, primary capabilities, structural approach; entry point for new contributors |
| 3 | Component Model | `component_model` | ✓ | Component names, responsibilities, ownership boundaries, relationships |
| 4 | Communication | `communication_paths` | ✓ | Communication paths, interaction patterns, contracts between components |
| 5 | Data Flow | `data_flow` | ✓ | Data entry/exit points, movement paths, ownership boundaries, transformations |
| 6 | Security | `security_considerations` | ✓ | Trust boundaries, threat model, access control model, data protection requirements |
| 7 | Rationale | `rationale` | | Decision reasoning, alternatives considered, trade-offs, rejection criteria |
| 8 | Constraints | `constraints` | | Non-functional requirements, platform limitations, organizational rules with source attribution |
| 9 | Traceability | `traceability` | | Tier model, derivation chain, downstream standards, non-contradiction rule |
| 10 | Operational Readiness | `operational_readiness` | | Deployment automation, rollback, runbooks, scaling, disaster recovery |
| 11 | Observability | `observability` | | Telemetry backend, correlation ID strategy, log aggregation, metrics retention |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/05-architecture.md` Engineering Intent.

Component Model, Data Flow, and Communication Paths must describe the same system without contradicting each other. Specifically:

- Every data ownership claim in Data Flow must trace to a component defined in Component Model
- Every communication path in Communication must connect components that Component Model defines as adjacent/related
- Component names must be used identically everywhere they appear across all sections
- The collection as a whole must read as one architecture, not several independent descriptions

If any section would introduce a component, data path, or communication path not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **Architectural purpose:** [1-2 sentences: why this architecture exists, what problems it solves, what qualities it optimizes for]

> **Scope boundaries:**
> - **In scope:** [architectural concerns this document covers]
> - **Out of scope:** [architectural concerns explicitly excluded, with reason]

> **Primary goals:** [ranked list of architectural priorities — e.g. scalability > maintainability > cost]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* architectural purpose: why this architecture exists, what problems it solves, and what qualities it prioritizes. The meta-level "This document defines the standard for Architecture Documentation..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> **Architectural purpose:** This architecture supports real-time inventory tracking across 50 warehouses with sub-second update latency. The primary problem is maintaining consistency across distributed inventory states during concurrent modifications from warehouse operators and e-commerce orders.
>
> **Scope boundaries:**
> - **In scope:** Inventory state synchronization, conflict resolution, warehouse-side data ownership
> - **Out of scope:** E-commerce order processing (covered by Feature Design), warehouse physical layout
>
> **Primary goals:** 1. Consistency under concurrent access, 2. Sub-second propagation, 3. Offline resilience per warehouse

**Incorrect example:**
> Architecture Documentation covers the microservices layout, the React component tree, the PostgreSQL schema, and the Kubernetes deployment manifests used by the system.
> *Why wrong: names specific technologies and implementation artifacts instead of stating the architectural purpose and scope boundaries.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the architectural purpose specific to this system; define scope boundaries explicitly (in-scope vs. out-of-scope); rank primary goals to guide trade-off decisions; derive from Vision document's Purpose and Philosophy's guiding principles
- **Don't:** Use generic mission statements; copy purpose from project charter or README; include goals without architectural impact; leave scope boundaries implicit

---

### 2. System Overview

**Template:**

```markdown
## System Overview

### Overview
[1-2 paragraphs: system purpose, primary capabilities, high-level approach]

### Structural Approach
[1 paragraph: how the system is organized at the top level]

### Diagram
[High-level component or system context diagram]
```

**Correct example:**
> DataSync is a distributed data synchronization platform that coordinates data exchange between enterprise systems. It provides reliable, ordered delivery of data changes across heterogeneous datastores, supporting both real-time and batch synchronization modes. The system is organized into an ingestion layer, a transformation engine, and a distribution layer, each with distinct ownership and scaling characteristics.

**Incorrect example:**
> DataSync uses Apache Kafka 3.4 with Spring Boot 3.1 for event streaming, PostgreSQL 15 for metadata storage, and Redis 7 for caching. The backend runs on AWS EKS with Kubernetes 1.27.
> *Why wrong: names specific library versions, frameworks, and cloud infrastructure — this is Engineering detail, not architectural overview.*

**Writing guidance:**
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

---

### 3. Component Model

**Template:**

```markdown
## Component Model

### Components

#### [Component Name]
- **Responsibility:** [what this component owns]
- **Ownership:** [data/processes owned]
- **Interfaces:** [how other components interact with it]

#### [Component Name]
- **Responsibility:** [what this component owns]
- **Ownership:** [data/processes owned]
- **Interfaces:** [how other components interact with it]

### Component Diagram
[Diagram showing all components and their relationships]
```

**Correct example:**
> **Ingestion Service**
> - **Responsibility:** Accepts data changes from external systems and validates their structure before passing them downstream.
> - **Ownership:** Raw incoming change events, ingestion queues.
> - **Interfaces:** Exposes a submission endpoint; publishes validated events to the Transform Engine.
>
> **Transform Engine**
> - **Responsibility:** Applies mapping rules to convert incoming data formats into the canonical system model.
> - **Ownership:** Mapping rules, transformation state, intermediate representations.
> - **Interfaces:** Consumes validated events from Ingestion; publishes canonical records to Distribution.

**Incorrect example:**
> The Ingestion Service is implemented as a Node.js 20 Express app with 4 REST endpoints (`/api/v1/ingest`, `/api/v1/batch`, `/api/v1/status`, `/api/v1/health`). It uses Bull queues backed by Redis and calls `validateSchema()` from the shared `@datasync/validation` package.
> *Why wrong: describes implementation details (runtime, endpoints, package names, function signatures) instead of responsibility and ownership boundaries.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- - **Do:** State each component's single responsibility; define ownership boundaries explicitly; include a component relationship diagram
- **Don't:** Describe class hierarchies or function signatures; conflate responsibility with implementation; list components without defining boundaries

**Required subsections:** Components (with one entry per component), Component Diagram
**Optional subsections:** Component Relationships, Boundary Definitions
**Required diagrams:** component relationship diagram
**Required cross-references:** System Overview, Communication, Data Flow

---

### 4. Communication

**Template:**

```markdown
## Communication

### Communication Paths
[For each communication path: source, destination, pattern (sync/async/event), contract]

### Interaction Patterns
[Description of communication patterns used across the system]

### Communication Diagram
[Sequence or flow diagram showing inter-component communication]
```

**Correct example:**
> **Ingestion → Transform Engine**
> - **Pattern:** Asynchronous, event-driven.
> - **Contract:** Ingestion publishes a validated event; Transform Engine acknowledges receipt and processes independently. Events are idempotent and ordered within a single source.
>
> **Transform Engine → Distribution**
> - **Pattern:** Asynchronous, queue-based.
> - **Contract:** Transform publishes canonical records with a unique identifier. Distribution guarantees at-least-once delivery and deduplicates on the identifier.

**Incorrect example:**
> Ingestion calls Transform via HTTP POST to `http://transform:8080/process` with a JSON body. It uses Axios with a 5-second timeout and retries 3 times with exponential backoff. Responses are validated against the OpenAPI schema in `transform-api.yaml`.
> *Why wrong: specifies network protocols, library choices, timeout values, and implementation-level retry logic — all of which belong in Engineering, not Architecture.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Define a contract for every component-to-component path; classify each interaction pattern (sync, async, event-driven); include a sequence diagram
- **Don't:** Specify network protocols or transport details; describe retry logic or timeout values; conflate communication paths with data paths

**Required subsections:** Communication Paths, Communication Diagram
**Optional subsections:** Interaction Patterns, Contract Definitions
**Required diagrams:** sequence diagram of primary communication paths
**Required cross-references:** Component Model, Data Flow

---

### 5. Data Flow

**Template:**

```markdown
## Data Flow

### Data Paths
[For each major data path: entry point, transformations, ownership boundaries, exit point]

### Processing Semantics
[For each data path: sync vs. async, batch vs. stream, ordering guarantees]

### Data Ownership
[Table or list mapping data entities to owning components]

### Data Flow Diagram
[Flowchart showing data movement through the system]
```

**Correct example:**
> **Inbound Data Path**
> - **Entry point:** External system submits data changes.
> - **Processing semantics:** Asynchronous, event-driven. Events are ordered within a single source; cross-source ordering is not guaranteed.
> - **Transformations:** Schema validation and format normalization.
> - **Ownership boundary:** Ingestion Service owns raw events until transformation completes.
> - **Exit point:** Canonical records delivered to Distribution.
>
> **Data Ownership**
> | Data Entity | Owning Component |
> |---|---|
> | Raw incoming events | Ingestion Service |
> | Canonical records | Transform Engine |
> | Delivery confirmations | Distribution Service |

**Incorrect example:**
> Data flows through a PostgreSQL table called `raw_events` with columns `id`, `payload`, `created_at`. The Transform Engine runs a SQL query `SELECT * FROM raw_events WHERE processed = false`, deserializes the JSONB payload using `JSON.parse()`, and inserts into `canonical_records` via an ORM bulk insert.
> *Why wrong: describes database schemas, SQL queries, and code-level operations — these are implementation details, not architectural data flow.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Trace every major data path from entry to exit; distinguish synchronous vs. asynchronous flows and batch vs. stream processing; assign ownership to a specific component at each boundary; include a data flow diagram
- **Don't:** Describe database schemas or SQL queries; reference ORM methods or serialization code; document data paths that bypass component boundaries; leave processing semantics implicit

**Required subsections:** Data Paths, Data Flow Diagram
**Optional subsections:** Data Ownership, Data Transformations
**Required diagrams:** data flow diagram covering all major paths
**Required cross-references:** Component Model, Communication, Security

---

### 6. Security

**Template:**

```markdown
## Security

### Trust Boundaries
[Description of where trust changes — external/internal, component-to-component]

### Threat Model
[Key threats, attack vectors, and mitigations at the architectural level]

### Security Controls
[Architectural security measures — access control model, data protection requirements]
```

**Correct example:**
> **Trust Boundaries**
> - **External → Ingestion:** Untrusted external systems submit data; Ingestion validates all inputs before internal processing.
> - **Ingestion → Transform:** Trusted boundary — both are internal components communicating over an internal network.
>
> **Threat Model**
> - **Spoofing:** External systems may impersonate legitimate data sources. Mitigation: authenticated submission with signed payloads.
> - **Data tampering:** Malicious payloads may attempt to exploit downstream processing. Mitigation: schema validation at the Ingestion boundary.

**Incorrect example:**
> We use JWT tokens signed with RS256 via the `jsonwebtoken` library. Passwords are hashed with bcrypt (12 rounds). The API gateway uses Kong 3.4 with rate limiting of 100 req/min. All traffic is encrypted with TLS 1.3.
> *Why wrong: specifies concrete libraries, library versions, configuration values, and protocol versions — these are Engineering implementation details, not architectural security controls.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** Define every trust boundary with source and destination; document the threat model before controls; tie each control to a specific threat
- **Don't:** Name specific security libraries or libraries' configuration values; describe implementation of encryption or authentication; omit a threat that has no documented mitigation

**Required subsections:** Trust Boundaries, Threat Model
**Optional subsections:** Security Controls, Access Control Model
**Required diagrams:** trust boundary diagram
**Required cross-references:** Component Model, Data Flow, Philosophy(02)

---

### 7. Rationale

**Template:**

```markdown
## Rationale

### [Decision Name]
- **Context:** [what prompted this decision]
- **Decision:** [what was decided]
- **Alternatives Considered:** [what else was evaluated]
- **Rejection Reason:** [why alternatives were rejected]
- **Architectural Goal:** [which goal this serves]
```

**Correct example:**
> **Event-Driven Ingestion**
> - **Context:** Multiple external systems submit data at unpredictable rates and volumes.
> - **Decision:** Ingestion publishes events asynchronously rather than processing synchronously.
> - **Alternatives Considered:** Synchronous request/response ingestion with backpressure.
> - **Rejection Reason:** Synchronous processing would couple external system availability to ingestion availability, violating the reliability pillar.
> - **Architectural Goal:** Resilient Connections.

**Incorrect example:**
> We chose Kafka over RabbitMQ because it has better throughput benchmarks and our team already knows the Java client library.
> *Why wrong: justifies a specific technology choice by implementation-level benchmarks and team familiarity — that belongs in Engineering's rationale, not Architecture's.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Record the context that prompted each decision; name the alternatives that were actually considered; tie every decision back to an architectural goal or pillar
- **Don't:** Justify decisions by technology benchmarks, licensing, or team familiarity; record decisions without a rejected alternative; let rationale entries go stale once a decision is superseded

---

### 8. Constraints

**Template:**

```markdown
## Constraints

### Hard Constraints
[Constraints that cannot be violated — with source and reason for each]

### Soft Constraints
[Preferences and guidelines that should be followed unless justified]

### Platform Constraints
[Hardware, OS, or runtime constraints that shape architecture]
```

**Correct example:**
> **Hard Constraints**
> - **Offline-first operation** (source: Platform Pillars) — the system must remain functional with no network connection; no component may assume live connectivity.
> - **Single-writer data ownership** (source: External Context) — the upstream partner system requires exactly one writer per record to avoid conflict resolution on their side.
>
> **Soft Constraints**
> - Prefer components that can be tested in isolation, unless a hard constraint makes isolation impractical.

**Incorrect example:**
> The system must use Rust 1.75+ and target a minimum of 4GB RAM.
> *Why wrong: states a language version and hardware minimum as if they were architectural constraints, without a source or architectural reason.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Attribute every constraint to its source (External Context, Platform Pillars, organizational rule); separate hard constraints from soft preferences explicitly; state the consequence of violating a hard constraint
- **Don't:** List a constraint without a source; mix implementation-level limits (language versions, dependency pins) into architectural constraints; present preferences as if they were immovable

**Required subsections:** Hard Constraints
**Optional subsections:** Soft Constraints, Platform Constraints
**Required diagrams:** none
**Required cross-references:** External Context, Platform Pillars(01)

---

### 9. Traceability

**Template:**

```markdown
## Traceability

### Derivation Chain
[Diagram showing Architecture's position in the documentation tier model]

### Downstream Impact
[List of standards that Architecture constrains or feeds into]

### Non-Contradiction Rule
[Statement that no downstream document may contradict Architecture]
```

**Correct example:**
> Tier 2: Architecture (System Overview, Component Model, Security)
>     ├──→ Tier 3: Feature Technical Design
>     └──→ Tier 5: Engineering (soft, non-mandatory)
>
> **Non-contradiction rule:** No downstream document may describe a component boundary, ownership assignment, or communication path that contradicts this Architecture. When a Feature Technical Design needs a boundary Architecture doesn't define, Architecture is updated first.

**Incorrect example:**
> Architecture traces to the `src/components/` directory and the deployment YAML files.
> *Why wrong: references source code and deployment configuration instead of the documentation hierarchy.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Show Architecture's tier position and every standard it feeds; state the non-contradiction rule explicitly; keep the diagram in sync when new standards derive from Architecture
- **Don't:** Reference source code, deployment artifacts, or CI/CD configuration; omit downstream standards from the diagram; leave the non-contradiction rule implicit

**Required subsections:** Derivation Chain, Non-Contradiction Rule
**Optional subsections:** Downstream Impact
**Required diagrams:** tier model diagram
**Required cross-references:** Vision(01), Feature Technical Design(10), Engineering(07)

---

### 10. Operational Readiness

**Template:**

```markdown
## Operational Readiness

### Deployment Automation
[CI/CD pipeline stages, gating criteria for production promotion]

### Rollback Procedure
[Automated vs. manual rollback, time target, tested status]

### Runbooks
[Top N known failure modes with linked runbooks and on-call routing]

### Scaling
[Horizontal and vertical scaling triggers with thresholds]

### Disaster Recovery
[RTO and RPO targets, derived from business requirements]

### Change Management
[Approval process, freeze windows, production promotion gates]
```

**Correct example:**
> **Deployment Automation**
> - Pipeline: Build → Integration Tests → Staging → Production
> - Gating: All integration tests pass; staging smoke test passes; one human approval for production
>
> **Rollback Procedure**
> - Automated rollback to previous version on health check failure
> - Rollback time target: < 5 minutes
> - Tested: Yes, weekly during game day exercises
>
> **Runbooks**
> - **Data ingestion stall:** Check ingestion queue depth; if > 10k for 5 min, restart ingestion service. [Runbook: ingestion-stall.md]
>
> **Disaster Recovery**
> - RPO: 1 hour (snapshot-based backup)
> - RTO: 4 hours (full re-deployment from last snapshot)

**Incorrect example:**
> We deploy using Kubernetes. Rollback is handled on a case-by-case basis by the on-call engineer. Scaling is manual.
> *Why wrong: lacks specific procedures, time targets, and tested status.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** operator
- **Do:** Document deployment pipeline stages with gating criteria; define rollback procedure with time target; link runbooks to specific failure modes; specify scaling triggers with thresholds; state RTO/RPO targets
- **Don't:** Describe deployment tools without procedures; state rollback as aspirational; omit time targets; leave scaling triggers vague

**Required subsections:** Deployment Automation, Rollback Procedure
**Optional subsections:** Runbooks, Scaling, Disaster Recovery, Change Management
**Required diagrams:** none
**Required cross-references:** Component Model, Engineering(07)

---

### 11. Observability

**Template:**

```markdown
## Observability

### Telemetry Backend
[Identified backend with justification relative to scale and cost]

### Correlation ID Strategy
[How correlation IDs are generated, propagated through async boundaries, and used for request tracing]

### Log Aggregation Pipeline
[Collection, storage, retention period, access controls]

### Metrics Retention
[Retention and downsampling policy, SLO monitoring architecture]

### On-Call and Alerting
[Alert routing, on-call escalation, SLO breach notification]
```

**Correct example:**
> **Telemetry Backend**
> - Backend: OpenTelemetry Collector → ClickHouse for traces, Prometheus for metrics
> - Justification: ClickHouse handles high-cardinality trace data at scale
>
> **Correlation ID Strategy**
> - Generated: UUID v4 at system entry point
> - Propagated: X-Correlation-ID header across HTTP; embedded in event envelope for async paths
>
> **Log Aggregation Pipeline**
> - Collection: Fluentd sidecar per component
> - Storage: ClickHouse, 90-day hot retention, 1-year cold (S3)

**Incorrect example:**
> We use logs and metrics. Correlation IDs are nice to have. Retention is handled by the platform team.
> *Why wrong: lacks specific infrastructure, retention periods, and correlation strategy.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** operator
- **Do:** Identify the telemetry backend with justification; document correlation ID generation and propagation across all async boundaries; define log retention and access controls; specify SLO monitoring architecture
- **Don't:** Name tools without justification; leave correlation ID propagation implicit; omit retention periods

**Required subsections:** Telemetry Backend, Correlation ID Strategy
**Optional subsections:** Log Aggregation Pipeline, Metrics Retention, On-Call and Alerting
**Required diagrams:** none
**Required cross-references:** Component Model, Communication, Engineering(07)

## Output Contract

Output a single complete markdown document containing all 11 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified (as markdown image references or Mermaid code blocks)
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
