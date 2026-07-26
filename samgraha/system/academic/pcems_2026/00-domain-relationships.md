```yaml
domain: pcems_2026
type: domain-relationships
tiers:
  - tier: 1
    domains: [introduction]
  - tier: 2
    domains: [methodology]
  - tier: 3
    domains: [findings]
  - tier: 4
    domains: [conclusion, title-and-metadata]
  - tier: 5
    domains: [references]
relationships:
  - from: introduction
    to: methodology
    type: guides
    mandatory: true
  - from: methodology
    to: findings
    type: validates
    mandatory: true
  - from: findings
    to: conclusion
    type: guides
    mandatory: true
  - from: methodology
    to: title-and-metadata
    type: informs
    mandatory: false
  - from: findings
    to: title-and-metadata
    type: informs
    mandatory: false
relationship_types:
  - guides
  - requires
  - validates
  - informs
```

# Domain Relationships (PCEMS 2026)

## Purpose
This document maps the cross-section dependencies for the PCEMS 2026 standards. It ensures that the paper's logical flow adheres to the conference's structural requirements.

## Traceability Chain

```text
Tier 1                  Tier 2                  Tier 3                  Tier 4                      Tier 5

Introduction ─ guides ─> Methodology ─ validates ─> Findings ─ guides ─> Conclusion
                                                    │                   │
                                                    │                   └─ informs ─> Title & Metadata
                                                    └─ informs ──────────────────────┘
                                                                                          References
```

## All Declared Relationships

| From | Relationship | To | Mandatory |
|------|--------------|-----|-----------|
| Introduction | guides | Methodology | Yes |
| Methodology | validates | Findings | Yes |
| Findings | guides | Conclusion | Yes |
| Methodology | informs | Title & Metadata | No |
| Findings | informs | Title & Metadata | No |

## Authoring Order

The tier structure dictates the generation order:
1. **Tier 1**: Introduction (establishes the gap)
2. **Tier 2**: Methodology (responds to the gap)
3. **Tier 3**: Findings (executes the methodology)
4. **Tier 4**: Conclusion + Title & Metadata (synthesized from everything above)
5. **Tier 5**: References (accumulated citations)

Cross-cutting domains (novelty, gaps, mathematics, tables, figures) sit
outside the tier system entirely — see `_master-schema.yaml`'s
`cross_cutting:` list. `novelty`/`gaps`/`mathematics` run as an analysis
pass *before* tier 1; `tables`/`figures` are consulted at audit time
inside tier 3.
