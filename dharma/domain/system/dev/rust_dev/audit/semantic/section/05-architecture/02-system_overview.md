# System Overview Audit

This section details the System Overview Audit.

## Version
1.0.0

## Engineering Intent
The system overview provides a high-level description of the system and its environment. It establishes context for all other architecture sections by describing what the system does, its deployment context, key architectural style, and relationship to external systems. It is the entry point for understanding the architecture.

## Audit Objectives
- System purpose and primary responsibilities are described
- Deployment context and environment are characterized
- Architectural style or pattern is identified (microservices, layered, etc.)
- External system dependencies and integrations are listed
- Key architectural characteristics are introduced
- Diagram references or visual representations are included

## Expected Quality
- Overview is concise enough for a new team member to understand in 5 minutes
- Architectural style is named and justified (not implied)
- External systems are identified with integration direction
- Deployment boundaries (on-prem, cloud, hybrid) are stated
- Overview content is consistent with detailed sections

## Red Flags
- Overview is a copy of requirements or PRD
- No architectural style or pattern identified
- External system dependencies are missing
- Overview contradicts detailed sections
- Deployment context is absent (assumed but not stated)
- Overview is too detailed (reads like a design spec)

## Edge Cases
- System of systems with multiple architectural styles
- Legacy system with undocumented architecture (reverse-engineered overview)
- System with no external dependencies (fully self-contained)
- Multiple deployment targets with different architectural characteristics

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 40 | System purpose and architectural style are clearly described |
| C2 | mandatory | 0 or 30 | Deployment context and external dependencies are identified |
| C3 | recommended | 0 or 30 | Overview is consistent with detailed architecture sections |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C1",
  "passed": true,
  "confidence": 0.95,
  "severity": "error",
  "evidence": { "section_id": 1, "paragraph_index": 0, "excerpt": "Samgraha is a cloud-native document processing platform built on a microservices architecture deployed on Kubernetes." },
  "message": "Architectural style and purpose clearly stated in opening paragraph."
}
```
