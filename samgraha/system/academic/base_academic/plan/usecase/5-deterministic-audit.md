# Use-case 5 — Deterministic Audit

**Depends on**: `assemble-paper-structure` (per domain — each domain must
have an `academic_narratives` row before its deterministic audit runs)

**Script**: `deterministic-audit.py` (det, per-domain single step)

**Inputs**:
- Each domain's latest `academic_narratives` draft
- `calculation/deterministic/{domain}.yaml` rule files

**Action**: Run deterministic mechanical checks against each domain's draft.
Cheap fail-fast before semantic scoring — deterministic FAIL short-circuits
semantic for that domain.

**Completion criteria** (checked by verify script):
- Every domain has a PASS deterministic verdict:
  `SELECT verdict FROM academic_deterministic_findings WHERE paper_id=? AND domain_id=?` = `PASS`
  for all domains

**Verify script**: `script/verify/uc5_det_audit.py --paper-id <id>`

**Rule**: Runs after assemble-paper-structure. Per-domain single-step
expanded at runtime. Re-runnable.
