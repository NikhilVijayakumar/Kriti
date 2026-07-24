# Use-case 5 — Deterministic Audit

**Script**: `deterministic_audit.py` (deterministic, single step per domain)

**Inputs**:
- Current draft for the domain
- `calculation/deterministic/{domain}.yaml` rules (mechanical checks)

**Action**: Run deterministic mechanical checks before semantic scoring.
Cheap fail-fast: missing required mermaid diagram, under reference-count
floor, banned AI-fingerprint phrases — these don't need a model call.

**Completion criteria**:
- One `academic_deterministic_findings` row per domain
- PASS/FAIL verdict + per-check findings JSON

**Rule**: Runs before semantic-audit. Deterministic FAIL short-circuits
semantic for that domain (saves model cost). Domain clears only when
both deterministic AND semantic PASS in the same pass.
