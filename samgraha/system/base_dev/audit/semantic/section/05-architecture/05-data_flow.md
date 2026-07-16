# Data Flow Audit

This section details the Data Flow Audit.

## Version
1.0.0

## Engineering Intent
Data flow describes how data moves through the system: sources, transformations, storage, and consumption endpoints. It must capture data schemas, flow direction, processing semantics (sync/async, batch/stream), and data lineage. Good data flow documentation enables impact analysis and data governance.

## Audit Objectives
- All major data flows are identified and documented
- Data sources and sinks are clearly specified
- Flow direction and processing semantics are defined
- Data transformations and their locations are described
- Data storage boundaries and retention are addressed
- Cross-component data contracts are documented

## Expected Quality
- Flows are traceable from origin to consumption
- Data schemas or formats are referenced
- Synchronous vs. asynchronous flows are distinguished
- Batch and stream processing are clearly separated
- Data volume and velocity characteristics are noted

## Red Flags
- Missing data sources or sinks
- Undocumented data transformations
- Data flows that contradict component interfaces
- No distinction between command, query, and event flows
- Data retention or deletion not mentioned
- Flows described at implementation detail level (SQL queries, API parameters)

## Edge Cases
- Event-driven systems with implicit data flows (event carriers)
- Data flows that cross trust boundaries or compliance zones
- External data sources with unknown schemas
- System with no persistent data (pure processing pipeline)

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | All major data flows are identified with sources and sinks |
| C2 | mandatory | 0 or 30 | Processing semantics (sync/async, batch/stream) are defined |
| C3 | recommended | 0 or 30 | Data transformations and storage boundaries are documented |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": false,
  "confidence": 0.75,
  "severity": "error",
  "evidence": { "section_id": 20, "paragraph_index": 3, "excerpt": "Order events flow from Order Service to Invoice Service via Kafka topic orders." },
  "message": "Flow identified but data schema and retention policy not documented."
}
```
