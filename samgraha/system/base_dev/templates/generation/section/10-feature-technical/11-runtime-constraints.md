# Runtime Constraints — Generation Template

> **Domain:** feature-technical
> **Section:** runtime_constraints
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Runtime Constraints
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Runtime Constraints section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / constraints | Runtime constraints must derive from Architecture operational constraints |
| `derives_from` | engineering / constraints | Runtime constraints must be consistent with Engineering constraints |

## Template

```markdown
## Runtime Constraints

### [Constraint Name] (source: [Architecture or External Context])
[How this constraint applies to this specific feature]
```

## Examples

**Correct:**
> **Constraint: Concurrency Limit** (source: Architecture runtime boundaries)
> The Order Processing Component must handle concurrent order submissions without data corruption. The architectural model limits concurrent processing to the resource allocation defined for this component class.

**Incorrect:**
> Use `java.util.concurrent.Semaphore` with permits=10. Configure Tomcat max threads to 200 in server.xml.
> *Why wrong: specifies implementation-level concurrency tools and server configuration rather than architectural operational constraints.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint as a clear operational limitation; cite the source from Architecture or External Context; explain how it applies to this feature
- **Don't:** Specify implementation tools, frameworks, or configuration files; provide performance benchmarks

**Minimum content:** 1 paragraph + constraint list
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Architecture(05) runtime boundaries, External Context(08)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
