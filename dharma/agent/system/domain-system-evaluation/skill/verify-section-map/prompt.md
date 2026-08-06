# Verify a Section Map

You are given one domain's Section Map. Check it against the map invariants
and produce a verdict plus findings.

## Invariants to check

1. **Unique ids** — `sections[]` ids are unique within the map.
2. **Order** — section `order` values are non-decreasing; no gaps in the
   intended sequence.
3. **Single root** — exactly one root section at the map's base level
   (level 1), and every other section has exactly one resolvable `parent_id`
   link.
4. **Resolvable profile references** — every section's `profile:` reference
   resolves to a real Section Profile of the same id and domain.
5. **Validation-block agreement** — the map-level `validation` block
   (hierarchy, ordering, structure, required) does not contradict the actual
   section set: no field in the validation block asserts something the rows
   violate.

## Finding shape

Every finding carries the audit-style fields the domain's profiles already
use:

```json
{
  "id": "MAP-ORDER-001",
  "condition": "section order is non-decreasing",
  "message": "section 'x3' has order 5 after section 'x2' at order 5",
  "severity": "error",
  "weight": 1.0,
  "mandatory": true,
  "evidence": "map.sections[2].order == 5; map.sections[1].order == 5",
  "kind": "defect"
}
```

`kind` is `defect` when the Domain System's declaration is wrong and `gap`
when the map references something that legitimately does not exist yet. If
every invariant holds, return `verdict: "pass"` and `findings: []`.

## Rules

- Verify the declaration, not the content quality of any produced document.
- Do not fix what you find; report it with the exact row as evidence.
- Do not name a specific repository or Domain System.
