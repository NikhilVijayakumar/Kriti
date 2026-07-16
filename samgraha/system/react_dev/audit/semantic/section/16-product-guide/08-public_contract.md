# Public Contract Audit

This section details the Public Contract Audit.

## Version
1.0.0

## Engineering Intent
Public Contract is the exhaustive, tabular reference for every input, output, flag, config key, and error condition a user can hit — with types, defaults, and required/optional status. It exists as the ground truth a user checks instead of reading source code.

## Audit Objectives
- Inputs (CLI flags, config keys, or API parameters) documented with type, default, required/optional status
- Outputs documented with type and description
- Error conditions listed with cause and resolution
- At least one of CLI Interface/Inputs is present, plus Error Conditions (both required)

## Expected Quality
- Presented as tables, not prose descriptions of flags
- Every input has a default stated (or explicitly marked as having none)
- Every listed error has both a cause and a concrete resolution, not just the error text

## Red Flags
- Flags/inputs described in prose instead of a table with type/default/required columns
- Required subsections missing entirely (no Error Conditions, or neither CLI Interface nor Inputs present)
- Error conditions listed without a resolution — reader hits the error with no path forward
- Contract doesn't match the actual current interface (stale flags, missing new ones)

## Edge Cases
- Interface with many rarely-used flags — acceptable to group advanced/rarely-used ones separately, but all still need type/default/required
- Breaking changes between versions — should be reflected in the contract as of the current version, with migration notes elsewhere if needed

## Scoring Criteria

| ID | Weight | Score | Description |
|---|---|---|---|
| C1 | mandatory | 0 or 30 | Inputs (CLI/config/API) documented in table form with type, default, required |
| C2 | mandatory | 0 or 30 | Error Conditions present with cause and resolution |
| C3 | mandatory | 0 or 20 | Outputs documented with type and description |
| C4 | recommended | 0 or 20 | Contract matches the actual current interface (no stale/missing entries) |

Score = sum of passed criterion scores, capped at 100.
Mandatory criterion failure = ERROR. Recommended = WARNING.

## Output Schema
```json
{
  "criterion_id": "C2",
  "passed": false,
  "confidence": 0.88,
  "severity": "error",
  "evidence": { "section_id": 62, "paragraph_index": 2, "excerpt": "| `ERR_INVALID_CONFIG` | Config file malformed |  |" },
  "message": "Error condition listed with no resolution — reader has no path forward on this error."
}
```
