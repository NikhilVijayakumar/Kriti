# Data Flow — Generation Template

> **Domain:** architecture
> **Section:** data_flow
> **Source:** `documentation-standards/05-architecture-standards.md` §Data Flow
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Data Flow section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / runtime_behavior | Data Flow must be consistent with what Feature Technical Design describes for runtime behavior |

## Template

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

## Examples

**Correct:**
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

**Incorrect:**
> Data flows through a PostgreSQL table called `raw_events` with columns `id`, `payload`, `created_at`. The Transform Engine runs a SQL query `SELECT * FROM raw_events WHERE processed = false`, deserializes the JSONB payload using `JSON.parse()`, and inserts into `canonical_records` via an ORM bulk insert.
> *Why wrong: describes database schemas, SQL queries, and code-level operations — these are implementation details, not architectural data flow.*

## Writing Guidance

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

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
