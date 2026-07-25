# Performance Considerations — Generation Template

> **Domain:** feature-technical
> **Section:** performance_considerations
> **Source:** `documentation-standards/10-feature-technical-standards.md` §Performance Considerations
> **Relationships:** `audit/deterministic/document/10-feature-technical-relationships.yaml`

Generate the Performance Considerations section for a Feature Technical Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / operational_readiness | Performance expectations must align with Architecture operational readiness |
| `derives_from` | feature-technical / runtime_constraints | Performance must be consistent with Runtime Constraints |

## Template

```markdown
## Performance Considerations

### [Performance Expectation Name]
- **Throughput:** [throughput requirement]
- **Latency constraint:** [latency expectation]
- **Resource limitation:** [resource boundary]
```

## Examples

**Correct:**
> **Performance Expectation: Search Response**
> - Throughput: The search component must support concurrent queries from multiple client components without degrading response times
> - Latency constraint: Search results must be available to the UI component within the time expected for interactive use
> - Resource limitation: Search indexing must not consume more than the resource allocation defined in Architecture runtime boundaries

**Incorrect:**
> Elasticsearch query must complete in under 200ms. Node.js event loop must not be blocked for more than 50ms.
> *Why wrong: specifies technology-specific benchmarks rather than architectural performance expectations.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State performance expectations as architectural constraints traceable to Feature Specification; define throughput, latency, and resource expectations at the system level
- **Don't:** Provide specific latency numbers or benchmarks; name profiling tools or caching libraries

**Minimum content:** 1 paragraph + performance list
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Feature Specification, Architecture(05) performance patterns

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
