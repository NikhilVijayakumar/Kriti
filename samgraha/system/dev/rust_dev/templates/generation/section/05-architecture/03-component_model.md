# Component Model — Generation Template

> **Domain:** architecture
> **Section:** component_model
> **Source:** `documentation-standards/05-architecture-standards.md` §Component Model
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Component Model section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / component_responsibilities | Component Model must define the components that Feature Technical Design's component responsibilities section references |

## Template

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

## Examples

**Correct:**
> **Ingestion Service**
> - **Responsibility:** Accepts data changes from external systems and validates their structure before passing them downstream.
> - **Ownership:** Raw incoming change events, ingestion queues.
> - **Interfaces:** Exposes a submission endpoint; publishes validated events to the Transform Engine.
>
> **Transform Engine**
> - **Responsibility:** Applies mapping rules to convert incoming data formats into the canonical system model.
> - **Ownership:** Mapping rules, transformation state, intermediate representations.
> - **Interfaces:** Consumes validated events from Ingestion; publishes canonical records to Distribution.

**Incorrect:**
> The Ingestion Service is implemented as a Node.js 20 Express app with 4 REST endpoints (`/api/v1/ingest`, `/api/v1/batch`, `/api/v1/status`, `/api/v1/health`). It uses Bull queues backed by Redis and calls `validateSchema()` from the shared `@datasync/validation` package.
> *Why wrong: describes implementation details (runtime, endpoints, package names, function signatures) instead of responsibility and ownership boundaries.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each component's single responsibility; define ownership boundaries explicitly; include a component relationship diagram
- **Don't:** Describe class hierarchies or function signatures; conflate responsibility with implementation; list components without defining boundaries

**Required subsections:** Components (with one entry per component), Component Diagram
**Optional subsections:** Component Relationships, Boundary Definitions
**Required diagrams:** component relationship diagram
**Required cross-references:** System Overview, Communication, Data Flow

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
