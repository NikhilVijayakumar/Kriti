# Domain Relationships (Python Hackathon)

## Purpose
This document maps the cross-domain dependencies for the Python Hackathon standard. It serves as the human-readable counterpart to `plan/core/tiers.yaml`.

## Traceability Chain

```text
Tier 1                  Tier 2                                  Tier 3                          Tier 4

Infrastructure ─ guides ─> Engineering ── requires ──────────────> Testing ── validates ───────> Runtime
   │                            ▲                                    ▲                             ▲
   │                            │                                    │                             │
Security ─────── guides ────────┤                                    │                             │
   │                            │                                    │                             │
Team Workflow ── guides ────────┘                                    │                             │
                                                                     │                             │
Documentation ── informs ───────> Engineering                        │                             │
                                                                     │                             │
Data Quality ─── informs ───────> MLOps ── requires ─> Infrastructure│                             │
                                                                     │                             │
AI Explanations ── validates ───> Runtime ─────────────────────────┴─────────────────────────────┘
```

## All Declared Relationships

| From | Relationship | To | Mandatory |
|------|--------------|-----|-----------|
| Infrastructure | guides | Engineering | Yes |
| Security | guides | Engineering | Yes |
| Team Workflow | guides | Engineering | Yes |
| Engineering | requires | Testing | Yes |
| Testing | validates | Runtime | Yes |
| Documentation | informs | Engineering | No |
| MLOps | requires | Infrastructure | Yes |
| Data Quality | informs | MLOps | No |
| AI Explanations | validates | Runtime | No |

## Authoring Order
The filenames in `documentation-standards/` (01-10) align with the audit execution order, establishing a predictable sequence regardless of the hierarchical tier.
