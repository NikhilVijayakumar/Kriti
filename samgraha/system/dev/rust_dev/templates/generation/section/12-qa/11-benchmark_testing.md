# Benchmark Testing — Generation Template

> **Domain:** qa
> **Section:** benchmark_testing
> **Source:** `documentation-standards/12-qa-standards.md` §BenchmarkTesting
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Benchmark Testing section for a Qa document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / crate_implementation | Benchmarks the performance-critical paths |

> *Structural rules: `audit/deterministic/section/12-qa/11-benchmark_testing.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
Performance-critical paths are continuously benchmarked to prevent regressions.

[Describe the use of tools like `criterion` to measure latency, throughput, and memory allocations.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The core routing algorithm is benchmarked using `criterion`. Regressions greater than 5% will fail the CI pipeline.

**Incorrect:**
> We will test if it feels fast.
> *Why wrong: Benchmarking must be statistical and automated.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** systems engineer
- **Do:** Specify statistical measurement tools.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
