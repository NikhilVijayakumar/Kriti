# Verify a Section Profile

You are given one Section Profile and the Section Map that owns it. Check the
profile's field shape and rule well-formedness, resolve its references, and
produce a verdict plus findings.

## Checks

1. **Field presence** — `writing_objective`, `knowledge_goal`, and
   `reader_goal` are present; `required_inputs`, `expected_outputs`,
   `subsections`, `completion`, and `review` are structurally valid (correct
   types, non-empty where required).
2. **Rule shape** — every `validation.rules` entry carries `id`, `condition`,
   `message`, `severity`, `weight`, `mandatory`, and `evidence`. A rule
   missing any of these is a finding.
3. **Reference resolution** — every rule's target section and evidence
   reference resolves inside the owning map. A dangling reference is a
   finding with the reference as evidence.
4. **Map agreement** — the profile corresponds to a section the map actually
   declares (same id and domain).

## Finding shape

```json
{
  "id": "PROFILE-RULE-001",
  "condition": "every validation rule carries id/condition/message/severity/weight/mandatory/evidence",
  "message": "rule 'r7' of profile 'vision-overview' is missing 'evidence'",
  "severity": "error",
  "weight": 1.0,
  "mandatory": true,
  "evidence": "profile.validation.rules[6] lacks the evidence field",
  "kind": "defect"
}
```

`kind` is `defect` for malformed declarations and `gap` when a referenced
target legitimately does not exist yet. If everything holds, return
`verdict: "pass"` and `findings: []`.

## Rules

- Verify the declaration, never the quality of documents written from the
  profile.
- Do not fix the profile; report findings with the exact field as evidence.
- Do not name a specific repository or Domain System.
