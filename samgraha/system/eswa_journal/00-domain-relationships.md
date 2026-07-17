```yaml
domain: eswa_journal
type: domain-relationships
tiers:
  - tier: 1
    domains: [problem_definition, related_work]
  - tier: 2
    domains: [methodology]
  - tier: 3
    domains: [experimental_setup, results, implications, limitations]
  - tier: 4
    domains: [introduction, abstract, conclusion, references]
relationships:
  - from: problem_definition
    to: methodology
    type: requires
    mandatory: true
  - from: related_work
    to: problem_definition
    type: guides
    mandatory: true
  - from: methodology
    to: experimental_setup
    type: requires
    mandatory: true
  - from: experimental_setup
    to: results
    type: validates
    mandatory: true
  - from: results
    to: implications
    type: informs
    mandatory: false
  - from: results
    to: conclusion
    type: guides
    mandatory: true
  - from: methodology
    to: abstract
    type: informs
    mandatory: true
  - from: results
    to: abstract
    type: informs
    mandatory: true
relationship_types:
  - guides
  - requires
  - validates
  - informs
```

# Domain Relationships (ESWA Paper)

## Purpose
This document maps the cross-section dependencies for the ESWA Paper standards. It ensures that the paper's logical flow adheres to the rigorous standards expected by a Q1 journal.

## Traceability Chain

```text
Tier 1                  Tier 2                  Tier 3                      Tier 4

Related Work ── guides ─> Problem Def ── req ─> Methodology ── req ───────> Experimental Setup
                                                   │                               │
                                                   │                               ▼
                                                   │                            Results ── guides ─> Conclusion
                                                   │                               │
                                                   │                               ├─ informs ─> Implications
                                                   │                               │
                                                   │                               └─ informs ─> Abstract
                                                   └─ informs ───────────────────────────────┘
```

## All Declared Relationships

| From | Relationship | To | Mandatory |
|------|--------------|-----|-----------|
| Problem Definition | requires | Methodology | Yes |
| Related Work | guides | Problem Definition | Yes |
| Methodology | requires | Experimental Setup | Yes |
| Experimental Setup | validates | Results | Yes |
| Results | informs | Implications | No |
| Results | guides | Conclusion | Yes |
| Methodology | informs | Abstract | Yes |
| Results | informs | Abstract | Yes |

## Authoring Order
The filenames in `documentation-standards/` (01-11) align with the audit execution order, establishing a predictable sequence regardless of the hierarchical tier.
