# Load Testing — Generation Template

> **Domain:** qa
> **Section:** load_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Load Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Load Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / system_overview | Load profiles must reflect the system's expected user load |
| `derives_from` | engineering / testing_standards | Performance targets must align with Engineering standards |

## Template

```markdown
## Load Testing

### Load Profiles

| Profile | Concurrent Users | Duration | Expected Response Time | Error Rate Threshold |
|---------|-----------------|----------|----------------------|---------------------|
| Baseline | [X] | [X min] | [X ms] | [X%] |
| Target | [X] | [X min] | [X ms] | [X%] |
| Stress | [X] | [X min] | [X ms] | [X%] |

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time (p95) | [X ms] | [Tool] |
| Throughput | [X req/s] | [Tool] |
| Error rate | [X%] | [Tool] |
```

## Examples

**Correct:**
> ### Load Profiles
>
> | Profile | Concurrent Users | Duration | Expected Response Time | Error Rate Threshold |
> |---------|-----------------|----------|----------------------|---------------------|
> | Baseline | 50 | 10 min | 200 ms | 0.1% |
> | Target | 200 | 30 min | 500 ms | 0.5% |
> | Stress | 500 | 15 min | 1000 ms | 2.0% |
>
> ### Performance Targets
>
> | Metric | Target | Measurement |
> |--------|--------|-------------|
> | Response time (p95) | 500 ms | Load testing tool metrics |
> | Throughput | 100 req/s | Load testing tool metrics |
> | Error rate | < 0.5% | Application logs |

**Incorrect:**
> The app should be fast. We expect it to handle many users without slowing down.
> *Why wrong: load testing requires specific numerical profiles and measurable performance targets.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Define load profiles with numeric concurrent-user counts and durations; set performance targets with specific thresholds; name the measurement tool
- **Don't:** Use qualitative load descriptions; define targets without units; skip the baseline profile

**Required subsections:** Load Profiles table, Performance Targets table
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Architecture(05), Engineering(07), Feature(04)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
