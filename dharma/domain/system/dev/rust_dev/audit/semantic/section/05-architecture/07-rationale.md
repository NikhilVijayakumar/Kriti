# Rationale Audit

This section details the Rationale Audit.

## Version
1.0.0

## Engineering Intent
Rationale preserves the reasoning behind significant architectural decisions — what was decided, what else was considered, and why the alternative was rejected. Unlike Constraints (what must hold), Rationale explains why the architecture looks the way it does, tied to an architectural goal or pillar rather than a technology preference.

## Audit Objectives
- Each entry names a specific decision, not a general design philosophy
- Context precedes the decision — the prompting situation is stated before the resolution
- At least one alternative that was genuinely considered is recorded
- Rejection reason is architectural (coupling, boundaries, resilience), not implementation-level (benchmarks, licensing, team familiarity)
- Every decision ties back to a named architectural goal or pillar

## Expected Quality
- Decisions are named memorably (e.g. "Event-Driven Ingestion"), not "Decision 1"
- Context states the forcing condition, not just background
- Alternatives Considered names a real option, not a strawman
- Rejection Reason references an architectural property the alternative would have violated
- Architectural Goal links to a pillar or principle stated elsewhere in the document set, not invented ad hoc

## Red Flags
- Decisions justified by technology benchmarks, licensing cost, or team familiarity instead of architectural properties
- No alternative recorded — reads as if only one option was ever considered
- Rationale entries that restate what the architecture does (duplicates System Overview/Component Model) instead of why it was chosen
- Stale entries describing a decision that has since been superseded, with no update or removal
- Rejection Reason absent or generic ("it was worse")

## Edge Cases
- Greenfield decisions with no rejected alternative because none was seriously evaluated (acceptable if stated explicitly, e.g. "no viable alternative identified at the time")
- A decision later reversed — the old entry should be marked superseded, not silently deleted or left contradicting current architecture
- Decisions inherited from a prior system/migration, where the original context is external to this repository

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | Each entry has Context, Decision, Alternatives Considered, and Rejection Reason |
| C2 | mandatory | 0 or 30 | Rejection Reason is architectural, not implementation/technology-level |
| C3 | recommended | 0 or 30 | Every decision ties to a named architectural goal or pillar |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.88,
  "severity": "error",
  "evidence": { "section_id": 41, "paragraph_index": 2, "excerpt": "We chose Kafka over RabbitMQ because it has better throughput benchmarks." },
  "message": "Rejection reason is a technology benchmark, not an architectural property — belongs in Engineering rationale, not Architecture."
}
```
