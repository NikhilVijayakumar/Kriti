# Academic-Class Relationship Types

Shared vocabulary for cross-domain dependency edges in `plan/core/tiers.yaml`
and `00-domain-relationships.md`. Both `pcems_2026` and `eswa_journal` use
this exact closed set — confirmed by reading both systems' relationship files.

## Allowed Types

| Type | Meaning | Direction |
|------|---------|-----------|
| `guides` | Source domain's output shapes/ constrains the target domain's content | source → target |
| `requires` | Target cannot be generated/audited until source completes | source → target |
| `validates` | Source domain's audit criteria verify target domain's output | source → target |
| `informs` | Source domain provides context/evidence that enriches target | source → target |

## Constraints

- Every relationship edge must use one of these four types exactly.
- No additional types are permitted at the academic-class level.
- Concrete systems may add edges using these types but cannot extend the
  vocabulary itself (unlike `rust_dev` which adds `inspires`, `derives`,
  `soft_aligns_with`, `references` — those are dev-class only).
- The `mandatory` boolean on each edge controls whether the relationship
  is a hard gate (tier_gate blocks) or soft advisory.

## Usage in `00-domain-relationships.md`

```yaml
relationships:
  - { from: introduction, type: guides, to: methodology, mandatory: true }
  - { from: methodology, type: validates, to: findings, mandatory: true }
```

## Usage in `plan/core/tiers.yaml`

Same structure — the `relationships:` list uses the same `{from, type, to}`
shape. The `relationship_types:` list at the bottom must always be exactly:

```yaml
relationship_types: [guides, requires, validates, informs]
```
