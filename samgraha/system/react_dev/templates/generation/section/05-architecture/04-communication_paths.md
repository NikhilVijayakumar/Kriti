# Communication — Generation Template

> **Domain:** architecture
> **Section:** communication_paths
> **Source:** `documentation-standards/05-architecture-standards.md` §Communication
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Communication section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / communication_paths | Communication paths must be consistent with what Feature Technical Design describes for communication |

## Template

```markdown
## Communication

### Communication Paths
[For each communication path: source, destination, pattern (sync/async/event), contract]

### Interaction Patterns
[Description of communication patterns used across the system]

### Communication Diagram
[Sequence or flow diagram showing inter-component communication]
```

## Examples

**Correct:**
> **Ingestion → Transform Engine**
> - **Pattern:** Asynchronous, event-driven.
> - **Contract:** Ingestion publishes a validated event; Transform Engine acknowledges receipt and processes independently. Events are idempotent and ordered within a single source.
>
> **Transform Engine → Distribution**
> - **Pattern:** Asynchronous, queue-based.
> - **Contract:** Transform publishes canonical records with a unique identifier. Distribution guarantees at-least-once delivery and deduplicates on the identifier.

**Incorrect:**
> Ingestion calls Transform via HTTP POST to `http://transform:8080/process` with a JSON body. It uses Axios with a 5-second timeout and retries 3 times with exponential backoff. Responses are validated against the OpenAPI schema in `transform-api.yaml`.
> *Why wrong: specifies network protocols, library choices, timeout values, and implementation-level retry logic — all of which belong in Engineering, not Architecture.*

## Writing Guidance

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

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
